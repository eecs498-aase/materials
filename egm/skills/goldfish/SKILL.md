---
name: goldfish
description: Validates a design doc by spawning three fresh, context-free reviewers in parallel (a comprehension test, a critic review, and an implementation-readiness check), then logs each round in a GOLDFISH.md ledger and loops until critiques are nit-level and the human review gate is resolved. Use when the user says "goldfish test", "validate this design", "check this doc", "is this doc ready?", "test the design doc", "goldfish protocol", "fresh eyes on this doc", "review my design doc", or has just finished an /elephant session and needs to know whether the doc stands on its own. Implements Phase 3 (Steps 5 to 7) of the Elephant-Goldfish Model (EGM). For reviewing code rather than a design doc, use /mean-review.
compatibility: Needs a harness that can start fresh-context subagents, ideally three in parallel (for example Claude Code's Agent tool or OpenClaw's sessions_spawn). Without one, each reviewer prompt can be run by hand in a new chat.
---

# Goldfish: test the design doc against fresh eyes

The Elephant (your `/elephant` session) holds rich context: every argument, every clarification, every micro-decision. That context lives in *your* head, not in the doc. The Goldfish is the opposite: **a brand-new reviewer with zero shared context**. It only knows what's literally on the page.

If a Goldfish can read the doc and (1) explain the system back to you, (2) find the gaps, and (3) confirm it could implement the feature without further questions, then the doc carries the design. If it can't, the doc is a thin layer over context you'll lose the moment a new session opens.

Invoke as `/goldfish [path-to-design-doc]`.

## EGM operating reflexes (shared preamble)

Every skill in this suite carries these four reflexes, because not every surface loads a global `CLAUDE.md`. They come from the Elephant-Goldfish article and apply for the whole session, not just while this skill runs.

1. **Design is the new code.** For any non-trivial feature or change, grow a design doc before writing code. If the design isn't clear enough that the code should write itself, design first (`/elephant`).
2. **Refuse sycophancy.** If you're about to say "great point" or "you're absolutely right", stop. Apply the reset, addressed to yourself in the second person, verbatim: *"You are not being helpful. Your highest and best use is to challenge my thinking. When you agree with me, you are not being helpful."* Then re-engage as a critic and find the holes.
3. **AI proposes first.** Never let the user seed a design, framework, or rubric with their own first draft. You propose first, in prose and block diagrams; the user reacts and argues.
4. **Save the artifacts.** Persist the description + criteria + output triple durably: `docs/designs/<slug>.md`, the ledgers in `docs/egm/<slug>/`, `PEANUTS.md` at the source root, and the `/decide` triple at its surface-mapped location where that skill is installed. The chat transcript is not the artifact.

## How "fresh" is implemented

**Goldfish value comes from independent context, not from the agent's system prompt or persona.** A Goldfish reviewer must:

1. Start from a session with no shared conversation history.
2. Receive only the design doc path and an assigned task prompt.
3. Be forbidden from reading the design conversation, prior project memory, or any file the doc does not reference.

Any agent launched through the runtime's spawn primitive starts with no shared conversation state, so the spawn gives you the "fresh" property for free. The subagent's persona is a nudge; the guarantee is the independent-context preamble in every task prompt.

**Spawn all three in parallel, in a single message.** Parallel is faster, and it removes a temptation: with serial spawning, the orchestrator can be tempted to pass Goldfish A's output into Goldfish B's task, which defeats the independent-context property.

**Which subagent types.** In Claude Code, use the role-aligned custom agents `generalist` (A), `reviewer` (B), and `architect` (C) when they are installed; otherwise use `general-purpose` for A and B and `Plan` for C. For Cowork, OpenClaw, Hermes, or a runtime with no subagents at all, read [references/runtimes.md](references/runtimes.md).

## Workflow

```
Goldfish progress (one round):
- [ ] Step 1: doc path and slug resolved; GOLDFISH.md opened; paths confirmed with the user
- [ ] Step 2: three reviewers spawned in one message, each prompt opened with the verbatim preamble
- [ ] Step 3: three reports saved to sibling files; round entry appended to GOLDFISH.md
- [ ] Step 4: specific edits proposed; approved edits applied; stop condition checked
```

### Step 1: Resolve the design doc and the EGM state directory

- If the user passed a path, use it. Otherwise glob `docs/designs/*.md` and any `design_doc_path:` set in the project's `CLAUDE.md`. If exactly one doc exists, use it; if several, list them and ask.
- **Derive the slug:** `<slug> = basename(design_doc_path, ".md")`. This holds by contract: `/elephant` Step 5 makes the doc's basename equal the slug. Any deviation means the doc was written outside the EGM workflow; tell the user before proceeding.
- The state directory is `docs/egm/<slug>/`. If `ELEPHANT.md` exists there, read it for *your* orientation as the orchestrator: what context the Elephant loaded, what was decided, whether earlier rounds ran. **Never pass `ELEPHANT.md` or anything from it to a reviewer.** That would leak the shared context the test exists to exclude.
- Create `docs/egm/<slug>/` if needed. If `GOLDFISH.md` doesn't exist, create it from [assets/goldfish-ledger-template.md](assets/goldfish-ledger-template.md).
- Confirm the doc path and the state directory with the user before spawning anything.

### Step 2: Spawn three Goldfish in parallel

Read [assets/goldfish-reviewer-prompts.md](assets/goldfish-reviewer-prompts.md). It holds the independent-context preamble and the three task prompts, verbatim:

