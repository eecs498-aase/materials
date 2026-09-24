---
theme: ../theme
title: "L07: Inside the Call: Messages, Streams, and Tool Calls"
info: |
  EECS 498 AASE — Lecture 07
  Applied Agentic Software Engineering, UMich Fall 2026
layout: title
class: text-left
transition: fade
mdc: true
highlighter: shiki
---

# Inside the call: messages, streams, and tool calls

## Lecture 07 · Sep 22, 2026

<!--
Good afternoon. Analyze starts today.

Direction: Every number and JSON fragment today was captured from qwen3.5:9b through Ollama
on 21 and 22 September and is in assets/wire-captures/. Four live moments, all in
assets/demo-runbook.md. Every output is also on the glass, so a dead network costs
the theatre and none of the content. Warm the model before the room fills.
-->

---
layout: default
---

<div class="label">Today</div>

# Three parts

1. One POST, one reply
2. The stream
3. Tools, and the loop on the wire

<div class="caption mt-6">Analyze begins here. Nothing is handed out for three weeks.</div>

<!--
Three parts. One POST and the reply that comes back. Then the stream, because every reply in your build arrives in pieces. Then tools, and the loop from Thursday, run for real.

Before anything else: nothing about Analyze is due, and nothing is handed out, until October 6. Today is lectures only. Your build is still the build.

Direction: Name them and move. The last paragraph is a promise L06 made and it gets kept in
every lecture until it is true.
-->

---
layout: default
---

<div class="label">Lab01, three weeks ago</div>

# The card we never opened

<div class="grid grid-cols-3 gap-6 mt-8 items-stretch">
  <div class="card">
    <ph-stack-bold class="text-3xl text-blue-600 mb-3" />
    <div class="font-semibold mb-1">Assemble</div>
    <div class="text-sm opacity-70 flex-1">L02, L03, the repo map</div>
  </div>
  <div class="card">
    <ph-chat-text-bold class="text-3xl text-amber-600 mb-3" />
    <div class="font-semibold mb-1">Answer</div>
    <div class="text-sm opacity-70 flex-1">A line of configuration</div>
  </div>
  <div class="card">
    <ph-pencil-simple-bold class="text-3xl text-blue-600 mb-3" />
    <div class="font-semibold mb-1">Apply</div>
    <div class="text-sm opacity-70 flex-1">F5, F6, the diff, the commit</div>
  </div>
</div>

<div class="caption mt-6">Three weeks on the blue cards. Today the amber one.</div>

<!--
Three weeks ago in lab you drew this. A harness assembles, the model answers, the harness applies.

Look at where this course has been. L02 and L03 were the first card: what goes in front of the model. The repo map, the token budget, who chose each part of the prompt. F5 and F6 are the third card: the parser, the diff, the approval, the commit.

The middle one has been a line in a YAML file. Three weeks, and nobody in this room has called a model from code they wrote.

Direction: This slide is a receipt, not a lesson. Do not re-teach the harness. The YAML line
is `model: ollama_chat/qwen3.5:4b` if anyone asks.
-->

---
layout: default
---

<div class="label">Why now</div>

# Three dates, one call

| When | What it needs |
|---|---|
| This week | You write the client. `ENDPOINT.md`, F1 |
| Thursday evening | An AI capability in `taskr`, two hours |
| Week 5 | The same call, with tools, unattended |

<!--
Three things need it open now, and they are one, three and fourteen days away.

This week you write the client. `ENDPOINT.md` is the contract and F1 grades what your program does when a reply fails part way through.

Thursday evening you have two hours to build an AI capability into `taskr`. The program you built across sixteen lessons. Whatever you write that evening, it sends the object I am about to put on the screen.

And in week 5 that same call grows one more field, and a loop runs it without you in the room.

That is why today is bytes and not concepts.
-->

---
layout: section
---

# One POST

## The request, field by field

<!--
Section divider. The first half is ENDPOINT.md read in the order the bytes go by,
which is their build this week.

Direction: do not stop here. Go straight to the request object.
-->
---
layout: default
---

<div class="label">ENDPOINT.md</div>

# The request object

```json
POST {base_url}/chat/completions

{
  "model": "qwen3.5:9b",
  "messages": [
    {"role": "system",    "content": "..."},
    {"role": "user",      "content": "..."},
    {"role": "assistant", "content": "..."},
    {"role": "user",      "content": "..."}
  ],
  "stream": true
}
```

<div class="caption mt-4">This is the entire interface between your program and the model.</div>

<!--
This is it. One HTTP POST, one JSON object. This is the entire interface between everything you have built and the model.

`model` is the identifier the server knows, sent unchanged. That `ollama_chat/` prefix you have been typing into Aider's config is Aider's routing, not the model's name, and your specification says so in the configuration section.

`messages` is the stack from Lab01, encoded as a list. Your system prompt is entry one. Your selected files, F3, are inside a message, because look at the object: there is no field for files. There is nowhere else to put them. The history is every earlier complete turn. Your newest message is last.

One thing not on the slide. `Authorization: Bearer`, and only when `api_key` is set. No key means no header at all, not an empty one, because Ollama rejects an empty one. And that key never appears in an error message, a log line, or a commit.

