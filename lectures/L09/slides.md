---
theme: ../theme
title: "L09: Stop conditions and the approval layer"
info: |
  EECS 498 AASE — Lecture 09
  Applied Agentic Software Engineering, UMich Fall 2026
layout: title
class: text-left
transition: fade
mdc: true
highlighter: shiki
---

# Stop conditions and the approval layer

## Lecture 09 · Sep 29, 2026

<!--
Good afternoon.

Direction: One live moment today, in the second half, from assets/demo-runbook.md. Run
`assets/live/reset` and warm qwen3.5:9b before the room fills. Every rehearsal outcome is
also on the glass, so a dead model costs the theatre and none of the content.
-->

---
layout: default
---

<div class="label">Today</div>

# Two parts

1. The reasons a run ends
2. The check in front of an action

<div class="caption mt-6">Analyze spec 2.2 to 2.5. Released October 6, built in Lab03.</div>

<!--
Two parts. The reasons a run ends, and the check that sits in front of an action nobody read first.

Together they are the week-5 part of the Analyze build. The spec calls them 2.2 to 2.5. It is handed out on October 6 and you build this in Lab03, so today you are hearing the part before you are holding it.
-->

---
layout: default
---

<div class="label">L07, last week</div>

# The nine-step run

| Steps | What it asked for |
|---|---|
| 1-3 | Read `cli.py`, `task.py`, `store.py` |
| 4-6 | Write all three, in dependency order |
| 7 | A test command |
| 8-9 | `rm -f ~/.taskr.json`, twice |

<div class="caption mt-6">Never said done. Ended because the loop ran out of turns.</div>

<!--
Last week ended on this run. A 9B was asked to add a priority flag to taskr add. It read the right three files. It wrote them in dependency order. Then at step 8 it asked to delete ~/.taskr.json, which is DEFAULT_PATH in store.py, which is the user's task list. At step 9 it asked again.

Two questions. Why did it end? Not for any reason anybody chose. The counter ran out.

What stood between the model and the rm? Nothing. The script answering the calls returned exit 0 without running anything, and that is the only reason this is a slide.
-->

---
layout: two-col
---

## A5: finite limits

Stop, and say what is unresolved

::right::

## A4: one check in code

A no is an answer, not an error

<div class="caption mt-10">Hackathon 1, Thursday. Built around typed actions. Next week: a shell string.</div>

<!--
Every one of you answered both of those questions on Thursday night, for a smaller problem.

A5 is the first question, why a run ends. It said stop after finite limits and tell the user what is unresolved. It said two more things you may have read past. Do not blindly repeat earlier successful changes. And a model call can fail, the Toolkit's occasional 502, and you handle it without losing the conversation. A limit, a cousin of the repeated call, and the endpoint failing: that paragraph already holds three of today's exits. We come back to your own limit at the break.

A4 is the second question, what stands in front of an action. Every write passes one check in your code, never just the prompt. In ask mode the user sees the change and it happens only if they approve. A no leaves Taskr unchanged and goes back to the model as the action's result.

And you all used it. SCENARIO.md, step 4: the first time it asks to make a change, say no. So everyone in this room has already denied an agent once, on purpose, and watched what the model did next.

*[Ask: What did yours do with the no? Take two answers.]*

Three things from Thursday carry into next week unchanged. The check lives in code, where the prompt cannot talk its way past it. A no is an answer, not an error: the model gets it as a result and the run goes on. And every call gets exactly one tool message, refused or not, or the API rejects the conversation.

Three things do not carry. Reads never asked on Thursday. Next week they do, and the second half says why. Bypass mode approved every write without asking. Next week has no bypass, and the rules file in week 6 is what sits between asking about everything and asking about nothing.

And the third is the one today is about. Thursday's changes were typed: move this block to three, mark that task done. The name told you the effect, and you could judge the change from its arguments. Next week the action is run_command, and its one argument is a shell string. The string is the action.

