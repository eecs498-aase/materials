# Stockroom planning assistant

A 40-minute guided example of adding AI to an ordinary application. This is not
an independent 40-minute build from scratch and it has no graded submission.

A workshop organizer asks for supplies. The stockroom already exposes `read()`
and `reserve(item, quantity)`. Build an interaction that investigates availability,
asks about tradeoffs, and reserves supplies with approval. Separately categorize
item names with one model call.

## Success criteria

- S1: Categorization makes one bounded call; ordinary code validates its output.
- S2: Model-selected actions reach actual stockroom functions through validated contracts.
- S3: An unavailable reservation returns an observation automatically; the assistant
  can ask a question and act on the answer.
- S4: A reservation requires approval, and rejection leaves inventory unchanged.
- S5: Execution is bounded and the final report distinguishes results from intentions.

## Forty minutes

| Minutes | Work |
|---|---|
| 0–5 | Read the problem and inspect ordinary functions |
| 5–13 | Compare two designs; inspect the worked design and contracts |
| 13–18 | Trace categorization and one function-to-action adapter |
| 18–30 | Specify, implement and verify execution feedback with Aider |
| 30–36 | Inspect failure, clarification, approval and resulting state |
| 36–40 | Reconcile the design and assess the worked submission |

Start with `reset --stage exercise`. The complete example is provided except for
one intentional feedback omission. Read specs/01-feedback.md, then implement that
increment using your permitted model. Tests must check the observation sent to the
next model request, not just whether an error was printed. The full example lives
in solution/ for comparison after the attempt. There is no need to type a whole
agent from scratch during this walkthrough.

## Design freedom

The example uses one JSON action per call. Native function calling, batches and
staged plans are alternatives. The choice here keeps one failure easy to inspect;
it is not a required architecture for another assignment. A model gets only the
actions its programmer exposes. JSON definitions by themselves do not execute
anything: the adapter validates and invokes ordinary functions.
