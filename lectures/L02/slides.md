---
theme: ../theme
title: "L02: How LLMs Code (Under the Hood)"
info: |
  EECS 498 AASE — Lecture 02
  Applied Agentic Software Engineering, UMich Fall 2026
layout: title
class: text-left
transition: fade
mdc: true
highlighter: shiki
---

# How LLMs Code (Under the Hood)

## Lecture 02 · Sep 3, 2026

<!--
Open the box. Theory lecture. No live coding today.
The payoff lands next lecture (L03) when the Big Three framework arrives.
-->

---
layout: statement
---

The developer who has internalized the mechanics has an *enormous* advantage.

<!--
The opener: why bother with theory. When it doesn't work, mental models win.
-->

---
layout: default
---

<div class="label">Four ideas</div>

# Today's mechanics

<div class="grid grid-cols-2 gap-6 mt-8 items-stretch">
  <div class="card">
    <ph-text-aa-bold class="text-3xl text-blue-600 mb-3" />
    <div class="font-semibold mb-1">Tokenization</div>
    <div class="text-sm opacity-70 flex-1">How the model sees your code.</div>
  </div>
  <div class="card">
    <ph-resize-bold class="text-3xl text-blue-600 mb-3" />
    <div class="font-semibold mb-1">Context window</div>
    <div class="text-sm opacity-70 flex-1">The only resource that matters.</div>
  </div>
  <div class="card">
    <ph-eye-slash-bold class="text-3xl text-blue-600 mb-3" />
    <div class="font-semibold mb-1">Hallucination</div>
    <div class="text-sm opacity-70 flex-1">Why the model makes things up.</div>
  </div>
  <div class="card">
    <ph-scales-bold class="text-3xl text-amber-600 mb-3" />
    <div class="font-semibold mb-1">Capability vs Knowledge</div>
    <div class="text-sm opacity-70 flex-1">Two axes of model improvement.</div>
  </div>
</div>

---
layout: section
---

# Tokenization

## What the model sees

---
layout: default
---

<div class="label">BPE intuition</div>

# Tokens, not words

<div class="mt-6">

- The model does not see characters
- The model does not see words
- The model sees **tokens** — chunks it has seen in training

</div>

<div class="caption mt-4">Byte-pair encoding: merge most common pairs, repeat until ~100K vocab.</div>

---
layout: default
---

<div class="label">Byte-pair encoding, worked</div>

# Where `getOrderById` goes

```text
1. start from characters
   g e t O r d e r B y I d                    12 tokens

2. merge the commonest adjacent pair. repeat, ~100K times
   e+r -> er      g+et -> get      O+rder -> Order

3. the merges that survived training are the vocabulary
   get  Order  By  Id                          4 tokens
```

<div class="caption mt-4">Nobody chose those four. They are just the pieces that were common enough to earn a slot.</div>

---
layout: default
---

<div class="label">o200k_base · the GPT-4o and 5 encoding</div>

# Real tokens, real IDs

<div style="font-family:'IBM Plex Mono',monospace;font-size:1.05em;color:var(--c-ink-soft);background:var(--c-code-bg);border:1px solid var(--c-rule);border-radius:6px;padding:.5rem .8rem;margin-top:1.4rem;display:inline-block">const order = await getOrderById(orderId);</div>

