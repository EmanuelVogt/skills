---
name: ca-spec-driven
description: Spec-driven feature work in 4 phases — Specify, Design, Tasks, Execute — sized by complexity; atomic tasks and commits, Execute delegated to workers in waves plus an independent Verifier. Triggers on "specify/discuss feature", "design", "tasks", "implement", "validate", "verify work", "UAT", "record decision", "pause/resume work".
license: CC-BY-4.0
metadata:
  author: Emanuel Vogt - github.com/EmanuelVogt
  version: 1.0.0
  based-on: TLC Spec-Driven 3.2.0 by Felipe Rodrigues (github.com/felipfr), CC-BY-4.0 — carries the 2026-08-17 fork's delegation model (Execute delegated to workers in waves from 4 tasks up, wave/cluster parallelism over vertical slices, English-only artifacts)
---

# CA Spec-Driven Development

Plan and implement features with precision. Granular tasks. Clear dependencies. Right tools. Zero ceremony.

```
┌──────────┐   ┌──────────┐   ┌─────────┐   ┌─────────┐
│ SPECIFY  │ → │  DESIGN  │ → │  TASKS  │ → │ EXECUTE │
└──────────┘   └──────────┘   └─────────┘   └─────────┘
   required      optional*      optional*     required

* Agent auto-skips when scope doesn't need it
```

## Critical Rules (read before acting)

**Loading this skill's files.** Reference files live under `references/` in this skill's own directory (where this `SKILL.md` resides). Resolve them relative to the skill directory — never the workspace root — and load them through the active skill by name; never assume a fixed install path. A card or a section you open is **read to its end** — never act on a truncated read; the long references are opened by section, never whole.

**Execution contract — every task, non-negotiable (holds even if you do not open the reference files):**

1. Tests derive from the spec's acceptance criteria and assert spec-defined outcomes — they never mirror the implementation.
2. The gate must pass (tests pass) before a task is done — the test runner decides, not self-assessment.
3. One atomic commit per task. Never batch tasks; never weaken, skip, or delete tests to make them pass.
4. After the LAST task, a fresh **Verifier always runs automatically** (author ≠ verifier) — spec-anchored outcome check + discrimination sensor. It is never optional and never prompted. See Sub-Agent Delegation.
5. **The orchestrator never implements a clustered plan.** From 4 tasks up, Execute is delegated to cheap workers — one per cluster, all clusters of a wave in parallel; pulling a cluster into the planning window is a violation, not a shortcut. A plan of **≤3 tasks** is the exception: the planning window implements it inline under the per-task cycle, and a fresh Verifier still closes it. See Sub-Agent Delegation.
6. **Everything this skill writes is English.** Every artifact under `.specs/` (`spec.md`, `context.md`, `design.md`, `tasks.md`, `validation.md`, `STATE.md`, lessons), feature folder names, task titles, wave reports and every payload to a worker, scout, runner or Verifier. Agents are the only readers and re-read each artifact on every turn for the life of the spec; another language costs ~30–40 % more tokens per read. The user's language is for the chat reply only. Quote in the original only what belongs to the product (a UI label, an error message, a domain term with no English equivalent), inside English sentences. The rule binds the agent on its own; a project may additionally enforce it with a hook that rejects a `.specs/` write reading as non-English prose (in Claude Code, a `specs-in-english` hook) — never assume one exists.

**Before Execute:** read [cards/orchestrator.md](references/cards/orchestrator.md) whole (≈4 kB) — the orchestrator's complete contract; [implement.md](references/implement.md) and [sub-agents.md](references/sub-agents.md) only by section, for a rule's rationale; confirm the wave/cluster plan (from `tasks.md`, or derived inline when Tasks was skipped) passes the cross-check, then dispatch wave 1. Workers and the Verifier do **not** read those references whole — each payload points at its card, [cards/worker.md](references/cards/worker.md) or [cards/verifier.md](references/cards/verifier.md), the complete operating contract for that role; the full references are consulted only by section, for the rationale of a single rule.

## Auto-Sizing: The Core Principle

