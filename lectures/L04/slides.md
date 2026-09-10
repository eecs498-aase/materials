---
theme: ../theme
title: "L04: Spec-Driven Coding"
info: |
  EECS 498 AASE — Lecture 04
  Applied Agentic Software Engineering, UMich Fall 2026
layout: title
class: text-left
transition: fade
mdc: true
highlighter: shiki
---

# Spec-Driven Coding

## Lecture 04 · Sep 10, 2026

<!--
The last technique before you build. Today: IDKs + specs + Architect Mode.
After today they have everything for Lab01 and the build. RED
-->

---
layout: default
---

<div class="label">Where we are</div>

# Today: the Prompt lever

<div class="mt-6 space-y-2">

- L03 gave you three levers and one instruction: be concrete
- The failure that dominates is still missing context
- A well-structured prompt changes how you manage context too

</div>

<div class="caption mt-6">Concrete was the instruction. Today it becomes a discipline.</div>

<!--
Don't re-teach the Big Three. One line, then move. The third bullet is the
one worth landing: a spec names its own file boundaries, so writing one is
context management whether or not you call it that.
-->

---
layout: default
---

<div class="label">Four things</div>

# What you leave with today

<v-clicks>

- The vocabulary of a precise prompt
- The structure that scales it past one request
- When a spec is worth writing, and when it is not
- Architect Mode, which runs a spec in one pass

</v-clicks>

<div class="caption mt-6">Everything here is aimed at Lab01 and the build that follows it.</div>

<!--
Four clicks, four things, no elaboration on any of them. Each one gets its
own block later. This slide exists so they can tell where they are when the
lecture turns.
-->

---
layout: section
---

# IDKs

## Information Dense Keywords

<!--
Divider. Say what the acronym stands for once, out loud. IDK is not a term
they have met and it is about to be on every slide. GREEN
-->

---
layout: two-col
---

## Vague

```text
Add another way
to output the data.
```

<div class="text-sm opacity-70 mt-4">Model guesses every detail.</div>

::right::

## IDK-rich

```text
CREATE output_format.py with
  format_as_html(...) -> str
UPDATE main.py: ADD html
  to --output-format choices
```

<div class="text-sm opacity-70 mt-4">Nothing left to guess. Usually right the first time.</div>

<!--
Same codebase, same context, two prompts for the same task.

Read the vague one, then list what the model has to guess: a text file
instead of HTML, no CLI change, a print() where a function belonged. Any one
of those guesses can be wrong.

Then the right column, where nothing is left to guess.

The line to land: this is the difference between a prompt you keep
re-running with different words and one that lands the first time.
-->

---
layout: default
---

<div class="label">Action keywords</div>

# The vocabulary

<div class="grid grid-cols-2 gap-4 mt-6 items-stretch">
  <div class="card">
    <div class="flex items-center gap-3 mb-2">
      <ph-plus-circle-bold class="text-2xl text-amber-600 shrink-0" />
      <div class="font-semibold">CREATE · ADD</div>
    </div>
    <div class="text-sm opacity-70">CREATE makes what does not exist. ADD appends to what does.</div>
  </div>
  <div class="card">
    <div class="flex items-center gap-3 mb-2">
      <ph-pencil-simple-bold class="text-2xl text-blue-600 shrink-0" />
      <div class="font-semibold">UPDATE · REPLACE</div>
    </div>
    <div class="text-sm opacity-70">UPDATE modifies in place. REPLACE swaps the implementation.</div>
  </div>
  <div class="card">
    <div class="flex items-center gap-3 mb-2">
      <ph-minus-circle-bold class="text-2xl text-blue-600 shrink-0" />
      <div class="font-semibold">DELETE · REMOVE</div>
    </div>
    <div class="text-sm opacity-70">DELETE takes out the whole thing. REMOVE takes out one line or argument.</div>
  </div>
  <div class="card">
    <div class="flex items-center gap-3 mb-2">
      <ph-copy-bold class="text-2xl text-blue-600 shrink-0" />
      <div class="font-semibold">MOVE · MIRROR</div>
    </div>
    <div class="text-sm opacity-70">MOVE relocates code. MIRROR copies a pattern into a new file.</div>
  </div>
