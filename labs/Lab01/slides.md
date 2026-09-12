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

# Schedule

1. Aider deep dive
2. Hackathon 1
3. The next assignment
4. Office hours

<!--
Put this up while the room settles and leave it up. The agenda is part of the
first block, not an extra segment in front of it.

Say out loud that the second half is genuinely office hours: they work, you
circulate, and nobody hands anything in today. Students who have been told all
term that labs end in a checkoff will not believe it unless you say it. The
slide no longer says so, so this is on you to say.

Do not preview the build past the word itself. The reveal is still yours to
make in the third section.
-->

---
layout: default
---

<div class="label">The program in the middle</div>

# The harness

Aider is a *harness*: a program that stands between you and a model.

| The harness | The model |
|---|---|
| Picks the text the model sees | Reads it |
| Decides what a reply may do | Writes a reply |
| Edits files, then commits | Nothing |

<div class="caption">Take one apart now, build one later.</div>

<!--
This is the slide the deck was missing. Sixteen practice lessons gave them the
muscle memory and none of the model, and the word "harness" is the one they
need, because it is the thing they build in Stage 1 and extend in Analyze.

Say the right-hand column out loud. The model's entire contribution is one
block of text. Every effect on their machine is the left column acting on it.

If anyone asks about models, endpoints or config: MODEL-POLICY.md, and it is
not today's subject. qwen3.5:9b recommended, 4B permitted, any compatible
endpoint.
-->

---
layout: default
---

<div class="label">Limits</div>

# What the model never touches

- Your disk
- Your shell
- Your last session

**Text in, text out. The harness does the rest.**

<!--
Three negatives, and each one is a design decision somebody made rather than a
limitation of the model.

The third is the one that surprises people: there is no memory between
sessions. Continuity is the harness resending the history, which is why
history spends their token budget later in the deck.

The 4B and the 9B are asked for different reply shapes, whole files against
diffs. That is why a classmate's session looks different from theirs, and why
the trace in the next ten minutes may not match what they ran in practice.
Worth saying here, not worth a slide.
-->

---
layout: default
---

<div class="label">The interface</div>

# What writes, and what does not

| | |
|---|---|
| Arranges context | `/add` `/read-only` `/drop` `/tokens` `/ask` `/diff` |
| Changes your files | `/code` `/undo` |

<div class="caption">Bare text means <code>/code</code>. The default writes.</div>

<!--
Two commands in the whole set touch the repository, and one of those is the
undo. That asymmetry is the approval layer they are about to build, visible in
a tool they already use.

/help lists more than this and the set moves between versions. Run it live if
asked rather than reciting.
-->

---
layout: default
---

<div class="label">The running example</div>

# One request, three files

```text
Add a --priority flag to taskr's add command.
```

<div class="grid grid-cols-3 gap-5 mt-6">
  <div class="card">
    <div class="font-semibold mb-1">taskr/cli.py</div>
    <div class="text-sm opacity-70">Parses the flag.</div>
  </div>
  <div class="card">
    <div class="font-semibold mb-1">taskr/task.py</div>
    <div class="text-sm opacity-70">Holds the value.</div>
  </div>
  <div class="card">
    <div class="font-semibold mb-1">taskr/store.py</div>
    <div class="text-sm opacity-70">Saves and loads it.</div>
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
Ask the room to find the arrow that writes a file. There is not one leaving the
amber box. The model produced text, and a program decided what to do with it.

This is a picture of Aider, not a required architecture for their build. They
will draw their own version of this in a week.
-->

---
layout: default
---

<div class="label">Step 1 · assemble</div>

# What goes into the request

| | |
|---|---|
| Fixed each turn | Instructions, added files, repo map |
| Grows each turn | Session history, your message |

**Context is a selection. A file you never added is not in it.**

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

# File selection with /add

```text
/add taskr/cli.py taskr/task.py taskr/store.py
/read-only specs/priority.md
/tokens
```

Added files can be rewritten. Read-only files can only be cited.

**Only these commands load a file.**

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

# The repo map

```text
taskr/store.py
  Store.add(title, tags) -> Task

taskr/task.py
  Task: id, title, tags
```

Signatures, ranked into a budget. No function bodies.

<!--
The excerpt is illustrative. Do not promise the map contains every file, and do
not use its silence as proof that a dependency is absent. When a student says
"the model should have known," check whether they added the file or only let the
map mention it. Source: https://aider.chat/docs/repomap.html