[Pause.] Now look at what is not in this object. Something you have been told twice is missing from here. What?

Direction: Pause on the last line and let the room answer before advancing. They have been
told twice that nothing is remembered.
-->

---
layout: statement
---

There is **no session field**. There is nowhere to *put* a memory.

<!--
There is no session. No conversation id, no cookie, no handle to last turn.

Lab01 told you nothing is remembered and continuity is the harness re-sending. This is why. It is not a policy decision somebody made. The request has nowhere to put a memory.

Everything the model knows about the last ten turns is in that list because you put it there. That is the whole reason F1 has a budget rule: the list only grows. When your program trims old turns or replaces them with a summary, it is editing this list before it sends it, and nothing on the other end notices or cares.

Direction: This is the slide to pause on.
-->

---
layout: default
---

<div class="label">ENDPOINT.md, graded</div>

# The URL rule

| Configured `base_url` | Where the request goes |
|---|---|
| `http://localhost:11434/v1` | `…:11434/v1/chat/completions` |
| `http://localhost:11434/v1/` | `…:11434/v1/chat/completions` |
| `https://api.example.edu` | `…example.edu/chat/completions` |

<div class="caption mt-6">Strip one trailing slash, append the path. Never invent a <code>/v1</code>.</div>

<!--
Take `base_url`, strip one trailing slash, append `/chat/completions`. Nothing else. Do not insert a `/v1` your configuration did not give you.

This looks like string handling and it is a design requirement. The rule in this course is that the model is an endpoint, not a vendor. A program you can repoint by editing one line of YAML has that property. A program that guesses at the path does not, and staff will run yours against an endpoint you have never seen.
-->

---
layout: default
---

<div class="label">Not in the minimum</div>

# Three more request fields

- `temperature` — L02's sampling step, as a dial
- `max_tokens` — a cap, and a test's best friend
- `tools` — the second half of today

<div class="caption mt-6">Omit <code>temperature</code> and the server picks. It does not pick zero.</div>

<!--
The object you just saw is the minimum. Three more fields, and none of them has come up in a lecture yet.

`temperature` is L02's sampling step with a dial on it. L02 said the model computes a distribution over the whole vocabulary and samples from it. This number scales that distribution before the sample. Near zero, the most likely token wins nearly every time. Higher, and the tail gets picked more often.

If you do not send it, the server picks a default, and the default is not zero. In week 7 your eval harness will want temperature zero where it can get it, so that three runs of one task differ because of the task rather than the dice. Even at zero they will not be identical on every server.

Stage 1 does not require you to send it. Your design document should say whether you do.

`max_tokens` caps the reply. It is a cheap way to make a test deterministic, and in two slides it is how I break something on purpose.

`tools` is the second half of today.
-->

---
layout: default
---

<div class="label">Compatibility</div>

# What "compatible" promises

- Ollama, llama.cpp, vLLM, every vendor: same object
- Nobody ratified it. One vendor's API won
- It frays at reasoning, at tools, at `usage`

<div class="caption mt-6"><code>ENDPOINT.md</code> draws the line: text chat completions, nothing more.</div>

<!--
One paragraph on why this works at all.

Ollama takes this object. So does llama.cpp's server, and vLLM, and every commercial vendor. Nobody ratified that. One vendor's HTTP API became the shape everybody copied, and the shape is now worth more than the vendor. That is why L01 could tell you the model is a line of configuration and mean it.

It frays at the edges and you will meet every edge today. Where a model's reasoning arrives differs by server. Whether a tool call arrives whole or in fragments differs by server. Whether usage shows up on a stream depends on a field one server invented and the others copied.

`ENDPOINT.md` draws the line: text chat completions and nothing more. Past that line you need a proxy in front of the service, not a change to your code.
-->

---
layout: section
---

# One reply, three endings

## What comes back, and what it obligates

<!--
Section divider. What comes back, and what each ending obligates.

Direction: the first live moment is on the next slide. Runbook command 1.
-->
---
layout: default
---

<div class="label">Live · stream false</div>

# The reply envelope

```json
{
  "choices": [{
    "message": {
      "role": "assistant",
      "content": "HTTP status 404 means the requested resource could not be found on the server.",
      "reasoning": "Thinking Process:\n\n1.  **Analyze the Request:** ..."
    },
    "finish_reason": "stop"
  }],
  "usage": {"prompt_tokens": 31, "completion_tokens": 465, "total_tokens": 496}
}
```

<div class="caption mt-4">Run it live. One short question, one short answer.</div>

<!--
Let us run one. System prompt says answer in one short sentence. Question: what does HTTP 404 mean. Streaming off, so the whole thing comes back at once.

[Run command 1.]

There it is. `choices` is a list, because the protocol lets you ask for several replies at once. You never will, and `choices[0]` is the one thing every client on the planet has hard-coded.

`message` is a role and a content. That is the shape.

Two other fields are the rest of this section. And hold on to that 465.

Direction: LIVE 1, runbook command 1. The completion count moves run to run. Anything over
about 200 carries the point; under 50 means the model is not reasoning, so say the
captured number is from yesterday and move on.
-->

---
layout: default
---

<div class="label">Every reply ends for a reason</div>

# Three finish reasons

