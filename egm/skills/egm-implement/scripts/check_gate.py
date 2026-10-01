#!/usr/bin/env python3
"""Check the /egm-implement entry gate for one design doc. Read-only.

Derives the slug from the design doc's filename, finds the EGM state
directory docs/egm/<slug>/, and reads GOLDFISH.md for two values:

  readiness          from the latest round entry: must be `ready`
  human_review_gate  from GOLDFISH.md's header (the frontmatter, or the
                     key: value lines above the first `## ` heading): must
                     be `passed` or `skipped-solo`. Round entries carry a
                     copy for the record; if the latest copy disagrees with
                     the header, the header wins and the output says so.
                     With no header field, the latest round's copy is used.

The script never writes a ledger and never changes a gate. Only a human
moves the gate; this only reports where it stands.

Usage:
  python3 check_gate.py docs/designs/<slug>.md
  python3 check_gate.py                    # if the design-doc folder holds one doc
  python3 check_gate.py --root ~/proj --json docs/designs/<slug>.md

Exit codes:
  0  GO              readiness is ready and the gate is passed or skipped-solo
  1  BLOCKED         something is missing or still pending; the output says what
  2  usage error     no doc given and none (or several) found, or bad flags
  3  CHECK-BY-HAND   a value is not one of the expected words; a person must read it
"""

import argparse
import glob
import json
import os
import re
import sys

GATE_VALUES = {"pending", "passed", "skipped-solo"}
READINESS_VALUES = {"not-yet", "ready"}
SOLO_WARNING = "Human review gate was skipped (solo mode). Proceeding under your sole judgment."

# Matches both `human_review_gate: passed` and `- **readiness:** ready` at the
# start of a line. Prose that merely mentions a field name mid-sentence is ignored.
FIELD_LINE = re.compile(r"^\s*(?:[-*]\s+)?[*`]*(human_review_gate|readiness)\s*:\s*[*`]*\s*(.*)$", re.M)
ROUND_HEADING = re.compile(r"^#{2,3}\s+Round\s+(\d+)\b", re.M | re.I)


def first_word(raw):
    """Normalize a ledger value: drop markdown emphasis, keep the first word.
    `**not-yet** (round incomplete)` becomes `not-yet`."""
    cleaned = raw.replace("*", "").replace("`", "").strip().lower()
    return re.split(r"[\s,;(]+", cleaned, maxsplit=1)[0] if cleaned else ""


def split_header(text):
    """Return (header, body). The header is YAML frontmatter when the file
    starts with `---`; otherwise it is everything above the first `## `
    heading (the plain `key: value` block older ledgers use)."""
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            return text[3:end], text[end + 4:]
    first_section = re.search(r"^## ", text, re.M)
    if first_section:
        return text[:first_section.start()], text[first_section.start():]
    return "", text


def read_goldfish(path):
    """Pull the header gate, the latest round's gate and readiness, the
    latest round number, and the header's design_doc_path."""
    with open(path, encoding="utf-8") as ledger:
        text = ledger.read()
    front, body = split_header(text)
    # The header may be proper YAML or collapsed onto one line, so search it.
    header_gate = re.search(r"human_review_gate\s*:\s*[*`]*\s*([\w-]+)", front)
    header_doc = re.search(r"design_doc_path\s*:\s*[`]?([^\s`]+)", front)
    rounds = [int(n) for n in ROUND_HEADING.findall(body)]
    # The last occurrence in the body belongs to the latest round entry.
    latest = {}
    for name, raw in FIELD_LINE.findall(body):
        latest[name] = raw.strip()
    # Raw values are kept; judging them is the caller's job.
    return {
        "header_gate": header_gate.group(1).lower() if header_gate else None,
        "round_gate_raw": latest.get("human_review_gate"),
        "readiness_raw": latest.get("readiness"),
        "latest_round": max(rounds) if rounds else None,
        "header_doc": header_doc.group(1) if header_doc else None,
    }


def design_doc_dir(root):
    """The design-doc folder: CLAUDE.md's `design_doc_path:` if set (the
    same setting /elephant and /goldfish honor), else docs/designs/."""
    claude_md = os.path.join(root, "CLAUDE.md")
    if os.path.isfile(claude_md):
        with open(claude_md, encoding="utf-8") as config:
            setting = re.search(r"^\s*design_doc_path:\s*[`]?([^\s`]+)", config.read(), re.M)
        if setting:
            return setting.group(1)
    return os.path.join("docs", "designs")


def resolve_doc(root, given):
    """Return (doc_path, error). With no argument, accept the only doc in
    the design-doc folder and refuse to guess between several."""
    if given:
        return given, None
    folder = design_doc_dir(root)
    found = sorted(glob.glob(os.path.join(root, folder, "*.md")))
    if len(found) == 1:
        return os.path.relpath(found[0], root), None
    listing = "\n  ".join(os.path.relpath(f, root) for f in found) or "(none)"
    return None, "error: pass the design doc path. {}/ holds:\n  {}".format(folder, listing)


