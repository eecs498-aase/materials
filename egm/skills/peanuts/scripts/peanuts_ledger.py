#!/usr/bin/env python3
"""Plan, start, and read the PEANUTS.md ledger for /peanuts.

Subcommands:
  plan [ROOT]   List every in-scope directory bottom-up (deepest first, then
                by path) with its depth and kind (leaf, branch, root).
                Changes nothing.
  init [ROOT]   Write ROOT/PEANUTS.md with every in-scope directory set to
                `pending`. Refuses to touch an existing ledger, because the
                ledger holds human approvals.
  next [ROOT]   Read ROOT/PEANUTS.md and report the review queue, blocked
                directories, and which directories may be generated now under
                the hard gate. Changes nothing.

A directory is in scope when it holds a source file or has an in-scope
subdirectory. A leaf has no in-scope subdirectories. In a git repo the file
list comes from `git ls-files`, so .gitignore is respected; vendored and
generated trees (node_modules, vendor, dist, build, target, .venv, ...) are
always skipped.

How `next` decides what may be generated:
  - The current level is the deepest depth that still has a `pending` or
    `needs-human-review` row. Work happens one level at a time, deepest first.
  - If that level has rows awaiting review, the verdict is REVIEW-FIRST.
  - Otherwise a pending row at that level is eligible when every immediate
    in-scope child is `approved` or `rolled-up` (the hard gate). Leaves have
    no children, so pending leaves at the current level are always eligible.
  - An in-scope directory missing from the ledger counts as an unfinished
    child, and a table row that does not parse is a ledger problem.

Exit codes:
  0  report printed (or ledger written)
  1  `next` found ledger problems: an unparseable row, an unknown status, or
     a gate violation
  2  usage error: bad root, no ledger for `next`, or nothing in scope
"""

import argparse
import datetime
import json
import os
import re
import subprocess
import sys

STATUSES = ("pending", "needs-human-review", "approved", "rolled-up", "blocked")
DONE = {"approved", "rolled-up"}
SKIP_DIRS = {".git", "node_modules", "vendor", "third_party", "dist", "build",
             "target", ".venv", "venv", "__pycache__", ".tox", ".mypy_cache",
             ".next", "coverage"}
SOURCE_EXTS = {
    ".py", ".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs", ".vue", ".svelte",
    ".java", ".kt", ".kts", ".scala", ".go", ".rs", ".c", ".h", ".cc", ".cpp",
    ".hpp", ".cs", ".swift", ".m", ".mm", ".rb", ".php", ".pl", ".sh", ".bash",
    ".zsh", ".lua", ".r", ".sql", ".dart", ".ex", ".exs", ".erl", ".hs", ".ml",
    ".fs", ".clj", ".html", ".css", ".scss", ".proto", ".graphql", ".tf",
}
SOURCE_NAMES = {"Makefile", "Dockerfile", "Rakefile", "Justfile"}
LEDGER = "PEANUTS.md"
HEADER_ROW = re.compile(r"^\|\s*directory\s*\|", re.I)
SEPARATOR_ROW = re.compile(r"^\|[\s|:-]+\|\s*$")
ROW = re.compile(r"^\|\s*([^|]+?)\s*\|\s*(\d+)\s*\|\s*(\w+)\s*\|\s*([\w-]+)\s*\|([^|]*)\|([^|]*)\|\s*$")


def list_files(root):
    """Relative paths of candidate files. git decides what is ignored when
    the root is inside a repo; otherwise walk the tree ourselves."""
    try:
        out = subprocess.run(
            ["git", "-C", root, "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
            check=True, capture_output=True).stdout.decode("utf-8", "replace")
        return [p for p in out.split("\0") if p]
    except (OSError, subprocess.CalledProcessError):
        pass  # not a git repo, or no git: fall back to a plain walk
    # Hidden directories are skipped too: they are tooling, not source.
    found = []
    for here, dirs, names in os.walk(root):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith(".")]
        rel = os.path.relpath(here, root)
        found += [os.path.normpath(os.path.join(rel, n)) for n in names]
    return found


