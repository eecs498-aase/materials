---
theme: ../../lectures/theme
title: "Lab01: How Aider works"
info: |
  EECS 498 AASE, Lab01
  Design and build a pair-programmer, Fall 2026
layout: title
class: text-left
transition: fade
mdc: true
highlighter: shiki
---

# How Aider works

## Lab01 · Design your pair-programmer · Sep 14–15, 2026


<!--
Two halves. The first takes apart the tool they have been using since Lab00.
The second hands them the build and gives them 45 minutes to start designing.
Finish instruction at minute 65 and protect the work block.
-->

---
layout: default
---

<div class="label">Lab01</div>

# The second half is office hours {.assert}

| | |
|---|---|
| First | Aider as the worked example: what the model sees, how a reply becomes a file change, how to read a failure |
| Then | The hackathon 1 briefing, and what you own for the build |
| Rest | Office hours, in this room. Your work, your questions, staff circulating |

<div class="caption">Nothing is collected at the end of this lab.</div>

<!--
Put this up while the room settles and leave it up. The agenda is part of the
first block, not an extra segment in front of it.

Say out loud that the second half is genuinely office hours: they work, you
circulate, and nobody hands anything in today. Students who have been told all
term that labs end in a checkoff will not believe it unless you say it.

Do not preview the build past the word itself. The reveal is still yours to
make in the third section.
-->

---
layout: default
---

<div class="label">The running example</div>

# One request touches three files {.assert}

```text
Add a --priority flag to taskr's add command.
```

<div class="grid grid-cols-3 gap-5 mt-6">
  <div class="card">
    <div class="font-semibold mb-1">taskr/cli.py</div>
    <div class="text-sm opacity-70">Accepts the flag and its default.</div>
  </div>
  <div class="card">
    <div class="font-semibold mb-1">taskr/task.py</div>
    <div class="text-sm opacity-70">Carries the value on a task.</div>
  </div>
  <div class="card">
    <div class="font-semibold mb-1">taskr/store.py</div>
    <div class="text-sm opacity-70">Writes it down and reads it back.</div>
  </div>
</div>

<!--
They met this request in the practice lessons, in whole-file mode. Today's
trace is diff mode and it is illustrative: a simplified turn, not a captured
transcript of a particular model. The three files matter later, when the
feature half-works.
-->

---
layout: section
---

# One turn

## Selected files to commit

<!--
Six steps. Say up front that only step 2 belongs to the model.
-->

---
layout: default
---

<div class="label">Who does what</div>

# Only Aider touches your files {.assert}

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

<div class="caption">No line runs from the model to your repository. You pick the task and judge the result.</div>

<!--
Ask the room to find the arrow that writes a file. There is not one leaving the
amber box. The model produced text, and a program decided what to do with it.

This is a picture of Aider, not a required architecture for their build. They
will draw their own version of this in a week.
-->

---
layout: default
---

<div class="label">Step 1 · assemble</div>

# Aider builds the request from parts you chose {.assert}

- The instructions that define the edit format
- The files you added, in full
- A repository map, when it is enabled
- The chat history from this session
- Your new message

**Context is a selection. A file on disk that you never added is not in it.**

<!--
Do not claim a fixed seven-part ordering. What actually goes into the prompt
depends on the coder, the model and the settings, and it changes between
releases. The list above is the shape, not the wire format.

Ask what the model would need in order to add priority consistently to the CLI,
the task and the store. That question sets up the next two slides.
-->

---
layout: default
---

<div class="label">Step 1 · selection</div>

# The /add command decides what the model reads {.assert}

```text
/add taskr/cli.py taskr/task.py taskr/store.py
/read-only specs/priority.md
/tokens
```

Added files can be rewritten. Read-only files can only be cited.

Naming a path in a sentence does not load it. Only these commands do.

<!--
Walk through why these three files and not the whole package. This is one
sensible selection, not a rule to add everything. Read-only context still
costs budget. /tokens tells you what you are spending, and nothing about
whether the edit will be correct.
-->

---
layout: default
---

<div class="label">Step 1 · repository map</div>

# The repo map carries signatures without bodies {.assert}

```text
taskr/store.py
  Store.add(title, tags) -> Task

taskr/task.py
  Task: id, title, tags
```

Aider builds a graph of definitions and references, then ranks the useful parts into a token budget.

A signature tells you where to look. It does not tell the model how the function works.