def judge_gate(info, report):
    """One gate verdict. The header is where a person records the gate;
    a round entry's copy only matters when the header has none."""
    round_gate = first_word(info["round_gate_raw"]) if info["round_gate_raw"] else None
    gate = info["header_gate"] or round_gate
    if not gate:
        report["blocked"].append("GOLDFISH.md has no human_review_gate field yet")
        return None
    # A value outside the three words means someone wrote prose there.
    if gate not in GATE_VALUES:
        report["unclear"].append("human_review_gate reads {!r}; expected pending, passed, or skipped-solo".format(gate))
        return None
    if info["header_gate"] and round_gate and round_gate != gate:
        report["warnings"].append("the latest round's copy says {}, the header says {}; the header is the gate, "
                                  "so update the round copy to match".format(round_gate, gate))
    # Only pending blocks; skipped-solo proceeds with a warning.
    if gate == "pending":
        report["blocked"].append("human_review_gate is pending: a reviewer records passed in GOLDFISH.md's header, "
                                 "or you record skipped-solo there yourself if you are working alone")
    elif gate == "skipped-solo":
        report["warnings"].append(SOLO_WARNING)
    return gate


def judge_readiness(info, report):
    """readiness comes from the latest round entry only."""
    raw = info["readiness_raw"]
    if raw is None:
        report["blocked"].append("GOLDFISH.md has no readiness field: no Goldfish round has finished")
        return None
    # Anything but the two words (say, "core ready, periphery not-yet")
    # is a judgment call the script must not make.
    value = first_word(raw)
    if value not in READINESS_VALUES:
        report["unclear"].append("latest readiness reads {!r}; expected ready or not-yet".format(raw))
        return None
    if value != "ready":
        report["blocked"].append("latest round says readiness: {}; run another /goldfish round".format(value))
    return value


def check(root, doc):
    """Run every check and return the report dict; never raises on a
    missing file, because a missing file is itself the answer."""
    slug = os.path.splitext(os.path.basename(doc))[0]
    state_dir = os.path.join("docs", "egm", slug)
    report = {"design_doc": doc, "slug": slug, "state_dir": state_dir,
              "blocked": [], "unclear": [], "warnings": [], "notes": []}
    if not os.path.isfile(os.path.join(root, doc)):
        report["blocked"].append("design doc {} does not exist".format(doc))
    # The state directory is created by /elephant; without it nothing ran.
    if not os.path.isdir(os.path.join(root, state_dir)):
        report["blocked"].append("{}/ does not exist: run /elephant and /goldfish first (or the doc's filename is not its EGM slug)".format(state_dir))
        return report
    # Neither file gates anything, but both change what happens next.
    for name, note in (("ELEPHANT.md", "exists: read it for orientation, not to re-derive the design"),
                       ("IMPLEMENT.md", "exists: you are resuming, so read it first")):
        if os.path.isfile(os.path.join(root, state_dir, name)):
            report["notes"].append("{} {}".format(name, note))
    # GOLDFISH.md is the one file the gate cannot do without.
    goldfish = os.path.join(root, state_dir, "GOLDFISH.md")
    if not os.path.isfile(goldfish):
        report["blocked"].append("{}/GOLDFISH.md does not exist: run /goldfish first".format(state_dir))
        return report
    # Everything below depends on what GOLDFISH.md says.
    info = read_goldfish(goldfish)
    report["latest_round"] = info["latest_round"]
    report["readiness"] = judge_readiness(info, report)
    report["human_review_gate"] = judge_gate(info, report)
    if info["header_doc"] and os.path.normpath(info["header_doc"]) != os.path.normpath(doc):
        report["warnings"].append("GOLDFISH.md names design_doc_path {}, not {}".format(info["header_doc"], doc))
    return report


def verdict_of(report):
    """BLOCKED beats CHECK-BY-HAND: a definite failure needs no human read."""
    if report["blocked"]:
        return "BLOCKED", 1
    if report["unclear"]:
        return "CHECK-BY-HAND", 3
    return "GO", 0


def main(argv=None):
    # Arguments only; an agent running this cannot answer interactive prompts.
    parser = argparse.ArgumentParser(description="Read-only check of the /egm-implement entry gate.")
    parser.add_argument("design_doc", nargs="?", help="path to the design doc (usually docs/designs/<slug>.md), relative to --root")
    parser.add_argument("--root", default=".", help="project root (default: current directory)")
    parser.add_argument("--json", action="store_true", help="print the report as JSON")
    args = parser.parse_args(argv)
    # Exit 2 is reserved for "I could not even tell which doc you meant".
    doc, error = resolve_doc(args.root, args.design_doc)
    if error:
        print(error, file=sys.stderr)
        return 2

    # The exit code carries the verdict so a caller can branch on it.
    report = check(args.root, doc)
    verdict, code = verdict_of(report)
    report["verdict"] = verdict
    if args.json:
        print(json.dumps(report, indent=2))
        return code
    # Plain text: the facts first, then every reason, then the verdict line.
    print("design doc:  {}\nstate dir:   {}/".format(report["design_doc"], report["state_dir"]))
    for key in ("latest_round", "readiness", "human_review_gate"):
        if key in report:
            print("{:<12} {}".format(key.replace("_", " ") + ":", report[key] if report[key] is not None else "?"))
    # Each reason gets its own line so none hides behind another.
    for key, label in (("blocked", "blocked"), ("unclear", "unclear"), ("warnings", "warning"), ("notes", "note")):
        for line in report[key]:
            print("{}: {}".format(label, line))
    print("verdict:     {}".format(verdict))
    return code


if __name__ == "__main__":
    sys.exit(main())
