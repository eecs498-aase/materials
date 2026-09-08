# What bin/demo --rehearse runs for this demo. Sourced, not executed.
#
# Three independent scenarios, each from a fresh working copy, because the
# thing under test is what one prompt does with one context -- not a sequence.
# Helpers: fresh (rebuild the copy), pass (one aider turn), check (a command
# in the copy), expect (what the runbook claims).

PROMPT="Add a new CLI argument --output-format with choices text, json, markdown."

# The flag existing is not the same as the flag working. A model that edits
# arg_parse.py and forgets main.py leaves a program that runs, exits 0, and
# prints the text report for every format. This is the check that catches it.
FEATURE_WORKS='
  diff -q <(python3 src/main.py transcript.txt --output-format json) \
          <(python3 src/main.py transcript.txt) >/dev/null && {
    echo "flag accepted and silently ignored: json output is identical to text"; exit 1; }
  python3 src/main.py transcript.txt --output-format json |
    python3 -c "import json,sys; json.load(sys.stdin)" || {
    echo "output changed but it is not JSON"; exit 1; }
  echo "json differs from text and parses"'

echo "Scenario 1: only main.py in context, decline the add"
fresh
pass "step 1 (main.py only)" "$PROMPT" src/main.py
check "program still runs" "python3 src/main.py transcript.txt --top 3"
expect "FAIL. main.py edited alone, arg_parse.py declined -- the partial"
expect "change that looks finished. If it PASSES with 1 commit, the model"
expect "asked for the file instead of guessing; scenario 2 gets past that."

echo
echo "Scenario 2: only main.py, and insist"
fresh
pass "step 1b (insist)" "$PROMPT Do it in src/main.py only. Do not touch any other file." src/main.py
check "program still runs" "python3 src/main.py transcript.txt --top 3"
expect "FAIL, with AttributeError on args.output_format."

echo
echo "Scenario 3: both files in context"
fresh
pass "step 2 (main.py + arg_parse.py)" "$PROMPT" src/main.py src/arg_parse.py
check "program still runs" "python3 src/main.py transcript.txt --top 3"
check "the feature actually works" "$FEATURE_WORKS"
expect "both PASS. Anything else is the demo's real result -- read the log."
