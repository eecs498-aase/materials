# What bin/demo --rehearse runs for this demo. Sourced, not executed.
#
# One working copy, three prompts in order, tests after each -- the same shape
# as the live demo, because here the prompts genuinely build on each other.
# Helpers: fresh (rebuild the copy), pass (one aider turn), check (a command
# in the copy), expect (what the runbook claims).
#
# Caveat worth knowing: each pass is its own aider run, so chat history does
# not carry between prompts. The files do, which is what these three prompts
# actually depend on. Prompt 2 asks for a test of the no-args path that prompt
# 1 created, and it can see it, because it is in the file.

fresh
check "tests green before anything" "pytest -q"
check "no-args crashes (this is why prompt 1 exists)" \
  "python3 notes.py 2>&1 | grep -q IndexError"
expect "both PASS. A green suite on a program that crashes is the point."

echo
pass "prompt 1 (parse_args)" \
  "Refactor parse_args() to handle the no-args case - print usage and exit cleanly." \
  notes.py test_notes.py
check "tests still green" "pytest -q"
# Both of prompt 1's known failure modes are invisible to pytest, so check the
# behaviour and the shape of the file, not the exit code. Whole-file edits drop
# `return argv[0], argv[1:]` and every command breaks. Diff edits insert a
# fixed parse_args above the original without removing it, so the original
# still wins, the suite stays green, and nothing was actually fixed.
check "parse_args defined exactly once" \
  "test \$(grep -c '^def parse_args' notes.py) -eq 1"
check "no-args prints usage, no traceback" \
  "python3 notes.py 2>&1 | grep -qi usage && ! python3 notes.py 2>&1 | grep -q Traceback"
expect "all three PASS. Exit code is the model's call - 0 or 1 both read as"
expect "'cleanly' - so it is not checked."

echo
pass "prompt 2 (test for it)" \
  "Add a unit test for the no-args path." \
  notes.py test_notes.py
# A test written against the fix prompt 1 was supposed to make is the thing
# that exposes prompt 1 having quietly done nothing. If this goes red, read
# the new test before you blame it.
check "tests still green" "pytest -q"
check "the suite actually grew" \
  "test \$(grep -c '^def test_' test_notes.py) -ge 5"
expect "both PASS. A test that was not added is the failure to watch for."

echo
pass "prompt 3 (dispatch)" \
  "Replace the if-chain in dispatch() with a dictionary lookup." \
  notes.py test_notes.py
check "tests still green" "pytest -q"
check "the if-chain is gone" "! grep -q 'elif command ==' notes.py"
expect "both PASS. Green tests with the if-chain still there means it agreed"
expect "with you and changed nothing, which is the quiet failure."
