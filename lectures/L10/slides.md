---
theme: ../theme
title: "L10: Skills and the Elephant-Goldfish Model"
info: |
  EECS 498 AASE — Lecture 10
  Applied Agentic Software Engineering, UMich Fall 2026
layout: title
class: text-left
transition: fade
mdc: true
highlighter: shiki
---

# Skills and the Elephant-Goldfish Model

## Lecture 10 · Oct 1, 2026

<!--
Good afternoon.

A change from the schedule you saw last week. Today was going to be serving a local model. It is skills and the Elephant-Goldfish Model instead, which is why you got a reading last night. Serving a local model has not gone away; where it lands is coming with the rest of the plan for the next few weeks.

Today has no live demo and nothing to install. Everything on the glass is a file you can open, and the skills themselves are in the materials repo now.

Direction: No live demo today. Every number on the glass comes from the instructor's EGM skill
files as of Oct 1 and from docs/egm in the course workspace, so nothing depends on a model behaving.
-->

---
layout: default
---

<div class="label">Today</div>

# Two parts

1. Skills
2. The Elephant-Goldfish Model

<div class="caption mt-6">Reading: Rensin, "Elephants, Goldfish, and the New Golden Age of Software Engineering"</div>

<!--
Two parts today. Skills, which are a way of packaging method so an agent can pick it up when it needs it. And the Elephant-Goldfish Model, a design method you will be handed as a set of skills.

You were sent Dave Rensin's article last night.

*[Ask: Hands up if you read it. Hands up if you got to the part about the goldfish.]*

Either way is fine. The second half covers what you need from it. If you read it, listen for the places where my implementation made a choice the article leaves open.
-->

---
layout: default
---

<div class="label">Lab01, L05, L07</div>

# Assemble, answer, apply

<div class="grid grid-cols-3 gap-6 mt-8 items-stretch">
  <div class="card">
    <ph-stack-bold class="text-3xl text-amber-600 mb-3" />
    <div class="font-semibold mb-1">Assemble</div>
    <div class="text-sm opacity-70 flex-1">Every word the model sees</div>
  </div>
  <div class="card">
    <ph-chat-text-bold class="text-3xl text-blue-600 mb-3" />
    <div class="font-semibold mb-1">Answer</div>
    <div class="text-sm opacity-70 flex-1">Text out, nothing more</div>
  </div>
  <div class="card">
    <ph-pencil-simple-bold class="text-3xl text-blue-600 mb-3" />
    <div class="font-semibold mb-1">Apply</div>
    <div class="text-sm opacity-70 flex-1">The harness acts on it</div>
  </div>
</div>

<div class="caption mt-8">Today lives in the first card.</div>

<!--
You have drawn this three times now. Lab01, L05, and L07 at the level of bytes. A harness assembles a request, the model answers with text, the harness applies it.

Everything today happens in the first card. A skill is a decision about what goes into the assembled request, and when. The Elephant-Goldfish Model is, underneath, a decision about what a session gets to see. Keep the cards in mind. The chat break asks you to put skills into the first one.
-->

---
layout: section
---

# Skills

## Method the agent loads when it needs it

<!--
First part. Skills.

About fifteen minutes. What a skill is on disk, what is inside the one required file, how it differs from a tool, and what it costs to give an agent too many of them. Hold on to the cost. It is the chat break.
-->

---
layout: default
---

<div class="label">Definition</div>

# What a skill is

A folder an agent loads when a task needs it.

- **Instructions** - SKILL.md, always
- **Resources** - files it may read
- **Scripts** - code it may run

<div class="caption mt-6">Written for a model to read, not for a program to call.</div>

<!--
Here is the definition. A skill is a folder that an agent loads when a task needs it. That is all.

Inside the folder are up to three kinds of thing. Instructions, which live in a file called SKILL.md, and every skill has one. Resources, which are files the instructions may send the model to read: a template, a checklist, a longer explanation. And scripts, code the agent may run when a step should come out the same every time.

