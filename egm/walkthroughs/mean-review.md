# mean-review: give the reviewer permission to be harsh

Skill: [`skills/mean-review/SKILL.md`](../skills/mean-review/SKILL.md).
Article section: "Phase 4: Implementation", Step 9 ("The 'Mean' Code
Review").

## What problem it solves

Ask a model to review code and it will tell you the code looks pretty good,
with a few suggestions. It was trained to be pleasant. The result is a review
that misses the swallowed exception on line 88 because pointing it out felt
rude.

Rensin's fix is one prompt, which he says is the one he actually uses:

> *I have a strong intuition that this code is of poor quality. Please tear it
> to shreds and tell me all the ways it sucks.*

Plus two demands: flag every place that goes 10 lines without a comment, and
insist on strict readability. Then fix what it finds and run it again, until
the critiques are trivial.

The prompt works because it changes what "helpful" means for this
conversation. The user has said, up front, that they expect bad news. The
skill keeps that frame in place for the whole review and adds the pieces a
single prompt can't: a defined scope, deterministic scans, a fixed output
format, and a loop.

## How it triggers

The description lists the phrases people say when they want this: "tear
this apart", "brutal review", "be mean", "find every way this sucks". It also
names its place in EGM (right after `/egm-implement`) while saying it works
on any code.

Two near misses are spelled out. "For a calibrated everyday review, use
/code-review where it exists" separates it from the polite review. "For
reviewing a design doc, use /goldfish" separates it from its sibling. In the
trigger tests, "give me harsh feedback on my resume" is the clever negative:
harsh, yes, but not code.

## The SKILL.md, section by section

**Opening.** Two paragraphs that make softening a failure: "If you soften
your findings, you are failing them." This is the skill arguing with the
model's training before the review starts.

**When to use it, and when not to.** A short comparison with `/code-review`.
Without it, a model with both skills installed would reach for the brutal one
on routine reviews, or the reverse.

**The framing prompt.** Rensin's sentence, verbatim, called "the
load-bearing frame". This is low freedom on purpose. A paraphrase such as
"please review critically" is exactly the softer version the model drifts
back to.

**Checklist.** Six steps, ending in the loop.

**Step 1, scope.** Argument, PR, branch diff, or working tree, in that order,
and say the scope back with numbers before starting ("7 changed files, 312
added lines"). A huge diff gets a warning and an offer to chunk it. If the
diff came from `/egm-implement`, the skill also reads `IMPLEMENT.md` and the
design doc, because a change that isn't in either is a finding.

**Step 2, read everything.** The full files, as well as the hunks. Most
correctness bugs in a change live in the code around it.

**Step 3, enforced scans.** Four rules that people skim past, run by a
script:

| Rule | Flags |
|---|---|
| `10-line` | 10 or more lines of real logic with no comment |
| `fn-length` | a function body over 50 lines |
| `weak-name` | a name like `data`, `tmp`, `result`, `handle`, `process`, `obj` |
| `silent-except` | an `except Exception:` or empty `catch {}` that swallows the error |

Each hit is tagged `[enforced]` in the punch list, so the user can tell a
deterministic hit from a judgment call. Then the **declarative carve-out**: a
60-line table of constants or a dataclass's field list needs no comment,
because its shape is the explanation. The script already skips those in
Python; the model drops them by hand in other languages. "If you flag a
declarative span, you are wrong" is a sentence written for a model that
loves to over-apply a rule it was just given.

**Step 4, the lenses.** Correctness first (off-by-ones, error paths, races,
leaks, security, tests that test nothing), then maintainability, then style.
This part is high freedom: lists of what to look for, no procedure.

**Step 5, the punch list.** A strict format: tag, `file:line`, one sentence
for the problem, one for the fix. No "you might consider". Nits are labeled
and go last, but they are never dropped.

**Step 6, loop.** Offer to re-run after fixes, and stop when the findings are
uniformly trivial. That's the article's "rinse and repeat".

**Tone calibration.** Sharp, not abusive. "This is broken, and here's why" is
right; "what were you thinking?" helps nobody fix anything. The skill
includes a rewrite rule for when the model starts hedging.

## What lives outside SKILL.md

| File | Loaded when | Why it is separate |
|---|---|---|
| `scripts/enforced_scans.py` | Run at Step 3; never read | The four scans are mechanical. The old version of this skill asked the model to do them with grep, which can't find "10 lines without a comment", so each run improvised something different. A script makes `[enforced]` mean the same thing every time. |
| `evals/trigger-evals.json` | Never, by the model | Trigger tests. |

How the script is built is worth a look, since you will write tools like it:

- Python files are parsed with `ast` and `tokenize`, so a `#` inside a string
  is not mistaken for a comment, and declarative code can be recognized.
- Other languages get line rules and every finding is marked `[heuristic]`,
  which tells the model to read the span before trusting it.
- It lists every file it skipped (a deleted file, a `.yaml`, a `.vue`), so a
  quiet run can't be mistaken for a clean one.
- It passes its own scans. A tool that enforces the 10-line comment rule and
  breaks it would not survive its first mean review.

## Worked example

`/egm-implement` just finished `webhook-retries` (see the
[egm-implement walkthrough](egm-implement.md)). The user types "mean review,
don't hold back."

**Step 1.** "Reviewing 8 changed files, 412 added lines, 37 removed, on
branch `webhook-retries`." The model reads `IMPLEMENT.md`: one drift entry,
resolved (the `http.py` timeout).

**Step 3.**

```
$ git diff --name-only main...HEAD | python3 ~/.claude/skills/mean-review/scripts/enforced_scans.py --stdin
shipyard/notify/worker.py:88  silent-except  except Exception swallows the error (no raise, no log)
shipyard/notify/worker.py:41-62  10-line  17 code lines with no comment
shipyard/notify/worker.py:30  fn-length  drain() body is 64 lines (limit 50)
shipyard/notify/outbox.py:22  weak-name  data (parameter)
skipped deploy/worker.yaml: no rules for .yaml files
4 finding(s) in 7 scanned file(s); 1 skipped
```

The YAML file is deployment config, declarative by nature, so there is
nothing to scan by hand.

**Step 4.** Reading the full `worker.py`, the model finds the real problem
the scans can't see: the worker marks an event `sent` *before* the HTTP call
returns, so a crash between the two loses the event, which is the exact
failure the feature exists to prevent.

**Step 5.**

```
1. [correctness] shipyard/notify/worker.py:71 Event is marked sent before the POST returns; a crash in between drops it, which is the bug this feature exists to fix. Fix: mark sent only after a 2xx, inside the same transaction as the attempt record.
2. [correctness][enforced] shipyard/notify/worker.py:88 `except Exception:` swallows everything, including the database error that would tell you the outbox is broken. Fix: catch the HTTP client's error only; log and re-raise the rest.
3. [readability][enforced] shipyard/notify/worker.py:41-62 The backoff calculation has no comment saying why the base is 30 seconds or why the cap is 1 hour. Fix: two lines stating the policy and pointing at the design doc section.
4. [readability][enforced] shipyard/notify/worker.py:30 `drain()` is 64 lines and claims, sends, and reschedules. Fix: split send and reschedule into their own functions.
5. [readability] shipyard/notify/outbox.py:40 `get_due()` returns events ordered by id, but the doc promises per-order ordering by creation time. Fix: order by (order_id, created_at), and test it.
6. [nit][enforced] shipyard/notify/outbox.py:22 `data` says nothing. Fix: `payload`.
```

Finding 1 is not in `IMPLEMENT.md`'s drift log, and finding 5 contradicts
the design doc. Both are exactly what the cross-check in Step 1 is for.

**Step 6.** The user fixes all six. The re-run returns two nits. Done.

## What the skill adds to the article

The article supplies the prompt, the 10-line rule, "demand strict
readability", and the loop. The skill adds the scope rules, the full-file
reading rule, three more enforced scans with a script behind them, the
declarative carve-out, the prioritized punch-list format, the tone rules, and
the cross-check against the design doc and `IMPLEMENT.md`.

## Review questions and exercises

1. Why does the skill insist on the framing prompt *verbatim*? Write a
   plausible paraphrase and explain how it could let the review go soft.
2. Run `enforced_scans.py` on code you wrote for this course. Pick one
   `10-line` finding and write the comment it wants. Was the comment
   useful, or did the rule misfire? If it misfired, was the span
   declarative?
3. The script marks non-Python findings `[heuristic]`. Find a JavaScript or
   shell snippet where a line rule gives a wrong answer (a false positive or
   a miss), and explain what a parser would do differently.
4. The punch list puts correctness before readability, yet the 10-line rule
   is called out as essential. Make the case that an uncommented 20-line
   block is a correctness risk as well as a style problem.
5. Ask a model for a code review twice on the same diff: once plainly, once
   with Rensin's framing prompt. Count the findings in each and classify
   them. What changed besides tone?
