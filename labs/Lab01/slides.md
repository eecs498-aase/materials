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

## Lab01 · Design your pair-programmer

September 14–15, 2026

<!--
This lab connects the tool students have used to the system they will design. The future-tool comparison stays here. Finish instruction at minute 65.
-->

---
layout: default
---

# Today: understand, then design

| Minutes | Work |
|---|---|
| 0–27 | Follow one request through Aider |
| 27–37 | Diagnose the model, context, and harness |
| 37–40 | Hackathon briefing |
| 40–55 | Your project, design artifacts, and grading |
| 55–65 | Claude Code and OpenClaw comparison |
| 65–110 | Draft, sketch, and review a first increment |

<!--
The work block starts at 65, not after an additional agenda segment. No one is expected to finish a substantial system spec today.
-->

---
layout: default
---

# One familiar request

```text
Add a --priority flag to taskr's add command.
```

You already met this request in the practice lessons.

Today we follow an illustrative diff-mode turn, from selected files to a commit.

<!--
Practice began in whole-file mode. Say that this is a simplified diff-mode trace, not a transcript claiming a particular model did exactly this. The feature spans CLI, task data, and storage.
-->

---
layout: default
---

# Who performs each action?

<svg viewBox="0 0 880 230" style="width:100%;height:230px" xmlns="http://www.w3.org/2000/svg">
<defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto"><path d="M0,0 L0,6 L7,3 z" fill="#2E5BFF"/></marker></defs>
<rect x="0" y="20" width="190" height="52" rx="4" fill="#F4F2EA" stroke="#E5E3DA"/><text x="95.0" y="52" text-anchor="middle" style="font-family:IBM Plex Sans,sans-serif;font-size:18px;fill:#1A1A1A">Assemble context</text>
<rect x="230" y="20" width="180" height="52" rx="4" fill="#F4F2EA" stroke="#E5E3DA"/><text x="320.0" y="52" text-anchor="middle" style="font-family:IBM Plex Sans,sans-serif;font-size:18px;fill:#1A1A1A">Model replies</text>
<rect x="450" y="20" width="190" height="52" rx="4" fill="#F4F2EA" stroke="#E5E3DA"/><text x="545.0" y="52" text-anchor="middle" style="font-family:IBM Plex Sans,sans-serif;font-size:18px;fill:#1A1A1A">Parse and apply</text>
<rect x="680" y="20" width="190" height="52" rx="4" fill="#F4F2EA" stroke="#E5E3DA"/><text x="775.0" y="52" text-anchor="middle" style="font-family:IBM Plex Sans,sans-serif;font-size:18px;fill:#1A1A1A">Git commit</text>
<path d="M190,46 H226" stroke="#2E5BFF" stroke-width="2" fill="none" marker-end="url(#arrow)"/>
<path d="M410,46 H446" stroke="#2E5BFF" stroke-width="2" fill="none" marker-end="url(#arrow)"/>
<path d="M640,46 H676" stroke="#2E5BFF" stroke-width="2" fill="none" marker-end="url(#arrow)"/>
<path d="M545,72 V150 H95 V77" stroke="#2E5BFF" stroke-width="2" fill="none" marker-end="url(#arrow)"/>
<text x="320" y="140" text-anchor="middle" style="font-family:IBM Plex Sans,sans-serif;font-size:17px;fill:#3D3D38">failure feedback</text>
</svg>

The harness prepares context and acts on the reply. The model supplies text.

The human chooses the task and evaluates the result.

<!--
This is a responsibility diagram of Aider, not a required architecture for their project. Ask students to locate the filesystem write: the model has not acquired direct access to their disk.
-->

---
layout: default
---

# 1. Assemble the model input

The request combines instructions, selected file contents, relevant history, and your new message.

Aider can also supply a repository map and edit-format examples.

**Context is selected information.** A file outside it may exist on disk without being available in full to the model.

<!--
Avoid claiming a universal seven-part ordering; actual prompt composition depends on coder, model, and settings. Ask what the model would need to implement priority consistently across CLI and storage.
-->

---
layout: default
---

# Choose editable and reference files

```text
/add taskr/cli.py taskr/task.py taskr/store.py
/read-only specs/priority.md
/tokens
```

Editable files can be changed. Read-only files explain the contract.

A linked document is not automatically loaded into context.

<!--
Explain why these files are relevant. This is an example selection, not an instruction to add every file. Read-only context still consumes space. /tokens gives a diagnostic, not a guarantee of implementation correctness.
-->

---
layout: default
---

# The repository map is a summary

