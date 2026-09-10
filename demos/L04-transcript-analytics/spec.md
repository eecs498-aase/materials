# Spec: charts and structured output for transcript-analytics

## High-Level Objective

Add word frequency visualization and structured file output to the transcript
analytics CLI.

## Mid-Level Objectives

- CREATE output formatters that render a completed analysis as plain text,
  JSON, Markdown, and YAML.
- CREATE chart functions that draw the top-word counts as a bar, pie, or line
  chart and save the image to a PNG file.
- ADD `--chart` and `--output-format` to the command line and make `main.py`
  call the new functions.

Each one is checkable on its own: run the program with the new flag and look
at what comes out.

## Implementation Notes

- Plan in prose. Name each file, say what goes in it and why, and stop there.
  Do not write the code in the plan; writing it twice is the slowest way to
  get it once.
- The Context section below is the complete file list for this change. Do not
  ask for any other file and do not name one that is not on those two lists.
- `matplotlib` and `pyyaml` are already dependencies in `pyproject.toml`. Use
  them. Do not add any other dependency and do not edit `pyproject.toml`.
- Charts are written to a file, never displayed. Call `savefig()`. Do not call
  `plt.show()` and do not select a backend in code.
- The flags live in `src/arg_parse.py`. That file owns every command-line
  argument in this program, so a flag added anywhere else does not exist.
- Follow the patterns already in the project: type hints on every signature,
  a docstring on every function, standard library imports first.
- `TranscriptAnalysis.summary` is `None` unless `--summarize` was passed, so
  every formatter has to survive an absent summary.
- Keep the existing plain-text report exactly as it reads today. `--output-format
  text` is the default and its output must not change.

## Context

### Beginning context

- `src/main.py`
- `src/arg_parse.py`
- `src/data_types.py` (readonly)
- `src/constants.py` (readonly)
- `src/llm.py` (readonly)
- `pyproject.toml` (readonly)
- `transcript.txt` (readonly)

### Ending context

- `src/main.py` (updated)
- `src/arg_parse.py` (updated)
- `src/output_format.py` (new file)
- `src/chart.py` (new file)

## Ordered Low-Level Tasks

1. CREATE `src/output_format.py`: define `format_as_text`, `format_as_json`,
   `format_as_md`, and `format_as_yaml`. **All four take the same two
   arguments and return a string:** `(analysis: TranscriptAnalysis,
   show_speakers: bool) -> str`. The three that do not need `show_speakers`
   still accept it, so that task 4 can call any of them the same way. MOVE the
   body of `render_text()` from `src/main.py` into `format_as_text()`.
   `format_as_json` uses `dataclasses.asdict`; `format_as_yaml` uses
   `yaml.safe_dump`; `format_as_md` writes a Markdown table of the top words.

2. CREATE `src/chart.py`: define `create_bar_chart(analysis:
   TranscriptAnalysis, path: str) -> None`, `create_pie_chart(...)`, and
   `create_line_chart(...)` with the same two parameters. Each one plots
   `analysis.top_words`, labels the axes, titles the figure with
   `analysis.source`, and saves to `path` with `savefig()`. The bar chart is
   horizontal and sorted descending.

3. UPDATE `src/arg_parse.py`: ADD `--output-format` with choices `text`,
   `json`, `md`, `yaml`, defaulting to `text`. ADD `--chart` with choices
   `bar`, `pie`, `line` and no default. ADD `--chart-file`, defaulting to
   `chart.png`.

4. UPDATE `src/main.py`: REMOVE `render_text()`. ADD imports from
   `output_format` and `chart`. In `main()`, build a dict mapping each
   `--output-format` choice to its formatter function, look up
   `args.output_format`, and call the result as
   `formatter(analysis, args.speakers)`. Every value in that dict is a plain
   function reference taking those two arguments; do not wrap any of them in a
   lambda. Print what it returns. When `args.chart` is set, look up the
   matching chart function the same way and call it with `analysis` and
   `args.chart_file`.
