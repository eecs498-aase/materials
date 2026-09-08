# notes: the L01 demo

The small codebase the L01 live demo runs on. `notes.py` is a sixty-line note
CLI with two deliberate flaws, and the demo fixes both in three prompts
without anyone typing a line of code.

You have this so you can run it yourself. Watching someone drive aider and
driving it are different skills, and only one of them is on the exam.

## Get a working copy

```sh
./reset
```

That builds a disposable copy at `demo-scratch/L01-notes-cli`, sets up aider's
config, makes it a git repo so `/undo` works, and runs the tests. Run it again
any time to start over. Do not run aider in this directory: the config files
here are undotted on purpose (`aider.conf.yml`, not `.aider.conf.yml`) so that
aider ignores them and this copy stays pristine.

Then:

```sh
cd demo-scratch/L01-notes-cli
aider notes.py test_notes.py
```

`./reset --model 4b` pins the 4B instead, which is worth doing once. See below.

## The two flaws

Open `notes.py` before you start. It is short on purpose.

- **`parse_args()` dies on no arguments.** `argv[0]` on an empty list is an
  `IndexError`. Run `python3 notes.py` and watch it crash.
- **`dispatch()` is an if-chain.** It works. It is just not how you would
  write it.

The tests pass anyway, all four of them, which is the first thing worth
noticing: a green suite is not the same as good code.

## The three prompts

Say them close to verbatim. They are the demo.

1. `Refactor parse_args() to handle the no-args case — print usage and exit cleanly.`
2. `Add a unit test for the no-args path.`
3. `Replace the if-chain in dispatch() with a dictionary lookup.`

After each one, **read the diff before you accept it**. That is the whole
point of the exercise. The model generates; you judge. Run the suite where
you can see it:

```
/run pytest -q
```

Four tests before, five after prompt 2, still green after prompt 3.

## What to actually pay attention to

Not the commands. `aider-practice` teaches the commands, and it teaches them
better than a five-minute demo can.

Pay attention to the loop: you describe an outcome, the model proposes a
change, you read it and decide. Three coordinated edits in five minutes with
zero lines typed is the shape of the collaboration, and the judging step is
the part that is still yours.

## Try it on the 4B

```sh
./reset --model 4b
```

Same three prompts, smaller model. Expect to work harder: more feedback
rounds, and at least one diff you should reject. That is not a defect, it is
the lesson arriving faster. The question is never "is this model bad." It is
context, model, or prompt, which is L03.

## Configuration

`aider.conf.yml` pins the 9B for both the main and the weak model, so Ollama
holds one model instead of swapping on every auto-commit.

## The thing to watch for on prompt 1

Prompt 1 works about half the time on the 9B. Ten runs, three fixes, and
switching aider's edit format barely moves it.

It does not fail the same way twice, so do not memorise a signature. Two of
the shapes seen in rehearsal: the model writes a corrected `parse_args()` and
leaves the original one in the file below it, so Python binds the second
definition and nothing changes; or it writes a no-args branch that returns
something `main()` cannot unpack, and every command breaks.

Here is the part that should bother you. Those two shapes look completely
different to the test suite. The first left all four tests green in twenty
runs, because no existing test calls `parse_args` with an empty list. The
second turns the suite red immediately.

So a green suite after prompt 1 tells you nothing about whether prompt 1
worked. Run `python3 notes.py` — the thing the prompt was about — and read
the diff before you accept it. Noticing that is the actual skill here, and it
is the reason you are given the codebase rather than a video.

## Configuration

`aider.conf.yml` pins the 9B for both the main and the weak model, so Ollama
holds one model instead of swapping on every auto-commit.

## The thing to watch for on prompt 1

Prompt 1 works about half the time on the 9B. Ten runs, three fixes; the
edit format barely moves it. When it fails it always fails the same way: the
model writes a corrected `parse_args()` and leaves the original one in the
file below it. Python binds the second definition, so the program still
crashes on no arguments and the diff looked fine.

Here is the part that should bother you. **The tests were green in all twenty
runs**, the broken ones included. Four tests that never call `parse_args` with
an empty list cannot see this bug. A green suite told you nothing.

So when you run this yourself: read the diff before you accept it, and if the
program still crashes afterwards, count the `def parse_args` lines. Catching
that is the actual skill the demo is about.

It also sets `think: false`. qwen3.5 is a reasoning model
and, left alone, spends its budget thinking before writing any code: measured
on this project, 1200 tokens of reasoning and zero characters of output, 23
seconds against 9. If your prompts take 25 seconds or more, the parameter did
not reach Ollama; add ` /no_think` to the end of each prompt instead.

`aider.model.metadata.json` prices these free local models at frontier rates
on purpose, so `/tokens` answers "what would this session have cost if I were
paying for it."
