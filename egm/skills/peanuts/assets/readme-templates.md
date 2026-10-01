# README templates for /peanuts

Three shapes: leaf (peanuts), branch (hay), and root. Keep them short: a leaf
is about half a page, a branch about a page, the root one to two pages. Every
README ends with the retirement line, unchanged.

## Leaf README (a directory with code and no in-scope subdirectories)

```markdown
# <directory name>

<Purpose: what this directory is for and why it exists as its own unit.
Two to four sentences.>

## Files

- `file_a.py`: <one line on what it does>
- `file_b.py`: <one line on what it does>

*This README exists to give AI sessions cheap context. It can be retired once design docs cover the files in this directory at least once. See `/elephant` for the design doc process.*
```

## Branch README (a directory whose subdirectories already have approved READMEs)

```markdown
# <directory name>

<Purpose: this directory's role in the larger system.>

## How the parts fit

<Subsystem composition: how the subdirectories work together at this level,
drawn from their READMEs. Name each subdirectory and its job in a phrase.>

- `child_one/`: <its job, in a phrase>
- `child_two/`: <its job, in a phrase>

## Files at this level

- `module.py`: <one line on what it does>

*This README exists to give AI sessions cheap context. It can be retired once design docs cover the files in this directory at least once. See `/elephant` for the design doc process.*
```

## Root README (the map a fresh session reads first)

```markdown
# <project name>

<What the system does, in a paragraph.>

## Major subsystems

- `subsystem_a/`: <what it owns; when you would descend into it>
- `subsystem_b/`: <...>

## Where to start for common tasks

- <task>: start in `<path>`

## Files at this level

- `<file>`: <one line>

*This README exists to give AI sessions cheap context. It can be retired once design docs cover the files in this directory at least once. See `/elephant` for the design doc process.*
```
