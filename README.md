# EECS 498 AASE Materials

Slides and handouts for EECS 498-016, Applied Agentic Software
Engineering, University of Michigan, Fall 2026.

## Layout

- `lectures/` holds one folder per lecture (`L01`, `L02`, ...), each
  with a `slides.md`, a `slides.pdf`, and a `slides.pptx`.
- `labs/` holds one folder per lab (`Lab00`, `Lab01`, ...), same shape.
- `demos/` holds the codebases the live demos run on, one folder per demo,
  named for the lecture it belongs to (`L01-notes-cli`,
  `L03-transcript-analytics`). Each has a README and a `reset` script: run
  `./reset` and it builds you a disposable working copy, configured and ready
  for aider. Run the demo yourself; that is why they are here.

The `slides.md` is the Slidev source the deck was built from. It is here
so you can read, search, or reuse the content. It expects a theme that
lives outside this repo, so it will not build as-is.

`git clone --depth 1` is the one you want if you only came for a deck or a
demo. Most of this repo's history is compiled slides.

Decks are posted around the time each lecture or lab is delivered.
If a week is missing, it has not happened yet.

## Links

- Course site: https://eecs498-aase.github.io
- Questions: Ed, or eecs-aase-staff@umich.edu
