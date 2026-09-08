---
theme: ../theme
title: "L03: The Big Three: Context, Model, Prompt"
info: |
  EECS 498 AASE — Lecture 03
  Applied Agentic Software Engineering, UMich Fall 2026
layout: title
class: text-left
transition: fade
mdc: true
highlighter: shiki
---

# The Big Three

## Lecture 03 · Sep 8, 2026

<!--
L02 = mechanics. L03 = framework on top.
This is the lecture they'll use the rest of their careers.
-->

---
layout: default
---

<div class="label">Week 2 · setup check</div>

# `aider-practice` status

<div class="mt-6 space-y-2">

- Model serving?
- Aider reaching it?
- Setup friction: weights that won't pull, a server Aider can't reach, a machine too small?

</div>

<div class="caption mt-6">Office hours all week, and any of us can do setup with you. <strong>Fri Sep 11</strong> is the gate plus all sixteen lessons.</div>

<!--
Show of hands, three times. All three failures are common and none of
them are the student's fault. Take names for office hours rather than
debugging in the room.
-->

---
layout: section
---

# Big Three

## Context · Model · Prompt

---
layout: default
---

<div class="label">Three levers</div>

# Every AI coding session

<div class="grid grid-cols-3 gap-6 mt-8 items-stretch">
  <div class="card">
    <ph-files-bold class="text-3xl text-blue-600 mb-3" />
    <div class="font-semibold mb-1">Context</div>
    <div class="text-sm opacity-70 flex-1">What does the model see right now?</div>
  </div>
  <div class="card">
    <ph-cpu-bold class="text-3xl text-blue-600 mb-3" />
    <div class="font-semibold mb-1">Model</div>
    <div class="text-sm opacity-70 flex-1">Which LLM? Capability + knowledge.</div>
  </div>
  <div class="card">
    <ph-chat-bold class="text-3xl text-amber-600 mb-3" />
    <div class="font-semibold mb-1">Prompt</div>
    <div class="text-sm opacity-70 flex-1">How clearly is intent expressed?</div>
  </div>
</div>

<!--
Define all three here, one at a time, before the bullseye lands.
Context: files, history, repo map, system prompt. Finite.
Model: a line of configuration, not a vendor loyalty.
Prompt: judged by consistency of output, not cleverness of phrasing.
-->

---
layout: statement
---

Two out of three is *not* enough.

<!--
The Bullseye. Magic happens at the intersection. Miss any one → off-target.
-->

---
layout: default
---

<div class="label">When AI is wrong, ask</div>

# Diagnostic

1. **Context** — was the file in the window?
2. **Model** — was it strong enough? recent enough?
3. **Prompt** — was intent clear?

<div class="caption mt-6">Most students blame the model. It's usually context.</div>

---
layout: default
---

<div class="label">Mapping back to L02</div>

# Each lever has a mechanic

<div class="mt-6 space-y-3">

- **Context** → context window economics. Bigger isn't free.
- **Model** → capability vs knowledge axes.
- **Prompt** → narrowing the sampling distribution.

</div>

<div class="caption mt-6">The Big Three isn't arbitrary. It's the framework on top of the mechanics.</div>

---
layout: section
---

# Context

## The lever you control most directly

---
layout: default
---

<div class="label">Four sources</div>

# What's in your context

<v-clicks>

- **Explicitly added files** — what you `/add`
- **Repo map** — auto-generated structure summary
- **Chat history** — accumulates until `/clear`
- **System prompt** — Aider's instructions to the model

</v-clicks>

---
layout: statement
---

Adding everything is *worse* than adding the right things.

