# Choosing Goldfish subagents per runtime

Read this when you are not in Claude Code, or when the Claude Code default in
SKILL.md does not apply.

## Contents

- The capability clause
- Runtime mapping table
- Cross-runtime symmetry
- Runtimes not listed
- Hermes `plan` profile

## The capability clause (the portable contract)

Spawn a **fresh, review-capable session with no shared conversation state**.
Isolated context is the requirement; the persona is a preference. Any runtime
that can start an isolated subagent session can run a Goldfish round. If yours
cannot, run each prompt by hand in a brand-new chat that has never seen the
design conversation, and paste the three reports back.

## Runtime mapping table

The Goldfish contract is identical across runtimes; only the subagent type name
changes.

| Runtime | Goldfish A (Comprehension) | Goldfish B (Critic) | Goldfish C (Readiness) |
|---|---|---|---|
| **Claude Cowork** | `general-purpose` | `general-purpose` | `Plan` |
| **Claude Code** | `generalist`* | `reviewer`* | `architect`* |
| **OpenClaw** | `generalist` | `reviewer` | `architect` |
| **Hermes** | `Main` | `Main` | `plan` profile (see below) |

\* Role-aligned custom subagents installed at
`~/.claude/agents/{generalist,reviewer,architect}.md`. **Fallback:** if they
are not installed, use `general-purpose` for A and B and `Plan` for C (the
Cowork row), since those ship with Claude Code.

Spawn primitives: Claude Code and Cowork use the `Agent` tool; OpenClaw uses
`sessions_spawn`; Hermes uses `delegate_task`.

## Cross-runtime symmetry

Claude Code and OpenClaw use the same three role-specific agents: `generalist`
for comprehension, `reviewer` for adversarial critique, `architect` for a
default-to-asking planner audit. In Claude Code they are custom subagents in
`~/.claude/agents/`; in OpenClaw they are workspace personas under
`~/.openclaw/agents/{generalist,reviewer,architect}/workspace/`. The
dispositions match, so the task prompt and the agent's system prompt push the
same direction in either runtime.

Cowork has no persistent home and no custom-agent registry, so it always runs
the built-in fallback row. Hermes lags: until a `plan` profile is installed, A
and B fall back to `Main` and C has no planner-class agent.

## Runtimes not listed

Use whichever fresh-context analytical subagent the runtime exposes for A and
B, and the closest planner-class agent for C (or the same analytical one). The
task prompts carry most of the role-setting work; the subagent choice is a
lens-sharpening nudge, not a load-bearer.

## Hermes `plan` profile

Add to `~/.hermes/config.yaml`:

```yaml
agent_profiles:
  plan:
    model: "<your preferred reasoning model>"
    system_prompt_file: "~/.hermes/profiles/plan.md"
    toolsets: ["file", "terminal"]
    max_iterations: 50
```

For the body of `~/.hermes/profiles/plan.md`, describe a software architect
agent that surfaces ambiguities as questions rather than producing confident
plans. OpenClaw's `~/.openclaw/agents/architect/workspace/SOUL.md` is a
workable starting point.