The caption is the part to hold on to. Everything in a skill is written for a model to read. There is no API, no function signature. The audience for a skill is the model, the same way the audience for a README is the next engineer.
-->

---
layout: default
---

<div class="label">The format</div>

# A skill on disk

```text
elephant/
├── SKILL.md                       required
├── references/
│   └── design-doc-sections.md     read on demand
├── assets/
│   ├── design-doc-template.md     copied into output
│   └── elephant-ledger-template.md
└── evals/
    └── trigger-evals.json         tests the description
```

<div class="caption mt-6">The instructor's elephant skill. No scripts/ here. Lives in .claude/skills/ or .agents/skills/.</div>

<!--
This is the real elephant skill, as it stands today. A folder named for the skill. One required file inside it, SKILL.md. The top of that file is a few lines of YAML frontmatter, and the rest is instructions written in Markdown, for a model to read.

Everything else is optional, and the folder names are conventions. references holds material the model reads only when SKILL.md tells it to; here, a page on what each section of a design doc should contain and how each one goes wrong. assets holds files the skill uses in its output rather than reads for guidance; here, the blank design doc and the blank ledger it copies. evals holds twelve requests, six that should load the skill and six near misses that should not, which is how you test a description. A scripts folder would hold code the agent runs rather than reads. Elephant has none, because nothing in a design conversation should be deterministic, but three of the other EGM skills do.

Where the folder lives decides who can use it. Claude Code looks in .claude/skills, in your home directory for personal skills or in the project for shared ones. Codex looks in .agents/skills.

There is no runtime, no registry, no SDK. If you can write a README you can write a skill. That is a large part of why they spread.
-->

---
layout: default
---

<div class="label">The top of SKILL.md</div>

# The frontmatter

```yaml
name: elephant
description: Runs a no-code design conversation for a new
  feature, refactor, or system change, then writes the
  four-section design doc that becomes the source of truth.
  Use when the user says "design a feature", "let's plan X",
  "spec this out", or otherwise opens a non-trivial design
  problem, even if they did not ask for a document.
  Hand the finished doc to /goldfish. Not for one-line
  fixes or questions about how existing code works.
```

<div class="caption mt-4">The instructor's elephant skill, trimmed.</div>

<!--
Here is the top of a real one, the elephant skill you will meet in the second half. Two fields matter. name, which is also how you call it by hand with a slash. And description.

Read the description the way the model reads it. The first sentence says what the skill does, in the third person. The second says when to use it, and it lists the phrases a user is likely to type, plus "even if they did not ask for a document", which pushes the model to reach for it a little more eagerly than it otherwise would. The last sentence says when not to use it. That is not decoration either. It is the only part of the skill the model sees before it decides whether to load the rest.
-->

---
layout: default
---

<div class="label">The rest of SKILL.md</div>

# The body of SKILL.md

```markdown
# Elephant: grow the design before you grow the code
## EGM operating reflexes (shared preamble)
## Hard rules: do not break these
## Workflow
### Step 2: The "No Code" rule (the interview)
### Step 3: The sycophant defense
### Step 5: Build the design doc, section by section
    Before drafting each one, read its entry in
    references/design-doc-sections.md
## Anti-patterns
## Why this skill exists
```

<div class="caption mt-4">Headings only, plus the line that sends the model to references/.</div>

<!--
Below the frontmatter is the body, and the body is just Markdown instructions. These are elephant's headings, with some steps left out.

It reads like a runbook written for a colleague. Reflexes that hold for the whole session. Hard rules that are never broken, such as no code in this session. A numbered workflow, with a checklist the model keeps as it goes. The mistakes to avoid. And why the skill exists at all, because a model follows a rule better when it knows what the rule is for.

