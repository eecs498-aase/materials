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
Two halves. The first takes apart the tool they have been using since Lab00,
in enough depth that they can recognise the same decisions in any harness. The
second hands them the build.

The deep dive is the point of the session now, not a warm-up for the assignment
reveal, so do not compress it to reach the packet. Office hours take whatever is
left.
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
layout: section
---

# The harness

## The program between you and the model

<!--
Section slide added 2026-09-13 on instructor direction: the harness is the
first section of the lab and should read as one. Eight slides under it. The
four harnesses they have already used, then what a harness is and what the
model never touches. Aider drawn as one, then what its reply looks like: the
edit block, the two shapes it comes in, and the general problem of recovering
an action from text. Then what Aider lacks that the familiar ones have.

The examples come before the definition, so the word lands on tools they know
before it gets an abstract shape. The reply slides moved here from the middle
of the deck the same night, because a reply is the harness's "answer" card and
was sitting in a section about caching.

The section exists because sixteen practice lessons gave them the muscle
memory and none of the model, and "harness" is the word they need: it is the
thing they build in Stage 1 and extend in Analyze.
-->

---
layout: default
---

<div class="label">Harnesses you know</div>

# You have already used four harnesses {.assert}

| | Puts in front of the model | Does with the reply |
|---|---|---|
| ChatGPT | Your messages, and notes it kept | Shows it to you |
| Cursor | Files you point at, and an index | A diff you accept |
| Claude Code | Files it read on its own, and notes you kept | Edits or runs commands, if allowed |
| Aider | Files you add, and a map | Writes it, then commits |

**One kind of model behind all four. The harness is what differs.**

<!--
Opens the section, on instructor direction, so the word lands on tools they
know before it gets a definition. Three of these they used before the course
and never called a harness. Read one row across: what the program put in
front of the model, and what it did with the text that came back. Every row
is the same two jobs, and the next slide names them.

ChatGPT's memory is the clean example. It feels like the model remembering
you. It is the harness keeping notes and pasting them into the prompt, and
two slides on is why: the model keeps nothing between sessions, so anything
that persists is the harness re-sending it. Claude Code's notes are the same
trick from the other side, a file you keep that is read in at the start of
every session.

Read the third column as the approval layer. Cursor waits for accept. Claude
Code asks, or does not, depending on a permission setting somebody chose.
Aider does not wait: it writes and commits, and /undo is the recovery. Their
build has to ask before it writes, which is the packet's rule, and this column
is the same decision made four different ways.

Do not go further into Claude Code than its row. How it decides what to read
and what to run is tomorrow's lecture, with a live demo behind it.
-->

---
layout: default
---

<div class="label">What a harness is</div>

# A harness is everything around the model {.assert}

<div class="grid grid-cols-3 gap-6 mt-8 items-stretch">
  <div class="card">
    <ph-stack-bold class="text-3xl text-blue-600 mb-3" />
    <div class="font-semibold mb-1">Assemble</div>
    <div class="text-sm opacity-70 flex-1">Picks every word the model will see.</div>
  </div>
  <div class="card">
    <ph-chat-text-bold class="text-3xl text-amber-600 mb-3" />
    <div class="font-semibold mb-1">Answer</div>
    <div class="text-sm opacity-70 flex-1">The model writes one reply. Text, nothing else.</div>
  </div>
  <div class="card">
    <ph-pencil-simple-bold class="text-3xl text-blue-600 mb-3" />
    <div class="font-semibold mb-1">Apply</div>
    <div class="text-sm opacity-70 flex-1">Decides what the reply may change, then changes it.</div>
  </div>
</div>

<div class="caption mt-6">Blue is the harness. Amber is the model.</div>

**Take one apart now, build one later.**

<!--
Reworked 2026-09-13 on instructor direction; the two-column table it replaces
read as confusing. Three cards in the order a turn happens, and the middle one
is the model's whole contribution.

The two column headings of the last slide are the two blue cards. Assemble is
what goes in front of the model. Apply is what is done with the reply. Say the
three words out loud: the last slide of the taught half adds three more to
them and asks which of the six belonged to the model. One, the answer.

Every effect on their machine is a blue card acting on the amber one's text.
That is the sentence the rest of the lab depends on.

If anyone asks about models, endpoints or config: MODEL-POLICY.md, and it is
not today's subject. qwen3.5:9b recommended, 4B permitted, any compatible
endpoint.
-->

---
layout: default
---

<div class="label">What a harness is</div>

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
history spends their token budget later in the deck, and why ChatGPT seeming
to remember them, two slides back, was its harness keeping notes.

The 4B and the 9B are asked for different reply shapes, whole files against
diffs. That is why a classmate's session looks different from theirs, and why
the trace they see later may not match what they ran in practice.
Worth saying here, not worth a slide.
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
The definition, drawn for the tool in hand. Ask the room to find the arrow that
writes a file. There is not one leaving the amber box. The model produced text,
and a program decided what to do with it.

Three boxes inside the Aider band, and they are the three cards with the commit
added: assemble the request, parse and apply the reply, record it. The next
three slides are the middle box: what a reply looks like, and what the harness
has to recover from it.

This is a picture of Aider, not a required architecture for their build. They
will draw their own version of this in a week.
-->

---
layout: default
---

<div class="label">The reply</div>

# Edit-shaped replies

```text
path/to/file.py
<<<<<<< SEARCH
the lines exactly as they appear on disk
=======
the lines that replace them
>>>>>>> REPLACE
```

**One block, one file. Nothing forces the set to be complete.**

<!--
Ask what a block like this does not tell you. It names one file. A change that
needs three files needs three blocks, and nothing in the format obliges the
model to produce all three. A student who reads one well-formed block sees a
finished feature.

Nothing has changed on disk yet. This is a proposal in a chat reply.
-->

---
layout: default
---

<div class="label">The other shape</div>

# Two reply shapes, set per model {.assert}

| | whole | diff |
|---|---|---|
| The model returns | The entire file, every time | Search and replace blocks |
| Fails by | Dropping a line you never mentioned | Not matching the lines on disk |
| Costs | Every line, every edit | Only the lines that change |
| Set for | The 4B | The 9B, if you switched it |

**A harness setting, one line per model. That is why sessions differ.**

<!--
Added 2026-09-13, late, on instructor direction for more substance. The last
slide showed one shape. This is the other, and it is the one most of them have
been running: the practice settings file gives the 4B and the 9B
`edit_format: whole`, with "try: diff" on the 9B.

