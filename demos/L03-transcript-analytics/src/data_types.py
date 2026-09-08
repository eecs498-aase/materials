"""The shapes the analysis passes around.

Plain dataclasses, no third-party dependencies. The demo has to run on a
podium machine with nothing installed but Python, so everything here is
standard library.
"""

from dataclasses import dataclass, field


@dataclass
class WordCount:
    """One word and how often it appeared."""

    word: str
    count: int


@dataclass
class Speaker:
    """One speaker and how much of the transcript belongs to them."""

    name: str
    lines: int
    words: int


@dataclass
class TranscriptAnalysis:
    """Everything the analyzer produces for a single transcript.

    `summary` stays None unless --summarize was passed and the local model
    answered, so every renderer has to treat it as optional.
    """

    source: str
    total_words: int
    unique_words: int
    average_word_length: float
    top_words: list[WordCount] = field(default_factory=list)
    speakers: list[Speaker] = field(default_factory=list)
    summary: str | None = None
