# peanuts: feed the Elephant before you ask it anything

Skill: [`skills/peanuts/SKILL.md`](../skills/peanuts/SKILL.md).
Article section: "Bootstrapping Your Reality (Or, 'Feeding the Elephant
Peanuts and Hay')".

## What problem it solves

EGM starts with a design conversation, and Step 1 of that conversation is
"point the AI at the relevant design docs or source tree." On a new project
that's easy. On a codebase with forty thousand lines and no design docs, it
isn't. Point a model at the whole tree and it runs out of context, gets
confused, and starts inventing how things work.

Rensin's answer is a hierarchy of small summaries. Every directory gets a
`README.md` saying what it is for and what each file does. The leaves get
written first, from the code alone (the peanuts). Each parent is written from
its children's READMEs plus its own files (the hay). At the end, a fresh
session can read only the READMEs and know which subsystem does what, for a
small fraction of the tokens the source would cost.

The catch, and the reason this is a skill and not a one-line prompt: leaf
READMEs written from code alone are wrong about half the time. If a parent is
summarized from wrong children, the error compounds all the way up. So every
level waits for a human to check the level below.

## How it triggers

The description says what it does first, then lists what people type:
"bootstrap this codebase", "generate READMEs", "feed the elephant", "onboard
me onto this codebase". The last trigger, "wants a fresh AI session to
understand a large existing project without reading every source file",
catches the request that never uses the word README at all.

The near miss is stated outright: "Not for greenfield projects whose design
docs already cover the code." Look at the should-not-trigger cases in
`evals/trigger-evals.json`. "Write a README for my new side project" contains
the word README and is still the wrong skill: it wants one human-facing
README, not a hierarchy for AI context.

## The SKILL.md, section by section

**Opening paragraphs.** The jungle metaphor and `sizeof(docs) << sizeof(code)`
come straight from the article. They tell the model what success looks like
(a session that reads only READMEs) before any step does.

**Shared preamble.** The four EGM reflexes, identical in all five skills.
Reflex 4 names `PEANUTS.md` as one of the artifacts to save.

**When to use it.** A short list, plus a "don't use" case. Without the
"don't", an eager model would happily generate READMEs for a repo that has
good design docs and make more to maintain.

**Hard rules.** Three of them, near the top so they survive when a long
session is compacted:

1. Bottom-up only. No README for a directory while any child is unreviewed.
2. The AI never decides a README is approved. A human's sign-off does.
3. `PEANUTS.md` drives the run.

Rule 2 is the interesting one. A model asked to "keep going" will mark its
own work approved to get unblocked. The skill closes that door in writing,
and the script (below) has no command that could open it.

**Ledger statuses.** Five states: `pending`, `needs-human-review`, `approved`,
`rolled-up`, `blocked`. The skill explains why five: fewer would mix up
"haven't tried" with "tried and waiting", more would be ceremony. Giving the
model the reason for a design choice lets it apply the choice sensibly in
cases the text doesn't cover.

**The ledger script.** Shows the three commands and what each one changes
(`plan` and `next` change nothing; `init` never overwrites). It also says what
to do by hand without Python.

**Workflow and checklist.** Step 0 confirms scope and warns about the 50%
leaf error rate *before* any work, because the user has to budget the review
time (the article says 5 to 10 minutes per leaf). Steps 1 to 4 are leaves,
human review, branches, root. Both article prompts appear verbatim, as quoted
frames, because they are the method; the model is not invited to improve
them.

**Retirement clause.** Every README ends with a line saying it is
scaffolding that design docs will replace. Without it, people preserve stale
READMEs forever.

**Anti-patterns** and **Where this skill sits in EGM** close the file. The
second one points forward: `/elephant` Step 1 reads this hierarchy instead of
the raw source.

## What lives outside SKILL.md

| File | Loaded when | Why it is separate |
|---|---|---|
| `scripts/peanuts_ledger.py` | Run at Step 0 and on every resume; never read | Finding in-scope directories, sorting deepest first, and applying the hard gate are exact jobs. A script does them the same way every time, and only its short report enters the request. |
| `assets/readme-templates.md` | When writing a README (Steps 1, 3, 4) | Three README shapes with the retirement line already in place. A template keeps every README the same shape across hundreds of directories. |
| `evals/trigger-evals.json` | Never, by the model | Twelve trigger tests for you. |