Whole is reliable on a small model because there is nothing to match, and
expensive because every edit resends the whole file. It fails by omission: the
model rewrites the file and quietly drops a line it was not thinking about,
which is what the L01 demo's first prompt did and nobody noticed. Diff is cheap
and fails loudly: the search text has to match the disk exactly, and when it
does not, the block is refused and the model is told so.

The bold line is the point. The shape is not a property of the model. It is
one line in a settings file the harness reads, and their build makes the same
choice when it decides what a reply has to look like.
-->

---
layout: default
---

<div class="label">The general problem</div>

# An action through a text channel

| The model returns | The harness needs |
|---|---|
| Prose | A file path |
| Prose | An exact region |
| Prose | The replacement text |

<div class="caption">Search blocks, tool-call JSON, tagged output. One problem.</div>

**Your parser is what turns a reply into an edit, or refuses to.**

<!--
Step back from the format for a moment. Whatever the model is asked to produce,
it is producing text, and the harness has to recover a machine-actionable
instruction from it. Search and replace blocks are one encoding of that. Function
calling is another. Tagged output is a third.

They all fail the same three ways: nothing parses, it parses but names something
that does not exist, or it parses and is wrong. Their error handling has to tell
those apart, because the recovery is different for each.

That is why the packet asks for match semantics and path validation as separate
requirements rather than one.
-->

---
layout: default
---

<div class="label">What Aider lacks</div>

# What Aider does not have

| Aider has no | You have seen it in |
|---|---|
| Editor around it | Cursor |
| Completions as you type | Cursor |
| Notes that outlive a session | ChatGPT, Claude Code |
| Files it went and found itself | Cursor, Claude Code |

**Every row is a harness feature. None of them is the model.**

<!--
The question under this slide is the one some of them have carried for two
weeks: why does the tool everyone talks about feel smarter than this one? Same
kind of model. What it lacks is machinery around the model, and every row here
is a decision somebody wrote code for.

Row three is worth a beat. Nothing carries between Aider sessions by default,
and nothing carries between ChatGPT or Claude Code sessions either. One
harness keeps notes for you, the other reads notes you keep, and both paste
them into the prompt. Continuity is always the harness re-sending, which is
the condition their own build runs under.

Row four is the one that matters next. Aider does not go looking for files;
they name them. The next section is about the one place it guesses, and why
that guess passed for intelligence.

Do not go past the fourth row. What happens when the model picks its next
action is tomorrow's lecture, with a live demo, and L05 opens on the question
this deck leaves open at the end of the taught half.

Their build lacks all four rows as well, by design. The packet excludes the map
and does not ask for an editor, completions or memory.
-->

---
layout: section
---

# Context

## Who decides what the model sees

<!--
Reworked 2026-09-13 on instructor direction. The section used to open on the
Aider diagram, which belongs to the harness, and the commands slide sat in
front of the section title and read as a stray. Both are where they belong
now, and the section reads as one question: for each part of the prompt, who
chose it, you or the harness.

L02 and L03 taught the window, the four sources, surgical selection and
/tokens. Do not re-teach them. The cut here is different: not what is in the
prompt but who put it there, and then the one part the harness chooses on its
own, which is the part that passed for intelligence.
-->

---
layout: default
---

<div class="label">Two choosers</div>

# Who chooses each part

| Part of the prompt | Chosen by |
|---|---|
| System prompt | Aider, by mode |
| Added and read-only files | You, by command |
| Repo map | Aider, by a ranking |
| History | You start it, Aider trims it |
| Your message | You |

**Two rows you never touched. One of them passed for intelligence.**

<!--
Same parts L03 listed, cut a different way. Read down the right-hand column
and sort the rows: yours, Aider's, shared.

Yours: the files and the message. Aider's: the system prompt, which changes
when they switch between ask and code, and the map, which they have never
typed a command for. Shared: the history, which they write one turn at a time
and Aider summarises with the weak model once it grows past a limit.

The model has no row, and two slides on says why: in Aider it can only write.
When it wants a file it can only mention the name, and Aider's regex and your
yes do the rest.

The bold line points at the next two slides. Of the two rows Aider owns, the
system prompt is dull and the map is the one that fooled them.
-->

---
layout: default
---

<div class="label">Your half</div>

# What you control

| | |
|---|---|
| Arranges context | `/add` `/read-only` `/drop` `/clear` `/tokens` |
| Changes your files | `/code` `/undo` |

<div class="caption">Bare text means <code>/code</code>. The default writes.</div>

**Most of the interface arranges context. Two commands write.**

<!--
Moved under the context section on 2026-09-13; it used to sit before the
section title. It is the human's half of the last slide, as commands.

Two commands in the whole set touch the repository, and one of those is the
undo. That asymmetry is the approval layer they are about to build, visible in
a tool they already use. Aider does not ask before it writes; their build must.

/help lists more than this and the set moves between versions. Run it live if
asked rather than reciting.
-->

---
layout: default
---

<div class="label">When the model wants a file</div>

# In Aider, the model can only write {.assert}

| | Aider | Claude Code |
|---|---|---|
| The model's verbs | Write | Read, search, edit, run |
| Wanting a file | Mentions its name in prose | Calls a read tool |
| Who lets it in | Aider spots the name, you say yes | A permission rule |
| What lands in the prompt | The file, re-read every turn | The file as it was, once |

**Everything else Aider does is an add-on around a model that only writes.**

<!--
Added 2026-09-13, late, on instructor direction: the two tools handle a file
the model wants in different ways, and the difference is worth a slide.

Start with the first row. The model in Aider has one verb. Its reply is edit
blocks, and everything else in the deck, the map, the file mention, the lint
and test loop, the shell suggestions, is machinery Aider bolts on around it to
make that one verb land better. None of it is the model deciding anything.

Row two is the one to say slowly. When Aider's model "asks for a file" it has
not asked for anything. It wrote a filename in prose, a regex in Aider found
it, Aider put "Add file to the chat?" on the screen, and a human said yes. The
model did not decide to read the file. It mentioned a name.

Claude Code's model does decide: it emits a read call and the harness runs it,
subject to a permission rule somebody configured. That is a real difference in
who chooses, and it is the closest this lab gets to tomorrow's question. Stop
at the file. How the loop continues after a read is L05.

Row four is the maintenance difference, and the middle section is about it.
Aider's copy is rebuilt from disk every turn, so it cannot go stale. Claude
Code's is a snapshot in the history, current until the file changes, and stale
after that until the model reads it again.
-->

---
layout: default
---

<div class="label">Aider's half</div>

# It knew about files you never added {.assert}