```text
taskr/store.py
  Store.add(title, tags) -> Task

taskr/task.py
  Task: id, title, tags
```

Aider ranks useful definitions and references within a token budget.

A signature can suggest where to look. It does not supply the function body.

<!--
The excerpt is illustrative. Aider builds a graph of definitions/references and ranks useful portions. Do not promise the map includes every file or proves a dependency absent. Source: https://aider.chat/docs/repomap.html
-->

---
layout: default
---

# Context has a budget

<svg viewBox="0 0 880 230" style="width:100%;height:230px" xmlns="http://www.w3.org/2000/svg">
<defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto"><path d="M0,0 L0,6 L7,3 z" fill="#2E5BFF"/></marker></defs>
<rect x="5" y="15" width="180" height="52" rx="4" fill="#F4F2EA" stroke="#E5E3DA"/><text x="95.0" y="47" text-anchor="middle" style="font-family:IBM Plex Sans,sans-serif;font-size:18px;fill:#1A1A1A">Input budget</text>
<rect x="230" y="15" width="180" height="52" rx="4" fill="#F4F2EA" stroke="#E5E3DA"/><text x="320.0" y="47" text-anchor="middle" style="font-family:IBM Plex Sans,sans-serif;font-size:18px;fill:#1A1A1A">Instructions</text>
<rect x="230" y="95" width="180" height="52" rx="4" fill="#F4F2EA" stroke="#E5E3DA"/><text x="320.0" y="127" text-anchor="middle" style="font-family:IBM Plex Sans,sans-serif;font-size:18px;fill:#1A1A1A">Selected files</text>
<rect x="460" y="15" width="180" height="52" rx="4" fill="#F4F2EA" stroke="#E5E3DA"/><text x="550.0" y="47" text-anchor="middle" style="font-family:IBM Plex Sans,sans-serif;font-size:18px;fill:#1A1A1A">History</text>
<rect x="460" y="95" width="180" height="52" rx="4" fill="#F4F2EA" stroke="#E5E3DA"/><text x="550.0" y="127" text-anchor="middle" style="font-family:IBM Plex Sans,sans-serif;font-size:18px;fill:#1A1A1A">Current request</text>
<path d="M185,41 H225" stroke="#2E5BFF" stroke-width="2" fill="none" marker-end="url(#arrow)"/>
<path d="M185,41 H205 V121 H225" stroke="#2E5BFF" stroke-width="2" fill="none" marker-end="url(#arrow)"/>
<path d="M185,41 H205 V195 H440 V41 H456" stroke="#2E5BFF" stroke-width="2" fill="none" marker-end="url(#arrow)"/>
<path d="M440,121 H456" stroke="#2E5BFF" stroke-width="2" fill="none" marker-end="url(#arrow)"/>
</svg>

More history leaves less room for current evidence.

If the necessary input cannot fit, the tool needs an explicit policy.

<!--
Ask what can be removed and what must survive. Their project will preserve system instructions, current request, and selected file contents, rejecting an oversized mandatory input rather than silently truncating it.
-->

---
layout: default
---

# 2. The reply is still text

```text
taskr/cli.py
<<<<<<< SEARCH
add.add_argument("title")
=======
add.add_argument("title")
add.add_argument("--priority", default="normal")
>>>>>>> REPLACE
```

This is a proposed replacement, not evidence that priority works.

<!--
A deliberately small illustrative block. It does not implement storage or validation. Ask what is missing. Reading only the happy-looking block would miss the incomplete feature.
-->

---
layout: default
---

# 3. Parse structure from the reply

A parser identifies a path, a SEARCH section, and replacement text.

It must also report malformed blocks without crashing.

**Parsing and validation answer different questions:** is this a block, and is this block applicable here?

<!--
Missing divider is a syntax error. A nonexistent path or zero exact matches can be a later validation error. Their design can separate those responsibilities; we grade outcomes rather than one function signature.
-->

---
layout: default
---

# 4. Applying an edit changes state

A useful proposal still needs a match against the actual file.

Aider can use fallback matching and can retain successful edits when other blocks fail.

Your Stage 1 contract requires exact, unambiguous matches and all-or-nothing application.

<!--
Do not describe partial application as untestable. It is testable with a different contract. Their stricter rule reduces recovery cases and makes the target state easier to reason about.
-->

---
layout: default
---

# 5. Failure can become new input

```text
Proposed edit
    → match failed
    → report the failure to the model
    → receive another proposal
```

Aider also supports lint/test feedback cycles when configured.

A feedback loop can exist without general model-selected tool use.