Direction: Do not ask what anyone's limit was. That is the chat break, and asking here spends it.
Good answers to the question: it asked why, it proposed something else, it said the work would
not fit. If someone says their model asked for the same change again, take it and say "hold that,
it has a name in ten minutes": that is the repeated call. If someone says their program crashed on
the no, take that too: that is A4 not met, and next week it costs more.
-->

---
layout: section
---

# Stopping

## The reasons a run ends

<!--
First half. The reasons a run ends.
-->

---
layout: default
---

<div class="label">L06's loop, unchanged</div>

# The done test in six lines

```python {3-4}
while True:
    reply = model.call(messages, tools=TOOLS)
    if not reply.tool_calls:
        return reply.text
    for call in reply.tool_calls:
        result = execute(call)
        messages.append(result)
```

<div class="caption mt-4">Spec 2.4: "Decide what the signal is."</div>

<!--
You have seen these six lines three times. Look at lines three and four. That is a stop condition. The run is done when a reply comes back with no tool call.

It is the default, and it is what L07's system prompt asked for: when the task is done, reply with a short summary and no tool call. The spec asks for more than the default. It says the model signals done in a way you defined, and decide what the signal is.
-->

---
layout: default
---

<div class="label">Spec 2.4, task complete</div>

# Three done signals

<div class="grid grid-cols-3 gap-6 mt-8 items-stretch">
  <div class="card">
    <ph-chat-text-bold class="text-3xl text-blue-600 mb-3" />
    <div class="font-semibold mb-1">No tool call</div>
    <div class="text-sm opacity-70 flex-1">Free. Silent is not finished</div>
  </div>
  <div class="card">
    <ph-flag-checkered-bold class="text-3xl text-blue-600 mb-3" />
    <div class="font-semibold mb-1">A finish tool</div>
    <div class="text-sm opacity-70 flex-1">Done on purpose. ~100 tokens</div>
  </div>
  <div class="card">
    <ph-check-circle-bold class="text-3xl text-amber-600 mb-3" />
    <div class="font-semibold mb-1">Verification</div>
    <div class="text-sm opacity-70 flex-1">Claimed, then checked</div>
  </div>
</div>

<!--
Three designs worth comparing.

No tool call. Free, and every model does it. Its weakness is that the absence of a call is not the presence of a claim.

A finish tool. Give the model finish, with a summary argument, and treat only a call to it as done. Now done is something the model says on purpose. It costs one more tool definition, about a hundred tokens on every request, because L07 measured three tools at four hundred. And small models sometimes call it early.

Verification. The model claims done and the harness checks: it runs the tests before it accepts the claim. That is L07's second fix, the one that turns a claim into an observation.

Direction: Keep moving. The next slide is where the first card fails.
-->

---
layout: two-col
---

## `finish_reason: "length"`

Cut off, not finished

::right::

## A question back

Nobody there to answer

<div class="caption mt-10">No tool call, and not done. The log needs a name for both.</div>

<!--
Two replies with no tool call that are not done.

Left: finish_reason length. L07 gave you an obligation for each finish reason, and length means the reply was cut off. Treat it as done and you accept half a sentence as the answer.

Right: a reply that asks a question. "Should I also update the web front end?" On Thursday there was a user, and a question was the conversation working. The week-7 gate runs with nobody at the keyboard. So your design has to say what a question means: done, a separate needs-input exit, or a failure. Any of the three is defensible. Leaving it undecided is not, because then your log calls it done.
-->

---
layout: default
---

<div class="label">Captured this morning · L07's task, tools real</div>

# Four runs, four dones

| Run | Steps | Exit | `taskr add x --priority high` |
|---:|---:|---|---|
| 1 | 10 | done | `TypeError` |
| 2 | 10 | done | Rejected: priority is an int |
| 3 | 15 | done | Works |
| 4 | 6 | done | `TypeError` |

<!--
This morning the same task ran four times through a loop with real tools and all six stop conditions. Same model, same tree as L07. Every run ended on its own signal. No limit fired once.