```text
package/store.py:
⋮
│class Store:
│    def add(self, title, tags=()) -> Task:
│    def remove(self, task_id: int) -> bool:
⋮
│    def search(self, text, tag=None) -> list[Task]:
⋮

package/models.py:
│@dataclass
│class Task:
⋮
```

<div class="caption mt-4">Signatures only. <code>⋮</code> is what was cut.</div>

**This is why it seemed to know your code.**

<!--
Everyone in the room has had this moment: they added one file, asked for a
change, and the reply named a class from a file they never mentioned. That was
not the model knowing the repo. It was this block, sent every turn.

Point at the vertical bars: that is aider quoting source lines. Point at the
dots: that is everything it decided not to spend tokens on. Signatures only,
no bodies, so the model can name a function it has never read.

The first session is when it looked cleverest, and there is a reason. With no
files added, Aider doubles the map's token budget, so the map is largest
exactly when they had given it nothing.

Ask what this is for. The answer is on the next slide: it is aider guessing
what you would have typed /add for.
-->

---
layout: default
---

<div class="label">Ranking</div>

# Where the repo map comes from

<div class="mt-2">
<svg viewBox="0 0 880 250" style="width:100%" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="rg" markerWidth="9" markerHeight="9" refX="8" refY="3" orient="auto" markerUnits="strokeWidth">
      <path d="M0,0 L0,6 L8,3 z" fill="#7A8099"/>
    </marker>
  </defs>

  <text x="30" y="26" text-anchor="start" style="font-family:'IBM Plex Mono',monospace;font-size:12px;fill:#7A8099">1. parse every file for what it defines and what it uses</text>
  <rect x="132" y="43" width="116" height="34" rx="17" fill="#F1EFE5" stroke="#DEDCD0"/>
  <text x="190" y="65" text-anchor="middle" style="font-family:'IBM Plex Mono',monospace;font-size:12px;fill:#1B2547">cli.py</text>
  <rect x="132" y="183" width="116" height="34" rx="17" fill="#F1EFE5" stroke="#DEDCD0"/>
  <text x="190" y="205" text-anchor="middle" style="font-family:'IBM Plex Mono',monospace;font-size:12px;fill:#1B2547">store.py</text>
  <rect x="292" y="113" width="116" height="34" rx="17" fill="#F1EFE5" stroke="#DEDCD0"/>
  <text x="350" y="135" text-anchor="middle" style="font-family:'IBM Plex Mono',monospace;font-size:12px;fill:#1B2547">models.py</text>
  <g stroke="#7A8099" stroke-width="1.3" fill="none" marker-end="url(#rg)">
    <path d="M190,77 L190,181"/>
    <path d="M240,72 L296,118"/>
    <path d="M240,188 L296,142"/>
  </g>
  <text x="200" y="133" text-anchor="start" style="font-family:'IBM Plex Mono',monospace;font-size:11px;fill:#7A8099">calls</text>
  <text x="258" y="84" text-anchor="start" style="font-family:'IBM Plex Mono',monospace;font-size:11px;fill:#7A8099">uses</text>
  <text x="258" y="186" text-anchor="start" style="font-family:'IBM Plex Mono',monospace;font-size:11px;fill:#7A8099">uses</text>
  <text x="30" y="238" text-anchor="start" style="font-family:'IBM Plex Mono',monospace;font-size:11px;fill:#7A8099">models.py is used by both, so it wins</text>

  <text x="520" y="26" text-anchor="start" style="font-family:'IBM Plex Mono',monospace;font-size:12px;fill:#7A8099">2. rank by what points at them</text>
  <text x="520" y="67" text-anchor="start" style="font-family:'IBM Plex Mono',monospace;font-size:12px;fill:#1B2547">models.py</text>
  <rect x="632" y="53" width="150" height="16" rx="2" fill="#2E5BFF"/>
  <text x="790" y="67" text-anchor="start" style="font-family:'IBM Plex Mono',monospace;font-size:11px;fill:#7A8099">0.44</text>
  <text x="520" y="111" text-anchor="start" style="font-family:'IBM Plex Mono',monospace;font-size:12px;fill:#1B2547">store.py</text>
  <rect x="632" y="97" width="112" height="16" rx="2" fill="#2E5BFF"/>
  <text x="790" y="111" text-anchor="start" style="font-family:'IBM Plex Mono',monospace;font-size:11px;fill:#7A8099">0.33</text>
  <text x="520" y="155" text-anchor="start" style="font-family:'IBM Plex Mono',monospace;font-size:12px;fill:#1B2547">cli.py</text>
  <rect x="632" y="141" width="78" height="16" rx="2" fill="#E8E6DA"/>
  <text x="790" y="155" text-anchor="start" style="font-family:'IBM Plex Mono',monospace;font-size:11px;fill:#7A8099">0.23</text>

  <line x1="512" y1="168" x2="840" y2="168" stroke="#D97706" stroke-width="1.3" stroke-dasharray="4 3"/>
  <text x="520" y="186" text-anchor="start" style="font-family:'IBM Plex Mono',monospace;font-size:11px;fill:#D97706">budget ends here</text>
  <text x="520" y="238" text-anchor="start" style="font-family:'IBM Plex Mono',monospace;font-size:11px;fill:#7A8099">cli.py is left out entirely</text>
</svg>
</div>

<div class="caption mt-2">PageRank, rendered until the budget ends.</div>

**Below the line is invisible, however relevant.**

<!--
Off the slide and worth saying: the ranking is tilted toward files you just
mentioned, and aider renders down the list until the tokens run out.

Say the ranking rule plainly: a file that lots of other files depend on scores
high, because it is probably the one you need to know about.

The dashed line is the point, and the bold line says it. It is not "here is
your repo," it is "here is as much of your repo as fits," and whatever falls
under the line is invisible to the model. The same guess that looked like
intelligence on the last slide is silent about everything below the line. 867
lines of aider to guess what you would have typed /add for.
-->

---
layout: default
---

<div class="label">Budget</div>

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

<div class="caption">One budget. Your message is what stops fitting.</div>

**Your build decides what to drop. The packet does not.**

<!--
The one context slide worth keeping, because it is the part L02 and L03 did not
show. They have seen that the window is finite and they have read /tokens. They
have not seen it fill up over a session.

Walk the two bars. Nothing about the early turn is wrong; the later turn is the
same prompt after the history has grown, and the thing that stops fitting is
their own message. Everything above it was spent before they typed.

The map is charged to this same budget, which on a 4B can be a third of the
window spent describing files the model then cannot see inside. That is why the
aider-practice cheatsheet says to turn it down, and why the map is out of scope
for the build. Say
so, so nobody spends week 4 on it.

