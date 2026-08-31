---
theme: ../../lectures/theme
title: "Lab 00: Setup Lab"
info: |
  EECS 498 AASE — Lab 00 (Setup Lab)
  Applied Agentic Software Engineering, UMich Fall 2026
layout: title
class: text-left
transition: fade
mdc: true
highlighter: shiki
---

# Welcome to AASE

## Lab 00 · Setup Lab · Aug 31 – Sep 1, 2026

<!--
Nothing today is graded. Say that out loud, twice.
Staff intros in person, by name. Then straight to the survey - it takes ten
minutes and they can be doing it while you talk through the next slides.
-->

---
layout: default
---

<div class="label">Step 1 · 10 minutes · start now</div>

# Join Ed, take the survey

<div class="mt-4 space-y-2">

1. Open Canvas. Click the **Ed** link. Join
2. Find the survey post on Ed. Open it

</div>

<div class="mt-10">

![Ed](./assets/ed-logo.png){width=92px class="rounded-2xl"}

</div>

<!--
Say these out loud rather than putting them on the slide:
- Sign in with umich.edu.
- It asks for your GitHub username. No username, no repo on Tuesday.
- If your laptop can't serve a model, say so on the hardware questions. That
  answer is what gets you a machine that can. Responses stay editable.
While the room fills it in, talk through the next five slides. Don't start the
steps until most hands are down.
-->

---
layout: default
---

<div class="label">The model · Ollama</div>

# Local LLMs on your machine

<div class="mt-4 space-y-2">

- `ollama pull` downloads a model. `ollama serve` runs it
- Free, private, no API key. It's just *yours*
- Small models fit a laptop. Bigger ones want the CAEN GPUs

</div>

<!--
While they fill in the survey. The pull is about 3 GB for the week-1 model; on
macOS opening the Ollama app replaces ollama serve. If your laptop can't take
it, the hardware questions on the survey are what get you a machine that can.
-->

---
layout: default
---

<div class="label">The tool · aider</div>

# Our programming tool

<div class="mt-4 space-y-2">

- A pair programmer in your terminal: describe a change, it edits your files
- Every edit is a git commit, so you can always *undo*
- It talks to whatever model Ollama is running. That's the whole stack

</div>

<!--
aider has no model inside. It's a client; you supply the server, which is why
the course costs nothing and why your model is a line of config rather than a
vendor. Don't preview L01 content here; today the tools just need to exist in
their heads.
-->

---
layout: section
---

# The steps

## Work at your own pace. Raise a hand.

<!--
Stop talking here. From this point the room works and staff circulate.
Leave the deck up so they can page through it themselves.
-->

---
layout: default
---

<div class="label">Step 2 · on your laptop</div>

# Clone `aider-ollama`

```bash
git clone https://github.com/eecs498-aase/aider-ollama.git
cd aider-ollama
python3 -m pip install aider-install && aider-install
```

<div class="mt-4 space-y-2">

- Its **README** has every step below, in more detail

</div>

<!--
Put the URL on the board: github.com/eecs498-aase/aider-ollama
HTTPS on purpose. Nobody sets up an SSH key today.
-->

---
layout: default
---

<div class="label">Step 3 · on your laptop</div>

# Serve a model

<div class="mt-4 space-y-2">

1. Install Ollama from **ollama.com/download**
2. Then, in the `aider-ollama` clone:

</div>

```bash
ollama serve &
ollama pull qwen3.5:4b
```

<div class="caption mt-4">About 3 GB. Let it finish.</div>

---
layout: default
---

<div class="label">Step 4 · on your laptop</div>

# Point aider at it

```bash
cp .env.local .env
bin/check
aider
```

<div class="caption mt-6">All green? You're done with the part that matters. A red line? Read it, then grab a TA.</div>

<!--
bin/check tests every hop between aider and the model. The one trap worth
naming out loud: a model with no settings entry gets a 2048-token context,
aider truncates your files, and the model starts inventing functions that
exist three lines further down. It reads as a stupid model. It's a
misconfiguration, and bin/check catches it.
-->

---
layout: default
---

<div class="label">Step 5 · on a CAEN machine</div>

# Same thing, with a GPU

```bash
bin/install-aider
bin/install-ollama

loginctl enable-linger $USER
ollama serve & ollama pull qwen3.5:9b
cp .env.local .env && bin/check
```

<div class="caption mt-4">Pull once. Your models are there at every lab machine.</div>

<!--
Two install scripts instead of a download, because nobody is root on these
machines. The rest is steps 3 and 4 again with a model twice the size.
enable-linger, once, or logging out kills ollama serve and it reads as a crash.
Behind the scenes, not for the slide: home is NFS. Ollama and the models live
there on purpose, so a pull follows them to every machine. aider is the one
thing that cannot start from a network home, so bin/install-aider builds it on
the machine's local disk and leaves a launcher that rebuilds it, about a
minute, at a machine that does not have it. If someone asks why the first
`aider` at a new machine takes a minute, that is why. They never manage it.
There is a third arrangement, aider on your laptop against the CAEN GPU over an
SSH tunnel. It's in the README. Not today.
-->

---
layout: default
---

<div class="label">Before you leave</div>

# Checklist

<v-clicks>

- On Ed
- Survey submitted
- `bin/check` all green

</v-clicks>

<div class="caption mt-6">Anything red? Read the repo's README, then grab a TA. There's no lab next week.</div>

<!--
Say the last line plainly. Week 2 is Labor Day, there is no lab, and the setup
gate is Fri Sep 11. Office hours are the venue between here and there.
-->

---
layout: end
---
