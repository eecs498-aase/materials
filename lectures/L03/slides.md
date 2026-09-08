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

<!--
L02 gave them tokenization, the context window, hallucination, capability
against knowledge. That was the mechanics. This is the framework on top.
Three choices in every session. Get one wrong and no amount of effort in
the other two saves you.
-->

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
layout: default
---

<div class="label">The bullseye</div>

# Where the three overlap

<div style="display:grid; grid-template-columns:7fr 5fr; gap:2.5rem; align-items:center; margin-top:0.5rem">
<div>
<svg viewBox="20 15 410 390" style="width:100%; max-height:340px" role="img"
     aria-label="Three overlapping circles labelled Context, Model and Prompt, with the region where all three overlap highlighted as the bullseye.">
  <g fill="var(--c-primary)" fill-opacity="0.07" stroke="var(--c-primary)" stroke-width="1.75">
    <circle cx="155" cy="145" r="110" />
    <circle cx="295" cy="145" r="110" />
    <circle cx="225" cy="266.24" r="110" />
  </g>
  <path d="M 186.52 163.19
           A 110 110 0 0 1 263.48 163.19
           A 110 110 0 0 1 225 229.85
           A 110 110 0 0 1 186.52 163.19 Z"
        fill="var(--c-highlight)" stroke="var(--c-amber)" stroke-width="2.5" />
  <text x="225" y="189" style="font: 600 11px var(--font-mono); letter-spacing:0.04em"
        fill="var(--c-amber)" text-anchor="middle">BULLSEYE</text>
  <g style="font: 600 17px var(--font-mono)" fill="var(--c-primary)" text-anchor="middle">
    <text x="105" y="138">Context</text>
    <text x="345" y="138">Model</text>
    <text x="225" y="322">Prompt</text>
  </g>
  <g style="font: 600 13px var(--font-mono)" fill="var(--c-ink-muted)" text-anchor="middle">
    <circle cx="280" cy="218" r="12" fill="var(--c-bg-0)" stroke="var(--c-rule-strong)" />
    <text x="280" y="222.5">1</text>
    <circle cx="170" cy="218" r="12" fill="var(--c-bg-0)" stroke="var(--c-rule-strong)" />
    <text x="170" y="222.5">2</text>
    <circle cx="225" cy="108" r="12" fill="var(--c-bg-0)" stroke="var(--c-rule-strong)" />
    <text x="225" y="112.5">3</text>
  </g>
</svg>
</div>
<div style="display:flex; flex-direction:column; gap:1.3rem; font-size:0.85em">
<div><strong>1 &middot; Model + prompt, no context.</strong> A clean, confident edit to a file it has never read. <em>Today's demo.</em></div>
<div><strong>2 &middot; Context + prompt, no model.</strong> Everything it needs, and it still loses the thread halfway through.</div>
<div><strong>3 &middot; Context + model, vague prompt.</strong> Right files, strong model, and it builds something reasonable that you never asked for.</div>
</div>
</div>

<!--
Draw it in the air first, then let the slide confirm it. Three circles,
target at the intersection.
Walk the three near-misses in order and ask which one they think is most
common before you say it. Zone 1 is the demo at 1:00, so name it now and
they will recognise it when it happens.
Zones 2 and 3 are the honest ones: a weak model and a vague prompt both
produce output that looks like progress.
-->

---
layout: statement
---

Two out of three is *not* enough.

<!--
The punchline of the diagram they just read. Say it flat, then move.
Effort in the other two levers does not buy back the one you missed.
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

<!--
The key point of the lecture. When something comes back wrong, ask these
three in order before you touch anything.
Most students blame the model. It is statistically the least common cause.
Usually it is context.
Tell them now that they will use this in Lab01 next week.
-->

---
layout: section
---

# Context

## The lever you control most directly

<!--
The lever they control most directly, and the one that causes the most
trouble. Most of the next twenty minutes lives here.
In a few weeks they implement this themselves.
-->

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

<!--
Added files are the only files the model can edit. Say that twice.
The repo map is an auto-generated summary, not a substitute for adding the
file.
Chat history accumulates until /clear. That is the second pitfall, two
slides from now.
The system prompt is Aider's own, and the default is fine for now.
-->

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

<div class="grid grid-cols-3 gap-6 mt-8 items-stretch">
  <div class="card">
    <ph-pencil-simple-bold class="text-3xl text-blue-600 mb-3" />
    <div class="font-semibold mb-1">Change</div>
    <div class="text-sm opacity-70 flex-1">Which files will this task edit? Only these can be edited at all.</div>
  </div>
  <div class="card">
    <ph-eye-bold class="text-3xl text-blue-600 mb-3" />
    <div class="font-semibold mb-1">Read</div>
    <div class="text-sm opacity-70 flex-1">Which does it have to understand first? Add these too.</div>
  </div>
  <div class="card">
    <ph-bookmark-simple-bold class="text-3xl text-amber-600 mb-3" />
    <div class="font-semibold mb-1">Reference</div>
    <div class="text-sm opacity-70 flex-1">Read-only background. Usually the repo map already covers it.</div>
  </div>
