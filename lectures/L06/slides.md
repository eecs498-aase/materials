---
theme: ../theme
title: "L06: From pair-coding to agent orchestration"
info: |
  EECS 498 AASE — Lecture 06
  Applied Agentic Software Engineering, UMich Fall 2026
layout: title
class: text-left
transition: fade
mdc: true
highlighter: shiki
---

# From pair-coding to agent orchestration

## Lecture 06 · Sep 17, 2026

<!--
This closes Apply and opens Analyze. The room was handed the build this week
and, on track, is inside the design rather than running code, so every argument
today is made against their own specification, by requirement ID, rather than
against somebody else's tool.

Nothing about Analyze is due next week. Say that more than once.
-->

---
layout: default
---

<div class="label">Where we are</div>

# Where the build stands

- The packet: seven features, every one numbered
- `design/SYSTEM.md` and three diagrams before code
- Then increment specs, one at a time

<div class="caption mt-6">Specs before code is graded. Nobody is behind.</div>

<!--
Thirty seconds. Do not audit the room and do not ask who has code; the office
hours conversation is the place for that. On track on Thursday means inside the
design, and the rubric reads that order out of git history.

README's reading order is EXAMPLES.md, then SPEC.md and RUBRIC.md; SPEC.md is
the staff contract, seven features with requirement IDs. The other two bullets
are what they write: L04's spec discipline grows into them, the system design
is what the increment specs cite, and each increment spec (specs/, one per
Aider increment) is the bounded, ordered kind they wrote for taskr.

The point of the slide is that they hold a real specification. Everything today
is argued against it, by requirement ID.
-->

---
layout: statement
---

Tuesday's promise: today the loop stops being *someone else's*.

<!--
L05's last slide said "Thursday, the loop stops being someone else's". It is
Thursday. Today the loop is theirs as a specification, it becomes theirs as
code across the build, and in three weeks it stops needing them.

Tuesday made the argument with Aider and a demo. Today the same argument gets
made with their specification, which is a much harder place to hide, because
every requirement has a number.

Place the title's word once. L01's fourth wave and Tuesday's fifth rung call
many agents at once orchestration, and that is Create. Today it means the
harness's job: deciding what the model may choose from, and enforcing it.
-->

---
layout: section
---

# The seam

## Where Apply stops and Analyze starts

---
layout: default
---

<div class="label">Naming it precisely</div>

# Three words for Aider's loop

<div class="grid grid-cols-3 gap-6 mt-8 items-stretch">
  <div class="card">
    <ph-arrows-clockwise-bold class="text-3xl text-blue-600 mb-3" />
    <div class="font-semibold mb-1">Fixed</div>
    <div class="text-sm opacity-70 flex-1">A small set of cycles, chosen when it was written.</div>
  </div>
  <div class="card">
    <ph-stack-simple-bold class="text-3xl text-blue-600 mb-3" />
    <div class="font-semibold mb-1">Shallow</div>
    <div class="text-sm opacity-70 flex-1">A turn never compounds on itself.</div>
  </div>
  <div class="card">
    <ph-user-bold class="text-3xl text-amber-600 mb-3" />
    <div class="font-semibold mb-1">Human-framed</div>
    <div class="text-sm opacity-70 flex-1">You choose files, each step, and when it ends.</div>
  </div>
</div>

<!--
Resist "Aider is not agentic." Tuesday already rejected that, and they will
remember. Aider has a loop, tools, planning in architect mode, and session
state.

Fixed means the repertoire was decided when the program was written, not when
it ran: edit, resend a miss up to three times (the number Lab01 gave them), run
the configured tests, plan first in architect mode. On the third try it has the
moves it had on the first. Shallow means nothing in a turn is chosen because of
something discovered two steps earlier, since there are no two steps earlier;
the offer to add a file (L03) routes through their yes, and the repo map
(Lab01) is a fixed ranking rule. Human-framed: Aider writes and commits before
asking, so for two weeks the turn ended at the commit and their /undo. L01 put
Aider in the third wave, a tool that reads and keeps going; finish the sentence
for them: inside a boundary they drew.

None of the three is an insult. A pair-programmer that narrowed its own scope
would be a worse pair-programmer.
-->

---
layout: default
---

<div class="label">Your own requirements</div>

# The three words as requirements

| In your spec | Which word |
|---|---|
| §1 — no discovery, no commands, no tool choice, no self-repair | Fixed |
| F1.4, F5.1 — one request, one reply, done | Shallow |
| F2.1, F6.6 — you `/add`, you approve | Human-framed |

<!--
This is the slide the lecture turns on. Put SPEC.md on the screen and read the
lines; let them find the IDs in their own copy.