Then I ran the feature. One of four works. Runs 1 and 4 read store.py and never changed it, so the add command now calls store.add with an argument it does not take, and plain taskr add is broken too. Run 2 made priority an integer, so high is rejected.

Four dones. One working feature. By the six lines, four successes.

Direction: The captures and a README are in assets/live/captures. If asked: the check was
`python -m taskr --file /tmp/x.json add x --priority high` on each run's diff.
-->

---
layout: default
---

<div class="label">Run 1, steps 6 to 8</div>

# The test that ran nothing

```text
$ python -m taskr.cli add "test" --priority high
exit 0

$ python -m taskr add "test" --priority high
TypeError: Store.add() takes from 2 to 3 positional arguments but 4 were given
```

<div class="caption mt-4">A check the model chose is not a check.</div>

<!--
Run 1 did test. Look at its test.

python -m taskr.cli. That imports cli.py and runs nothing, because cli.py has no main guard. Exit zero from a program that did nothing. The model ran it three times, saw three zeros, and said done.

The second command is the one a user would type. TypeError.

That is the argument for verification, and it is also its limit. The harness can only confirm done with a check it trusts, and a check the model chose is not one. pytest on a suite you wrote before the run is. Whatever the model decides to run as its test is evidence of what it believes, not of what works.

*[Pause.]*
-->

---
layout: statement
---

A run that ends on a limit *has not finished*.

<!--
The other half of the rule.

L07's run did not finish. It ran out. If its log said "stopped", the log was hiding the most important fact about the run. A run that ends on a limit ended because a number was reached, and the work is in whatever state step N left it in. That is a different outcome from done, and it needs a different name.

There are five of them.
-->

---
layout: default
---

<div class="label">Spec 2.4</div>

# Six stop conditions

| Condition | Catches |
|---|---|
| Task complete | The model signals done |
| Step limit | The obvious runaway |
| Token budget | A growing context |
| Wall clock | A hung command |
| Repeated call | The same call forever |
| Consecutive errors | A run that has lost the plot |

<!--
This is the spec's list, section 2.4, and it is your checklist for Lab03. The spec says you need all six, and each one needs a distinct exit reason in the run log.

Read it as one plus five. The first row is the one we just spent ten minutes on. Task complete is the exit you want: the run ends because the work is done, in a way you defined. The other five are limits. Each one ends the run because a number was reached, and a run that ends on a limit has not finished. So when I say six stop conditions, I mean done, plus five limits.

Now read the right-hand column as a chain. The step limit is the obvious one: it catches the runaway. The spec justifies the next two by what the ones above them miss. The token budget exists because the step limit does not catch a loop whose context is growing. The wall clock exists because neither of those catches a hung command. The last two are about the model's behaviour rather than the run's size: the same call forever, which is the most common way a small model gets stuck, and a string of errors it is not recovering from.

Two things hold for all five. Each gets its own name in the log, because "stopped" will tell you nothing when you read the log next week. And each has a number you choose. The spec does not choose it for you.

The next five slides take them one at a time. For each: the run the others let through, and the one decision inside it you have to write down.

Direction: Do not explain the rows here; the next five slides do. This slide is for the
one-plus-five split and the chain in the right column. If asked what the numbers should be:
there is no right answer. The four rehearsals used 20 steps, 16000 tokens, 600 seconds, 3
repeats and 3 errors, and never hit one of them.
-->

---
layout: default
---

<div class="label">Condition 2</div>

# Step limit

- The backstop for the other five
- The bluntest: L07's nine
- **Your call:** requests, or tool calls?

<!--
The step limit catches the obvious runaway: the model keeps asking and nothing else ends it. It is the cheapest check and the backstop for all the others.

It is also the bluntest. L07's run ended on one, after the damage and before the work. Nobody chose nine.

One decision inside it: what counts as a step. A request to the model, or a tool call? One reply can carry three parallel calls, so the two counts drift apart. Either is fine. Write down which, because your threshold means something different under each.
-->

---
layout: default
---