<div style="display:flex;flex-wrap:wrap;gap:.4rem;margin-top:1.2rem">
<div style="display:flex;flex-direction:column;min-width:0"><div style="font-size:.58em;text-align:center;color:var(--c-ink-muted);font-family:'IBM Plex Mono',monospace;padding-bottom:.3rem">1671</div><div style="font-family:'IBM Plex Mono',monospace;font-size:1.02em;white-space:pre;padding:.4rem .55rem;border-radius:6px;background:rgba(46,91,255,.09);border:1px solid var(--c-rule);color:var(--c-ink)">const</div></div>
<div style="display:flex;flex-direction:column;min-width:0"><div style="font-size:.58em;text-align:center;color:var(--c-ink-muted);font-family:'IBM Plex Mono',monospace;padding-bottom:.3rem">2569</div><div style="font-family:'IBM Plex Mono',monospace;font-size:1.02em;white-space:pre;padding:.4rem .55rem;border-radius:6px;background:var(--c-bg-2);border:1px solid var(--c-rule);color:var(--c-ink)">·order</div></div>
<div style="display:flex;flex-direction:column;min-width:0"><div style="font-size:.58em;text-align:center;color:var(--c-ink-muted);font-family:'IBM Plex Mono',monospace;padding-bottom:.3rem">314</div><div style="font-family:'IBM Plex Mono',monospace;font-size:1.02em;white-space:pre;padding:.4rem .55rem;border-radius:6px;background:rgba(46,91,255,.09);border:1px solid var(--c-rule);color:var(--c-ink)">·=</div></div>
<div style="display:flex;flex-direction:column;min-width:0"><div style="font-size:.58em;text-align:center;color:var(--c-ink-muted);font-family:'IBM Plex Mono',monospace;padding-bottom:.3rem">4021</div><div style="font-family:'IBM Plex Mono',monospace;font-size:1.02em;white-space:pre;padding:.4rem .55rem;border-radius:6px;background:var(--c-bg-2);border:1px solid var(--c-rule);color:var(--c-ink)">·await</div></div>
<div style="display:flex;flex-direction:column;min-width:0"><div style="font-size:.58em;text-align:center;color:var(--c-ink-muted);font-family:'IBM Plex Mono',monospace;padding-bottom:.3rem">717</div><div style="font-family:'IBM Plex Mono',monospace;font-size:1.02em;white-space:pre;padding:.4rem .55rem;border-radius:6px;background:rgba(217,119,6,.16);border:1px solid rgba(217,119,6,.55);color:var(--c-ink)">·get</div></div>
<div style="display:flex;flex-direction:column;min-width:0"><div style="font-size:.58em;text-align:center;color:var(--c-ink-muted);font-family:'IBM Plex Mono',monospace;padding-bottom:.3rem">4861</div><div style="font-family:'IBM Plex Mono',monospace;font-size:1.02em;white-space:pre;padding:.4rem .55rem;border-radius:6px;background:rgba(217,119,6,.16);border:1px solid rgba(217,119,6,.55);color:var(--c-ink)">Order</div></div>
<div style="display:flex;flex-direction:column;min-width:0"><div style="font-size:.58em;text-align:center;color:var(--c-ink-muted);font-family:'IBM Plex Mono',monospace;padding-bottom:.3rem">1582</div><div style="font-family:'IBM Plex Mono',monospace;font-size:1.02em;white-space:pre;padding:.4rem .55rem;border-radius:6px;background:rgba(217,119,6,.16);border:1px solid rgba(217,119,6,.55);color:var(--c-ink)">By</div></div>
<div style="display:flex;flex-direction:column;min-width:0"><div style="font-size:.58em;text-align:center;color:var(--c-ink-muted);font-family:'IBM Plex Mono',monospace;padding-bottom:.3rem">906</div><div style="font-family:'IBM Plex Mono',monospace;font-size:1.02em;white-space:pre;padding:.4rem .55rem;border-radius:6px;background:rgba(217,119,6,.16);border:1px solid rgba(217,119,6,.55);color:var(--c-ink)">Id</div></div>
<div style="display:flex;flex-direction:column;min-width:0"><div style="font-size:.58em;text-align:center;color:var(--c-ink-muted);font-family:'IBM Plex Mono',monospace;padding-bottom:.3rem">33050</div><div style="font-family:'IBM Plex Mono',monospace;font-size:1.02em;white-space:pre;padding:.4rem .55rem;border-radius:6px;background:rgba(46,91,255,.09);border:1px solid var(--c-rule);color:var(--c-ink)">(order</div></div>
<div style="display:flex;flex-direction:column;min-width:0"><div style="font-size:.58em;text-align:center;color:var(--c-ink-muted);font-family:'IBM Plex Mono',monospace;padding-bottom:.3rem">906</div><div style="font-family:'IBM Plex Mono',monospace;font-size:1.02em;white-space:pre;padding:.4rem .55rem;border-radius:6px;background:var(--c-bg-2);border:1px solid var(--c-rule);color:var(--c-ink)">Id</div></div>
<div style="display:flex;flex-direction:column;min-width:0"><div style="font-size:.58em;text-align:center;color:var(--c-ink-muted);font-family:'IBM Plex Mono',monospace;padding-bottom:.3rem">2245</div><div style="font-family:'IBM Plex Mono',monospace;font-size:1.02em;white-space:pre;padding:.4rem .55rem;border-radius:6px;background:rgba(46,91,255,.09);border:1px solid var(--c-rule);color:var(--c-ink)">);</div></div>
</div>

