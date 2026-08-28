# Plan — top tier, mapped context, no gate

**Goal:** turn the confirmed brief plus the live context map into `plan.md` — atomic tasks, a
wave/cluster layout that runs everything the dependency graph allows in parallel, gate commands,
and a tier per cluster. Then **proceed**: the plan is announced in one chat line, never submitted
for approval (SKILL.md Rule 1 — the brief was the gate).

This phase runs in the main window on purpose: the scouts' context map is already resident, and
planning quality is the highest-leverage token spend of the run. Do not re-discover what Research
mapped; a scout is dispatched here only for the Touches audit below.

## 0. One plan or several? (segment before you author)

A brief can be bigger than any one plan should be. Before authoring tasks, check: do the ACs
decompose into **independently shippable slices** — each a coherent subset a user could QA on its
own? If yes AND a single plan would blow its caps (~20 tasks or ~10 kB) or weld unrelated
verticals into one epic, **segment**: sequential `plan-01.md`, `plan-02.md`…, each a complete
pipeline of its own — waves → wave verifiers → Reviewer → QA loop → `Status: Done` — before the
next segment's plan is authored. Write the map into `research.md` § Segments (segment · AC ids ·
status), one line each.

- Slice by AC subsets (verticals), never by layer — "backend plan / frontend plan" is the epic
  smell wearing a costume.
- Author segment k+1 ONLY after segment k closes: it plans on top of what actually landed, not on
  a guess. The map line reserves its scope; the detail waits. A later segment invalidated by an
  earlier QA costs one map-line edit, not a re-plan.
- Segment k+1 needs no new gate — the brief already confirmed every AC; each segment's QA is the
  human contact. `RUNS.md` gets one entry per segment.
- The common case stays common: one shippable slice → one `plan.md`, none of this ceremony.

## 1. Tasks

Break the work into atomic tasks — ONE component / function / endpoint / file-change each, tests
travelling with their code (never a shared "write the tests" task). Every task carries:

```
### T<n>: [imperative title]
Touches: [every file it creates or modifies, tests included — exhaustive and honest]
Depends on: [task IDs | none]
Exclusive: [yes only for: migration, contract/codegen regen, lockfile/root config, shared dist]
Done when: [binary, testable criteria; name the AC ids it delivers]
Tests: [unit | integration | e2e | none]  ·  Gate: [scoped command from Gate Commands]
Tier: [low | mid | high — one clause of why]
Rollback: [Exclusive tasks only — the undo (down-migration, regen from the previous contract,
lockfile revert); when the 3-strike bound trips, the escalation hands the user this, not just the failure]
```

`Touches` is the clustering input and the worker's ownership grant — a worker that needs an
unlisted file STOPS the cluster. Two honesty rules pay for themselves:

- **Layer completeness.** A task that reads or persists data names its whole vertical — port +
  repository/adapter + their tests — not just the layer it is "about". A cross-module read names
  the owning module's facade (+ its port/repo when new).
- **One owner per file.** A file that would collect one-line edits from many tasks (DI/module
  registration, router, barrel) becomes ONE wiring task at the end of the chain that needs it.

**Touches audit (mandatory, before the wave plan):** one scout call batching every intended
cluster's questions (answers ≤1.5 kB per cluster), over the whole vertical each owns — for every file the tasks create: who must import/register it; for every
export they change: who consumes it. Answers land in `Touches` or become a wiring task. Measured in
the parent's origin project: most mid-run ownership stops were files no task had listed.

## 2. Waves and clusters

- **Cluster** = ordered tasks for ONE worker: a **vertical slice of 4–8 tasks** (domain → ports →
  repos → api → tests of one area, wiring last). Tasks sharing a file are one cluster by
  definition; the slice then grows along its vertical even where files don't overlap — one owner
  per area beats one owner per file.
- **Wave** = clusters with no dependency between them and no file in common, dispatched
  **concurrently**. Waves are the barrier: the next starts only after every cluster reported and
  the wave verifier passed.
- **Exclusive task** = a wave of its own, alone.

Algorithm (condensed from the parent; it is the same one):

