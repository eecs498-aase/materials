# EGM: the Elephant-Goldfish Model as five skills

This folder holds five Agent Skills that turn one design method into
something a coding agent can follow, plus a set of pages that take the skills
apart so you can learn how skills are built. Install the skills and use them.
Then read the pages and argue with the choices.

## Where the method comes from

The Elephant-Goldfish Model is Dave Rensin's. He described it in
[Elephants, Goldfish and the New Golden Age of Software Engineering](https://drensin.medium.com/elephants-goldfish-and-the-new-golden-age-of-software-engineering-c33641a48874)
(April 2026), written from what his team at Google learned building with AI.
Read the article first. It is the spec these skills implement, and it is
better written than any summary of it.

The short version:

- **Design is the new code.** When a model writes most of the code, the
  artifact a human can stand behind is the design. So the design judgments
  have to land in a document before any code exists.
- **The Elephant** is a long, context-rich AI session (and the design doc it
  helps you write). It remembers every argument you had with it.
- **The Goldfish** is a brand-new session with no memory. It knows only what
  is on the page.
- **Feed the Elephant; test it against the Goldfish.** If a fresh session
  can't understand, critique, and implement from your doc alone, the doc is
  leaning on context that disappears the moment the chat closes.

The skills are this course's implementation of the method. Where a skill adds
something the article doesn't say (a ledger file, a script, a gate), the
walkthrough for that skill tells you.

## The five skills

| Skill | Article | What it does | Writes |
|---|---|---|---|
| [`peanuts`](walkthroughs/peanuts.md) | Bootstrapping ("peanuts and hay") | Builds a bottom-up tree of README files for a big codebase, with a human review gate at each level | a `README.md` per directory, `PEANUTS.md` |
| [`elephant`](walkthroughs/elephant.md) | Phases 1 and 2 | Runs the no-code design conversation, then writes the four-section design doc | `docs/designs/<slug>.md`, `ELEPHANT.md` |
| [`goldfish`](walkthroughs/goldfish.md) | Phase 3, Steps 5 to 7 | Sends the doc to three fresh reviewers in parallel and loops until only nits remain | `GOLDFISH.md`, reviewer reports |
| [`egm-implement`](walkthroughs/egm-implement.md) | Phase 4, Step 8 | Builds only the files the doc lists, and stops when reality and the doc disagree | the code, `IMPLEMENT.md` |
| [`mean-review`](walkthroughs/mean-review.md) | Phase 4, Step 9 | Reviews the diff as harshly as it can, with four scans a script enforces | a punch list |

The ledgers (`ELEPHANT.md`, `GOLDFISH.md`, `IMPLEMENT.md`) live together in
`docs/egm/<slug>/`, one folder per feature. The slug is the design doc's
filename without `.md`, and the four skills after `peanuts` rely on that.

## How they fit together

```
  big legacy codebase?
        |
        v
   /peanuts ----> README.md in every directory (+ PEANUTS.md)
        |                  |
        |   (Step 1 reads the READMEs instead of the source)
        v                  v
  an idea ----> /elephant ----> docs/designs/<slug>.md
                   |                    |
                   v                    v
             ELEPHANT.md           /goldfish  <------------+
                                        |                  |
                          3 fresh reviewers in parallel    |
                                        |                  |
                                  GOLDFISH.md      edit the doc, run again
                                        |                  |
                           only nits left? ---- no --------+
                                        |
                                       yes
                                        |
                       a human signs off (or you record skipped-solo)
                                        |
                                        v
                                 /egm-implement ----> code + IMPLEMENT.md
                                        |
                          (drift? stop, fix the doc first)
                                        |
                                        v
                                  /mean-review ----> punch list, fix, run again
```

Each arrow is a handoff you start yourself. No skill runs the next one for
you. That is on purpose: the gaps between them are where a human decides.

## What is in this folder

```
egm/
├── README.md                  you are here
├── anatomy-of-a-skill.md      how a skill is built, using these five
├── walkthroughs/              one page per skill
│   ├── peanuts.md
│   ├── elephant.md
│   ├── goldfish.md
│   ├── egm-implement.md
│   └── mean-review.md
└── skills/                    the skills themselves; copy these to install
    ├── elephant/
    ├── goldfish/
    ├── egm-implement/
    ├── mean-review/
    └── peanuts/
```

Suggested reading order: [anatomy-of-a-skill.md](anatomy-of-a-skill.md)
first, then the walkthroughs in pipeline order (peanuts, elephant, goldfish,
egm-implement, mean-review). Keep the matching `SKILL.md` open beside each
walkthrough.

## Installing the skills

Each skill is a folder with a `SKILL.md` inside. Installing one means putting
that folder where your harness looks for skills. That's all.

You need `git` and `python3` (3.9 or newer, standard library only) for the
three helper scripts.

### Claude Code

Personal install, available in every project on your machine:

```sh
git clone --depth 1 https://github.com/eecs498-aase/materials.git
mkdir -p ~/.claude/skills
cp -R materials/egm/skills/* ~/.claude/skills/
```

Or install into one project, so everyone who clones it gets them, by copying
into that project's `.claude/skills/` and committing it.

Start `claude`, run `/skills`, and the five should be listed. Type
`/elephant` to start one directly, or just describe what you want ("let's
design webhook retries before we write anything") and let the model pick the
skill from its description. If a skill never triggers on its own, the
description is the first thing to check.

### Codex, OpenClaw, and other harnesses that read SKILL.md

The `SKILL.md` format is an open spec ([agentskills.io](https://agentskills.io/specification)),
and many harnesses read it. A common shared location is `.agents/skills/` in
a project or `~/.agents/skills/` in your home directory. Codex and OpenClaw
both look there:

```sh
mkdir -p ~/.agents/skills
cp -R materials/egm/skills/* ~/.agents/skills/
```

Other tools (Gemini CLI, OpenCode, Cursor, GitHub Copilot in VS Code, and
more) each document their own folder. The list is at
[agentskills.io/clients](https://agentskills.io/clients). These skills keep
their frontmatter to the fields in the spec, so they load anywhere the spec
does.

Two parts are harness-specific. `goldfish` needs a way to start fresh
subagents (its `references/runtimes.md` covers several harnesses, and how to
do it by hand). Invocation syntax also varies by harness. Claude Code and
several others expose each skill as a slash command such as `/goldfish`;
where yours doesn't, name the skill or let the description match.

### Aider

Aider has no skill loader, so you are the loader. Add a skill's body to the
chat by hand, from your clone of this repo (the `git clone` line above):

```
/read-only path/to/materials/egm/skills/elephant/SKILL.md
```

Replace `path/to/materials` with wherever your clone lives.

Notice what that costs. Aider now sends the whole body in every request it
assembles, whether you need it or not, and keeps sending it until you
`/drop` the file. A harness with real skill support sends only the one-line
description until the model asks for more. The anatomy page explains that
difference, and it is most of the point.

For `goldfish` in Aider, each reviewer is a new `aider` session that has
never seen your design chat. Give it the doc with `/read-only` and paste one
prompt from `skills/goldfish/assets/goldfish-reviewer-prompts.md`.

## Trying them without risk

Make a throwaway git repo with a few files of real code in it, and run
`/elephant` on a small feature. A first design conversation takes 20 to 30
minutes if you actually argue. Then run `/goldfish` on the doc it writes and
read what three strangers think of it.

`elephant` and `goldfish` write only under `docs/`. `peanuts` writes a
`README.md` per directory and `PEANUTS.md` at the root of the tree.
`egm-implement` changes code, and only the files your design doc lists.

On a real repo, run `peanuts` on a branch. It writes a `README.md` into every
in-scope directory and can overwrite one that is already there, so you want
`git diff` to show you what changed and an easy way back.

## Each skill also ships trigger tests

Every skill has `evals/trigger-evals.json`: twelve realistic requests, half
of which should load the skill and half of which should not (near misses,
on purpose). They are the starting point for measuring whether a description
works. The anatomy page has an exercise that uses them.