<!--
The excerpt is illustrative. Do not promise the map contains every file, and do
not use its silence as proof that a dependency is absent. When a student says
"the model should have known," check whether they added the file or only let the
map mention it. Source: https://aider.chat/docs/repomap.html
-->

---
layout: default
---

<div class="label">Step 1 · budget</div>

# Everything you add spends the same budget {.assert}

<div class="mt-2">
<svg viewBox="0 0 960 300" style="width:100%;max-height:300px" role="img"
     aria-label="Two horizontal bars showing one input budget. In an early turn, instructions, repo map, selected files, history and your message fit with headroom left. In a later turn the history has grown and your message no longer fits inside the limit.">
  <line x1="830" y1="40" x2="830" y2="272" stroke="var(--c-rule-strong)" stroke-width="2" stroke-dasharray="5 5" />
  <text x="830" y="28" text-anchor="middle" style="font:500 11.5px var(--font-mono); letter-spacing:0.12em" fill="var(--c-ink-muted)">BUDGET LIMIT</text>
  <text x="118" y="106" text-anchor="end" style="font:500 11.5px var(--font-mono); letter-spacing:0.12em" fill="var(--c-ink-muted)">EARLY TURN</text>
  <text x="118" y="228" text-anchor="end" style="font:500 11.5px var(--font-mono); letter-spacing:0.12em" fill="var(--c-ink-muted)">LATER TURN</text>
  <g stroke="var(--c-rule-strong)">
    <rect x="130" y="64" width="110" height="76" fill="var(--c-bg-2)" />
    <rect x="240" y="64" width="100" height="76" fill="var(--c-bg-2)" />
    <rect x="340" y="64" width="230" height="76" fill="var(--c-primary)" fill-opacity="0.16" stroke="var(--c-primary)" />
    <rect x="570" y="64" width="90" height="76" fill="var(--c-primary)" fill-opacity="0.07" stroke="var(--c-primary)" />
    <rect x="660" y="64" width="90" height="76" fill="var(--c-bg-2)" />
    <rect x="750" y="64" width="80" height="76" fill="none" stroke-dasharray="4 4" />
  </g>
  <g style="font:500 11.5px var(--font-mono)" fill="var(--c-ink-soft)" text-anchor="middle">
    <text x="185" y="106">instructions</text>
    <text x="290" y="106">repo map</text>
    <text x="455" y="106">selected files</text>
    <text x="615" y="106">history</text>
    <text x="705" y="106">message</text>
    <text x="790" y="106">headroom</text>
  </g>
  <g stroke="var(--c-rule-strong)">
    <rect x="130" y="186" width="110" height="76" fill="var(--c-bg-2)" />
    <rect x="240" y="186" width="100" height="76" fill="var(--c-bg-2)" />
    <rect x="340" y="186" width="230" height="76" fill="var(--c-primary)" fill-opacity="0.16" stroke="var(--c-primary)" />
    <rect x="570" y="186" width="260" height="76" fill="var(--c-primary)" fill-opacity="0.07" stroke="var(--c-primary)" />
    <rect x="830" y="186" width="90" height="76" fill="var(--c-rose)" fill-opacity="0.12" stroke="var(--c-rose)" stroke-dasharray="4 4" />
  </g>
  <g style="font:500 11.5px var(--font-mono)" fill="var(--c-ink-soft)" text-anchor="middle">
    <text x="185" y="228">instructions</text>
    <text x="290" y="228">repo map</text>
    <text x="455" y="228">selected files</text>
    <text x="700" y="228">history</text>
  </g>
  <text x="875" y="228" text-anchor="middle" style="font:500 11.5px var(--font-mono)" fill="var(--c-rose)">message</text>
  <text x="875" y="284" text-anchor="middle" style="font:500 11.5px var(--font-mono)" fill="var(--c-rose)">does not fit</text>
</svg>
</div>

<div class="caption">History and the repo map spend the same budget as the file you actually care about.</div>

<!--
Ask what they would drop first and what has to survive. Their Stage 1 contract
keeps the system instructions, the current request and the added file contents,
and refuses an oversized required input instead of silently trimming it. That
refusal is a design decision they have to write down and test.
-->

---
layout: default
---

<div class="label">Step 2 · the reply</div>

# The model answers with edit-shaped text {.assert}

```text
taskr/cli.py
<<<<<<< SEARCH
add.add_argument("title")
=======
add.add_argument("title")
add.add_argument("--priority", default="normal")
>>>>>>> REPLACE
```

This block adds a flag to the CLI. Nothing stores the value and nothing validates it.