<div class="caption mt-8">11 tokens for 42 characters. The four amber ones are exactly what the last slide predicted, and <code>Id</code> is token 906 <em>both</em> times.</div>

<!--
This is the payoff for the previous slide: getOrderById really does come
back as get / Order / By / Id, and here are the numbers.

Two things to point at if there is time. The dot in the middle of a chip
is a leading space, which is part of the token, so " order" and "order"
are different tokens. And "(order" is one token: the tokenizer swallowed
the paren with the word, which is why token counts are hard to guess.

Caveat if asked: these IDs are o200k_base. qwen3.5 uses a different
vocabulary, so the numbers differ. The idea does not.
-->

---
layout: default
---

<div class="label">Two consequences</div>

# What tokenization costs you

<div class="grid grid-cols-2 gap-6 mt-8 items-stretch">
  <div class="card">
    <ph-currency-dollar-bold class="text-3xl text-blue-600 mb-3" />
    <div class="font-semibold mb-1">Unit of cost</div>
    <div class="text-sm opacity-70 flex-1">Verbose code costs more — in dollars on a vendor, in RAM and seconds on your own machine.</div>
  </div>
  <div class="card">
    <ph-eye-bold class="text-3xl text-blue-600 mb-3" />
    <div class="font-semibold mb-1">Unit of attention</div>
    <div class="text-sm opacity-70 flex-1">Every token competes for focus. Your identifiers fragment into common pieces, so they carry no special weight.</div>
  </div>
</div>

---
layout: two-col
---

## 9 tokens

```python
def f(x):
    return x * 2
```

::right::

## ~35 tokens

```python
def calculate_double_of_input_value(
    input_value: int
) -> int:
    """Return value times two."""
    return input_value * 2
```

<!--
Same function. Verbose costs 4× more.
Not "more informative" — more expensive and more distracting.
-->

---
layout: section
---

# Context Window

## The only resource that matters

---
layout: default
---

<div class="label">Inside vs outside</div>

# What the model sees

<div class="mt-6 space-y-2">

- **Inside the window**: files, history, repo map, system prompt
- **Outside the window**: *nothing*
- No DB. No web fetch. No retrieval

</div>

<div class="caption mt-6">This is the single most important fact about LLMs for an engineer.</div>

---
layout: default
---

<div class="label">Why bigger ≠ better</div>

# Three costs of large context

<div class="grid grid-cols-3 gap-6 mt-8 items-stretch">
  <div class="card">
    <ph-currency-dollar-bold class="text-3xl text-blue-600 mb-3" />
    <div class="font-semibold mb-1">Cost</div>
    <div class="text-sm opacity-70 flex-1">Tokens billed, or RAM and seconds on your own box. Attention is quadratic: 2× context ≈ 4× work.</div>
  </div>
  <div class="card">
    <ph-clock-bold class="text-3xl text-blue-600 mb-3" />
    <div class="font-semibold mb-1">Latency</div>
    <div class="text-sm opacity-70 flex-1">Tens of seconds to first token on a laptop where a tight prompt starts at once.</div>
  </div>
  <div class="card">
    <ph-warning-bold class="text-3xl text-rose-600 mb-3" />
    <div class="font-semibold mb-1">Quality</div>
    <div class="text-sm opacity-70 flex-1">Needle-in-haystack: bigger can be <em>worse</em>.</div>
  </div>
</div>

<!--
Rose accent on the surprising one — quality degradation.
-->

---
layout: default
---

<div class="label">One step of generation</div>

# Weighing the whole window

