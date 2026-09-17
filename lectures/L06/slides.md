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
Three parts today. The project packet that lands after this lecture, how to
work with a model whose code you have to understand, and how the one command
their program already has grows into tool calling and an agent loop.
-->

---
layout: default
---

<div class="label">Today</div>

# Three parts

1. The project: `ai-assistant`
2. Working with the model
3. From edit blocks to tool calls

<!--
Name the three and move on. The first is logistics and should be quick. The
second is the one to spend time on. The third ends where Analyze begins.
-->

---
layout: section
---

# The project

## `ai-assistant`, due October 6

---
layout: default
---

<div class="label">The build</div>

# Your own pair-programmer

- A terminal chat about files you choose
- The model proposes edits, you approve
- Each approved change becomes a commit

<div class="caption mt-6">Aider, the tool you have used for three weeks. Now you write one.</div>

<!--
Keep this general. They have used Aider for three weeks, so they already know
what a pair-programmer does: you pick files, ask for a change, read the diff,
and it lands in git. They are now writing a small one of their own, in Python,
against a model endpoint.

It works on a separate target repository, never the one it lives in.

What it deliberately does not do: find files on its own, run commands, or
choose its next step. Hold on to that. The last part of today adds exactly
those things.

They build it with Aider, and it never calls Aider. Tell them to read
EXAMPLES.md before anything else. It shows the finished program session by
session.
-->

---
layout: default
---

<div class="label">SPEC.md section 3</div>

# What staff supply and what you decide

| Staff supply | You decide |
|---|---|
| The contract: 7 features | Modules, interfaces and state |
| A starter loop, `bin/assistant`, `bin/test` | Estimator, trimming, file delimiter |
| `ENDPOINT.md` and `ACCEPTANCE.md` | Error messages and commit ownership |
| | Your tests |

<!--
The starter is an echo loop in assistant/cli.py with /quit wired up. It is a
place to begin, not a design they must keep.

The packet is less specific than they might expect, and that is on purpose.
SPEC.md says what the program does from the outside. Everything on the right is
theirs, and the rubric's requirements row pays for settling those decisions,
not for restating the spec. There is no prescribed architecture and no hidden
test suite.

This matters for the middle of today. When the spec does not name a decision,
they have to, and a name is what lets them and the model talk about it.
-->

---
layout: default
---

<div class="label">README.md</div>

# The order of work

1. Read the packet, `EXAMPLES.md` first
2. Design and diagrams, reviewed cold
3. Increments, each spec written first
4. Live evidence, usage, reflection

<div class="caption mt-6">Design is committed before application code.</div>

<!--
Step 2: design/SYSTEM.md and three diagrams (components and data flow, one
request sequence, the edit lifecycle), using DESIGN-GUIDE.md as the checklist.
Then a fresh Aider session reviews the document without the chat that drafted
it. That is the fastest way to find what is missing.

Step 3: an increment spec in specs/ before each increment, from the five-section
template. Load only the files that increment needs and verify before moving on.
Try the program on a disposable target repository, never on this one.

Step 4: the live edit-prompt protocol in ACCEPTANCE.md with every attempt
recorded, USAGE.md, REFLECTION.md, and diagrams updated to match what they built.
-->

---
layout: default
---

<div class="label">RUBRIC.md</div>

# How the build is graded

| Half | Points |
|---|---:|
| Specification and design | 50 |
| Implementation and tests | 50 |

- Specs before code, read from commit order
- No hidden tests or requirements
- No points for suffering

<!--
Half the grade is the writing. Requirements, architecture, increment specs, the
three diagrams, specs-before-code and the reflection.

Specs before code is scored from git history, so the order they commit in is
evidence.

No points for suffering is the rubric's own phrase. More prompts, more failures
and longer logs earn nothing. An efficient workflow that succeeds can earn full
marks. Tests for unfinished features stay in the suite as strict xfail, never
deleted or weakened.
-->

---
layout: default
---

<div class="label">Dates</div>

# Dates and deliverables

