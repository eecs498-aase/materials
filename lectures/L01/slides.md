---
theme: ../theme
title: "L01: Course intro + the AI coding landscape"
info: |
  EECS 498 AASE — Lecture 01
  Applied Agentic Software Engineering, UMich Fall 2026
layout: title
class: text-left
transition: fade
mdc: true
highlighter: shiki
---

# Course intro + the AI coding landscape

## Lecture 01 · Sep 1, 2026

<!--
Title slide. Energy up. Today is Day 1.
The arc of the lecture: orient → land the philosophy → discussion → then (and only then) the tool.
-->

---
layout: statement
---

Smile.

<!--
Beat one. Just the word. Let them actually do it — wait for it.
Embodied cognition: posture and expression move cognitive performance.
-->

---
layout: statement
---

Smile. *You belong here.*

<!--
Beat two, appended. Now the reason.
Neighbor affirmation: turn and tell them. Then move.
-->

---
layout: default
---

<div class="label">Roadmap · 80 min</div>

# Where we're headed today

<v-clicks>

- **One object, three verbs** — what we'll do this semester
- **How this course runs** — where things live, grading, what it asks
- **AI coding landscape** — wave history, where we are in 2026
- **Code curator philosophy** — the mental model
- **Discussion** — two questions
- **The tool** — Aider, and what it feels like
- **This week** — `aider-practice` + setup gate + what you're building

</v-clicks>

<!--
Land the arc. Note: tool comes LAST. We earn the tool by talking principles first.
-->

---
layout: section
---

# Course Shape

## Apply · Analyze · Create

<!--
Bridge: Now that we've named our presence, here's the 15-week shape.
-->

---
layout: default
---

<div class="label">Course Arc · 15 weeks</div>

# One object. Three verbs.

<div class="grid grid-cols-3 gap-6 mt-8 items-stretch">
  <div class="card">
    <ph-user-bold class="text-3xl text-blue-600 mb-3" />
    <div class="font-semibold mb-1">Apply · Wks 1–3</div>
    <div class="text-sm opacity-70 flex-1">Use a coding agent to build one. Aider against your own endpoint → a pair-programmer.</div>
  </div>
  <div class="card">
    <ph-code-bold class="text-3xl text-blue-600 mb-3" />
    <div class="font-semibold mb-1">Analyze · Wks 4–7</div>
    <div class="text-sm opacity-70 flex-1">Take yourself out of the loop. Tools, stop conditions, then measure what broke.</div>
  </div>
  <div class="card">
    <ph-tree-structure-bold class="text-3xl text-amber-600 mb-3" />
    <div class="font-semibold mb-1">Create · Wks 8–15</div>
    <div class="text-sm opacity-70 flex-1">Grow it into an assistant. Memory, method, and a way to reach it that isn't a terminal.</div>
  </div>
</div>

<!--
Create in amber: it's the destination, the "moment" of the slide.
Say the line out loud: it is all ONE repository, weeks 1 to 15.
-->

---
layout: section
---

# How This Course Runs

## Sites · staff · grades · calendar

<!--
Brisk. The syllabus carries detail; this is the map. But slow down on
integrity and on the hackathon evenings.
-->

---
layout: default
---

<div class="label">Five places</div>

# Where things live

| | |
|---|---|
| **Course site** `eecs498-aase.github.io` | Syllabus + schedule. Wins on dates and policy |
| **Ed** `edstem.org` | Questions **and announcements**. This is where we reach you |
| **GitHub** `aase-student` | Everything you receive. Your own repo per handout. **Accept the invite in your email** |
| **Canvas** | Grades |
| **Podcast** (optional) | A Brief before each lecture, a Deep Dive after |

<div class="caption mt-6">Lectures are recorded (CAEN + Zoom). Podcast episodes are AI-generated from course materials and <em>de-identified</em> transcripts. Nobody is named. Want something out? Email the staff address; it comes out.</div>

<!--
Say the recording line plainly, don't bury it. Ed is the one they must
actually check — the podcast announcement is already up there.
-->

---
layout: default
---

<div class="label">Staff · one address</div>

# Who you're dealing with

- **Marcus Darden** — instructor
- **Rafe Symonds**, **Zilin Wang** — GSIs
- **Rushil Kagithala** — IA

<div class="mt-6">

`eecs-aase-staff@umich.edu` reaches all four.

</div>

<div class="caption mt-4">Personal things (extensions, accommodations, hardware) → email. Anything the class would benefit from hearing → Ed.</div>

<!--
Office hours start this week; confirmed times and rooms go up on Ed.
-->

---
layout: default
---

<div class="label">Grading · no exams</div>

# How you're graded

