---
name: ca-full-cycle
description: End-to-end feature pipeline with ONE human gate before code — Research (grilling rounds + parallel code scouts; a raw concept is stress-tested before convergence), then autonomous Plan → Implement → Review — top-tier planning over mapped context, cheap workers in parallel waves, a verifier per wave, an independent Reviewer — closing with a human QA loop. Trigger on "full cycle", "research this and implement it", "resolve this end to end", "run the full cycle", "implement this autonomously", "QA findings", "resume full-cycle".
license: CC-BY-4.0
metadata:
  author: Emanuel Vogt - github.com/EmanuelVogt
  version: 1.0.0
  based-on: ca-spec-driven 1.0.0 (same author), itself derived from TLC Spec-Driven 3.2.0 by Felipe Rodrigues (github.com/felipfr), CC-BY-4.0. Keeps the wave/cluster delegation model, the tier-per-dispatch economics and the independent-verification stance; trims four phase gates down to one, adds a per-wave verifier and closes with a human QA loop.
---

# CA Full-Cycle — Research · Plan · Implement · Review

One human gate before code, one human loop after it. Everything between runs alone.

```
┌──────────┐   ┌────────┐   ┌───────────┐   ┌──────────┐   ┌────────┐
│ RESEARCH │ → │  PLAN  │ → │ IMPLEMENT │ → │  REVIEW  │ → │   QA   │
└──────────┘   └────────┘   └───────────┘   └──────────┘   └────────┘
 human + AI       AI            AI              AI           human
 (the gate)    top tier     worker waves    independent     fix loop
```

The human's job is to make the problem understood (Research) and to judge the result (QA). The
pipeline's job is everything else — and it never stops in the middle to ask whether it may continue.

## Critical Rules (read before acting)

**Loading this skill's files.** References live under `references/` in this skill's own directory.
Resolve them relative to the skill directory — never the workspace root. A card or a section you
open is **read to its end**. Sub-agents open the long references only by section, never whole; the
orchestrator reads its current phase reference whole.

1. **One gate before code.** The brief confirmation closes Research — the single pre-execution
   approval. From there to the end of Review the pipeline is autonomous: never ask permission to
   plan, to dispatch a wave, to run the Reviewer, or to fix a gap the machinery caught. The human
   returns at QA. The only mid-pipeline escalations are the bounded-failure valves (3 strikes), a
   worker's `spec-ambiguity` stop, and a discovery that invalidates the brief — those go to the
   user; nothing else does.
2. **Tests derive from the brief's ACs** and assert brief-defined outcomes — they never mirror the
   implementation. The gate (the test runner) decides a task is done, not self-assessment. Never
   weaken, skip, or delete a test to make it pass. A red that turns green on re-run with no code
   change is a flaky finding to report — never a pass to absorb.
3. **One atomic, pathspec-limited commit per task.** Never batch tasks into one commit.
4. **The orchestrator never implements a clustered plan.** From 4 tasks up, Implement is delegated
   to workers — one per cluster, all clusters of a wave in parallel; pulling a cluster into the
   planning window is a violation, not a shortcut. A plan of **≤3 tasks** runs inline in the
   planning window (light path) — and rules 5–6 still hold.
5. **Verification is structural, never prompted.** A fresh **wave verifier** closes every wave
   (gate + delivery check + one discrimination mutant); a fresh, independent **Reviewer** closes
   the feature (author ≠ reviewer, evidence-or-zero). Neither is optional, neither is offered as a
   question. Declared limit: the wave verifier anchors on the plan, the Reviewer on the brief — a
   wrong plan is caught by the brief-anchored close; a wrong brief is caught only by human QA.
   That is what QA is for.
6. **Artifacts in English, chat in the user's language.** Everything under `.ca-plans/` plus
   slugs, payloads, summaries and verdicts is English — agents are the only readers, and English
   re-reads are cheaper. The QA script is chat, so it follows the user; product text (UI labels,
   error messages) is quoted as-is.

