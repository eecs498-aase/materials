---
theme: ../theme
title: "L05: Modern agentic CLIs"
info: |
  EECS 498 AASE — Lecture 05
  Applied Agentic Software Engineering, UMich Fall 2026
layout: title
class: text-left
transition: fade
mdc: true
highlighter: shiki
---

# Modern agentic CLIs

## Lecture 05 · Sep 15, 2026

<!--
Both lab sections have already met. Do not preview Lab01 and do not reveal the
build; they have both. This lecture surveys the category Lab01 opened.

Claude Code appears on this machine only. Nobody in the room needs an account,
and no slide asks for one.
-->

---
layout: default
---

<div class="label">Where we are</div>

# Lab01 left one question open {.assert}

You followed one request through six steps: assemble, answer, parse, apply,
repair, commit.

At every step, the thing that picked what happened next was you, or a rule
somebody wrote down in advance.

<!--
Thirty seconds of recall, no more. Monday's room did this yesterday, Tuesday's
finished ninety minutes ago, so this is a pointer and not a recap.

If you want one answer out loud, ask which of the six steps belonged to the
model. Step 2, and only step 2.
-->

---
layout: statement
---

Who picks the *next action*?

<!--
This is the whole instrument. One question, asked of any tool, now or in three
years when all of today's names have changed.

Say that out loud: the names on these slides will age badly and the question
will not.
-->

---
layout: section
---

# The autonomy gradient

## Five rungs, and where you have been standing

---
layout: default
---

<div class="label">The gradient</div>

# Five rungs, not a ranking {.assert}

<div class="mt-2">
<svg viewBox="0 0 900 300" style="width:100%;max-height:300px" role="img"
     aria-label="Five rungs rising left to right: completion, chat beside the code, pair-programmer at the command line, agentic command line, many agents at once. A dividing line falls between rung three and rung four, marking where the model begins picking the next action.">
  <line x1="60" y1="262" x2="860" y2="262" stroke="var(--c-rule-strong)" stroke-width="2" />
  <g stroke="var(--c-rule-strong)" fill="var(--c-bg-1)">
    <rect x="70" y="222" width="140" height="34" rx="6" />
    <rect x="230" y="186" width="140" height="70" rx="6" />
    <rect x="390" y="150" width="140" height="106" rx="6" />
    <rect x="550" y="114" width="140" height="142" rx="6" />
    <rect x="710" y="78" width="140" height="178" rx="6" />
  </g>
  <rect x="390" y="150" width="140" height="106" rx="6" fill="var(--c-primary)" fill-opacity="0.14" stroke="var(--c-primary)" stroke-width="2" />
  <g style="font:600 12px var(--font-mono); letter-spacing:0.1em" fill="var(--c-ink-muted)" text-anchor="middle">
    <text x="140" y="282">1</text>
    <text x="300" y="282">2</text>
    <text x="460" y="282">3</text>
    <text x="620" y="282">4</text>
    <text x="780" y="282">5</text>
  </g>
  <g style="font:500 13px var(--font-sans)" fill="var(--c-ink)" text-anchor="middle">
    <text x="140" y="214">completion</text>
    <text x="300" y="178">chat beside code</text>
    <text x="460" y="142">pair-programmer</text>
    <text x="620" y="106">agentic CLI</text>
    <text x="780" y="70">many at once</text>
  </g>
  <line x1="540" y1="40" x2="540" y2="262" stroke="var(--c-amber)" stroke-width="2.5" stroke-dasharray="6 5" />
  <text x="540" y="30" text-anchor="middle" style="font:600 12px var(--font-mono); letter-spacing:0.1em" fill="var(--c-amber)">THE MODEL STARTS CHOOSING</text>
</svg>
</div>

<div class="caption">The blue rung is where you have spent two weeks.</div>

<!--
Walk up it once, fast, one sentence each. The detail is in content.md and they
do not need all of it.

The dashed line is the slide. Rungs 1 to 3 differ in how much they automate.
Rung 4 differs in who decides. That is a change of kind, not of degree.
-->

---
layout: default
---

<div class="label">Rung 3</div>

# You are on rung 3 {.assert}

| | At rung 3 |
|---|---|
| You hand over | One bounded edit task |
| You choose | The files, and where the task ends |
| It automates | Matching, repair, tests, the commit |
| You check | Between tasks |

<div class="caption">Real automation inside a boundary you drew.</div>

<!--
Do not let rung 3 sound primitive. Aider runs commands, loops on test output,
and commits. What it does not do is pick the next task.

If someone says "so Aider is not agentic," push back: it has the parts, and we
are about to check that claim properly.
-->

---
layout: default
---

<div class="label">The trade</div>