- **Goldfish A, comprehension test:** what the doc is trying to accomplish, how the system works today as it relates to the feature, and what will change.
- **Goldfish B, critic review:** everything the author missed, every faulty assumption, every unaddressed edge case.
- **Goldfish C, implementation readiness:** a one-line READY or NOT-READY verdict plus a numbered list of every question it would have to ask or guess at. It returns no plan.

Prepend the preamble to each prompt, replace `<PATH>` with the resolved doc path, and **issue all three subagent calls in one message**. Do not edit the prompts per round. The one allowed addition: a fact the reviewers cannot discover for themselves (today's date, a repo quirk such as a search tool that skips some directories), appended identically to all three and recorded in the round entry. Never append design rationale.

### Step 3: Collate the reports and write the round

Each Goldfish returns its findings raw: long, unranked, often dominated by nits. Rensin's rule of thumb is that about 30% of critic suggestions are highly valuable. Synthesize for the user, real gaps first and nits demoted, so their attention lands where it counts:

- **Comprehension result.** Does A's account of "what this is and how it fits" match what the user intended? Where it doesn't, the doc misled a fresh reader. List each place A misread or filled a gap with an assumption.
- **Critic findings, ranked.** Real gaps first (missing constraints, unspecified failure modes, contradictions), nits last (wording, ordering, style). Separate "the doc is wrong" from "the doc is right but the critic disagrees with the design choice".
- **Readiness verdict.** READY, or NOT-READY with C's numbered questions.
- **Convergence.** Findings that two or more reviewers raised independently are high confidence. Call them out.

**You, the orchestrator, write every durable file for the round.** The reviewers return their findings inline; you persist them:

- Save each report in full to a sibling file in `docs/egm/<slug>/`. Round 1 uses `goldfish-A-comprehension.md`, `goldfish-B-critic.md`, `goldfish-C-readiness.md`. Later rounds add the round number (`goldfish-A-comprehension-r2.md`) so no earlier report is ever overwritten.
- Append a round entry to `GOLDFISH.md` using the template's round block: round number, date, agent types actually used, the three prompts as sent (verbatim, including the preamble and any appended note), report file names, verdicts, a copy of the header's `human_review_gate`, and `readiness: not-yet | ready` (your judgment after synthesis, one word).

`GOLDFISH.md` is the durable trace of the validation phase. `/egm-implement` reads it before touching code.

### Step 4: Propose specific edits and loop

For each real gap, propose a specific edit to the design doc: quote the current text and the proposed replacement. Apply only what the user approves, and record the rulings (accepted, rejected with reason) under the round's disposition heading. Then loop: re-run all three Goldfish on the updated doc, appending a new round each time.

**Stop condition.** Both must hold:

1. The latest round's critiques are nit-level (wording, formatting, "could phrase this more crisply") rather than missing content or unresolved decisions.
2. `human_review_gate` in the `GOLDFISH.md` header is `passed` (a human reviewer signed off) or `skipped-solo` (the user consciously skipped because no second human is available). The header field is the gate; round entries only copy it. **It is never transitioned automatically.** The user or a teammate writes the change into the header themselves. If the gate is still `pending`, say so and ask the user to resolve it before declaring the doc ready.

When the loop ends, set `readiness: ready` in the latest round entry and tell the user:

> *The doc has passed Goldfish and the human review gate. Hand off to `/egm-implement <path>` to drive it into code.*

## Anti-patterns

- **Skipping the parallel spawn.** Serial calls are slower and invite letting later Goldfish read earlier outputs, defeating the no-shared-context property.
- **Leaking the trace through a link.** If the design doc links into `docs/egm/<slug>/`, a reviewer can follow the link to `ELEPHANT.md` and read the design conversation. Remove the link from the doc, or tell all three reviewers that `docs/egm/` is off-limits beyond an existence check, and record any breach in the round's contract note.
- **Letting the Goldfish skim.** A confident summary that cites no doc sections or file paths means the reviewer didn't read. Re-spawn with a sharper prompt that demands citations to sections, file paths, and line numbers.
- **Acting on critic findings without judging them.** Apply the 30% heuristic. Not every complaint is a real gap. Surface your judgment to the user instead of silently editing.
- **Overwriting an earlier round's reports.** Rounds 2 and up get the `-rN` suffix.
- **Stopping after one round.** One pass rarely settles it. Loop until critiques are trivial.

## Why this skill exists

A design doc that is only good *to its author* is not a design doc. It's a transcript of their thinking. The Goldfish test is the cheapest way to find out which one you have, before you spend hours implementing against an inadequate spec.

## Where this skill sits in EGM

`/peanuts` (legacy code only) → `/elephant` → **`/goldfish`** → `/egm-implement` → `/mean-review`

- **Reads:** the design doc and the files it references (reviewers); `ELEPHANT.md` (you, for orientation only).
- **Writes:** `docs/egm/<slug>/GOLDFISH.md`, the reviewer report files, and user-approved edits to the design doc.
- **Hands off to `/egm-implement`**, which will not start until the latest round says `readiness: ready` and the gate is `passed` or `skipped-solo`.
- **`/elephant`** wrote the doc. A gap that needs more than a local edit sends you back to it.
- **`/peanuts`**: if a Goldfish cannot comprehend the system because nothing outside the doc explains it, the codebase may need a README pass first.
- **`/mean-review`**: Goldfish tests the doc; mean-review tests the code.