## Sizing

No ceremony table — the task count decides, after Plan:

| Plan size | Implement | Wave verifier | Reviewer |
| --- | --- | --- | --- |
| **≤3 tasks** (light) | Inline in the planning window, per-task cycle, gates via the log-on-disk pattern | One, after the last task | Always — mid tier when non-P0, high otherwise |
| **4+ tasks** | Workers, one per cluster, waves in parallel | One per wave | Always — high tier by default |

## .ca-plans Structure

```
.ca-plans/
├── DECISIONS.md        # cross-run project decisions — lean AD log (below)
├── RUNS.md             # one entry per completed run: size, wall time, tokens, est. cost (review.md § Closeout)
└── [feature]/          # short English kebab-case slug (guest-agenda-load, not a translated one)
    ├── research.md     # the brief: problem, context map, decisions, ACs with proofs
    ├── plan.md         # born with the slug; statuses + wave plan + gate commands (plan-NN.md when segmented)
    └── review.md       # Reviewer report + QA findings log (≤ ~6 kB)
```

`plan.md` is born as a stub with the slug and is the run's whole state: the header `Status:` line —
`Research → Planning → Implementing (wave k/N) → Review → QA → Done`, each transition written the
moment the phase changes — cluster statuses (written at dispatch and at wave close), and, only when
a run pauses or blocks, a `## Handoff` section (implement.md § *Pause / blocked*). No per-run state
file beyond it. A brief whose ACs decompose into independently shippable slices segments at Plan
into sequential `plan-NN.md`, each closing its own Review and QA before the next is authored
(plan.md § *One plan or several?*); `research.md` § Segments carries the map.

**DECISIONS.md is the project's memory across runs.** One line per project-level decision:
`AD-nn · active | superseded by AD-mm · <decision> · <run slug, date>`. Appended when Research or
Plan settles something future runs must conform to (a convention, a boundary, a chosen pattern) —
feature-local D-nn stay in the run's `research.md`. Read at the start of every Research; an
`active` AD is a constraint the new brief conforms to or explicitly supersedes, never silently
ignores.

## Phases

| Phase | Who | Reference |
| --- | --- | --- |
| Research — intake, concept stress-test, scout fan-out, grilling, the brief, the gate | human + AI | [research.md](references/research.md) |
| Plan — tasks, clusters, waves, tiers; auto-proceeds | AI (top tier) | [plan.md](references/plan.md) |
| Implement — dispatch, collect, verify per wave | AI | [implement.md](references/implement.md) |
| Review + QA — independent review, QA script, correction loop | AI, then human | [review.md](references/review.md) |

**Resume:** step 0 — `git status --short`: a dirty tree means a worker died mid-task or a
verifier died between inject and restore; restore any modification no resumable cluster owns
(`git checkout -- <file>`) before anything else — a live mutant poisons every later gate. Then
read `.ca-plans/*/plan*.md` `Status:` lines, pick the open run (in a segmented run, the open
segment), re-read its `research.md` whole
(at `Status: QA`, `review.md` too) and check drift: `git diff --stat <Base>..HEAD` against the
brief's `Base:` hash — re-scout only the drifted areas of the Context Map, never trust a stale
map and never remap a fresh one. A `## Handoff` section is the interrupted state — act on it,
then delete it (it describes a moment, not the run). Cluster rows stuck at `running`: reconcile
against `git log` (commits are the truth — atomic per task), mark what landed `done <hash>`,
re-dispatch the remainder as the same clusters — dead agents cannot be resumed. Then continue at
the phase the status names.

## Sub-Agent Delegation

The window that ran Research and Plan is the orchestrator — the most expensive context in the
session. During Implement it dispatches, collects, records; it never edits code, never runs a test
itself (measured in ca-spec-driven's origin project: a worker pays a median 21 turns and 94k of
context before its first edit — which is why clusters are vertical slices, not single tasks).