Cut from the slide and worth saying: a signature tells you where to look, it
does not tell the model how the function works. Students read a map line as
evidence the model understands the function.
-->

---
layout: default
---

<div class="label">Step 1 · budget</div>

# One shared token budget

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

<div class="caption">One budget: history, map, and files.</div>

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

# Edit-shaped replies

```text
taskr/cli.py
<<<<<<< SEARCH
add.add_argument("title")
=======
add.add_argument("title")
add.add_argument("--priority", default="normal")
>>>>>>> REPLACE
```

**Adds the flag. Stores nothing. Validates nothing.**

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

# The parse step

<div class="grid grid-cols-2 gap-6 mt-6">
  <div class="card">
    <div class="flex items-center gap-3 mb-2">
      <ph-brackets-angle-bold class="text-2xl text-blue-600 shrink-0" />
      <div class="font-semibold">Parsing asks: is this a block?</div>
    </div>
    <div class="text-sm opacity-70">A missing divider is a syntax error.</div>
  </div>
  <div class="card">
    <div class="flex items-center gap-3 mb-2">
      <ph-target-bold class="text-2xl text-amber-600 shrink-0" />
      <div class="font-semibold">Validation asks: does it apply?</div>
    </div>
    <div class="text-sm opacity-70">Unknown path, or zero exact matches.</div>
  </div>
</div>

<div class="caption">Two questions. Two error messages.</div>

<!--
Their design may split these across two functions or keep them in one. We grade
the error behavior, not the signature. What we do want is that a malformed block
and an unapplicable block are distinguishable to the person reading the output.
-->

---
layout: default
---

<div class="label">Step 4 · apply</div>

# Exact-match application

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

<div class="caption">Two extra spaces. Zero matches.</div>

**Your contract: exact matches only, all blocks or none.**

<!--
Two spaces are enough to break a match. Show the difference before you name it.

Partial application is not untestable, it is testable against a different
contract. Do not tell them one policy is the only defensible one. The stricter
rule is here because it makes the state after a failure trivial to state and
to assert.

Cut from the slide: Aider itself can fall back to looser matching and can keep
the blocks that did apply. Their Stage 1 contract does neither, and that is the
contrast worth drawing out loud.
-->

---
layout: default
---

<div class="label">Step 5 · repair</div>

# The repair loop

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

<div class="caption">A fixed cycle, not the model's choice.</div>

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

# One commit per edit set

```text
* 8f2a1c3  aider: add --priority to the add command
* 41b9e07  aider: store priority on Task
* 0c7d5e1  initial taskr
```

**Git reverses files. It does not reverse a sent email.**

<!--
Keep two kinds of commit apart: the ones Aider makes while they build, and the
ones their assistant will make in a target repo. In Stage 1 the target is
disposable and clean, so an owned HEAD commit can be undone safely. A human
commit on top, or a dirty tree, means their tool has to refuse.

Running shell commands arrives in the Analyze phase and brings consequences git
cannot undo.

Undo means resetting to the parent of a commit their own session created. It
will not touch a commit someone else made, which is the guard in "guarded undo".
-->

---
layout: default
---

<div class="label">Check · 3 minutes</div>

# The six steps, recapped

With the person next to you:

1. What entered the context?
2. Which program read the reply?
3. What could look correct and be wrong?
4. What evidence proves it works?

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

# Three failure symptoms

| Symptom | Check first |
|---|---|
| Calls a function that does not exist | The file was never added |
| Block looks right, will not apply | The file changed since |
| Tests pass, feature still broken | The tests missed the gap |
| The request times out | Endpoint, model, input size |

<div class="caption">One symptom, several causes. Find the evidence.</div>

<!--
Push back on "the model is too weak" every time it comes up today. Ask what
observation would distinguish a weak model from a missing file, and make them
answer before they change models.
-->

---
layout: default
---

<div class="label">Diagnosis</div>

# Better results, same model

<div class="grid grid-cols-2 gap-6 mt-6">
  <div class="card">
    <div class="font-semibold mb-2">A chat window</div>
    <div class="text-sm opacity-70">You paste in. You paste back. You hope.</div>
  </div>
  <div class="card">
    <div class="font-semibold mb-2">Aider, same model</div>
    <div class="text-sm opacity-70">Reads what you selected, applies a fixed format, commits.</div>
  </div>
</div>

<div class="caption">Fix the harness, then judge the model.</div>

<!--
Do not let this become "the model does not matter" or "every failure is
context." Both halves are real. The point is that the harness is the half they
are about to build, and it is the half they control.
-->

