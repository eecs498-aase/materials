# IMPLEMENT: <slug>

feature: <slug>
design_doc_path: docs/designs/<slug>.md
goldfish_path: docs/egm/<slug>/GOLDFISH.md
goldfish_round_used: <N>
human_review_gate: <passed | skipped-solo>
start_date: <YYYY-MM-DD>
status: in-progress

<!--
Keep each header field on its own line. When work ends, replace
"status: in-progress" with "status: complete" and add:
end_date: <YYYY-MM-DD>
next_step: /mean-review
-->

<One short paragraph on build order: follow the doc's Detailed Implementation
order, or say how and why you re-sequenced it (producers before consumers).>

## Files touched

| path | change | status |
|---|---|---|
| <path> | <one-line summary of the change> | planned |

<!-- status is planned, in-progress, or done. One row per file the doc
     enumerates; never a row for a file the doc does not list. -->

## Drift

<!-- One entry per mismatch between the doc and reality. Copy this block: -->

- date: <YYYY-MM-DD>
- type: missing-file | wrong-mechanism | new-assumption-needed | doc-conflict
- description: <what specifically is missing or wrong>
- proposed resolution: <update doc section X to say Y; OR rewrite section Z with /elephant's discipline; OR re-run /goldfish; OR talk to the user>
- status: open

<!-- When resolved, replace "status: open" with one of:
     resolved: doc edited in place at <path>
     resolved: section <name> rewritten
     resolved: full /elephant rerun
     resolved: /goldfish rerun, round <N+1> -->

## Verification

- step: <what was run>
- command: <exact command>
- result: pass | fail | partial
- notes: <any output worth keeping>