<!--
Deliberately small and deliberately incomplete. Ask what is missing before you
say it: task.py never gains the field, store.py never writes it. A student who
reads only this block sees a finished feature.

Nothing has changed on disk yet. This is a proposal in a chat reply.
-->

---
layout: default
---

<div class="label">Step 3 · parse</div>

# Aider parses the reply before it trusts it {.assert}

<div class="grid grid-cols-2 gap-6 mt-6">
  <div class="card">
    <div class="flex items-center gap-3 mb-2">
      <ph-brackets-angle-bold class="text-2xl text-blue-600 shrink-0" />
      <div class="font-semibold">Parsing asks: is this a block?</div>
    </div>
    <div class="text-sm opacity-70">A missing divider is a syntax error. Report it and keep running.</div>
  </div>
  <div class="card">
    <div class="flex items-center gap-3 mb-2">
      <ph-target-bold class="text-2xl text-amber-600 shrink-0" />
      <div class="font-semibold">Validation asks: does it apply?</div>
    </div>
    <div class="text-sm opacity-70">An unknown path, or zero exact matches, fails later and for a different reason.</div>
  </div>
</div>

<div class="caption">Two questions, two error messages. A student who merges them writes one useless message for both.</div>

<!--
Their design may split these across two functions or keep them in one. We grade
the error behavior, not the signature. What we do want is that a malformed block
and an unapplicable block are distinguishable to the person reading the output.
-->

---
layout: default
---

<div class="label">Step 4 · apply</div>

# An edit lands only on an exact match {.assert}

<div class="grid grid-cols-2 gap-6 mt-4">
  <div class="card">
    <div class="font-semibold mb-2">On disk</div>

```text
add.add_argument("title")
```

  </div>
  <div class="card">
    <div class="font-semibold mb-2">In the SEARCH block</div>

```text
add.add_argument( "title" )
```

  </div>
</div>

<div class="caption">Two extra spaces. Zero matches. The block is well formed and cannot be applied.</div>

Aider can fall back to looser matching, and it can keep the blocks that did apply.

**Your Stage 1 contract does neither. Exact matches only, and all blocks or none.**

<!--
Two spaces are enough to break a match. Show the difference before you name it.

Partial application is not untestable, it is testable against a different
contract. Do not tell them one policy is the only defensible one. The stricter
rule is here because it makes the state after a failure trivial to state and
to assert.
-->

---
layout: default
---

<div class="label">Step 5 · repair</div>

# A failed edit becomes the next prompt {.assert}

<div class="mt-2">
<svg viewBox="0 0 900 278" style="width:100%;max-height:290px" role="img"
     aria-label="A proposed edit is matched against the file. On a match it is applied. On no match the failure is reported back and becomes a new proposed edit. Lint and test output can be fed back the same way.">
  <defs>
    <marker id="lp-b" markerWidth="9" markerHeight="9" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="var(--c-primary)" /></marker>
    <marker id="lp-a" markerWidth="9" markerHeight="9" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="var(--c-amber)" /></marker>
  </defs>
  <rect x="60" y="34" width="230" height="68" rx="8" fill="var(--c-bg-1)" stroke="var(--c-primary)" stroke-width="1.5" />
  <rect x="350" y="34" width="230" height="68" rx="8" fill="var(--c-bg-1)" stroke="var(--c-primary)" stroke-width="1.5" />
  <rect x="640" y="34" width="210" height="68" rx="8" fill="var(--c-bg-1)" stroke="var(--c-primary)" stroke-width="1.5" />
  <g style="font:500 15px var(--font-mono)" fill="var(--c-ink)" text-anchor="middle">
    <text x="175" y="73">proposed edit</text>
    <text x="465" y="73">match the file</text>
    <text x="745" y="73">applied</text>
  </g>
  <g stroke="var(--c-primary)" stroke-width="2" fill="none">
    <path d="M290,68 H344" marker-end="url(#lp-b)" />
    <path d="M580,68 H634" marker-end="url(#lp-b)" />
  </g>
  <path d="M465,102 V168 H175 V108" stroke="var(--c-amber)" stroke-width="2" fill="none" marker-end="url(#lp-a)" />
  <text x="320" y="158" text-anchor="middle" style="font:500 13px var(--font-sans)" fill="var(--c-amber)">no match, send the failure back</text>
  <path d="M745,102 V236 H120 V108" stroke="var(--c-amber)" stroke-width="2" stroke-dasharray="6 4" fill="none" marker-end="url(#lp-a)" />
  <text x="440" y="226" text-anchor="middle" style="font:500 13px var(--font-sans)" fill="var(--c-amber)">lint or test output, when you configure it</text>
