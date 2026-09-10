# What bin/demo --rehearse runs for this demo. Sourced, not executed.
#
# Two scenarios from two fresh copies. Scenario 1 is the demo: the whole spec,
# in one paste, in Architect Mode. Scenario 2 is the control that says whether
# the spec is doing any work, and it is the one worth reading -- the same
# request, written the way somebody would type it without a spec.
# Helpers: fresh (rebuild the copy), pass (one aider turn), check (a command
# in the copy), expect (what the runbook claims).
#
# Caveat that matters here more than it did in L03. Architect Mode asks two
# questions a pipe cannot answer: "Edit the files?" after the plan, and
# "Create new file?" for each file the spec says to create. bin/demo's default
# answer stream is a run of `n`, which is right for L03 (declining IS that
# scenario) and would make this one produce nothing at all. `--yes-always`
# takes the other side of every one of them.
#
# Two things follow. The plan is auto-accepted, so what this measures is model
# time and the files that land, never the pause -- the pause is real and it is
# yours to run live. And `--yes-always` also says yes to "Add file to the
# chat?", which in Architect Mode re-runs the architect and throws away the
# plan; that is how the 2026-09-09 rehearsal produced two files instead of
# four. The demo's `read:` list now holds every readonly file in the spec so
# the question does not come up, but if it ever does, the log records it. Read
# the log, not just the PASS lines.
YES=--yes-always

# The spec, read off disk rather than pasted in here, so the rehearsal and the
# lecture cannot drift apart.
SPEC="$(cat "$demo_dir/spec.md")"

# The editable half of the spec's Beginning context, which is also what the
# runbook tells you to open aider with. The readonly half is in
# `aider.conf.yml`'s `read:` list and arrives on its own. If these ever
# disagree, the runbook is wrong.
FILES="src/main.py src/arg_parse.py"

# Exit 0 is not the same as "the feature works". A model that adds the flag to
# arg_parse.py and never reads it in main.py leaves a program that runs, exits
# 0, and prints the same text report for every format. This is the check that
# catches it, and it is the L03 failure one lecture later.
JSON_WORKS='
  diff -q <(uv run --quiet main transcript.txt --output-format json) \
          <(uv run --quiet main transcript.txt) >/dev/null && {
    echo "flag accepted and silently ignored: json output is identical to text"; exit 1; }
  uv run --quiet main transcript.txt --output-format json |
    python3 -c "import json,sys; json.load(sys.stdin)" || {
    echo "output changed but it is not JSON"; exit 1; }
  echo "json differs from text and parses"'

# A chart that is not on disk is not a chart, whatever the program printed.
CHART_WORKS='
  rm -f chart.png
  uv run --quiet main transcript.txt --chart bar >/dev/null || {
    echo "--chart bar did not run"; exit 1; }
  test -s chart.png || { echo "no chart.png was written"; exit 1; }
  python3 -c "
import sys
head = open(\"chart.png\", \"rb\").read(8)
sys.exit(0 if head == b\"\\x89PNG\\r\\n\\x1a\\n\" else 1)" || {
    echo "chart.png exists but is not a PNG"; exit 1; }
  echo "chart.png written and it is a real PNG"'

echo "Scenario 1: the whole spec, Architect Mode, one paste"
fresh
check "the program runs before anything" "uv run --quiet main transcript.txt --top 3"
pass "spec (architect + editor)" "$SPEC" $YES $FILES
check "program still runs" "uv run --quiet main transcript.txt --top 3"
check "output_format.py exists" "test -f src/output_format.py"
check "chart.py exists" "test -f src/chart.py"
check "the flags got defined" "uv run --quiet main transcript.txt --output-format json --chart bar >/dev/null"
check "json actually works" "$JSON_WORKS"
check "the chart actually works" "$CHART_WORKS"
check "plt.show() never made it in" "! grep -rn 'plt.show()\|pyplot.show()' src/"
expect "all of these PASS, and the wall-clock on the pass line is the number"
expect "that decides whether the demo fits the slot. Two model calls, four"
expect "files. Anything above about five minutes and you cut the walkthrough."

echo
echo "Scenario 2: the same request without a spec (the control)"
fresh
pass "no spec, one sentence" \
  "Add word frequency charts and structured file output to this CLI." $YES $FILES
check "program still runs" "uv run --quiet main transcript.txt --top 3"
check "json actually works" "$JSON_WORKS"
check "the chart actually works" "$CHART_WORKS"
expect "at least one FAIL, and which one is the interesting part. This is the"
expect "slide's claim under test: the spec is not ceremony, it is the reason"
expect "the first run lands. If this scenario passes clean, say so in class"
expect "instead of claiming a difference the room did not see."