| | Share of your grade |
|---|---|
| **Administrative** — lecture + lab attendance, bonuses | 10% |
| **Apply** — weeks 1–3, build to end of 4 | 18% |
| **Analyze** — weeks 4–7 | 22.5% |
| **Create** — weeks 8–15 | 49.5% |

<div class="mt-6">

The three phases split the other 90% as **20 / 25 / 55**.

</div>

<!--
The gate framing matters: it kills the "did I pass" anxiety and makes
running it early the obvious move.
-->

---
layout: default
---

<div class="label">Calendar</div>

# 28 lectures · 13 labs · 3 evenings

<div class="grid grid-cols-3 gap-6 mt-8 items-stretch">
  <div class="card">
    <ph-chalkboard-teacher-bold class="text-3xl text-blue-600 mb-3" />
    <div class="font-semibold mb-1">Lectures</div>
    <div class="text-sm opacity-70 flex-1">Tue + Thu, 3:00–4:30, LCSIB 1355</div>
  </div>
  <div class="card">
    <ph-wrench-bold class="text-3xl text-blue-600 mb-3" />
    <div class="font-semibold mb-1">Labs</div>
    <div class="text-sm opacity-70 flex-1">Mon 3:30 (GGBL 2153) or Tue 12:30 (DOW 1005). Same content, attend either</div>
  </div>
  <div class="card">
    <ph-moon-stars-bold class="text-3xl text-amber-600 mb-3" />
    <div class="font-semibold mb-1">Hackathons</div>
    <div class="text-sm opacity-70 flex-1"><strong>Evenings</strong>, whole cohort, weeks 4 · 7 · 15. First: <strong>Thu Sep 24</strong></div>
  </div>
</div>

<div class="caption mt-6">Put Sep 24 in your calendar tonight. If an evening is genuinely impossible for you, tell us early and we build a makeup path.</div>

<!--
Land the evening commitment now. Someone in this room has a job or a
kid and needs three weeks of warning, not three days.
-->

---
layout: default
---

<div class="label">What the course asks</div>

# The short version

- **Attendance** — **10% of your grade**, 60% lecture / 40% lab. Poll Everywhere, app or browser. **70% earns full credit**
- **Late work** — 10%/day for 3 days, then zero. No late days
- **Individual work** — talk about ideas freely, never share code or prompts
- **Costs** — *nothing*. No textbook, no LLM spend. If your laptop can't serve a model, CAEN covers you. Details on Ed

<!--
Costs gets the serif emphasis: it's the promise that makes the local
model policy fair, and it's why nobody needs a subscription.
-->

---
layout: statement
---

If you can *explain* it, it's yours.

<!--
THE slide of the day. Slow down.

AI use is required here, not tolerated. What's graded is understanding:
explain any line you hand in, document tools/models/prompts. If you
can't explain it, it isn't yours — and that's an Honor Code matter.
-->

---
layout: section
---

# Where We Are

## Fall 2026

<!--
Bridge: Before we go further into our plan, situate where we are in the industry.
-->

---
layout: default
---

<div class="label">Four waves</div>

# A brief history

<v-clicks>

- **Wave 1 — Autocomplete** (2021–22). GitHub Copilot. One file, you drive.
- **Wave 2 — Chat** (2022–23). ChatGPT, then chat inside the IDE. Ask, paste, adapt.
- **Wave 3 — Agentic tools** (2023–25). Cursor and Aider, then Claude Code and Codex. Multi-file edits; the tool runs commands.
- **Wave 4 — Orchestration** (2025–now). Several agents, long-running, supervised. Where Create takes us.

</v-clicks>

<!--
Autocomplete predates wave 1 — Kite, TabNine — but Copilot is where it
became load-bearing, so that is where the clock starts.
Most students entered at Wave 3. We're heading to Wave 4 by December.
-->

---
layout: statement
---

The hype was steep. The reality is *more interesting*.

<!--
Honesty moment. AI did not replace programmers. A new category of workflow emerged.
The developers who learned to work WITH AI became dramatically more productive.
-->

---
layout: section
---

# Take Five

## Talk to your neighbor

<!--
Bridge: Pause. Connect this to your own experience before we layer on the philosophy.
-->

---
layout: default
---

<div class="label">5 minutes · neighbor conversation</div>

# Compare notes

<div class="mt-6 text-base">

> Think about the last time you wrote code with help from an AI tool — or the last time you wrote code *without* one. What felt productive? What felt frustrating? When you finished, did you feel like you had *learned* something, or just *gotten an answer*?

</div>

<div class="caption mt-6">This question sits underneath everything in this course.</div>

---
layout: section
---

# Code Curator

## The Philosophy