| Value | Your program's obligation |
|---|---|
| `stop` | The model ended it. F5 may look for edit blocks |
| `length` | Cut off. An explicit error, never an edit |
| `tool_calls` | It is asking. Second half |

<div class="caption mt-6">Information for your code, not for the user.</div>

<!--
Every reply ends for a reason and the reason is a field. Three values you will see, and read the second column: each one is an obligation on your program, not a status line for your user.

`stop` means the model ended its own reply. That is the only value under which F5 is allowed to go looking for edit blocks.

`length` means it got cut off.

`tool_calls` means it is asking you for something. Second half.
-->

---
layout: default
---

<div class="label">Live · max_tokens 8</div>

# A truncated reply

```json
"message": {
  "role": "assistant",
  "content": "",
  "reasoning": "Here's a thinking process that leads to"
},
"finish_reason": "length"
```

<div class="caption mt-4">Empty content. The model did not say nothing.</div>

<!--
Same request, `max_tokens` set to eight.

[Run command 2.]

Content is an empty string. The reasoning field is eight tokens long. The model did not say nothing; the server cut it off mid-thought.

A program that reads `content`, sees empty, and tells the user the model had no answer has misread this reply.

Now imagine the cut happens at four hundred tokens instead of eight. The text looks finished. It may contain what looks like a complete edit block, because a closing marker is short and the model may well have got there. A program that applies it has done something much worse than print the wrong message.

`ENDPOINT.md` says truncation produces an explicit application error. This field is how you know. Same for content filtering, a malformed event, an HTTP failure, and a stream that ends without finishing.

Direction: LIVE 2, runbook command 2. This one is reliable.
-->

---
layout: default
---

<div class="label">usage</div>

# The number your estimator is graded against

```text
"usage": {"prompt_tokens": 31, "completion_tokens": 465, "total_tokens": 496}
```

- `/tokens` predicts. This field counted
- Send once, compare, calibrate. One afternoon

<div class="caption mt-6">F1 lets the estimate be crude. It does not let it be uncalibrated.</div>

<!--
The server counted for you. Thirty-one tokens in, 465 out.

Your `/tokens` command shows an estimate, and F1 lets that estimate be crude. A fixed characters-per-token ratio is fine as long as it is deterministic.

This field is the ground truth that estimate gets measured against. Send one request, compare `prompt_tokens` to what `/tokens` predicted, adjust your ratio. That is the entire calibration and it is an afternoon's work, not a project.

`ENDPOINT.md` tells you to err on the high side. The reason for that is four slides away.

Measured on this model, 2026-09-22: an empty user message costs 10 prompt tokens. "Hi" costs 11. "Explain TCP in detail." costs 16, and the same sentence twice costs 21. So six of those sixteen are the words and ten are a fixed floor, the chat template's role markers and turn delimiters, added per message before the model sees anything.

That floor is what a characters-per-token estimator cannot see: it counts the string, never the scaffolding, so it undercounts every request and the error grows with the history. Another reason to err high. Keep this in your pocket rather than on the glass; it is the answer to a question someone always asks.
-->

---
layout: default
---

<div class="label">465 billed, 14 seen</div>

# Where reasoning arrives

| Server | Where the thinking lands |
|---|---|
| Ollama `/v1` | A `reasoning` field beside `content` |
| Others | Inside `content`, in `<think>` tags |

<div class="caption mt-6">Three decisions: show it? keep it in history? is a block in it a proposal?</div>

<!--
Now the 465.

The answer you read is fourteen tokens long. You were billed 465. The other 451 are the model thinking, and with `qwen3.5` you get them whether you asked for them or not.

Where they land is one of those edges. Through Ollama's `/v1` endpoint they arrive in a field called `reasoning`, sitting next to `content`. Through other servers, or with other settings, they arrive inside `content` between think tags. `ENDPOINT.md` names both, and it says a delta carrying only reasoning is not a malformed event. You now know why that sentence is in there.

Three decisions fall out, and your design document has to state them. Does the user see it. Does it go into history. And the one `ENDPOINT.md` asks for by name: if an edit block shows up inside the reasoning, is that a proposal?

Think about that last one. The model drafts in there. The captured reasoning for that one-sentence answer had a draft 1, a draft 2 and a draft 3. A parser that reads the whole message will find blocks the model itself threw away.

Direction: The chat break is about the second decision. Do not answer it here.
-->

---
layout: section
---

# The stream

## `stream: true`, which Stage 1 always is

<!--
Section divider. stream: true, which Stage 1 always is.

Direction: runbook command 3 is on the next slide. Let it scroll.
-->
---
layout: default
---

<div class="label">Live · the same question</div>

# A reply as events

```text
data: {"choices":[{"delta":{"role":"assistant","content":"","reasoning":"Thinking"}}]}

data: {"choices":[{"delta":{"content":"","reasoning":" Process"}}]}

...

data: {"choices":[{"delta":{"content":" server"}}]}

data: {"choices":[{"delta":{},"finish_reason":"stop"}]}

data: [DONE]
```

<div class="caption mt-4">516 events for one sentence. Most carried no text at all.</div>

<!--
`ENDPOINT.md` says `stream` is always true in Stage 1, and F1 says the reply prints as chunks arrive. So here is the same question again, streaming.