1. `level(T) = 0` if no deps, else `1 + max(level of deps)`; one wave per level, in order.
2. Exclusive tasks leave their level → own wave, placed right before the first dependent wave.
3. Within a wave, cluster by shared files, then grow each cluster along its vertical.
4. **Fold linear chains**: a next-wave task whose deps all sit in cluster C, with no other
   dependents outside C and no file shared elsewhere, joins C (while C < ~8 tasks) — kills
   barriers that gate a single task.
5. Target 2–4 clusters per wave. **Objective, in order:** fewest workers with disjoint whole
   verticals → parallelism → fewest waves → small clusters. ≥3 single-task non-exclusive clusters
   in one wave = the vertical was cut by layer; re-cluster. (Measured in the parent's origin
   project: 44 of 45 clusters in one feature held a single task — 43 warm-ups paid for one file
   each.)

**Cross-check (mandatory, self-run, before dispatching):** per cluster — every dep in an earlier
wave or earlier in the same cluster? no file shared with a sibling of the same wave (Touches
unions, tests included)? every exclusive alone? **every AC id claimed by ≥1 task's `Done when`**
(an unclaimed AC is otherwise caught only by the Reviewer — the most expensive rework loop the
pipeline has)? Any ❌ → re-cluster. Record ONE line in `plan.md` ("Cross-check: pass — N clusters,
all ACs claimed"), never the worked table — it is write-once/read-never state paid on every
re-read.

## 3. Gate commands

From the Context Map's discovered commands (never invented): **quick** (scoped unit), **full**
(quick + only the e2e/integration specs the task touched), **wave** (typecheck + lint + unit of the
wave's touched areas; `full-unit` variant only for a wave that touched shared code — mark it in the
wave table), **final** (build + lint + ALL tests, e2e included — runs at the Reviewer, plus ONE closing re-run
if any commit lands after it; never per task, never per wave).

## Template: `.ca-plans/[feature]/plan.md`

```markdown
# [Feature] — Plan

## Execution Protocol (MANDATORY)
Implement with the `ca-full-cycle` skill — activate it by name and follow its Implement flow and
Critical Rules. If it cannot be activated, STOP and tell the user.

**Status:** Research → Planning → Implementing (wave k/N) → Review → QA → Done   ← the run's
single resume point; write every transition the moment it happens
**Started:** [ISO datetime, at slug creation]
**Pre-run tests:** [passed/skipped counts + the list/collect command that produced them — Implement pre-flight]
**Brief:** `.ca-plans/[feature]/research.md`

## Gate Commands
| Level | Command |
| quick / full / wave / final | … |

## Wave Plan
| Wave | Cluster | Tasks (order) | Files (Touches union) | Tier | Gate | Status |
| 1 | C1 | T1 → T2 → T3 | … | mid | scoped | pending |
| 2 (exclusive) | C3 | T7 | … | high | full-unit | pending |

Cross-check: [pass — N clusters, no shared files, exclusives alone, every AC claimed]

## Tasks
### T1: …
[fields above]
```

Statuses (`pending → running → done <hash> | stopped <reason>`) live in the Wave Plan table —
`running` and the wave's start HEAD are written in the pre-dispatch edit; hashes, close status and
the wave's dispatch metrics (tokens/duration from the completion notifications — the run report's
raw data) at wave close. The orchestrator is the only writer of `.ca-plans/` during Implement.
Cap ≤ ~10 kB.

## 4. Proceed

- **4+ tasks** → one chat line — "plan: N tasks, W waves, C clusters (tiers: …) — dispatching
  wave 1" — then [implement.md](implement.md).
- **≤3 tasks** → light path: the task list IS the plan (still written to `plan.md`, waves
  collapsed to one); the planning window implements inline — [implement.md](implement.md)
  § *Light path*.
- Planning surfaces a hole in the brief (an AC that cannot be made precise, a contradiction) →
  that is a Rule-1 escalation: one pointed question to the user, fold the answer into
  `research.md`, continue. Ask only what blocks the plan.
- A choice made here that future runs must conform to (a convention, a chosen pattern, a boundary)
  → append it to `.ca-plans/DECISIONS.md` as the next AD-nn before dispatching. Feature-local
  choices stay in this plan.
- Mid-Implement, a plan proven structurally wrong has a surgical repair route —
  implement.md § *Failure handling* — that re-plans only what never dispatched; it is not a new
  Plan phase and owes no gate.
