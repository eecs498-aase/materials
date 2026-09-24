---
theme: ../theme
title: "L08: Hackathon 1 Briefing"
info: |
  EECS 498 AASE — Lecture 08
  Applied Agentic Software Engineering, UMich Fall 2026
layout: title
class: text-left
transition: fade
mdc: true
highlighter: shiki
---

# Hackathon 1 briefing

## Lecture 08 · Sep 24, 2026

<!--
Two things today. L07 is not finished, and it goes first. Then this: the briefing for tonight.

Keep a laptop handy. The last ten minutes are a setup check, and a problem found now is cheaper than one found at check-in.

Direction: this deck starts at the chat break, after the rest of the L07 deck. If L07 finished early, start here early.
-->

---
layout: default
---

<div class="label">Chat break</div>

# Habits with a stronger model

Tonight Aider runs a far stronger model, still on a 32K budget.

Write one line: one habit from aider-practice that matters *more* with a stronger model, and one that matters less.

Be ready to say why.

<!--
OK, Zoom, we're on break.

Five minutes. One line each in the chat.

When they come back, take three or four answers. Good ones on the "more" side: reading the diff before accepting it, because a strong model writes plausible code faster than you can check it; keeping the chat small; committing in small steps. On the "less" side: rewording a prompt five times to get a small model to follow a format.

The point to land: a better model moves the bottleneck to you reading and deciding. It does not remove it.

OK, Zoom, we're back.
-->

---
layout: default
---

<div class="label">Tonight</div>

# The evening at a glance

| | |
|---|---|
| **When** | Tonight, 7 to 9 PM |
| **Where** | Leinweber 1355 |
| **Work** | Individual |
| **Weight** | 9% of your grade |
| **Bring** | Your laptop and its charger |

<!--
Tonight, seven to nine, in Leinweber 1355. Two hours, on your own, and it is 9% of the course.

You work on your own laptop. There are no lab machines tonight, so bring the charger. Two hours on battery is not a bet to make.
-->

---
layout: statement
---

Tonight is about **taskr**. The rest is in your repository at *seven*.

<!--
That is everything I will say about the task. It is about taskr. What you do with it is in the repository you get at check-in, and not on any slide today.

Please do not ask me for more. The answer is the same for everyone: seven o'clock.
-->

---
layout: default
---

<div class="label">Format</div>

# How the evening works

- **Modular**: do as much as you can do well
- **Judged on evidence**, not feature count
- **The brief** is in your repository
- **Submit** by pushing before 9 PM

<!--
It is modular on purpose. Do as much as you can, and do it well. Doing less, properly, beats starting everything.

It is judged on evidence: what you can show working, and what you can explain. There is no point breakdown, and feature count is not the measure. Saying clearly what does not work is worth more than hoping nobody tries it.

Everything you need to know about the task is in the brief in your repository. Read it first.

Submitting means pushing to your repository before nine. The safety branch, which I will come to, pushes as you go, but push your main branch yourself at the end.
-->

---
layout: section
---

# The model

## gpt-5.6-luna, on your own key

<!--
Section divider. The model and the key.
-->

---
layout: default
---

<div class="label">What changes tonight</div>

# From qwen to gpt-5.6-luna

| | So far | Tonight |
|---|---|---|
| **Model** | `qwen3.5:9b` | `gpt-5.6-luna` |
| **Runs on** | Your laptop | OpenAI, through U-M |
| **Context** | 32K tokens | 32K, by design |
| **Class** | Small, open weights | Frontier, hosted |
| **Speed** | Your hardware | About 80 tokens a second |

<!--
Everything you have driven so far was a small open model, mostly the 9B on your own machine, with a 32K context.

Tonight every model call goes to gpt-5.6-luna. It is an OpenAI model, served through the U-M GPT Toolkit. It is a different class of model, far stronger at code, and when we measured it yesterday it produced about 80 tokens a second end to end.

That is why tonight is two hours of real building and not two hours of fighting the model. One row did not change, though, and that is the next slide.

One oddity. The Toolkit hands a streamed reply over in one burst at the end. A long answer shows nothing for a few seconds and then all of it. That is the gateway, not your code.

