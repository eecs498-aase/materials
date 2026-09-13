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
layout: section
---

# Context

## What the harness sends, and what comes back

<!--
This block is now about context rather than a walkthrough of a whole turn
(instructor cuts 2026-09-13). Most of it is the repo map, because that is the
part nobody has met before and the part that quietly spends their budget.

Say up front that only the reply belongs to the model. Everything else in this
block is the harness deciding what the model gets to see.
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

<div class="label">The request</div>

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

Ask what the model would need in order to change three files consistently, when
nothing has told it which three. That question sets up the repo map.

The /add slide was cut on 2026-09-13 because they have been doing this for two
weeks. Two things it carried, worth saying if anyone asks rather than putting
back on the glass: added files can be rewritten while read-only files can only
be cited, and adding the whole package is not a selection strategy, it is a way
to spend the budget.
-->

---

<div class="label">Repository map</div>

# The repo map

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

**Files you never added.**

<!--
Point at the vertical bars: that is aider quoting source lines. Point at the
dots: that is everything it decided not to spend tokens on.
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

<!--
Off the slide and worth saying: the ranking is tilted toward files you just
mentioned, and aider renders down the list until the tokens run out.

Say the ranking rule plainly: a file that lots of other files depend on scores
high, because it is probably the one you need to know about.
The dashed line is the point. It is not "here is your repo," it is "here is as
much of your repo as fits," and whatever falls under the line is invisible to
the model. 867 lines of aider to guess what you would have typed /add for.
-->

---
layout: default
---

<div class="label">Cost</div>

# What the map costs

<div class="mt-2">
<svg viewBox="0 0 880 230" style="width:100%" xmlns="http://www.w3.org/2000/svg">
  <text x="30" y="22" text-anchor="start" style="font-family:'IBM Plex Mono',monospace;font-size:12px;fill:#7A8099">repo map on</text>
  <rect x="30" y="32" width="60" height="46" fill="#DEDCD0" stroke="#CFCCBE"/>
  <text x="60.0" y="60" text-anchor="middle" style="font-family:'IBM Plex Mono',monospace;font-size:12px;fill:#1B2547">system</text>
  <rect x="90" y="32" width="92" height="46" fill="#DEDCD0" stroke="#CFCCBE"/>
  <text x="136.0" y="60" text-anchor="middle" style="font-family:'IBM Plex Mono',monospace;font-size:12px;fill:#1B2547">examples</text>
  <rect x="182" y="32" width="232" height="46" fill="#FFE9C7" stroke="#D97706"/>
  <text x="298.0" y="60" text-anchor="middle" style="font-family:'IBM Plex Mono',monospace;font-size:12px;fill:#1B2547">repo map</text>
  <rect x="414" y="32" width="286" height="46" fill="#2E5BFF" stroke="#2E5BFF"/>
  <text x="557.0" y="60" text-anchor="middle" style="font-family:'IBM Plex Mono',monospace;font-size:12px;fill:#FBFAF5">your files</text>
  <rect x="700" y="32" width="72" height="46" fill="#DEDCD0" stroke="#CFCCBE"/>
  <text x="736.0" y="60" text-anchor="middle" style="font-family:'IBM Plex Mono',monospace;font-size:12px;fill:#1B2547">turn</text>
  <rect x="772" y="32" width="48" height="46" fill="#DEDCD0" stroke="#CFCCBE"/>

  <text x="30" y="118" text-anchor="start" style="font-family:'IBM Plex Mono',monospace;font-size:12px;fill:#7A8099">repo map off</text>
  <rect x="30" y="128" width="60" height="46" fill="#DEDCD0" stroke="#CFCCBE"/>
  <text x="60.0" y="156" text-anchor="middle" style="font-family:'IBM Plex Mono',monospace;font-size:12px;fill:#1B2547">system</text>
  <rect x="90" y="128" width="92" height="46" fill="#DEDCD0" stroke="#CFCCBE"/>
  <text x="136.0" y="156" text-anchor="middle" style="font-family:'IBM Plex Mono',monospace;font-size:12px;fill:#1B2547">examples</text>
  <rect x="182" y="128" width="518" height="46" fill="#2E5BFF" stroke="#2E5BFF"/>
  <text x="441.0" y="156" text-anchor="middle" style="font-family:'IBM Plex Mono',monospace;font-size:12px;fill:#FBFAF5">your files</text>
  <rect x="700" y="128" width="72" height="46" fill="#DEDCD0" stroke="#CFCCBE"/>
  <text x="736.0" y="156" text-anchor="middle" style="font-family:'IBM Plex Mono',monospace;font-size:12px;fill:#1B2547">turn</text>
  <rect x="772" y="128" width="48" height="46" fill="#DEDCD0" stroke="#CFCCBE"/>

  <line x1="30" y1="196" x2="820" y2="196" stroke="#DEDCD0" stroke-width="1"/>
  <text x="30" y="216" text-anchor="start" style="font-family:'IBM Plex Mono',monospace;font-size:11px;fill:#7A8099">0</text>
  <text x="820" y="216" text-anchor="end" style="font-family:'IBM Plex Mono',monospace;font-size:11px;fill:#7A8099">the whole context window</text>
