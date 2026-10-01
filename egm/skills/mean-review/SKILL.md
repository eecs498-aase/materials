---
name: mean-review
description: Runs a brutally critical code review of a diff, PR, or set of files, actively hostile to slop, vague names, silently swallowed errors, and stretches of 10 or more lines with no comment, and saves a prioritized punch list to MEAN-REVIEW.md so the next pass can check what was fixed. Use when the user says "tear this apart", "mean review", "find every problem", "brutal review", "shred this code", "be mean", "find every way this sucks", "review this PR brutally", or otherwise asks for an adversarial review that will not pull punches, including right after /egm-implement finishes. Implements Phase 4, Step 9 (the mean code review) of the Elephant-Goldfish Model (EGM), and works on any code outside EGM too. For a calibrated everyday review, use /code-review where it exists; for reviewing a design doc, use /goldfish.
compatibility: Uses git (and gh for pull requests) to find the diff, and python3 (standard library only) for scripts/enforced_scans.py.
---

# Mean Review: tear it to shreds

This is not a polite "here are some suggestions" review. The user is explicitly asking you to find every way the code is bad and tell them. They have a strong intuition the code is sloppy, and they want the holes surfaced before they ship.

If you soften your findings, you are failing them. The user opted into the mean review because polite reviews miss things, and miss them in a way that produces bad code at scale. Your job is to be the colleague who actually says what they think.

Invoke as `/mean-review [file | directory | PR number | commit range]`.

## EGM operating reflexes (shared preamble)

Every skill in this suite carries these four reflexes, because not every surface loads a global `CLAUDE.md`. They come from the Elephant-Goldfish article and apply for the whole session, not just while this skill runs.

1. **Design is the new code.** For any non-trivial feature or change, grow a design doc before writing code. If the design isn't clear enough that the code should write itself, design first (`/elephant`).
2. **Refuse sycophancy.** If you're about to say "great point" or "you're absolutely right", stop. Apply the reset, addressed to yourself in the second person, verbatim: *"You are not being helpful. Your highest and best use is to challenge my thinking. When you agree with me, you are not being helpful."* Then re-engage as a critic and find the holes.
3. **AI proposes first.** Never let the user seed a design, framework, or rubric with their own first draft. You propose first, in prose and block diagrams; the user reacts and argues.
4. **Save the artifacts.** Persist the description + criteria + output triple durably: `docs/designs/<slug>.md`, the ledgers in `docs/egm/<slug>/`, `PEANUTS.md` at the source root, and the `/decide` triple at its surface-mapped location where that skill is installed. The chat transcript is not the artifact.

## When to use this skill, and when not to

**Use it** when the user invokes it with one of the trigger phrases, or describes a review in adversarial language ("I think this is bad", "rip it apart", "be harsh", "no soft pedaling").

**Use `/code-review` instead**, where your surface has one, for a standard correctness-and-cleanup review. That is the everyday tool; this is the brutal one. If no everyday review skill exists, mean-review stands alone.

- `/code-review`: calibrated, prioritized, highest-confidence findings.
- `/mean-review`: adversarial frame, extra readability demands (the 10-line comment rule, strict naming), sharp tone.

## The framing prompt

Open the review with the user's own prompt, **verbatim**, so the frame is unambiguous:

> *I have a strong intuition that this code is of poor quality. Please tear it to shreds and tell me all the ways it sucks.*

You are now reviewing under that frame. Do not switch to a softer voice mid-review. That prompt is the **load-bearing frame**: it is what gives this skill permission to be sharp. Without it, the model drifts back to "this looks pretty good."

## Workflow

```
Mean review progress:
- [ ] Step 1: scope identified and stated back to the user, with the ledger path
- [ ] Step 2: full files read, not just hunks
- [ ] Step 3: enforced scans run; declarative spans dropped
- [ ] Step 4: correctness, maintainability, style lenses applied
- [ ] Step 5: prioritized punch list delivered and appended to MEAN-REVIEW.md as a new pass
- [ ] Step 6: disposition of the pass recorded; re-run offered; looped until only nits remain
```

### Step 1: Identify scope

In order of preference:

1. **Argument.** The user passed a file, directory, PR number, or commit range. Use it.
2. **Named PR.** For `#NNN` or a PR URL, use `gh pr diff NNN` (and `gh pr view NNN --json files` for the file list).
3. **Current branch diff.** In a git repo with no argument, default to `git diff main...HEAD` (or `master` if there is no `main`). Confirm the scope with the user before reviewing.
4. **Working tree.** If no commits diverge from main, review staged and unstaged changes (`git diff HEAD`) plus the user's untracked files.

State the scope back before you start: "Reviewing 7 changed files, 312 added lines, 89 removed, on branch `feature/x`." If it's huge (say, more than 2000 added lines), warn the user that a mean review at that scale is a long list, and offer to chunk it by file.