<!--
Explain that Aider has real automation. Never say it cannot run commands or tests. Its normal task framing and available repair cycles differ from a general tool-selection loop. Source: https://aider.chat/docs/usage/lint-test.html
-->

---
layout: default
---

# 6. Git records the accepted change

A commit gives a concrete before/after boundary.

Undo needs rules about ownership and changes made afterward.

**Git is useful recovery infrastructure. It does not undo every side effect a program can cause.**

<!--
Keep Aider development commits distinct from commits created by the student assistant in a target repo. In Stage 1 the target is disposable and clean; owned HEAD commits can be undone. Running shell commands arrives later and has consequences git cannot reverse.
-->

---
layout: default
---

# Explain the request back to us

For the priority feature, identify:

1. Which information enters context?
2. Which program interprets the reply?
3. What could appear correct while still being wrong?
4. What evidence would establish the feature works?

<!--
Use the last three minutes of the first block. Pair discussion, then take two answers. Seek the missing storage update or persistence test. Do not reward memorizing a source filename.
-->

---
layout: default
---

# Diagnose before re-prompting

| Observation | Investigate |
|---|---|
| Code calls an interface that does not exist | Missing context or incorrect design |
| Valid-looking block cannot match | Stale text or invalid generated edit |
| Tests pass but the feature is incomplete | Weak acceptance criteria or tests |
| A request times out | Endpoint configuration, service, or limits |

<!--
This begins the 10-minute diagnosis block. There may be more than one cause. Ask what evidence distinguishes two explanations before declaring the model too weak.
-->

---
layout: default
---

# Same model, different harness

A bare chat client can suggest code.

Aider adds repository context, an edit protocol, and actions on files.

Better results may come from better context and checking, even when the model is unchanged.

<!--
Do not claim the model is irrelevant or that every failure is context. Students can improve their harness and their prompts while still measuring model limitations.
-->

---
layout: default
---

# Practice: choose the next action

The model adds `--priority`. The command runs. After restarting the program, every task has normal priority.

What do you inspect before asking the model to try again?

Write one missing acceptance criterion and name a test that would catch it.

<!--
Give four minutes to pairs and two for responses. A persistence round-trip test is a good answer. The student should infer a storage problem from evidence, not blindly add all files or switch models.
-->

---
layout: default
---

# Hackathon 1: September 24

Two hours in the course browser workspace.

A new feature prompt is revealed in the room and applied to your own project.

Submit during the session. Keep a runnable increment available beforehand.

The event has separate grading. Ask staff early about conflicts or accommodations.

<!--
Three minutes including logistics. Exact room/time and the course model must be announced by staff; do not invent them. The existing project is preparation, but no separate hackathon solution is assigned. Build due the next day.
-->

---
layout: default
---

# Your project starts with a design

You receive a transport adapter and development tooling.

You design the application, write its specification, and use Aider to implement it in increments.

**There is no supplied conversation loop or required module layout.**

<!--
Minute 40. The adapter protects the learning sequence: HTTP transport is implemented in Analyze. It does not supply a config loader or state model. Do not hand out a module diagram as the answer.
-->

---
layout: default
---

# All seven features remain

| Feature | Required behavior |
|---|---|
| F1 | Conversation, budget handling, streamed replies |
| F2 | Add, drop, list, and clear context |
| F3 | Current file contents rendered consistently |
| F4 | A tested edit-format prompt |
| F5 | Parsing with useful errors |
| F6 | Exact edits, complete preview, explicit approval |
| F7 | One commit per accepted edit set, guarded undo |

<!--
Configuration and lifecycle are cross-cutting requirements, not a hidden eighth feature. No scope cut accompanies the redesign. Point to SPEC.md for complete edge cases.
-->

---
layout: default
---

# YAML config, any compatible endpoint

```yaml
base_url: https://api.example.edu/v1
model: course-model-id
api_key_env: ASSISTANT_API_KEY
context_budget: 8000
timeout_seconds: 60
temperature: 0.2
```

You implement loading and validation. The adapter handles transport.

<!--
The schema is a shared external contract. Students choose its internal representation. base_url can include any path prefix; the adapter adds /chat/completions only. Aider has a separate YAML config. No Ollama-specific dependency belongs in the application.
-->

---
layout: default
---

# Staff requirements, student decisions

| We specify | You design |
|---|---|
| Observable behavior and safety rules | Responsibilities and state ownership |
| API and configuration contract | Internal interfaces and error flow |
| Acceptance scenarios and rubric | Tests, fixtures, implementation increments |
| Semester direction | Where later capabilities can enter |