Direction: numbers from hackathons/toolkit-models.md, measured Sep 23.
-->

---
layout: statement
---

A *strong* model, on the **32K** budget you know.

<!--
Luna accepts over a million tokens of context. Tonight you get thirty-two thousand, the same budget you have worked to all term, in Aider and in the model call your own code makes.

That is deliberate. Aider is set to 32K and warns you when a chat goes past it. The model call in your repository refuses any request over 32K, and that limit is not yours to change. So you keep doing what you have done since aider-practice: only the files you are working on in the chat, the rest dropped, the chat cleared between tasks.

Why take a million-token window away? Because deciding what goes in front of the model is the skill this course is about. A huge window lets sloppy habits hide until the session gets slow, expensive and confused. Tonight you get a far better model, and you still work the way you did before.
-->

---
layout: default
---

<div class="label">Your key</div>

# The Toolkit key and its budget

- **Where**: toolkit.umgpt.umich.edu
- **Sign in**: your U-M account
- **Credit**: $25, the whole budget
- **Model**: `gpt-5.6-luna` only

<!--
The key comes from toolkit.umgpt.umich.edu. Sign in with your U-M account and create a key on that page.

It carries $25 of credit. That is the budget for every model call you make tonight.

Luna is the only model. The repository is already set up for it. Do not switch Aider to something bigger. It will not help you, and it spends the budget ten times faster.

Create the key before you arrive and keep it somewhere you can paste from.
-->

---
layout: default
---

<div class="label">Given: taskr/model.py</div>

# One request to the model

```python
body = {"model": "gpt-5.6-luna", "messages": messages}
if tools:
    body["tools"] = tools                   # actions the model may ask for
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}",   # your Toolkit key
}
request = urllib.request.Request(
    base_url + "/chat/completions",         # base_url ends in /v1
    data=json.dumps(body).encode(), headers=headers)
with urllib.request.urlopen(request) as response:
    reply = json.load(response)
message = reply["choices"][0]["message"]    # content, or tool_calls
```

<div class="caption mt-4">You call it: <code>call(messages, base_url=..., model=..., api_key=..., tools=...)</code></div>

<!--
This is the whole model call, and it is already in your repository, in taskr/model.py, with a comment on every step. You do not write it. You call it.

Top to bottom. The body names the model and carries the conversation, plus the tools when you pass them: the actions the model may ask your code to run. That is L07's request object.

The key goes in the Authorization header, as the word Bearer and then the key. That is the one line people get wrong when they write this themselves.

It POSTs to your base URL plus /chat/completions. The base URL already ends in /v1.

The reply's message is in the first choice. Either it has text in content, or it has tool_calls because the model wants an action run.

Your code passes call the messages, the tools and the settings from your .env, and gets that message back. A wrong key comes back as "model HTTP error 401", and the key itself never appears in the error.
-->

---
layout: default
---

<div class="label">Measured Sep 23</div>

# What $25 buys

| Run | Cost |
|---|---|
| A scripted run of the whole evening | $0.24 |
| Typical evening, estimated | About $1 |
| Heavy evening, estimated | $2 to $4 |

<div class="caption mt-6">The way to spend all $25: calling the model over and over, with nothing to stop it.</div>

<!--
Yesterday we ran a scripted strong student through the whole evening, with Aider held to the same 32K you will have. Total: 24 cents. The biggest single request was about 22 thousand tokens, so 32K was never in the way.

A typical evening is about a dollar. Someone who runs everything many times is two to four.

So there is one way to spend all $25, and it is yours to prevent: anything that calls the model over and over with nothing to stop it, sending a longer conversation each time. Each call costs more than the last, and one left running all evening can spend the whole key.

Aider prints the cost of every message. Glance at it.
-->

---
layout: default
---

<div class="label">Working with Luna</div>

# Using a strong model well

- **The 32K budget**: `/drop` files, `/clear` between tasks
- **Small commits**: one working step each
- **"Add file to the chat?"**: usually N

<!--
Inside 32K, Aider needs the same care it always did. Keep only the files you are working on in the chat. Drop the rest. Clear between tasks. If Aider warns that the chat is over 32K, that is your cue to clear, not to say yes.