</div>

<div class="caption mt-6">Add only those, <code>/drop</code> the rest, <code>/tokens</code> often. Context is design, not setup.</div>

<!--
Three questions, asked before every task, not once at the start of a
session.
Only the first card can be edited at all. The second is what the model has
to read to get the first right.
Reference is usually where the repo map is already enough.
-->

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

<!--
Missing context is the most common failure in this course. The model edits
what is in context, so a file that was never added cannot be fixed. Aider
offers to add it and taking the offer saves you. Decline it, or use a tool
that does not ask, and one file gets updated alone: a partial change that
looks finished.
History bleed is subtler. Ten minutes on task A, start task B, and those
messages are still sitting there carrying assumptions. /clear resets the
conversation and keeps the files.
This sets up the break. Do not answer it here.
-->

---
layout: statement
---

<div class="label">Chat break · 5 min</div>

Ten files, one function to change, *three* callers. How do you decide what to add? Discuss your strategy.

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

<!--
Context is what you feed the model. This is the other half of the same
decision.
Ten minutes here, then prompt.
-->

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

<!--
Speed and size track reasoning ability. Smarter tends to be bigger, which
on their own hardware means slower and hungrier for RAM rather than more
expensive in dollars. The tradeoff does not disappear when the bill does.
Some models do 128K, some do 1M, and L02 already told them bigger is not
automatically better. Needle in a haystack is real.
-->

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

<!--
Per task, not per term. That is the whole slide.
The leaderboard is worth knowing, and it is a proxy for their task rather
than a substitute for running their task.
-->

---
layout: default
---

<div class="label">Apply rule of thumb</div>

# Start on the model that fails

<div class="mt-6 space-y-3">

- **Start on 4b.** It fails where you can see it, and the failure is the lesson
- **Move to 9b** when it stops teaching you and starts merely costing you an afternoon

</div>

<div class="mt-10 mb-2 text-xl">A model that covers for your mistakes <em>hides the mistakes you need to see.</em></div>

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

<!--
The last lever, and the shortest section, because L04 is the whole lecture
on it.
-->

---
layout: default
---

<div class="label">The prompt spectrum</div>

# How far down to specify

<div style="display:flex; justify-content:center; margin-top:0.5rem">
<svg viewBox="0 0 900 290" style="width:100%; max-height:300px" role="img"
     aria-label="A three-band spectrum: outcome on the left is under-specified, interface in the middle is just enough, implementation on the right is over-specified. An arrow labelled more intent points from the middle back toward the left.">
  <g style="font: 500 11px var(--font-mono); letter-spacing:0.1em" fill="var(--c-ink-muted)" text-anchor="middle">
    <text x="160" y="42">UNDER-SPECIFIED</text>
    <text x="450" y="42">JUST ENOUGH</text>
    <text x="740" y="42">OVER-SPECIFIED</text>
  </g>
  <rect x="20" y="58" width="280" height="58" rx="8" fill="var(--c-primary)" fill-opacity="0.07" stroke="var(--c-primary)" stroke-width="1.5" />
  <rect x="310" y="58" width="280" height="58" rx="8" fill="var(--c-highlight)" stroke="var(--c-amber)" stroke-width="2.5" />
  <rect x="600" y="58" width="280" height="58" rx="8" fill="var(--c-primary)" fill-opacity="0.07" stroke="var(--c-primary)" stroke-width="1.5" />
  <g style="font: 600 17px var(--font-mono)" text-anchor="middle">
    <text x="160" y="93" fill="var(--c-primary)">OUTCOME</text>
    <text x="450" y="93" fill="var(--c-amber)">INTERFACE</text>
    <text x="740" y="93" fill="var(--c-primary)">IMPLEMENTATION</text>
  </g>
  <g style="font: 400 12px var(--font-mono)" fill="var(--c-ink-soft)" text-anchor="middle">
    <text x="160" y="146">"another way to output"</text>
    <text x="450" y="146">"format_as_html() -&gt; str"</text>
    <text x="740" y="146">"iterate the speakers dict"</text>
  </g>
  <g style="font: 400 11px var(--font-sans)" fill="var(--c-ink-muted)" text-anchor="middle">
    <text x="160" y="167">the model guesses</text>
    <text x="450" y="167">you set the seam, it writes the body</text>
    <text x="740" y="167">you did the work, it adds nothing</text>
  </g>
  <g stroke="var(--c-amber)" stroke-width="2.5" fill="var(--c-amber)">
    <line x1="520" y1="212" x2="262" y2="212" />
    <polygon points="250,212 264,205 264,219" stroke="none" />
  </g>
  <text x="385" y="240" style="font: 600 12.5px var(--font-mono)" fill="var(--c-amber)" text-anchor="middle">more intent, aim further left</text>
