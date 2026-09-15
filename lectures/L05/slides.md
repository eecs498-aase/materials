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

You sorted the prompt by who chose each part.

| Part of the prompt | Chosen by |
|---|---|
| System prompt | Aider, by mode |
| Added and read-only files | You, by command |
| Repo map | Aider, by a ranking |
| History | You start it, Aider trims it |
| Your message | You |

**Two rows you never touched. One of them passed for intelligence.**

<!--
Thirty seconds of recall, no more. Monday's room did this yesterday, Tuesday's
finished ninety minutes ago, so this is a pointer and not a recap.

Lab01's table, unchanged. It is here because the whole lecture is about that
right-hand column, and because the answer they gave yesterday is about to get
one row longer.

Read down the right side and stop. Do not answer the next slide.
-->

---
layout: default
---

<div class="label">Aider is one</div>

# Aider, the model, and the repo

<div class="mt-2">
<svg viewBox="0 0 900 330" style="width:100%;max-height:330px" role="img"
     aria-label="Aider sits between your repository and the model. Aider reads files, sends prompt text up to the model, receives reply text, then writes and commits. No line connects the model to the repository.">
  <defs>
    <marker id="ar-b" markerWidth="9" markerHeight="9" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="var(--c-primary)" /></marker>
    <marker id="ar-a" markerWidth="9" markerHeight="9" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="var(--c-amber)" /></marker>
  </defs>
  <rect x="300" y="8" width="300" height="58" rx="8" fill="var(--c-highlight)" stroke="var(--c-amber)" stroke-width="2.5" />
  <text x="450" y="34" text-anchor="middle" style="font:600 17px var(--font-mono)" fill="var(--c-amber)">the model</text>
  <text x="450" y="53" text-anchor="middle" style="font:400 12.5px var(--font-sans)" fill="var(--c-ink-soft)">text in, text out</text>
  <rect x="40" y="128" width="820" height="92" rx="10" fill="var(--c-bg-1)" stroke="var(--c-rule-strong)" />
  <text x="58" y="151" style="font:500 11px var(--font-mono); letter-spacing:0.14em" fill="var(--c-ink-muted)">AIDER</text>
  <rect x="70" y="160" width="220" height="44" rx="6" fill="var(--c-bg-0)" stroke="var(--c-primary)" stroke-width="1.5" />
  <rect x="340" y="160" width="220" height="44" rx="6" fill="var(--c-bg-0)" stroke="var(--c-primary)" stroke-width="1.5" />
  <rect x="610" y="160" width="220" height="44" rx="6" fill="var(--c-bg-0)" stroke="var(--c-primary)" stroke-width="1.5" />
  <g style="font:500 14.5px var(--font-mono)" fill="var(--c-ink)" text-anchor="middle">
    <text x="180" y="187">assemble request</text>
    <text x="450" y="187">parse and apply</text>
    <text x="720" y="187">commit</text>
  </g>
  <rect x="40" y="256" width="820" height="54" rx="10" fill="var(--c-bg-1)" stroke="var(--c-rule-strong)" />
  <text x="450" y="289" text-anchor="middle" style="font:500 15px var(--font-mono)" fill="var(--c-ink)">your files  ·  git repository</text>
  <g stroke="var(--c-amber)" stroke-width="2" fill="none">
    <path d="M180,158 V100 H350 V70" marker-end="url(#ar-a)" />
    <path d="M550,68 V100 H450 V156" marker-end="url(#ar-a)" />
  </g>
  <g style="font:500 12.5px var(--font-sans)" fill="var(--c-amber)" text-anchor="middle">
    <text x="264" y="91">prompt text</text>
    <text x="502" y="91">reply text</text>
  </g>
  <g stroke="var(--c-primary)" stroke-width="2" fill="none">
    <path d="M110,252 V210" marker-end="url(#ar-b)" />
    <path d="M450,208 V250" marker-end="url(#ar-b)" />
    <path d="M720,208 V250" marker-end="url(#ar-b)" />
  </g>
  <g style="font:400 12.5px var(--font-sans)" fill="var(--c-ink-muted)">
    <text x="122" y="236">reads</text>
    <text x="462" y="236">writes</text>
    <text x="732" y="236">records</text>
  </g>
</svg>
</div>

<div class="caption">The model touches no file.</div>

<!--
Lab01's slide, as they saw it. Do not re-teach it: ask them to name the three
boxes and move.

The three boxes are five of the six steps, which is the point of putting it
back up. Assemble the request. The model answers. Parse the reply and apply
it. Record it. Nobody drew them as a numbered line yesterday, and the next
slide does.
-->

---
layout: default
---

<div class="label">The loop, written out</div>

# Six steps, in order

<div class="mt-4 text-base">