[Run command 3. Let it scroll.]

What came back is not a JSON object. It is Server-Sent Events: one `data:` line per event, a blank line between them, the same envelope with a `delta` where `message` was.

[Show the count.] Five hundred and sixteen events. For one sentence. Most of them carried a fragment of reasoning and an empty content.

Your reply is the concatenation of every content delta, assembled by you. The model wrote it in order. Nothing tells you the order was complete except the finish reason and the sentinel.

Direction: LIVE 3, runbook command 3. Count in front of them with grep -c. Scroll back to the
top for the opening delta and to the bottom for [DONE].

The opener on the glass carries role, an empty content and reasoning "Thinking".
Say the role is the part that matters and the reasoning fragment is this model
being this model. Do not call it empty; the slide shows it is not.
-->

---
layout: default
---

<div class="label">What your client accepts without complaint</div>

# Six kinds of event

| Event | Carries |
|---|---|
| Opening delta | The `role`. Here, a reasoning fragment too |
| Reasoning-only delta | Thinking. Hundreds of them |
| Content delta | The text the user sees |
| Empty delta | The `finish_reason` |
| Usage-only event | No `choices` at all |
| `[DONE]` | Not JSON. The normal end |

<!--
Six kinds, and your client accepts all of them without complaining. `ENDPOINT.md`'s list of things to accept is this list, and every row on it is a bug somebody has shipped.

The opening delta announces the role. On this capture it also carries the first fragment of reasoning, so it is not empty; on a model that does not reason it would be the role and an empty content. Either way it holds no answer text. Then reasoning-only deltas, in the hundreds. Content deltas, the ones the user sees. An empty delta carrying the finish reason. A usage event with no `choices` in it at all, if you asked for one. And `[DONE]`, which is not JSON, and which is the only thing that tells you the stream ended normally.

That last one catches people. A client that calls `json.loads` on every `data:` line dies on the final one.
-->

---
layout: statement
---

A stream that dies at event 400 has already **printed most of a reply**.

<!--
Now the consequence.

A stream that dies at event four hundred has already printed most of a reply. The text on your screen looks finished. It may well contain a complete edit block.

Direction: The setup for the next slide. Do not resolve it here.
-->

---
layout: default
---

<div class="label">F1, and the reason for each verb</div>

# The failed-stream rule

| Your program | Because |
|---|---|
| Records no assistant turn | The next request would carry a reply it never finished |
| Treats nothing as an edit | F5 and F6 rest on the proposal being complete |
| Says so, stays usable | The user has to be able to retry |

<div class="caption mt-6">The one clause of the contract with a safety consequence.</div>

<!--
So F1 says: record no assistant turn, treat nothing in it as an edit, tell the user, stay usable. `ENDPOINT.md` calls this the one clause of the contract with a safety consequence, and here is why each verb is in there.

No assistant turn, because if that half-finished reply goes into your history, the next request carries text the model never wrote the end of, and the model continues from it. Every request after that one, too.

No edit, because the whole guarantee in F5 and F6 is that nothing gets written without a complete proposal shown in full. You cannot know it was complete.

Stay usable, because the user has to be able to retry.

This is F6.6 from Thursday, met from the other side. On Thursday it was the user hitting Ctrl-C at the approval prompt and nothing being written. Here it is the network, and your program owes exactly the same thing.
-->

---
layout: default
---

<div class="label">Lab00's bin/check had a line about this</div>

# The truncation nobody reports

- Ollama keeps 4k tokens unless told otherwise
- Over that: no error, no `length`, no message
- It drops the **start**. Your system prompt, your first file

<div class="caption mt-6">Raise it to 32k. Your 24000 budget fits with room for the reply.</div>

<!--
One more, and this one has cost students weeks.

Ollama keeps a four thousand token context window unless you tell it otherwise. Send a longer request and it does not return `length`, does not return an error, and does not say a word. It drops the beginning of your prompt and answers the rest.

The beginning of your prompt is your system prompt and your first selected file.

So the model stops using your edit format, because it never saw the instructions. Or it invents a function that is in the part of the file it did not get. And it looks exactly like a stupid model. L02 warned you about that symptom. This is one of its causes, and it is a misconfiguration.

Aider dodges it by sending a field that is not in the standard request, on every single call. Your program sends only the standard request, so the fix is on the server: raise it to 32k. Lab00's `bin/check` had a line about this and now you know what the line was for.

Your `context_budget` of 24000 fits inside 32k with room for the reply. That is why the default is that number, and why `ENDPOINT.md` tells you to err high. Nothing on the wire protects you here. Your configuration and your estimator do.
-->

---
layout: default
---

<div class="label">Five minutes with a neighbor</div>

# The 451 tokens you did not see

That reply billed **465** completion tokens. **14** of them were the sentence.

Your program appends that turn to history and charges it against `context_budget`.

Write one line: `charged: <number>, reasoning: keep | drop`

<div class="caption mt-6">Then be ready to say what your choice costs on the next request.</div>

<!--
Five minutes with your neighbour.

That reply billed 465 completion tokens. Fourteen of them were the sentence you read. Your program has to append that turn to history and charge it against `context_budget`.

