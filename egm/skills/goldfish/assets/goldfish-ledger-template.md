---
feature: <slug>
design_doc_path: docs/designs/<slug>.md
date_opened: <YYYY-MM-DD>
human_review_gate: pending
rounds: []
---

# GOLDFISH: <slug>

Validation trace for `docs/designs/<slug>.md`. The orchestrating session
appends one round entry per Goldfish round; reviewer reports live in sibling
files. Reviewers never read this directory.

<!--
Keep each header field on its own line.
human_review_gate in this header IS the gate. Only a person changes it:
pending, passed, or skipped-solo. /egm-implement's gate check reads it here.
Each round entry records a copy, so update the latest copy to match.
readiness is one word: not-yet or ready. Put nuance in the notes, not the field.
-->

---

## Round <N>: <YYYY-MM-DD>

- **round:** <N>
- **date:** <YYYY-MM-DD>
- **agent_type:** A `<type>`, B `<type>`, C `<type>`, spawned in parallel in one message
- **prompts:** <the three prompts exactly as sent, verbatim, including the preamble, the filled-in path, and any appended note. Indent them as a code block.>
- **what was under review:** <the doc as of commit or date>
- **reports:** `goldfish-A-comprehension<-rN>.md`, `goldfish-B-critic<-rN>.md`, `goldfish-C-readiness<-rN>.md`
- **verdicts:** A: <comprehended or not, and where it misread>. B: <counts by severity>. C: <READY or NOT-READY, number of questions>.
- **convergence:** <findings two or more reviewers raised independently; treat these as high confidence>
- **contract note:** <held, or how independence was breached (for example, a reviewer followed a link into docs/egm/)>
- **human_review_gate:** <copy of the header value: pending | passed | skipped-solo>
- **readiness:** <not-yet | ready>

### Round <N> disposition: <YYYY-MM-DD>

<!-- After the user rules on the proposed edits: what was accepted and applied
     to the doc, what was rejected and why. -->