def is_source(path):
    """Code by extension or by a well-known build-file name. Docs, images,
    and data do not make a directory need a README."""
    name = os.path.basename(path)
    return name in SOURCE_NAMES or os.path.splitext(name)[1].lower() in SOURCE_EXTS


def parent_of(directory):
    """Parent directory in ledger notation, where the root is '.'."""
    head = os.path.dirname(directory)
    return head if head else "."


def depth_of(directory):
    """Path components below the root; the root itself is depth 0."""
    return 0 if directory == "." else directory.count("/") + 1


def scope(root, excludes):
    """Map each in-scope directory to its set of in-scope children."""
    in_scope = set()
    for path in list_files(root):
        parts = path.split("/")
        # Skip vendored trees even when someone committed them.
        if any(p in SKIP_DIRS for p in parts[:-1]) or not is_source(path):
            continue
        directory = "/".join(parts[:-1]) or "."
        if any(directory == e or directory.startswith(e + "/") for e in excludes):
            continue
        # Every ancestor of a source directory is in scope too (the hay).
        while True:
            in_scope.add(directory)
            if directory == ".":
                break
            directory = parent_of(directory)
    # Invert the parent links so each directory knows its in-scope children.
    children = {d: set() for d in in_scope}
    for directory in in_scope:
        if directory != ".":
            children[parent_of(directory)].add(directory)
    return children


def bottom_up(children):
    """Deepest first, then alphabetical: the order /peanuts walks."""
    return sorted(children, key=lambda d: (-depth_of(d), d))


def kind_of(directory, children):
    """leaf (peanuts), branch (hay), or root (the top-level map)."""
    if directory == ".":
        return "root"
    return "branch" if children[directory] else "leaf"


def cmd_plan(root, excludes, as_json):
    """Print the walk order. Changes nothing."""
    children = scope(root, excludes)
    if not children:
        print("error: no source files found under {}".format(root), file=sys.stderr)
        return 2
    # One record per directory, already in walk order.
    rows = [{"directory": d, "depth": depth_of(d), "kind": kind_of(d, children)} for d in bottom_up(children)]
    if as_json:
        print(json.dumps(rows, indent=2))
        return 0
    # Summary first, so the user can sanity-check the size before saying go.
    leaves = sum(1 for r in rows if r["kind"] == "leaf")
    print("{} directories in scope ({} leaves), deepest level {}".format(len(rows), leaves, rows[0]["depth"]))
    for row in rows:
        print("{:>3}  {:<6}  {}".format(row["depth"], row["kind"], row["directory"]))
    return 0


def cmd_init(root, excludes):
    """Write a fresh ledger with every directory pending."""
    path = os.path.join(root, LEDGER)
    # Overwriting would erase human approvals, so an existing ledger wins.
    if os.path.exists(path):
        print("{} already exists; not touching it. Run `next` to read it.".format(path))
        return 0
    children = scope(root, excludes)
    if not children:
        print("error: no source files found under {}".format(root), file=sys.stderr)
        return 2
    # The header says what the statuses mean, for whoever opens the file.
    today = datetime.date.today().isoformat()
    lines = [
        "# PEANUTS ledger", "",
        "root: {}".format(root), "date_opened: {}".format(today),
        "excluded: {}".format(", ".join(excludes) if excludes else "(none)"), "",
        "Status is one of: " + ", ".join(STATUSES) + ".",
        "Only a human moves a directory to approved. Rows are in bottom-up order.", "",
        "| directory | depth | kind | status | updated | notes |",
        "|---|---|---|---|---|---|",
    ]
    # One row per directory; `updated` and `notes` start empty.
    for directory in bottom_up(children):
        lines.append("| {} | {} | {} | pending |  |  |".format(directory, depth_of(directory), kind_of(directory, children)))
    with open(path, "w", encoding="utf-8") as ledger:
        ledger.write("\n".join(lines) + "\n")
    print("wrote {} with {} directories, all pending".format(path, len(children)))
    return 0