The script's `next` command is the feedback loop. It works one level at a
time, deepest first: the current level is the deepest one that still has
work open. After a batch it reports the review queue, anything blocked, what
is eligible now, and any **gate violation** (a parent marked for review while
a child was never approved). Its verdict (`REVIEW-FIRST`, `GENERATE`,
`FIX-LEDGER`, `STUCK`, `DONE`) tells the model which branch of the workflow
it is on.

`next` is also strict about the ledger itself. A row it can't parse, say a
status someone wrote as `**approved**`, is reported as a problem instead of
being skipped. That matters: a skipped row would make its parent look
eligible, and the gate would have a hole in it exactly where a human had
been sloppy.

## Worked example

`shipyard` is a made-up Python order-and-shipping service: about 40,000
lines, written by people who have left, with no docs. The team wants to add
webhook retries (the running example for the next four walkthroughs), but
nobody can explain how orders reach the webhook code.

**Step 0.** The user types "onboard me onto this codebase, it's huge." The
skill loads. The model confirms the root and runs `plan`:

```
$ python3 ~/.claude/skills/peanuts/scripts/peanuts_ledger.py plan .
23 directories in scope (14 leaves), deepest level 4
  4  leaf    shipyard/carriers/ups/rates
  4  leaf    shipyard/carriers/ups/labels
  ...
  1  branch  shipyard
  0  root    .
```

It shows the user that shape, warns that about half the leaf descriptions
will be wrong and need 5 to 10 minutes each, and suggests
`--exclude shipyard/legacy_v1` for a dead subtree the user mentions. The user
agrees. `init` writes `PEANUTS.md` with 21 rows, all `pending`.

**Step 1.** `next` reports the current level as depth 4 and lists the six
leaves there as eligible. The shallower leaves wait their turn. The model
writes a README in each of the six, marks each `needs-human-review`, and
notes its doubts in the ledger.

**Step 2.** The model stops and hands the queue to the user, naming its
doubts: "`retry.py` might be the HTTP retry for carrier APIs or for webhooks;
unclear." The user fixes two leaves, including that line: it is carrier-only,
and webhooks have no retry at all, which is the bug they came to fix. All six
become `approved`.

**Step 3.** `next` moves to depth 3. Eligible now: the branch
`shipyard/carriers/ups` (both its children are approved) and four leaves at
that depth. The branch README is written from its two children's READMEs plus
its own files, and the children become `rolled-up`. The leaves get the leaf
treatment. Then review again, and up one more level.

**Step 4.** The root README maps the subsystems. The user approves it and
`next` says `DONE`. When the team runs `/elephant` for webhook retries, Step
1 reads twenty-one READMEs instead of forty thousand lines.

## What the skill adds to the article

The article gives the two prompts, the bottom-up order, the 50% figure, and
the human check. The skill adds the `PEANUTS.md` ledger with its five
statuses, the hard gate stated as a rule, the review queue as an explicit
handoff, the script, and the README templates. None of that changes the
method; it makes the method survive a session that crashes halfway up the
tree.

## Review questions and exercises

1. Why must a parent README wait for its children to be *approved*, rather
   than merely *written*? Give a concrete example of an error compounding up two levels.
2. The skill batches within a level but never across levels. What would go
   wrong if it generated levels 3 and 2 in one pass? And why does a shallow
   *leaf* wait for the deeper levels, even though it has no children?
   (There are arguments both ways. Make one.)
3. Run `peanuts_ledger.py plan` on a repo you have (a lab, a project, an
   open-source tool). How many directories and leaves? Which directories
   would you `--exclude`, and why?
4. Hand-edit a `PEANUTS.md` so a branch is `needs-human-review` while one of
   its children is still `pending`, then run `next`. What does it report, and
   what exit code does it return? Why is that a useful signal to an agent?
5. The retirement clause says a README can go once design docs cover its
   files. Who would notice that moment in a real team, and how? Propose a
   check that could detect it.