Section 1's "what this program is not" is a fixed repertoire written down as a
requirement: the list of things it will not do is longer than the list it will.
F1.4 makes every request the same three things and F5.1 parses one complete
reply; F1.5 trims rather than reads when the budget is hit. Shallower than
Aider: no repo map, no offer to add a file. Their program is more human-framed
than the tool they are building it with.
-->

---
layout: default
---

<div class="label">F6.5, F6.6, F6.7</div>

# An approval layer for files

- A complete unified diff before any write
- Explicit approval, or nothing happens
- Blank, EOF, interrupt: all mean no

<div class="caption mt-6">Aider writes first. Yours must ask. One kind of action, and the most important code you write this month.</div>

<!--
Pause here. They do not think of it as an approval layer and it is exactly one,
and it is one Aider does not have: Aider writes and commits, and /undo is the
recovery.

F5.4, F6.2 and F6.7 make it a mechanism rather than a request: a block naming a
file outside the selected set is rejected however confidently the model asked,
and F4.4 says the prompt is not what enforces it. Their program is
constitutionally incapable of changing a file they did not put in front of it
and did not say yes to. Hold that thought for forty minutes; the second half is
what happens to it when a shell arrives.
-->

---
layout: default
---

<div class="label">Every turn, for two weeks</div>

# Three decisions a human supplies

1. **Which files** are in play
2. **What the next step** is
3. **When the turn** is over

<!--
Strip the vocabulary away and this is all a pair-programmer is. One is L03's
context lever; two is its prompt lever, one bounded task per turn, which
Tuesday called where the task ends; three is the commit and /undo for Aider,
and the yes or no at the prompt for their build.

Lab01's harness table had four rows: what the model sees, what happens to a
reply, what comes next, what survives the session. These are the first three
from the person's side; the fourth is on v0's exclusion list.

Number two is today. Taking it away forces the other two: a program choosing
its next step has to choose what to read (a search problem) and when it is
finished (a stop-condition problem).
-->

---
layout: statement
---

Take the second one away.

<!--
Say it and leave it up for a beat.

They still type the goal. What they stop supplying is the next step. Not new
intelligence, not a better model (L03: the failure was never the model, and the
fix is not the model either). The same model, handed a set of actions and a
loop that lets it pick the next one, behaves like a different category of
software.

If someone says L04's architect run already did this: they pasted a whole spec
and read the result, but the spec listed its steps in order so the model would
not have to discover them. Decision two, supplied in advance. An agent
discovers the order as it goes.
-->

---
layout: section
---

# Deepen and generalize

## Two moves, and they land in different weeks

---
layout: default
---

<div class="label">Generalize</div>

# A tool layer with many verbs

- `read_file` — the program chooses, not you
- `write_file` — same edits, no `/add`
- `run_command` — the one that changes your machine

<!--
Read file sounds redundant when /add exists, and the difference is the whole
point. /add is them choosing. read_file as a tool is the program choosing,
which means it can go and look at something nobody mentioned because of
something it saw two steps ago.

L02's rule survives the move: the best context is the smallest that holds the
relevant information. A model picking its own reads is filling its own
haystack, which is one reason the stop conditions are code.

Flag run_command and move on. It gets fifteen minutes after the break.
-->

---
layout: default
---

<div class="label">Function calling</div>

# The shape of a tool call

```json
{"tool_calls": [
  {"name": "read_file",   "arguments": {"path": "cli.py"}},
  {"name": "write_file",  "arguments": {"path": "cli.py", "content": "..."}},
  {"name": "run_command", "arguments": {"command": "pytest -q tests/"}}
]}
```

<div class="caption mt-4">Three verbs, one shape. A parseable request, not prose. Your code decides what happens next.</div>

<!--
You describe each tool as a name, a description, and a parameter schema. The
model replies with a structured request rather than text. The three calls are
the three verbs from the last slide; a reply may carry one or several, which is
why the loop slide iterates over the array.

Walk the JSON slowly. This shape is the entire reason an approval layer is
possible at all: there is a moment, after the ask and before the act, that
belongs to code they wrote. L04 showed them that moment already, as the
architect pause: the cheapest place to catch a misunderstanding, because
nothing has touched disk.

Lab02's example does this with a JSON action their own parser recognizes rather
than native function calling. Same shape; either is a valid protocol.
-->

---
layout: statement
---

The model never runs anything. It *asks*.

<!--
The sentence to carry out of the first half. L02 said it in week one: the core
inference call has no lookup and no hands; tools are wrapped on by a program,
and they were told they would write those tools in week 5. This is that
promise being kept.

If a student objects that Claude Code clearly ran commands on Tuesday: it
asked, and the harness ran them, having consulted a permission setting. Same
shape, more polish.
-->

---
layout: default
---