Then the bold line, which is the whole reason this slide is still here. Ask what
they would drop first and what has to survive. Their Stage 1 contract keeps the
system instructions, the current request and the added file contents, and refuses
an oversized required input instead of silently trimming it. That refusal is a
design decision they have to write down and test, and the packet does not make it
for them.
-->

---
layout: section
---

# Maintaining the prompt

## Nothing carries over, so every part is rebuilt each turn

<!--
Reworked 2026-09-13, late, on instructor direction: the prompt's structure
and how Aider manages it, and nothing about caching. Five slides. The prompt
top to bottom. How Aider keeps each part current. Architect mode as a second
prompt built fresh. Errors written for the model. After an edit lands. The
cost slide ("Higher up is more expensive to change") was cut later the same
night; prefix reuse is one sentence in the order slide's notes now.

Gone from here: "Edit-shaped replies" and "An action through a text channel",
which now sit in the harness section where a reply belongs; "How a file update
arrives" and "What it remembers", merged into "After an edit lands"; and "The
silent undo", cut.

Open with the one sentence everything else follows from. The model keeps
nothing between turns. Turn twelve sends everything turn one sent, plus more.
That is not a limitation to work around, it is the condition their own build
runs under.
-->

---
layout: default
---

<div class="label">In order</div>

# The prompt, top to bottom

<div class="mt-2">
<svg viewBox="0 0 900 340" style="width:100%;max-height:280px" role="img"
     aria-label="The eight parts of Aider's prompt stacked top to bottom: system prompt, examples, read-only files, repo map, history, added files, your message, format reminder. The top four rarely change; the bottom four change every turn. An arrow down the side reads first token to last token.">
  <defs>
    <marker id="pr-ar" markerWidth="9" markerHeight="9" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="var(--c-ink-muted)" /></marker>
  </defs>
  <rect x="300" y="24" width="360" height="40" rx="4" fill="var(--c-bg-2)" stroke="var(--c-rule-strong)" />
  <text x="480" y="48.7" text-anchor="middle" style="font:500 13px var(--font-mono)" fill="var(--c-ink)">system prompt</text>
  <rect x="300" y="68" width="360" height="26" rx="4" fill="var(--c-bg-2)" stroke="var(--c-rule-strong)" />
  <text x="480" y="85.7" text-anchor="middle" style="font:500 13px var(--font-mono)" fill="var(--c-ink)">examples</text>
  <rect x="300" y="98" width="360" height="30" rx="4" fill="var(--c-bg-2)" stroke="var(--c-rule-strong)" />
  <text x="480" y="117.7" text-anchor="middle" style="font:500 13px var(--font-mono)" fill="var(--c-ink)">read-only files</text>
  <rect x="300" y="132" width="360" height="34" rx="4" fill="var(--c-bg-2)" stroke="var(--c-rule-strong)" />
  <text x="480" y="153.7" text-anchor="middle" style="font:500 13px var(--font-mono)" fill="var(--c-ink)">repo map</text>
  <rect x="300" y="170" width="360" height="48" rx="4" fill="var(--c-primary)" fill-opacity="0.12" stroke="var(--c-primary)" />
  <text x="480" y="198.7" text-anchor="middle" style="font:500 13px var(--font-mono)" fill="var(--c-ink)">history</text>
  <rect x="300" y="222" width="360" height="48" rx="4" fill="var(--c-primary)" fill-opacity="0.12" stroke="var(--c-primary)" />
  <text x="480" y="250.7" text-anchor="middle" style="font:500 13px var(--font-mono)" fill="var(--c-ink)">added files</text>
  <rect x="300" y="274" width="360" height="32" rx="4" fill="var(--c-primary)" fill-opacity="0.12" stroke="var(--c-primary)" />
  <text x="480" y="294.7" text-anchor="middle" style="font:500 13px var(--font-mono)" fill="var(--c-ink)">your message</text>
  <rect x="300" y="310" width="360" height="22" rx="4" fill="var(--c-primary)" fill-opacity="0.12" stroke="var(--c-primary)" />
  <text x="480" y="325.7" text-anchor="middle" style="font:500 13px var(--font-mono)" fill="var(--c-ink)">format reminder</text>
  <path d="M286,24 H280 V94 H286" fill="none" stroke="var(--c-rule-strong)" stroke-width="1.5" />
  <text x="270" y="63" text-anchor="end" style="font:500 11.5px var(--font-mono); letter-spacing:0.12em" fill="var(--c-ink-muted)">RARELY</text>
  <path d="M286,98 H280 V166 H286" fill="none" stroke="var(--c-rule-strong)" stroke-width="1.5" />
  <text x="270" y="136" text-anchor="end" style="font:500 11.5px var(--font-mono); letter-spacing:0.12em" fill="var(--c-ink-muted)">WHEN YOU ASK</text>
  <path d="M286,170 H280 V332 H286" fill="none" stroke="var(--c-rule-strong)" stroke-width="1.5" />
  <text x="270" y="255" text-anchor="end" style="font:500 11.5px var(--font-mono); letter-spacing:0.12em" fill="var(--c-ink-muted)">EVERY TURN</text>
  <line x1="700" y1="38" x2="700" y2="318" stroke="var(--c-ink-muted)" stroke-width="1.5" marker-end="url(#pr-ar)" />
  <text x="714" y="36" style="font:500 11.5px var(--font-mono); letter-spacing:0.12em" fill="var(--c-ink-muted)">FIRST TOKEN</text>
  <text x="714" y="330" style="font:500 11.5px var(--font-mono); letter-spacing:0.12em" fill="var(--c-ink-muted)">LAST TOKEN</text>
</svg>
</div>

**Stable at the top, volatile at the bottom. The order is a design decision.**

<!--
The eight parts in the order Aider sends them, read from the source. The
brackets group them by how often they change: the system prompt and its worked
examples almost never, the read-only files and the map when they ask for
something, and the bottom four every single turn.

Work the bold line rather than the parts. The parts that change every turn
were deliberately put last. One sentence on why, and no slide: a server skips
re-reading an opening it has already seen, so stable-first makes most turns
cheaper. Put the order up and let someone in the room guess that before you
say it.

Their build assembles this same thing, and the packet asks them to say what
goes in it and in what order. This slide is the argument that the answer is a
design decision rather than a detail.
-->

---
layout: default
---

<div class="label">Every turn</div>

# How Aider keeps each part current