---
layout: default
---

<div class="label">Practice · 6 minutes</div>

# A feature that half works

```text
$ taskr add "ship lab" --priority high
added #4
$ taskr list
#4  ship lab   priority: high

$ taskr list        # new process, same database
#4  ship lab   priority: normal
```

**What do you inspect first?**

<!--
Four minutes in pairs, two for answers. A persistence round trip is the answer
you are hoping for: write it, restart, read it back.

Watch for the two reflexes you want to break. Adding every file in the package
is not diagnosis, and switching models is not diagnosis.

The exercise, which is no longer written on the slide: write the acceptance
criterion that was missing, and the test that would have caught it. Say it
twice; it is the whole point of the six minutes.
-->

---
layout: default
---

<div class="label">Thursday September 24</div>

# Hackathon 1

- Two hours, your own project
- Prompt revealed in the room
- Submit before you leave
- Graded separately from the build

**Bring a runnable increment.**

<div class="caption">Build due <strong>Friday September 25, 11:59 PM</strong>.</div>

<!--
Three minutes including logistics. Room, time and the model in the workspace are
announced by staff. Do not invent any of them here.

Say the accommodations line out loud: conflicts and accommodations go to staff
now, not the week of.

The caption is the only place in the deck a student sees the build deadline, now
that the after-lab slide is gone. Do not skip past it.
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

# What the packet contains

<div class="grid grid-cols-2 gap-6 mt-6">
  <div class="card">
    <div class="font-semibold mb-2">In the packet</div>
```text
SPEC  ACCEPTANCE  RUBRIC  CHECKLIST
GLOSSARY  EXAMPLES  DESIGN-GUIDE
WORKFLOW  + the Aider config
```
  </div>
  <div class="card">
    <div class="font-semibold mb-2">Not in the packet</div>
    <div class="text-sm opacity-70">Application code. Tests. A layout. A diagram.</div>
  </div>
</div>

<div class="caption"><code>CHECKLIST.md</code> lists what you hand in.</div>

<!--
This is the slide that answers the question every student is holding: no
starter application and no supplied session module.

Point at CHECKLIST.md by name and say it is the submission list, so nobody
reconstructs one from these slides. GLOSSARY.md is where a word has a Stage 1
meaning that differs from its everyday one, and that meaning is the graded one.

They implement the endpoint client in Stage 1 and extend it for function
calling in Analyze.

Say the division out loud, since the slide no longer carries it: they run
`aider` to build the thing, and they write `bin/assistant` as the thing.
-->

---
layout: default
---

<div class="label">The application</div>

# The assistant's behavior

```text
/files                 → list selected files
/add greet.py          → include this file in model requests
What does greet do?    → stream an answer about the selected code
Change Hello to Hi.    → validate the reply and preview a diff
```

**A terminal assistant over selected files. Not all of Aider.**

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

# The approval step

| State | `greet.py` | Git |
|---|---|---|
| Diff shown, waiting | `Hello` | No commit |
| Approved | `Hi` | One commit |
| Declined | `Hello` | No commit |
| Undone | `Hello` | Reset to parent |

**One invalid block cancels the whole proposal.**

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

# The seven features

| Feature | Required behavior |
|---|---|
| F1 | Conversation, budget handling, streamed replies |
| F2 | Add, drop, list and clear context |
| F3 | Current file contents, rendered consistently |
| F4 | An edit-format prompt you have tested |
| F5 | Parsing with useful errors |
| F6 | Exact edits, complete preview, explicit approval |
| F7 | One commit per edit set, guarded undo |

<!--
Configuration and lifecycle are not a hidden eighth feature, and there is no
scope cut this term. Where they score, from RUBRIC.md: configuration sits
inside F1's four points and is not a gate, so unfinished configuration does not
zero the rest of F1. The lifecycle commands score separately, under Operating
instructions in the evidence group. Every edge case is in SPEC.md.
-->

---
layout: default
---

<div class="label">Configuration</div>

# The assistant's config schema

```yaml
base_url: https://api.example.edu/v1
model: course-model-id
api_key_env: ASSISTANT_API_KEY
context_budget: 8000
timeout_seconds: 60
temperature: 0.2
```

**Schema fixed. Loading and validation are yours.**

<!--
base_url can carry any path prefix. Their client appends /chat/completions and
nothing else.

Say explicitly that this YAML is not the .aider.conf.yml they already have in
aider-practice. Two files, two owners: that one configures the tool they use,
this one is a schema their own program has to implement. The deck no longer
walks through Aider's own config, so name the distinction out loud rather than
assuming the contrast landed earlier in the hour.