</div>

<div class="caption mt-4">The pair is the point. ADD ≠ CREATE.</div>

<!--
Four pairs, eight verbs. Read the pairs, do not define each verb.

CREATE and ADD is the pair that matters, which is why it is the amber card.
ADD appends to something that exists, CREATE generates net new. Pick the
wrong one and the model does the wrong thing.
-->

---
layout: statement
---

`[ACTION] [LOCATION]: [DETAIL]`

<!--
The pattern. Repeatable. Compact. Predictable. YELLOW
-->

---
layout: default
---

<div class="label">Examples</div>

# Pattern in practice

```text
CREATE main.py with
  analyze_transcript(filepath: str) -> TranscriptAnalysis

UPDATE output_format.py: ADD
  format_as_yaml() after format_as_json()

DELETE main.py: REMOVE
  the unused print_debug() function
```

<!--
Three examples, read as instructions rather than as text on a slide.

The point is cost. The pattern is shorter to write than a paragraph, not
longer, and it usually lands the first time instead of costing three rounds
of iteration.
-->

---
layout: default
---

<div class="label">Why IDKs work — L02 callback</div>

# Narrow the sampling distribution

- Vague prompt → wide distribution → model picks training-prior
- Precise prompt → narrow distribution → model picks what you said
- IDKs work because of *mechanics*, not English fluency

<!--
The L02 callback, and the slide that stops IDKs from sounding like a style
preference. Autoregressive sampling: a vague prompt leaves the distribution
wide, so the model picks the most common completion in its training data. A
precise prompt narrows it, so the model picks what fits your constraints.

Say the last bullet plainly. IDKs work because of the mechanics, not because
the model understands English better.
-->

---
layout: section
---

# Prompt Levels

## High · Mid · Low

<!--
Divider. High, mid, low, then advance
-->

---
layout: default
---

<div class="label">Three levels</div>

# Where to operate

<div class="grid grid-cols-3 gap-6 mt-8 items-stretch">
  <div class="card">
    <ph-cloud-bold class="text-3xl text-blue-600 mb-3" />
    <div class="font-semibold mb-1">High</div>
    <div class="text-sm opacity-70 flex-1">"Make it better." Natural, risky.</div>
  </div>
  <div class="card">
    <ph-target-bold class="text-3xl text-amber-600 mb-3" />
    <div class="font-semibold mb-1">Mid · sweet spot</div>
    <div class="text-sm opacity-70 flex-1">"UPDATE chart.py: word_count_bar_chart() — top quartile green, sort desc."</div>
  </div>
  <div class="card">
    <ph-keyboard-bold class="text-3xl text-blue-600 mb-3" />
    <div class="font-semibold mb-1">Low</div>
    <div class="text-sm opacity-70 flex-1">"Line 47, replace X with Y." Verbose, typist.</div>
  </div>
</div>

<div class="caption mt-6">The sweet spot shifts with the model. Frontier tolerates higher; a 4B needs more.</div>

<!--
Amber on the sweet spot — it's the moment of the slide.

The caption is the calibration point: don't hand them a fixed level, hand
them the habit of noticing which one their model needs today. ORANGE
-->

---
layout: section
---

# Plan = Prompt

## The planning bottleneck

<!--
Divider. Name it and advance. The argument is on the next slide, so do not
start making it here.
-->

---
layout: default
---

<div class="label">2024 vs 2026</div>

# The bottleneck has shifted

<v-clicks>

- **2024**: can the AI understand what I want?
- **2026**: can *I* specify what I want?
- Quality of output bounded by quality of plan
- AI = executor. You = architect.
- A human contractor asks questions when the spec is vague. An LLM guesses.

</v-clicks>

<!--
The whole argument, five clicks. 2024 asked whether the AI could understand
you. 2026 asks whether you can say what you want.

Click four is the claim. The AI is the executor, you are the architect, and
the planning is the engineering work.

