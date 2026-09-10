# transcript-analytics, with a spec

The codebase the L04 live demo runs on. It is the same program L03 used, at
the same starting point, with two things added: a `pyproject.toml` so the
project can declare dependencies, and `spec.md`, the five-section spec the
demo hands to Aider in one paste.

L03 typed one sentence at a time and watched a two-file change fall apart.
L04 writes the whole thing down first and runs it in one pass. Same model,
same program, different amount of planning.

## Get a working copy

```sh
./reset
```

That builds a disposable copy at `demo-scratch/L04-transcript-analytics`
beside the root of your clone, sets up aider's config, installs the
dependencies with `uv sync`, makes it a git repo so `/undo` works, and checks
that the program runs and matplotlib imports. It prints the full path when it
finishes, so you never have to work it out. Run it again any time to start
over. Do not run aider in this directory: the config files here are undotted
on purpose (`aider.conf.yml`, not `.aider.conf.yml`) so aider ignores them and
this copy stays pristine.

The first `./reset` on a machine downloads matplotlib and pyyaml, which takes
maybe fifteen seconds. Every one after that is served from uv's cache and
takes about a second.

Then:

```sh
cd ../../demo-scratch/L04-transcript-analytics
uv run main transcript.txt
uv run main transcript.txt --top 5 --speakers
```

`--summarize` is the only thing that needs a model. `./reset` writes the `.env`
that points at it. If nothing is listening it prints `summary unavailable` and
the rest of the report still works, on purpose.

## The five files, and the two that are missing

| File | Owns |
|------|------|
| `src/main.py` | counting, and printing the report |
| `src/arg_parse.py` | every command-line flag |
| `src/constants.py` | the stopword list and the tuning values |
| `src/data_types.py` | the shapes the analysis passes around |
| `src/llm.py` | the one call to a model |

`src/chart.py` and `src/output_format.py` do not exist. Writing them is the
demo. The spec says so in its Ending context section, which is the section
students skip and the one that decides what the model is allowed to touch.

## The spec

Read [`spec.md`](spec.md) before you run anything. It is short, and every one
of the five sections earns its place:

1. **High-Level Objective.** One sentence. Why any of this.
2. **Mid-Level Objectives.** Three outcomes you can check by running the
   program.
3. **Implementation Notes.** The engineering judgment the model would
   otherwise have to guess at. "Use matplotlib and pyyaml, they are already
   dependencies." "Never call `plt.show()`." "The flags live in
   `arg_parse.py`."
4. **Context.** Beginning and ending file lists, with `(new file)` and
   `(readonly)` markers.
5. **Ordered Low-Level Tasks.** Four IDK-rich steps in dependency order.

Notice what Implementation Notes buys you. Every line in that section is
something you would otherwise have written in a review comment after the fact.
Put it in the spec and you skip the review round.

Notice too that task 3 names `src/arg_parse.py`. That is L03's lesson written
down: the flags live in that file, so a spec that only says "add a `--chart`
flag to main.py" produces a program that accepts nothing. The spec is where
you stop the model from having to know that.

## Run the demo yourself

```sh
./reset && cd ../../demo-scratch/L04-transcript-analytics
aider src/main.py src/arg_parse.py
```

Two files on the command line, not four. `.aider.conf.yml` sets
`edit-format: architect`, so aider comes up in Architect Mode with no flags,
and it carries a `read:` list holding the rest of the spec's Beginning
context: `data_types.py`, `constants.py`, `llm.py`, `pyproject.toml`, and
`transcript.txt`. Those are the ones the spec marks `(readonly)`, and `read:`
is aider's word for the same idea. The command line holds the two files the
spec says may change.

Then, in aider:

1. Paste the whole of `spec.md`. All five sections, in one message.
2. **The plan stops and waits.** `auto-accept-architect: false` is set on
   purpose. Read the plan before you accept it. Nothing has been written to
   disk yet, so this is the cheapest place in the entire workflow to notice
   that the model misunderstood you.
3. Accept. The editor turns the plan into files: `src/output_format.py` and
   `src/chart.py` created, `src/arg_parse.py` and `src/main.py` updated.
4. Run it:

   ```sh
   uv run main transcript.txt --chart bar --output-format json
   ```

   You should get JSON on stdout and a `chart.png` on disk.

`./reset` puts it back so you can run it again.

## What to actually watch for

**If aider asks "Add file to the chat?", say no.** Type `S` to skip all of
them. The default is Yes, and Yes is the expensive answer in Architect Mode:
adding a file re-runs the architect, the second reply is usually "you can
proceed as described" rather than a plan, and the editor then builds from that
instead of from the plan you read. You get fewer files than you asked for and
no error anywhere. This demo's config loads every readonly file up front so
the question should not come up, but it is worth knowing why the answer
matters, because it will come up somewhere else.

**Read the plan.** It is the only artifact in this workflow that is cheap to
fix. A plan that has misread the spec costs you one keystroke to reject; the
same misunderstanding caught after the edit costs you a `/undo`, a rewrite,
and another few minutes of model time.

**Check the flags actually got defined.** The failure worth knowing is the
quiet one: a run that exits 0 and does nothing. Two commands tell you the
difference:

```sh
uv run main transcript.txt --output-format json | head -3
uv run main transcript.txt | head -3
```

If those two print the same thing, the flag was accepted and ignored. That is
worse than a crash, because no exit code will tell you.

**Compare it to L03.** Same codebase, same model, and the change L04 asks for
is bigger than the one L03 could not land. The difference is that this time
the file list, the ordering, and the constraints were written down before the
model saw them.

## Try it on the 4B

```sh
./reset --model 4b
```

Same spec, smaller model in both seats. This is the honest test of whether a
spec is doing the work: the 4B has less capacity to infer what you left out,
so anything vague in the spec shows up as something wrong in the output. If
the 4B lands the spec and the 9B lands the spec, the spec is carrying its
weight.

## Configuration

`aider.conf.yml`, `aider.model.settings.yml`, and `aider.model.metadata.json`
are the same three files you have in `aider-practice`, pointed at this
project. `./reset` copies them into the working copy with their leading dots.
The differences from L03's copies are worth a look: `edit-format: architect`
and `editor-model` set up the two seats, `auto-accept-architect: false` is
what makes the plan stop, and `num_ctx` is larger because a spec plus four
files plus a plan is more than L03 ever held at once.

The metadata file prices both local models at frontier rates on purpose, so
`/tokens` shows you what the session would have cost if you were paying for
it.

`matplotlibrc` pins matplotlib's backend to `Agg`. That is not a style
choice. On macOS the default backend opens a window, and a `plt.show()` the
model added on its own initiative would block the program until somebody
closed it. With `Agg`, `savefig()` still writes the PNG and nothing blocks.