<div class="label">Deepen</div>

# The loop that picks its step

```python
while True:
    reply = model.call(messages, tools=TOOLS)
    if not reply.tool_calls:
        return reply.text          # the model is done
    for call in reply.tool_calls:
        result = execute(call)     # your code, your rules
        messages.append(result)
```

<!--
Six lines and the pair-programmer's loop is gone. Nothing in there says which
file to read, what the next step is, or when to stop.

The model supplies all three, turn after turn, from inside a single request the
user typed once.

This is week 5's lab. They will write this exact shape.
-->

---
layout: default
---

<div class="label">What did not change</div>

# What the harness still does

- The model still only emits text
- Every read, write and command is yours
- What moved is *who chose*

<!--
Worth being explicit, because the loop slide reads as a loss of control and it
is not, quite.

Tie it back to Tuesday's question, which is now answered from the inside: who
picks the next action. In week 5 their own code will be the thing that stopped
picking.
-->

---
layout: default
---

<div class="label">Week 5</div>

# Four stop conditions

- A cap on iterations
- A cap on tokens
- A detector for repeated identical calls
- A clean interrupt, mid-loop

<!--
A loop that runs until the model says it is finished will sometimes not finish.
Same tool, same arguments, forever. Or it decides a task is complete when it is
not.

They have the beginnings of the last one. F6.6 says an interrupt at the prompt
writes nothing; F6.10 restores every affected file when a write fails part way.
What Stage 1 scopes out, a crash mid-write, is what an unattended loop has to
survive. That requirement gets considerably more interesting when the thing
being interrupted is a loop rather than a turn.
-->

---
layout: default
---

<div class="label">Five minutes with a neighbor</div>

# Handing one task over

Pick one task from your own build that you would hand over completely,
so that you type it once and read the result at the end.

What would the program be allowed to do without asking you first?

What is the earliest thing on that list you would refuse?

<div class="caption mt-6">Which was harder to write down, the permission or the refusal?</div>

<!--
**"OK, Zoom, we're on break."**

Circulate. Five minutes.

**"OK, Zoom, we're back."**

Take two or three. Listen for whether anybody reaches for a rule rather than a
yes or no. If somebody does, that is the second half and you can name them for
it. If nobody does, say so out loud and use it as the transition.
-->

---
layout: section
---

# Agent v0

## Weeks 5 to 7, in the repository you already have

---
layout: default
---

<div class="label">One repository, weeks 1 to 15</div>

# From pair-programmer to v0

- No new repo, no fresh start
- The same git history, all term
- It ends as the assistant you demo

<!--
Structural fact and they should hear it from you before they read it in the
Analyze packet: the design they commit this week is in the same history as the
agent they gate in week 7. Lab01 called this milestone M2; the packet calls it
v0.

It is also the cheapest authenticity evidence the course has, though you do not
need to say that part.
-->

---
layout: default
---

<div class="label">Three build weeks</div>

# What each week delivers

| Week | The piece | The question it answers |
|---|---|---|
| 5 | Tools, the loop, stop conditions, manual approval | Why does it not stop? |
| 6 | Auto-approval rules, decision log, endpoint measured | What did the human silently supply? |
| 7 | Eval harness and the gate | Where does it fail, measured? |

<!--
Built in weeks 5 to 7. Week 4 belongs to Apply, and the Analyze packet does not
land until October 6, when the build is due.

Week 5 is the week the program stops being a pair-programmer. Week 6 is where
the human actually leaves. Week 7 is where they find out what that cost.
-->

---
layout: default
---

<div class="label">By design, not by accident</div>

# What v0 will not do

- No command sandbox
- No session across runs
- No sub-agents, no MCP, no hooks
- No compaction when the context fills

<!--
State this plainly. Some of them have read about the tools in the June version
of this course and will expect those things here.

Every item is a week in Create, weeks 10 to 13, and they will be adding it to
an agent they wrote rather than to a tool somebody handed them.
-->

---
layout: statement
---

That list is the *syllabus* for Create.

<!--
Leaving week 7 with a measured list of everything your agent cannot do is not a
failure report.

It is the only honest way to start the second half of a course like this, and
it is why Analyze ends in a teardown report rather than a demo.
-->

---
layout: section
---

# The approval layer

## Forced by a mechanism, not chosen out of caution

---
layout: default
---

<div class="label">Today</div>

# What git covers

- One commit per accepted, nonempty edit set
- `/undo` walks back your session's commit
- Refuses when a human commit intervenes

<div class="caption mt-6">A complete guarantee, while files are all you touch.</div>

<!--
F7.3, F7.5 and F7.6. They are designing this, and the spec is exact about it.

Emphasize "complete". There is no hole in it today, because git's model of the
world is files and files are the only thing their program touches.
-->