Look at the indented line under step 5. That is the body pointing at a file in references. The model reads the section guide only when it reaches that step, not before. A skill can hide detail inside itself the same way the description hides the whole body. Hold that thought until after the break.
-->

---
layout: statement
---

**The description** decides *when*.

The body decides how.

<!--
So the description is the trigger. If it is vague, the skill never fires, or it fires on the wrong request. If it is good, the agent reaches for the method on its own when a user says "let's plan this," without anyone typing a slash command.

Most of the craft in writing a skill is in that one paragraph. Third person, what it does, when to use it, the words people actually say.
-->

---
layout: default
---

<div class="label">Where method can live</div>

# Four homes for instructions

| Home | Enters the request |
|---|---|
| System prompt, AGENTS.md | Every request |
| Tool definition | Every request, as a schema |
| Skill | When the task calls for it |
| Your own head | When you retype it |

<!--
Where else could the elephant's instructions live? Four places.

The system prompt, or a project file like AGENTS.md or CLAUDE.md that the harness pastes in. That goes into every request whether it is relevant or not.

A tool. L07 showed you tool definitions travel as JSON schemas in every request too. But a tool is an action the harness performs. "Design before you code" is not an action. It is a way of working.

A skill. The method rides along only when the task calls for it.

And the one most of you used on Hackathon 1: your own head. You retype the method into the chat each session, slightly differently each time, and forget half of it on the night.

The design doc for this course calls a skill portable context plus a trigger. That is the sentence to keep.
-->

---
layout: default
---

<div class="label">Not the same thing</div>

# Skill versus tool

| | Tool | Skill |
|---|---|---|
| What it is | A function | Instructions |
| Who acts | The harness runs it | The model follows it |
| In the request | Full schema, always | Description, then body |
| What comes back | A result | A way of working |

<div class="caption mt-6">A tool does something. A skill changes how the model decides what to do.</div>

<!--
Because they are easy to confuse, here they are side by side.

A tool is a function. You met them in L07: a name, a description, a JSON schema for the arguments. The model emits a call, and the harness runs real code: reads a file, runs a command. What comes back is a result, a tool message, and the model reasons about it.

A skill is instructions. Nothing executes when a skill is used. The model reads it, and what changes is the model's behavior for the rest of the task: it starts interviewing you instead of writing code.

They also cost differently. Every tool's full schema rides in every request, because the model has to know the arguments to call it. A skill rides as its description until the model asks for the body.

Two places they meet. First, a skill's instructions usually tell the model which tools to use and when, so a skill is often a method for using tools well. Second, and this is the one for the break: the model has to get the body somehow.

*[Ask: If nothing executes, how does the body of a skill get into the conversation?]*

Direction: Take one or two guesses and do not resolve it. It is the chat break's second question.
-->

---
layout: default
---

<div class="label">Five EGM skills, measured</div>

# The cost of knowing everything

| What the agent holds | Characters | About |
|---|---:|---:|
| Five descriptions | 3,659 | 900 tokens |
| Five full SKILL.md files | 70,697 | 18,000 tokens |

<div class="caption mt-6">At roughly four characters a token. Twenty skills is four times this.</div>

<!--
Here is why the trigger matters. These are the instructor's five EGM skills as of this morning.

All five descriptions together are about three and a half thousand characters. Call it 900 tokens. All five full SKILL.md files are about seventy-one thousand characters, around eighteen thousand tokens. That is a factor of nineteen, and it does not count the templates and reference pages that sit beside each SKILL.md.

Remember L09. The prompt in the L07 trace grew from 471 tokens to 3252 in nine steps, and that was enough to need a token budget. Eighteen thousand tokens of method, before the user has typed anything, is a different problem. And nobody stops at five skills. A working setup has twenty or forty.

Hold that number. It is the chat break.
-->

---
layout: default
---

<div class="label">An open format</div>

# One SKILL.md, many harnesses

- **Claude Code** - where the format started
- **Codex CLI and others** - read the same folder
- **Aider** - no skills, yet

