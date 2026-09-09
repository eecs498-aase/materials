---
theme: ../../lectures/theme
title: "Lab03: Build the agent: tools, function calling, and the loop"
layout: title
class: text-left
transition: fade
mdc: true
---

# Build the agent

## Lab03 · September 28–29, 2026

Continue your assistant, design, and history.

<!--
Triage unfinished Stage 1 work before dependent implementation.
-->

---
layout: default
---

# Preserve the boundary snapshot

Keep the Apply submission in history.

Repair unfinished foundations with staff support.

Continue in the same repository; the submitted grade does not change.

<!--
No replacement starter or staff reference is handed out.
-->

---
layout: default
---

# Revise the control-flow design

The model can now request a tool.

Your program validates the call, obtains approval, and returns a result.

A stop condition bounds what happens next.

<!--
Follow the current Analyze assignment for schemas and stop conditions. Students choose internal interfaces.
-->

---
layout: default
---

# Replace transport, keep configuration

Write your own client as the API lessons introduce function calling.

Keep the configurable API base, model identifier, credentials, and limits.

No hard-coded Ollama dependency.

<!--
Stage 1 supplied transport only. Preserve provider-independent YAML behavior and tests.
-->

---
layout: default
---

# Prove that denial means no action

Use a fake model response requesting a tool. Deny the request.

Assert the tool did not execute, the target stayed unchanged, and the loop received the denial.

Then test a harmless approved operation in a disposable target.

<!--
Do deterministic checks before live endpoint testing. Git does not protect against arbitrary shell effects.
-->

---
layout: default
---

# Implement one bounded increment

Update the system spec and relevant diagrams.

Write an increment spec, choose Aider context, and implement with tests.

Keep Stage 1 edit protections while adding the new control path.

<!--
This replaces the retired single-pass exercise. Model policy covers design and code.
-->

---
layout: default
---

# Leave with evidence

Capture a denied action from your implementation, or record the blocker with staff.

Update diagrams and name the next verifiable result.

Push the work and session evidence.

<!--
No separate ten-point lab assignment. The Analyze rubric controls project grading.
-->