<!--
Bridge: Hold whatever you just discussed with your neighbor. Here's the mental model that reframes it.
-->

---
layout: two-col
---

## Typist

<div class="mt-6 space-y-4">
  <div class="flex gap-3 items-start">
    <ph-keyboard-bold class="text-3xl text-blue-600 mt-1 flex-shrink-0" />
    <div>
      <div class="font-semibold">Writes lines</div>
      <div class="text-sm opacity-70">Syntax, formatting, boilerplate.</div>
    </div>
  </div>
  <div class="flex gap-3 items-start">
    <ph-clock-bold class="text-3xl text-blue-600 mt-1 flex-shrink-0" />
    <div>
      <div class="font-semibold">Spends time on HOW</div>
      <div class="text-sm opacity-70">Implementation mechanics.</div>
    </div>
  </div>
  <div class="flex gap-3 items-start">
    <ph-user-bold class="text-3xl text-blue-600 mt-1 flex-shrink-0" />
    <div>
      <div class="font-semibold">Owns the keystrokes</div>
      <div class="text-sm opacity-70">Correct means "I typed it right."</div>
    </div>
  </div>
</div>

::right::

## Curator

<div class="mt-6 space-y-4">
  <div class="flex gap-3 items-start">
    <ph-compass-bold class="text-3xl text-amber-600 mt-1 flex-shrink-0" />
    <div>
      <div class="font-semibold">Specifies intent</div>
      <div class="text-sm opacity-70">What and why, not how.</div>
    </div>
  </div>
  <div class="flex gap-3 items-start">
    <ph-magnifying-glass-bold class="text-3xl text-amber-600 mt-1 flex-shrink-0" />
    <div>
      <div class="font-semibold">Evaluates output</div>
      <div class="text-sm opacity-70">Reviews, redirects, accepts.</div>
    </div>
  </div>
  <div class="flex gap-3 items-start">
    <ph-shield-check-bold class="text-3xl text-amber-600 mt-1 flex-shrink-0" />
    <div>
      <div class="font-semibold">Owns the outcome</div>
      <div class="text-sm opacity-70">Correct means "it works and I can defend it" — whoever typed it.</div>
    </div>
  </div>
</div>

<!--
The philosophical shift. Same engineer, different time allocation.
-->

---
layout: statement
---

**KISS**: Keep prompts focused; resist the urge to over-explain.

<!--
Not the networking protocol. KISS in this course = clarity beats verbosity.
-->

---
layout: section
---

# PollEv

<!--
Presenter cue only — switch to the browser tab holding the activity.
Set it live, read the question and all four options aloud, give it ~60s,
show results, then come back to the deck.
-->

---
layout: two-col
---

## Bad

<div style="min-height:200px">
<div class="text-sm opacity-60 mb-1">Writing something new</div>

```text
Please could you help me write
a Python function that iterates
through a list of integers,
checks if each one is even,
and if it is even adds it to
a new list... actually I think
a list comprehension is cleaner
but I'm not sure...
```

</div>

<div class="text-sm opacity-60 mb-1">Chasing a failure</div>

```text
The tests are failing. Something
with dates? Or the timezone
maybe? Can you look at it and
just make it work.
```

::right::

## Good

<div style="min-height:200px">
<div class="text-sm opacity-60 mb-1">Writing something new</div>

```text
Write a function that extracts
the even numbers from a list.
```

</div>

<div class="text-sm opacity-60 mb-1">Chasing a failure</div>

```text
test_parse_date fails on
"2026-02-30". Make parse_date
raise ValueError on invalid
dates instead of returning None.
```

<!--
B almost always produces better results. The model infers the rest.
Adding caveats compounds ambiguity; it doesn't resolve it.
-->

---
layout: default
---

<div class="label">Preview · L03</div>

# The Big Three

<div class="grid grid-cols-3 gap-6 mt-8 items-stretch">
  <div class="card">
    <ph-files-bold class="text-3xl text-blue-600 mb-3" />
    <div class="font-semibold mb-1">Context</div>
    <div class="text-sm opacity-70 flex-1">What does the AI know when it starts?</div>
  </div>
  <div class="card">
    <ph-cpu-bold class="text-3xl text-blue-600 mb-3" />
    <div class="font-semibold mb-1">Model</div>
    <div class="text-sm opacity-70 flex-1">Which AI? Capability vs cost vs speed.</div>
  </div>
  <div class="card">
    <ph-chat-bold class="text-3xl text-amber-600 mb-3" />
    <div class="font-semibold mb-1">Prompt</div>
    <div class="text-sm opacity-70 flex-1">How do you specify what you want?</div>
  </div>
</div>