<div class="caption mt-6">Spec: agentskills.io. Each tool documents where it looks for the folder.</div>

<!--
Anthropic published skills for Claude Code, then put the format out as an open specification. Several other harnesses now read the same folder layout, including OpenAI's Codex CLI, which looks in .agents/skills. Where each one looks differs, so check the docs for the tool you use.

The point for this course is the last line. Aider, the tool you have spent five weeks inside, has no notion of a skill. It has a conventions file you can pass in, which is the always-in-the-prompt option from two slides ago. The machinery that decides when to load a skill does not exist there.

Direction: Do not expand on Aider's missing pieces here. The Analyze changes are coming, and
they are the instructor's to announce. One sentence and move on.
-->

---
layout: section
---

# The Elephant-Goldfish Model

## Design before code

<!--
Now the method itself. The Elephant-Goldfish Model.

Fifteen minutes before the break. The article in three parts, the one-line thesis, and the Elephant: the long design session and the document it produces. The Goldfish, which is the half that makes the method work, comes after the break, because it turns out to be the same kind of decision as the break question.
-->

---
layout: default
---

<div class="label">The reading</div>

# Rensin's article in three parts

| Part | Claim |
|---|---|
| 1 | A tool, not a toy |
| 2 | The Elephant-Goldfish Model |
| 3 | We are all managers now |

<div class="caption mt-6">Dave Rensin, Distinguished Engineer, Google. drensin.medium.com</div>

<!--
Dave Rensin is a Distinguished Engineer at Google who spent the last few years leading Google's internal push to use AI well. The article is what he learned. Three parts.

Part one: a tool, not a toy. Use the model as an interrogator before you use it as a researcher. Agree on acceptance criteria with it before you ask for output. Then run the real query in a fresh session with both of those as input. His line is that most people are outsourcing their judgment and calling it productivity.

Part two is the model we are spending today on.

Part three: we are all managers now. You will manage agents the way a manager manages people: set the outcome, scope the authority, say when to escalate, then look away with confidence. He recommends taking a first-time manager course, and he is not joking.

If you read it, notice that part one already contains the whole idea in miniature. Interrogate, define done, then a fresh session. Part two scales that up to a feature.
-->

---
layout: statement
---

*Design* is the new code.

<!--
This is his thesis. The design document is the artifact that matters. Code is downstream of it, increasingly generated, increasingly opaque. If the doc is right, the code can be regenerated. If the doc is wrong, no amount of good code saves you.

You have heard a version of this already. L04 was spec-driven development. Your Apply build is graded half on specification and design. EGM is the method that makes the design good enough to carry that weight.
-->

---
layout: default
---

<div class="label">EGM, step one</div>

# The Elephant

- **No code** until the doc passes
- **Interview** before proposing
- **Model drafts first**, you push back
- **One doc**, four sections

<!--
The Elephant is a long-running session with a lot of context. It is where the design gets grown. Four rules in the instructor's version.

No code. Not a function, not pseudocode, until the design document has passed the Goldfish test you will see after the break.

Interview first. The model asks you questions before it proposes anything. That is Rensin's interrogator idea.

The model drafts first and you push back. The skill calls this the sycophant defense. If you propose first, the model tends to agree with you. If it has to commit to a proposal before it hears yours, you get a real second opinion.

And the output is one document with four sections, next slide.
-->

---
layout: default
---

<div class="label">What the Elephant writes</div>

# The four-section design doc

| Section | Holds |
|---|---|
| Problem | Three to five plain sentences |
| Technical plan | A block diagram, light on jargon |
| Alternatives | Rejected ideas, and why |
| Detailed implementation | Every file, every change |

<!--
Four sections.

The problem, in three to five plain sentences. If you cannot state it that briefly you do not understand it yet.

The technical plan, at the level of a block diagram, with as little jargon as you can manage.