<div class="label">Condition 3</div>

# Token budget

- L07: 471 to 3252 tokens in nine steps
- One large read: +10,000 in one step
- Checked before the request goes out
- **Your call:** next request, or run total?

<!--
The step limit does not catch a loop whose context is growing. L07's prompt went from 471 tokens to 3252 in nine steps, sevenfold. Nine steps of that is harmless. One read_file of a large file, or a run_command whose output is a full test log, adds ten thousand in one step, and the step limit does not notice.

Check it before the request goes out: the last reply's prompt tokens, plus its completion tokens, plus an estimate for what you have appended since. usage is the ground truth from L07, so every check after the first is anchored on a real number.

Two numbers go by this name, so pick one. The size of the next request protects the context window, which is what 2.4 means. The total across the run protects your wallet. On Thursday's Toolkit key that was real money: the hackathon README said the way to spend all twenty-five dollars is a model loop with no step limit. On a local model, it is time.

v0 has no compaction. When the size check fires, the run ends. It does not summarize and carry on.
-->

---
layout: default
---

<div class="label">Condition 4</div>

# Wall clock

- `flask run`, a watcher, `git commit`'s editor
- No request, so no step, no tokens
- Per-command timeout, plus a run budget
- Standard input closed

<!--
Neither of those catches a hung command. The model runs something that never exits. No new request goes out, so no step is counted and no token is spent.

The candidates are ordinary. A test runner in watch mode. git commit opening an editor. A command waiting on standard input. And in a repository with a Flask front end, which aider-practice has from lessons 11 to 16, flask run, which a model testing its web change will start and which never returns.

A run-level clock checked between steps cannot interrupt any of those, because the loop is stuck inside execute. So wall clock is two mechanisms: a timeout on every command and every model request, and a budget for the run as a whole. Close standard input on every command, and the stdin case becomes an immediate error instead of a hang.

One caveat, because it is on the slide. Closing standard input fixes programs that read standard input. It does not fix an editor. git commit with no message opens one, and an editor can talk to the terminal directly instead of reading standard input, so it can still sit there waiting. For that case the per-command timeout is what ends it, or you set GIT_EDITOR=true in the command's environment so git never opens an editor at all.
-->

---
layout: default
---

<div class="label">Condition 5</div>

# Repeated identical call

- Identical: tool name plus parsed arguments
- A repeat after a write is progress
- Exact match misses L07's steps 8 and 9

<!--
The most common small-model failure: the same call, forever. It reads a file, does not act on it, and reads it again.

"Identical" needs a definition. Compare the tool name and the parsed arguments with the keys sorted, not the raw arguments string, where whitespace differs.

Then decide whether a repeat is always a loop. Running pytest again after a fix is the work going well. Running it again with nothing written in between is the loop. Key on the call and its result, or reset the count on any write, and you can tell them apart.

And notice what exact matching misses. L07's steps 8 and 9 both deleted the task list, and they are not identical: one ends in python -c, the other in python cli.py add.
-->

---
layout: default
---

<div class="label">Condition 6</div>

# Consecutive tool errors

- Consecutive: any success resets it
- Could not run: an error
- Ran and exited 1: **your call**

<!--
The model has lost the plot and is not recovering. Errors are results, spec 2.1, so the model is told every time, and a few in a row can be the model correcting itself. Many in a row is not. The count is consecutive, reset by any success.

What counts as an error is the decision. A tool that could not do what was asked is one: no such file, a command killed by its timeout, arguments that were not valid JSON.

A command that ran and exited non-zero is less clear. pytest exiting 1 is information. Count it as an error and you stop a run in the middle of fixing a test.

The second half adds one more case: whether a denial counts.
-->

---
layout: default
---

<div class="label">L07's run, checked against all six</div>

# The six against L07's run

| Condition | On L07's run |
|---|---|
| Done | Never |
| Step limit | Fired, at nine |
| Token budget | Only if under 3168 |
| Wall clock | Nothing ran |
| Repeated call | Never: 8 and 9 differ |
| Consecutive errors | Never: all "succeeded" |