| When | What |
|---|---|
| After this lecture | The packet, in your repository |
| Before any app code | `design/SYSTEM.md` and diagrams |
| Thu Sep 24, evening | Hackathon 1, separate |
| Tue Oct 6, 11:59 PM | The build is due |

<div class="caption mt-6">One repository, all semester. Commit your Aider history.</div>

<!--
Hackathon 1 is a separate two-hour assessment on a supplied application. It does
not need a finished build.

Late work loses 10% per day for three days. Push. A commit that exists only on a
laptop is not submitted.

The same repository carries through Analyze and Create, so preserve the history.
Aider does not commit .aider.chat.history.md, so they commit it themselves at
the end of each session, and never add it to Aider's editable context.
-->

---
layout: section
---

# Working with the model

## Understanding what it writes and what it says

---
layout: default
---

<div class="label">Your job now</div>

# Who understands the code

- The model writes most of the lines
- You own the decisions and outcomes
- Understanding at the right level

<!--
This is the shift the course is built on. Writing code by hand has dropped off,
and so has reading every line. Nobody can keep up with a model line by line, and
that is not the goal. The goal is knowing what the code decides and whether it
does what you meant. "The model wrote it" is still not an answer to any rubric
row.

So the engineering work moves. It moves into the plan, the prompt, and above all
into understanding what came back: the code, and also the prose around the code,
where the model says what it did.
-->

---
layout: default
---

<div class="label">Context lives in two places</div>

# What you hold in your head

- The design and why it is that way
- Where you are in the build
- What is actually verified
- What the model only claimed

<div class="caption mt-6">The model keeps none of this between sessions.</div>

<!--
Every session the model starts from the files you gave it. You are the one who
remembers that the trimming policy was decided last Tuesday, that increment 3
is half done, and that "all tests pass" came from the model, not from bin/test.

The last two bullets are the dangerous pair. Verified and claimed look identical
in a chat window. Keeping them apart is your job, and it is done in your head
unless you give it somewhere better to live.
-->

---
layout: default
---

<div class="label">The hard part</div>

# Judgment at the right distance

| Distance | What it looks like |
|---|---|
| Too close | Reading every line it wrote |
| Too far | Accepting what you never checked |
| About right | Checking contracts and outcomes |

<div class="caption mt-6">Not every line. Every decision.</div>

<!--
This is genuinely hard and nobody gets it right the first week.

Too close and you are reading at human speed behind a model that writes at
machine speed, and you still miss the decision that mattered. Too far and you are
rubber-stamping, which is how a stale-preview bug ends up in a build that
"works".

About right means you know which decisions matter, you check that each one was
kept, and you let tests and diffs carry the detail. You cannot do that without
a way to point at the decisions. Which is the next slide.
-->

---
layout: statement
---

A working relationship needs *shared names*.

<!--
Pause. The rest of this section is one construct, reference points, and then
the question of what else does the same job.
-->

---
layout: default
---

<div class="label">A construct you define</div>

# Reference points

| Name | What it points at |
|---|---|
| `F6` | Previewing and applying edits |
| `design/SYSTEM.md` §6 | Where your safety decisions live |
| `specs/03-preview.md` | The increment that delivers it |
| `test_stale_preview_refused` | What checks it |

<div class="caption mt-4">A short, stable name that you, the model and staff resolve the same way.</div>

<!--
A reference point is a keyword for project state. It is dense: "F6" carries a
whole feature in two characters, to a person across the table or into a prompt,
and a harness can resolve it without the paragraph being pasted in.

When you wrote the code yourself, the name of a thing lived in the code and you
could go look. When a model writes the code from your plan and your prompt, the
name has to live somewhere the model, the grader and you can all point at.
Otherwise every one of them is interpreting a sentence.

Under a context budget that compression is not tidiness. It is what makes the
conversation fit.
-->

---
layout: default
---

<div class="label">From planning this lecture</div>

# Decision codes in a session