def read_ledger(path):
    """Return (rows, problems). Rows keep the ledger's order. Any table row
    that does not parse is a problem, never silently skipped: a dropped row
    would make its parent look eligible and open a hole in the gate."""
    rows, problems = [], []
    with open(path, encoding="utf-8") as ledger:
        for number, line in enumerate(ledger, start=1):
            text = line.rstrip("\n")
            if not text.lstrip().startswith("|"):
                continue
            match = ROW.match(text)
            # The header row and the |---| separator are the only table rows
            # allowed not to match.
            if not match:
                if not (HEADER_ROW.match(text) or SEPARATOR_ROW.match(text)):
                    problems.append("line {}: row does not parse; keep exactly six cells, a bare status word, "
                                    "and no '|' inside notes: {}".format(number, text.strip()))
                continue
            directory, depth, kind, status = match.group(1), int(match.group(2)), match.group(3), match.group(4)
            # A typo in a status would silently stall the walk; report it.
            if status not in STATUSES:
                problems.append("line {}: {} has unknown status {!r} (use one of: {})".format(
                    number, directory, status, ", ".join(STATUSES)))
            rows.append({"directory": directory, "depth": depth, "kind": kind, "status": status,
                         "notes": match.group(6).strip()})
    return rows, problems


def ledger_excludes(path):
    """The `excluded:` header line that `init` wrote, as a list of paths."""
    with open(path, encoding="utf-8") as ledger:
        for line in ledger:
            if line.startswith("excluded:"):
                value = line.split(":", 1)[1].strip()
                return [] if value == "(none)" else [os.path.normpath(v.strip()) for v in value.split(",") if v.strip()]
    return []


def analyse(rows, current):
    """Apply the walk order and the hard gate to the ledger, following the
    skill's resume rule: work the deepest level that still has a pending or
    needs-human-review row, and only that level. `current` is today's scope;
    an in-scope directory missing from the ledger counts as unfinished."""
    status = {r["directory"]: r["status"] for r in rows}
    depth = {r["directory"]: r["depth"] for r in rows}
    missing = set(current) - set(status)
    # Parent/child links come from the ledger plus anything missing from it.
    kids = {d: [] for d in set(status) | missing}
    for directory in kids:
        if directory != "." and parent_of(directory) in kids:
            kids[parent_of(directory)].append(directory)
    report = {"level": None, "review_queue": [], "blocked": [], "eligible": [], "waiting": [],
              "violations": [], "mark_rolled_up": [], "new_dirs": sorted(missing),
              "gone_dirs": sorted(set(status) - set(current))}
    # The current level: deepest depth with work still open (blocked rows wait).
    open_rows = [d for d, s in status.items() if s in ("pending", "needs-human-review")]
    level = max((depth[d] for d in open_rows), default=None)
    report["level"] = level
    for row in rows:
        directory, state = row["directory"], row["status"]
        unfinished = sorted(k for k in kids[directory] if status.get(k) not in DONE)
        # Sort each directory into the one bucket that says what to do next.
        if state == "needs-human-review":
            report["review_queue"].append(directory)
        elif state == "blocked":
            report["blocked"].append(directory)
        elif state == "pending" and row["depth"] == level and not unfinished:
            report["eligible"].append(directory)
        elif state == "pending":
            report["waiting"].append(directory)
        # A README above an unapproved child breaks the gate: bad leaves compound.
        if state in ("needs-human-review", "approved", "rolled-up") and unfinished:
            report["violations"].append("{} is {} but children are not approved: {}".format(
                directory, state, ", ".join(unfinished)))
        # Once a parent README exists, an approved child has been consumed.
        if state == "approved" and directory != "." and status.get(parent_of(directory)) in ("needs-human-review", "approved"):
            report["mark_rolled_up"].append(directory)
    report["review_at_level"] = [d for d in report["review_queue"] if depth[d] == level]
    return report