# Higher rungs spend more to ask less {.assert}

<div class="grid grid-cols-2 gap-6 mt-6">
  <div class="card">
    <div class="flex items-center gap-3 mb-2">
      <ph-trend-up-bold class="text-3xl text-blue-600 shrink-0" />
      <div class="font-semibold">Cost per unit of work</div>
    </div>
    <div class="text-sm opacity-70">A run that searches, reads five files and runs your tests three times spends far more attention than one bounded edit.</div>
  </div>
  <div class="card">
    <div class="flex items-center gap-3 mb-2">
      <ph-trend-down-bold class="text-3xl text-amber-600 shrink-0" />
      <div class="font-semibold">Decisions you make yourself</div>
    </div>
    <div class="text-sm opacity-70">Fewer choices per finished outcome, and less of your attention spent on each one.</div>
  </div>
</div>

<!--
This trade is the entire gradient. Everything else is detail.

Do not quantify it. Any multiple you say out loud will be wrong by next month
and somebody will quote it back to you.
-->

---
layout: default
---

<div class="label">Choosing a rung</div>

# Rung 3 fits a change you can name {.assert}

A two-line fix in a file you can point at is cheaper and safer at rung 3.

Paying rung 4 prices for it buys nothing.

**The skill is picking the rung, and you cannot pick what you cannot see.**

<!--
The reflex this is aimed at: reaching for the most autonomous tool available
because it is the most autonomous tool available.

Ask when they would rather have the bounded version. Answers you are hoping
for involve knowing exactly what to change, or a blast radius they care about.
-->

---
layout: section
---

# What makes a tool agentic

## Four primitives, and a test you can apply

---
layout: default
---

<div class="label">Definitions</div>

# Four primitives, not a vibe {.assert}

<div class="grid grid-cols-4 gap-4 mt-6">
  <div class="card">
    <ph-arrows-clockwise-bold class="text-2xl text-blue-600 mb-2" />
    <div class="font-semibold mb-1">Loop</div>
    <div class="text-sm opacity-70">Takes another step without being asked.</div>
  </div>
  <div class="card">
    <ph-wrench-bold class="text-2xl text-blue-600 mb-2" />
    <div class="font-semibold mb-1">Tools</div>
    <div class="text-sm opacity-70">Actions beyond emitting text.</div>
  </div>
  <div class="card">
    <ph-list-checks-bold class="text-2xl text-amber-600 mb-2" />
    <div class="font-semibold mb-1">Planning</div>
    <div class="text-sm opacity-70">Breaks a goal into steps.</div>
  </div>
  <div class="card">
    <ph-brain-bold class="text-2xl text-amber-600 mb-2" />
    <div class="font-semibold mb-1">Memory</div>
    <div class="text-sm opacity-70">Something survives the turn.</div>
  </div>
</div>

<div class="caption">"Agentic" is used to mean "recent." These four are checkable.</div>

<!--
Read them once. The next slide is where the work happens, so do not linger.
-->

---
layout: default
---

<div class="label">The test</div>

# Aider has all four {.assert}

| Primitive | Where it already is in Aider |
|---|---|
| Loop | A failed edit becomes the next prompt; tests can feed back |
| Tools | Reads, writes, commits, runs the commands you configured |
| Planning | A plan drafted in prose, stopping for a human to read |
| Memory | Session history, plus a repo map of code you never added |

<!--
This is the slide that surprises the room, so let it. They expect a column of
crosses.

Anyone who has configured lint and test commands has watched the loop run. Ask
if someone has; it lands better from a student.
-->

---
layout: statement
---

The difference is *who chooses*.

<!--
Pause here. This is the sentence the lecture turns on.

Not which primitives exist. Which of them the human still holds.
-->

---
layout: default
---

<div class="label">The move</div>

# One choice changes the rung {.assert}

At rung 3 you choose the files, the boundary, and whether to run the plan.

Move the choosing of the next action from the harness to the model, and
everything people find surprising about agentic tools follows.

<div class="caption">One change. Not a new category of intelligence.</div>

<!--
Worth saying plainly: no new model capability is required to cross this line.
The same model, given a tool menu and a loop that lets it pick, behaves like a
different kind of software.
-->

---
layout: section
---

# Chat break

## Five minutes, on the design you drafted yesterday

---
layout: default
---

<div class="label">Chat break · 5 minutes</div>

# Move your own design up a rung {.assert}

Your assistant sits at rung 3, and your specification puts it there.

Pick **one** primitive you would add: the model choosing its next action,
discovering files you never selected, or carrying state between sessions.

**Then say what you would have to build first to make it safe.**

<!--
**"OK, Zoom, we're on break."**

Five minutes. Circulate.