</svg>
</div>

<div class="caption">Aider chooses the next action here from a fixed set. It is a repair cycle, not a tool the model picked.</div>

<!--
Say clearly that Aider has real automation. It runs commands, it can run your
tests, and it can loop on their output. Never say it cannot.

The distinction that matters is who picks the next action. Here the harness has
a fixed repair cycle. In the tools we look at after the break, the model picks.
Source: https://aider.chat/docs/usage/lint-test.html
-->

---
layout: default
---

<div class="label">Step 6 · commit</div>

# Every accepted edit becomes one commit {.assert}

```text
* 8f2a1c3  aider: add --priority to the add command
* 41b9e07  aider: store priority on Task
* 0c7d5e1  initial taskr
```

Undo means resetting to the parent of a commit your own session created.

**Git reverses file changes. It does not reverse an email that has already been sent.**

<!--
Keep two kinds of commit apart: the ones Aider makes while they build, and the
ones their assistant will make in a target repo. In Stage 1 the target is
disposable and clean, so an owned HEAD commit can be undone safely. A human
commit on top, or a dirty tree, means their tool has to refuse.

Running shell commands arrives in the Analyze phase and brings consequences git
cannot undo.
-->

---
layout: default
---

<div class="label">Check · 3 minutes</div>

# The six steps account for the whole feature {.assert}

For `--priority`, answer with the person next to you:

1. What entered the context, and what did not?
2. Which program read the reply?
3. What could look correct and still be wrong?
4. What evidence would show the feature works?

<!--
Pairs for two minutes, then take two answers. You are listening for the missing
storage write or the missing persistence test. Do not reward naming a source
file inside aider.
-->

---
layout: section
---

# Diagnosis

## Read the failure before you re-prompt

<!--
Ten minutes. The habit to build: a symptom is evidence about which of the three
levers is wrong, and re-running the same prompt tests nothing.
-->

---
layout: default
---

<div class="label">Diagnosis</div>

# Each failure has its own symptom {.assert}

| What you see | What to check first |
|---|---|
| It calls a function that does not exist | The file defining it was never added |
| The block looks right and will not apply | The file changed after the model saw it |
| Tests pass, the feature is still broken | The tests never covered the missing part |
| The request times out | The endpoint URL, the served model, the input size |

<div class="caption">More than one cause can produce the same symptom. Name the evidence that separates them.</div>

<!--
Push back on "the model is too weak" every time it comes up today. Ask what
observation would distinguish a weak model from a missing file, and make them
answer before they change models.
-->

---
layout: default
---

<div class="label">Diagnosis</div>

# Aider improves results without a better model {.assert}

<div class="grid grid-cols-2 gap-6 mt-6">
  <div class="card">
    <div class="font-semibold mb-2">A chat window</div>
    <div class="text-sm opacity-70">You paste code in. It answers with code. You copy the answer back and hope you pasted the right version.</div>
  </div>
  <div class="card">
    <div class="font-semibold mb-2">Aider, same model</div>
    <div class="text-sm opacity-70">It reads the files you selected, answers in a fixed edit format, applies the result and commits it.</div>
  </div>
</div>

<div class="caption">The model still has limits. You can measure them once the harness stops being the variable.</div>

<!--
Do not let this become "the model does not matter" or "every failure is
context." Both halves are real. The point is that the harness is the half they
are about to build, and it is the half they control.
-->

---
layout: default
---

<div class="label">Practice · 6 minutes</div>

# The priority value disappears on restart {.assert}

```text
$ taskr add "ship lab" --priority high
added #4
$ taskr list
#4  ship lab   priority: high

$ taskr list        # new process, same database
#4  ship lab   priority: normal
```

What do you inspect first? Write the acceptance criterion that was missing, and the test that would have caught it.

<!--
Four minutes in pairs, two for answers. A persistence round trip is the answer
you are hoping for: write it, restart, read it back.

Watch for the two reflexes you want to break. Adding every file in the package
is not diagnosis, and switching models is not diagnosis.
-->

---
layout: default
---

<div class="label">September 24</div>

# Hackathon 1 runs in the browser workspace {.assert}

- Two hours, during the session, on your own project
- The feature prompt is revealed in the room
- You submit before you leave
- Graded on its own, separately from the build

**Bring a runnable increment. There is no separate hackathon project to prepare.**

<!--
Three minutes including logistics. Room, time and the model in the workspace are
announced by staff. Do not invent any of them here.