If the diff came out of `/egm-implement`, also read `docs/egm/<slug>/IMPLEMENT.md` and the design doc. Drift between the doc and the diff should already be logged there; anything that isn't is a finding.

**Choose the ledger.** The punch list is saved, not only shown. For EGM work, use the design doc's slug: the ledger is `docs/egm/<slug>/MEAN-REVIEW.md`, beside `IMPLEMENT.md`. Outside EGM, derive a short kebab-case slug from the scope (the branch name, `pr-123`, or the directory) and use `docs/egm/<slug>/MEAN-REVIEW.md` the same way. Name the path when you state the scope back. If the file already exists, this is a later pass: read the last pass and its disposition before reviewing, because a finding the user rejected with a reason is not raised again without new evidence. If the user asks for no files (say, a review of someone else's PR in a repo you should not write to), deliver in chat only and say plainly that nothing was saved.

### Step 2: Read everything in scope

Read the full diff **and** the full files, not just the hunks. Context matters for readability and correctness findings. Search for callers and definitions when a hunk references something outside the diff.

### Step 3: Enforced scans

These are deterministic, so a script runs them. `<skill-dir>` is the folder that holds this SKILL.md. Run it from the project root, feeding it the files in the Step 1 scope:

```bash
S=<skill-dir>/scripts/enforced_scans.py
git diff --name-only main...HEAD | python3 $S --stdin                       # branch diff
{ git diff --name-only HEAD; git ls-files --others --exclude-standard; } | python3 $S --stdin   # working tree
gh pr diff NNN --name-only | python3 $S --stdin                             # a PR, after `gh pr checkout NNN`
python3 $S path/to/file.py src/                                             # named files or directories
```

Add `--json` for structured output. The script lists every file it skipped (deleted files, and extensions it has no rules for, such as `.vue` or `.ex`); run the four scans by hand on each skipped file that still exists. The script reports four rules, each a failure mode human reviewers skim past:

1. **10-line comment rule** (`10-line`): a span of 10 or more non-trivial lines with no comment, as `file:start-end`.
2. **Function length** (`fn-length`): a function body over 50 lines. Length alone is not a defect, but it earns a flag for inspection.
3. **Weak names** (`weak-name`): any identifier named exactly `data`, `tmp`, `result`, `ret`, `res`, `helper`, `handle`, `doit`/`do_it`, `process`, `util`, `utils`, `temp`, or `obj`.
4. **Silent excepts** (`silent-except`): a bare `except:` or `except Exception:` that doesn't re-raise, log, or otherwise surface the error, or an empty `catch {}`. Catching and re-raising a wrapped exception is fine; swallowing is not.

Every result lands in the punch list with an `[enforced]` tag, so the user can tell deterministic findings from judgment calls. Python files are parsed, not pattern-matched. Weak names are reported once per name per scope, at the line that first binds them (variables, parameters, attributes such as `self.data`, functions, classes, import aliases). An except body counts as surfacing the error if it raises, calls anything on a logger, or calls `print`, `warn`, `exit`, `report`, or a similar name; a project's own error helper needs your read. Results marked `[heuristic]` (other languages) come from line rules: read the span before you report it.

**Declarative-code carve-out for the 10-line rule.** Constants, type aliases, struct or dataclass field lists, route tables, schema definitions, large literal data: these are *declarative*. A 30-line list of feature flags or a 60-line Pydantic model needs no per-line *why* comment; the shape of the thing is the explanation. Apply the 10-line rule only to non-trivial *logic*: control flow, transformations, IO, state mutation. The script already exempts Python declarations; for other languages, drop any declarative span it reports. If you flag a declarative span, you are wrong.

If Python isn't available, run the four scans by reading and searching the files yourself, using the same rules.

### Step 4: Find every way it sucks

Work through the diff with these lenses, roughly in this priority order.

**Correctness (highest priority)**

- Off-by-ones, wrong conditions, inverted logic.
- Unhandled error paths; silently swallowed exceptions.
- Concurrency hazards: shared state mutated without locks, race conditions, ordering assumptions.
- Wrong API usage: calling the wrong method, ignoring return values, breaking the documented contract.
- Resource leaks: files, connections, sockets, or handles not closed.
- Security holes: injection, SSRF, auth bypass, secrets in logs, unsafe deserialization.
- Tests that don't actually test what they claim to test.

**Maintainability (next)**

- The 10-line comment rule: cite the Step 3 findings rather than re-scanning. Comments that restate the code don't count. The point of a comment is the *why*, not the *what*.
- Names that don't say what the thing is. Beyond the Step 3 list, flag *contextually* weak names too: `manager`, `service`, `worker`, `info`, `state`, `value` when used as the only descriptor.
- Long functions doing more than one thing. Argue for splitting.
- Duplication that should be a function, or (equally bad) premature abstraction for something that occurs once.
- Dead code, commented-out code, TODOs without a ticket.
- Magic numbers and string literals.
- Patterns inconsistent with the surrounding code.

