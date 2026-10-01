# egm-implement: build the doc, only the doc

Skill: [`skills/egm-implement/SKILL.md`](../skills/egm-implement/SKILL.md).
Article section: "Phase 4: Implementation", Step 8 ("Coding with
Guardrails").

## What problem it solves

The article's Step 8 is one prompt: "Read this design doc and the files it
references. Implement the feature as described. Follow the plan exactly."
Because the doc lists every file and every change, the model has rails to
run on. If the session crashes, a new one reads the doc and carries on.

That works when everything goes to plan. The skill is about the two moments
when it doesn't:

1. **Before the first edit.** Is this doc actually approved? A model asked to
   "implement the design" will implement whatever doc is lying around,
   including one that failed its last Goldfish round.
2. **The first surprise.** Halfway through, the code needs a change to a file
   the doc never mentions. The natural, helpful move is to just make it. Do
   that a dozen times and the doc no longer describes the system, and the
   "source of truth" is fiction.

So the skill adds an entry gate, a rule that drift is surfaced instead of
absorbed, and a ledger (`IMPLEMENT.md`) that records both.

## How it triggers

"Implement this design", "build the feature from the doc", "egm implement",
"execute the plan", and the description's condition: a *Goldfish-approved*
design doc in `docs/designs/`. It also says up front that it refuses to start
until the gate is resolved, so the model knows that before it loads anything.

The near misses in `evals/trigger-evals.json` are instructive: "add a
--verbose flag, it's a two line change" (no design doc, too small), "let's
plan the notifications feature, no code yet" (elephant), "implement
quicksort for my homework" (no design doc at all). Each shares a word with
the triggers and wants something else.

## The SKILL.md, section by section

**Opening.** Where the skill sits between `/goldfish` and `/mean-review`,
and the three things it makes authoritative: the doc (source of truth),
`GOLDFISH.md` (entry gate), `IMPLEMENT.md` (trace). Then the article's Step 8
prompt, quoted as the working frame.

**Hard rules.** Four: no code until ready *and* the human gate is resolved;
no file the doc doesn't list; log as you go, not afterward; end with a
handoff to `/mean-review`. Rule 2 is the one that does the most work. It
turns "I noticed something" from a reason to edit into a reason to stop.

**Checklist.** Six steps, with Step 4 marked "(standing)": drift can appear
at any point, so it is not a phase you pass through once.

**Step 1, the gate.** The skill runs a script rather than asking the model to
read `GOLDFISH.md` and judge:

```sh
python3 <skill-dir>/scripts/check_gate.py docs/designs/webhook-retries.md
```

Each exit code maps to one action:

| Exit | Verdict | The skill says |
|---|---|---|
| 0 | GO | Proceed. If the gate is `skipped-solo`, show and log the warning. |
| 1 | BLOCKED | Stop. Tell the user exactly what is missing and what to run. |
| 2 | usage | Ask which doc. |
| 3 | CHECK-BY-HAND | A ledger value is prose, or two values disagree. Show the lines; the human decides. |

Exit 3 is the interesting design choice. Real ledgers drift from the format.
One real `GOLDFISH.md` reads `readiness: core **ready**; periphery not-yet`.
A script that guessed would be wrong half the time. A script that always
blocked would be ignored. So it refuses to guess and hands that one decision
back to a person.

Notice also where the script looks for the gate: the `human_review_gate`
field in the `GOLDFISH.md` header. Round entries and `ELEPHANT.md` carry
copies for the record, but the header is the one place a person signs off,
so there is never a question of which copy counts.

**Step 2, the ledger.** Created from a template, or read and resumed. The
resume case is the article's crash recovery made concrete: the new session
reads which files are `done` and continues.

**Step 3, implement.** Walk the doc's file list. Re-ordering is allowed
(producers before consumers) as long as it is logged. One file per logical
change, because everything here flows into a review next.

**Step 4, drift.** Four triggers (unlisted file, change can't work as
written, new file needed, false assumption), one response: stop, log an
entry, recommend a resolution, and wait. The resolutions scale with the
size of the surprise: a small clarification edits the doc in place, a
section-level change is rewritten with Elephant discipline, and a big one
goes back through `/goldfish`.

**Step 5, verification.** Run the smallest real check the doc names (or the
project implies), record the exact command and result, and if it fails,
treat that as drift and loop.

**Step 6, hand off.** Close the ledger, point at `/mean-review`, and don't
run it. Writing code and attacking code are different jobs, and a review
started by the same session that wrote the code is softer.

## What lives outside SKILL.md

| File | Loaded when | Why it is separate |
|---|---|---|
| `scripts/check_gate.py` | Run once at Step 1; never read | The gate is fragile (exact field names, two places the gate can be written) and must be the same every time. Read-only: it never sets a gate. |
| `assets/implement-ledger-template.md` | Step 2, and again when logging a drift or a verification | The header fields, the files table, and the exact drift and verification entry formats. |
| `evals/trigger-evals.json` | Never, by the model | Trigger tests. |

## Worked example

`webhook-retries` passed round 2 of Goldfish and a teammate signed off (see
the [goldfish walkthrough](goldfish.md)). The user types "implement it".

**Step 1.**

```
$ python3 ~/.claude/skills/egm-implement/scripts/check_gate.py docs/designs/webhook-retries.md
design doc:  docs/designs/webhook-retries.md
state dir:   docs/egm/webhook-retries/
latest round: 2
readiness:   ready
human review gate: passed
note: ELEPHANT.md exists: read it for orientation, not to re-derive the design
verdict:     GO
```

**Step 2.** `IMPLEMENT.md` is created with seven rows in `## Files touched`,
all `planned`, matching the doc's seven entries. The model notes that it will
build the outbox migration first, though the doc lists it fourth.

**Step 3.** The migration, the outbox model, and the worker go in, each a
separate change, each row flipped to `done`.

**Step 4.** Writing the worker, the model finds that the HTTP client in
`shipyard/notify/http.py` has a hard-coded 2-second timeout and no way to
pass one in. The doc assumed it was configurable, and `http.py` is not in
the file list. The model stops and logs:

```
- date: 2026-10-14
- type: new-assumption-needed
- description: notify/http.py hard-codes timeout=2; the doc's worker passes a per-attempt timeout. http.py is not in Detailed Implementation.
- proposed resolution: add notify/http.py to section 4 (accept an optional timeout, default 2) and to section 2's diagram
- status: open
```

The user agrees. The model edits the doc in place, marks the drift
`resolved: doc edited in place at docs/designs/webhook-retries.md`, and only
then changes `http.py`.

**Step 5.** `pytest tests/notify -q` passes; command and result are
recorded.

**Step 6.** The ledger closes with `status: complete` and `next_step:
/mean-review`. The model tells the user the diff is ready and stops.

## What the skill adds to the article

The article's Step 8 is a single prompt plus "if it crashes, start a new
session with the doc". The skill adds the entry gate and its script, the
rule against unlisted files, the drift procedure, the `IMPLEMENT.md` ledger,
recorded verification, and the deliberate pause before review. The prompt is
still there, quoted as the frame.

## Review questions and exercises

1. Why does the gate check need a person when a ledger value is prose? Write
   two different `readiness:` lines that a careless parser would read as
   `ready` but a person would not.
2. "While I'm here, let me also rename X" is listed as drift. Argue the
   other side: when is absorbing a tiny unlisted change the right call? Then
   explain what the doc loses if you do it ten times.
3. Run `check_gate.py` against a hand-built `docs/egm/demo/GOLDFISH.md` in a
   scratch directory. Produce each of the four exit codes on purpose and
   write down what you changed each time.
4. Step 6 says not to run `/mean-review` automatically. What would a review
   look like if it were written by the same session, in the same turn, that
   wrote the code? Relate this to the sycophancy reflex.
5. Look at the drift entry in the worked example. Which of the four
   resolutions (edit in place, rewrite a section, full Elephant rerun,
   Goldfish rerun) would you choose if the timeout change had also needed a
   new config file and a change to the deploy pipeline? Why?