Say the accommodations line out loud: conflicts and accommodations go to staff
now, not the week of. Build is due the next day, September 25.
-->

---
layout: section
---

# The build

## Design first, then implement in increments

<!--
Minute 40. Fifteen minutes. Everything here is also written down in their
packet, so do not read the rubric aloud line by line.
-->

---
layout: default
---

<div class="label">Stage 1 · the packet</div>

# The packet gives you specs and no code {.assert}

<div class="grid grid-cols-2 gap-6 mt-6">
  <div class="card">
    <div class="font-semibold mb-2">In the packet</div>
    <div class="text-sm opacity-70">SPEC.md, RUBRIC.md, ACCEPTANCE.md, EXAMPLES.md, DESIGN-GUIDE.md, WORKFLOW.md, and the Aider configuration you build with.</div>
  </div>
  <div class="card">
    <div class="font-semibold mb-2">Not in the packet</div>
    <div class="text-sm opacity-70">Application code. Tests. A module layout. A conversation loop. A diagram of the answer.</div>
  </div>
</div>

<div class="caption">You run <code>aider</code> to build it. You write <code>bin/assistant</code> to run what you built.</div>

<!--
This is the slide that answers the question every student is holding. No
starter application, no supplied session module, no TOML to edit, no two
prescribed specs.

They implement the endpoint client in Stage 1 and extend it for function
calling in Analyze.
-->

---
layout: default
---

<div class="label">The application</div>

# Your assistant reads files and proposes edits {.assert}

```text
/files                 → list selected files
/add greet.py          → include this file in model requests
What does greet do?    → stream an answer about the selected code
Change Hello to Hi.    → validate the reply and preview a diff
```

A terminal assistant over selected text files. Not all of Aider.

<!--
Open EXAMPLES.md from the template and walk the four transcripts: a question, an
approved edit, a cancellation, an undo. Say that these are the expected
behavior, not a recording of a staff implementation.

Ask what happens to the files and to HEAD at each point. That question starts
their acceptance criteria, which is a better use of this block than a tour of
the feature list.
-->

---
layout: default
---

<div class="label">The safety rule</div>

# Nothing changes on disk until you approve it {.assert}

| Point in the interaction | `greet.py` | Git |
|---|---|---|
| Diff shown, waiting | Still `Hello` | No new commit |
| You approve | Now `Hi` | One owned edit commit |
| You decline | Still `Hello` | No new commit |
| You undo the approved edit | Back to `Hello` | Reset to the parent commit |

**One invalid block cancels the whole proposal, including the blocks that were fine.**

<!--
Use the exact greeting files and replies from EXAMPLES.md so the table matches
what they will read tonight.

Undo assumes an owned, current-session HEAD and a clean target. A human commit
on top, or uncommitted changes, means refuse. Ask them what they would assert in
a test for each row.
-->

---
layout: default
---

<div class="label">Scope</div>

# Seven features define the build {.assert}

| Feature | Required behavior |
|---|---|
| F1 | Conversation, budget handling, streamed replies |
| F2 | Add, drop, list and clear context |
| F3 | Current file contents, rendered consistently |
| F4 | An edit-format prompt you have tested |
| F5 | Parsing with useful errors |
| F6 | Exact edits, complete preview, explicit approval |
| F7 | One commit per accepted edit set, guarded undo |

<!--
Configuration and lifecycle run across all seven. They are not a hidden eighth
feature and there is no scope cut this term. Every edge case is in SPEC.md.
-->

---
layout: default
---

<div class="label">Configuration</div>

# One YAML file selects the endpoint and model {.assert}

```yaml
base_url: https://api.example.edu/v1
model: course-model-id
api_key_env: ASSISTANT_API_KEY
context_budget: 8000
timeout_seconds: 60
temperature: 0.2
```

The schema is fixed. How you load, represent and validate it is yours.

<!--
base_url can carry any path prefix. Their client appends /chat/completions and
nothing else. Aider's own YAML config is a separate file and unrelated.

No Ollama-specific dependency belongs anywhere in the application. Provider
independence is a requirement, not a preference.
-->

---
layout: default
---

<div class="label">Ownership</div>

# You own the architecture {.assert}

| We specify | You design |
|---|---|
| Observable behavior and safety rules | Responsibilities and who owns state |
| The API and configuration contract | Internal interfaces and error flow |
| Acceptance scenarios and the rubric | Tests, fixtures, increment boundaries |
| Where the course is going | Where later capabilities enter |