<svg viewBox="0 0 900 250" class="w-full mt-4" role="img" aria-label="One token being generated, with weighted links back to every token already in the window">
<path d="M450 82 Q 276 145 102 176" fill="none" stroke="var(--c-primary)" stroke-width="1.9" opacity="0.22"/>
<path d="M450 82 Q 334 145 218 176" fill="none" stroke="var(--c-primary)" stroke-width="5.2" opacity="0.59"/>
<path d="M450 82 Q 392 145 334 176" fill="none" stroke="var(--c-primary)" stroke-width="1.5" opacity="0.17"/>
<path d="M450 82 Q 450 145 450 176" fill="none" stroke="var(--c-primary)" stroke-width="2.1" opacity="0.24"/>
<path d="M450 82 Q 508 145 566 176" fill="none" stroke="var(--c-primary)" stroke-width="1.6" opacity="0.19"/>
<path d="M450 82 Q 566 145 682 176" fill="none" stroke="var(--c-primary)" stroke-width="5.8" opacity="0.64"/>
<path d="M450 82 Q 624 145 798 176" fill="none" stroke="var(--c-primary)" stroke-width="4.5" opacity="0.51"/>
<rect x="50" y="176" width="104" height="46" rx="7" fill="var(--c-bg-1)" stroke="var(--c-rule)"/>
<text x="102" y="205" text-anchor="middle" fill="var(--c-ink)" style="font-family:'IBM Plex Mono',monospace;font-size:19px">import</text>
<rect x="166" y="176" width="104" height="46" rx="7" fill="var(--c-bg-1)" stroke="var(--c-rule)"/>
<text x="218" y="205" text-anchor="middle" fill="var(--c-ink)" style="font-family:'IBM Plex Mono',monospace;font-size:19px">httpx</text>
<rect x="282" y="176" width="104" height="46" rx="7" fill="var(--c-bg-1)" stroke="var(--c-rule)"/>
<text x="334" y="205" text-anchor="middle" fill="var(--c-ink)" style="font-family:'IBM Plex Mono',monospace;font-size:19px">…</text>
<rect x="398" y="176" width="104" height="46" rx="7" fill="var(--c-bg-1)" stroke="var(--c-rule)"/>
<text x="450" y="205" text-anchor="middle" fill="var(--c-ink)" style="font-family:'IBM Plex Mono',monospace;font-size:19px">resp</text>
<rect x="514" y="176" width="104" height="46" rx="7" fill="var(--c-bg-1)" stroke="var(--c-rule)"/>
<text x="566" y="205" text-anchor="middle" fill="var(--c-ink)" style="font-family:'IBM Plex Mono',monospace;font-size:19px">=</text>
<rect x="630" y="176" width="104" height="46" rx="7" fill="var(--c-bg-1)" stroke="var(--c-rule)"/>
<text x="682" y="205" text-anchor="middle" fill="var(--c-ink)" style="font-family:'IBM Plex Mono',monospace;font-size:19px">httpx</text>
<rect x="746" y="176" width="104" height="46" rx="7" fill="var(--c-bg-1)" stroke="var(--c-rule)"/>
<text x="798" y="205" text-anchor="middle" fill="var(--c-ink)" style="font-family:'IBM Plex Mono',monospace;font-size:19px">.</text>
<rect x="392" y="32" width="116" height="50" rx="8" fill="var(--c-amber)"/>
<text x="450" y="65" text-anchor="middle" fill="var(--c-bg-0)" style="font-family:'IBM Plex Mono',monospace;font-size:21px;font-weight:600">get</text>
</svg>

<div class="caption mt-4">Thicker line, more weight. It leans on <code>httpx</code> and the dot, but it scored <em>every</em> token to find that out.</div>

<!--
Walk it: the model is choosing what follows "httpx." and to do that it
scores every token already in the window, not just the nearby ones.
Thickness is attention weight. Then the setup for the next slide: this
whole picture happens again for the token after "get", and again after
that.
-->

---
layout: default
---

<div class="label">Why cost grows faster than context</div>

# Every token attends to every other

| Tokens in the window | Pairs scored | Relative work |
|---|---:|---:|
| 1K | 1,000,000 | 1× |
| 2K | 4,000,000 | 4× |
| 8K | 64,000,000 | 64× |
| 32K | 1,024,000,000 | *1024×* |

<div class="caption mt-6">Double the context, quadruple the work. The window is a budget, not a container.</div>

<!--
The number to land: 32× the text is not 32× the cost, it is 1000×.
This is why "just paste the repo in" fails on a laptop.
-->

---
layout: default
---

<div class="label">Pedagogy of /add</div>

# Aider's friction is the lesson

```text
/add main.py        → file enters context
/drop main.py       → file leaves context
/tokens             → see exactly what's in the window
/clear              → reset history (keep files)
```

<div class="caption mt-4">Not a limitation. The discipline you'd want anyway.</div>

---
layout: default
---

<div class="label">The long session</div>

# Context drift

<div class="mt-6 space-y-2">

- History accumulates: every turn you sent, every turn it returned
- Fifty messages in, most of the window is *dead weight*
- The model can't separate what's true now from what was true at message 3

</div>