One line on paper, in this shape: charged, a number; reasoning, keep or drop. Then be ready to say what your choice costs you on the next request.

"OK, Zoom, we're on break."

[Circulate. Five minutes.]

"OK, Zoom, we're back."

[Take five. Write the numbers on the board.]

They do not agree, and that is the point. Drop it and the model cannot see its own reasoning next turn, which starts to matter on a multi-step task. Keep it and 451 tokens of drafting eat the budget F1 reserves for your files.

Hold that thought, because the next section opens with four hundred tokens that arrive the same way and are not optional.

What the numbers on the board will mean, measured from this capture: the answer
is 78 characters, the reasoning 2311.

  14        the answer only, as the server counted it
  ~20       the same answer as THEIR estimator sees it (chars/4 on 78 chars)
  ~30       answer plus the per-message template floor from the usage slide
  ~40-80    a summary of the reasoning; F1 allows a model-written summary that
            counts toward the budget, so "keep the gist, drop the drafts" has a
            real number behind it
  ~100-150  the tail of the reasoning only. This capture has eight labelled
            sections, from "Analyze the Request" to "Final Polish"; keeping the
            last two and discarding three rejected drafts is a coherent rule
  465       everything, as billed
  ~598      everything, as a chars/4 estimator charges it

Two things to say while writing them up. Almost nobody should write 14, because
14 is read off usage and their own estimator gives about 20. And the last row is
the surprise: on prose, chars/4 overshoots, so the honest "keep" number is
higher than the server's own.

The rows that matter are the summary, the reasoning tail, and 598. Those are the
students who heard a policy question rather than a lookup.

Direction: The answer's shape is on the slide before the clock starts. One line, on paper.
The collection feeds the next section.
-->

---
layout: section
---

# The tool envelope

## The same four parts, on the wire

<!--
Section divider. The same four parts, on the wire.

Direction: the break just ended on 451 optional tokens. This section opens on 400
that are not.
-->
---
layout: default
---

<div class="label">L06: a name, a description, a schema</div>

# The four parts of an action

| Part | Whose |
|---|---|
| Name and description | The model's. What it reads to choose |
| Argument contract | Yours. Code that checks the ask |
| Dispatch | Yours. Code that does it |
| Observation | Yours. The next message in the list |

<div class="caption mt-6">Describing a tool gives the model the ability to ask. Nothing more.</div>

<!--
On Thursday I told you a tool is a name, a description and a parameter schema, that the model replies with a structured request to call one, and that your program executes it and puts the result back.

Split that into four parts, because they live in four different places and only one of them belongs to the model.

The name and description are the part written for the model to read. The argument contract is code you write that checks what it asked for. The dispatch is code you write that does the thing. The observation is the next message in the list.

Be careful with row one. It is the part addressed to the model, not the only part the model sees: the whole definition, schema included, is rendered into the prompt as text, and the next slide measures it. What makes row one the model's is that it is the only part written to persuade a reader. Rows two to four are written to be executed, and the model cannot reach them.

Here is the misconception to kill now. Describing a tool to a model does not give the model the tool. It gives the model the ability to ask. Rows two, three and four are what make the ask do anything at all, and they are where every rule you care about lives.

Direction: This holds whichever envelope they pick. Native and text differ in row one only.
-->

---
layout: default
---

<div class="label">Live · three tools</div>

# A tool definition

```json
{
  "type": "function",
  "function": {
    "name": "read_file",
    "description": "Read a UTF-8 text file from the repository.",
    "parameters": {
      "type": "object",
      "properties": {"path": {"type": "string"}},
      "required": ["path"]
    }
  }
}
```

<div class="caption mt-4">The three the Analyze spec names: <code>read_file</code>, <code>write_file</code>, <code>run_command</code>.</div>

<!--
Live. Three tools, the three the Analyze specification names for week 5. Read a file, write a file, run a command.

And a task: add a `--priority` flag to `taskr`'s `add` command. Every file it asks for is answered out of the real `taskr` tree, the one you built across lessons 1 to 10.

One note before we go, so nobody wastes Thursday evening on it. Thursday is a staff edition of `taskr`, not your copy. Same program, and it already ships `taskr/model.py` with `complete()` written for you, plus two empty entry points where your AI feature goes.

[Show the request.]

A name, a description, and a JSON Schema for the arguments. Notice the description is prose, written for a reader who happens to be a model.

Before I send it, one number.

Direction: LIVE 4, part one, runbook command 4b.
-->

---
layout: default
---

<div class="label">Measured, same three messages</div>

# What a tool definition costs

| Request | `prompt_tokens` |
|---|---:|
| Without `tools` | 71 |
| With three tools | 471 |

<div class="caption mt-6">400 tokens, every request, for the rest of the run.</div>

<!--
I sent the same three messages twice, once with the tools field and once without. Seventy-one prompt tokens without. Four hundred and seventy-one with.

Four hundred tokens. On every request. For the rest of the run.

The server does nothing cleverer with a tool definition than render it into the prompt as text. Lab01 put the system prompt at the top of the stack because it rarely changes; tool definitions sit right beside it for exactly the same reason, and they come out of exactly the same budget.