| Part | Every turn, Aider |
|---|---|
| System prompt | Swaps it with the mode: ask, code, architect |
| Read-only files | Re-reads them from disk |
| Repo map | Re-ranks it around what you just named |
| History | Adds your message and its reply, summarises when long |
| Added files | Re-reads them from disk, whole |
| Your message | Appends a format reminder, dropped when the window is nearly full |

**Nothing is remembered. Every row is rebuilt.**

<!--
The slide the instructor asked for: not what is in the prompt, but what Aider
does to each part between one turn and the next. Every row was read out of
the 0.86.2 source.

The system prompt is chosen by mode, and ask mode also drops the worked
examples. Read-only and added files are read
from disk again on every turn, so there is exactly one copy of each and it is
current. The map is re-ranked around the filenames and identifiers in the
message just typed. The history grows by both halves of every turn and is
summarised by the weak model once it passes a token limit. And the format
reminder is stuck onto the end of the student's own message, and left out
when there is no room for it.

Ask which rows their build has. The system prompt, the files, the history and
the message. No map, and the reminder is theirs to decide. Then ask which of
those they have to re-read every turn, and why: the answer is the files, and
the reason is the last slide of this section. Next: architect mode, which
builds a second prompt out of these same parts.
-->

---
layout: default
---

<div class="label">Two prompts</div>

# Architect mode starts the editor clean {.assert}

<div class="mt-2">
<svg viewBox="0 0 900 350" style="width:100%;max-height:280px" role="img"
     aria-label="Two prompts side by side. The architect prompt is the full stack: a planning system prompt, read-only files, repo map, history, added files, your message, and its reply is a plan. The editor prompt is three parts: the edit-format system prompt, the added files, and the plan handed over as a message. No history, no map.">
  <defs>
    <marker id="ar-plan" markerWidth="9" markerHeight="9" refX="8" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="var(--c-amber)" /></marker>
  </defs>
  <text x="70" y="34" style="font:500 11.5px var(--font-mono); letter-spacing:0.12em" fill="var(--c-ink-muted)">ARCHITECT · THE MODEL YOU TALK TO</text>
  <rect x="70" y="52" width="300" height="36" rx="4" fill="var(--c-bg-2)" stroke="var(--c-rule-strong)" />
  <text x="220" y="74.5" text-anchor="middle" style="font:500 12.5px var(--font-mono)" fill="var(--c-ink)">system prompt: plan, do not edit</text>
  <rect x="70" y="92" width="300" height="26" rx="4" fill="var(--c-bg-2)" stroke="var(--c-rule-strong)" />
  <text x="220" y="109.5" text-anchor="middle" style="font:500 12.5px var(--font-mono)" fill="var(--c-ink)">read-only files</text>
  <rect x="70" y="122" width="300" height="30" rx="4" fill="var(--c-bg-2)" stroke="var(--c-rule-strong)" />
  <text x="220" y="141.5" text-anchor="middle" style="font:500 12.5px var(--font-mono)" fill="var(--c-ink)">repo map</text>
  <rect x="70" y="156" width="300" height="44" rx="4" fill="var(--c-primary)" fill-opacity="0.12" stroke="var(--c-primary)" />
  <text x="220" y="182.5" text-anchor="middle" style="font:500 12.5px var(--font-mono)" fill="var(--c-ink)">history</text>
  <rect x="70" y="204" width="300" height="44" rx="4" fill="var(--c-primary)" fill-opacity="0.12" stroke="var(--c-primary)" />
  <text x="220" y="230.5" text-anchor="middle" style="font:500 12.5px var(--font-mono)" fill="var(--c-ink)">added files</text>
  <rect x="70" y="252" width="300" height="30" rx="4" fill="var(--c-primary)" fill-opacity="0.12" stroke="var(--c-primary)" />
  <text x="220" y="271.5" text-anchor="middle" style="font:500 12.5px var(--font-mono)" fill="var(--c-ink)">your message</text>
  <rect x="70" y="294" width="300" height="34" rx="4" fill="var(--c-highlight)" stroke="var(--c-amber)" stroke-width="2" />
  <text x="220" y="315.5" text-anchor="middle" style="font:500 12.5px var(--font-mono)" fill="var(--c-ink)">its reply: a plan</text>
  <text x="530" y="34" style="font:500 11.5px var(--font-mono); letter-spacing:0.12em" fill="var(--c-ink-muted)">EDITOR · A SECOND CALL, STARTED EMPTY</text>
  <rect x="530" y="52" width="300" height="36" rx="4" fill="var(--c-bg-2)" stroke="var(--c-rule-strong)" />
  <text x="680" y="74.5" text-anchor="middle" style="font:500 12.5px var(--font-mono)" fill="var(--c-ink)">system prompt: the edit format</text>
  <rect x="530" y="92" width="300" height="44" rx="4" fill="var(--c-primary)" fill-opacity="0.12" stroke="var(--c-primary)" />
  <text x="680" y="118.5" text-anchor="middle" style="font:500 12.5px var(--font-mono)" fill="var(--c-ink)">added files</text>
  <rect x="530" y="140" width="300" height="34" rx="4" fill="var(--c-highlight)" stroke="var(--c-amber)" stroke-width="2" />
  <text x="680" y="161.5" text-anchor="middle" style="font:500 12.5px var(--font-mono)" fill="var(--c-ink)">the plan</text>
  <text x="530" y="202" style="font:400 13px var(--font-sans)" fill="var(--c-ink-soft)">no history · no map</text>
  <path d="M372,311 H450 V157 H524" fill="none" stroke="var(--c-amber)" stroke-width="2" marker-end="url(#ar-plan)" />
  <text x="460" y="324" style="font:400 13px var(--font-sans)" fill="var(--c-ink-soft)">handed over as a message</text>
</svg>
</div>

**Two prompts. The second is built fresh: the files and the plan, nothing else.**

<!--
Added 2026-09-13, late, on instructor direction. They used this in lesson 6
and the lesson said it was two model calls. This is what the two prompts hold,
built out of the same parts as the last two slides.

From the source: when the plan is accepted, Aider creates a second coder with
empty history, no repo map, the edit-format system prompt, and the plan as its
only user message. The editor sees the files and the plan. Nothing else. The
architect's own prompt is the full stack, and it stays in one mode for the
whole conversation, so its system prompt never swaps.

Say why it is built that way. A long prompt full of history is a good prompt
for deciding what to do and a bad one for producing an exact edit. Splitting
the job gives each call the prompt it needs: the whole picture for the plan,
a short focused one for the edit. That is the reason architect mode scores
better on small models, and it is a structure decision, not a model feature.

`auto-accept-architect: false` in the practice repo is why it stopped to ask
before the second call. Their build could do the same in an increment: plan
with the full context, edit with a small one.
-->