<div class="caption">Different architectures can earn full marks. Designing for a future you cannot describe cannot.</div>

<!--
The last line is the one to say out loud. A plugin framework in week 3, written
for a capability they have not been given yet, is a cost with no evidence behind
it. Future compatibility needs a reason.
-->

---
layout: default
---

<div class="label">Specifications</div>

# Specs come in two sizes {.assert}

<div class="grid grid-cols-2 gap-6 mt-6">
  <div class="card">
    <div class="font-semibold mb-2">System spec, written once</div>
    <div class="text-sm opacity-70">Behavior, architecture, interfaces, failure handling, verification, and why you chose it.</div>
  </div>
  <div class="card">
    <div class="font-semibold mb-2">Increment spec, one per change</div>
    <div class="text-sm opacity-70">Scoped context, ordered tasks, and a result you can check when it is done.</div>
  </div>
</div>

<div class="caption">Commit the design before the application code. Revise it when evidence changes a decision.</div>

<!--
A system spec is not one giant context dump. Requirements map to planned tests,
and those test files do not have to exist yet.

Experiments are allowed. Label them, and reconcile them with the design before
you build on top of them.
-->

---
layout: default
---

<div class="label">Diagrams</div>

# Three diagrams answer three questions {.assert}

| Diagram | The question it answers |
|---|---|
| Components and data flow | Who owns state, and what crosses each boundary? |
| Request sequence | Who does what during one proposed edit? |
| Edit lifecycle | When can an edit be approved, rejected or undone? |

<div class="caption">Mermaid is enough. Keep the first versions in git and update the final ones to match what you built.</div>

<!--
Their diagrams describe their system. Copying the Aider picture from earlier
today earns nothing. Label anything not yet implemented, and tie component names
to real code once the code exists.
-->

---
layout: default
---

<div class="label">Build rubric</div>

# Specification and diagrams carry 40 points {.assert}

| Criterion | Points |
|---|---:|
| Requirements and acceptance criteria | 10 |
| Architecture and interface design | 10 |
| Aider implementation specs | 10 |
| Diagrams: components 4, sequence 3, lifecycle 3 | 10 |

<div class="caption">Completeness and usefulness are graded. Document length is not.</div>

<!--
These are points inside the build grade, not percentages of the course grade.
The build is 4.5% of the course and is due September 25.

Design keeps its credit when the implementation falls short, as long as the
design's claims and the final status are honest.
-->

---
layout: default
---

<div class="label">Build rubric</div>

# Behavior and verification carry 40 points {.assert}

| Criterion | Points |
|---|---:|
| Required functionality, scored feature by feature | 20 |
| Behavioral tests | 8 |
| Safety and recovery tests | 7 |
| Fake integration 3, live evidence 2 | 5 |

<div class="caption">A correct failing test can earn test credit while exposing an unfinished feature.</div>

<!--
The per-feature split is in RUBRIC.md. Only one F4 point depends on the live
model actually succeeding, and honest evidence of an unsuccessful run still
earns the reporting points.

They write every test, including the client protocol checks.
-->

---
layout: default
---

<div class="label">Build rubric</div>

# Evidence and reconciliation carry 20 points {.assert}

| Criterion | Points |
|---|---:|
| Spec-first history | 5 |
| Deliberate Aider use | 5 |
| Diagnosis and design reconciliation | 5 |
| Operating instructions | 3 |
| Model disclosure and evidence index | 2 |

<div class="caption">Evidence means a pointer someone can follow. Volume of logs is not evidence.</div>

<!--
No points for suffering, and no repeated deductions for one missing feature
across otherwise sound artifacts.

Policy violations go through academic integrity procedures, not the rubric.
-->

---
layout: default
---

<div class="label">Model rule</div>

# The model rule covers your specification too {.assert}

- Drafting, critique, diagrams, code and tests all fall under it
- The 9B is recommended, the 4B is permitted
- Secondary models get recorded the same way
- Any compatible hosting service is allowed

**A different provider does not authorize a different model.**

<!--
Exact model IDs and the observed-session exception are in the assignment packet.
Read them from there rather than from memory.

The pattern being ruled out is a frontier model for the design followed by a
local model for the code. Keep the sessions, disclose real aliases and any
quantization you know about.
-->

---
layout: default
---

<div class="label">Through December</div>

# One repository carries you to December {.assert}

