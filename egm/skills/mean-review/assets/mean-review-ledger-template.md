---
slug: <slug>
scope: <branch, PR, commit range, or paths>
design_doc_path: <docs/designs/<slug>.md, or none outside EGM>
date_opened: <YYYY-MM-DD>
---

# MEAN-REVIEW: <slug>

Punch lists from /mean-review, one pass per run, newest last. Earlier passes
are never rewritten.

<!--
Each pass records the scope and the list exactly as delivered.
The disposition is written after the user acts on the list: fixed, or
rejected with a reason. A finding rejected with a reason is not raised again
without new evidence.
-->

---

## Pass <N>: <YYYY-MM-DD>

- **scope:** <what was reviewed, for example "7 changed files, 312 added lines, 89 removed, on branch feature/x">
- **counts:** <correctness N, readability N, nit N; N of them enforced>

<the punch list, exactly as delivered>

### Pass <N> disposition: <YYYY-MM-DD>

<!-- Fixed: item numbers. Rejected: item number and the user's reason.
     Say here when the remaining findings were all nits and the loop stopped. -->
