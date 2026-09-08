"""notes - a very small note CLI.

Deliberately imperfect in two places, both of which the L01 demo fixes live:
parse_args() does not survive being called with no arguments, and dispatch()
is an if-chain. Keep this file short: it goes on a projector.
"""
import sys
from pathlib import Path

NOTES = Path("notes.txt")


def parse_args(argv):
    """Split argv into a command and its arguments."""
    return argv[0], argv[1:]


def read_notes():
    if not NOTES.exists():
        return []
    return [ln for ln in NOTES.read_text().splitlines() if ln.strip()]


def cmd_add(args):
    if not args:
        print("add: nothing to add")
        return 1
    with NOTES.open("a") as f:
        f.write(" ".join(args) + "\n")
    return 0


def cmd_list(args):
    notes = read_notes()
    if not notes:
        print("no notes yet")
        return 0
    for i, note in enumerate(notes, 1):
        print(f"{i}. {note}")
    return 0


def cmd_count(args):
    print(len(read_notes()))
    return 0


def dispatch(command, args):
    """Run one command by name."""
    if command == "add":
        return cmd_add(args)
    elif command == "list":
        return cmd_list(args)
    elif command == "count":
        return cmd_count(args)
    else:
        print(f"unknown command: {command}")
        return 1


def main(argv=None):
    command, args = parse_args(argv if argv is not None else sys.argv[1:])
    return dispatch(command, args)


if __name__ == "__main__":
    sys.exit(main())
