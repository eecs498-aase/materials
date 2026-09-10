"""Transcript analytics: read a meeting transcript, report what is in it.

    uv run main transcript.txt
    uv run main transcript.txt --top 5 --speakers

Structure: `arg_parse.py` owns the flags, `constants.py` owns the tuning
values, `data_types.py` owns the shapes, `llm.py` owns the one call to a
model. This file does the counting and the printing.
"""

import sys
from collections import Counter

from arg_parse import parse_args
from constants import IGNORED_WORDS, SPEAKER_NAME_MAX_LEN, WORD_EDGE_PUNCTUATION
from data_types import Speaker, TranscriptAnalysis, WordCount
from llm import summarize


def split_speaker(line: str) -> tuple[str | None, str]:
    """Split "NAME: text" into ("NAME", "text").

    Returns (None, line) when the line has no speaker label, so continuation
    lines are still counted as words -- they just belong to nobody.
    """
    name, separator, rest = line.partition(":")
    if not separator or len(name) > SPEAKER_NAME_MAX_LEN or "\t" in name:
        return None, line
    return name.strip(), rest.strip()


def words_in(text: str) -> list[str]:
    """Lowercased words with edge punctuation stripped, empties dropped."""
    return [
        cleaned
        for token in text.split()
        if (cleaned := token.strip(WORD_EDGE_PUNCTUATION).lower())
    ]


def analyze(path: str, top_n: int) -> TranscriptAnalysis:
    """Count words and speakers in the transcript at `path`."""
    with open(path, encoding="utf-8") as handle:
        lines = handle.read().splitlines()

    all_words: list[str] = []
    per_speaker: dict[str, Speaker] = {}

    for line in lines:
        if not line.strip():
            continue
        name, said = split_speaker(line)
        spoken = words_in(said)
        all_words.extend(spoken)
        if name is None:
            continue
        # First time we see a name, start its tally; after that, add to it.
        speaker = per_speaker.setdefault(name, Speaker(name=name, lines=0, words=0))
        speaker.lines += 1
        speaker.words += len(spoken)

    # The frequency table is about the meeting, so the filler and the
    # function words come out before the top-N is taken.
    interesting = Counter(word for word in all_words if word not in IGNORED_WORDS)
    top_words = [WordCount(word=word, count=count) for word, count in interesting.most_common(top_n)]

    total_length = sum(len(word) for word in all_words)
    return TranscriptAnalysis(
        source=path,
        total_words=len(all_words),
        unique_words=len(set(all_words)),
        average_word_length=total_length / len(all_words) if all_words else 0.0,
        top_words=top_words,
        speakers=sorted(per_speaker.values(), key=lambda s: s.words, reverse=True),
    )


def render_text(analysis: TranscriptAnalysis, show_speakers: bool) -> str:
    """Render the analysis as the plain-text report."""
    out = [
        f"Transcript: {analysis.source}",
        f"  total words:   {analysis.total_words}",
        f"  unique words:  {analysis.unique_words}",
        f"  avg length:    {analysis.average_word_length:.2f}",
        "",
        f"Top {len(analysis.top_words)} words",
    ]
    for entry in analysis.top_words:
        out.append(f"  {entry.count:>4}  {entry.word}")

    if show_speakers and analysis.speakers:
        out.extend(["", "Speakers"])
        for speaker in analysis.speakers:
            out.append(f"  {speaker.words:>5} words  {speaker.lines:>3} lines  {speaker.name}")

    if analysis.summary:
        out.extend(["", "Summary", f"  {analysis.summary}"])

    return "\n".join(out)


def main(argv: list[str] | None = None) -> int:
    """Entry point. Returns the process exit code."""
    args = parse_args(argv)

    try:
        analysis = analyze(args.transcript, args.top)
    except OSError as error:
        print(f"could not read {args.transcript}: {error}", file=sys.stderr)
        return 1

    if args.summarize:
        with open(args.transcript, encoding="utf-8") as handle:
            analysis.summary = summarize(handle.read())
        if analysis.summary is None:
            print("summary unavailable (no model answered)", file=sys.stderr)

    print(render_text(analysis, show_speakers=args.speakers))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
