# Tasks

**Goal**: Break into GRANULAR, ATOMIC tasks. Clear dependencies. Explicit file ownership. Right tools. A wave/cluster execution plan that runs everything the dependency graph allows in parallel.

**Language**: `tasks.md` — titles, "Done when", matrix, wave plan — is English (SKILL.md Critical Rule 6); workers read it by section on every dispatch.

**Skip this phase when:** There are ≤3 obvious steps. In that case, tasks are implicit — go straight to Execute and list them inline in your implementation plan.

## Why Granular Tasks?

| Vague Task (BAD) | Granular Tasks (GOOD)             |
| ---------------- | --------------------------------- |
| "Create form"    | T1: Create email input component  |
|                  | T2: Add email validation function |
|                  | T3: Create submit button          |
|                  | T4: Add form state management     |
|                  | T5: Connect form to API           |
| "Implement auth" | T1: Create login form             |
|                  | T2: Create register form          |
|                  | T3: Add token storage utility     |
|                  | T4: Create auth API service       |
|                  | T5: Add route protection          |

**Benefits of granular:**

- **Agents don't err** - Single focus, no ambiguity
- **Easy to test** - Each task = one verifiable outcome
- **Clean commits** - Each task = one atomic, revertable commit
- **Errors isolated** - One failure doesn't block everything

**Rule**: One task = ONE of these:

- One component
- One function
- One API endpoint
- One file change

---

## Process

### 1. Review Design

Read `.specs/features/[feature]/design.md` before creating tasks.

### 1.5. Generate the Test Coverage Matrix (ALWAYS)

This step ALWAYS runs — there is no precondition. Decide which of two paths to take, then generate the three sections below.

**Step 0 — Read project quality/testing guidelines (ALWAYS, before anything else).**

Before sampling tests or inferring anything, scan the project for documented quality and testing standards. Stack-agnostic sources to check (illustrative, not exhaustive):

- Agent/AI instructions: `AGENTS.md`, `CLAUDE.md`, `.cursor/rules/**`, `.github/copilot-instructions.md`
- Contributor guides: `CONTRIBUTING.md`, `docs/` (testing, quality, or standards subdocs), README testing section
- Tool configuration: coverage thresholds in the test runner config (e.g., `jest.config.*`, `vitest.config.*`, `pytest.ini`, `.nycrc`, `Makefile` coverage targets, CI coverage gates)

**If guidelines are found:** the Coverage Expectation (see matrix below) conforms to them. Existing test samples fill gaps in style/location/framework only. Cite the specific files found in the matrix provenance note.

**If no guidelines are found:** apply the strong default — cover every spec AC and every listed edge case; domain/business logic maps 1:1 to spec ACs; routes/e2e cover happy + edge + error paths. This default may exceed the current repo's depth, which is intentional.

**Decision:**

- **Existing tests in the repo** → infer the matrix and gate commands by sampling the codebase.
- **No tests at all** → ask the user: "What test types will this project use (unit / integration / e2e / none)? What commands run them?"

**How to infer (path 1 — existing tests):**

1. **Sample test files.** Locate 5–10 existing test files. Map each file's location relative to its source file to identify which code layers are exercised and at what level (unit, integration, e2e). Use these samples for style, location patterns, framework, and test type — and as a **floor** (never produce tests less thorough than existing ones for the same layer). Existing tests are NOT a ceiling on thoroughness; the thoroughness target comes from the spec ACs, listed edge cases, and guidelines (or strong default). The Coverage Expectation column captures the target per layer.
2. **Discover commands from the repo.** Do NOT invent commands and do NOT assume an ecosystem. Read the project's own build/task manifests, test config, and CI workflows to extract the actual commands — for example: `package.json` / `project.json` (JS/TS), `Makefile`, `pyproject.toml` / `tox.ini` / `pytest` (Python), `Cargo.toml` (Rust), `go test` invocations (Go), `pom.xml` / `build.gradle` (Java/Kotlin), `Gemfile` / `Rakefile` (Ruby), `composer.json` (PHP), `.github/workflows` / `.gitlab-ci.yml`. The list is illustrative; detect what this repo actually uses.

