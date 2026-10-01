---
name: peanuts
description: Bootstraps a legacy codebase for AI work by generating a bottom-up hierarchy of README.md files (peanuts at the leaves, hay at the branches), with a human review gate at every level and progress tracked in a PEANUTS.md ledger, so a fresh session can load the project's context cheaply. Use when the user says "bootstrap this codebase", "generate READMEs", "feed the elephant", "peanuts and hay", "add context files for AI", "document this monolith", "README hierarchy", "onboard me onto this codebase", or wants a fresh AI session to understand a large existing project without reading every source file. Implements the "feeding the Elephant peanuts and hay" bootstrap of the Elephant-Goldfish Model (EGM). Not for greenfield projects whose design docs already cover the code.
compatibility: Uses python3 (standard library only) for scripts/peanuts_ledger.py; uses git, when present, to respect .gitignore.
---

# Peanuts: feed the Elephant peanuts and hay

A million-line codebase is "the entire jungle." Point an AI at it and the model chokes: it loses context, gets confused, hallucinates. The fix is a hierarchy of small, compressed, high-nutrition summaries, **a README.md in every directory**, written by recursive bottom-up summarization. Peanuts at the leaves, hay at the branches.

With that hierarchy in place, a fresh session at the repo root can feed on just the READMEs and understand the major subsystems almost at once, using a small fraction of the context window it would burn reading source. This skill drives that process.

Invoke as `/peanuts [source-root]`.

## EGM operating reflexes (shared preamble)

Every skill in this suite carries these four reflexes, because not every surface loads a global `CLAUDE.md`. They come from the Elephant-Goldfish article and apply for the whole session, not just while this skill runs.

1. **Design is the new code.** For any non-trivial feature or change, grow a design doc before writing code. If the design isn't clear enough that the code should write itself, design first (`/elephant`).
2. **Refuse sycophancy.** If you're about to say "great point" or "you're absolutely right", stop. Apply the reset, addressed to yourself in the second person, verbatim: *"You are not being helpful. Your highest and best use is to challenge my thinking. When you agree with me, you are not being helpful."* Then re-engage as a critic and find the holes.
3. **AI proposes first.** Never let the user seed a design, framework, or rubric with their own first draft. You propose first, in prose and block diagrams; the user reacts and argues.
4. **Save the artifacts.** Persist the description + criteria + output triple durably: `docs/designs/<slug>.md`, the ledgers in `docs/egm/<slug>/`, `PEANUTS.md` at the source root, and the `/decide` triple at its surface-mapped location where that skill is installed. The chat transcript is not the artifact.

## When to use this skill

- The user has a legacy codebase with no design docs and is starting to use AI on it.
- A fresh AI session can't make sense of the project because there's too much surface area.
- The user wants to onboard a new engineer, or themselves, onto an unfamiliar repo.
- The user says one of the trigger phrases.

**Don't use it** for a greenfield project with rigorous design docs: there, the design docs cover the code and READMEs are redundant. Once design docs cover 100% of the code files, the READMEs can be deleted (or not; the user's call).

## Hard rules

1. **Bottom-up only.** Never generate a README for a directory while any immediate in-scope child is `pending`, `needs-human-review`, or `blocked`. Bad leaves compound up the tree.
2. **Never decide that a README is approved.** A human's sign-off moves a directory to `approved`: their own edit to the ledger, or a review task they closed. The whole point of the gate is that the AI is not the judge.
3. **`PEANUTS.md` drives the run.** It is the skill's ledger and the source of truth for progress, on the first run and on every resume.

## Ledger statuses

Every directory in `PEANUTS.md` has exactly one status. Five states map the lifecycle (not done, awaiting review, ready, consumed) plus a sideband for failures. Fewer would conflate "haven't tried" with "tried and waiting"; more would be ceremony.

- `pending`: not yet generated.
- `needs-human-review`: README written by this skill, awaiting human review.
- `approved`: a human signed off. The parent may roll up once every sibling is `approved`.
- `rolled-up`: the parent README has consumed this child's README; nothing further to do.
- `blocked`: generation was attempted and failed (missing files, ambiguous purpose, user deferred it). Surface it on the next resume.

