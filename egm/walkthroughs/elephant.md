# elephant: grow the design before you grow the code

Skill: [`skills/elephant/SKILL.md`](../skills/elephant/SKILL.md).
Article sections: "Phase 1: Growing the Elephant (No Code Yet)" and "Phase 2:
Teaching the Elephant".

## What problem it solves

Ask a coding agent for a feature and it starts typing code in the first
reply. That feels fast. It also means every design decision, such as where
the retry state lives or what happens on the tenth failure, was made by the
model in the middle of a sentence. Now it is buried in a diff nobody
designed.

Rensin's claim is that once AI writes most of the code, the design document
is the artifact a person can actually stand behind: *design is the new
code*. So the Elephant phase forbids code. You and the model argue about the
problem for 20 to 30 minutes, the model proposes a design first, you argue
about that for as long as it takes (his sessions sometimes run 2 to 3 days),
and only then do you write a four-section doc, one section at a time.

The skill's job is to keep a model on that path. Models are trained to be
helpful, and in a design conversation "helpful" means agreeing with you and
writing code. Both are what this skill exists to stop.

## How it triggers

The description opens with what the skill produces (the four-section doc),
then the phrases: "design a feature", "let's plan X", "build X", "spec this
out", "design doc first". It adds "even if they did not ask for a document",
because the person who most needs a design conversation is the one who said
"build me a rate limiter" and expects code.

That breadth is risky. "Build X" appears in a lot of requests, so the
description ends with the boundary: "Not for one-line fixes or questions
about how existing code works." In `evals/trigger-evals.json`, "fix the typo
in the README" and "rename the variable tmp" are the near misses that test
that boundary. So is "the design doc for webhook-retries passed review, go
ahead and implement it", which belongs to `/egm-implement`.

## The SKILL.md, section by section

**Opening.** One paragraph says the output is a document, not code, and
names the rule the whole skill serves. Everything after it can be read as a
consequence of that paragraph.

**Shared preamble.** Four reflexes, copied into every EGM skill. Reflex 2 is
the sycophancy reset, worded as a line the model says to itself. (A note on
sources: the article's Step 3 line is "You are not being helpful. Your
highest and best use is to challenge my thinking." The skill appends "When
you agree with me, you are not being helpful," which echoes the article's
Part 1.)

**Hard rules.** Four, at the top: no code in this session; you propose the
first draft, not the user; no sycophancy; build the doc one section at a
time. Rule 2 deserves a second look. If the user brings a draft and the
model reacts to it, the user's blind spots become the design's blind spots.
The article says it is "very important" that the AI proposes first, because
its proposal is also a test of whether it understood the problem.

**Checklist.** Seven lines, one per step. An Elephant session can span days
and several context resets, so the checklist is mirrored by `current_step` in
the ledger. A resumed session reads where it was.

**Step 0, the state directory.** The skill picks a slug (`webhook-retries`),
creates `docs/egm/<slug>/`, and starts `ELEPHANT.md` from a template. If the
file exists, the skill refuses to resume silently and offers three choices
(resume, new slug, rotate the old file). The text calls silent resume a
footgun: picking up a stranger's half-finished design because the names
matched is a real failure.

**Step 1, context loading.** Read the design docs and the most relevant code
(or the `/peanuts` READMEs), then say back what you understood and ask to be
corrected. "A wrong mental model on minute one becomes hallucinated code on
minute ten." What was read gets logged, so the next session doesn't have to
re-read it.

**Step 2, the interview.** It opens with the article's no-code prompt,
verbatim. The model says it to itself in the second person, because that is
the frame. Then come the instructions for a good interview: one or two
questions at a time, challenge assumptions, push on failure modes, argue.
This is the highest-freedom part of the skill. No script can hold a good
design argument, so the text gives goals and examples, not steps.

**Step 3, the sycophant defense.** A standing instruction, not a one-time
step. When the conversation gets easy, the model is probably agreeing too
much.

**Step 4, first draft.** The model writes its own technical proposal in
prose and block diagrams, even if the user has one. When the user corrects
it, the model asks for the file that proves it and reads it. That last habit
matters. A correction backed by a file changes what the model believes. A
correction without one tends to change only its apology.

**Step 5, the doc.** The filename must equal the slug. That one rule is what
lets `/goldfish` and `/egm-implement` find the ledgers from nothing but the
doc's path. Then the four sections, in order, each approved before the next:
Problem (3 to 5 plain sentences), Technical Plan (explanatory prose),
Alternatives (every rejected idea with its reason), Detailed Implementation
(every file, what changes, why).