---
layout: default
---

<div class="label">Failure as input</div>

# Errors written for the model

Aider answers the model, not you.

- The failed block, quoted back
- Lines from the file that nearly match
- A note if the work already exists

**An error message is a prompt.**

<!--
When a block fails to apply, what comes back is not a message for the human. It
is written to be read by the model on the next turn: here is your block, here
are the lines it almost matched, and if the replacement text is already in the
file, a question asking whether the block was needed at all.

That reframing is worth the slide on its own. In a system whose only actuator is
text, an error message is another prompt, and its job is to make the next attempt
better rather than to describe what went wrong.

Aider will do this up to three times before giving up. Their build does not have
to retry at all, but it does have to decide, and the packet scores the failure
paths.
-->

---
layout: default
---

<div class="label">Grounding</div>

# After an edit lands

<div class="mt-2">
<svg viewBox="0 0 900 340" style="width:100%;max-height:280px" role="img"
     aria-label="The prompt stack with two parts called out. History is kept word for word, so it still holds the model's own reply quoting the old lines. Added files are rebuilt from disk every turn, so they hold the current text with no diff and no old copy.">
  <rect x="80" y="24" width="300" height="40" rx="4" fill="var(--c-bg-2)" stroke="var(--c-rule-strong)" />
  <text x="230" y="48.7" text-anchor="middle" style="font:500 13px var(--font-mono)" fill="var(--c-ink)">system prompt</text>
  <rect x="80" y="68" width="300" height="26" rx="4" fill="var(--c-bg-2)" stroke="var(--c-rule-strong)" />
  <text x="230" y="85.7" text-anchor="middle" style="font:500 13px var(--font-mono)" fill="var(--c-ink)">examples</text>
  <rect x="80" y="98" width="300" height="30" rx="4" fill="var(--c-bg-2)" stroke="var(--c-rule-strong)" />
  <text x="230" y="117.7" text-anchor="middle" style="font:500 13px var(--font-mono)" fill="var(--c-ink)">read-only files</text>
  <rect x="80" y="132" width="300" height="34" rx="4" fill="var(--c-bg-2)" stroke="var(--c-rule-strong)" />
  <text x="230" y="153.7" text-anchor="middle" style="font:500 13px var(--font-mono)" fill="var(--c-ink)">repo map</text>
  <rect x="80" y="170" width="300" height="48" rx="4" fill="var(--c-highlight)" stroke="var(--c-amber)" stroke-width="2" />
  <text x="230" y="198.7" text-anchor="middle" style="font:500 13px var(--font-mono)" fill="var(--c-ink)">history</text>
  <rect x="80" y="222" width="300" height="48" rx="4" fill="var(--c-primary)" fill-opacity="0.12" stroke="var(--c-primary)" />
  <text x="230" y="250.7" text-anchor="middle" style="font:500 13px var(--font-mono)" fill="var(--c-ink)">added files</text>
  <rect x="80" y="274" width="300" height="32" rx="4" fill="var(--c-bg-2)" stroke="var(--c-rule-strong)" />
  <text x="230" y="294.7" text-anchor="middle" style="font:500 13px var(--font-mono)" fill="var(--c-ink)">your message</text>
  <rect x="80" y="310" width="300" height="22" rx="4" fill="var(--c-bg-2)" stroke="var(--c-rule-strong)" />
  <text x="230" y="325.7" text-anchor="middle" style="font:500 13px var(--font-mono)" fill="var(--c-ink)">format reminder</text>
  <line x1="382" y1="194" x2="420" y2="194" stroke="var(--c-amber)" stroke-width="2" />
  <text x="430" y="190" style="font:600 14px var(--font-sans)" fill="var(--c-ink)">Kept word for word</text>
  <text x="430" y="210" style="font:400 13px var(--font-sans)" fill="var(--c-ink-soft)">its own reply is still here, quoting the old lines</text>
  <line x1="382" y1="246" x2="420" y2="246" stroke="var(--c-primary)" stroke-width="2" />
  <text x="430" y="242" style="font:600 14px var(--font-sans)" fill="var(--c-ink)">Rebuilt from disk, every turn</text>
  <text x="430" y="262" style="font:400 13px var(--font-sans)" fill="var(--c-ink-soft)">the current text, no diff, no old copy</text>
</svg>
</div>

**Never told what changed. Shown what is true now, and left with what it quoted.**

<!--
Merged 2026-09-13, late, from "How a file update arrives" and "What it
remembers", which the instructor found hard to present as two slides. Same
stack as the rest of the section, two parts called out.

The question once they understand the prompt is rebuilt: after an edit lands,
is the model told, or does the text change under it? Both, and the second
matters more.

The file block is rebuilt from disk, so there is one copy of each file and it
is current. No diff is ever sent and no old copy is kept. Aider also adds one
line to the history, in the student's voice, saying it committed with a given
hash. That is all the model is told.

The history is the other half. The model's own replies stay word for word, and
they are full of edit blocks quoting the old text. So its record of the
previous version is exactly the lines it chose to change and nothing around
them, a biased sample of the past. That is why Aider's own prompt warns the
model that other messages may hold outdated contents. It cannot fix that, only
warn.

Two consequences worth saying. A file they edit themselves in another window
is picked up next turn with no announcement. And /undo on the course models
tells the model nothing, so its history still holds the edit it proposed and
the file no longer does. The silent undo slide came off the deck tonight; the
fact stays here, and it is why their specification requires undo to be an
owned, current-session operation on a clean target.
-->

---
layout: section
---

# Hackathon 1

## One feature on your own build, in one evening

<!--
Section slide added 2026-09-14 at the instructor's request, so the hackathon
reads as its own block rather than a tail on the grounding slides. Two slides
under it: the format, and the workspace. Three or four minutes in total.
-->

---
layout: default
---

<div class="label">Thursday September 24</div>

# The format

- Two hours, your own project
- Prompt revealed in the room
- Submit before you leave
- Graded separately from the build

<!--
Three minutes including logistics. Room, time and the model in the workspace are
announced by staff. Do not invent any of them here.

Say the accommodations line out loud: conflicts and accommodations go to staff
now, not the week of.

This slide carries the hackathon date and nothing else. The build deadline is on
the project slide, which is the only place a student should look for it.
-->

---
layout: default
---

<div class="label">Hackathon 1</div>

# The hackathon workspace

- Browser VS Code, already set up
- Aider pointed at the course endpoint
- Your repository already cloned
- A Python reference pack, offline