Click five is the asymmetry that prices it. A human contractor who gets an
ambiguous spec asks a clarifying question. An LLM does not, it guesses. So
ambiguity costs more here than it does with people, and writing a precise
spec is not extra work. It is the work.

The statement slide next is the payoff for this one. Do not say it here.
-->

---
layout: statement
---

The spec **IS** the prompt.

<!--
The payoff for the slide before it. Not an artifact you produce before
you prompt. The spec IS the instruction.

Say it, then stop talking. Let it sit.
-->

---
layout: default
---

<div class="label">Decision rule</div>

# When to use a spec

<div class="grid grid-cols-2 gap-6 mt-6 items-stretch">
  <div class="card">
    <ph-check-bold class="text-3xl text-emerald-600 mb-3" />
    <div class="font-semibold mb-1">Yes</div>
    <div class="text-sm opacity-70 flex-1">3+ files coordinated · interdependent steps · reproducibility · build-from-scratch · archive</div>
  </div>
  <div class="card">
    <ph-x-bold class="text-3xl text-rose-600 mb-3" />
    <div class="font-semibold mb-1">No</div>
    <div class="text-sm opacity-70 flex-1">Single bug fix · one-fn refactor · "while you're in here, also X"</div>
  </div>
</div>

<div class="caption mt-6">If you would write a design doc for a human contractor, write a spec.</div>

