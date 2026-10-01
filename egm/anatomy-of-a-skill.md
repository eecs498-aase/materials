# Anatomy of a skill

You have built a harness. You know the loop: the harness **assembles** a
request, the model **answers**, the harness **applies** the answer. A skill is
a way to put instructions into that loop without paying for them in every
request. This page shows how, using the five EGM skills in `skills/` as the
examples.

## Contents

- What a skill is
- Where a skill enters the loop
- Frontmatter
- The description is the trigger
- The body
- Progressive disclosure: references and assets
- Scripts
- Portability
- Testing a skill
- Review questions and exercises

## What a skill is

A folder with a file named `SKILL.md` in it. That file has two parts: YAML
frontmatter between `---` lines, and a markdown body. Anything else in the
folder is optional.

```
goldfish/
├── SKILL.md                        frontmatter + instructions (required)
├── references/runtimes.md          read only when the body says to
├── assets/goldfish-reviewer-prompts.md
├── assets/goldfish-ledger-template.md
└── evals/trigger-evals.json        for you, the author; the model never reads it
```

The format is an open spec at [agentskills.io](https://agentskills.io/specification).
Claude Code, Codex, OpenClaw, Gemini CLI, Cursor, and many others read it.

## Where a skill enters the loop

Think about Aider's repo map. Every request Aider assembles carries a map of
your repo (file names and signatures), but only the most relevant parts of
it, cut to fit a token budget (`--map-tokens`, 1,000 by default). Full file
contents go in only for the files you `/add`. The map is cheap and always
there. The contents are expensive and there on purpose.

Skills work the same way, with one difference that matters: **the model, not
you, decides when the expensive part goes in.**

Three levels, loaded at three different times:

| Level | What | When it is in the request | Rough cost here |
|---|---|---|---|
| 1. Catalog | `name` and `description` of every installed skill | Every request, from the first one | about 175 tokens per EGM skill |
| 2. Body | the rest of `SKILL.md` | From the request after the model asks for it | 3,000 to 3,900 tokens per EGM skill |
| 3. Resources | files in `references/`, `assets/`, `scripts/` | Only after the body tells the model to read or run one | a few hundred to about 1,500 tokens each; a script costs only its output |

Here is what happens when you type "let's design webhook retries before we
write any code" in Claude Code with the EGM skills installed:

```
Request 1  ASSEMBLE  system prompt + tools + skill catalog + your message
                     (the five EGM descriptions are ~900 tokens of the catalog)
           ANSWER    "call the Skill tool: elephant"
           APPLY     harness reads skills/elephant/SKILL.md

Request 2  ASSEMBLE  everything above + the elephant body as a new message
           ANSWER    asks for a slug, opens the design conversation
           APPLY     writes docs/egm/webhook-retries/ELEPHANT.md

   ... many turns later, at Step 5 ...

Request N  ASSEMBLE  everything so far (the body is still there)
           ANSWER    "read references/design-doc-sections.md"
           APPLY     harness reads that one file
Request N+1          now the section guidance is in the request too
```

Some details to notice:

- **The model chose the skill from the description alone.** It had not seen
  the body. Whatever the description doesn't say, the model doesn't know when
  deciding.
- **The body arrives in a later request than the one that triggered it.**
  Loading costs a round trip.
- **Once loaded, the body stays.** Claude Code keeps it in every later request
  of the session and does not re-read the file. So the body should be written
  as standing instructions for the whole task, not one-time steps, and every
  line in it is paid for on every turn after loading.
- **Long sessions get compacted.** When Claude Code summarizes a long
  conversation, it re-attaches only the first 5,000 tokens of each loaded
  skill. Whatever must survive belongs near the top.
- Harnesses differ in mechanism. Some give the model a dedicated tool (Claude
  Code's `Skill` tool); others list each `SKILL.md` path and let the model
  read the file with an ordinary file tool. The three levels are the same
  either way.

Aider, which has no skill support, is the useful contrast. If you
`/read-only` a `SKILL.md`, the whole body rides in every request until you
`/drop` it, needed or not. That is level 2 without level 1.

## Frontmatter

Here is the `goldfish` frontmatter:

```yaml
---
name: goldfish
description: Validates a design doc by spawning three fresh, context-free reviewers in parallel (a comprehension test, a critic review, and an implementation-readiness check), then logs each round in a GOLDFISH.md ledger and loops until critiques are nit-level and the human review gate is resolved. Use when the user says "goldfish test", ... For reviewing code rather than a design doc, use /mean-review.
compatibility: Needs a harness that can start fresh-context subagents, ideally three in parallel ...
---
```

The spec allows six fields:

| Field | Required | Rules |
|---|---|---|
| `name` | yes | lowercase letters, digits, hyphens; up to 64 characters; must match the folder name |
| `description` | yes | up to 1,024 characters; what it does and when to use it |
| `license` | no | a license name or a bundled file |
| `compatibility` | no | up to 500 characters; environment needs (tools, network, product) |
| `metadata` | no | a map of string keys to string values, for your own tooling |
| `allowed-tools` | no | experimental; tools pre-approved to run without asking |

Claude Code accepts more (`argument-hint`, `disable-model-invocation`,
`context: fork`, `hooks`, `paths`, and others). They are real and often
useful, but they exist only in Claude Code. Anthropic's skill packaging
validator rejects them, and other surfaces may too. The EGM skills stay
inside the six so they install anywhere.

A lesson from this suite's own history: the earlier versions had a line
`tools: Read, Write, Edit, Bash, Glob, Grep`. That is a field for *subagent*
files, not skills. Claude Code ignored it without a word, so nobody noticed,
while Anthropic's packaging validator rejects any field outside the spec.
Unknown fields fail silently in one place and loudly in another. Validate
against the spec. (The right skill field, `allowed-tools`, means something
else entirely: it pre-approves tools rather than restricting them.)

## The description is the trigger

The description is the only thing the model sees when it decides whether to
load your skill. It does the work a function signature and a docstring do
together. The elephant description, taken apart:

> **Runs a no-code design conversation for a new feature, refactor, or system
> change, then writes the four-section design doc (...) that becomes the
> source of truth.**

What it does, first, in the third person. The description is pasted into the
model's context next to dozens of others, so "I can help you design" or "You
can use this to..." reads as if someone is talking. Third person reads as a
label. It goes first because harnesses may truncate long descriptions.

> **Use when the user says "design a feature", "let's plan X", "build X", ...
> "design doc first", or otherwise opens a non-trivial design problem, even if
> they did not ask for a document.**

When to use it, with the phrases people actually type. Models tend to
*under*-trigger skills, so the last clause pushes: it names the case where the
user needs the skill but didn't say so.

> **Implements Phases 1 and 2 of the Elephant-Goldfish Model (EGM). Hand the
> finished doc to /goldfish.**

Where it sits, in the article's own numbering. All five skills say this the
same way.

> **Not for one-line fixes or questions about how existing code works.**

The near miss. "Build X" is in the trigger list, and "build" is in half of all
requests. This sentence tells the model where the line is. `goldfish` and
`mean-review` do the same for each other: one reviews docs, the other code.

## The body

Most bodies follow this layout. The exceptions: `elephant` has no
invocation line, and `goldfish` and `mean-review` have no Hard rules
section. Each part is there for a reason.

1. **A title and a short paragraph on the problem.** The model reads *why*
   before *what*. An agent that knows the purpose makes better calls in
   situations the steps don't cover.
2. **An invocation line** (`Invoke as /goldfish [path-to-design-doc]`). This
   documents the argument without using `argument-hint`, which only Claude Code
   understands.
3. **The shared preamble**, the four EGM reflexes. It is copied word for word
   into all five skills. That duplication is deliberate: a skill can't link to
   a file outside its own folder, and you can't count on any one skill being
   installed, so each carries its own copy.
4. **Hard rules**, near the top. They are the instructions that must survive
   compaction and that the model must weigh against everything after.
5. **A checklist** the model copies and ticks off. An Elephant session can run
   for days; the checklist (mirrored by `current_step` in `ELEPHANT.md`) is
   how the session knows where it is.
6. **The steps**, many opening with "**Why this step exists.**" Explaining
   the reason works better than shouting MUST. A model that knows why the
   Goldfish must run in parallel won't "helpfully" pass one reviewer's output
   to the next.
7. **Anti-patterns**: the specific mistakes a model makes here. These are the
   most valuable lines in most skills, and they come from watching real runs.
   The goldfish rule about design docs that link to `docs/egm/` came from a
   real round where reviewers followed that link and read the design
   conversation they were supposed to be blind to.
8. **Where this skill sits in EGM**: the pipeline, what it reads, what it
   writes, who it hands off to. Same shape in all five, so handoffs line up.

### Degrees of freedom

Not every instruction should be equally strict. Match strictness to how
fragile the step is.

- **Low freedom (exact text, exact command).** The no-code prompt in
  `elephant`, the reviewer preamble in `goldfish`, the mean-review framing
  prompt, the `check_gate.py` command. These are narrow bridges: a softer
  rewording of the sycophancy reset lets the spiral come back within a turn.
- **Medium freedom (a template to adapt).** The design doc skeleton and the
  ledger templates in `assets/`.
- **High freedom (goals and heuristics).** The Elephant interview: "ask one or
  two questions at a time", "push on the edges". There is no script for a good
  design argument.

## Progressive disclosure: references and assets

The body says *when* to read each extra file. "See references/ for details"
is too vague; the model either reads everything or nothing. Compare these
lines from the EGM skills:

- `elephant`, on the four doc sections: "Before drafting each one, read its
  entry in references/design-doc-sections.md".
- `goldfish`: "For Cowork, OpenClaw, Hermes, or a runtime with no subagents
  at all, read references/runtimes.md." A Claude Code user never pays for that
  file.
- `egm-implement`: "create it from assets/implement-ledger-template.md".

Two folders, two jobs:

| Folder | Holds | The model... | EGM examples |
|---|---|---|---|
| `references/` | guidance | reads it to decide how to act | `design-doc-sections.md`, `runtimes.md` |
| `assets/` | templates and fixed text | copies it into a file or a message | ledger templates, `goldfish-reviewer-prompts.md`, `readme-templates.md` |

Keep every reference one link away from `SKILL.md`. A model that follows a
link from a reference file to a third file tends to skim it with something
like `head`, and misses the part that mattered.

Templates are worth their file even when short. In the course's own EGM
traces, a ledger header once got reflowed onto one line, and every tool that
read it had to cope. A template keeps the field names exact, and the
`egm-implement` gate script depends on those exact names.

## Scripts

Some steps don't need judgment. They need to be the same every time. Those
belong in a script.

| Skill | Script | Deterministic job |
|---|---|---|
| `egm-implement` | `scripts/check_gate.py` | Is the doc marked ready, and has a human signed off? |
| `mean-review` | `scripts/enforced_scans.py` | The 10-line comment rule, long functions, weak names, swallowed exceptions |
| `peanuts` | `scripts/peanuts_ledger.py` | Which directories are in scope, in what order, and which may be generated now |

Why a script instead of an instruction:

- **It is executed, not read.** Only its output enters the next assembled
  request. The roughly 500 lines of `enforced_scans.py` cost the model
  nothing; its ten-line report costs ten lines.
- **It is the same every run.** The old mean-review text asked the model to
  find "10 or more lines with no comment" using grep. Grep can't do that. The
  model would improvise something different each time, and a finding tagged
  `[enforced]` would mean nothing.

How these scripts are written for an agent, not a person:

- **No prompts.** An agent can't answer "Are you sure? [y/N]". Everything
  comes in as arguments or stdin.
- **`--help` that teaches.** It is how the model learns the interface.
- **Exit codes that mean something.** `check_gate.py` returns 0 for GO, 1 for
  BLOCKED, 2 for a usage error, and 3 for CHECK-BY-HAND, so the skill can say
  exactly what to do for each.
- **Errors that say what to do next.** "docs/egm/nope/ does not exist: run
  /elephant and /goldfish first" beats "Error: not found".
- **Report, don't decide.** None of the three scripts changes a gate or a
  status. `check_gate.py` never sets `human_review_gate`, and
  `peanuts_ledger.py` never marks a directory `approved`. The scripts measure;
  people decide. That split is the whole EGM philosophy in miniature.

Scripts are referenced by a path relative to the skill's folder
(`<skill-dir>/scripts/check_gate.py`), because the skill could be installed
anywhere.

## Portability

These skills run in more than one harness, so they are written for the
lowest common denominator:

- Frontmatter uses only the six spec fields.
- Steps name the job ("spawn three fresh subagents in one message"), and a
  reference file maps the job onto each harness's tool names.
- Every script is standard-library Python, and each skill says what to do by
  hand if Python is missing.

## Testing a skill

Seeing a skill trigger tells you the model found it. It doesn't tell you the
skill helped. Two separate questions, two kinds of test:

1. **Does it trigger on the right requests?** Each EGM skill has
   `evals/trigger-evals.json`: six requests that should load it and six near
   misses that should not. Run each in a fresh session and record what loads.
2. **Does it do better than no skill?** Run a realistic task with the skill
   and again with it turned off, each in a fresh session, and compare. Fresh
   matters: the session where you wrote the skill knows things the skill
   doesn't say.

Anthropic's `skill-creator` skill automates both loops. The second one is a
Goldfish test for skills: does the instruction carry the intent without the
author in the room?

## Review questions and exercises

1. In your own words, which of the three levels is in *every* request your
   harness assembles, and why does that make the description the most
   carefully worded part of a skill?
2. Install the EGM skills in Claude Code, start a session, and run
   `/context` before and after `/elephant` loads. How much did the request
   grow? Compare it with the table above.
3. Take `skills/mean-review/evals/trigger-evals.json`. For each of the six
   should-not-trigger requests, write one sentence saying which words in it
   could fool a naive keyword match. Then add two near misses of your own.
4. Find one instruction in any EGM body that you think is redundant, the kind
   of thing the model would do anyway. Delete it in a copy, run the same task
   both ways, and report whether anything changed.
5. `goldfish` keeps its runtime table in `references/` but its reviewer
   prompts in `assets/`. Argue for or against moving the prompts into
   `SKILL.md` itself. What does each choice cost, per request?
6. Aider has no skill loader. Design one: what would your harness put in the
   assembled request at level 1, what tool would the model call to reach level
   2, and how would you keep a loaded body from riding along forever?
7. Write a small skill of your own (one `SKILL.md`, under 60 lines) for a
   task you repeat in this course. Write its description first, and five
   trigger tests before the body.
