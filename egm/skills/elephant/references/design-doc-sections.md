# The four sections of an EGM design doc

Read the entry for a section right before you draft it (Step 5). Each entry
says what the section is for, what good looks like, and how it usually goes
wrong.

## Contents

- Section 1: Problem
- Section 2: Technical Plan
- Section 3: Alternatives
- Section 4: Detailed Implementation

## Section 1: Problem (3 to 5 sentences, plain English)

What is the user trying to solve? Why does it matter? Who's affected? No
jargon. A non-engineer should be able to read it and understand the business
problem.

If it runs past 5 sentences, you are either solving more than one problem or
you have drifted into the technical plan. Trim.

**Weak:** "We need to refactor the webhook module to use a queue with
exponential backoff."
(That is a solution, not a problem.)

**Better:** "When a customer's server is down, we drop the webhook and they
never learn their order shipped. Support hears about it days later. About 2%
of deliveries fail this way, mostly during customers' own deploys. We need
deliveries to survive a receiver that is briefly unavailable."

## Section 2: Technical Plan (jargon-light, block diagram)

The big components and how they fit together. A block diagram if it helps
(ASCII or mermaid). The goal is **explanatory prose**: text someone can read
in one sitting and come away with a clear mental model of what is being
built. Light on jargon. Heavy on intent and flow.

Goes wrong when it turns into a file list (that is Section 4) or a list of
technologies with no account of how data moves between them.

## Section 3: Alternatives (rejected ideas, and why)

This section is **critical for guardrails**. Document every approach that came
up during the design conversation and was rejected, with the reason. When a
future session (AI or human) asks "why didn't you just use X?", this section
is the answer. Without it, every debate re-runs from scratch, and a model will
happily propose alternatives that were already ruled out.

Be specific. "We considered putting this in the auth layer instead of the
middleware. Rejected because the auth layer doesn't see preflight requests,
and we need to handle those." Not "we considered other approaches and
rejected them."

Your `## Interview decisions` notes in `ELEPHANT.md` are the raw material.

## Section 4: Detailed Implementation (the longest section)

For every file that will be **created** or **changed**, list:

- the path,
- what changes (new functions, modified functions, deleted code),
- why: the rationale, tied back to the Technical Plan.

**Demand exhaustiveness.** If you catch yourself writing "and similar changes
to the other handlers", stop and enumerate them. This section nails the
implementation to specific files so it cannot wander: `/egm-implement`
refuses to touch any file that is not listed here. Vague implementation
sections produce vague implementations.

A good Detailed Implementation section is long and slightly tedious. That is
correct. If yours is short, you are missing files.

Order the entries however reads best. `/egm-implement` re-sequences into
dependency order (producers before consumers) when it builds, and logs the
change of order.