Alternatives. Every idea you rejected and the reason. This is the section people skip and the one that saves you most, because six weeks from now someone, possibly you, will propose the rejected idea again.

And detailed implementation, the longest section. Every file that changes and what changes in it. Rensin is explicit that the doc enumerates every file. That is what lets the code be generated against it later.

Direction: This is the end of the first half. If running long, skip the alternatives
explanation; it comes back with the course design example after the break.
-->

---
layout: default
---

<div class="label">Chat break</div>

# The Assemble question

Twenty skills, each SKILL.md about 4,000 tokens.

1. On turn 1, where does each skill go in the request?
2. What happens before a full SKILL.md appears?
3. Which turn's Assemble does it land in?

<div class="caption mt-6">On paper, five minutes. Sketch the request.</div>

<!--
OK, Zoom, we're on break.

Here is the question. Your harness assembles one request per turn. Give it twenty skills, each SKILL.md around four thousand tokens. On paper: on turn 1, where does each skill go in the request? What has to happen before a skill's full text shows up? And which turn's Assemble does it land in?

Sketch the request as boxes: system, tools, messages. Put the skills somewhere.

Direction: Walk the room. Look for three answers. Everything in the system prompt: ask what
that costs at twenty skills. Nothing until the user names the skill: ask how the model would know
it exists. And the index-then-load answer: ask them to say which message the body arrives in.
-->

---
layout: section
---

# Back to Assemble

## Where skills go

<!--
OK, Zoom, we're back.

Let's put skills into the first card. The answer key first, so everyone knows where we are going, then the three levels behind it, then one skill followed across two real requests.
-->

---
layout: default
---

<div class="label">Chat break</div>

# Break answer key

| Question | Answer |
|---|---|
| Turn 1: where does each skill go? | Name and description, system prompt |
| What comes before the body? | The model calls a load tool |
| Which turn's Assemble? | The next one, as a tool result |

<div class="caption mt-6">All twenty bodies in the system prompt: about 80,000 tokens, every request.</div>

<!--
The answer key, short version, then we take it apart.

One. On turn 1, each skill contributes only its name and description, as a list in the system prompt. Twenty skills, a couple of thousand tokens.

Two. Before a body shows up, the model has to ask for it, and it asks the only way a model can ask a harness for anything: a tool call. That is the answer to the question I left hanging before the break. Nothing executes when a skill is used, but something executes to load it.

Three. The body lands in the next turn's Assemble, as the result of that call, in the messages.

And the caption is the cost of the obvious answer. Twenty bodies at four thousand tokens is eighty thousand tokens, on every request, before the user types a word.

*[Ask: Who got all three? Who got one and two but put the body in the system prompt?]*

Direction: The last case is a good wrong answer. Some harnesses do re-assemble the system prompt
with the loaded body. Say the course answer is the tool result because that is what students will
build, and the two are equivalent for cost after the first load.
-->

---
layout: default
---

<div class="label">The answer</div>

# Three levels of loading

| Level | Enters Assemble | Five EGM skills |
|---|---|---:|
| Name, description | Every request | ~900 tokens |
| SKILL.md body | After the model asks | ~3,500 each |
| references, scripts | When the body points | What it reads |

<div class="caption mt-6">Anthropic's term: progressive disclosure.</div>

<!--
Three levels.

Level one: every skill's name and description go into every request, usually in the system prompt as a short list. That is the 900 tokens. It is an index, and it is what lets the model know a skill exists.

Level two: the body of SKILL.md enters only after the model asks for it. Not on the turn the user typed the request. On a later turn.

Level three: the files in references and assets, and the output of scripts, enter only if the body tells the model to go get them. You saw that line in elephant's step 5 before the break. A long template can sit on disk for a hundred sessions and never cost a token.

Anthropic calls this progressive disclosure. You already know the idea. It is a table of contents.
-->

---
layout: default
---

<div class="label">L07's terms</div>