Everyone names a capability; that half is easy. The half that separates the
room is the guardrail, and the second half of this lecture is an hour-long
worked example of it. If nobody reaches it in the answers, say so and use it as
the transition.

**"OK, Zoom, we're back."**
-->

---
layout: section
---

# PollEv

<div class="mt-5 font-mono text-2xl text-blue-600">https://PollEv.com/marcusdarden365</div>

<!--
Attendance question, about a minute, and it counts. Full text in
`assets/poll-everywhere.md`.

Switch to the browser tab, set it live, read the question and all four options
aloud, give it sixty seconds, show results, come back.

The div is deliberate: the theme uppercases section subtitles and an uppercased
URL path is a different path. Do not "fix" it to an h2.
-->

---
layout: section
---

# The same request, one rung up

## Live, on this machine

---
layout: default
---

<div class="label">The request</div>

# You know what this took at rung 3 {.assert}

```text
Add a --priority flag to taskr's add command.
```

You added three files, because a file you do not add is not in the context.
You framed the task. You read the diff. You found the missing write yourself.

<!--
Same request as Lab01, deliberately. One task at two rungs is the only honest
comparison available in eighty minutes.

Nobody needs the taskr recap. They have been living in it for two weeks.
-->

---
layout: default
---

<div class="label">Live demo</div>

# Nobody types /add {.assert}

<div class="grid grid-cols-3 gap-5 mt-6">
  <div class="card">
    <div class="font-semibold mb-1">It searches</div>
    <div class="text-sm opacity-70">Finds where arguments are parsed, without being told.</div>
  </div>
  <div class="card">
    <div class="font-semibold mb-1">It reads</div>
    <div class="text-sm opacity-70">Follows the code to the files the change actually touches.</div>
  </div>
  <div class="card">
    <div class="font-semibold mb-1">It runs</div>
    <div class="text-sm opacity-70">Executes the tests and reacts to what they say.</div>
  </div>
</div>

<div class="caption">Context assembly became something the program does by acting.</div>

<!--
Switch to the terminal here and drive it. Runbook in `assets/demo-runbook.md`;
if the network is down, the recording is in `assets/demo-fallback.md`.

Narrate the decisions, not the typing. Every time it picks a file, say that
nobody told it to.

Rehearse this before delivering. What it actually does today is a fact about
today's build, not something these slides can promise.
-->

---
layout: default
---

<div class="label">The trace</div>

# Each result chooses the next step {.assert}

```text
search "add_argument"   → three hits, one in cli.py
read cli.py             → finds the parser
read store.py           → finds the save path
edit cli.py, task.py, store.py
run tests               → 1 failed
edit store.py
run tests               → passed
```

Nothing in that order was written down in advance, by anyone.

<!--
Label this as illustrative shape, not a transcript of the run they just
watched. The live run is the evidence; this is the pattern.

The question to leave hanging, because the next section answers it: who stops
a run that is going wrong?
-->

---
layout: default
---

<div class="label">Honesty</div>

# Today's run is a fact about today {.assert}

What you just watched is what this model and this build did with this
repository, this afternoon.

**A run that goes badly is more useful than one that goes well. Do not rescue
it too quickly.**

<!--
Say this whether the demo went well or badly, and say it after rather than
before, so it does not read as pre-emptive excuse-making.

Speed is not the lesson. A tool that gets to the same place faster is a
convenience; a tool that decides which place to go is a different object.
-->

---
layout: section
---

# What the harness still decides

## The part the demo hides

---
layout: default
---

<div class="label">The menu</div>

# The model picks from a menu it did not write {.assert}

<div class="mt-2">
<svg viewBox="0 0 900 290" style="width:100%;max-height:290px" role="img"
     aria-label="The model sits inside a harness. The harness exposes a fixed set of tools, applies permissions, and holds the stop condition. The model chooses among the exposed tools only.">
  <rect x="40" y="22" width="820" height="242" rx="12" fill="var(--c-bg-1)" stroke="var(--c-rule-strong)" stroke-width="2" />
  <text x="62" y="48" style="font:600 11px var(--font-mono); letter-spacing:0.14em" fill="var(--c-ink-muted)">THE HARNESS, WHICH SOMEBODY WROTE</text>
  <rect x="330" y="64" width="240" height="56" rx="8" fill="var(--c-highlight)" stroke="var(--c-amber)" stroke-width="2.5" />
  <text x="450" y="98" text-anchor="middle" style="font:600 16px var(--font-mono)" fill="var(--c-amber)">the model picks</text>
  <g stroke="var(--c-rule-strong)" fill="var(--c-bg-0)">
    <rect x="70" y="168" width="170" height="44" rx="6" />
    <rect x="260" y="168" width="170" height="44" rx="6" />
    <rect x="450" y="168" width="170" height="44" rx="6" />
    <rect x="640" y="168" width="170" height="44" rx="6" />
  </g>
  <g style="font:500 14px var(--font-mono)" fill="var(--c-ink)" text-anchor="middle">
    <text x="155" y="195">search</text>
    <text x="345" y="195">read</text>
    <text x="535" y="195">edit</text>
    <text x="725" y="195">run command</text>
  </g>
  <g stroke="var(--c-primary)" stroke-width="2" fill="none" stroke-dasharray="4 4">
    <path d="M400,120 L160,164" />
    <path d="M430,120 L348,164" />
    <path d="M470,120 L532,164" />
    <path d="M500,120 L718,164" />
  </g>
  <text x="450" y="242" text-anchor="middle" style="font:500 13px var(--font-sans)" fill="var(--c-ink-soft)">permissions gate these  ·  a stop condition ends the loop</text>