<div style="background:#16181c;color:#e4e4e4;font-family:'IBM Plex Mono',ui-monospace,monospace;border-radius:8px;padding:18px 22px;font-size:0.8rem;line-height:1.5">
<div style="color:#8a8f98;margin-bottom:8px">model: decisions before I write the slides</div>
<div style="display:grid;grid-template-columns:4.5rem 1fr;row-gap:0">
<div style="padding:5px 0;border-bottom:1px solid #5a606b;color:#7aa2f7">Code</div><div style="padding:5px 0;border-bottom:1px solid #5a606b;color:#7aa2f7">Decision</div>
<div style="padding:5px 0;border-bottom:1px solid #2e333b;color:#e0af68">D1</div><div style="padding:5px 0;border-bottom:1px solid #2e333b;color:#e4e4e4">The live demo is Claude Code in a repository</div>
<div style="padding:5px 0;border-bottom:1px solid #2e333b;color:#e0af68">D2</div><div style="padding:5px 0;border-bottom:1px solid #2e333b;color:#e4e4e4">The approval layer moves out of this lecture</div>
<div style="padding:5px 0;border-bottom:1px solid #2e333b;color:#e0af68">D3</div><div style="padding:5px 0;border-bottom:1px solid #2e333b;color:#e4e4e4">READ and RUN use made-up markers, not F5's</div>
<div style="padding:5px 0;border-bottom:1px solid #2e333b;color:#e0af68">D4</div><div style="padding:5px 0;border-bottom:1px solid #2e333b;color:#e4e4e4">The tool-call build-up is slides, not live code</div>
<div style="padding:5px 0;border-bottom:1px solid #2e333b;color:#e0af68">D5</div><div style="padding:5px 0;border-bottom:1px solid #2e333b;color:#e4e4e4">The chat break becomes a discussion question</div>
</div>
<div style="color:#8a8f98;margin-top:8px">… D6 to D18</div>
</div>

<!--
This is modeled on planning this lecture with Claude Code. The session was set up so
that any time the model presented three or more decisions, options or findings,
every one got a short code: D for decisions, O for options, Q for questions. The
real table ran to D18.

Point out that nothing about the model changed. One line in a conventions file
told it to number things. The payoff is on the next slide.
-->

---
layout: default
---

<div class="label">The payoff</div>

# Answering by code

<div style="background:#16181c;color:#e4e4e4;font-family:'IBM Plex Mono',ui-monospace,monospace;border-radius:8px;padding:18px 22px;font-size:0.8rem;line-height:1.5">
<div style="display:grid;grid-template-columns:4.5rem 1fr;row-gap:0;row-gap:2px">
<div style="color:#9ece6a">you</div><div>D1 yes. D3 yes. D4 no, do READ live. D5 yes.</div>
<div style="height:10px"></div><div></div>
<div style="color:#7aa2f7">model</div><div>D1, D3, D5 kept.</div>
<div></div><div>D4 changed: READ is live, RUN stays on slides.</div>
<div></div><div>D2 still open. Keep it out?</div>
<div style="height:10px"></div><div></div>
<div style="color:#9ece6a">you</div><div>D2 yes.</div>
</div>
</div>

<div class="caption mt-6">Five of eighteen decisions, in two lines.</div>

<!--
Without codes, that first reply is a paragraph: "I agree with the demo idea and
the markers, but I'd rather do the read part live..." and the model has to guess
which proposal each clause is about. With codes, every clause lands on exactly
one decision, and the model's answer is checkable the same way. It even caught
that D2 was never answered.

This is the working relationship at small scale. The model presents in names,
you answer in names, and nothing gets lost between the two.
-->

---
layout: default
---

<div class="label">DESIGN-GUIDE.md section 1</div>

# Names the packet leaves to you

- SPEC names its 7 features
- You name your acceptance criteria
- Each of your IDs traces to a feature

<div class="caption mt-6">"Restating SPEC.md section 4 earns nothing." RUBRIC.md</div>