| Role | Does | Tier per dispatch | Card / contract |
| --- | --- | --- | --- |
| **Scout** | Maps code during Research and audits Touches during Plan: returns `file:line` + one-line facts, never file content, ≤1.5 kB | low for a pointed question, mid for a module map | contract in the payload |
| **Worker** | Executes ONE cluster: tasks in order, tests from ACs, scoped gate logged to disk, atomic commit each | low mechanics · **mid default** · high domain-critical | [cards/worker.md](references/cards/worker.md) |
| **Wave verifier** | Closes a wave, alone: runs the wave gate itself, checks delivery against the plan, kills one mutant on the wave's riskiest task, returns PASS/gaps | mid · high for a P0/exclusive wave | [cards/wave-verifier.md](references/cards/wave-verifier.md) |
| **Reviewer** | Closes the feature, fresh and independent: AC evidence check, Final gate, discrimination sensor, `review.md` | high default; mid only for light non-P0 runs | [cards/reviewer.md](references/cards/reviewer.md) |
**Tier is judgement per dispatch, never hard-coded** — passed as `model` on every call (Claude
Code: haiku/sonnet/opus). Worker high is narrow: domain entities/transitions, transactions/outbox,
migrations, contract regen, an ADR-governed rule. **P0** (auth, payments, money movement,
availability/booking, data integrity) raises the Reviewer to high even on a light run. Twice failed
at one tier → one tier up (measured in the parent's origin project: a high-tier agent costs ≈5× a
mid-tier one — spend it where a wrong answer costs a re-verify loop, not by habit).

**Harness mapping (Claude Code):** workers/verifiers/Reviewer dispatch as
`Agent(subagent_type: "general-purpose", model: <tier>)` with the card path in the payload; scouts
as the native `Explore` agent. Of ca-spec-driven's installed role templates, prefer only
`repo-scout` — the others (`spec-worker`, `spec-verifier`, `shell-runner`) embed the parent's
contract and artifact paths and will hunt files that do not exist here. **Resuming a live
sub-agent** (fix loops, gap re-checks) is `SendMessage` to the agent id from its dispatch result,
held in the orchestrator's context; agents die with the session, so after a restart every "resume"
degrades to a fresh dispatch carrying the resumed scope. **No heavy command raw in a window** —
any gate or count an agent runs itself uses the log-on-disk pattern (worker card § 4): output to a
file, `grep`/`head` back the ≤30 lines that matter. **Degraded mode (no sub-agents):** say so
first, then run cluster by cluster in wave order in the current window under the same
ownership/git/gate rules, with a self-review pass at the end (reduced assurance — same window,
author ≠ reviewer does not hold). Never fall back silently.

## Model Economics (the point of the pipeline)

- **Research**: scouts are low/mid and disposable; every important fact lands in the main window —
  the context map is the asset the whole run spends from.
- **Plan**: happens in the main window, on top of that mapped context. If the session is not on a
  top-tier model when Plan starts, say one line — "plan phase: a top-tier model pays for itself
  here; switch with /model, or I continue on the current one" — then continue either way. Never
  block on it; `/model` is the user's.
- **Implement**: the expensive window orchestrates; cheap workers type. Payloads ≤ ~150 words,
  summaries ≤1.5 kB — every character a sub-agent returns is paid on every later orchestrator turn.
- **Review**: one high-tier fresh read of the whole diff beats three mid-tier passes over slices —
  it is the last independent check before a human sees the work.

## Output Behavior

Be conversational, not robotic. One line per wave (clusters + tiers dispatched / done, verifier
verdict), never per task. Chat in the user's language; disk and payloads in English (Rule 6). The
main window targets <40 k tokens of loaded artifacts: `research.md` ≤ ~8 kB, `plan.md` ≤ ~10 kB,
`review.md` ≤ ~6 kB — a line that is neither an AC, a decision, a task field, evidence nor a
status does not belong in them.