**The complexity determines the depth, not a fixed pipeline.** Before starting any feature, assess its scope and apply only what's needed:

| Scope       | What                     | Specify                                                 | Design                                          | Tasks                         | Execute                                               |
| ----------- | ------------------------ | ------------------------------------------------------- | ----------------------------------------------- | ----------------------------- | ----------------------------------------------------- |
| **Small**   | ≤3 files, one sentence   | One-liner spec (inline)                                 | Skip                                            | Skip                          | Inline in the planning window + Verifier (light)      |
| **Medium**  | Clear feature, <10 tasks | Spec (brief, ≤ ~8 kB)                                   | Skip — design inline (or ≤ ~8 kB)               | Skip — inline wave plan       | ≤3 tasks → light: inline in the planning window, 1 Build gate at end, Verifier (light); 4+ tasks → vertical clusters in parallel waves + Verifier |
| **Large**   | Multi-component feature  | Full spec + requirement IDs                             | Architecture + components                       | Full breakdown + wave plan    | 2–4 vertical clusters per wave, one worker each + Verifier |
| **Complex** | Ambiguity, new domain    | Full spec + [discuss gray areas](references/discuss.md) | [Research](references/design.md) + architecture | Breakdown + wave plan         | Same (2–4 vertical clusters per wave) + [interactive UAT](references/validate.md) |

**Rules:**

- **Specify and Execute are always required** — you always need to know WHAT and DO it
- **Execute is delegated from 4 tasks up** — the execution model follows the task count, not the scope label: 4+ tasks go to workers, ≤3 run inline in the planning window. The Verifier is dispatched either way (see Sub-Agent Delegation)
- **Design is skipped** when the change is straightforward (no architectural decisions, no new patterns)
- **Tasks is skipped** when there are ≤3 obvious steps (they become the inline Execution Plan of Light Execute)
- **Discuss is triggered within Specify** when the agent detects ambiguous gray areas that need user input, or when the feature has any implicit-requirement dimension present (persistence/state, external calls, auth, payments, concurrency, state transitions)
- **Interactive UAT is triggered within Execute** only for user-facing features with complex behavior

**Safety valve:** Even when Tasks is skipped, Execute ALWAYS starts by listing atomic steps inline — with `Depends on` and `Touches` per step. **≤3 steps** run as [Light Execute](references/sub-agents.md) — inline in the planning window, no worker, no waves. **4+ steps or complex dependencies** fold into waves/clusters (see [implement.md](references/implement.md)) — if that reveals >5 steps, STOP and create a formal `tasks.md`; the Tasks phase was wrongly skipped.

## .specs Structure

```
.specs/
├── STATE.md            # Project memory: Decisions log (AD-NNN) + Handoff snapshot
├── LESSONS.md          # Self-improving lessons playbook (rendered by scripts/lessons.py — do not hand-edit)
├── lessons.json        # Canonical lessons state (machine-owned)
└── features/
    ├── [feature]/       # In progress
    │   ├── spec.md         # Requirements with traceable IDs
    │   ├── context.md      # User decisions for gray areas (only when discuss is triggered)
    │   ├── design.md       # Architecture & components (only for Large/Complex)
    │   ├── tasks.md        # Atomic tasks with verification (only for Large/Complex)
    │   └── validation.md   # Verifier report: PASS/FAIL, per-AC evidence, sensor result, diff range
    └── done/
        └── [feature]/   # Completed — move here on closeout (do NOT rename to <feature>-done)
            └── handoff-archive.md  # its STATE.md Handoff entries, moved here at closeout
```