**Step 6, check and hand off.** A short self-check before saving: does every
component in the plan map to a file, does any "and similar changes" hide an
unlisted file, does every alternative say why it lost. Then
`human_review_gate: pending` goes in the ledger, and the user is pointed to
`/goldfish`. The skill never runs the next skill itself.

**Anti-patterns, why it exists, where it sits.** The anti-patterns are the
ways this goes wrong in practice: one-shotting the doc, reacting to the
user's draft, stopping when the user agrees, the "quick snippet to
illustrate".

## What lives outside SKILL.md

| File | Loaded when | Why it is separate |
|---|---|---|
| `assets/elephant-ledger-template.md` | Step 0, once | `/goldfish` and `/egm-implement` read this ledger for orientation, and `check_gate.py` only checks that it exists. The template keeps the header fields exact, so a resumed session finds `current_step` where it expects it. |
| `assets/design-doc-template.md` | Step 5, once | The four-section skeleton, with a comment in each section saying what goes there. |
| `references/design-doc-sections.md` | Step 5, before each section | The long guidance and examples for each section. |
| `evals/trigger-evals.json` | Never, by the model | Trigger tests. |

The reference file is the best example in this suite of *why* progressive
disclosure helps, beyond saving tokens. Step 5 often happens days after the
skill loaded. By then the conversation may have been compacted, and Claude
Code re-attaches only the first 5,000 tokens of a skill after compaction.
Reading the section guidance fresh, right when it is needed, is more reliable
than hoping it survived.

## Worked example

The `shipyard` team (see the [peanuts walkthrough](peanuts.md)) wants webhook
retries: when a customer's server is down, today the "order shipped" webhook
is simply dropped.

The user types: "build retries for our webhooks."

The skill loads. Step 0 proposes the slug `webhook-retries` and creates the
ledger. Step 1 reads the root README and `shipyard/notify/README.md`, then
says back: "Webhooks are sent synchronously from `notify/dispatch.py` inside
the order transaction, and a failure is logged and dropped. Is that right?"
The user corrects one thing: dispatch runs after commit, not inside the
transaction. The model asks which file shows that, reads it, and logs both
files under `## Context loaded`.

Step 2 opens with the no-code prompt. Then, one at a time:

> How long can a customer's endpoint be down before a retried "shipped"
> event is worse than no event at all?

> If an order ships and then is cancelled while the first event is still
> retrying, which event should the customer see first?

The user hadn't thought about the second one. Twenty minutes later the
problem is clear, including a decision to give up after 24 hours and mark
the delivery failed where support can see it.

Step 4: the model proposes a durable outbox table, written after commit,
drained by a worker with exponential backoff, and a dead-letter state. The
user wants Redis instead. The model asks why, hears "we already run Redis",
and argues back: the outbox survives a Redis restart, and ordering per order
is easy in one table. The user agrees, and the model records "Redis queue:
rejected, loses events on restart" for the Alternatives section.

Step 5 writes `docs/designs/webhook-retries.md` one section at a time. The
first draft of Detailed Implementation says "update the dispatchers
accordingly." The Step 6 check catches it: which dispatchers? The model
enumerates all three, each with its change and reason. The ledger gets
`human_review_gate: pending` and `next_step: /goldfish
docs/designs/webhook-retries.md`.

## What the skill adds to the article

The article supplies the phases, the no-code prompt, the reset, the "you go
first" rule, the four sections, and the time estimates. The skill adds the
`docs/egm/<slug>/` folder and `ELEPHANT.md` ledger, the slug-equals-filename
contract, the refusal to resume silently, the human review gate field, and
the pre-handoff check. Those additions exist so that a design spread over
three days and five sessions still behaves like one conversation.

## Review questions and exercises

1. Hard rule 2 makes the model propose first even when the user has a draft.
   Describe a design flaw that would survive if the model only reviewed the
   user's draft, and how a model-first proposal could surface it.
2. Why does the skill quote the no-code prompt verbatim instead of saying
   "tell yourself not to write code"? Relate your answer to degrees of
   freedom.
3. Run `/elephant` on a small feature for a project of yours. Count the
   questions the model asked before proposing anything. Did it argue with you
   at least once? If not, use the reset line and note what changed.
4. The slug must equal the doc's filename. Trace exactly which other skill
   and which script would break, and how, if you saved the doc as
   `retries-v2.md` with slug `webhook-retries`.
5. Write the Alternatives section for a decision you made recently in your
   own code. Could someone a month from now tell, from that section alone,
   why you rejected each option?