<!--
Put all six against L07's run.

Done never fired: no reply was a plain answer. The step limit fired, at a number nobody chose. A token budget stops it before the rm only if it is set under 3168, a number set by file sizes. Wall clock: nothing hung, because nothing ran. Repeated call: never, 8 and 9 differ. Errors: never, every stub reported success.

Two of the six cannot fire on this run at all. The two that can stop it before step 8 do so by accident: a step limit of seven, or a token budget under 3168, lands before the rm because the rm happened to come late in a short task. The same numbers stop a bigger task in the middle of its reads.

Not one of the six looks at what a call does. Hold that for the second half.
-->

---
layout: default
---

<div class="label">Placement</div>

# Where each check sits

```python
while True:
    # before the request: step limit, token budget, wall clock
    reply = model.call(messages, tools=TOOLS)
    # after the reply: done, truncated
    for call in reply.tool_calls:
        # before executing: repeated call
        result = execute(call)
        # after the result: consecutive errors
```

<div class="caption mt-4">A sketch, not the build.</div>

<!--
The checks go in three places, and the place follows from what each one needs to see.

The first three refuse to spend another request, so they go before the call. Done needs a reply to judge. Repeated call has to fire before the call executes, or the third identical write happens anyway. Errors need the result.

This is a sketch, not the build. What you write in Lab03 also carries the approval prompt, the run log, and the append L07 said everyone forgets.
-->

---
layout: default
---

<div class="label">The exit path</div>

# One way out

- One exception, one handler, one log line
- Six is the minimum
- `truncated`, `endpoint_error`
- A crash has no exit line

<!--
Every exit goes through one place. The demo agent raises one exception type carrying the reason, and one handler writes the exit line and prints the summary. The alternative is a break in five places and a return in a sixth, and sooner or later one of them forgets to log. A run whose log ends without an exit line is the one you will most want to understand.

Six is the minimum, not the list. The demo agent has two more, because things happen that the spec does not name and the log still needs a word for them. truncated is the length case. endpoint_error is the POST itself failing: a dead server, a stream that dies part way, which is F1, or the Toolkit's occasional 502 from Thursday.

A crash is not an exit reason. It is a run with no exit line.
-->

---
layout: default
---

<div class="label">Spec 2.5, the run log</div>

# The exit line

```json
{"event": "exit", "reason": "done", "steps": 10,
 "working_seconds": 59, "waiting_seconds": 0}
```

<div class="caption mt-4">Teardown question 4: "Which one fires most, and what does that tell you?"</div>

<!--
That is run 1's last line. The spec lists what a run records: the task, every step, every call and its approval decision, tokens in and out, time, and the exit reason.

The exit line is the one the week-7 teardown counts. Question 4 is on the slide. You can only answer it from names you recorded.

The exit is also a message to a person. A5 said tell the user what is unresolved. Unattended, the person reads it afterwards, so the exit should say what the run was doing when it stopped, not only why.

And the names are reference points in the sense L06 meant. token_budget in your code, your design document and your teardown is the same word in three places, and anyone, including a model you hand the log to, can point at it.
-->

---
layout: default
---

<div class="label">Five minutes with a neighbor</div>

# The Hackathon 1 limit

Thursday, A5: your loop had to stop after finite limits.

`counted: <what>, limit: <number>, fired: yes | no | don't know`

<div class="caption mt-6">Then: which of the six is it, and one run it would not have stopped?</div>

<!--
Five minutes with your neighbour.

On Thursday your assist loop had to stop after finite limits. Think about the limit in your own code. One line on paper, in this shape: what it counted, the number, and whether it ever fired, yes, no, or don't know.

Then be ready to say which of today's six it is, and one run it would not have stopped.

"OK, Zoom, we're on break."

[Circulate. Five minutes.]

"OK, Zoom, we're back."