<!--
This is why the packet is less specific. SPEC.md stops at the feature. The token
estimator, the trimming policy, the delimiter, how an owned commit is marked,
what each error says: those are decisions, and DESIGN-GUIDE section 1 asks for
each one as an acceptance criterion with a stable ID of their own, mapped to the
feature it serves. The rubric calls that mapping traceable and pays 10 points
for it.

The format is theirs. Something like F6-3 for "a stale preview is refused"
works. What matters is that it is short, it never changes meaning, and it shows
up in the design, the increment spec, the test name and the commit.
-->

---
layout: default
---

<div class="label">Human to model</div>

# Prompting by name

<div class="grid grid-cols-2 gap-6">
<div>

**By paraphrase**

```text
fix the approval stuff so
it's safer
```

</div>
<div>

**By name**

```text
specs/03, task 2 only.
Deliver F6-3.
Make test_stale_preview_refused
pass. Edit preview.py only.
```

</div>
</div>

<!--
The left hands the model a sentence to interpret. It will interpret it, and it
will pick its own idea of "safer".

The right hands it an increment, a task boundary, one criterion, a test that
decides whether it is done, and the file it may touch. Every one of those is a
name the model can resolve against files in its context, and every one is
something the student can check afterwards.

A prompt that paraphrases a requirement drifts from it, and the model cannot
tell. The ID does not drift.
-->

---
layout: default
---

<div class="label">Model to human</div>

# Asking for answers in your names

```text
Before I review: which criteria does this change deliver,
what did you run, and what did you not verify?
```

```text
Delivers    F6-3
Touched     assistant/preview.py
Ran         nothing
Unverified  F6-3 against a real target repository
```

<!--
Names work in both directions. Most of the work of understanding model output is
separating what it did from what it says it did. Ask for the report in your
terms and that separation is a checklist instead of a reading exercise.

"Ran: nothing" is the line you were looking for. Without asking, that would have
been a paragraph saying the change handles stale previews correctly.

Then check it. The names make the claims checkable. They do not make them true.
-->

---
layout: default
---

<div class="label">Human to human, human to harness</div>

# Project state in one line

```text
specs/03 · F6-3 done · F6-4 red: test_write_failure_restores
```

- A message to staff or a neighbor
- The first line of a fresh session
- A commit message

<!--
That line is a complete statement of where a project is, and none of it is a
paraphrase. Staff at office hours know what to open. A fresh Aider or Claude
Code session knows what to load. The commit history reads as a record of
decisions.

This is also the answer to "what you hold in your head". Written down in these
terms, it stops living only in your head.
-->

---
layout: default
---

<div class="label">Where it breaks</div>

# How names fail

- A paraphrase replaces the ID
- The model invents an ID
- The named file is not in context
- A name changes meaning mid-build

<!--
Paraphrase: the prompt says "the trimming rule" and the model picks one.

Invented IDs: models are happy to cite F6-7 when there is no F6-7. Only use names
that resolve to a line in a file.

Not in context: a name is only as good as what it resolves to. If SYSTEM.md is
not loaded, "section 6" is a guess. Check what the session can see.

Changed meaning: renumbering criteria halfway through breaks every test name and
commit that cited them. Add new IDs, do not reuse old ones.
-->

---
layout: default
---

<div class="label">Live demo</div>

# Claude Code in a repository

- Name the task by reference point
- Ask for the report in those names
- Check each claim

<!--
Switch to the terminal and drive it.

Demo content to be written.

Narrate the checking, not the typing. Every time the model makes a claim, say
out loud whether it was verified or only stated.
-->

---
layout: default
---

<div class="label">Five minutes with a neighbor</div>

# Other ways to read a model's output

Reference points are one construct.

Name **one other habit or construct** that makes a model's output easier to understand.

<div class="caption mt-6">One line each. We will collect five.</div>

<!--
**"OK, Zoom, we're on break."**

Circulate. Five minutes.

**"OK, Zoom, we're back."**

Take five and write them on the board. Seeds if the room is quiet:

- Ask for a plan before any edit
- A fixed shape for every reply
- A list of what was not verified
- Small diffs, one task at a time
- Tests as the judge, not the model's summary
- A conventions file the model always loads
- Diagrams the model has to keep current
- Commit messages that cite IDs