<!--
They are learning to design within constraints. Different architectures can satisfy the same assignment. Future compatibility needs a rationale, not a premature plugin framework.
-->

---
layout: default
---

# Two levels of specification

**System spec:** behavior, architecture, interfaces, failure handling, verification, and rationale.

**Increment specs:** scoped context, ordered tasks, and a testable result for each change.

Commit the initial design before application implementation. Revise it when evidence changes a decision.

<!--
A substantial spec is not one giant context dump. Requirements map to planned tests; those test names need not exist in the initial design. Experiments are allowed when labeled and reconciled before the dependent implementation.
-->

---
layout: default
---

# Three diagrams explain your design

| Diagram | Question it answers |
|---|---|
| Components and data flow | Who owns state and crosses each boundary? |
| Request sequence | Who does what during one proposed edit? |
| Edit lifecycle | When may an edit be approved, rejected, or undone? |

Keep initial versions in git. Update the final diagrams to describe what you built.

<!--
Their diagrams must show their system, not copy the Aider diagram. Mermaid is enough. Label unimplemented parts and tie component names to code once it exists.
-->

---
layout: default
---

# 40 points: specification and diagrams

| Criterion | Points |
|---|---:|
| Requirements and acceptance criteria | 10 |
| Architecture and interface design | 10 |
| Aider implementation specs | 10 |
| Diagrams: components 4, sequence 3, lifecycle 3 | 10 |

Completeness and usefulness matter. Document length does not.

<!--
All points shown are within the build grade. Design can retain credit when implementation falls short, provided its claims and final status are accurate.
-->

---
layout: default
---

# 40 points: behavior and verification

| Criterion | Points |
|---|---:|
| Required functionality, scored by feature | 20 |
| Behavioral tests | 8 |
| Safety and recovery tests | 7 |
| Fake integration 3, live evidence 2 | 5 |

A correct failing test can earn test credit while exposing an unfinished feature.

<!--
The rubric contains each feature suballocation. Only one F4 outcome point depends on live-model success; honest unsuccessful evidence can earn live-reporting points. Supplied transport tests earn no application-test credit.
-->

---
layout: default
---

# 20 points: evidence and reconciliation

| Criterion | Points |
|---|---:|
| Spec-first history | 5 |
| Deliberate Aider use | 5 |
| Diagnosis and design reconciliation | 5 |
| Operating instructions | 3 |
| Model disclosure and evidence index | 2 |

<!--
Explain evidence as concrete pointers, not log volume. No points for suffering and no repeated deductions for one missing feature across otherwise sound artifacts. Policy violations use academic-integrity procedures.
-->

---
layout: default
---

# The model rule includes the spec

Use the permitted Stage 1 models for drafting, critique, diagrams, code, and tests.

The 9B is recommended; the 4B is permitted. Record secondary models too.

Any compatible hosting service is allowed. A different provider does not authorize a different model.

<!--
The assigned packet states the exact model IDs and observed-session exception. No frontier design followed by local implementation. Keep design and development sessions, disclose actual aliases and known quantization.
-->

---
layout: default
---

# From a first increment to December

Start with one small, verifiable result. Continue through all requirements.

Analyze adds model-selected tools and a loop. Create hardens the agent and adds memory and another way to reach it.

Keep one repository and history. Refactor when needed; preserve phase snapshots.

<!--
Close the 15-minute project block. Dates remain Sep 25 for the build and Sep 24 for hackathon 1. Do not promise a workload estimate. A runnable slice early reduces integration surprises.
-->

---
layout: default
---

# What changes with Claude Code?

| Aider workflow | General agentic CLI workflow |
|---|---|
| Human frames a bounded edit task | Human supplies a broader task |
| Selected files and a repo map guide context | Tools can discover and read files |
| Edit/repair cycles follow harness rules | Model can choose tools and next steps |
| Human checks progress between tasks | Permissions and stop rules bound autonomy |

<!--
Keep this comparison in lab. It is a mechanism comparison, not a claim that Aider lacks automation or that an agentic CLI needs no human judgment. Claude Code is the concrete comparison; no subscription is required for Stage 1. Source: https://code.claude.com/docs/en/overview
-->

---
layout: default
---

# The same priority request, later

An agentic CLI may search for argument parsing, read storage code, edit both, and run tests before returning.

Each tool result becomes evidence for the next decision.

**Who controls the next step, and what stops a bad one?**

<!--
Use a hypothetical trace, not an unobserved product demonstration. The model can choose actions only from what its harness exposes and permissions allow. Students build this responsibility in Analyze.
-->