**Output contract — render these two sections verbatim into `tasks.md`** (the exact headings downstream phases reference):

---

## Test Coverage Matrix

> Generated from codebase, project guidelines, and spec — confirm before Execute. Guidelines found: [list files, e.g. `AGENTS.md`, `jest.config.ts` — or "none — strong defaults applied"].

| Code Layer | Required Test Type | Coverage Expectation | Location Pattern | Run Command |
| ---------- | ------------------ | -------------------- | ---------------- | ----------- |
| [layer] | [unit/integration/e2e/none] | [depth target for this layer] | [glob or path pattern] | [command] |

**Coverage Expectation values** — set from guidelines first; use strong defaults when no guideline applies:

| Layer type | Strong default (no guideline) |
| ---------- | ----------------------------- |
| Domain / business-logic (service, use-case, domain model) | All branches; 1:1 to spec ACs; every listed edge case has a test |
| Route / controller / e2e / integration | All routes in scope: happy path + every listed edge case + error/failure paths |
| Repository / data-access | Key query paths + error handling; infer from existing repo tests |
| Entity / config / schema | none — build gate only |

These defaults may exceed the current repo's depth. That is intentional — they are a **target**, not a reflection of what already exists.

*Example (filled in):*

| Code Layer | Required Test Type | Coverage Expectation | Location Pattern | Run Command |
| ---------- | ------------------ | -------------------- | ---------------- | ----------- |
| Service | unit | All branches; 1:1 to spec ACs; all listed edge cases | `src/**/__test__/*.spec.ts` | `yarn test:unit` |
| Repository | integration | Key query paths + error paths | `src/**/__test__/*.e2e-spec.ts` | `yarn test:e2e` |
| Controller/Resolver | e2e | All routes: happy + edge + error | `src/**/__test__/*.e2e-spec.ts` | `yarn test:e2e` |
| Entity / Config | none | — (build gate only) | — | build gate only |

## Gate Check Commands

> Generated from codebase — confirm before Execute.