</svg>
</div>

<div class="caption mt-4"><strong>Intent</strong> is why you want it done that way. It is not a point on this line, it is what moves the target.</div>

<!--
Prompts have two parts. The instruction is what you want done. The intent
is the reason you want it done that way. Leave the intent out and the model
fills it from training-data priors, a guess you never got to see.
The line this slide rests on: specification closes decisions, intent steers
the ones you left open. That is why one is a band and the other is an
arrow. Say it before you explain the arrow.
Then pre-empt the misread: the arrow is not telling them to be vaguer, it
is telling them the target gets wider on that end when you say why. Intent
extends the left edge and does nothing to the right edge, because it cannot
rescue you from having already written the code yourself.
Aim for the interface: name the file, the function, the signature, the call
site, and stop. You own the seam, the model writes the body.
Required, not optional: the arrow has a length and its length is model
capability. On the 4B it is short. A paragraph of why can bury the one
sentence of what, which is L02's needle in a haystack aimed at their own
prompt. Keep intent to a clause this term.
-->

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

<!--
The vague one sets a direction and leaves every specific decision to the
model. It is not wrong, it is unpredictable, and unpredictable is the
problem.
The specific one is longer to write and faster to use. Predictability is
the goal, not brevity.
L04 formalizes this as an IDK prompt.
-->

---
layout: statement
---

What > How.

<!--
Specify outcome, not implementation. But "what" has to be specific enough
to succeed.
Sharper now that they have the spectrum: specify down to the interface and
stop there. "What > How" is not "be vague and the AI will figure it out."
-->

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

<!--
The recap before the demo. Each lever is one of last lecture's mechanics
with a handle on it.
Land this: every piece of prompting advice they will ever read reduces to
one of these three. "Add the file" exploits the window. "Be specific"
exploits the priors.
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

1. Aider with only `src/main.py`. Prompt: `--output-format` flag.
2. It proposes a rewrite of `arg_parse.py`, a file it never read. Decline.
3. Run the program. Clean diff, `AttributeError`. Then `/undo`.
4. `/add src/arg_parse.py`. Same prompt. Coherent, and it runs.
5. `/tokens`: chat history is the biggest line, bigger than all five files.
6. `/model ollama_chat/qwen3.5:4b`, `/clear`, `/drop`, `/add src/main.py`. Same prompt.

</v-clicks>

<div class="caption mt-4">The codebase is yours: <code>materials/demos/L03-transcript-analytics</code>. Run the demo again at home.</div>

<!--
Five files. arg_parse.py owns every command-line flag, main.py owns the
counting and the printing. Say that out loud before you start, because the
whole demo turns on it.
Step 2 is the moment: it proposes a rewrite of a file it has never read,
and what is on screen is a diff, so the minus lines are a line-by-line
inventory of what it got wrong. Point at -default=DEFAULT_TOP_N against
+default=10.
Two prompts to decline there, not one. The second one defaults to Yes, and
taking the default writes the invented file to disk and loses the demo.
Step 4 is the lecture in one sentence: same model, same prompt, one more
file.
Step 6 drops and re-adds on purpose. Without it all five files are still in
context and the 4B cannot reproduce the failure. Same mistake, faster: the
failure was never the model.
If a step misbehaves, say the sentence and move on. The model can only
change files that are in context.
-->

---
layout: default
---

<div class="label">Take home</div>

# Three questions for you

1. 50-file project, change auth across API layer — how do you /add?
2. Why does adding **all** files make results *worse*?
3. Model switch mid-session — what changes?

<div class="caption mt-6">Most "the AI is wrong" failures collapse to question 1 or 2.</div>

<!--
Not rhetorical. Ask them to actually answer these before Lab01.
Question 2 is the one most of them get wrong: worse, not merely more
expensive.
-->

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

<!--
The concrete payoff: /add and /drop are one of the seven features they
implement in weeks 3 and 4. Pulling a file into context is another, and
the trimming behind multi-turn history is a third.
They are drilling this week the exact behaviour they will have to write.
-->

---
layout: default
---

<div class="label">What's next</div>

# Lab01 + the build

<v-clicks>

- **Fri Sep 11** — setup gate, and all sixteen lessons due
- **Mon Sep 14 / Tue Sep 15** — Lab01: the pivot lab
- **The build** — seven features, weeks 3 and 4. Starts after Lab01, spec graded with it
- **L04 Thu Sep 10** — Spec-Driven Coding, two days from now

</v-clicks>

<div class="caption mt-6">Use today's diagnostic in Lab01 when things break. <em>Context, model, or prompt?</em></div>

<!--
Friday is the gate and all sixteen lessons, both.
They are not building yet. The build starts after Lab01 and the spec is
graded with it.
Thursday is Spec-Driven Coding: plan equals prompt, the artifact that makes
"be concrete" reproducible at scale, and the last technique before the
build.
-->

---
layout: end
---