<div class="mt-4">
<svg viewBox="0 0 900 150" style="width:100%;max-height:180px" role="img"
     aria-label="A timeline with three phases: Apply adds one loop with exact edits and git, Analyze adds model-selected tools, Create adds memory, hardening and another way in.">
  <line x1="80" y1="70" x2="820" y2="70" stroke="var(--c-rule-strong)" stroke-width="2" />
  <g fill="var(--c-primary)">
    <circle cx="170" cy="70" r="7" />
    <circle cx="450" cy="70" r="7" />
    <circle cx="730" cy="70" r="7" />
  </g>
  <g style="font:600 12px var(--font-mono); letter-spacing:0.14em" fill="var(--c-primary)" text-anchor="middle">
    <text x="170" y="48">APPLY</text>
    <text x="450" y="48">ANALYZE</text>
    <text x="730" y="48">CREATE</text>
  </g>
  <g style="font:400 13px var(--font-sans)" fill="var(--c-ink-soft)" text-anchor="middle">
    <text x="170" y="102">one loop, exact edits, git</text>
    <text x="450" y="102">model-selected tools</text>
    <text x="730" y="102">memory, hardening, another way in</text>
  </g>
</svg>
</div>

Start with one small result you can check. Refactor when you need to, and keep the phase snapshots.

<!--
Close the project block here. Build due September 25, hackathon September 24.

Do not estimate the workload out loud. Do say that a runnable slice early is
what keeps the December integration from being a surprise.
-->

---
layout: section
---

# What comes next

## The same request, in a different kind of tool

<!--
Minutes 55 to 65. This is a mechanism comparison, not a product tour and not a
recommendation. Nothing here is a Stage 1 dependency and no subscription is
needed for this course.
-->

---
layout: default
---

<div class="label">Future tool · Claude Code</div>

# Claude Code lets the model pick the next step {.assert}

| Aider | A general agentic CLI |
|---|---|
| You frame a bounded edit task | You hand over a broader task |
| Selected files and a repo map | Tools that discover and read files |
| A fixed repair cycle | The model picks the next tool |
| You check between tasks | Permissions and stop rules bound it |

<!--
Do not turn the left column into a weakness. Aider automates plenty. What
changes on the right is who decides the next action.

Source: https://code.claude.com/docs/en/overview
-->

---
layout: default
---

<div class="label">Future tool · the same request</div>

# An agentic CLI runs the whole request itself {.assert}

```text
grep -rn "add_argument" taskr/   → finds cli.py
read taskr/store.py              → finds the save path
edit cli.py, task.py, store.py
pytest -q                        → 1 failed
edit store.py
pytest -q                        → passed
```

**Each result is evidence for the next decision. Who stops a bad one?**

<!--
Label this a hypothetical trace. You have not run it and it is not a product
demonstration.

The model can only choose from what the harness exposes and what permissions
allow. That sentence is the whole design problem, and they build it in Analyze.
-->

---
layout: default
---

<div class="label">Future tool · instructions</div>

# Written instructions still need a harness {.assert}

- Project instructions give persistent guidance
- Skills package instructions for a particular task
- Hooks attach checks to events
- Tool integrations expose actions and results

**Prose asks. Code and permissions enforce.**

<!--
Stay at mechanism level and do not promise a week for each branded feature.

Their DEVELOPMENT.md is the first version of this habit: instructions written
for a session that has not happened yet.
-->

---
layout: default
---

<div class="label">Future tool · OpenClaw</div>

# A gateway gives one agent many ways in {.assert}

<div class="mt-2">
<svg viewBox="0 0 900 290" style="width:100%;max-height:300px" role="img"
     aria-label="Three clients feed into a gateway that handles connections and routing. The gateway connects down to an agent runtime with tools and to connected nodes.">
  <defs>
    <marker id="gw" markerWidth="9" markerHeight="9" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="var(--c-primary)" /></marker>
  </defs>
  <g stroke="var(--c-rule-strong)" fill="var(--c-bg-1)">
    <rect x="90" y="14" width="200" height="48" rx="8" />
    <rect x="350" y="14" width="200" height="48" rx="8" />
    <rect x="610" y="14" width="200" height="48" rx="8" />
  </g>
  <g style="font:500 14px var(--font-mono)" fill="var(--c-ink)" text-anchor="middle">
    <text x="190" y="44">chat channel</text>
    <text x="450" y="44">web client</text>
    <text x="710" y="44">another service</text>
  </g>
  <rect x="60" y="118" width="780" height="58" rx="10" fill="var(--c-highlight)" stroke="var(--c-amber)" stroke-width="2.5" />
  <text x="450" y="153" text-anchor="middle" style="font:600 16px var(--font-mono)" fill="var(--c-amber)">gateway: connections and routing</text>
  <g stroke="var(--c-rule-strong)" fill="var(--c-bg-1)">
    <rect x="110" y="214" width="300" height="58" rx="8" />
    <rect x="490" y="214" width="300" height="58" rx="8" />
  </g>
  <g style="font:500 14px var(--font-mono)" fill="var(--c-ink)" text-anchor="middle">
    <text x="260" y="249">agent runtime and tools</text>
    <text x="640" y="249">connected nodes</text>
  </g>
  <g stroke="var(--c-primary)" stroke-width="2" fill="none">
    <path d="M190,62 V114" marker-end="url(#gw)" />
    <path d="M450,62 V114" marker-end="url(#gw)" />
    <path d="M710,62 V114" marker-end="url(#gw)" />
    <path d="M260,176 V210" marker-end="url(#gw)" />
    <path d="M640,176 V210" marker-end="url(#gw)" />
  </g>