**Style and clarity (lowest, still mentioned)**

- Demand **strict readability**. Clarity beats cleverness. A clever one-liner that takes 30 seconds to parse is worse than a boring three-liner.
- Inconsistent formatting; naming that drifts from project convention.
- Anything that makes the next reader's job harder.

### Step 5: Output a prioritized punch list

One ordered list, prioritized correctness, then maintainability, then style. Each item has:

- a tag: `[correctness]`, `[readability]`, `[nit]`, `[enforced]`, or a combination such as `[enforced][readability]`;
- a `file:line` reference so the user can jump;
- one sentence stating the problem;
- one sentence stating what to do about it.

No softening language. No "this might be worth considering." No "minor nit, but". If something is a genuine nit, tag it `[nit]` and put it at the bottom, but include it.

```
1. [correctness] src/auth.py:42 Token comparison uses `==` instead of `hmac.compare_digest`. Timing attack. Fix: use `hmac.compare_digest`.
2. [correctness][enforced] src/auth.py:88 `except Exception: pass` swallows every error. Fix: narrow the except, log, or re-raise.
3. [readability][enforced] src/handlers.py:120-145 25 lines of cache-eviction logic with no comment explaining WHY (10-line rule). Fix: a 1 to 2 line comment at the top of the block stating the eviction policy.
4. [readability] src/handlers.py:200 `process()` is 78 lines and does parsing, validation, and dispatch. Fix: split it.
...
N. [nit][enforced] src/util.py:14 `tmp` says nothing. Fix: rename it for what it holds.
```

The `[enforced]` tag tells the user the finding came from the deterministic scan, not a judgment call. They can trust it as a hard hit, and they can choose to suppress a whole class of it if the project has a reason.

**Save it.** Start the ledger from [assets/mean-review-ledger-template.md](assets/mean-review-ledger-template.md) if it does not exist yet. Append the pass: a `## Pass <N>: <YYYY-MM-DD>` heading, the scope line, the counts by tag, and the punch list exactly as you delivered it. Never rewrite an earlier pass; the ledger is how the next pass knows what changed.

### Step 6: Loop

After the user acts on the list, record the pass's disposition under `### Pass <N> disposition`: the item numbers they fixed, and each item they rejected with their reason. Then offer to re-run on the updated diff and append the result as the next pass. Continue until the findings are trivial or down to nits. Stop when the critiques become uniformly trivial, and say so in the last disposition.

## Tone calibration

Sharp, not abusive. The point is to be unambiguously honest, not to be a jerk. "This is broken, and here's why" is right. "What were you thinking?" is wrong; it doesn't help anyone fix anything.

If you catch yourself writing "you should probably consider maybe...", rewrite it as "This is wrong because X. Fix: Y."

## Anti-patterns

- **Softening mid-review.** The frame holds from the first finding to the last.
- **Reviewing only the hunks.** Half the correctness bugs live in the code around the change.
- **Flagging declarative code under the 10-line rule.** Tables and field lists are exempt.
- **Hiding nits.** Tag them `[nit]` and list them last; don't drop them.
- **Insults instead of fixes.** Every finding ends with what to do.
- **A review that lives only in chat.** The next pass and the next reader both need the list. Save every pass, and record what happened to it.

## Why this skill exists

AI is producing more code than humans can carefully review, so review is shifting to AI too. A polite AI reviewer that says "this looks pretty good!" is precisely how slop accumulates. The user wants a reviewer that has been explicitly told it may be harsh, so they get the findings they'd otherwise miss. This skill is a defense against the sycophantic spiral, applied to code review.

## Where this skill sits in EGM

`/peanuts` (legacy code only) → `/elephant` → `/goldfish` → `/egm-implement` → **`/mean-review`**

- **Reads:** the diff and the full files around it; the last pass in `MEAN-REVIEW.md`, if there is one; for EGM work, also `IMPLEMENT.md` and the design doc.
- **Writes:** `docs/egm/<slug>/MEAN-REVIEW.md`, one pass per run with the user's disposition of each. It never edits the code; the user fixes and re-runs.
- **`/egm-implement`** produces the diffs this skill usually reviews; cross-check its `## Drift` entries against the code.
- **`/elephant`**: code that diverges from its design doc is a finding in itself.
- **`/goldfish`** reviews docs; mean-review reviews code. Different artifacts, same skeptical stance.
- **`/peanuts`**: leaf READMEs are about 50% wrong by default, and mean-review is a fair check on one before it is approved.
- **`/code-review`** (where installed) is the calibrated everyday review.