</svg>
</div>

<div class="caption">Somebody decided a search tool exists and a database client does not.</div>

<!--
The most important sentence today: the model can only choose from what the
harness exposes, and only under the conditions the harness enforces.

In Analyze they write this box. Say that here; it is the first time the phase
ahead has a concrete shape.
-->

---
layout: default
---

<div class="label">Safety</div>

# Permissions are the real safety layer {.assert}

You already built this shape. Nothing changes on disk until a human approves
it, and that holds whatever the model says, because your program enforces it.

**The same question scales up: when the model can run commands, which ones run
without being asked?**

<!--
Tie it to their own specification explicitly. They wrote the approval gate last
week and may not have noticed it was the same idea.

Do not answer the question on the slide. It is Analyze's, and Lab03's.
-->

---
layout: statement
---

Prose asks. Code and permissions *enforce*.

<!--
They met this line in Lab01. Repetition is the point: it is the design rule the
whole course keeps returning to.

Concretely: a prompt asks the model to stay inside the selected files, and
validation is what actually keeps it there.
-->

---
layout: default
---

<div class="label">Stopping</div>

# A loop needs a reason to stop {.assert}

A goal it can recognize as met. A budget it can spend. A human who interrupts.

At rung 3 the task boundary was the stop condition, and you drew it by hand
every single time.

<!--
Ask what happens without one. You are looking for "it runs forever" and then,
better, "it does damage forever."

This is a design problem, not a model problem, which is the through-line of the
whole second half.
-->

---
layout: default
---

<div class="label">Your build</div>

# Rung 3 is the point, not a limitation {.assert}

Exact matching. One approval before any write. One commit per accepted edit
set. A guarded undo.

Those are what make the state after a failure something you can say in a
sentence and assert in a test.

<div class="caption">Build that, and you have built what a loop needs underneath it.</div>

<!--
The anxiety in the room after a demo like that one is that they are building
last year's tool. Address it directly.

Skip these mechanisms and adding a loop on top just means failing faster.
-->

---
layout: default
---

<div class="label">The habit</div>

# The trace is the evidence {.assert}

When a run produces the wrong outcome, the output does not tell you why.

Which step picked the wrong file? Which result did it misread? Which missing
tool did it improvise around?

**"The model is bad at this" is the answer people reach for, and rarely the one
the evidence supports.**

<!--
Same diagnostic discipline as lab, applied to a longer chain. In lab the three
levers were context, model and prompt; here the chain is longer and the
evidence is the run itself.
-->

---
layout: default
---

<div class="label">The week</div>

# The build is due in ten days {.assert}

| When | What |
|---|---|
| Thu Sep 17 | L06 closes Apply |
| Mon 21 / Tue 22 | Lab02, supported build time |
| Thu Sep 24, evening | Hackathon 1, on your own project |
| Fri Sep 25, 11:59 PM | The build is due |

<!--
Read it once and move. Everything here is also in their repository and on the
schedule.

Bring a runnable increment to the hackathon; the prompt is revealed in the
room.
-->

---
layout: default
---

<div class="label">Take these with you</div>

# Three questions

1. Where on the gradient is the tool you reach for by default, and did you
   choose that or inherit it?
2. What would have to be true before you would let a model run a command
   without asking you?
3. What would you need to see in a trace to be convinced a run failed for a
   reason other than the model?

<!--
Leave this up during questions. Number two is the one that comes back in
Analyze, and number three is the one that makes them better engineers this
week.
-->

---
layout: statement
---

Thursday, the loop stops being *someone else's*.

<!--
The bridge. L06 closes Apply and hands over to Analyze, where they write the
box from the harness slide rather than watching it work.
-->

---
layout: end
---