[Tally by show of hands on the board. Column one, what was counted: model calls, tool calls, loop turns, tokens, time, something else, nothing. Column two: how many said don't know.]

Direction: Expect model calls or loop turns to dominate. Do not grade the answers. The
next slide reads the tally back.
-->

---
layout: section
---

# Approval

## The check in front of an action

<!--
Second half. The check in front of an action.
-->

---
layout: default
---

<div class="label">The board, read back</div>

# The tally, against the six

- Most counted one thing: the step limit
- Every "don't know": no exit line
- None of the six judges an action

<!--
Read the board.

Most of you counted one thing, and it was model calls or loop turns. That is the step limit, one of six. It was right for Thursday: a user was watching, the run was short, and the step limit is the backstop. It is not enough for a run nobody watches.

Every "don't know" is the argument from before the break. If your loop stopped and you cannot say whether the limit fired, your loop did not record why it ended.

Then the harder point. Every condition in the first half is about the run: how long, how big, how repetitive. None of them looks at what a call does.
-->

---
layout: statement
---

Stop conditions end runs. They do not *judge actions*.

<!--
Stop conditions end runs. They do not judge actions.

L07's step 8 would not be stopped by any of them on purpose. For that you need the second thing you built on Thursday.
-->

---
layout: default
---

<div class="label">Apply's safety net</div>

# What `/undo` walks back

| The call | `/undo` |
|---|---|
| `write_file taskr/cli.py` | Walks it back |
| `rm -f ~/.taskr.json` | Nothing: never tracked |
| `git reset --hard` | Nothing: git was the net |
| `pip install ...` | Nothing: not your repo |
| `curl ... \| sh` | Nothing: someone else's program |

<!--
Apply's safety net was a commit per edit and /undo. It was enough, because the only thing Aider changed was files in your repository, and git tracks those.

First row: a write to a tracked file. Undo walks it back. That is what it is for.

Everything else. rm on a file in your home directory: git never knew about it. git reset --hard or git clean: it destroys the uncommitted work git was protecting. pip install: it changed your Python, not your repo. curl piped to sh: it ran someone else's program as you.

The design document's rule is one sentence. Approvals ship with the tools, in the same week, because git does not cover bash. Your Stage 1 file protections stay. They confine write_file to the repository. They do nothing for a shell string.
-->

---
layout: two-col
---

## Thursday

```text
add_task(title, due)
```

The name is the effect

::right::

## Next week

```text
run_command(command)
```

The argument is a program

<div class="caption mt-10">The same check, a different argument.</div>

<!--
On Thursday the permission check sat in front of typed actions. The model asked for something like add_task with a title and a date. The name told you the effect, and the arguments were data. Showing the user the change was easy, because the change was the arguments.

run_command has one argument, and it is a program. The name tells you nothing about the effect. The same check, in the same place in the loop, now has to show a person something they can judge, and the person has to be able to judge it from what is shown.
-->

---
layout: default
---

<div class="label">L07's four parts, plus one</div>

# The approval step in the harness

1. Parse the arguments
2. Boundary checks in code
3. The person: allow or deny
4. Dispatch, or the denial as the result

<div class="caption mt-6">Code refuses what nobody should be asked about.</div>

<!--
L07 split an action into four parts: the description, written for the model; the argument contract, code that checks what it asked for; the dispatch, code that does it; and the observation, the next message. The approval prompt goes between the contract and the dispatch.

In order. Parse the arguments: invalid JSON is an error result and nobody is asked about it. Boundary checks in code: a path outside the repository is refused without asking. Then the person. Then dispatch, or the denial, as the call's result.

The spec calls this part ten lines. It is. The decisions inside the ten lines are the lecture.
-->

---
layout: default
---

<div class="label">Inside the ten lines</div>

# Four approval decisions

<div class="grid grid-cols-2 gap-6 mt-6 items-stretch">
  <div class="card">
    <div class="font-semibold mb-1">What to show</div>
    <div class="text-sm opacity-70">The whole call. A diff, not a byte count</div>
  </div>
  <div class="card">
    <div class="font-semibold mb-1">What a denial returns</div>
    <div class="text-sm opacity-70">A tool message, with the reason</div>
  </div>
  <div class="card">
    <div class="font-semibold mb-1">Whether reads ask</div>
    <div class="text-sm opacity-70">This week, yes</div>
  </div>
  <div class="card">
    <div class="font-semibold mb-1">Waiting and the clock</div>
    <div class="text-sm opacity-70">Record it, do not count it</div>
  </div>
</div>

<!--
Four decisions.

What to show. The whole call. The full command, never truncated, never paraphrased. For write_file, a diff against the file on disk, not a byte count. L07's stub answered with a byte count, and nobody can approve a byte count. Never the model's own summary of what the call does. In ten minutes you will see why.

What a denial returns. A tool message for that call's id, with the person's reason. Not an exception, and not a skipped message. Every tool call gets exactly one tool message, even a refused one: that is Thursday's REFERENCE.md. Then the model decides what to do, knowing it was told no.

Whether reads ask. On Thursday they never did. The spec says every call stops, reads included, and there is a reason beyond caution. A read_file puts the file into the next request. On a hosted endpoint, the file leaves your machine, and a .env inside the repository passes the boundary check. Next week's rules will auto-approve most reads. This week they ask.

Waiting and the clock. Someone who takes ten minutes to answer should not fire wall_clock. Count model and tool time against the limit, and record waiting time separately. How much of the run was you is exactly what next week is trying to shrink.

One more from the first half: does a denial count as a tool error? If it does, three denials end the run. That may be what you want. Write it down either way.
-->

---
layout: default
---

<div class="label">Live · L07's task, tools real</div>

# The approval prompt, live

- Three reads: `y`, `y`, `y`
- A write: read the diff
- Out of the repo, or the task list: **no**
- The exit line, then one real `add`

<div class="caption mt-6">Scratch copy of taskr. Fake home. Three tasks in ~/.taskr.json.</div>

<!--
Same task as L07, same model. The tools are real this time, in a scratch copy of taskr, with a fake home directory holding a task list of three tasks. Every call stops at a prompt, and I answer.

Four things to watch. The first three prompts are reads, and they are y, y, y. That is where fatigue starts. The write shows a diff, and I will read a line of it. Anything that leaves the repository, or runs taskr add against the default path, gets a no with a reason, and then we watch what the model does with the no. And at the end, the exit line, and one real taskr add to see whether done meant done.

Direction: Runbook section 2. `python3 assets/live/agent.py`. Read one diff line out loud.
Deny any `run_command` that runs `taskr add` without `--file`, leaves the repo, or uses `rm`;
type the reason. If the model does nothing notable, say so and go back to "Four runs, four
dones", which is what four rehearsals did.
-->

---
layout: default
---

<div class="label">Spec 2.2, and week 10</div>

# The model's stated reason

- "Clean up the test state"
- "Verify the change"
- v0 trusts it. Week 10 attacks that

<div class="caption mt-6">Approve the command. Never the explanation.</div>

<!--
A model will tell you why it wants to run a command, in its reply text, or in an argument you gave it room for. Clean up the test state. Verify the change.

v0's approval layer trusts whatever the model says a command is for. The course design names that as the specific weakness week 10 attacks.

Approve the command. Never the explanation.
-->

---
layout: default
---

<div class="label">Runs 2 and 3, approved</div>

# A test with a side effect

```text
python -c "from taskr.cli import main;
           main(['add', 'test task', '--priority', 'high'])"
```

- Runs the real `add`
- Saves to `DEFAULT_PATH`: `~/.taskr.json`
- Two junk tasks per run. `/undo`: nothing

<!--
Some commands are not dangerous to read and are dangerous to run.

This is how runs 2 and 3 tested their change. It looks like a test, and it is one. It also runs the real add, which saves to DEFAULT_PATH, which is the user's task list. Both runs left two junk tasks in it.

The rehearsal approved every one of those commands, because nothing in their text mentions a home directory. Would you have caught it at step 13 of a run?
-->

---
layout: default
---

<div class="label">Step 11, then step 12</div>

# Commands that point at files

```text
step 11  write_file   tests/conftest.py
step 12  run_command  pytest
```

- `pytest` runs every `conftest.py`
- Same for `make`, `npm test`

<div class="caption mt-4">You approve a command in a state.</div>

<!--
pytest runs every conftest.py and test file in the repository. If step 11 wrote conftest.py, approving pytest at step 12 is approving whatever that file says. make and npm test are the same: the command is a pointer to a file, and the model may have just written the file.

So the unit you approve is not a command. It is a command in a state: what the command is, plus everything written since you last read the repository. The prompt shows the first. Only you hold the second.
-->

---
layout: default
---

<div class="label">What v0 does not do</div>

# Approval fatigue

- Step 30: a keypress, not a decision
- No defense in v0, by design
- Also missing: a sandbox

<!--
Count the y's from the demo. By step 30 of a real session, the prompt is a keypress, not a decision.

v0 has no defense against that, and the design says so. It is on the list of what v0 does not do, next to the missing sandbox and a rule that was safe for one task and not the next. That list is the syllabus for Create.
-->

---
layout: default
---

<div class="label">Week 6</div>

# Rules, after a week of watching

- Matched against the requested call
- Deny wins over allow
- Unmatched: a person decides
- **This week:** note what you approve

<!--
Next week a rules file goes in front of the prompt. Rules match the requested call, deny wins over allow, and anything unmatched falls through to a person.

Why wait a week? Build the manual path first and live with it before writing a single rule. After a week of answering your own agent, you know what it asks for. So keep a note this week of what you approved and denied. That list is your first rules file.

The week-7 gate runs with nobody there, and it measures the tension in both directions. Rules too tight and the run stalls waiting for a person who is not coming. Too loose and you find out the other way. And teardown question 5 asks for the most alarming thing your agent ever asked to do. Start collecting.
-->

---
layout: default
---

<div class="label">Dates</div>

# This week and next

| When | What |
|---|---|
| This week | Lab02, Hackathon 1.5 · L10 Thursday |
| Mon Oct 5 / Tue Oct 6 | Lab03: build the agent |
| Tue Oct 6, 11:59 PM | Apply build due |
| Tue Oct 6 | Analyze spec handed out |

<!--
This week: Lab02 is the Hackathon 1 post-mortem and starts Hackathon 1.5. Thursday is L10.

Lab03, October 5 and 6, you build the agent: tools, the loop, the stop conditions, the manual prompt. You leave having denied something your own agent asked to do.

Tuesday October 6 the Apply build is due at 11:59 PM, and the Analyze spec is handed out the same day. Today was its sections 2.2 to 2.5.
-->

---
layout: default
---

<div class="label">Take these with you</div>

# Three questions

1. `pytest` exits 1 three times. Which exit?
2. A ten-minute call at step 12. The log?
3. You approved `pytest`. What did you approve?

<!--
Three to take with you.

pytest exits 1 three times in a row while the model fixes a test. Which of your exits fires, and should it?

Your wall clock is 300 seconds, and you took a ten-minute phone call at step 12. What does your log say?

You approved pytest at step 12. What did you approve?

Direction: Do not answer them.
-->

---
layout: default
---

<div class="label">Coming up · L10</div>

# The endpoint behind the clock

- Four rehearsals: 31 to 60 seconds
- Nearly all of it the model
- Thursday: serving a local model

<!--
The four rehearsal runs took 31 to 60 seconds of model and tool time, and nearly all of it was the model. A wall-clock limit is a number of seconds, but what spends them is the endpoint: how many tokens per second your machine produces, and how many of them the model spends reasoning before it answers.

Thursday is that endpoint, the thing behind the base_url line in your config.
-->

---
layout: end
---

<!--
End slide. Questions.

Direction: if nobody has one, the three questions are on the previous slides. Offer Ed.
-->