# One skill across two requests

<div class="grid grid-cols-2 gap-10 mt-4 text-sm">
  <div>
    <div class="font-semibold mb-2">Request n</div>
    <div class="card mb-2" style="padding:0.6rem 0.9rem"><span>system: rules + <b>skill index</b></span></div>
    <div class="card mb-2" style="padding:0.6rem 0.9rem">tools: read_file, load_skill, ...</div>
    <div class="card" style="padding:0.6rem 0.9rem">user: "let's plan a priority flag"</div>
    <div class="caption mt-3">Answer: call load_skill("elephant")</div>
  </div>
  <div>
    <div class="font-semibold mb-2">Request n+1</div>
    <div class="card mb-2" style="padding:0.6rem 0.9rem">system: unchanged</div>
    <div class="card mb-2" style="padding:0.6rem 0.9rem">tools: unchanged</div>
    <div class="card" style="padding:0.6rem 0.9rem">user, then the call, then<br><b>tool: elephant's SKILL.md body</b></div>
    <div class="caption mt-3">Answer: a question for the user</div>
  </div>
</div>

<!--
Here is the answer key drawn as the two requests, in L07's terms.

Request n. The assembled request carries the index. The user says "let's plan a priority flag for taskr." The model matches that against the elephant description, and its answer is not text for the user. It is a tool call. load_skill is a stand-in name. In Claude Code the tool is called Skill. In a harness without one, it can be as plain as a read_file on the SKILL.md path.

The harness applies that call, and the result is the body of SKILL.md.

Request n+1. Assemble now includes that result as a tool message, in the conversation, not the system prompt. The model reads the method and starts following it, which for elephant means asking you questions instead of writing code.

So the answer to "which turn" is: the one after the model asks. A skill costs one extra round trip, and that is the price of not paying eighteen thousand tokens on every request.
-->

---
layout: default
---

<div class="label">EGM, step two</div>

# The Goldfish

- **Fresh session**, no memory
- **Only the doc** as input
- **Can it build this?** If not, the doc fails

<!--
Back to EGM. The Elephant has all the context. Every argument, every clarification, every decision you made at eleven at night. That context lives in the session, not in the doc.

The Goldfish is the opposite. A brand new session with no memory of the conversation. It gets the design document and nothing else.

If the Goldfish can read the doc and explain the system back, find the gaps, and say it could build the thing without asking anything, the doc carries the design. If it cannot, the doc is a thin layer over context you are about to lose the moment a session closes.

And notice what a Goldfish is in today's terms. It is an Assemble decision. The whole trick is a request assembled with almost nothing in it.
-->

---
layout: default
---

<div class="label">The instructor's goldfish skill</div>

# Three Goldfish reviewers

<div class="grid grid-cols-3 gap-6 mt-8 items-stretch">
  <div class="card">
    <ph-book-open-bold class="text-3xl text-blue-600 mb-3" />
    <div class="font-semibold mb-1">A: Comprehension</div>
    <div class="text-sm opacity-70 flex-1">Explain it back</div>
  </div>
  <div class="card">
    <ph-magnifying-glass-bold class="text-3xl text-blue-600 mb-3" />
    <div class="font-semibold mb-1">B: Critic</div>
    <div class="text-sm opacity-70 flex-1">Find the gaps</div>
  </div>
  <div class="card">
    <ph-hammer-bold class="text-3xl text-blue-600 mb-3" />
    <div class="font-semibold mb-1">C: Readiness</div>
    <div class="text-sm opacity-70 flex-1">Could I build this?</div>
  </div>
</div>

<div class="caption mt-8">Run in parallel. Their reports drive the next round of edits.</div>

<!--
Rensin describes one Goldfish. The instructor's skill runs three at once, each with a different job, each in its own fresh context.

A, comprehension. Read the doc and explain the system back. If its explanation is wrong, the doc is unclear, not the reader.

