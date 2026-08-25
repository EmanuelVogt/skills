# Role templates

The four delegation roles of **CA Spec-Driven Development**, as ready-to-install sub-agent
definitions. The skill's prose names them; these files are what makes them real:

| File | Role |
| --- | --- |
| `spec-worker.md` | Implements ONE cluster of tasks in a wave — scoped gate, one atomic commit per task. |
| `spec-verifier.md` | Independent Verifier after the last wave — spec-anchored coverage, Final gate, mutation sensor. |
| `repo-scout.md` | Answers "where is X" in a context that gets discarded — returns `file:line`, never file content. |
| `shell-runner.md` | Runs one command, absorbs the log, returns exit code + literal failures. |

## Install

Copy the four files into the harness's sub-agent directory — in Claude Code, `.claude/agents/`
(project) or `~/.claude/agents/` (all projects). Claude Code loads agent definitions at session
start: **restart the session after installing**. Nothing else needs editing — the templates
resolve the skill's own `references/` at runtime and read whatever agent guide the project ships.

## The `model:` field

Each file's frontmatter `model:` is only a **default tier** for that role. The orchestrator picks
a tier per dispatch — low / mid / high by the risk of the cluster — and passes it explicitly;
that choice wins over the file. Keep the defaults unless a whole role is consistently mis-tiered
in your project.

## Without them

The skill still runs: see § *Sub-Agent Delegation* in `SKILL.md` for Degraded mode, where the
main session does the work inline, one wave at a time, and pays for every log it reads.