| Gate Level | When to Use | Command |
| ---------- | ----------- | ------- |
| Quick | After tasks with unit tests only | [unit test command, scoped to the touched area] |
| Full | After tasks with e2e/integration tests | [unit command + e2e/integration run scoped to ONLY the spec files the task created or touched (test-runner path filter) — never the whole e2e suite] |
| Build | Once per wave (orchestrator, through the runner, after every cluster reported) | [typecheck + lint + unit tests **scoped to the areas the wave touched** (test-runner path filter over the union of the wave's `Touches`); `full-unit` variant = typecheck + lint + the full unit suite, only for a wave marked so in the Wave Plan; a wave of config/docs/CI only → typecheck + lint. Never integration/e2e; the only project-wide typecheck between waves] |
| Final | Once per feature, at the Verifier's build-level gate | [build + lint + ALL tests, including the full unit suite and the complete e2e/integration suite — the one full run of the feature] |

**Suite-cost rule (hard):** the complete e2e/integration suite runs exactly ONCE per feature — at the Final gate, after the last task — and so does the full unit suite. Per-task gates stay scoped to the code the task touched, and the Build gate runs once per wave, never inside a worker (parallel workers each running the full unit suite would fight for CPU and pick up each other's half-written specs). If the test runner cannot scope an e2e run (no path filter), downgrade that task's gate to Quick and let the Final gate catch cross-cutting breakage — failures found there are fixed together in a closing pass, which is cheaper than re-running the full suite per task.

**Wave gate scope is decided from `Touches`, in the Tasks phase:** a wave is `gate: full-unit` when any of its tasks touches shared code — a shared package, a domain kernel/entity, module wiring/registration, the contract, or any file imported from outside the areas the wave touches; otherwise `gate: scoped`. Mark it in the Wave Plan `Notes` column; the orchestrator re-derives it inline when Tasks was skipped. Measured in the origin project: a 3 500-test unit suite ran twice for waves that were config/docs/CI only, then a third time at the Final gate.

---

**Co-located tests:** Every task that creates or modifies a code layer with a required test type MUST include writing/updating those tests in the same task. Tests are NOT separate tasks. The tests must satisfy the layer's **Coverage Expectation** from the matrix — not merely exist.

| Task creates...                           | Done When must include...                                                                                          |
| ----------------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| Code layer with "unit" requirement        | Unit tests written satisfying the layer's Coverage Expectation (e.g., 1:1 AC mapping for domain logic; all listed edge cases covered) + quick gate passes |
| Code layer with "e2e" requirement         | E2E tests written satisfying the layer's Coverage Expectation (e.g., every route the task adds: happy path + edge + error paths) + full gate passes |
| Code layer with "integration" requirement | Integration tests written satisfying the layer's Coverage Expectation + full gate passes                           |
| Code layer with "none" requirement        | Gate check at appropriate level                                                                                    |

### 2. Break Into Atomic Tasks

**Task = ONE deliverable**. Examples:

- ✅ "Create UserService interface" (one file, one concept)
- ❌ "Implement user management" (too vague, multiple files)

### 3. Define Dependencies and File Ownership

For each task:

- **Depends on** — what MUST be done before this task can start (task IDs only; "none" is a valid, valuable answer — it is what lets the task run in wave 1).
- **Touches** — every file the task creates or modifies, **tests included**. This list is the clustering input: two tasks that name the same file can never run in parallel. Be exhaustive and honest; a worker that needs an unlisted file stops and reports, and the plan gets corrected.
- **Exclusive** — `yes` when the task regenerates the contract (e.g. a contract-regen step such as `pnpm contract` rewriting `openapi.json` and the `generated/` client in a generated-client stack), adds a migration, changes the lockfile or root config, or rebuilds a shared package's build output. Exclusive tasks run alone in their own wave.

**Author for parallelism** — the plan is only as parallel as its file ownership:

- **One owner per file.** A file that would collect one-line edits from many tasks (a DI/module file registering providers, a router, a feature slice's model index, a shared type barrel) becomes **its own wiring task** at the end of the chain that needs it, instead of five tasks each touching it. Five tasks sharing `module.ts` are one serial cluster; five tasks plus one wiring task are one parallel wave and a tail.
- **Tests travel with their code** — the spec file is in the same task's `Touches`; never a shared "write the tests" task that spans areas.
- **Independent roots.** Prefer several small tasks with `Depends on: none` (interface, DTO, fixture, entity) over one "foundation" task everything hangs from.
- **Touches audit (mandatory, one scout call per cluster)** — audit the **whole vertical the cluster owns** (module file, ports, repositories, facades, api, specs), not one task at a time: the cluster is the ownership unit, so a file missed anywhere in the slice stops the same worker. A `Touches` list written from the design alone under-specifies the blast radius (measured in the origin project: most `blocked-by-ownership` stops were files no task listed — a module file the design named wrongly, a builder in a sibling dataset, one line in a permission types file). Before the Wave Plan, ask the scout (the `repo-scout` template under this skill's `agents/` directory; mid tier, one call per area): for every file the tasks create — which file must import/register it; for every exported symbol they change — who consumes it. Each answer lands in a task's `Touches` (or becomes a wiring task). A file named by `design.md` is verified on disk, never copied.
- **Layer completeness.** A `Touches` that names only the layer the task is "about" is the other half of the blast radius (measured in the origin project: three further stops in one feature — two API read models and a facade, each needing a port + repository nobody listed). Before presenting, every task that persists or reads data names the **whole vertical**: in a ports-and-adapters layout, the port (e.g. under `domain/ports/`) + its implementation (e.g. under `infrastructure/repositories/`, + its integration spec) — no module runs SQL from the application or api layer; every cross-module read names the **facade method in the owning module** plus that module's port/repo files when the method does not exist yet. A narrowed glob (`application/**`, `api/**`) is never an ownership grant for a vertical.

### 4. Create the Wave Plan

Compute waves and clusters from `Depends on` / `Touches` / `Exclusive` with the algorithm in [sub-agents.md](sub-agents.md) § *Waves and clusters* — level → wave; shared files and the rest of the same vertical → cluster; fold linear chains; exclusive → own wave. A cluster is a **vertical slice of 4–8 tasks** (domain, ports, repositories, api, tests of one area, wiring last), a wave holds **2–4 clusters**, and a single-task cluster is only for an exclusive or a genuinely isolated task. Objective: fewest workers with disjoint ownership, then parallelism, then small clusters — every worker pays a warm-up of ~20 turns before its first edit, so a plan of one-task clusters pays it once per task.

**The in-flight cap is not a wave boundary.** At most 4 clusters run at once, but a level with more than 4 clusters is still **one wave** — the orchestrator dispatches four and queues the rest FIFO, one gate at the end. Never split a level into "wave 8" and "wave 8b" to honour the cap: each extra wave is a barrier plus a Build gate (a runner run and an orchestrator turn) that buys nothing. A wave that exists only because of the cap is an authoring error, not a plan.

Render the plan as the `## Wave Plan` section of `tasks.md` (template below): waves in order, clusters per wave with their task order and file union, exclusive waves marked. **Three or more single-task non-exclusive clusters in one wave** is an authoring smell — the vertical was cut by layer instead of by area; merge them into the slice's cluster (wiring last). So is a wave with a single non-exclusive cluster while other tasks wait — go back to step 3 and split the shared file, not the wave.

### 5. Validate Before Presenting (MANDATORY)

Before showing tasks to the user, run ALL four pre-approval checks. These are NOT optional — they are gates. If any check fails, restructure the tasks and re-run until all pass.

**Check 1: Task Granularity** — verify each task is atomic (see Granularity Check section).

**Check 2: Diagram-Definition Cross-Check** — verify the wave plan matches every task's `Depends on` field (see Diagram-Definition Cross-Check section). Build the cross-check table and include it in the output.

**Check 3: Test Co-location Validation** — verify every task's `Tests` field matches the **Test Coverage Matrix** generated above (see Test Co-location Validation section). Build the validation table and include it in the output.

**Check 4: Wave/Cluster Cross-Check** — for every cluster: all dependencies sit in an earlier wave or earlier in the same cluster; no file shared with a sibling cluster of the same wave; every exclusive task is alone in its wave (see Wave/Cluster Cross-Check section). Build the table and include it in the output.

**Output all tables with the tasks** so the user can see the validation results. Any ❌ means you MUST restructure before presenting — do not show failing tasks to the user and ask them to approve.

**Note on the generated matrix:** The two sections (`Test Coverage Matrix`, `Gate Check Commands`) are provisional — generated from codebase sampling or user input and included in this file for user confirmation as part of task approval. They become authoritative once the user approves the tasks.

### 6. ASK About MCPs and Skills

**CRITICAL**: Before execution, ask the user:

> "For each task, which tools should I use?"
>
> **Available MCPs**: [list from project or user]
> **Available Skills**: [list from project or user]

---

## Template: `.specs/features/[feature]/tasks.md`

```markdown
# [Feature] Tasks

## Execution Protocol (MANDATORY -- do not skip)

Implement these tasks with the `ca-spec-driven` skill: **activate it by name and follow its Execute flow and Critical Rules.** Do not search for skill files by filesystem path. The skill is the source of truth for the full flow (per-task cycle, sub-agent delegation, adequacy review, Verifier, discrimination sensor).

**If the skill cannot be activated, STOP and tell the user — do not proceed without it.**

---

**Design**: `.specs/features/[feature]/design.md`
**Status**: Draft | Approved | In Progress | Done

---

<!-- The two sections below are generated by step 1.5 of the Tasks process and filled in during task creation. Do not manually populate them — they are produced by the agent from codebase sampling. -->

## Test Coverage Matrix

[Generated in step 1.5 — see process above]

## Gate Check Commands

[Generated in step 1.5 — see process above]

---

## Wave Plan

Waves run in order (barrier + Build gate between them). Clusters inside a wave run **in parallel**, one worker each; tasks inside a cluster run in the listed order. Exclusive waves hold one task and nothing else in flight.

| Wave | Cluster | Tasks (in order) | Files (union of Touches) | Notes |
| ---- | ------- | ---------------- | ------------------------ | ----- |
| 1 | C1 | T1 → T2 → T4 | `src/path/to/file.ts`, `src/services/YService.ts`, `src/services/YService.spec.ts` | service vertical · gate: scoped |
| 1 | C2 | T3 → T5 | `src/components/ZComponent.tsx`, `src/components/ZComponent.spec.tsx`, `src/hooks/useZ.ts`, `src/hooks/useZ.spec.ts` | screen vertical, disjoint from C1 · gate: scoped |
| 2 | C3 | T6 | `src/module.ts`, `src/router.tsx` | wiring — depends on C1 + C2, so it folds into neither · gate: full-unit (module wiring) |
| 3 (exclusive) | C4 | T7 | `*.contract.ts`, `openapi.json`, `generated/**` | contract regen (example: a generated-client stack) — alone · gate: full-unit |

```
Wave 1:  [C1: T1 → T2 → T4]  ∥ [C2: T3 → T5]
Wave 2:  [C3: T6]
Wave 3:  [C4: T7]  (exclusive)
```

---

## Task Breakdown

### T1: [Create X Interface]

**What**: [One sentence: exact deliverable]
**Where**: `src/path/to/file.ts`
**Touches**: `src/path/to/file.ts`
**Depends on**: None
**Exclusive**: no
**Reuses**: `src/existing/BaseInterface.ts`
**Requirement**: [FEAT]-01

**Tools**:

- MCP: `filesystem` (or NONE)
- Skill: NONE

**Done when**:

- [ ] Interface defined with all methods from design
- [ ] Types exported correctly
- [ ] No TypeScript errors

**Tests**: [unit/e2e/integration/none — from coverage matrix]
**Gate**: [quick/full/build — from gate check commands]

---

### T2: [Implement Y Service]

**What**: [Exact deliverable]
**Where**: `src/services/YService.ts`
**Touches**: `src/services/YService.ts`, `src/services/YService.spec.ts`
**Depends on**: T1
**Exclusive**: no
**Reuses**: `src/services/BaseService.ts` patterns

**Tools**:

- MCP: `filesystem`, `context7`
- Skill: NONE

**Done when**:

- [ ] Implements interface from T1
- [ ] Handles error cases from design
- [ ] Gate check passes: `[quick gate command from the Gate Check Commands above]`
- [ ] Test count: [N] tests pass (no silent deletions)

**Tests**: unit
**Gate**: quick

---

### T3: [Create Z Component]

**What**: [Exact deliverable]
**Where**: `src/components/ZComponent.tsx`
**Touches**: `src/components/ZComponent.tsx`, `src/components/ZComponent.spec.tsx`
**Depends on**: None
**Exclusive**: no
**Reuses**: `src/components/BaseComponent.tsx`

**Tools**:

- MCP: `filesystem`
- Skill: NONE

**Done when**:

- [ ] Component renders correctly
- [ ] Handles props from interface
- [ ] Follows existing component patterns
- [ ] Gate check passes: `[quick gate command from the Gate Check Commands above]`
- [ ] Test count: [N] tests pass (no silent deletions)

**Tests**: unit
**Gate**: quick

---

### T4: [Add A Feature to Y]

**What**: [Exact deliverable]
**Where**: `src/services/YService.ts` (modify)
**Touches**: `src/services/YService.ts`, `src/services/YService.spec.ts`
**Depends on**: T2
**Exclusive**: no
**Reuses**: Existing service patterns

**Tools**:

- MCP: `filesystem`, `github`
- Skill: `api-design`

**Done when**:

- [ ] Feature works per acceptance criteria
- [ ] Gate check passes: `[full gate command from the Gate Check Commands above]`
- [ ] Test count: [N] tests pass (no silent deletions)

**Tests**: integration
**Gate**: full

**Commit**: `feat([scope]): [description]`

---

## Wave Execution Map

Waves run in sequence; clusters inside a wave run in parallel; tasks inside a cluster run in order:

```
Wave 1:  [C1: T1 → T2 → T4]  ∥ [C2: T3 → T5]
Wave 2:  [C3: T6]
Wave 3:  [C4: T7]  (exclusive)
```

**How wave-based execution works:**

At Execute the orchestrator never implements a cluster. For each wave it dispatches **one cheap worker per
cluster, all at once** (≤4 in flight; more queue FIFO), waits for every compact summary, runs the
Build gate **once** through the runner (scoped or full-unit as the Wave Plan says), records results
in `tasks.md`, and moves to the next wave.
After the last wave it dispatches the Verifier. Workers execute their cluster's tasks in order
(implement → scoped gate → atomic, pathspec-limited commit), own only the files in their `Touches`
union, run their own scoped gate redirected to a log, delegate an open navigation question to a
scout, and report a compact summary.
See [sub-agents.md](sub-agents.md) for the full model — clustering algorithm, dispatch protocol,
worker payload and rules, git protocol for parallel workers, compact summary contract, failure
handling.

**The orchestrating agent's role during Execute:**
1. Validate the wave plan (Check 4) against the current `tasks.md`; re-derive it if tasks changed
2. Dispatch every cluster of the wave in one message
3. Receive the compact summaries; wait for all of them
4. Run the wave's Build gate through the runner
5. Update `tasks.md` with results (only writer of `.specs/` during Execute)
6. On STOPPED / gate FAIL: failure handling in `sub-agents.md` before the next wave
7. After the last wave: dispatch the Verifier

---

## Task Granularity Check

Before approving tasks, verify they are granular enough:

| Task                            | Scope         | Status       |
| ------------------------------- | ------------- | ------------ |
| T1: Create email input          | 1 component   | ✅ Granular  |
| T2: Add validation function     | 1 function    | ✅ Granular  |
| T3: Create form with all fields | 5+ components | ❌ Split it! |
| T4: Connect to API              | 1 function    | ✅ Granular  |

**Granularity check**:

- ✅ 1 component / 1 function / 1 endpoint = Good
- ⚠️ 2-3 related things in same file = OK if cohesive
- ❌ Multiple components or files = MUST split

---

## Diagram-Definition Cross-Check

Before approving tasks, verify the execution diagram is consistent with the task definitions. These are independent artifacts that can drift — the diagram is drawn for visual clarity while task bodies are written for precision. Both must agree.

For each task, check:

| Task | Depends On (task body) | Diagram Shows | Status |
| ---- | ---------------------- | ------------- | ------ |
| T[N] | [deps from body] | [deps from diagram arrows] | ✅ Match or ❌ Mismatch |

**Rules:**

- Every `Depends on` in a task body must have a corresponding arrow in the diagram.
- Every arrow in the diagram must correspond to a `Depends on` in the target task's body.
- A task must never depend on a task in a later wave, nor on a sibling cluster of its own wave — dependencies point to earlier waves or to earlier tasks in the same cluster only.

---

## Wave/Cluster Cross-Check

Before approving tasks, verify the wave plan is dispatchable as written. Two clusters in the same wave will run at the same time in the same checkout — a shared file or a hidden dependency between them is a race, not a slowdown.

| Wave | Cluster | Tasks (order) | Files (union of Touches) | Deps outside earlier waves / own cluster? | Files shared with a sibling cluster? | Exclusive alone? | Status |
| ---- | ------- | ------------- | ------------------------ | ----------------------------------------- | ----------------------------------- | ---------------- | ------ |
| 1 | C1 | T1 → T2 → T4 | `src/path/to/file.ts`, `src/services/YService.ts`, `src/services/YService.spec.ts` | none | none | n/a | ✅ |
| 3 | C4 | T7 | `*.contract.ts`, `openapi.json`, `generated/**` | none | none | yes — only cluster in wave 3 | ✅ |

**Rules:**

- Every dependency of every task resolves to an earlier wave or to an earlier task in the same cluster.
- Sibling clusters in one wave share **no** file (compare the `Touches` unions, tests included).
- A task with `Exclusive: yes` is the only task in its wave.
- Cluster size 4–8 tasks (one vertical slice, wiring last); a single-task cluster only for an exclusive or genuinely isolated task. Three or more single-task non-exclusive clusters in one wave, or a wave with one non-exclusive cluster while unrelated tasks wait later → go back to step 3 (merge the vertical; split the shared file into a wiring task) before presenting.
- No wave exists only because of the 4-in-flight cap: clusters of the same dependency level share one wave and queue FIFO (step 4).
- Every task that reads or persists data names its port + repository files; every cross-module read names the owning module's facade (+ port/repo if new) — step 3 *Layer completeness*.

A project may enforce part of this mechanically — in Claude Code, a `.claude/hooks/wave-plan-check.mjs` hook re-runs the sibling-overlap (exact path or glob containment — `a/b/**` covers `a/b/c.ts`) and exclusive-alone checks on every write of `tasks.md`, reading the `### T<n>` `Touches` fields and the `## Wave Plan` table, and a violation comes back as one line per pair. Never assume such a check is installed: the table above is yours to build, and the dependency and cluster-size rules stay yours to check either way.

---

## Test Co-location Validation

Before approving tasks, verify EVERY task's `Tests` field is consistent with the **Test Coverage Matrix** generated above. This is a hard gate — tasks that fail this check MUST be fixed.

For each task, check: does the task create or modify a code layer that has a required test type in the coverage matrix? If yes, the task's `Tests` field MUST match.

| Task | Code Layer Created/Modified | Matrix Requires | Task Says | Status |
| ---- | --------------------------- | --------------- | --------- | ------ |
| T[N]: [name] | [layer from coverage matrix] | [test type] | [task's Tests field] | ✅ OK or ❌ VIOLATION |

**Rules:**

- "Tested in another task" is NOT a valid justification for `Tests: none`. That is test deferral — the exact anti-pattern this validation prevents.
- `Tests: none` is only valid when the coverage matrix says "none" for that code layer.
- If a task creates MULTIPLE code layers (e.g., service + controller), use the HIGHEST test type required by any of them.
- Any ❌ VIOLATION → restructure the task to include its required tests before proceeding.

**Resolving compilation dependencies:**

When a task creates code that can't be tested until a later task completes (e.g., a controller that needs module wiring before its e2e tests can run), do NOT defer the tests to a separate task. Instead, restructure:

1. **Merge forward:** Move the untestable task's tests into the earliest task where they become runnable (e.g., the wiring task includes wiring + e2e tests for the controller it enables).
2. **Merge backward:** Absorb the blocking dependency into the current task so it becomes self-testable (e.g., controller task includes its own module registration).

Pick whichever option keeps tasks atomic and cohesive. The goal: no task produces unverified code. If code can't be tested in the task that creates it, the task boundaries are wrong.

---

## Tips

- **Waves are barriers, clusters are parallel** — a wave completes (and its Build gate passes) before the next; clusters inside it run at the same time
- **Touches decides parallelism** — one owner per file; wiring files get their own task
- **Reuses = Token saver** — Always reference existing code
- **Tools per task** — MCPs and Skills prevent wrong approaches
- **Dependencies are gates** — Clear what blocks what
- **Done when = Testable** — If you can't verify it, rewrite it
- **Requirement ID = Traceable** — Every task traces back to a spec requirement
- **One commit per task** — Plan the commit message format in advance

---

## Task Verification Standards

Every task MUST follow the `Done when` + `Tests` + `Gate` fields defined in the **Task Breakdown** template above. Each `Done when` entry must be specific, testable (binary pass/fail), and reference the gate check command from the `Gate Check Commands` section. Include the expected test count to prevent silent deletions.