## The ledger script

`scripts/peanuts_ledger.py` does the deterministic parts: finding what's in scope, ordering it, writing the initial ledger, and applying the hard gate. Run it from anywhere, giving the source root (`<skill-dir>` is the folder that holds this SKILL.md):

```bash
python3 <skill-dir>/scripts/peanuts_ledger.py plan <root>   # in-scope dirs, deepest first; changes nothing
python3 <skill-dir>/scripts/peanuts_ledger.py init <root>   # writes <root>/PEANUTS.md, all pending; never overwrites
python3 <skill-dir>/scripts/peanuts_ledger.py next <root>   # review queue, blocked, eligible now; changes nothing
```

Add `--exclude <dir>` (repeatable) to leave a subtree out; `init` records the excludes in the ledger and `next` reuses them. Add `--json` for structured output. A directory is in scope when it holds source files or has an in-scope subdirectory; `.gitignore`, vendored, and generated trees are skipped.

`next` works one level at a time, deepest first. The **current level** is the deepest depth that still has a `pending` or `needs-human-review` row. A row is **eligible** when it is `pending`, at the current level, and every immediate in-scope child is `approved` or `rolled-up`. A directory missing from the ledger counts as an unfinished child, and a row that doesn't parse is a ledger problem. The verdict is one of `FIX-LEDGER` (an unparseable row, an unknown status, or a gate violation; exit 1), `REVIEW-FIRST` (the current level has rows awaiting review), `GENERATE`, `STUCK` (only blocked work remains), or `DONE`.

You update statuses by editing the `status` column of `PEANUTS.md`. The script never changes a status.

If Python isn't available, do the same by hand: list the directories with `git ls-files`, sort deepest first then by path, and check each parent's children before rolling up.

## Workflow

```
Peanuts progress:
- [ ] Step 0: root confirmed; plan shown; ~50% leaf error rate warned; PEANUTS.md created or read
- [ ] Step 1: leaf batch generated; each leaf marked needs-human-review with its uncertainties
- [ ] Step 2: review queue surfaced; wait for the human to approve or correct
- [ ] Step 3: branch READMEs rolled up level by level, each gated the same way
- [ ] Step 4: root README written and approved
```

### Step 0: Scope and confirm

Before touching files:

1. Identify the root of the source tree to document. Default to the current working directory; confirm with the user.
2. Run `plan`. Show the user the shape: number of directories, number of leaves, deepest level. Offer `--exclude` for anything that shouldn't get READMEs. Get a thumbs up before proceeding.
3. Warn the user now about the leaf error rate: **expect about 50% of leaf descriptions to be wrong**, because at the leaves the AI has only the code to go on. The article budgets 5 to 10 minutes of human fixing per leaf. This is not optional, and they need to know before they start.
4. If `PEANUTS.md` doesn't exist, run `init`. If it does, you are resuming: run `next` and show the user where things stand.

### Step 1: Leaf directories (the peanuts)

Run `next` and take the eligible directories at the current level (on the first pass, the deepest leaves). **Everything eligible at one level may be batched**, because generation is not the judgment gate; the human review afterward is. For each leaf in the batch, keeping each leaf's reasoning separate from the others:

1. Read every code file in the directory (skip vendored and generated code).
2. Write `README.md` there, using the leaf shape in [assets/readme-templates.md](assets/readme-templates.md): a **Purpose** paragraph and a **File index** with one line per file. Use the article's prompt as the frame:

   > *Read the files in this directory and produce a new file named README.md. This file should (a) explain the purpose of this directory and the files contained in it and (b) enumerate each file in the directory and a short description of its function.*

3. Set the leaf's status to `needs-human-review` in `PEANUTS.md`, with the date in `updated` and, in `notes`, the descriptions you are least sure about: ambiguous function names, files whose purpose isn't obvious from the code, integration glue.

### Step 2: Hand the batch to a human