<div class="caption mt-6">L03 goes deep. Today's preview only.</div>

---
layout: section
---

# Discussion

## Two Questions

<!--
Bridge: We've named the principle. Two questions to pressure-test it.
-->

---
layout: default
---

<div class="label">Take one minute each · then we discuss</div>

# Two questions

<v-clicks>

1. If AI can write code, why do you need EECS 281?
2. When would you *not* want to use AI to write code?

</v-clicks>

<!--
Q1 → CS fundamentals still matter; you evaluate the output.
Q2 → learning, security-critical, deep maintenance.
-->

---
layout: section
---

# The Tool

## Why Aider — for now

<!--
Bridge: We've talked principles. NOW the tool — and only because principles came first.
-->

---
layout: default
---

<div class="label">Tool choice · pedagogical</div>

# Why Aider in Apply?

<v-clicks>

- **Big Three are explicit.** No GUI hides context, model, or prompt decisions.
- **Speaks the OpenAI-compatible API.** So it talks to the model *you* serve.
- **Small enough to rebuild.** And you will, starting week 3.

</v-clicks>

<!--
Land reason 2 hard: your model is a line of config, not a dependency.
That is why this course costs nothing to take.
Claude Code arrives in L05 as a DEMO. No account needed. Say it plainly.
-->

---
layout: section
---

# AI Pair-Coding

## A first look

<!--
Bridge: A few minutes — not a tutorial — of what AI pair-coding actually feels like.
Setup was the Setup Lab; the commands are `aider-practice`. Today, just feel the loop.
-->

---
layout: default
---

<div class="label">3 prompts · ~5 minutes</div>

# What the loop feels like

```text
Prompt 1 → "Refactor parse_args() to handle no-args case
            cleanly; print usage and exit."

Prompt 2 → "Add a unit test for the no-args path."

Prompt 3 → "Replace the if-chain in dispatch() with a
            dictionary lookup."
```

<div class="caption mt-4">Three coordinated changes. Tests pass. I wrote zero lines of code.</div>

---
layout: statement
---

I described outcomes. The model produced them. I *judged*.

<!--
That's the collaboration shape. Not the commands — the shape.
-->

---
layout: section
---

# This Week

## `aider-practice` · setup gate · the build

<!--
Bridge: Setup is on you. Here's exactly how the week works.
-->

---
layout: default
---

<div class="label">After class · aider-practice · sixteen guided lessons</div>

# Every lesson is a failing test

<v-clicks>

- **Part 1, lessons 1–10** this week — build `taskr`'s command line on `qwen3.5:4b`
- **Part 2, lessons 11–16** next week — a web front end on the same data. `9b` *recommended*, not required
- You drive Aider until the test passes. *You never have to wonder whether you're done*
- **Setup gate + all sixteen lessons due Fri Sep 11**
- **Lab01** Mon Sep 14 / Tue Sep 15 — the pivot lab

</v-clicks>

<div class="caption mt-6">You already got Aider running in the Setup Lab. Stuck after that? Office hours — any of us, not just me. Times and rooms on Ed by Friday.</div>

---
layout: default
---

<div class="label">The build · shape today, spec at L03</div>

# Your first project

<div class="grid grid-cols-3 gap-6 mt-8 items-stretch">
  <div class="card">
    <ph-package-bold class="text-3xl text-blue-600 mb-3" />
    <div class="font-semibold mb-1">What you build</div>
    <div class="text-sm opacity-70 flex-1">A <strong>pair-programmer</strong>. Everyone builds the same thing: <strong>seven fixed features</strong> on a starter we give you</div>
  </div>
  <div class="card">
    <ph-clock-bold class="text-3xl text-blue-600 mb-3" />
    <div class="font-semibold mb-1">When</div>
    <div class="text-sm opacity-70 flex-1">Build it in <strong>weeks 3–4</strong>, about <strong>6 hrs/week</strong>. Planned due <strong>Fri Sep 25</strong></div>
  </div>
  <div class="card">
    <ph-check-bold class="text-3xl text-amber-600 mb-3" />
    <div class="font-semibold mb-1">What you hand in</div>
    <div class="text-sm opacity-70 flex-1">Code that passes the <strong>feature gate</strong>, plus your spec, session logs, and a short reflection</div>
  </div>
</div>

<div class="caption mt-6">This is the shape, not the spec. The spec — or its release date — comes at <strong>L03, Tue Sep 8</strong>. Nothing to do about it this week: you are in <code>aider-practice</code>.</div>

---
layout: statement
---

Aider will be gone. The *principles* won't.

<!--
The durable thing is the framework. Tools come and go. Claude Code and
Codex are already the successors; say so if it comes up.
-->

---
layout: end
---