<!--
The caption with the token figures and the closing line about bringing a build
that runs both came off this slide on 2026-09-14 at the instructor's request.
Both points are still worth saying; they are yours to say, not the slide's.


Nobody installs anything and nobody needs the network. The workspace opens with
the tools already pointed at the right place and their own repository in it.

The caption is the point of the slide and it connects straight back to the
budget block. The reference pack in the image is most of the Python
documentation, converted so a model can read it, and it is roughly eighty times
any context window in the room. It is split into parts small enough to add one
at a time.

So the exercise is not whether the documentation is available. It is which
pages, and choosing well is the difference between finishing and not. That is
the context budget with a grade attached.

Announce the room, the start time and the makeup path from the current staff
announcement. Do not invent any of them here.

**The weight slide was cut on 2026-09-13 and the number is yours to say or not.**
For the record: hackathon 1 is 10 of the 20 Apply parts, so half the Apply grade
against a quarter for the build and a quarter for the practice lessons. It is
not on the glass any more.

The bold line is the preparation instruction and it is the one thing here that
changes what they do tonight. The prompt asks for one feature on their own code,
revealed in the room, so a repository that does not run cannot be started on.
Anyone mid-refactor that evening has a much worse two hours.
-->

---
layout: section
---

# The pair-programmer

## What Stage 1 asks for

<!--
The reveal. They have spent two weeks driving a harness and the last hour
taking one apart; now they build one.

Lead with what the thing is, not with the paperwork. The packet carries the
requirements and they can read it.
-->

---
layout: default
---

<div class="label">Stage 1 · the project</div>

# A harness from scratch

Everything in the last hour, written by you.

| | |
|---|---|
| It holds | A set of files you chose |
| It asks | A model endpoint you configure |
| It writes | Only after you approve |

<div class="caption">Aider without Aider. Same job, your code.</div>

<div class="caption">Due <strong>Tuesday October 6, 11:59 PM</strong>.</div>

<!--
Say the one-sentence version out loud: a terminal pair-programmer over files
you select, talking to an endpoint you configure, that never edits without
asking. Everything else in the packet is detail under that sentence.

It is not a clone of Aider and it does not need to be. No repo map, no lint
loop, no architect mode. What it must have is the spine they just watched.

If somebody asks how big it is: smaller than they fear, and the specification
work is the part that decides how long it takes.

The date under the caption is the only place in the deck a student sees the
build deadline. Say it out loud rather than skipping past it.
-->

---
layout: default
---

<div class="label">Stage 1 · how it runs</div>

# Specification before implementation

You write the requirements before you write the code, and the commit history
has to show it.

| What you write | When | Covers |
|---|---|---|
| System design | Once, before implementation | Config, run contract, seven features |
| Three diagrams | With the design | Components, sequence, edit lifecycle |
| Increment specs | One before each slice you choose | Ordered, testable, context scoped |

<div class="caption">No specification is supplied.</div>

<!--
This is the whole shape of Stage 1 and the thing most of them will get wrong by
starting with code. Nobody hands them a specification: they write their own
requirements, their own acceptance criteria, and their own increments.

The history is evidence, not bureaucracy. A design committed after the code it
describes earns nothing, and they cannot reconstruct it at the end.

Row by row. The requirements have to cover the configuration and execution
contracts as well as the seven features, with observable outcomes, edge cases
and exclusions, and each one has to trace to an acceptance criterion of their
own. The diagrams describe their system, not Aider: copying this morning's
picture earns nothing, Mermaid is enough, and labels have to be legible and
accurate. There is no length requirement anywhere in this section.

An increment is not a commit and not a single change. It is a sizeable slice of
the build that they break out and define themselves, with an observable result,
its own scoped context and its own ordered tasks. Closest thing they have met is
an aider-practice lesson, except that here they write the lesson.

They choose how many there are and where the boundaries fall. The packet is
explicit about that and the rubric scores whether the set covers the whole build
in a sensible order, not whether there are many of them.
-->

---
layout: default
---

<div class="label">Grading</div>

# Specification and design

**50 of the 100 build points.**

| Criterion | Points |
|---|---:|
| Requirements and acceptance criteria | 10 |
| Architecture and interface design | 10 |
| Increment specs | 10 |
| The three diagrams | 4 / 3 / 3 |
| Specs before code | 5 |
| What changed and why | 5 |

<!--
Do not read the table out. The one thing worth saying: a part they designed and
did not implement keeps its design credit as long as it is labelled.

Architecture credit includes explaining where tool execution, a replacement
endpoint client and a non-terminal interface would fit, without building them.

The last two rows are read from git history rather than from a document. Specs
before code is scored on commit order, and what changed and why is the
reconciliation between the design they started with and the system they
finished. A design that worked does not need an invented failure.
-->

---
layout: default
---

<div class="label">Grading</div>

# Implementation and tests

**50 of the 100 build points.**

| Criterion | Points |
|---|---:|
| Functional correctness | 25 |
| Custom test cases | 9 |
| Failure-path tests | 8 |
| End-to-end runs and live evidence | 5 |
| Operating instructions | 3 |

<div class="caption"><code>RUBRIC.md</code> carries every row.</div>

<!--
100 points across two sections of 50. These are build points, not course-grade
percentages: the build is 4.5% of the course.

Functional correctness is the seven features, scored one row each in RUBRIC.md.
Half credit exists for behavior that partly works, so an unfinished feature is
not a zero.

Test count and coverage earn nothing by themselves. A test earns credit when it
asserts an outcome and isolates the filesystem. Weakening an assertion to turn
the suite green is scored as what it is.

Configuration sits inside F1's five points and is not a gate.

Staff read the repository snapshot at the deadline, run their own tests, and
work through ACCEPTANCE.md. There is no hidden suite and no requirement that is
not in SPEC.md. Routine tests use fakes rather than a live model; live checks
are documented separately and opt in, and an honestly reported failed live
attempt still earns its evidence points.

Send them to RUBRIC.md rather than reading rows aloud. It names the requirement
IDs each row scores.
-->

---
layout: default
---

<div class="label">What you keep</div>

# The evidence trail

| | |
|---|---|
| Commits | Specs before the code they describe |
| Sessions | Which context, which model, what happened |
| Reconciliation | Where the design changed, and why |

<!--
None of this can be reconstructed the night before, which is why it is worth a
minute here. Commits and reconciliation are the last two scored rows on the
specification slide.

Sessions and model disclosure are required but score no points of their own.
They are what lets staff follow the rest of the evidence, so a submission
without them loses credit wherever a claim cannot be checked.
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
layout: section
---

# Autonomy, and where your harness goes