</svg>
</div>

<div class="caption mt-2">Same window either way.</div>

**On a small model the map can outweigh the files.**

<!--
Off the slide: on a small model the map often costs more than the files it was
guessing about.

This is why aider-practice turns it down. On a 4B with a small window the map
can eat a third of the budget to describe files the model then cannot see the
insides of anyway.
It is out of scope for the build. Say so here, so nobody spends week 4 on it.
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

<div class="label">Thursday September 24</div>

# Hackathon 1

- Two hours, your own project
- Prompt revealed in the room
- Submit before you leave
- Graded separately from the build


<div class="caption">Build due <strong>Tuesday September 29, 11:59 PM</strong>.</div>

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

# The pair-programmer

## What Stage 1 asks for

<!--
Minutes 40 to 58. This is the reveal. They have spent two weeks driving a
harness and the last half hour taking one apart; now they build one.

Lead with what the thing is, not with the paperwork. The packet carries the
requirements and they can read it.
-->

---
layout: default
---

<div class="label">Stage 1 · the project</div>

# A harness from scratch

Everything in the last half hour, written by you.

| | |
|---|---|
| It holds | A set of files you chose |
| It asks | A model endpoint you configure |
| It writes | Only after you approve |

<div class="caption">Aider without Aider. Same job, your code.</div>

<!--
Say the one-sentence version out loud: a terminal pair-programmer over files
you select, talking to an endpoint you configure, that never edits without
asking. Everything else in the packet is detail under that sentence.

It is not a clone of Aider and it does not need to be. No repo map, no lint
loop, no architect mode. What it must have is the spine they just watched.

If somebody asks how big it is: smaller than they fear, and the specification
work is the part that decides how long it takes.
-->

---
layout: default
---

<div class="label">Stage 1 · how it runs</div>

# Specification before implementation

You write the requirements before you write the code, and the commit history
has to show it.

| | |
|---|---|
| System design | Once, before implementation |
| Increment specs | One per change, before it |

<div class="caption">No specification is supplied.</div>

<!--
This is the whole shape of Stage 1 and the thing most of them will get wrong by
starting with code. Nobody hands them a specification: they write their own
requirements, their own acceptance criteria, and their own increments.

The history is evidence, not bureaucracy. A design committed after the code it
describes earns nothing, and they cannot reconstruct it at the end.

Increment specs are what an Aider session can actually execute: scoped context,
ordered tasks, a checkable result.
-->

---
layout: default
---

<div class="label">What you write</div>

# The design artifacts

| Artifact | Covers |
|---|---|
| Your requirements | Config, run contract, seven features |
| Increment specs | Ordered, testable, context scoped |
| Three diagrams | Components, sequence, edit lifecycle |

<!--
Their requirements have to cover the configuration and execution contracts as
well as the seven features, with observable outcomes, edge cases and exclusions,
and each one has to trace to an acceptance criterion of their own.

The diagrams describe their system, not Aider. Copying this morning's picture
earns nothing. Mermaid is enough, labels have to be legible and accurate, and
there is no length requirement anywhere in this section.
-->

---
layout: default
---

<div class="label">Grading · 50 points</div>

# Specification and design

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

<div class="label">Grading · 50 points</div>

# Implementation and tests

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

# What comes next

## One repository, grown until December

<!--
Minutes 58 to 65. Short. The point is the arc, not a tour of tools.

Nothing here is a Stage 1 dependency and no subscription is needed for this
course.
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

**Nothing is thrown away. Each phase grows the last.**

<!--
Walk the timeline left to right and say what changes at each dot: first the
human is in the loop, then the model picks the tools, then it keeps state and
survives contact with real work.

Build advice that used to sit on this slide and still belongs in the room: one
small checkable result first, and keep the phase snapshots.

Do not estimate the workload out loud. Do say that a runnable slice early is
what keeps the December integration from being a surprise.
-->

---
layout: default
---

<div class="label">Where this is going</div>

# What an agentic CLI adds

| Aider | An agentic CLI |
|---|---|
| You frame a bounded task | You hand over a broad one |
| You select the files | It discovers them |
| A fixed sequence of steps | The model picks the next tool |
| You check between tasks | Permissions bound it |

<!--
Do not turn the left column into a weakness. Aider automates plenty. What
changes on the right is who decides the next action.

Source: https://code.claude.com/docs/en/overview
-->

---
layout: default
---

<div class="label">By December</div>

# The harness by December

You will have built the kind of tool this lab took apart: a coding agent in the
shape of Claude Code or OpenClaw, running against a model you configure, grown
from the pair-programmer you start on Monday.

**Today you drive one. In December you will have written one.**

<!--
This is the last thing they hear before office hours, so land it and stop.

Name the two tools as a shape, not as a target to clone and not as something
they need an account for. What makes it that shape is the list they will build:
tools the model chooses, an approval layer, state that survives a run, more
than one way in.

The design habit to start now: when a decision could close off one of those,
leave a boundary rather than an implementation. That is the useful half of the
slide this replaced.
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
