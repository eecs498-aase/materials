# ELEPHANT: <slug>

feature: <slug>
design_doc_path:
date_opened: <YYYY-MM-DD>
current_step: 0
last_update: <YYYY-MM-DD>
human_review_gate: pending
next_step:

<!--
Keep each header field on its own line; a reflowed header that runs the
fields together is hard to parse. Update current_step and last_update
whenever a step finishes. human_review_gate here is a record copy: the gate
itself is the human_review_gate field in GOLDFISH.md's header, and only a
person changes either one (pending, passed, or skipped-solo).
-->

## Context loaded

<!-- Step 1. One line per file read: path, then what you learned from it.
     Write "greenfield: nothing to load" if Step 1 was skipped. -->

- `path/to/file`: what it told you about the system, as it bears on this feature.

## Interview decisions

<!-- Steps 2 to 4. Dated bullets, added as decisions land. Include the
     approaches the user or you rejected, with the reason: they become
     Section 3 (Alternatives). -->

## Section status

<!-- Step 5. One entry per approved section. -->

- Section 1 (Problem): approved <YYYY-MM-DD>. <decisions or rejected alternatives raised while writing it>
- Section 2 (Technical Plan): approved <YYYY-MM-DD>. <...>
- Section 3 (Alternatives): approved <YYYY-MM-DD>. <count of entries>
- Section 4 (Detailed Implementation): approved <YYYY-MM-DD>. <...>

<!-- Later, /goldfish rounds may send you back here. Record each response as
     "## Goldfish round N response (<YYYY-MM-DD>)" with the rulings taken. -->