B, critic. Find what is missing, contradictory, or hand-waved.

C, readiness. Read it as the person who has to build it. Could I start tomorrow? What would I have to ask?

Then the three reports come back to the Elephant session, which proposes edits, and you run the Goldfish again. Round after round, until the reviewers have nothing left that matters.
-->

---
layout: default
---

<div class="label">Five skills, one method</div>

# The EGM skill set

| Skill | Step | Writes |
|---|---|---|
| `peanuts` | Before: feed the Elephant | A README per directory |
| `elephant` | Grow the design | The design doc |
| `goldfish` | Test the doc | `GOLDFISH.md` |
| `egm-implement` | Build to the doc | `IMPLEMENT.md` |
| `mean-review` | Tear it apart | `MEAN-REVIEW.md` |

<!--
Here is the instructor's implementation as a set. Five skills.

peanuts runs before anything, on an existing codebase. It walks the tree bottom up and writes a short README in every directory, so an Elephant session can load the shape of a large project cheaply. Peanuts at the leaves, hay at the branches. Notice that is progressive disclosure again, for a codebase.

elephant grows the design and writes the doc. goldfish tests it and keeps a record, GOLDFISH.md. egm-implement refuses to start until that record says the doc passed and a human has signed off. Then it builds to the doc and keeps a ledger, IMPLEMENT.md, flagging any change that drifts from the plan. mean-review is Rensin's last step: a separate fresh session told to find every way the code is bad, and not to be polite about it. It saves each pass as a punch list in its own ledger file, with what you fixed and what you rejected, so the next pass knows what the last one found.

Each skill hands off to the next by name. That handoff is in their descriptions, which is how the agent knows the order.
-->

---
layout: default
---

<div class="label">docs/egm/f26-course-design</div>

# This course's design, six rounds

| What | Count |
|---|---:|
| Goldfish rounds | 6 |
| Reviewer reports | 18 |
| Contradiction caught, round 5 | Withheld `taskr` specs |

<!--
This is not hypothetical. The course you are taking was designed this way. The design doc for Fall 2026 went through six Goldfish rounds. Three reviewers each round, eighteen reports, all kept in the workspace.

One example from round 5. An earlier draft planned to hold back two taskr lessons as a fresh test for the week-7 gate. The critic pointed out that this contradicted the rest of the design: all sixteen lessons were mandatory, and later lessons build on earlier ones, so you cannot withhold one without breaking the ones after it. That plan was cut and replaced with freshly written gate specs.

Nobody in the Elephant session saw it, because everyone in that session knew what was meant. That is the point of a Goldfish.
-->

---
layout: default
---

<div class="label">An Elephant opener, verbatim</div>

# The pivot prompt: situation

```text
# Course Pivot

A feedback session from students has us revamping the course. This is an experimental course so that is alright.
Feedback is in instance/f26/feedback
We are still interested in many of our original design ideas.
Multifaceted pivot is upcoming

- Today's lecture is about Skills and EGM
- Break question gets at how and where skills get included during the Assemble step
- Students were given original Dave Rensin article about EGM last night to read before class today, some of them will have done that
- My implementation of EGM will be discussed and eventually given to them
  - Review the current EGM skill set and update with any best practices for skills that are newer or not implemented already
  - Add a second pass to fully document the EGM skills in a fashion that is meant for instruction so students can read, review, and learn
```

<style>
.slidev-layout pre, .slidev-layout pre code { white-space: pre-wrap !important; word-break: break-word; }
.slidev-layout .slidev-code { font-size: 0.62em !important; line-height: 1.4 !important; }
</style>

<!--
Last piece. A real design prompt, from this morning. This is the instructor's prompt to a coding agent, word for word, typos and all. It is on the glass because it was written to be shown to you.

Read it as an Elephant opener. The first block is situation: why the change, where the evidence is, what stays. Then the work for today, which is this lecture, including the break question you just answered.