Close by pointing out that every one of these is a construct the engineer
defines, not a feature of the model.
-->

---
layout: section
---

# From edit blocks to tool calls

## Growing the one command your program has

---
layout: default
---

<div class="label">SPEC.md F5</div>

# The one command your program has

```text
greet.py
<<<<<<< SEARCH
print("Hello")
=======
print("Hi")
>>>>>>> REPLACE
```

<div class="caption mt-4">Text from the model. Your code parses it and acts, on yes.</div>

<!--
Look at this the other way round. The model writes text. The program finds a
marker it recognizes, pulls out the arguments, and does something in the world
with them, after asking.

That is a command. Their program has exactly one. The question for the rest of
the lecture is what happens when we add a second.
-->

---
layout: default
---

<div class="label">Where the pair-programmer stalls</div>

# When the model needs a file

```text
you     why does greet() print twice?
model   I can't tell without main.py, which calls greet().
you     /add main.py
you     ok, look again
```

<div class="caption mt-4">The model knew what it needed. Only you could fetch it.</div>

<!--
This happens constantly with Aider and it will happen with their program. The
model sees one file, reasons about it, and says what it needs next. Aider cannot
read a file on its own. It can offer to add one, but you still have to say yes
and resend. Their Stage 1 program is stricter still: only /add puts a file in
front of the model.

So in this exchange the person did no thinking. The model named the file. The
person typed it back.
-->

---
layout: default
---

<div class="label">The question</div>

# Why not let it read

- It already names the file it needs
- Reading changes nothing on disk
- You were only relaying

<div class="caption mt-6">So give it a way to ask.</div>

<!--
Take the objection seriously first. We made the user choose files on purpose:
it keeps context small and keeps the user in control. Those are real reasons.

But reading is the safest action there is. Nothing on disk changes, and there is
nothing to undo. If the model can already name the file, making a person copy
that name into /add adds a step and no judgment.

So we let it ask. The same way it already asks for an edit.
-->

---
layout: default
---

<div class="label">Add a command</div>

# A READ command

```text
I need to see the tests before I change anything.
<<<<<<< READ
tests/test_cli.py
>>>>>>> END
```

<div class="caption mt-4">Your code reads the file and sends its contents back.</div>

<!--
Same idea, different marker. The model asks for a file. The harness reads it and
puts the contents in the next message.

Compare with /add. /add is the user choosing. READ is the model choosing, because
of something it saw a moment ago.

This is not in the Stage 1 spec, and the markers here are made up for the
lecture. The point is how little it takes.
-->

---
layout: default
---

<div class="label">Add another</div>

# A RUN command

```text
Let me check the suite first.
<<<<<<< RUN
bin/test
>>>>>>> END
```

<div class="caption mt-4">Your code runs it and sends the output back.</div>

<!--
And again. The model asks for a command. The harness runs it and returns what it
printed.

Flag it: this is the first command that changes the machine rather than a file,
and git does not undo it. Come back to that at the end.
-->

---
layout: default
---

<div class="label">The harness grows</div>

# A dispatcher for three commands

```python
for block in parse_blocks(reply):
    if block.kind == "EDIT":
        result = propose_edit(block.path, block.search, block.replace)
    elif block.kind == "READ":
        result = read_file(block.path)
    elif block.kind == "RUN":
        result = run_command(block.command)
    messages.append({"role": "user", "content": result})
```

<!--
Walk it line by line. One parser, one branch per command, and every branch ends
the same way: a result goes back into the conversation.

Ask the room what the fourth command would be. Search, list a directory, fetch a
URL. Each one is another elif. Let them notice that the branches all look alike.
-->

---
layout: default
---

<div class="label">The pattern</div>

# One shape for every command

| Block | Name | Arguments |
|---|---|---|
| `SEARCH/REPLACE` | `edit_file` | path, search, replace |
| `READ` | `read_file` | path |
| `RUN` | `run_command` | command |