No Ollama-specific dependency belongs anywhere in the application. Provider
independence is a requirement, not a preference.
-->

---
layout: default
---

<div class="label">Ownership</div>

# Architecture ownership

| We specify | You design |
|---|---|
| Observable behavior and safety rules | Responsibilities and who owns state |
| The API and configuration contract | Internal interfaces and error flow |
| Acceptance scenarios and the rubric | Tests, fixtures, increment boundaries |
| Where the course is going | Where later capabilities enter |

<div class="caption">Different architectures can earn full marks.</div>

<!--
The last line is the one to say out loud. A plugin framework in week 3, written
for a capability they have not been given yet, is a cost with no evidence behind
it. Future compatibility needs a reason.
-->

---
layout: default
---

<div class="label">Specifications</div>

# Two sizes of spec

<div class="grid grid-cols-2 gap-6 mt-6">
  <div class="card">
    <div class="font-semibold mb-2">System spec, written once</div>
    <div class="text-sm opacity-70">Behavior, architecture, interfaces, failures.</div>
  </div>
  <div class="card">
    <div class="font-semibold mb-2">Increment spec, one per change</div>
    <div class="text-sm opacity-70">Scoped context, ordered tasks, a checkable result.</div>
  </div>
</div>

<div class="caption">Commit the design before the code.</div>

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

# The three diagrams

| Diagram | Answers |
|---|---|
| Components and data flow | Who owns state? |
| Request sequence | Who does what in one edit? |
| Edit lifecycle | When can an edit be undone? |

<div class="caption">Mermaid is enough. Commit the first versions.</div>

<!--
Their diagrams describe their system. Copying the Aider picture from earlier
today earns nothing. Label anything not yet implemented, and tie component names
to real code once the code exists.
-->

---
layout: default
---

<div class="label">Build rubric</div>

# Rubric: the three buckets

| Group | Points |
|---|---:|
| Specification and diagrams | 40 |
| Behavior and verification | 40 |
| Evidence and reconciliation | 20 |

<div class="caption"><code>RUBRIC.md</code> carries the split, and grades you.</div>

<!--
These are points inside the build grade, not percentages of the course grade.
The build is 4.5% of the course and is due September 25.

Do not read the table out. Send them to RUBRIC.md, which carries the
per-criterion breakdown this slide summarizes, and spend the time on the four
things worth saying out loud instead:

- Completeness and usefulness are graded. Document length is not.
- A correct failing test can earn test credit while exposing an unfinished
  feature. Only one point in the whole rubric depends on the live model
  actually succeeding, and honest evidence of a failed run still earns the
  reporting points.
- Design keeps its credit when the implementation falls short, as long as the
  design's claims and the final status are honest. No repeated deductions for
  one missing feature across otherwise sound artifacts.
- Evidence means a pointer someone can follow. Volume of logs is not evidence.

Policy violations go through academic integrity procedures, not the rubric.
-->

---
layout: default
---

<div class="label">Model rule</div>

# Model rules for specifications

- Drafting, critique, diagrams, code, tests
- 9B recommended, 4B permitted
- Secondary models recorded too
- Any compatible host allowed

**A different provider is not a different model.**

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

# One repository to December

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

**One small checkable result first. Keep the phase snapshots.**

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

# Claude Code on the same request

| Aider | An agentic CLI |
|---|---|
| You frame a bounded task | You hand over a broad one |
| You select the files | It discovers them |
| A fixed repair cycle | The model picks the next tool |
| You check between tasks | Permissions bound it |

<!--
Do not turn the left column into a weakness. Aider automates plenty. What
changes on the right is who decides the next action.

Source: https://code.claude.com/docs/en/overview
-->

---
layout: default
---

<div class="label">Future tool · instructions</div>

# Harness versus instructions

- Project instructions: persistent guidance
- Skills: instructions for one task
- Hooks: checks attached to events
- Integrations: actions and results

**Prose asks. Code and permissions enforce.**

<!--
Stay at mechanism level and do not promise a week for each branded feature.

Their DEVELOPMENT.md is the first version of this habit: instructions written
for a session that has not happened yet.
-->

---
layout: default
---

<div class="label">Design for it now</div>

# Boundaries for later capability

- Where could a model-chosen tool enter?
- Could you swap the endpoint client?
- Could a web interface reuse this?

<div class="caption">Answer with a boundary, not an implementation.</div>

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
layout: end
---
