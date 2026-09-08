# transcript-analytics

The small codebase the L03 live demo runs on, and the one L04 and L05 come
back to. Five Python files, no dependencies, no API keys.

To get it, clone this repo (`--depth 1` skips the history, which is mostly
compiled slide decks):

```sh
git clone --depth 1 https://github.com/eecs498-aase/materials.git
cd materials/demos/transcript-analytics
```

If you have Python 3.10 or newer you can run it right now:

```sh
python3 src/main.py transcript.txt
python3 src/main.py transcript.txt --top 5 --speakers
```

`--summarize` is the only thing that needs a model:

```sh
cp .env.example .env          # then edit if your Ollama is not on 11434
python3 src/main.py transcript.txt --summarize
```

If nothing is listening, it prints `summary unavailable` and the rest of the
report still works. That is on purpose.

## The five files

| File | Owns |
|------|------|
| `src/main.py` | counting, and printing the report |
| `src/arg_parse.py` | every command-line flag |
| `src/constants.py` | the stopword list and the tuning values |
| `src/data_types.py` | the shapes the analysis passes around |
| `src/llm.py` | the one call to a model |

The split is the point. A change to the command line touches `arg_parse.py`.
A change to the report touches `main.py`. Most changes touch both, and an
aider session that has only one of them in context produces half a change
that looks finished.

## Trying the demo yourself

The lecture demo is five steps against `qwen3.5:9b`. Copy it out of your
clone first. Aider commits as it goes, and you want those commits in a
throwaway repo you can delete, not on top of this one:

```sh
cp -R demos/transcript-analytics ~/l03-demo && cd ~/l03-demo
git init -q && git add -A && git commit -qm "before"
aider src/main.py
```

Delete `~/l03-demo` and copy it again for a clean run.

Then, in aider:

1. `Add a new CLI argument --output-format with choices text, json, markdown.`
   Watch it write a whole `arg_parse.py` it has never seen. Compare the
   invented one to the real one: it hardcodes `default=10` where the real
   file reads `DEFAULT_TOP_N`. Aider offers to add the file. **Say no** (`S`
   declines a whole run of those offers), so that edit is discarded and only
   the `main.py` edit lands.
2. Run the program: `python3 src/main.py transcript.txt`. It is broken, and
   the diff looked fine. The flag was never defined, because the file that
   defines flags was never in context.
   (If instead the model asked for the file and wrote nothing, say
   `Do it in src/main.py only. Do not touch any other file.` and you land in
   the same place.)
3. `/undo`, then `/add src/arg_parse.py`, then the **same prompt as step 1**,
   word for word. Now it holds together and the program runs.
4. `/tokens` after each step, then `/drop` and `/add src/` and `/tokens`
   again. Watch the number, and watch the repo map line shrink as you add
   files.
5. `/model ollama_chat/qwen3.5:4b` and run step 1 again. Compare. The
   provider prefix is not optional: bare `/model qwen3.5:4b` does not match
   `.aider.model.settings.yml` and aider falls back to defaults.

`git reset --hard <first commit>` puts it back so you can run it again.

## Configuration

`.aider.conf.yml`, `.aider.model.settings.yml`, and
`.aider.model.metadata.json` are the same three files you have in
`aider-practice`, pointed at this project. The metadata file prices both
local models at frontier rates on purpose, so `/tokens` shows you what the
session would have cost if you were paying for it.