## Harnesses got better. You will build that yourself.

<!--
Rewritten 2026-09-15 on instructor direction. The old opening of this section
argued for Aider and for the weak models, and both arguments had already been
made in L01 to L04, so those three slides are gone: "This is where the field
started", "Aider is good to learn on" and "The models are weak on purpose".
The section now opens on autonomy: what a harness decides, how much of that
the model has been handed since 2023, and the fact that this course reaches
those milestones in one repository. The three slides after that were kept and
tightened.

Five slides. What a harness decides, and who got to decide it in 2023 against
2025. The three milestones, M1 to M3, built here in order. One repository
to December. You will know how Claude Code works. The same loop with more
machinery, ending on what is left for L05.

Each slide's notes end with a "Next:" line saying what the following slide
carries, so nothing gets said a slide early.
-->

---
layout: default
---

<div class="label">Autonomy</div>

# Autonomy is decisions handed to the model {.assert}

| The harness decides | 2023, Aider | 2025, an agentic CLI |
|---|---|---|
| What the model sees | You, with `/add` | The model asks, and reads it |
| What happens to a reply | An edit, shown to you first | A tool call, checked against a rule |
| What comes next | You type the next request | The model picks the next action |
| What survives the session | Nothing | Notes, memory, a run it can resume |

**The model call did not change shape. Everything around it did.**

<!--
Every row is a decision the harness makes, and the two columns are who it lets
make it. Read the middle column first: in Aider they made every one of these
themselves for two weeks, and the model's contribution was one block of text.
Then the right column: the same four decisions, and at each one the harness
now lets the model choose and checks the choice against a rule.

That is what "more autonomous" means, and it is where the complexity and the
power of a 2025 harness live. The model on the right is often the same model
as on the left. What changed is how much of its own turn it gets to decide.

Do not say how a harness lets the model pick the next action, or what that
costs. L05 spends ninety minutes on exactly that, with a live demo.

Next: the milestones, M1 to M3, built here in order.
-->

---
layout: default
---

<div class="label">Milestones</div>

# Project milestones

| Milestone | Who takes the step | When you build it |
|---|---|---|
| M1. Pair-programmer | You choose the files and approve the edit; the model writes | Apply, starting this week |
| M2. Agent | The model picks the next action; a rule you wrote approves it | Analyze |
| M3. Assistant | It keeps state between runs and survives real work | Create |

**A bigger model buys none of this. Every milestone is harness you wrote.**

<!--
The three milestones are the three phases, and the order is the order harnesses
grew in. M1 is the build they are reading about this week: they choose
what the model sees, and nothing touches disk until they say yes. M2 moves
one decision, the next action, from them to the model, and the price of that
move is an approval layer they have to write. M3 is what makes it usable
day after day: memory, hardening, more than one way in.

The bold line is the design of the course. The model does not grow between
now and December, so nothing they gain in autonomy comes from a bigger model.
It comes from harness code in their own repository. That is also why the
model is one config line and the harness is the product.

Next: the same three milestones as a timeline, with what each adds in code. Do
not walk the phases here; the next slide does.
-->

---
layout: default
---

<div class="label">Through December</div>

# One repository to December

<div class="mt-4">
<svg viewBox="0 0 900 150" style="width:100%;max-height:180px" role="img"
     aria-label="A timeline with three phases: Apply is M1, one loop with exact edits and git; Analyze is M2, the model picks its tools; Create is M3, memory, hardening and another way in.">
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
    <text x="170" y="102">M1: one loop, exact edits, git</text>
    <text x="450" y="102">M2: the model picks its tools</text>
    <text x="730" y="102">M3: memory, hardening, another way in</text>
  </g>
</svg>
</div>

**Nothing is thrown away. Each phase grows the last.**

<!--
Walk the timeline left to right and say what each dot adds in code: M1 is
the loop, exact edits and git they build this month; M2 is tools the model
chooses and the approval layer that gates them; M3 is state that survives
a run, hardening, and another way in.

Build advice that used to sit on this slide and still belongs in the room: one
small checkable result first, and keep the phase snapshots.

The 2023-against-2025 table two slides back is as far as the tool comparison
goes in this lab. L05 has the live demo; do not reconstruct it here.

Do not estimate the workload out loud. Do say that a runnable slice early is
what keeps the December integration from being a surprise.

Next: the destination, named. Do not say Claude Code on this slide. The dots
are Apply, Analyze and Create, and the next slide says what they add up to.
-->

---
layout: default
---

<div class="label">The destination</div>

# You will know how Claude Code works {.assert}

By December: an M3 harness in the shape of Claude Code, grown from the
M1 pair-programmer you start this week.

| Using it | Knowing it |
|---|---|
| Approve a permission prompt | Write the rule it enforces |
| Watch it find the file | Write the search that found it |
| Type, and the file changes | Write the parser that changed it |

**Everyone else will use it. You will have written each layer.**

<!--
Merged 2026-09-13, late, from "You will know how Claude Code works" and "The
harness by December", on the instructor's reading that he was saying this
slide's content a section early. There is now one place in the deck that
names the destination, and it is here.

The lead line first. Name Claude Code, or OpenClaw, as a shape, not a target
to clone and not something they need an account for. What makes it that shape
is the list they will build: tools the model chooses, an approval layer, state
that survives a run, more than one way in. The design habit to start now: when
a decision could close off one of those, leave a boundary rather than an
implementation.

Then the table. Say the left column as what a user sees and the right column
as what a builder knows. Each row is a moment they will recognise from using
the tool, paired with the code in their own repository that does the same job:
the loop this month, the tools and the permission gate in Analyze, memory and
hardening in Create.

Nobody needs a subscription for anything in this course.

Next: the open question. Do not say who picks the next action here.
-->

---
layout: default
---

<div class="label">Every tool you will meet</div>

# The same loop, more machinery

- Assemble, answer, parse, apply, repair, commit
- Every tool you will meet runs it
- What differs is who takes each step

**Left for L05: how the model gets to pick the next action, and what it costs.**

<!--
The bridge, and the end of the taught half. Six steps, and today they followed
one request through all of them. Every tool of this kind, whatever its name and
whoever makes it, runs the same six.

Ask the room which of the six belonged to the model in their own sessions.
One: the answer. At every other step the thing that decided what happened
next was them, or a rule somebody wrote down in advance.

Then leave the bold line up. The autonomy slide already said that at M2
the model picks the next action. What this deck has not said is how a harness
makes that possible and what it costs, and L05 opens on exactly that with a
live demo. Saying more here spoils it.

This is the last slide before office hours. Leave the line up.
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
