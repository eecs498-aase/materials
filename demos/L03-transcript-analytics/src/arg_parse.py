"""Every command-line flag this program accepts.

This module owns the parser. If a flag is not built here, `main.py` cannot
see it no matter what `main.py` says about it -- which is the whole point of
the L03 demo.
"""

import argparse

from constants import DEFAULT_TOP_N


def build_parser() -> argparse.ArgumentParser:
    """Build the argument parser for the transcript analyzer."""
    parser = argparse.ArgumentParser(
        prog="transcript-analytics",
        description="Count words and speakers in a meeting transcript.",
    )
    parser.add_argument(
        "transcript",
        help="path to the transcript file to analyze",
    )
    parser.add_argument(
        "--top",
        type=int,
        default=DEFAULT_TOP_N,
        metavar="N",
        help=f"how many frequent words to report (default: {DEFAULT_TOP_N})",
    )
    parser.add_argument(
        "--speakers",
        action="store_true",
        help="include the per-speaker breakdown",
    )
    parser.add_argument(
        "--summarize",
        action="store_true",
        help="ask the local model for a one-paragraph summary",
    )
    return parser


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse argv (or sys.argv when argv is None)."""
    return build_parser().parse_args(argv)