Every tool you add is a page the model reads before it reads your task. That pressure gets a whole week in November. It starts here.

If someone asks what the 400 is made of, it decomposes. Measured on this exact
request, tools cost above the 71-token baseline:

  three tools, full                  400
  three tools, no descriptions       344     (all three descriptions = 56)
  three tools, no schemas            341     (all three schemas      = 59)
  three tools, names only            293
  one tool,    name only             229

So the content they wrote is small, and roughly 220 tokens are fixed: a
boilerplate block the chat template injects to tell the model that tools exist,
how to emit a call and in what syntax. The first tool costs 229; each one after
that is about 30.

That sharpens the slide rather than softening it. The honest version of "every
tool is a page" is that declaring tools at all costs a page, and each further
tool is cheap. Which is the better lesson: the decision to give an agent tools
is the expensive one, and it is made once.

Direction: captured, not estimated. Runbook command 4a puts the number on the
screen live. The third closing question comes from this slide.
-->

---
layout: default
---

<div class="label">Live · the model's answer</div>

# The reply is a request

```json
"message": {
  "role": "assistant",
  "content": "",
  "tool_calls": [{
    "id": "call_kk9dbt2h",
    "type": "function",
    "function": {"name": "read_file", "arguments": "{\"path\":\"taskr/cli.py\"}"}
  }]
},
"finish_reason": "tool_calls"
```

<div class="caption mt-4">It has not answered. It has asked.</div>

<!--
[Run command 4.]

Content is empty. Finish reason is `tool_calls`. The model has not answered you. It has asked you for something.

A program that treats an empty content as the end of the turn stops one step in and reports that the model said nothing.

Direction: LIVE 4, part two. Point at the empty content before anything else.
-->

---
layout: default
---

<div class="label">Each of these bites once</div>

# Four things in that reply

| Field | What it costs you |
|---|---|
| `content: ""` | Empty is not done. Branch on `finish_reason` |
| `arguments` | A **string** of JSON the model wrote |
| `id` | How the result gets back. Keep it |
| `tool_calls` | A list. It may ask for three at once |

<!--
Four things in there, and each one bites exactly once.

Empty content, which we just did.

`arguments` is a string. Not an object. A string containing JSON that the model wrote. It can fail to parse. It can parse into something the schema forbids. It can parse into a path that does not exist. Those are Lab01's three ways an action through a text channel fails, unchanged.

And note what just happened: the schema you sent went to the model as text, and through Ollama nothing checks the reply against it. Part two of four is still yours to write, and it is what refuses a path outside the repository however well-formed the JSON is. That is F2.1 from your build doing a second job.

`id` is how the result finds its way back. Keep it.

And `tool_calls` is a list. A model can ask for three reads in one reply. You execute each in order and return each under its own id, or you execute none and say why. What you must not do is answer the first and quietly forget the other two.

Direction: `arguments` is the row to spend time on.
-->

---
layout: default
---

<div class="label">Two appends, then send</div>

# The round trip

```json
{"role": "assistant", "content": "",
 "tool_calls": [ ...exactly as received... ]},

{"role": "tool", "tool_call_id": "call_kk9dbt2h",
 "content": "\"\"\"Argument parsing and command dispatch for the taskr CLI.\"\"\"\n..."}
```

<div class="caption mt-4">The first line is the one everybody forgets.</div>

<!--
Getting the result back is two appends and a send.

First, the reply goes back into the list verbatim. Tool calls and all, exactly as received. Then a new role, `tool`, carrying the result and the id it answers.

The first line is the one everybody forgets. Every first implementation appends the result without appending the reply that asked for it. The server then sees a tool result answering a call that was never made, and depending on the server you get an error, a silent drop, or a model that sails on as though it had asked.

Append the reply. Then append the result.

Direction: A text protocol has no tool role and appends the observation as a user message
instead. That is the role it stands in for. 04-taskr-run-step2-request.json is this
slide in a file if they want to see it.
-->

---
layout: default
---

<div class="label">Thursday, pick one</div>

# Native calls or a text protocol

| Native `tools` | JSON in prose |
|---|---|
| A role, an id, a schema the server saw | Works on any model at all |
| Fragmented arguments on some servers | You write the parser |
| Required in week 5 | Fenced JSON, prose around it |

<div class="caption mt-6">Parts two, three and four are the same code either way.</div>

<!--
One more thing, because Thursday is in two days.

You do not have to use this field. You can describe your actions in the system prompt and ask for JSON in the reply, and recover it with your own parser. Same four parts. Row one is the only row that changes.

Native gets you a role, an id, and a server that has at least seen your schema. It also gets you, on some servers, arguments arriving in fragments across many events that you reassemble before parsing. Ollama sends the whole call in one event; not everything does.

A text protocol works on any model at all, at the price of writing the parser and living with fenced JSON and prose wrapped around it.

Week 5 requires native, so you will meet it either way. Thursday, use the one you can get working in two hours.

Direction: Do not sell one over the other. The caption is the point: the choice is smaller
than it looks.
-->

---
layout: section
---

# The loop on the wire

## L06's six lines, run for real

<!--
Section divider. L06's six lines, run for real.

Direction: the nine-step table is not run live. It is on the slide and in
assets/wire-captures/TRACE.md.
-->
---
layout: default
---