<div class="grid grid-cols-6 gap-2 items-stretch">
  <div class="card"><div class="text-sm font-semibold">1 assemble</div><div class="text-xs opacity-70 mt-1">you and Aider, per the table</div></div>
  <div class="card"><div class="text-sm font-semibold">2 answer</div><div class="text-xs opacity-70 mt-1">the model. Text out</div></div>
  <div class="card"><div class="text-sm font-semibold">3 parse</div><div class="text-xs opacity-70 mt-1">Aider, by a fixed rule</div></div>
  <div class="card"><div class="text-sm font-semibold">4 apply</div><div class="text-xs opacity-70 mt-1">Aider, or it refuses</div></div>
  <div class="card" style="border-color:var(--c-amber)"><div class="text-sm font-semibold" style="color:var(--c-amber)">5 repair</div><div class="text-xs opacity-70 mt-1">only if 4 failed</div></div>
  <div class="card"><div class="text-sm font-semibold">6 commit</div><div class="text-xs opacity-70 mt-1">Aider, every time</div></div>
</div>

</div>

<div class="caption mt-6">One request, start to finish, and the order never varies. Step 2 is the only one the model takes.</div>

<!--
The diagram before this drew three boxes. This is the same thing as a line,
because the argument needs an order to point at.

Five of the six were on that diagram. Step 5 is the one it does not draw, and
the next slide is why.

The number to land: exactly one of six belongs to the model. Ask for it out
loud rather than saying it. At every other step the thing deciding what
happens next is them, or a rule somebody wrote down in advance.
-->

---
layout: default
---

<div class="label">The one that loops back</div>

# Repair is an insertion, not a stage

<div class="mt-4 space-y-2">

- A block that does not match is **normal**, not exceptional
- Aider writes the failure back as a prompt, and step 2 runs again
- Up to three times, then it gives up and tells you

</div>

<div class="caption mt-6">It re-enters at step 2. It never chooses a different step, and it never chooses a different file.</div>

<!--
Say this, in these words: a block that does not match is normal, not
exceptional. The model quotes the lines it wants to replace, and the quote has
to match the file exactly. One line it remembered wrong, and the block does not
apply. Aider sends the miss back as the next prompt and runs step 2 again, up
to three times, then it stops and tells you.

This is the slide that keeps the "Aider has a loop" claim honest twenty
minutes from now, so do not skip it.

Repair is the only backward arrow in the whole sequence, which is why it was
not on Lab01's diagram: three boxes left to right cannot draw it.

The two things that make it a fixed loop rather than a decision: it always
re-enters at the same step, and the repertoire it re-enters with is the same
one it started with. Nothing new becomes possible on attempt two.

Say the retry limit. Three, then it stops. A loop with a counter is still a
loop, and it is still not choosing.
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

<div class="caption">The blue rung is where you have spent two weeks. M1 is this rung; M2 and M3 are rung 4.</div>

<!--
Walk up it once, fast, one sentence each. The detail is in content.md and they
do not need all of it.

The dashed line is the slide. Rungs 1 to 3 differ in how much they automate.
Rung 4 differs in who decides. That is a change of kind, not of degree.

Lab01 names three milestones for the build: M1 pair-programmer, M2 agent, M3
assistant. Those are the shapes one repository passes through; the rungs are
where any tool sits. M1 is rung 3, M2 crosses the dashed line to rung 4, M3
stays there and hardens it. Say it once so the two ladders do not compete.
Monday's room heard the older closing without the milestone names, so say
them as if new.
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

The six steps, for the callback: 1 assemble, you and Aider per the table.
2 answer, the model, text out. 3 parse, Aider by a fixed rule. 4 apply,
Aider, or it refuses. 5 repair, only if 4 failed, and it re-enters at 2.
6 commit, Aider, every time. One of six belongs to the model. At every other
step the chooser is you or a rule somebody wrote down in advance.
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

## Five minutes, on the tool you already know

---
layout: default
---

<div class="label">Chat break · 5 minutes</div>

# Give one choice away {.assert}

Two weeks of Aider on taskr. Three choices are still yours every time:
which files it sees, where the task ends, whether the plan runs.

Hand **exactly one** of them to the model.

**Then say what you would have to build before you would let that loose
on a repository you care about.** Which is more work, the handover or the guardrail?

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
Same request as lesson three, deliberately. One task at two rungs is the only honest
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
there is no recording behind this, so if the network is down see `assets/demo-fallback.md`.

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

You were handed this shape in lab. Nothing changes on disk until a human
approves it, and that holds whatever the model says, because the program
enforces it, not the prompt.

**The same question scales up: when the model can run commands, which ones run
without being asked?**

<!--
Tie it to the specification they were handed: F6, preview, approval and
application. Lab01's closing table already put it in front of them as the rule
they will write.

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

# The build is due in three weeks {.assert}

| When | What |
|---|---|
| Thu Sep 17 | L06 closes Apply |
| Mon 21 / Tue 22 | Lab02, supported build time |
| Thu Sep 24, evening | Hackathon 1, on your own project |
| Tue Oct 6, 11:59 PM | The build is due |

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