<!--
Two semantic accents: emerald (works) and rose (don't). The one slide that earns it.

The caption is the rule. Say it, then let them apply it in the break.
-->

---
layout: default
---

<div class="label">The codebase you know</div>

# taskr

<div class="mt-2">

The task manager you have been living in. `task.py` is the record, `store.py` is the JSON on disk, `cli.py` is the commands. So far it can only `add` and `list`.

</div>

<div class="text-sm mt-4">

- `taskr done 3` — mark a task complete
- `taskr rm 3` — delete a task
- `taskr list --tag work` — filter by tag
- `taskr add "..." --due fri` — a due date, shown in the listing
- `taskr list --json` — machine-readable output

</div>

<div class="caption mt-4">Pick one, or bring your own. Either way, name the file and the function.</div>

<!--
This exists because "think of a change" is a cold start and the break is only
five minutes. Five options so nobody spends two of those minutes choosing.

They are deliberately different sizes, which is the calibration point. `done`
touches all three files, because a task has no done field yet: that is the one
where a high-level prompt breaks down. `list --json` is one function and
`to_dict()` already exists, so it survives a much higher level.

Say that out loud if the room needs a nudge: the answer to "how high can I go"
depends on how much of the change is already sitting in the codebase.
-->

---
layout: statement
---

<div class="label">Chat break · 5 min</div>

Take a change you'd make to `taskr`. Write it as ACTION LOCATION: DETAIL, then the *highest level that still lands first try*.

<!--
0:35. The fixed break. Full prompt is the chat_break field in overview.md.

taskr on purpose: two weeks of aider-practice means every one of them knows
cli.py, store.py and task.py, and has already calibrated a model against
them. Nobody is blocked on unfamiliar code, which is what a five-minute
break cannot absorb.

Push them toward the highest level that still works, not the safest. The
point is calibration, and "what moved your line" is the question worth
pulling out loud at 0:39: the answer is almost always the model.

They can run it in Aider tonight, which is the whole reason it is taskr and
not something hypothetical.
-->

---
layout: section
---

# PollEv

<div class="mt-5 font-mono text-2xl text-blue-600">https://PollEv.com/marcusdarden365</div>

<!--
The URL is on the slide so the back rows can join without asking. Leave it up
while they answer.

It is a div rather than the usual section subtitle on purpose: the theme
uppercases those, and a uppercased URL path is not the same path. Do not
"fix" it back to an h2.

Presenter cue otherwise. Switch to the browser tab holding the activity, set
it live, read the question and all four options aloud, give it about 60
seconds, show results, then come back to the deck.

This one counts toward attendance, unlike L01's test run. Say so.

Question, options, the answer and what to say after the results are in
assets/poll-everywhere.md. It is L02's needle in a haystack, and the answer
is the argument for the Context section they are about to be taught.
-->

---
layout: section
---

# Spec Anatomy

## Five sections

<!--
Divider. Five sections. Advance.
-->

---
layout: default
---

<div class="label">The structure</div>

# Spec document

<v-clicks>

1. **High-Level Objective** — "what" and "why", generally stated
2. **Mid-Level Objectives** — 3-5 measurable outcomes
3. **Implementation Notes** — deps, standards, constraints
4. **Context** — beginning + ending files
5. **Ordered Low-Level Tasks** — IDK-rich, dependency-ordered

</v-clicks>

<!--
The map, one click per section. Name each and move on, they get unpacked on
the next three slides.

Worth saying out loud that this is a markdown file, not a tool or a form.
They can write one in any editor today.
-->

---
layout: default
---

<div class="label">Sections 1 to 3</div>

# Objectives and notes

<div class="grid grid-cols-3 gap-6 mt-8 items-stretch">
  <div class="card">
    <ph-compass-bold class="text-3xl text-blue-600 mb-3" />
    <div class="font-semibold mb-1">High-level</div>
    <div class="text-sm opacity-70 flex-1">One sentence of why. "Add word frequency visualization and structured file output to the transcript analytics CLI."</div>
  </div>
  <div class="card">
    <ph-check-bold class="text-3xl text-blue-600 mb-3" />
    <div class="font-semibold mb-1">Mid-level</div>
    <div class="text-sm opacity-70 flex-1">Three to five outcomes, each independently verifiable. Chart functions, output formatters, two new CLI flags.</div>
  </div>
  <div class="card">
    <ph-wrench-bold class="text-3xl text-amber-600 mb-3" />
    <div class="font-semibold mb-1">Notes</div>
    <div class="text-sm opacity-70 flex-1">Use matplotlib, it's already a dependency. Follow the patterns in the project. Briefly comment every new function.</div>
  </div>
</div>

<div class="caption mt-6">Objectives say what done looks like. Notes say what the model must not guess.</div>

<!--
Notes is where your engineering judgment goes. Anything you'd correct in
review, put here instead and skip the review round.
-->

---
layout: default
---

<div class="label">Section 4 · the most-skipped one</div>

# Context: beginning + ending

```text
### Beginning context
- src/main.py
- src/data_types.py (read-only)
- pyproject.toml (read-only)

### Ending context
- src/main.py (updated)
- src/chart.py (new file)
- src/output_format.py (new file)
```

<div class="caption mt-4">Eliminates ambiguity. Model knows exactly what's in scope.</div>

<!--
The most often omitted section and the most important one, which is what the
label says. Say it that way.

Beginning context is what the model may read and edit. Ending context is
what should exist afterward. New files get (new file), untouchables get
(read-only).

This is the section that stops the model wandering into files you never
meant it to open. That sentence is the reason the section exists.
-->

---
layout: default
---

<div class="label">Section 5 · ordered tasks</div>

# Compounding sequence

```text
1. CREATE output_format.py with
   format_as_text/json/md/yaml

2. CREATE chart.py with
   create_bar/pie/line_chart —
   colors: top green, bottom red

3. UPDATE main.py: ADD --chart,
   --output-format, call new fns
```

<div class="caption mt-4">Task 3 references Task 1's outputs because Task 1 ran first.</div>

<!--
Read the three tasks in order, then the caption. Task 3 can reference
format_as_json() because Task 1 already ran. The sequence carries the
dependencies so the model does not have to infer them.

Stay on this slide for that point. There is no separate slide for it.

Close on the analogy to how they already work: types first, then the
functions that use them, then the call sites.
-->

---
layout: section
---

# Architect Mode

## Spec in action

<!--
Bridge: they have the five sections now. Watch one spec that has all five
run end to end, against a model on a laptop.

Mistakes come after the demo, not before. Do not preview them here.
-->

---
layout: default
---

<div class="label">Reasoning + Editing</div>

# Architect Mode in Aider

```bash
aider --architect \
      --model ollama_chat/qwen3.5:9b \
      --editor-model ollama_chat/qwen3.5:9b
```

- **Architect** — drafts the plan in prose
- **Editor** — turns the plan into edits
- `auto-accept-architect: false` — the plan stops. Read it.

<div class="caption mt-4">Same model in both seats. The demo's config sets all three, so on screen you will see just <code>aider src/main.py src/arg_parse.py</code>.</div>

<!--
Correct the assumption before they form it: two roles, not two models. Same
model in both seats is fine, and on a laptop it is usually what you want. A
small model is noticeably better at one job than at two, which is the whole
win. The 9B architect with the 4B editor is a fair experiment to run once,
not a requirement.

Third bullet is the one to land. aider-practice lesson 6 sets it false on
purpose, so the plan stops and waits. Nothing is on disk yet, so this is the
cheapest place in the workflow to catch a model that misunderstood you.

Flag it and move on: plan, then act, then check is a loop. They write one in
week 5.
-->

---
layout: default
---

<div class="label">Live demo</div>

# Watch it run

<v-clicks>

1. `spec.md` on screen. Walk the five sections.
2. `aider src/main.py src/arg_parse.py` — Architect Mode, no flags.
3. Paste the spec. The architect writes a plan in prose.
4. **Read the plan out loud, then `y`.** Nothing is on disk yet.
5. Four files: `output_format.py`, `chart.py` new; `arg_parse.py`, `main.py` updated.
6. `uv run main transcript.txt --chart bar --output-format json`

</v-clicks>

<!--
Six clicks. Step 4 is the beat and it is the one you cannot cut.

Show the spec and walk its five sections before launching anything. Otherwise
the room watches output scroll without knowing what was asked for.

Read the banner against the spec on the other screen. Two files editable,
five read-only, and that is the Context section they were about to skip.
Aider implements (read-only); it is not a note to yourself.

Step 4: nothing is on disk. If it misunderstood you, this costs one
keystroke. After the edit it costs a /undo and four minutes of model time.

If aider asks "Add file to the chat?", answer S. The default is Yes and Yes
re-runs the architect, which loses the plan.

If it stalls, switch to the recording. Do not debug Python in front of the
room. Full runbook: assets/demo-runbook.md.
-->

---
layout: section
---

# Common Mistakes

## Before you write your own

<!--
Bridge: You have seen a clean spec run. Before you write your own, the four things graders consistently see go wrong.
-->

---
layout: default
---

<div class="label">Common spec mistakes</div>

# What graders see

<v-clicks>

- **Vague MLOs** — "make it better" sneaks in
- **Missing context section** — model touches files it shouldn't
- **Out-of-order tasks** — Task 1 references Task 3
- **Code in tasks** — implementation, not instructions

</v-clicks>

<div class="caption mt-6">Specs are communication artifacts. Treat them as such.</div>

<!--
Four clicks, and say plainly that you will see all four.

Code where instructions belong is the most common. They write the
implementation into the task instead of describing it.

The caption is the frame. A spec is a communication artifact, so the test is
whether another person could execute it.
-->

---
layout: default
---

<div class="label">Recap</div>

# What to take away

<v-clicks>

- **IDKs** name the action and the location, which narrows the sampling distribution
- **Mid-level** is the sweet spot, and the sweet spot moves with the model
- **Plan = Prompt.** The spec is the instruction, not a document about it
- **Ordered tasks** compound, so later steps lean on earlier ones
- **Architect Mode** splits planning from editing. One job per call
- **Specs earn their cost** on three or more coordinated files

</v-clicks>

<!--
Six clicks, one line each, no elaboration. They have heard all of it once
already. This is the version they write down.

If the clock is short, click through and land only the third one: the spec
is the instruction, not a document about it.
-->

---
layout: default
---

<div class="label">For the room</div>

# Three questions

<div class="mt-6 space-y-3">

1. How is a spec different from one very long prompt?
2. Would you write a spec for a bug fix? Where does it become overkill?
3. Why put "comment every function" in the spec instead of hoping for it?

</div>

<!--
Take two of the three out loud if the clock allows. Question 3 is the one
worth landing: standards you don't write down are standards the model
never had.
-->

---
layout: default
---

<div class="label">This week</div>

# Lab01 + the build

<v-clicks>

- **Tomorrow (Fri Sep 11)** — Aider setup gate + all sixteen lessons
- **Mon Sep 14 / Tue Sep 15** — Lab01, the pivot lab
- **Fri Sep 25** — the build is due (end of week 4)
- **Not yet** — `aider-practice` finishes this week; the build starts after Lab01

</v-clicks>

<!--
Dates, said once and clearly. Setup gate and all sixteen aider-practice
lessons are due tomorrow, Friday September 11. Lab01 is Monday September 14
for the Monday section, Tuesday September 15 for the Tuesday section. The
build is due Friday September 25.

Last click prevents a week of confusion. They are not building yet.
aider-practice finishes this week and the build starts after Lab01.
-->

---
layout: default
---

<div class="label">The build · due Fri Sep 25</div>

# The seven features

<div class="mt-2">A terminal coding assistant: conversation, files in context, model-written edits applied behind a diff.</div>

<div class="text-sm mt-3">

| | Required behavior |
|---|---|
| **F1** | Conversation, budget handling, streamed replies |
| **F2** | Add, drop, list and clear context |
| **F3** | Current file contents, rendered consistently |
| **F4** | An edit-format prompt you have tested |
| **F5** | Parsing with useful errors |
| **F6** | Exact edits, complete preview, explicit approval |
| **F7** | One commit per accepted edit set, guarded undo |

</div>

<!--
Say the line the slide no longer has room for: Aider's spine, not its
feature list, and everyone builds the same seven.

Most of the room has not seen this list. It went public yesterday inside the
Lab01 deck and nothing pointed them at it, so read all seven aloud rather
than assuming. The next slide says which two of the seven today feeds directly, so this
is the setup for it, not a detour.

The description is the part they need first: they are building the thing they
have been driving for two weeks. F2 is /add and /drop, which is L03's demo,
and F4 is the spec written for one small model, which is the next slide.

Table matches Lab01's exactly, on purpose. The full spec with the checked
behaviors is in the starter repo.
-->

---
layout: default
---

<div class="label">Both are graded</div>

# What this feeds

<div class="grid grid-cols-2 gap-6 mt-8 items-stretch">
  <div class="card">
    <ph-package-bold class="text-3xl text-blue-600 mb-3" />
    <div class="font-semibold mb-1">Your build's spec doc</div>
    <div class="text-sm opacity-70 flex-1">Seven features on a starter is the "three or more files, from scratch" case. The spec is a required deliverable.</div>
  </div>
  <div class="card">
    <ph-code-bold class="text-3xl text-amber-600 mb-3" />
    <div class="font-semibold mb-1">Feature F4, the edit-block prompt</div>
    <div class="text-sm opacity-70 flex-1">A spec written for one small model. Leave it vague and your parser rejects the output, so nothing lands on disk.</div>
  </div>
</div>

<div class="caption mt-6">Everything today is about to become code you hand in.</div>

<!--
Both cards are graded work, which is the label. Say that first.

Left card: seven features on a starter is exactly the three or more files,
building from scratch case from the decision rule, so the spec is a required
deliverable.

Right card is the one worth the time. F4 is the instruction that tells a
model how to emit an edit. That is a spec written for an audience of one
small model, and it is the least forgiving one all term. Leave it vague and
the parser rejects the output, so nothing lands on disk.

Then the offer: bring a spec draft to office hours this week. The first one
will not be perfect, and that is fine.
-->

---
layout: default
---

<div class="label">Next lecture</div>

# Modern Agentic CLIs

<div class="mt-6 space-y-2">

- The same spec you write today, handed to Claude Code and to Codex
- A demo from the podium. No account, nobody is asked to buy anything
- More autonomy, different behavior, and the Big Three still applies

</div>

<div class="caption mt-6">The mature version of the thing you are about to build. Tuesday.</div>

<!--
Say the no-account line plainly and early. Someone is already wondering
whether they have to buy something. It is a demo from the podium.

Same spec, more autonomous tool, different behavior, and the Big Three still
applies. What they are looking at is the mature version of the thing they
are about to build.
-->

---
layout: end
---
