# Worked reconciliation

This is an authored teaching example, not a record of a timed student attempt.
The exercise removes one line from the worked implementation so the class can
observe a missing feedback path and repair it from a specification.

The completed implementation supports the four described actions and a separate
one-call classifier. Deterministic tests check a failed reservation, clarification,
subsequent successful reservation, approval rejection, invalid classification and
a bounded malformed-output loop. These tests do not establish live model quality.

The important distinction is between printing an error and delivering an error
as input to the next decision. In the broken exercise, the user sees the failure
but the next request does not contain it. Adding feedback reconciles implementation
with the original design rather than changing the design.

A design change worth investigating is validation before approval. The current
adapter asks to reserve five markers, receives approval, and only then learns
that three exist. Earlier validation could avoid an unhelpful approval question.
Another limitation is the model-authored final report; execution traces remain
the stronger evidence of what happened. No claim of a live rehearsal is made.