<div class="caption mt-6"><code>/clear</code> between tasks. Claude Code (L05) compacts for you, and compaction is lossy.</div>

---
layout: statement
---

<div class="label">Chat break · 5 min</div>

Talk to your neighbor: when a long chat *degrades*, what is happening inside the window?

<!--
0:35. The fixed break. Prompt is the chat_break field in overview.md.

Think about a long conversation with an assistant that got worse toward
the end. What did you do — new chat? re-explain? Now say what was
actually happening, in today's vocabulary.

Don't police vocabulary. The point is translating their own experience
into the model we just built. Two or three answers out loud, then move.
-->

---
layout: section
---

# Hallucination

## The misleading word

---
layout: default
---

<div class="label">What's actually happening</div>

# The model is doing what it was trained to do

<v-clicks>

- Autoregressive sampling
- Pick most likely next token from a distribution
- No fact-check step
- No DB lookup
- No "wait, does this exist?"

</v-clicks>

<!--
"Hallucination" sounds like a mistake. It's not a mistake — it's the design.
-->

---
layout: default
---

<div class="label">Why "requests" not "httpx"</div>

# Statistical priors win when context is silent

<v-clicks>

- Training data: 100× more `import requests` than `import httpx`
- Your project uses httpx
- Prompt doesn't mention it
- Model produces `requests` — plausible, wrong for *your* context

</v-clicks>

<!--
Not "made up" — wrong real library for the wrong real project.
-->

---
layout: default
---

<div class="label">Three flavors in code</div>

# Common hallucinations

<div class="grid grid-cols-3 gap-6 mt-8 items-stretch">
  <div class="card">
    <ph-function-bold class="text-3xl text-rose-600 mb-3" />
    <div class="font-semibold mb-1">Invented APIs</div>
    <div class="text-sm opacity-70 flex-1">user.get_profile() — plausible, not real.</div>
  </div>
  <div class="card">
    <ph-clock-counter-clockwise-bold class="text-3xl text-rose-600 mb-3" />
    <div class="font-semibold mb-1">Stale knowledge</div>
    <div class="text-sm opacity-70 flex-1">pandas 1.x APIs in a 2.0 codebase.</div>
  </div>
  <div class="card">
    <ph-warning-circle-bold class="text-3xl text-rose-600 mb-3" />
    <div class="font-semibold mb-1">Wrong signatures</div>
    <div class="text-sm opacity-70 flex-1">Wrong kwarg, wrong dtype — subtle.</div>
  </div>
</div>

---
layout: statement
---

When the model needs a fact, *show it the fact*.

<!--
The deepest reason to manage context: accuracy. Not cost. Not speed.
-->

---
layout: default
---

<div class="label">The limit</div>

# What context cannot fix

<div class="mt-6 space-y-2">

- "What's the latest version of our internal library?"
- The answer isn't in your repo either, so no `/add` produces it
- The model guesses, *plausibly*, and you cannot tell from the output

</div>

<div class="caption mt-6">Hand it the fact, or build a tool that looks the fact up. You build those in week 5.</div>

---
layout: section
---

# Capability vs Knowledge

## Two axes

---
layout: two-col
---

## Capability

<div class="mt-6 space-y-3">
  <div><strong>Reasoning skill.</strong> Multi-step, cross-file, holding constraints.</div>
  <div><strong>Scales with</strong>: model size.</div>
  <div><strong>qwen3.5:4b → 9b → frontier</strong>.</div>
</div>

::right::

## Knowledge

<div class="mt-6 space-y-3">
  <div><strong>What the model read</strong>. Recency. Niche depth.</div>
  <div><strong>Scales with</strong>: training data size + freshness.</div>
  <div><strong>Small + recent</strong> can beat large + old.</div>
</div>

<!--
Two axes. Confusing them = bad model choices.
-->

---
layout: default
---

<div class="label">The ladder · you live on the bottom two rungs</div>

# Why not the top rung?