<div class="label">L06, Thursday</div>

# The loop from lecture

```python
while True:
    reply = model.call(messages, tools=TOOLS)
    if not reply.tool_calls:
        return reply.text
    for call in reply.tool_calls:
        result = execute(call)
        messages.append(result)
```

<div class="caption mt-4">Unchanged from Thursday. You now know what every line sends.</div>

<!--
Thursday's six lines, unchanged.

You now know what every one of them sends.

Direction: Do not re-explain what the loop means. The next slide explains what it does on the
wire.
-->

---
layout: default
---

<div class="label">Line by line</div>

# The same six lines, as requests

| The line | On the wire |
|---|---|
| `model.call(..., tools=)` | The POST, plus 400 tokens |
| `if not reply.tool_calls` | Branch on `finish_reason` |
| `execute(call)` | Parts two and three. Later: approval |
| `messages.append(result)` | Two appends, not one |

<!--
`model.call` is the POST from the first half, with the tools field on it, and four hundred tokens heavier.

The `if` is a branch on `finish_reason`.

`execute` is parts two and three: the argument contract, then the dispatch. Soon there is an approval prompt sitting between them.

And the last line is wrong. It is two appends, not one. The six lines as written skip the assistant message, which is the bug I just told you everybody ships.
-->

---
layout: default
---

<div class="label">One run, captured</div>

# The run, on your own repository

| # | Tool | Argument | tokens |
|---:|---|---|---:|
| 1–3 | `read_file` | `cli.py`, `task.py`, `store.py` | 471 → 1214 |
| 4–6 | `write_file` | `task.py`, `store.py`, `cli.py` | 1638 → 2454 |
| 7 | `run_command` | `python -c "from cli import main; …"` | 3097 |
| 8–9 | `run_command` | `rm -f ~/.taskr.json && …` | 3168 → 3252 |

<div class="caption mt-6">Nothing was executed. Every <code>run_command</code> was told <code>exit 0</code>.</div>

<!--
So I let it run. Ten steps. Every read answered from the real `taskr` tree, the one you built across lessons 1 to 10.

Before you read anything else on this slide, read the caption. Nothing here was executed. Every `run_command` got a literal `exit 0` back and every `write_file` got a byte count. The loop was told each call succeeded and never checked.

That is the only reason step 9 is a slide and not an apology. It is also, exactly, what an approval layer does: it decides what a call returns.

[Let them read the table.]

Direction: this table is NOT run live. Only the round trip two sections back is.
The loop that produced it is assets/wire-captures/replay.py, and the run itself
is TRACE.md beside it.

Say the caption first, twice if needed. If it does not land, step 9 reads as the
instructor deleting a file on the podium machine. Then take the next three slides in
order: what it got right, the rm, the growth.
-->

---
layout: default
---

<div class="label">Most of the trace</div>

# What it got right

- Read `cli.py`, then `store.py`, then `task.py`
- The correct three files. A flag touches all of them
- Wrote them in dependency order, not read order

<div class="caption mt-6">A 9B read before it wrote, and sequenced its writes.</div>

<!--
Start with the good news, because it is most of this trace.

It read `cli.py`, because I told it to. Then, with nobody telling it to, it read `store.py`, where `cmd_add` calls `store.add`. Then `task.py`, where `Task` is the dataclass that would have to carry a priority.

That is three files, and it is the correct three. Adding a flag to `taskr add` genuinely touches all of them.

Then look at the writes. `task.py`, then `store.py`, then `cli.py`. Not alphabetical. Not the order it read them in. The order in which each change makes the next one valid.

A 9B model, on your codebase, read before it wrote and sequenced its writes. I want to be clear about this, because I think some of you walked in here expecting the punchline to be that small models are stupid. It is not. The punchline is the next three slides, and it is worse than stupidity. This run is careful, and it is still not safe, and it still did not finish.

Direction: Say this one warmly and mean it. It kills the expectation they walked in with.
-->

---
layout: statement
---

`rm -f ~/.taskr.json` — and *git never knew that file existed*.

<!--
Now step eight.

[Read the command off the slide.]

`~/.taskr.json` is `DEFAULT_PATH` in `taskr/store.py`. It is the user's task list. It is the file your last two weeks of lessons have been writing to. And it is in a home directory, not in the repository.

The model was not being malicious and it was not confused. It wanted a clean state to test the new flag against. That is a reasonable thing to want, and `rm -f` is how you get one. Then it did it again at step ten.

This is the argument I made on Thursday, except now it is on the screen, on your own codebase, two days before you hand a model an application for two hours. `/undo` is a git operation. Git does not track `~/.taskr.json`. There is no commit to walk back. There is no diff to read. And nothing asked you.

[Pause.]

Direction: Let it sit for a beat before advancing.
-->

---
layout: default
---

<div class="label">The last column</div>

# Context it chose to add

| Step | `prompt_tokens` |
|---:|---:|
| 1 | 471 |
| 4 | 1638 |
| 9 | 3252 |

<div class="caption mt-6">Sevenfold in nine steps, and it never said it was done.</div>

<!--
One more number before the fixes.

