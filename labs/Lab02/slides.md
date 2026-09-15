---
theme: ../../lectures/theme
title: "Lab02: From functions to agent actions"
layout: title
class: text-left
transition: fade
mdc: true
---

# From functions to agent actions

Lab02 · September 21–22, 2026

40-minute example · 70-minute project work

<!--
Introduce the stockroom example. This is guided design and one implementation increment, not a full build from scratch. No lab deliverable.
-->

---
layout: default
---

# The stockroom problem

“Prepare supplies for five workshop participants.”

Three markers available.

<!--
Minutes 0–5. Open the ordinary inventory functions. Storage and quantity checks already work. The user has not told us whether sharing is acceptable. Do not reveal the real hackathon domain.
-->

---
layout: default
---

# Two possible designs

- A complete plan first
- One decision after each observation
- User input at consequential choices

<!--
Minutes 5–9. Compare both approaches. A plan-first system can also continue after observations; it is not inherently wrong. Ask students which information would change a decision. More calls are not evidence of a better design.
-->

---
layout: default
---

# The design contract

- Model and application responsibilities
- Action inputs and outcomes
- User decisions and stopping conditions

<!--
Minutes 9–13. Open design/SYSTEM.md and FLOW.md. Point to a rejected alternative. The example owns its boundaries; students will choose theirs in the assessment. The reset history is supplied example history, not evidence of a student design process.
-->

---
layout: default
---

# Classification and agency

<div class="grid grid-cols-2 gap-8"><div><h2>Classification</h2><p>Items → one call → validated labels</p></div><div><h2>Agent</h2><p>Goal → action → observation → decision</p></div></div>

<!--
Minutes 13–15. Open categorize. It performs one bounded prompt and ordinary validation. The model does not choose the next operation. In the agent, the next operation depends on observations.
-->

---
layout: default
---

# Function and action contracts

```python
# Application function
inventory.reserve(item, quantity)

# Model request
{"action": "reserve",
 "args": {"item": "marker", "quantity": 5}}
```

<!--
Minutes 15–18. Description and argument contract make a capability visible; validation and dispatch actually invoke it. Open dispatch. This example uses text JSON; native function calling is another valid protocol. The model does not execute Python.
-->

---
layout: default
---

# The feedback increment

- Read the increment spec
- Predict the failing test
- Implement with scoped Aider context
- Inspect the diff and result

<!--
Minutes 18–30. Open the exercise. The missing observation causes two tests to fail. Commit the increment specification before implementation. Keep the model context small. If live editing stalls, compare the worked solution and preserve the timebox.
-->

---
layout: default
---

# The next decision

```text
reserve(marker, 5)
→ only 3 available
ask whether participants can share
→ user agrees
reserve(marker, 3)
→ 3 reserved
```

<!--
Minutes 30–33. Use the rehearsed live example or the scripted fallback. Label the fallback prominently: these are test responses, not evidence of a live model solve. The failed action must enter the next request automatically.
-->

---
layout: default
---

# Evidence in application state

- Three markers reserved
- Rejection leaves stock unchanged
- Repeated failures stop

<!--
Minutes 33–36. Inspect inventory.json and the tests. A confident final sentence does not establish a reservation. Ask whether approval should happen before or after checking availability. This is a design question, not merely more defensive code.
-->

---
layout: default
---

# A defensible submission

- Reasoned design choices
- Working action and observation flow
- Evidence and acknowledged limitations

<!--
Minutes 36–40. Open REFLECTION.md. Explain that design quality and meaningful behavior matter more than counts of tools, calls or agents. The sample honestly names model-authored final reports and approval timing as limitations. The actual prompt is revealed at the event.
-->

---
layout: default
---

# Your project increment

- One observable result
- Relevant spec and context
- A test that detects failure

<!--
Minutes 40–100. Ten minutes to choose the next ai-assistant increment, then fifty to build and verify. Staff circulate. The assistant build remains due October 6. The hackathon uses a supplied application, so no completed homework application is required that evening.
-->

---
layout: default
---

# Design reconciliation

- Update decisions and diagrams
- Record evidence and limitations
- Commit and push

<!--
Minutes 100–110. Preserve the supported-work close. No separate lab submission. Check the course announcement for hackathon logistics and model availability.
-->