All of it in English, including `[feature]` (a short English kebab-case slug: `guest-agenda-full-load`, not a slug in the user's language) — Critical Rule 6.

## Workflow

**New feature:**

1. Specify → (Design) → (Tasks) → Execute (depth auto-sized)

**Resume work:**

Read `.specs/STATE.md` — Handoff section for in-flight state, Decisions section to re-confirm active constraints — then propose the next step.

**Closeout (after Verifier PASS + merge local):**

Move `.specs/features/[feature]/` → `.specs/features/done/[feature]/` (keep the same folder name). Do **not** rename to `[feature]-done`. Move the feature's entries out of `.specs/STATE.md` § Handoff into `done/[feature]/handoff-archive.md` — the Handoff carries open work only ([memory.md](references/memory.md)).

## Context Loading Strategy

**On-demand load (only what the current task needs):**

- `.specs/STATE.md` — orchestrator only: Decisions section (read at Design, re-read on resume); Handoff section (read on resume only). Workers and the Verifier never read it — `design.md` carries the decisions a task needs
- confirmed lessons — load at Specify and Design via `python3 scripts/lessons.py list --status confirmed` ([lessons.md](references/lessons.md)); confirmed only, never candidates
- spec.md (when working on a specific feature)
- context.md (when designing or implementing from user decisions)
- design.md (when implementing from design)
- tasks.md (when executing tasks)

**Never load simultaneously:** multiple feature specs, multiple architecture docs. Size caps by scope, target <40k tokens loaded and the monitoring footer: [context-limits.md](references/context-limits.md).

## Sub-Agent Delegation

**Always on from 4 tasks up, never offered.** The window that planned the feature is the orchestrator: for a clustered plan it dispatches, collects and records — it never implements a cluster, never runs a test itself. Four tasks → one worker; forty tasks → many workers, in parallel; ≤3 tasks it implements inline (§ *Light Execute*), and the Verifier is dispatched all the same. Full mechanics — roles, clustering algorithm with worked example, dispatch protocol, payload templates, git protocol, compact summary, failure handling, Verifier — in [sub-agents.md](references/sub-agents.md); the rules below are the ones that get broken by an orchestrator who never opened it.

- **Roles:** orchestrator (planning window) · **workers** (one per cluster) · **scout** (finds code, returns `file:line`) · **runner** (runs the main window's gates — the Build gate and the Final gate — returning exit code + literal failures) · **Verifier** (fresh, independent). Workers run their own scoped gates, redirected to a log, and nest a scout for a question they cannot scope; the Verifier nests the runner for its Final gate; scouts and runners never nest further. The four roles ship as templates under this skill's `agents/` directory — `spec-worker.md`, `repo-scout.md`, `shell-runner.md`, `spec-verifier.md` (in Claude Code, install them into `.claude/agents/`); the nesting rules bind each agent on its own, and a project may additionally enforce them with a hook. Where sub-agents do not exist at all, *Degraded mode* below is the fallback.
- **Cards, not references.** A worker's whole contract is [cards/worker.md](references/cards/worker.md), the Verifier's [cards/verifier.md](references/cards/verifier.md), the orchestrator's own [cards/orchestrator.md](references/cards/orchestrator.md) — ≈4 kB each, the only file each role reads whole; the long references only by section. Workers and the Verifier never read `STATE.md`; the orchestrator reads it one section at a time.
- **Tier is judgement per dispatch, never hard-coded** — passed as `model` on every call: mechanics → **low** (haiku in Claude Code; payload forbids reformatting); everything else, root config/tooling/CI/docs/tests included → **mid** (sonnet), the default; domain entities/transitions, transaction/outbox/ambient-context work, migrations, contract regen, ADR-governed rule → **high** (opus). Verifier mid by default, high only for auth, payments, availability/booking rules, data integrity (P0). Twice failed at one tier → one tier up. State the tier in the wave report. Table: sub-agents.md § *Model selection*.
- **Waves and clusters — always parallel where the graph allows:** a **cluster** = ordered tasks sharing files/deps, one worker; a **wave** = clusters with no dependency and no file in common, dispatched **concurrently**; **exclusive** tasks (contract regen, migrations, lockfile/root config, shared `dist`) get a wave of their own. A cluster is a **vertical slice of 4–8 tasks** (domain, ports, repos, api, tests of one area, wiring last), **2–4 clusters per wave**; a single-task cluster only for an exclusive or genuinely isolated task, and ≥3 single-task non-exclusive clusters in one wave is a smell. Objective: fewest workers with disjoint ownership, then parallelism, then small clusters. Authored in Tasks (cross-check table); re-derived inline when Tasks was skipped. ≤3 tasks → Light Execute (no worker: the planning window implements inline, one gate at the end).
- **Per wave:** dispatch all clusters in one message (payload ≤ ~150 words, pointers not rules) → wait for every compact summary → **Build gate once** through the runner (scoped to the wave's touched areas; full unit only for a wave marked `full-unit`; never per task, never inside a worker) → record in `tasks.md` (orchestrator is the only `.specs/` writer during Execute) → one line to the user → next wave. Workers share one checkout: file ownership is absolute (a worker needing an unowned file STOPS), commits are pathspec-limited, `stash`/`add -A`/`commit -a`/branch ops are forbidden.
- **Verifier (always-on, never prompted):** fresh after the last wave — **author ≠ verifier**, evidence-or-zero. Spec-anchored outcome check against each AC's declared proof (`test` | `gate` | `probe`) · the **Final gate** (the one full-suite run) · discrimination sensor sized by risk (Light 1–2 · default 3 · P0 ≥5; inject once, run once) · writes `validation.md` once · returns a compact verdict + ranked gaps · distills lessons from grounded failures ([lessons.md](references/lessons.md)). Gaps → fix tasks → re-verify by resuming the same Verifier; bounded to 3 iterations, then escalate.
- **Turn budget ≈120 per agent**, `HANDOFF:` block on overrun → re-dispatch same type and tier with the block pasted first; returns ≤1.5 kB.
- **Degraded mode (no sub-agents):** say so first, then execute cluster by cluster in wave order in the current window under the same ownership/git/gate rules, and run `validate.md` as a fresh-eyes pass at the end. Never fall back silently.

## Commands

**Feature-level (auto-sized):**
| Trigger Pattern | Reference |
|----------------|-----------|
| Specify feature, define requirements | [specify.md](references/specify.md) |
| Discuss feature, capture context, how should this work | [discuss.md](references/discuss.md) |
| Design feature, architecture | [design.md](references/design.md) |
| Break into tasks, create tasks | [tasks.md](references/tasks.md) |
| Implement task, build, execute | [implement.md](references/implement.md) |
| Validate, verify, test, UAT, walk me through it | [validate.md](references/validate.md) |

**Memory:**
| Trigger Pattern | Reference |
|----------------|-----------|
| Record decision, this is a project-level decision | [memory.md](references/memory.md) |
| Pause work, end session, I need to stop | [memory.md](references/memory.md) |
| Resume work, continue, pick up where we left off | [memory.md](references/memory.md) |
| Load lessons, what have we learned, apply past lessons | [lessons.md](references/lessons.md) |
| Record lesson, distill lessons (auto-runs after validation) | [lessons.md](references/lessons.md) |

## Knowledge Verification Chain

Any technical decision walks, in strict order: **codebase → project docs (incl. `.specs/STATE.md` Decisions) → Context7 MCP → web search → flag as uncertain**. Never skip to "uncertain" while a step is available; step 5 is always flagged, never presented as fact; **never assume or fabricate** an API, pattern or behavior — "I don't know" beats a cascading failure across design → tasks → implementation. Full chain and rules: [design.md](references/design.md) § *Research*.

## Output Behavior

**Model split is built in:** Specify, Design and Tasks run in the planning window; a clustered Execute runs in workers, scouts, runners and the Verifier at the tier the orchestrator picks per dispatch (a ≤3-task plan runs inline, and its Verifier is still a dispatch). Never pull a cluster into the planning window because a tier proved weak — raise the tier.

Be conversational, not robotic. Report per wave in one line (clusters dispatched with their tiers / done, gate result), not per task. The chat reply follows the user's language; everything written to disk or sent to a sub-agent is English (Critical Rule 6) — a spec discussed in the user's language is still recorded in English.

## Code Analysis

Use available tools with graceful degradation. See [code-analysis.md](references/code-analysis.md).
