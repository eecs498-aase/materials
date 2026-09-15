# Worked design: stockroom assistant

## Purpose and behavior

Help an organizer reserve supplies when the initial request may exceed stock.
Success means a useful, approved reservation or an honest explanation of what
could not be done. S1 is a separate classifier. S2–S5 form the agent workflow.

## Decision and alternative

Choose a reactive conversation with one action per call. Stock availability and
the user's willingness to share can change the next step. An alternative is one
initial call that emits a complete reservation plan. That is efficient when all
constraints are known, but cannot incorporate a later user answer unless it also
has a continuation mechanism. Batching could be useful for large inventories;
this example has three items and favors inspectable decisions.

## Responsibilities and state

`inventory.py` owns stock, reservations and categories on disk. `assistant.py`
owns the conversation and action budget. `model.py` only transports messages.
`dispatch` validates model requests, asks for approval, and invokes application
functions. Conversation state lasts for one invocation. Resumable sessions and
multi-user inventory access are out of scope.

## Action contracts

The model emits `{action, args}`. This is a text protocol, not native provider
function calling. Only exact known argument names are accepted.

| Action | Input | Observation / effect |
|---|---|---|
| inspect | empty object | Current inventory; no mutation |
| reserve | item string, positive integer quantity | Approval followed by reservation result, denial, or failure |
| ask | question string | User answer, returned to the same conversation |
| finish | message string | End the interaction |

Model proposals are untrusted. Unknown actions and invalid arguments become error
observations. No dynamic Python evaluation is used. Stock arithmetic stays in
ordinary code. The prompt requests helpful planning, but availability is enforced
by `Inventory.reserve`, not by confidence in the model.

## Feedback and limits

Every success, denial or failure is delivered before the next model decision.
The agent has ten calls at most. A transport outage ends with an error rather
than retrying indefinitely. The initial design requires automatic feedback;
specs/01-feedback.md fills the exercise's intentionally omitted implementation.

## Verification

S1: test_classification_is_one_call and test_bad_classification_cannot_change_inventory.
S3: test_failure_feedback_and_clarification_change_next_action verifies both the
request context and saved inventory. S4: test_denial_does_not_change_stock.
S5: test_malformed_output_reaches_next_request_and_stops. Live rehearsal is separate:
a scripted trace cannot establish that a real model chooses sensible actions.

## Known limitations

The final message is model-authored and not mechanically reconciled against all
prior results. Inspect the trace and inventory when evaluating its truthfulness.
Reservation approval happens before the stock check, which is simple but can ask
the user to approve an infeasible action. A stronger design would validate before
approval and validate again at execution. Denial is returned to the model but is
not a persistent prohibition; subsequent mutations still require approval.
