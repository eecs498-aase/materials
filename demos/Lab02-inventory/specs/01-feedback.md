# Increment: execution results inform the next decision

## Goal

Implement S3 and support S5. An error displayed in the terminal must also become
an observation in the conversation sent to the next model call.

## Design

Follow design/SYSTEM.md, Feedback and limits. Do not change the application
functions or the JSON action format. Preserve observations for successful actions
as well as failures and user answers.

## Change

In assistant.py, find the omitted feedback step after the trace is emitted. Append
a user-role observation message containing the JSON result. This text protocol
uses user-role observations; a native tool-call protocol would use tool-result
messages associated with call IDs instead.

## Verification

Run bin/inventory test. Before the change the feedback and malformed-output tests
fail; afterward they pass. Inspect the scripted trace and saved inventory. Test
with scripted messages first, then have the instructor rehearse the live model.