---
layout: default
---

<div class="label">Week 5, when `run_command` lands</div>

# The hole a shell opens

```text
/undo  →  rm -rf build/
/undo  →  git reset --hard
/undo  →  curl … | sh
/undo  →  pip install anything
```

<div class="caption mt-4">None of these were ever in the repository.</div>

<!--
Go slowly and let the list land. The net now has a hole in it the exact size of
everything git does not track.

And the loop issuing those commands is on their own laptop, driven by a 4B
or a 9B, models they have watched be confidently wrong for two weeks.

An earlier version of this course scheduled the permission model for week 10.
That is five weeks of unsupervised shell access with nothing in front of it,
which is not a pedagogical risk, it is a broken machine.
-->

---
layout: default
---

<div class="label">Four steps</div>

# Four steps of an approval layer

1. **Intercept** before execution, never after
2. **Prompt** to allow or deny, command shown
3. **Consult** a rules file for auto-approval
4. **Log** the decision, whatever it was

<!--
Three of the four are already in their specification, for files. Point back at the F6.5
diff and the F6.6 yes.

Step one is the one worth dwelling on. After the model asks and before your
code acts, there is a moment that belongs to them. Everything else is what they
choose to do with it.
-->

---
layout: default
---

<div class="label">The order is the lesson</div>

# Manual first, rules second

- Week 5: the prompt, about ten lines
- Week 6: the rules file, after a week of watching

<div class="caption mt-6">A rule written before you have seen the traffic is a guess.</div>

<!--
The prompt ships in week 5 with run_command because nothing else is protecting
the machine, and because it is genuinely ten lines.

The rules file waits a week on purpose. This is the design's own advice turned
into a schedule: build the manual path, live with it, then write rules. They
will want to skip to the rules. Tell them the week-6 lab depends on having a
week of their own traffic to write against.
-->

---
layout: default
---

<div class="label">Week 7, unattended</div>

# The tension the gate measures

- **Too tight** — the run stalls, no human to ask
- **Too loose** — you find out the other way

<div class="caption mt-6">Your approval log is graded evidence.</div>

<!--
The gate runs v0 against a fixed task with nobody in the room, so an agent that
asks about every command stalls, and L01 told them gates are scored rather than
passed: it earns whatever it finished before it stalled.

So the gate does not really measure whether the agent works. It measures the
allowlist. They can run it at home all week; hackathon 2 in week 7 is the
observed attempt, a room full of people finding out which way they got it
wrong.

The teardown report asks the question only the log can answer: which rules did
you loosen to pass, and what did that cost you?
-->

---
layout: default
---

<div class="label">What is ahead</div>

# The weeks ahead

| When | What |
|---|---|
| Mon 21 / Tue 22 | Lab02: a 40-minute actions example, then build time |
| Tue Sep 22 | L07, where Analyze starts |
| Thu Sep 24, evening | Hackathon 1, on a supplied application |
| Tue Oct 6, 11:59 PM | The build is due, then the Analyze packet |

<div class="caption mt-6">Nothing about Analyze is handed out next week. Spend Lab02's second half on the build.</div>

<!--
Say the caption out loud. A student who leaves thinking Analyze work starts
Monday will spend the most valuable supported build time of the phase on the
wrong thing.

The Analyze packet does not exist for them until October 6, the day the build
is due. That is deliberate: they never hold two graded specs at once. Analyze
arrives in the lectures first and on paper later.

Lab02 opens with forty minutes on a stockroom app: functions become actions the
model requests, in the shape they saw an hour ago, one increment built with
Aider from an increment spec. Then seventy minutes of supported build: finish
the design, then increments and tests, reconciled against design/SYSTEM.md.

Hackathon 1 is two hours on a supplied, working application: they design and
build its AI capabilities from a prompt revealed in the room and submit inside
the session. It does not depend on their build and nothing from it goes into
their build.
-->

---
layout: default
---

<div class="label">Take these with you</div>

# Three questions

1. Which decision would you give up first, and what breaks?
2. What would you allowlist, and what would you never?
3. Forty steps, wrong answer: what did you log?

<!--
Leave this up through questions.

Number two comes back in week 6 as an actual file they write. Number three is
the one that makes them better engineers this week, because it is a question
about their own build's logging and they can act on it in Lab02.
-->

---
layout: statement
---

Tuesday, we *open* the client.

<!--
The bridge to L07, whose title says "the client you were handed".

For two weeks the endpoint was one line in Aider's configuration and a client
somebody else wrote. This week they are writing their own against ENDPOINT.md:
the request, the roles, the stream. Tuesday opens both, the one they were
handed and the one they are writing, and Analyze starts in this room.
-->

---
layout: end
---
