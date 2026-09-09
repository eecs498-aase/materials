---
theme: ../../lectures/theme
title: "Lab02: Supported build and verification"
layout: title
class: text-left
transition: fade
mdc: true
---

# Supported build and verification

## Lab02 · September 21–22, 2026

Your Stage 1 assistant, in your existing repository.

<!--
Set a concrete goal for the work block. No new application or separate lab grade.
-->

---
layout: default
---

# Choose one observable result

Name the requirement and acceptance scenario.

Open the increment spec and the relevant design sections.

Identify the test that will distinguish success from a plausible-looking result.

<!--
Ten-minute intake. If design is incomplete, finish it before application implementation.
-->

---
layout: default
---

# Work with relevant context

Load reference material read-only. Add only the files this increment may edit.

Ask Aider for one bounded task. Inspect the diff and run the relevant tests.

Revise the design when the evidence changes a decision.

<!--
Staff circulate during the long work block. Do not prescribe module names.
-->

---
layout: default
---

# Test the behavior you care about

A parser returning an error does not prove the disk stayed unchanged.

Check file contents and git state before and after rejection.

Use fakes for routine tests and disposable repositories for edits.

<!--
Ask for a plausible defect each assertion would catch. Supplied adapter tests earn no student test credit.
-->

---
layout: default
---

# Exercise a recovery case

Choose a published scenario: malformed proposal, cancellation, a stale preview, failed write, or unsafe undo.

Predict the result, run the check, and compare.

A correct failing test is useful evidence.

<!--
Minutes 80–100. No live-model requirement for safety checks. Do not touch the development repository.
-->

---
layout: default
---

# YAML selects the endpoint

Change the API base or model identifier through configuration.

The application must not depend on Ollama-specific requests or a fixed hostname.

Provider freedom still follows the permitted-model policy.

<!--
Use fake transport for deterministic configuration checks. Aider and the application have separate YAML settings.
-->

---
layout: default
---

# Reconcile before you leave

Update diagrams and the spec when responsibilities changed.

Record tests run and known limitations. Commit session evidence and push your work.

No points for suffering. No repeated deductions for one shortfall.

<!--
Last ten minutes. Independent missing artifacts still lose their own points.
-->

---
layout: default
---

# Keep the next deadline visible

Hackathon 1: September 24.

Stage 1 build: September 25, 11:59 PM.

Keep a runnable increment available.

<!--
The complete rubric and acceptance scenarios are in the student repository. Confirm event logistics through the course announcement.
-->