def cmd_next(root, excludes, as_json):
    """Read the ledger and say what may happen next. Changes nothing."""
    path = os.path.join(root, LEDGER)
    if not os.path.exists(path):
        print("error: no {} in {}; run `init` first".format(LEDGER, root), file=sys.stderr)
        return 2
    # Unknown statuses are reported, not fatal: the rest is still useful.
    rows, problems = read_ledger(path)
    if not rows:
        print("error: {} has no ledger rows".format(path), file=sys.stderr)
        return 2
    # Excludes recorded at init apply on every later run, so nobody has to
    # remember to pass the same --exclude flags again.
    excludes = sorted(set(excludes) | set(ledger_excludes(path)))
    report = analyse(rows, scope(root, excludes))
    report["problems"] = problems
    root_done = any(r["directory"] == "." and r["status"] == "approved" for r in rows)
    # The verdict is a suggestion for the agent, in priority order.
    if problems or report["violations"]:
        verdict = "FIX-LEDGER"
    elif root_done:
        verdict = "DONE"
    # Human review at the current level outranks new generation there.
    elif report["review_at_level"]:
        verdict = "REVIEW-FIRST"
    elif report["eligible"]:
        verdict = "GENERATE"
    else:
        verdict = "STUCK"
    report["verdict"] = verdict
    # Exit 1 only for a broken ledger, so a caller can stop on it.
    code = 1 if verdict == "FIX-LEDGER" else 0
    if as_json:
        print(json.dumps(report, indent=2))
        return code
    print_next(path, rows, report)
    return code


def print_next(path, rows, report):
    """Human-readable form of the `next` report."""
    print("ledger: {} ({} directories)".format(path, len(rows)))
    if report["level"] is not None:
        print("current level: depth {} (the deepest with pending or needs-human-review rows)".format(report["level"]))
    # Most urgent first: a broken ledger, then what needs a human, then work.
    labels = [
        ("problems", "ledger problems"),
        ("violations", "gate violations"),
        ("review_queue", "review queue (needs-human-review): surface these first"),
        ("blocked", "blocked: surface these too"),
        ("eligible", "eligible to generate (pending, at the current level, every child approved or rolled-up)"),
        ("mark_rolled_up", "approved but already consumed by a parent: mark rolled-up"),
        ("new_dirs", "in scope now but missing from the ledger (add rows; they count as unfinished)"),
        ("gone_dirs", "in the ledger but no longer in scope"),
    ]
    # Empty buckets stay quiet; the waiting count is enough on its own.
    for key, label in labels:
        if report[key]:
            print("{}: {}".format(label, len(report[key])))
            for item in report[key]:
                print("  " + item)
    print("waiting (shallower level, or children unfinished): {}".format(len(report["waiting"])))
    print("verdict: {}".format(report["verdict"]))


def main(argv=None):
    # Arguments only; an agent running this cannot answer interactive prompts.
    parser = argparse.ArgumentParser(description="Plan, start, and read the /peanuts PEANUTS.md ledger.")
    parser.add_argument("command", choices=("plan", "init", "next"))
    parser.add_argument("root", nargs="?", default=".", help="source-tree root (default: current directory)")
    parser.add_argument("--exclude", action="append", default=[], metavar="DIR",
                        help="directory to leave out, relative to root (repeatable)")
    parser.add_argument("--json", action="store_true", help="print JSON (plan and next)")
    args = parser.parse_args(argv)
    # Validate the root once here so every subcommand can trust it.
    if not os.path.isdir(args.root):
        print("error: {} is not a directory".format(args.root), file=sys.stderr)
        return 2
    # Excludes are compared as normalized paths relative to the root.
    excludes = [os.path.normpath(e) for e in args.exclude]
    if args.command == "plan":
        return cmd_plan(args.root, excludes, args.json)
    if args.command == "init":
        return cmd_init(args.root, excludes)
    return cmd_next(args.root, excludes, args.json)


if __name__ == "__main__":
    sys.exit(main())
