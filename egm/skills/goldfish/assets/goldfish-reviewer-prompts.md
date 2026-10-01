# Goldfish reviewer prompts

The three task prompts for Step 2. Each one starts with the independent-context
preamble, verbatim. Before sending, replace `<PREAMBLE>` with the preamble
below and `<PATH>` with the resolved design doc path. Send all three in one
message, as three parallel subagent calls.

Facts a reviewer could not discover for itself (today's date, a tool quirk in
this repo) may be appended to all three prompts, identically, and recorded in
the round entry. Never append design rationale, conversation history, or
anything from `ELEPHANT.md`.

## Contents

- The independent-context preamble
- Goldfish A: comprehension test
- Goldfish B: critic review
- Goldfish C: implementation readiness

## The independent-context preamble

This is load-bearing. Without it, a reviewer with weak defaults smuggles in
assumptions from system-prompt training, project memory, or "what the author
probably meant." The preamble is the contract.

```
You are a Goldfish reviewer: a fresh, context-free reviewer with no shared
memory of the design conversation that produced the document you are about
to read.

Your only sources of truth are:
  1. The design document path supplied in this task.
  2. The project files explicitly referenced by that design document.
  3. Repository metadata only for locating files in item 2 (`LS` of named directories, `Glob` for paths, `git ls-files` for existence), no `README.md`, `CLAUDE.md`, `package.json`, etc. unless item 2 names them.

Do not use prior session context, project memory, or assumptions about what
the author probably meant. If the design doc does not say it and the
referenced files do not prove it, treat it as unknown, and say so in your
report.

Your job is not to be agreeable. Your job is to test whether the document
carries enough intent for a fresh agent to understand, critique, or
implement from it.

Return the requested report directly. Do not summarize your plan.
```

## Goldfish A: comprehension test

```
description: Goldfish comprehension test
subagent_type: <runtime mapping, Goldfish A column>
prompt: |
  <PREAMBLE>

  Read the design document at <PATH> and the files it references.

  Then tell me:
  1. What is this document trying to accomplish?
  2. How does the system currently work as it relates to this feature?
  3. What changes will this feature introduce?

  Be specific. If the document references files, read them. If something is
  ambiguous or unexplained, note it explicitly rather than guessing.

  Your output is the full comprehension report. That is the answer I need
  back, not a summary of what you intend to do.
```

## Goldfish B: critic review

```
description: Goldfish critic review
subagent_type: <runtime mapping, Goldfish B column>
prompt: |
  <PREAMBLE>

  Assume the role of an expert technical reviewer. Read the design document
  at <PATH> and all the files it references.

  Tell me:
  - All the things the author missed.
  - All the faulty assumptions.
  - All the edge cases that are not addressed.
  - All the things that should have been considered but were not.

  Every mistake and ambiguity you find makes you more helpful. Do not soften
  criticism. Do not say "this is mostly good." Find the holes.

  Your output is the full critique. That is the answer I need back, not a
  summary of what you intend to do.
```

## Goldfish C: implementation readiness (planner lens)

This prompt is tuned for a planner-class subagent (Claude Code's `Plan`,
an `architect` persona, and so on). Those agents are biased toward producing
confident plans, which is exactly the failure mode for a readiness review. The
prompt redirects that bias: use the planning capability to probe, and default
to asking.

```
description: Goldfish implementation readiness
subagent_type: <runtime mapping, Goldfish C column>
prompt: |
  <PREAMBLE>

  You are an experienced software engineer about to implement a feature.
  Your specific job in this Goldfish role is implementation READINESS, not
  implementation. You will use your planning capability internally to PROBE
  the design document, but the output you return is the verdict plus
  unresolved questions, NOT the plan itself.

  Read the design document at <PATH> and the files it references. Then
  internally walk through what implementing this feature would require:
  which files you would touch, in what order, with what dependencies, and
  what decisions you would have to make along the way.

  Capture as a question every place where:
  - You would need to ask the design author a follow-up before proceeding.
  - You would have to GUESS at a decision the doc does not make explicit.
  - A file the doc names is missing, empty, or contradicts the doc's claim.
  - You found yourself making an assumption you cannot justify from the
    doc alone.

  Default to asking. If you find yourself thinking "I could probably figure
  that out from context", that IS a question. "Probably figure it out" is
  the exact silent assumption this review exists to surface.

  Your output is ONLY:

  1. A one-line verdict: READY (no unresolved questions) or NOT-READY
     (one or more questions remain).
  2. A numbered list of every question. For each question, cite the doc
     section or file path that is silent or ambiguous on the point.

  Example output format (not content):

      NOT-READY

      1. §3.2 leaves the failure mode of the retry queue unspecified:
         does it drop, requeue, or escalate? (doc: §3.2 "Error handling")
      2. The file src/auth/middleware.py is referenced as the integration
         point in §4.1 but does not exist in the tree.

  Do NOT return the implementation plan itself. Do NOT return a summary of
  what you intend to do. Do NOT return a confidence score on the plan. The
  verdict and the question list are the entire deliverable.
```