After the batch, surface the review queue:

> *I generated leaf READMEs for: [list]. All are `needs-human-review` in `PEANUTS.md`. The descriptions I'm least sure of: [for each README, the specific files or lines]. Please skim each and either (a) set it to `approved` in the ledger, or (b) tell me what to correct. I won't generate any parent README until every immediate child is `approved`; bad leaves compound up the tree.*

If the environment has a task system, create one user-blocked review task per leaf, pointing at the README. A task the human closes counts as their sign-off: record `approved` for that directory and note the closed task in `notes`.

When `next` says `REVIEW-FIRST`, surface the queue again before generating anything else.

### Step 3: Non-leaf directories (the hay)

When `next` lists a branch as eligible (it is at the current level and every immediate child is `approved` or `rolled-up`), write its README this way. Any leaf eligible at the same level goes in the same batch but follows Step 1.

1. Read **all the README.md files in its immediate subdirectories**.
2. Read **the code in this directory only**: files at this level, not recursively.
3. Write `README.md` using the branch shape: **Purpose** (its role in the larger system), **how the parts fit** (subsystem composition), and a **file index** for files at this level. Use the article's prompt as the frame:

   > *Please read all the README.md files in all the subdirectories below me, then read the code in just this directory and create a file here named README.md. Using that information this file should (a) explain the purpose of this directory and the files contained in it and (b) enumerate each file in the directory and a short description of its function.*

4. Update `PEANUTS.md`: each immediate child becomes `rolled-up`; this directory becomes `needs-human-review`.

Branch accuracy is much better than leaf accuracy, because the children's summaries anchor the model, but still note anything you're unsure of. The same gate applies: the grandparent waits until this README is `approved`.

### Step 4: The root README

At the repo root, write the top-level README using the root shape: a map of the major subsystems that gives a fresh session enough of a mental model to know which subtree to descend into for any task. This is the file a new session reads first. Mark the root `needs-human-review`; once a human approves it, the bootstrap is done and `next` says `DONE`.

### The retirement clause

Every README ends with this line, unchanged (the templates include it):

> *This README exists to give AI sessions cheap context. It can be retired once design docs cover the files in this directory at least once. See `/elephant` for the design doc process.*

It tells future readers the README is scaffolding, so nobody preserves a stale README after design docs supersede it.

## Anti-patterns

- **Generating level N before level N+1 below it is approved.** Batch within the current level; never across levels. `next` enforces this.
- **Bundling unrelated leaves into one write.** One leaf's README is one write. Keep each leaf's reasoning isolated.
- **Documenting vendored or generated code.** `node_modules/`, `vendor/`, `target/`, `dist/`, `.venv/`, `__pycache__/`: skip them.
- **Long READMEs.** Half a page for a leaf, a page for a branch, one to two for the root. Three pages means the model is over-explaining; rewrite for concision.
- **Auto-approving.** Never transition `needs-human-review` to `approved` without a human's sign-off.

## Why this works

`sizeof(docs) << sizeof(code)`. A fresh session loaded with the README hierarchy gets a working mental model of the codebase for a small fraction of the context it would burn reading source, and can spend the rest on the actual problem instead of re-bootstrapping.

The bonus: once a codebase is documented this way, onboarding a new engineer becomes "load these READMEs into a notebook tool, hand it to them, and ask them to write a design doc for their first feature." See `/elephant` for that protocol.

## Where this skill sits in EGM

**`/peanuts`** (legacy code only) → `/elephant` → `/goldfish` → `/egm-implement` → `/mean-review`

- **Reads:** the source tree, one directory at a time, bottom-up.
- **Writes:** a `README.md` per in-scope directory and `PEANUTS.md` at the source root.
- **Hands off to `/elephant`**, whose Step 1 loads the README hierarchy instead of the raw source. Design docs then supersede the READMEs over time.
- **`/goldfish`**: design docs must pass the Goldfish test; READMEs are scaffolding and don't need that rigor.
- **`/mean-review`**: run it on any leaf README you don't trust before it is approved.