<div class="grid grid-cols-3 gap-6 mt-8 items-stretch">
  <div class="card">
    <ph-number-circle-four-bold class="text-3xl text-blue-600 mb-3" />
    <div class="font-semibold mb-1">qwen3.5:4b</div>
    <div class="text-sm opacity-70 flex-1">~2.5 GB. Fails fast and fails obviously. Where you start.</div>
  </div>
  <div class="card">
    <ph-number-circle-nine-bold class="text-3xl text-blue-600 mb-3" />
    <div class="font-semibold mb-1">qwen3.5:9b</div>
    <div class="text-sm opacity-70 flex-1">~6 GB at Q4. The course default. Part 2 of aider-practice needs it.</div>
  </div>
  <div class="card">
    <ph-buildings-bold class="text-3xl text-amber-600 mb-3" />
    <div class="font-semibold mb-1">Frontier</div>
    <div class="text-sm opacity-70 flex-1">Someone else's datacenter. Strong on both axes. You will not run one in this course.</div>
  </div>
</div>

<div class="caption mt-6">A frontier model covers for you. A 4B <em>doesn't</em>. Two weeks from now you'll have run 4b and 9b and felt the gap yourself.</div>

<!--
Don't assert this — promise the experiment. Everyone runs the same repo on
4b and then 9b over the next two weeks. That beats any benchmark I could
show. Be clear that frontier is the rung they are NOT on: it is here to
name what they are giving up and why, not as something they get access to.
-->

---
layout: default
---

<div class="label">Choosing</div>

# Match model to task

<v-clicks>

- **Cost-sensitive batch** (1000× repeats) → smallest model that clears the bar
- **Reasoning-heavy single task** → the most capable model you have
- **Niche library or framework** → capability won't save you. That's a *context* problem
- **Anything you're learning on** → the rung that fails where you erred

</v-clicks>

<div class="caption mt-6">Usually right in production, usually wrong in a classroom. The skill is telling which room you're in.</div>

---
layout: section
---

# Diagnostic

## When output is wrong

---
layout: default
---

<div class="label">Ask in order</div>

# Three questions

1. **Context** — did the model have what it needed?
2. **Hallucination** — did it invent an API?
3. **Capability or knowledge** — task too hard? too new?

<div class="caption mt-6">Tokenization is not on the list. It sits underneath all three and is almost never what you can act on.</div>

---
layout: statement
---

Tools wrap the model. The *core inference call* has no lookup.

<!--
Why doesn't the model just look things up? Because the core inference doesn't.
Tools wrap it. You build those in week 5.
-->

---
layout: default
---

<div class="label">Four mechanics</div>

# What to take away

<div class="mt-6 space-y-2">

- **Tokens** are the unit of cost and the unit of attention
- **The context window** is the only resource that matters. Spend it deliberately
- **Hallucination** is pattern completion with no lookup. Fix it with context
- **Capability and knowledge** are different axes. Big against recent

</div>

<div class="caption mt-6">Four mechanics. Every failure you hit this term is one of them wearing a costume.</div>

---
layout: default
---

<div class="label">This week</div>

# `aider-practice` Part 1

<div class="mt-6 space-y-2">

- Setup gate and all sixteen lessons due **Fri Sep 11**
- Re-read your own Aider chat logs with today's vocabulary
- Every mechanic from this lecture is *already in them*

</div>

<div class="caption mt-6">Next: L03, the Big Three. Tuesday.</div>

---
layout: end
---

---
layout: default
---

<div class="label">Go deeper · optional</div>

# YouTube Deep Dives

<div class="grid grid-cols-2 gap-6 mt-8 items-stretch">
  <div class="card">
    <ph-text-aa-bold class="text-3xl text-blue-600 mb-3" />
    <div class="text-xs uppercase tracking-widest opacity-60 mb-1" style="font-family:'IBM Plex Mono',monospace">Tokenization</div>
    <div class="font-semibold mb-2">Let's build the GPT Tokenizer</div>
    <a href="https://www.youtube.com/watch?v=zduSFxRajkE" class="text-sm break-all">youtube.com/watch?v=zduSFxRajkE</a>
  </div>
  <div class="card">
    <ph-eye-bold class="text-3xl text-blue-600 mb-3" />
    <div class="text-xs uppercase tracking-widest opacity-60 mb-1" style="font-family:'IBM Plex Mono',monospace">Attention</div>
    <div class="font-semibold mb-2">Attention in transformers, step-by-step</div>
    <a href="https://www.youtube.com/watch?v=eMlx5fFNoYc" class="text-sm break-all">youtube.com/watch?v=eMlx5fFNoYc</a>
  </div>
</div>

<div class="caption mt-6">Neither is required. Both go a level below today.</div>

<!--
Leave this up while the room files out. Not assessed, not required.
The tokenizer video is long; tell them the first 30 minutes is the part
that pays for itself.
-->
