# goldfish: test the doc against a reader with no memory

Skill: [`skills/goldfish/SKILL.md`](../skills/goldfish/SKILL.md).
Article section: "Phase 3: The Goldfish Protocol" (Steps 5 to 7).

## What problem it solves

After an Elephant session, the design doc reads perfectly to you and to the
session that helped write it. Both of you remember the three days of
argument behind every sentence. Neither of you can tell what the doc says on
its own.

A Goldfish is a session that remembers nothing. Give it only the doc and the
files the doc points to, and see what it makes of them. Rensin uses three:

- **Comprehension** (Step 5): explain what this is trying to do and how the
  system works today. If it can't, the doc is missing context.
- **Critic** (Step 6): find everything missed, every faulty assumption, every
  unhandled edge case. He finds about 30% of the suggestions highly valuable,
  which is plenty.
- **Readiness** (Step 7): could you implement this in one pass? Every
  question it would need to ask is a hole in the doc.

Then fix the doc and run all three again, until the findings are nit-picks.
Then a real human reviews it.

## How it triggers

"Goldfish test", "validate this design", "is this doc ready?", "fresh eyes on
this doc", and the most common real case: "has just finished an /elephant
session and needs to know whether the doc stands on its own".

The boundary with `mean-review` is written into both descriptions: goldfish
reviews a *design doc*, mean-review reviews *code*. The trigger tests include
"tear apart the diff on this branch" (mean-review's job) and "summarize this
design doc for my manager" (shares the words, wants something else). One
negative is about actual goldfish dying in a tank. A keyword-matching
harness would fall for it; a description that says what the skill *does*
won't.

## The SKILL.md, section by section

**Opening.** The Elephant/Goldfish contrast in two paragraphs, and the three
tests a doc must pass. Then the invocation line, `/goldfish
[path-to-design-doc]`.

**How "fresh" is implemented.** This is the core idea of the skill, so it
comes before the workflow. The point is that the value comes from
*independent context*, not from a clever reviewer persona. Three
requirements: no shared history, only the doc path and a task, and a ban on
reading the design conversation. A subagent spawn gives you the first one
for free. The preamble in every prompt enforces the third.

Then the rule that surprises people: **spawn all three in one message, in
parallel.** Speed is the minor reason. The major one is that a serial
orchestrator is tempted to paste Goldfish A's findings into Goldfish B's
prompt "for context", which quietly turns three independent readers into one
reader and two echoes. Parallel spawning makes that impossible.

**Which subagent types.** One default (Claude Code's role agents if
installed, else `general-purpose` and `Plan`) and a pointer to
`references/runtimes.md` for everything else. A default beats a menu.

**Step 1, resolve.** Find the doc, derive the slug from its filename (the
contract `/elephant` set up), find `docs/egm/<slug>/`. The orchestrator reads
`ELEPHANT.md` to orient itself and is told, in bold, never to pass any of it
to a reviewer.

**Step 2, spawn.** Read the prompts from `assets/`, prepend the preamble,
fill in the path, issue three calls in one message. "Do not edit the prompts
per round" keeps rounds comparable.

**Step 3, collate and write.** Reviewers return reports inline; the
orchestrator writes every file. That keeps reviewers from needing write
access and keeps the record in one hand. The synthesis order is deliberate:
real gaps first, nits last, and findings that two or more reviewers raised
independently called out as high confidence. Round 2 and later save reports
with an `-rN` suffix so earlier rounds are never overwritten.

**Step 4, edit and loop.** Every proposed edit quotes the current text and
the replacement, and the user approves each one. The stop condition has two
halves, and both must hold: the critiques are nit-level, *and* a human has
set `human_review_gate` in the `GOLDFISH.md` header to `passed` (or
`skipped-solo`, when you truly work alone). The header is the gate; each
round entry keeps a copy for the record. The skill never sets the gate
itself.

**Anti-patterns.** Each one is a way the independence quietly breaks or the
loop ends early. One came from a real run: a design doc linked to its own
`docs/egm/` folder, two reviewers followed the link, and they read the
design conversation they were supposed to be blind to.

## What lives outside SKILL.md

| File | Loaded when | Why it is separate |
|---|---|---|
| `assets/goldfish-reviewer-prompts.md` | Step 2, every round | 150 lines of exact prompt text. It is copied into messages, not used for reasoning, so it is an asset. |
| `assets/goldfish-ledger-template.md` | Step 1, first round only | The `GOLDFISH.md` header and the round block, including the exact `readiness` and `human_review_gate` fields that `/egm-implement` checks. |
| `references/runtimes.md` | Only outside Claude Code | Subagent names for Cowork, OpenClaw, and Hermes, and how to run the test by hand. A Claude Code user never pays for it. |
| `evals/trigger-evals.json` | Never, by the model | Trigger tests. |

Look at how the Goldfish C prompt in the assets file is written. It runs on a
*planner* subagent, and planners are built to produce confident plans, the
exact opposite of what a readiness check needs. So the prompt says, in
capitals, to use the planning ability internally and return only a verdict
and questions: "'Probably figure it out' is the exact silent assumption this
review exists to surface."

## Worked example

`docs/designs/webhook-retries.md` is done (see the [elephant
walkthrough](elephant.md)). The user types "goldfish test it".

**Step 1.** Slug `webhook-retries`; state directory found; `GOLDFISH.md`
created from the template. The model confirms both paths.

**Step 2.** Three calls go out in one message. Each starts with the preamble
("Your only sources of truth are: 1. The design document path... 2. The
project files explicitly referenced by that design document...").

**Step 3.** The reports come back:

- **A (comprehension)** explains the outbox design correctly, but describes
  the dead-letter state as "deleted after 24 hours". The doc said "marked
  failed". A fresh reader got it wrong, so the sentence is ambiguous.
- **B (critic)** returns 31 findings. Two matter: nothing says what happens
  to queued events when a customer *changes* their webhook URL, and the
  worker's batch size is unstated. Most of the rest are wording.
- **C (readiness)** says NOT-READY with 6 questions. Question 2 is the same
  URL-change problem B found. That is convergence: two reviewers who never
  saw each other's work found the same hole.

The model writes the three report files and a round 1 entry with
`readiness: not-yet`. Its summary to the user leads with the URL-change gap
and the dead-letter wording, and lists 24 of B's findings as nits.

**Step 4.** The model proposes four edits, each quoting old and new text.
The user accepts three and rejects one ("batch size is an ops setting, not a
design decision"), and the disposition is recorded. Round 2 comes back with
nits only, and C says READY. The user's teammate reads the doc, and the user
edits the `GOLDFISH.md` header to `human_review_gate: passed`. The model
copies that into the round 2 entry, marks it `readiness: ready`, and points
to `/egm-implement`.

## What the skill adds to the article

The article runs each Goldfish as a separate fresh chat, by hand. The skill
runs them as parallel subagents with a written independence contract (the
preamble), adds a third question to the comprehension prompt ("what changes
will this feature introduce?"), rewrites the readiness prompt to return
questions instead of a yes, keeps every round in `GOLDFISH.md`, and turns
"show it to a real human" into a gate field that only a person can set.

## Review questions and exercises

1. Why is "fresh" guaranteed by the spawn and the preamble rather than by
   the reviewer's persona? What would you lose by running all three
   reviewers in the session that wrote the doc, with a "pretend you haven't
   seen this" instruction?
2. The skill demands a parallel spawn. Describe, step by step, how a serial
   orchestrator could contaminate Goldfish C with Goldfish A's output without
   anyone intending it.
3. Take a design doc or spec you have written for this course. Run the three
   prompts from `assets/goldfish-reviewer-prompts.md` by hand, each in a
   brand-new chat. Which reviewer found the most useful thing? What fraction
   of B's findings would you act on? Compare with Rensin's 30%.
4. The stop condition requires a human sign-off even when the critiques are
   trivial. Argue for or against `skipped-solo` existing at all.
5. The Goldfish C prompt is tuned against a planner's habit of producing
   confident plans. Find one other place in any EGM skill where a prompt is
   written to push *against* a model's default behavior. What default is it
   fighting?