Direction: The full text is in assets/pivot-prompt.md. It spans two slides; do not shrink it
further. The instructor decides how much of the course change to discuss here.
-->

---
layout: default
---

<div class="label">An Elephant opener, verbatim</div>

# The pivot prompt: asks

```text
- Current plan for P2 is to have students use a stronger model to adapt Aider to become more like Claude Code. This is the Analyze phase but with a new source repo
- The old repo stops at end of P1, Pair Programmer
- Decisions that need advice
  - Which model should students be using for maximum learning opportunity
  - Which harness " 
- An additional 2-3 weeks of roadmap after this pivot needs to be discussed

Also, include this prompt verbatim in this or a future lecture, as an example of design and good prompts
```

<style>
.slidev-layout pre, .slidev-layout pre code { white-space: pre-wrap !important; word-break: break-word; }
.slidev-layout .slidev-code { font-size: 0.62em !important; line-height: 1.4 !important; }
</style>

<!--
The second block is the asks. A plan stated as a plan. The decisions that are open, stated as open, and the advice wanted on each. Then a roadmap that needs discussing, not deciding.

Look at the verbs. "Decisions that need advice", not "decide". "Needs to be discussed", not "write the roadmap". Those words set how much authority the agent has. It is allowed to recommend; it is not allowed to choose. That is Rensin's part three in one line: scope the authority before you hand over the work.

And the last line is why you are reading it.

*[Ask: If you were the agent, what is the first question you would ask back?]*
-->

---
layout: two-col
---

## What it does well

Settled and open, kept apart. Evidence named. Asks for advice, not answers.

::right::

## What a Goldfish flags

No acceptance criteria. "Which harness" unfinished. No deadline stated.

<div class="caption mt-10">Rensin, part 1: criteria before output.</div>

<!--
What it does well. It separates what is settled from what is open, so the agent does not relitigate the plan. It names where the evidence is instead of summarizing it. And on the hard calls it asks for advice, which keeps the judgment with the person who owns it. That is Rensin's part one.

What a Goldfish would flag. There are no acceptance criteria: what does a finished lecture look like, what makes the advice good enough? The harness question trails off mid-line. And it never says this lecture is at three o'clock, which the agent had to work out from the date.

An Elephant session would have asked about all three. That is the interview step, and it is why the method starts with questions.

*[Ask: What else would your Goldfish flag?]*
-->

---
layout: default
---

<div class="label">Close</div>

# Takeaways

- **A skill** is portable context plus a trigger
- **The index** is always in; the body is earned
- **A Goldfish** is a nearly empty Assemble

<!--
Three things to keep.

A skill is portable context plus a trigger. The description is the trigger, and it is where the craft is.

The index is always in the request. The body is earned, one round trip later, when the model asks for it.

And a Goldfish is an Assemble decision too: a request built with only the document in it, which is exactly why it can tell you whether the document stands on its own.
-->

---
layout: default
---

<div class="label">Close</div>

# Before Tuesday

- **Rensin's article**, if not yet read
- **One SKILL.md**, read closely
- **Your description** for one method you repeat

<!--
Before Tuesday.

If you did not read the article, read it. It is short and it is the source for everything in the second half.

Read one SKILL.md closely. The instructor's EGM skills are in the materials repo now, under egm, with an anatomy-of-a-skill page and a walkthrough of each one. Start with the README there.

And write one description. Pick something you find yourself retyping to a coding agent: how you want commits written, how you want tests run. Write the description paragraph that would make an agent load it at the right moment. Just the description. That is the hard part.

Direction: The skills and walkthroughs are published at materials/egm (commit 4f76140).
-->

---
layout: end
---

<!--
Questions.

If the room is quiet, two prompts. Which of today's five skills would have changed how your Hackathon 1 evening went? And what would you put in the description of a skill for the method you used that night?

Anything that comes up after today goes on Ed. See you Tuesday.
-->