One Aider prompt to answer No. When Luna's reply mentions a file that is not in the chat, Aider asks "Add file to the chat?". If the reply only mentions it, say N. Saying yes sends the reply back without applying its edit, and the change is gone. That one cost our test run the same edit twice.

Commit small working steps. Aider commits for you, and the smaller the step the easier the undo.
-->

---
layout: section
---

# Setup and recording

## Before you arrive, and the first ten minutes

<!--
Section divider. What you do before tonight, and what happens when you sit down.
-->

---
layout: default
---

<div class="label">Before tonight</div>

# Before you arrive

- **Laptop** and charger
- **Python 3.10+**, git, Aider 0.86.2
- **Your Toolkit key**, saved
- **GitHub push** without a password prompt

<!--
Laptop and charger.

Python 3.10 or newer, git, and Aider 0.86.2, the install you used for aider-practice. If aider --version works today, it works tonight.

Your Toolkit key, created and saved somewhere you can paste from.

And GitHub. Your repository pushes in the background after every commit, so git has to push without asking for a password. SSH is the reliable way. ssh -T git@github.com should greet you by name. The invitation goes to the GitHub username you gave in the start-of-term survey.
-->

---
layout: default
---

<div class="label">At check-in</div>

# The first ten minutes

1. **Check in** on the form
2. **Accept** your GitHub invitation
3. **Clone** your repository
4. **Run** the setup script

<div class="caption mt-6">The exact steps are on the screen tonight.</div>

<!--
The same for everyone.

Check in on the form when you sit down. It is how we know you are in the room, and it is what gets you a repository.

A few minutes later GitHub sends you an invitation to your own private repository. Accept it.

Clone it and run the setup script. That is the whole start.

The exact commands will be on the screen tonight. You do not need to copy anything now.
-->

---
layout: default
---

<div class="label">Required</div>

# Everyone runs bin/setup

1. **Run** `bin/setup`
2. **Paste** your Toolkit key when it asks
3. **Check** that every step says ok

<div class="caption mt-6">Anything says PROBLEM? Tell us straight away.</div>

<!--
Everyone must run bin/setup. It is not optional.

Run it, paste your key when it asks, and read what it prints. It checks everything for you: the key, the model, the recording of your Aider work, and pushing to GitHub. Every step should say ok.

If anything says PROBLEM, put your hand up straight away. Do not work around it. Fixed in minute three it takes five minutes. Found at half past eight, it can cost you your evidence.
-->

---
layout: default
---

<div class="label">Evidence</div>

# What gets recorded

- **Every Aider commit** carries its conversation
- **Every commit** snapshotted to `safety/<machine>`
- **`/undo`** works, and the undone change is kept
- **`bin/aider-log`** lists it all

<!--
Your Aider transcript is graded evidence, and you never have to remember to commit it. Every commit Aider makes carries .aider.chat.history.md, the conversation that produced that change.

Every commit also adds a snapshot to a branch named safety and your machine, and it is pushed to GitHub in the background. If your laptop dies at nine, your work is already on GitHub.

/undo still works exactly as you know it. The undone change stays on the safety branch, so nothing you try is lost, and you do not need to be careful with undo.

bin/aider-log shows every change Aider made with the prompt behind it, including the ones you undid.

Leave the safety branch and the hooks alone.
-->

---
layout: default
---

<div class="label">Setup check, now</div>

# The setup check

```text
python3 --version        # 3.10 or newer
git --version
aider --version          # 0.86.2
ssh -T git@github.com    # greets you by name
```

<div class="caption mt-6">Then sign in at toolkit.umgpt.umich.edu and check your key exists.</div>

<!--
Laptops open. Run these four, then sign in at the Toolkit site and make sure you have a key.

Hands up if any of them fails. Staff are walking the room. Fixing Python or SSH now takes five minutes. At check-in it takes twenty of your evening.

Direction: give this the last ten minutes. Walk the room.
-->

---
layout: end
---

<!--
Questions.

The answer to "what is the task" is: in your repository at check-in.

See you tonight.
-->