<div class="caption mt-6">A name plus arguments. That is a *tool call*.</div>

<!--
This is the step to slow down on. Strip the markers away and every command is
the same two things: which one, and with what.

Once you see that, the custom markers are just a clumsy encoding. Describe each
command to the model as a name, a description and a parameter schema, and let
it reply in a structured format instead. That is function calling. We did not
add a new idea. We generalized the one their program already has.
-->

---
layout: default
---

<div class="label">Function calling</div>

# The shape of a tool call

```json
{"tool_calls": [
  {"name": "read_file",   "arguments": {"path": "tests/test_cli.py"}},
  {"name": "run_command", "arguments": {"command": "bin/test"}},
  {"name": "edit_file",   "arguments": {"path": "greet.py", "search": "...", "replace": "..."}}
]}
```

<div class="caption mt-4">Same three commands, parseable without a custom format.</div>

<!--
The same table, in JSON. The endpoint does the formatting work, and the harness
gets a list it can loop over instead of text it has to scan for markers.

Nothing else changed. The dispatcher is the same if/elif, keyed on name. And
once commands are just names in a table, adding one is adding a row, which is
why tool calling extends to anything a function can do.
-->

---
layout: statement
---

The model never runs anything. It *asks*.

<!--
The sentence to carry out of this part. The model emits text. Every read, every
command, every write is executed by code the student wrote, and that code can
say no.
-->

---
layout: default
---

<div class="label">Who drives</div>

# Who sends the result back

```text
you     why does bin/test fail?
model   READ tests/test_cli.py
you     (contents) keep going
model   RUN bin/test
you     (output) keep going
model   SEARCH/REPLACE tests/test_cli.py
```

<div class="caption mt-4">Every "keep going" is you, being the loop.</div>

<!--
With READ and RUN added but nothing else changed, this is what a session looks
like. The model asks, the harness acts, and then a person has to send the result
back and say continue.

That person is doing no thinking. They are a loop with a keyboard. So automate
them.
-->

---
layout: default
---

<div class="label">Automate the person</div>

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
Six lines, and the "keep going" is gone. Nothing in there says which file to
read, what the next step is, or when to stop. The model supplies all three from
a request the user typed once.

That is an agent. It is the dispatcher from four slides ago with the person
replaced by while True.
-->

---
layout: default
---

<div class="label">What the loop changed</div>

# Before and after the loop

- The model still only writes text
- Your code still does every action
- The model now picks the next step

<div class="caption mt-6">Only the last line changed.</div>

<!--
The loop can look like handing over control. It is narrower than that. The model
still produces nothing but text. Every read, run and edit is still code the
student wrote, and that code can refuse. The one thing that moved is who decides
what happens next: in their Stage 1 program, the person; in the loop, the model.
-->

---
layout: default
---

<div class="label">What is left</div>

# What the loop still needs

- A cap on iterations and tokens
- A detector for repeated calls
- A clean interrupt, mid-loop
- Approval before `run_command`

<div class="caption mt-6">Undo covers files. It does not cover a shell.</div>

<!--
A loop that runs until the model says it is done will sometimes never be done.
Same call, same arguments, forever. Or it decides it finished when it did not.
So stop conditions become code rather than a key the user presses.

And RUN is the command their safety net does not cover. /undo is a git
operation, and git does not undo rm -rf, a package install, or anything outside
the repository. Their Stage 1 program already asks before it writes a file. The
agent has to ask before it runs a command.

That is Analyze. Do not go further today.
-->

---
layout: default
---

<div class="label">What to do next</div>

# This week and the next two

| When | What |
|---|---|
| Tonight | Read `EXAMPLES.md`, then SPEC |
| Before any app code | Design, diagrams, cold review |
| Thu Sep 24, evening | Hackathon 1 |
| Tue Oct 6, 11:59 PM | The build is due |

<!--
Say the order out loud. Read, design, review, then increments.

The build is where they practice the middle of today: name their own
acceptance criteria, prompt Aider by those names, and check what comes back.
-->

---
layout: end
---