</svg>
</div>

<!--
Your terminal is one entry point. A gateway is what makes it several.

Keep the client connections separate from the agent runtime in their heads. This
is not several agents working on one task. OpenClaw is a comparison, not a
library anyone here has to adopt.
Source: https://docs.openclaw.ai/concepts/architecture
-->

---
layout: default
---

<div class="label">Design for it now</div>

# Your design names where new capability enters {.assert}

- Where could a model-selected tool join your control flow?
- Could you swap the endpoint client without touching state management?
- Could a web interface reuse the same application behavior?

<div class="caption">Answer with a boundary, not an implementation. You are allowed to change your answer in November.</div>

<!--
End the comparison here, at minute 65. Nothing after this slide is yours to
talk through.
-->

---
layout: section
---

# Office hours

## The rest of the session is yours

<!--
Stop talking. Staff circulate from here. Leave the deck up so students can page
back through it themselves.

This is the point where you say plainly that nothing is due at the end of
today. Most of them will still expect a checkoff.
-->

---
layout: default
---

<div class="label">Office hours</div>

# Spend this time on whatever is in your way {.assert}

Staff are in the room. Good things to use them for:

1. Your repository access or tooling not running
2. A requirement in the packet you read two ways
3. The boundary of your first increment
4. A design decision you want argued with

<div class="caption">Nothing here is collected. Start wherever your build is actually stuck.</div>

<!--
No application exists to run yet. They launch aider directly with .env and the
supplied configuration, and they write bin/assistant themselves.

If someone lacks repository access, fix it immediately and let them read the
packet while you do. Do not hand them an unrelated clone as a substitute.
That one is worth hunting for rather than waiting to be asked about.

The list is a menu, not an order of work. A student who spends the whole time
reading SPEC.md has used it correctly.
-->

---
layout: default
---

<div class="label">Worth doing</div>

# A partner finds what you stopped seeing {.assert}

If you want a second pair of eyes before you leave, trade these three:

1. What has to be true when this increment is done?
2. Which decision would the model still have to guess?
3. What test would catch a plausible mistake here?

<div class="caption">Optional, and not recorded anywhere. Bring anything ambiguous in the packet to staff instead.</div>

<!--
Fifty students at five minutes each is 250 staff-minutes, so there is no full
design review queue today and do not promise one.

Peer review is about contracts and verification. It is not code sharing. A
blocking question gets a concrete follow-up through Ed or office hours.

What you are looking for as you circulate: an observable outcome, named state
ownership, explicit error behavior, and one meaningful test. Accept different
architectures. Do not require a particular file, class or module count.
-->

---
layout: default
---

<div class="label">The build · due Fri Sep 25</div>

# Finish the design before you write code {.assert}

1. Complete the system design and the three diagrams
2. Review them in a fresh permitted-model session
3. Commit the design and the first increment spec

Then build, test and revise one increment at a time.

<div class="caption">This is the build talking, not this lab. Submission packet, deadlines and exact scoring all live in your repository.</div>

<!--
Say the distinction out loud. Nothing on this slide is due because of today;
it is the order of work for a project that has been due Sep 25 all along, and
a room that has just been told the lab collects nothing can hear this list as
a lab assignment if you let it.

Read the packet list once: design, diagrams, specs, code and tests,
configuration example, DEVELOPMENT.md, operating README, evidence, AI_LOG.md,
reflection, and the preserved sessions.

Lab02 is supported implementation and verification time. September 25 does not
move.
-->

---
layout: end
---