---
layout: default
---

# Instructions still need a harness

Project instructions provide persistent guidance.

Skills package instructions for particular tasks. Hooks attach checks to events. Tool integrations expose actions and results.

None of these removes the need for clear contracts and verification.

<!--
Keep product feature details at mechanism level, avoid promising exact weeks for every branded feature. Their DEVELOPMENT.md starts the habit of writing instructions for a future session. Code and permissions enforce constraints that prose alone cannot guarantee.
-->

---
layout: default
---

# OpenClaw adds a gateway

<svg viewBox="0 0 880 230" style="width:100%;height:230px" xmlns="http://www.w3.org/2000/svg">
<defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto"><path d="M0,0 L0,6 L7,3 z" fill="#2E5BFF"/></marker></defs>
<rect x="235" y="0" width="410" height="52" rx="4" fill="#F4F2EA" stroke="#E5E3DA"/><text x="440.0" y="32" text-anchor="middle" style="font-family:IBM Plex Sans,sans-serif;font-size:18px;fill:#1A1A1A">Chat channels and clients</text>
<rect x="220" y="85" width="440" height="52" rx="4" fill="#F4F2EA" stroke="#E5E3DA"/><text x="440.0" y="117" text-anchor="middle" style="font-family:IBM Plex Sans,sans-serif;font-size:18px;fill:#1A1A1A">Gateway: connections and routing</text>
<rect x="100" y="172" width="270" height="52" rx="4" fill="#F4F2EA" stroke="#E5E3DA"/><text x="235.0" y="204" text-anchor="middle" style="font-family:IBM Plex Sans,sans-serif;font-size:18px;fill:#1A1A1A">Agent runtime and tools</text>
<rect x="505" y="172" width="250" height="52" rx="4" fill="#F4F2EA" stroke="#E5E3DA"/><text x="630.0" y="204" text-anchor="middle" style="font-family:IBM Plex Sans,sans-serif;font-size:18px;fill:#1A1A1A">Connected nodes</text>
<path d="M440,52 V80" stroke="#2E5BFF" stroke-width="2" fill="none" marker-end="url(#arrow)"/>
<path d="M320,137 V153 H235 V167" stroke="#2E5BFF" stroke-width="2" fill="none" marker-end="url(#arrow)"/>
<path d="M560,137 V153 H630 V167" stroke="#2E5BFF" stroke-width="2" fill="none" marker-end="url(#arrow)"/>
</svg>

A gateway gives an agent ways to receive requests and reach connected capabilities.

<!--
OpenClaw is a concrete future-system comparison, not a library students must adopt. Source: https://docs.openclaw.ai/concepts/architecture. Keep client/node connections distinct from the agent runtime; the gateway is not simply several agents on one task.
-->

---
layout: default
---

# Design for the next boundary

Where could a model-selected tool enter your current control flow?

Could the endpoint client be replaced without rewriting state management?

Could a web interface use the same application behavior as the terminal?

<!--
End future comparison at minute 65. Ask for boundary reasoning, not December implementation. Students may change their answers as the course progresses.
-->

---
layout: default
---

# Work block: 45 minutes

| Minutes | Your result |
|---|---|
| 0–8 | Read the packet; confirm development tooling |
| 8–23 | Interpret requirements; sketch responsibilities |
| 23–35 | Write a first increment with a checkable result |
| 35–43 | Exchange a focused review; ask staff about blockers |
| 43–45 | Commit the draft and record your next decision |

<!--
No application exists to run yet. bin/dev test checks the transport, not a completed feature. The whole initial system spec is finished after lab, before application implementation. Use peer review plus staff triage.
-->

---
layout: default
---

# Review a decision, not the polish

Ask your partner:

- What must be true when this increment is done?
- Which decision would the model still have to guess?
- What test would catch a plausible mistake?

Record the question and your response. Bring assignment ambiguities to staff.

<!--
Do not require every student to queue for a five-minute full-design review. Record unresolved questions and a follow-up path. Peer review concerns contracts, not sharing implementation solutions.
-->

---
layout: default
---

# Before you implement

Finish the initial system design and diagrams.

Use a fresh permitted-model session to review them. Commit the design and the first increment spec.

Then build, test, and revise one increment at a time.

<!--
Remind students of the complete submission packet: design, diagrams, specs, code/tests, configuration example, DEVELOPMENT.md, operating README, evidence, AI_LOG.md, reflection, and sessions. All exact requirements and scoring live in their repository.
-->