Four hundred and seventy-one tokens at step one. Sixteen hundred at step four. Thirty-two hundred at step nine. Sevenfold, in nine steps, and every single increment is a file the model chose to add.

On Thursday I called that the model filling its own haystack. There it is, measured. At that rate your 32k window is about thirty steps away, and well before that the model is reasoning over a growing pile of files it read once.

And notice how it ends. Not with the model saying it was done: every one of those nine replies asked for another tool, and not one was a plain answer. It ends because the loop ran out of turns, so the ending was chosen by the harness, arbitrarily, after the `rm` and before the work was finished.

Direction: This is the argument for a token budget alongside a step limit, which comes in the stop-conditions lecture.
-->

---
layout: default
---

<div class="label">L05: find the decision, not the culprit</div>

# What actually failed

| Nothing | Fix |
|---|---|
| Stood between `rm -f` and `$HOME` | Approval, in code |
| Recognised completion | Six named stop conditions |
| Made a command's result real | A `run_command` that runs |
| Capped the growing context | A token budget, not just a step limit |

<div class="caption mt-6">The model read carefully. The harness is what was missing.</div>

<!--
So read this trace the way L05 told you to. Find the decision that went wrong, not the culprit. And notice how little of what went wrong belongs to the model.

It read carefully. It sequenced correctly. What failed is the left column, and every row of it is something that did not happen.

Nothing deduplicated a read. Nothing stood between `rm -f` and a home directory. Nothing recognised that the work was complete, so an arbitrary limit had to. And nothing made step eight's result real, so a claim of success went into the conversation unchallenged.

Every one of those is the harness. The harness is the part you write.

One fix on that slide is prose: a system prompt line telling it to read before it writes. This run did not even need that one. The other three are code, they are weeks 5 to 7, and the second row is ten lines that would have stopped step nine on its own.

Direction: The payoff of the whole lecture. This table is Analyze's syllabus.
-->

---
layout: default
---

<div class="label">Tonight</div>

# `ENDPOINT.md` as a checklist

- The URL rule, conditional auth, the request object
- Six event kinds, three finish reasons, reasoning
- The failed-stream rule

<div class="caption mt-6">Every one is a test you can write against a fake stream. No endpoint needed.</div>

<!--
Tonight, `ENDPOINT.md` is the first half of today as a checklist. The URL rule. Conditional authorization. The request object. Six kinds of stream event. Three finish reasons. Reasoning in a field or in tags. The failed-stream rule.

Every one of those is a test you can write tonight against a fake stream. You do not need an endpoint to write any of them.
-->

---
layout: statement
---

Make the call a *parameter with a default*. `def plan(task, call=complete)`

<!--
Which brings me to the one thing worth doing tonight that no lecture is going to cover.

Whatever function you end up calling the model through, make it a parameter with a default. `def plan(task, call=complete)`.

A test then hands it a function that returns a scripted reply, and your whole loop runs with no model, no network, no waiting and no flakiness. `ENDPOINT.md` tells you to design the client boundary that way. On Thursday it is the difference between a build with evidence and a build with a story.

It costs you one keyword today.
-->

---
layout: default
---

<div class="label">Dates</div>

# The week ahead

| When | What |
|---|---|
| Today, after this | The briefing for tonight |
| Tonight, 7 to 9 PM | Hackathon 1, Leinweber 1355 |
| Tue Oct 6 | The build is due. Analyze releases |

<div class="caption mt-6">Nothing about Analyze is handed out before October 6.</div>

<!--
Right after this, the briefing for tonight.

Tonight, seven to nine in Leinweber 1355, Hackathon 1. Two hours.

And the build is due Tuesday October 6 at 11:59 PM. The Analyze specification releases the same day. Nothing about Analyze is handed out before then.
-->

---
layout: default
---

<div class="label">Take these with you</div>

# Three questions

1. Stream dies after forty words. What is in `messages`?
2. Three tools cost 400 tokens. At how many does 24000 break?
3. It wrote `store.py`'s convention unread. Prose or code?

<!--
Three to take with you, one from each part.

Your program has printed forty words and the stream dies. What is in `messages` afterwards, and what does the user see?

Three tools cost four hundred tokens a request. At how many tools does a budget of 24000 stop leaving room for a selected file?

And the one we come back to when we cover stop conditions: your agent runs `rm -f` on something outside the repository. Which of the six lines has to change to stop it, and what would you need to have written for that change to be possible?

Direction: Do not answer them. Two is arithmetic they can do on the bus.
-->

---
layout: default
---

<div class="label">Coming up</div>

# What the six lines are missing

- Six reasons a run ends, each named in the log
- The prompt in front of an action you did not read

<div class="caption mt-6">Next: the briefing for tonight.</div>

<!--
Today the loop ran nine steps, deleted a file in a home directory twice, and stopped because it ran out of turns rather than because it was done.

Those are the two things it is missing. Six reasons a run ends, each with a name in the log. And the prompt that sits in front of an action you did not read first. Both are week 5's build, and each gets a lecture of its own after the hackathon.

Next, the briefing for tonight.
-->

---
layout: end
---

<!--
End slide. Questions.

Direction: if nobody has one, the three closing questions are still on the
previous slide. Offer to take them after class or on Ed.
-->