<!--
The wrong instinct. aider **/*.py looks helpful, isn't.
-->

---
layout: default
---

<div class="label">The skill</div>

# Surgical context

```text
For any task, ask:
  - Which files will this CHANGE?
  - Which files does the model need to READ?
  - Which files are read-only REFERENCE?

Add only those. /drop the rest. /tokens often.
```

<div class="caption mt-4">Context is design, not setup.</div>

---
layout: default
---

<div class="label">Reading the budget</div>

# Where your tokens go

```text
/tokens

  repo map              1,800
  chat history          3,100
  main.py               6,000
  arg_parse.py          1,300
  -----------------------------
  total                12,200   of 32,768
```

<div class="caption mt-4">Check it before and after anything big. It is the only honest view of the window.</div>

<!--
Broken down by source, which is what makes it a diagnostic and not a
counter. When the repo map or the history is the biggest line, that is
the finding.
-->

---
layout: default
---

<div class="label">Two pitfalls</div>

# Where students get stuck

<div class="grid grid-cols-2 gap-6 mt-8 items-stretch">
  <div class="card">
    <ph-file-x-bold class="text-3xl text-rose-600 mb-3" />
    <div class="font-semibold mb-1">Missing context</div>
    <div class="text-sm opacity-70 flex-1">arg_parse.py not /add-ed → model only edits main.py → broken result.</div>
  </div>
  <div class="card">
    <ph-clock-counter-clockwise-bold class="text-3xl text-rose-600 mb-3" />
    <div class="font-semibold mb-1">Chat history bleed</div>
    <div class="text-sm opacity-70 flex-1">Task B inherits assumptions from Task A. Fix: /clear.</div>
  </div>
</div>

---
layout: statement
---

<div class="label">Chat break · 5 min</div>

Ten files, one function to change, *three* callers. Which files do you add?

<!--
0:35. The fixed break. Prompt is the chat_break field in overview.md.

There is no single right answer, and that is the point: the habit being
built is treating context as a design decision, not setup. Push for
strategies, not file lists. Two or three out loud, then move.
-->

---
layout: section
---

# Model

## Match capability to task

---
layout: default
---

<div class="label">Four dimensions</div>

# Choosing

<v-clicks>

- **Reasoning ability** — capability from L02
- **Speed** — usually correlated with capability
- **Cost** — dollars on a vendor, RAM and seconds on your own box
- **Context window size** — but bigger ≠ better (L02!)

</v-clicks>

---
layout: default
---

<div class="label">The engineering question</div>

# Right model for this job

<div class="grid grid-cols-2 gap-6 mt-8 items-stretch">
  <div class="card">
    <ph-wrench-bold class="text-3xl text-blue-600 mb-3" />
    <div class="font-semibold mb-1">One-line bug fix</div>
    <div class="text-sm opacity-70 flex-1">A cheap, fast model clears the bar. Capability spent here buys nothing.</div>
  </div>
  <div class="card">
    <ph-tree-structure-bold class="text-3xl text-amber-600 mb-3" />
    <div class="font-semibold mb-1">Three new files, interdependent</div>
    <div class="text-sm opacity-70 flex-1">The strongest model you have. Getting it wrong costs more than the call.</div>
  </div>
</div>

<div class="caption mt-6">Benchmarks (<code>aider.chat/docs/leaderboards/</code>) proxy for your task. They don't replace it.</div>

---
layout: default
---

<div class="label">Apply rule of thumb</div>

# Start on the model that fails

```text
Start on 4b. Move to 9b when it stops teaching you
and starts merely costing you an afternoon.

A model that covers for your mistakes
hides the mistakes you need to see.
```

<div class="caption mt-6">Switch with <code>/model ollama_chat/qwen3.5:9b</code>. Files and history persist; the new model reads all of it fresh.</div>

<!--
Say out loud that this is the opposite of what they'd do at work.
Crossover is around lesson 6, the first real refactor, for most of them.
-->

---
layout: section
---

# Prompt

## Specify intent precisely

---
layout: default
---

<div class="label">Two components</div>

# Instruction and intent

<div class="mt-6 space-y-3">

- **Instruction** — what you want done
- **Intent** — the reason you want it done that way

</div>

<div class="caption mt-6">Leave the intent out and the model fills it from training-data priors.</div>

---
layout: two-col
---

## Vague

```text
Add another way
to output the data.
```

<div class="text-sm opacity-70 mt-4">Model guesses. Maybe text. Maybe print(). May skip CLI flag. Unpredictable.</div>

::right::

## Specific

```text
CREATE output_format.py:
  format_as_html(...) -> str
UPDATE main.py: ADD
  html to --output-format
```

<div class="text-sm opacity-70 mt-4">Predictable. Repeatable. First-try success.</div>

---
layout: statement
---

What > How.

<!--
Specify outcome, not implementation. But "what" must be specific.
"What > How" ≠ "be vague and AI will figure it out."
-->

---
layout: section
---

# Live Demo

## Context as engineering decision

<!--
Bridge: we've named the framework and taken each lever apart.
Now watch it decide an actual edit.
-->

---
layout: default
---

<div class="label">5-file transcript analytics codebase</div>

# Demo flow

<v-clicks>

1. Aider with only `main.py`. Prompt: `--output-format` flag.
2. It invents an `arg_parse.py` it has never seen. Decline it.
3. Run the program. Clean diff, `AttributeError`.
4. `/add arg_parse.py`. Same prompt. Coherent, and it runs.
5. `/tokens`: 1,746 → 1,998 → 3,962 for the whole `src/`.
6. `/model ollama_chat/qwen3.5:4b`. Same prompt. Compare.

</v-clicks>

<div class="caption mt-4">The codebase is yours: <code>materials/demos/transcript-analytics</code>. Run the demo again at home.</div>

---
layout: default
---

<div class="label">Take home</div>

# Three questions for you

1. 50-file project, change auth across API layer — how do you /add?
2. Why does adding **all** files make results *worse*?
3. Model switch mid-session — what changes?

<div class="caption mt-6">Most "the AI is wrong" failures collapse to question 1 or 2.</div>

---
layout: default
---

<div class="label">The Big Three</div>

# What to take away

<div class="mt-6 space-y-2">

- **Context, model, prompt.** Three levers, every session you will ever run
- **Context is usually the problem.** Most "the AI is wrong" is missing context
- **Model choice is technical**, not a preference. Match capability to task
- **Prompts say what, not how.** Named file, named function, stated outcome

</div>

<div class="caption mt-6">Two out of three is not enough. Ask the question before you retype the prompt.</div>

---
layout: default
---

<div class="label">What's next</div>

# Lab01 + the build

<v-clicks>

- **Fri Sep 11** — setup gate, and all sixteen lessons due
- **Mon Sep 14 / Tue Sep 15** — Lab01: the pivot lab
- **The build** — seven features, weeks 3 and 4. Starts after Lab01, spec graded with it
- **L04** Thursday — Spec-Driven Coding

</v-clicks>

<div class="caption mt-6">Use today's diagnostic in Lab01 when things break. <em>Context, model, or prompt?</em></div>

---
layout: end
---
