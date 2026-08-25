# Sub-Agent Delegation (Execute)

Full mechanics of Execute: roles, wave/cluster planning, dispatch protocol, the parallel-safe git
protocol, gates, failure handling, and the Verifier. Reference text, read by section: the
orchestrator's operating contract is [cards/orchestrator.md](cards/orchestrator.md), the worker's
[cards/worker.md](cards/worker.md), the Verifier's [cards/verifier.md](cards/verifier.md).

## The one rule

**The orchestrator never writes a cluster.** The window that specified, designed and broke the
feature into tasks is the most expensive context in the session and holds the whole plan; every
line of implementation it writes is paid again on every later turn. From **4 tasks up** Execute is
therefore delegated — no offer, no "this one is simple enough": one worker per cluster, and the
Verifier always. The exception is a plan of **≤3 tasks**: there the worker costs more than it
saves. It pays a full warm-up (a median 21 turns and 94k of context before its first edit, measured
in the origin project) plus a payload, a summary and the orchestrator's turns around it, to
write three files the planning window already holds in context. Those the window implements inline,
under the same per-task cycle — and the fresh Verifier still runs (§ *Light Execute*).

## Roles

| Role | Does | Tier (chosen per dispatch) | Nests |
| --- | --- | --- | --- |
| **Orchestrator** | Reads the plan, computes/validates waves and clusters, dispatches, collects compact summaries, updates `tasks.md`, runs the wave gate, dispatches the Verifier, routes gaps. Never edits code, never runs a test itself. | The main window (strong) | dispatches everything below |
| **Worker** | Executes ONE cluster: its tasks in order, each through the per-task cycle (tests → implement → scoped gate run directly → atomic commit). Reports a compact summary. | low/mid/high per cluster, see *Model selection* | `scout` (optional) |
| **Scout** | Finds code: where a symbol lives, who consumes it, the map of an area. Returns `file:line` + one sentence, never file content. **Mandatory on the main thread**, optional inside a worker/Verifier — there a scoped `grep -n` and a `Read` at a known file are the default. | low (haiku) for a pointed question; mid (sonnet) for a module map or when finding needs judgement | — |
| **Runner** | Runs the gates of the **main window**: the orchestrator's Build gate and the Verifier's Final gate. Saves the full log to a file, returns exit code + literal failures. Not for a worker's scoped gate — that one the worker runs itself. | low (haiku); mid only to slice a log with dozens of failures | — |
| **Verifier** | Independent, fresh: spec-anchored coverage check, discrimination sensor, Final gate, `validation.md`, lessons. Never fixes. | mid (sonnet); high per feature risk, see *Model selection* | `scout` (optional), `runner` (Final gate) |

**Each role reads its card, not the references.** The worker's whole contract is
`references/cards/worker.md`, the Verifier's is `references/cards/verifier.md` — ≤4 kB, the only
file the payload tells them to read whole. `implement.md`, `sub-agents.md` and `validate.md` are the
rationale layer behind the cards: read by section with `offset`/`limit` when one rule needs its why.

**Turn budget ≈120 per agent, with handoff.** A worker or Verifier that runs out of turns mid-work
commits/records what is green and ends its summary with a `HANDOFF:` block (tasks or steps done,
next one with its `file:line`, decisions already taken, what remains). For the orchestrator a
`HANDOFF:` is not a failure and not a new cluster: **re-dispatch a fresh agent of the same type and
the same tier, with the handoff block pasted as the first lines of its payload**, and keep counting
it as the same cluster (or the same Verifier run) in `tasks.md` and in the wave report — where the
tier is stated, as for any dispatch. Escalation rules apply to `gate-failed`, never to a handoff.

### Model selection — judgement per dispatch, never hard-coded

**Delegation is always; the tier is a decision — on every dispatch, for every role.** The
`model:` in a role template is only a fallback; the caller picks the tier on every dispatch
(worker, verifier, scout and runner alike) by looking at what that dispatch actually touches — in
Claude Code, by passing `model` on every `Agent` call. A project may enforce this with a hook that
blocks a dispatch of any of the four roles without an explicit tier and prints that role's tier
guide; never assume one exists. Cost is per worker and disposable; a wrong tier costs a re-dispatch or, worse, a bad merge
— pick by risk, not by habit.

**Mid is the default for every worker cluster — no exception for "central" or "everyone
depends on it".** That includes root config, tooling, CI and docs, and tests written from a
precise spec. High is narrow: only when the cluster edits domain entities/transitions,
transaction/outbox/ambient-context code, a migration, contract regeneration, or a rule an ADR
governs. "Ordering-sensitive config" is not, by itself, a reason for high — a precise `Touches`
payload is the mitigation for a wide-blast-radius file, not a stronger model. The Verifier follows
the same default: mid unless the spec touches auth, payments, availability/booking rules, or data
integrity (P0) — tooling, CI, docs and build/resolution features stay mid even sitting in a
pre-push gate or the prod build path. Low stays for pure mechanics, but its payload must say
"surgical edits, no formatter runs" — a low-tier docs worker reformatted two files with a
formatter with no such instruction.

**Cost anchor:** a high-tier sub-agent runs ≈5× the token cost of a mid-tier one per token.
Measured in the origin project: one Medium feature spent ≈¾ of its cost on high-tier workers
plus one high-tier verifier; its low-tier scouts and runners were a rounding error.

| Tier | Worker — when the cluster… | Verifier — when the feature… | Scout / Runner |
| --- | --- | --- | --- |
| **low** (haiku in Claude Code) | is pure mechanics: fixtures, renames, config, copy, a spec file mirroring an existing one — payload must forbid reformatting | never | runner for the Build/Final gate; scout for one known symbol |
| **mid** (sonnet in Claude Code) — default for every cluster | is anything not listed under high: CRUD, UI from the design system, tests from a precise spec, root config, tooling, CI, docs, wiring with an existing pattern to copy | default for every feature: spec has precise outcomes and nothing below applies | scout default; runner only to slice a red log |
| **high** (opus in Claude Code) — narrow | edits domain entities/transitions, transactions/outbox/ambient-context, a migration, contract regeneration, or a rule an ADR governs | touches auth, payments, availability/booking rules, or data integrity (P0) — a weak verifier passing bad work is worse than none | scout for a whole-module map when the answer drives design |

**Escalate before you repeat:** a cluster STOPPED `gate-failed` twice at one tier is re-dispatched
one tier up, not a third time at the same tier; a Verifier FAIL whose gaps are architectural rather
than test-shaped means the *worker* tier was wrong for that cluster — fix at the higher tier and
note it in the wave report. State the tier you chose and why in the wave's one-line report, so the
user can correct the habit, not just the outcome.

**Keeping worker context clean is the point; a hop is only one way to do it.** A worker that pastes
3 000 lines of test-runner output into itself loses the task — but so does a worker that spends four turns
dispatching a runner, re-reading its answer and re-dispatching it at a higher tier (measured in the
origin project: 73 of 196 worker→runner dispatches had to escalate a tier just to slice a red log).
So the worker and the Verifier **run their own gates directly, with the log on disk** —
`LOG=$(mktemp -t ca-run).log; <cmd> > "$LOG" 2>&1; echo exit=$?`, then `grep -n`/`tail -n 80`
on the log, never the whole log into context. The hop stays where the log is genuinely too big for
the caller: the orchestrator's Build gate and the Verifier's Final gate. Navigation still goes to a
scout when the question is open; a scoped `grep -n` inside a worker never needed one. Scout and
runner never nest further.

**Harness mapping** — the roles are generic; each harness names them differently:

| Role | Claude Code | Other harnesses |
| --- | --- | --- |
| Worker | `Agent(subagent_type: "spec-worker", model: <tier>)` — the `spec-worker` role template under this skill's `agents/` directory (in Claude Code, install it into `.claude/agents/`); tier per cluster, required | one sub-agent per cluster with the worker payload below; if the harness has no sub-agents, see *Degraded mode* |
| Scout | `Agent(subagent_type: "repo-scout", model: "haiku"\|"sonnet")` — the `repo-scout` template under this skill's `agents/`; low tier for a pointed question, mid for a module map; tier required, the dispatch itself optional inside a worker | a repo-discovery routine the worker runs itself |
| Runner | `Agent(subagent_type: "shell-runner", model: "haiku")` — the `shell-runner` template under this skill's `agents/`; low tier; main window's Build gate and the Verifier's Final gate only; tier required | the same two gates redirected to a file by whoever runs them |
| Verifier | `Agent(subagent_type: "spec-verifier", model: <tier>)` — the `spec-verifier` template under this skill's `agents/`; mid, or high for critical features; required | one fresh sub-agent with the Verifier payload |
| Concurrency | all clusters of a wave in **one message with N `Agent` calls** (they run concurrently); wait for every notification before the wave gate | dispatch all clusters of a wave at once if the harness allows; otherwise sequentially, still one worker per cluster |
| Resume (fix→re-verify, fix worker) | `SendMessage` to the agent id returned by the original `Agent` call — same context, no re-read; only while that agent is under its ≈120-turn budget | fresh agent with the previous summary/verdict pasted first |

**The discipline is normative on the agent itself**, hook or no hook: the main thread navigates at
most twice per turn and runs nothing heavy. Inside worker and Verifier neither navigation nor gate
runs are counted — they run their own commands — but the **Read byte budget** holds for the
agent's lifetime, the guard against a worker reading a 30 kB reference whole before it edits
anything; scout and runner are unconstrained. A project may enforce all of this with hooks (one
over the delegation rules, one requiring an explicit tier on every dispatch of the four roles, in
the main window and inside nesting subagents alike) — never assume they exist; where they do not,
the same rules are text in the card and in the worker payload.

**Degraded mode (no sub-agents at all):** say so to the user first, then execute cluster by cluster
in the current window — one cluster at a time, in wave order, still applying the file-ownership,
git and gate rules below, and still running `validate.md` as a fresh-eyes pass at the end. Never
silently fall back.

---

## Waves and clusters

Two units replace the old phase/batch pair:

- **Wave** — a set of clusters that can run **in parallel**: no dependency between them, no file in
  common. Waves run in order; a wave starts only after the previous wave's clusters all reported
  and the wave gate passed. Waves are the barrier.
- **Cluster** — an **ordered** list of tasks handed to **one worker**, executed sequentially: a
  cohesive **vertical slice of ~4–8 tasks** — the domain, ports, repositories, api and tests of one
  area, with that area's wiring task last. Tasks in a cluster share files, a layer chain or a
  dependency; a cluster is the unit of context and of commit authorship. A worker pays its own
  warm-up before it edits anything (measured in the origin project: a median 21 turns and 94k
  of context before the first code edit); a slice amortises that warm-up, a single task repays it.
- **Exclusive task** — a task that touches something every other task depends on being stable:
  contract regeneration (in a generated-client stack, a step such as `pnpm contract` rewriting
  `openapi.json` and `generated/`), migrations, lockfile or
  root config, rebuilding a shared package's `dist`. It is a **wave on its own** — one cluster,
  one worker, nothing else in flight.

**Inputs** — every task in `tasks.md` carries `Depends on` (task IDs), `Touches` (every file it
creates or modifies, tests included) and `Exclusive` (yes/no). Clustering is only as good as the
`Touches` list; a task that discovers it needs an unlisted file stops and reports (see worker rules).

**Algorithm** (authored in the Tasks phase; re-derived by the orchestrator when the Tasks phase was
skipped and the plan is inline):

1. **Level** — `level(T) = 0` if `T` has no dependencies, else `1 + max(level of its deps)`.
2. **Wave** — one wave per level, in level order. Exclusive tasks leave their level and become a
   wave of their own placed right before the first wave that depends on them.
3. **Cluster within a wave** — tasks that share any file (transitively) form one cluster, and each
   cluster then grows along its **vertical**: the port, repository, use case, api and test tasks of
   the same area belong to one worker even when their files never literally overlap — one owner per
   area beats one owner per file. Order inside a cluster follows dependencies, then task number.
4. **Fold linear chains** — a task `Y` of the next wave joins cluster `C` (appended after its
   dependencies) when **all three** hold: every dependency of `Y` is in `C`; every *other* task that
   depends on those same dependencies is already in `C`; `Y` shares no file with any cluster other
   than `C`. Repeat while `C` holds fewer than ~8 tasks. This removes barriers that gate a single
   task without ever serialising work that could run beside something else.
5. **Size** — a cluster should hold **4–8 tasks** (one vertical slice, wiring last) and a wave
   **2–4 clusters**. A **single-task cluster** is for an exclusive task (migration, contract regen,
   lockfile, root config, shared `dist`) or a genuinely isolated one — a task whose area no other
   task in the plan touches. Above 4 clusters in flight, dispatch the first four and start the next
   as each one reports (FIFO), and **do not cut the level into two waves**: the cap limits
   concurrency, never wave membership (a split adds a barrier and a Build gate for nothing).
6. **Re-derive on change** — the levels are only as good as the `Depends on`/`Touches` they were
   computed from. After any re-plan, Touches correction or `blocked-by-ownership` stop during
   Execute, the orchestrator has a scout recompute the levels of every undispatched task; a task
   whose dependencies are all DONE joins the wave in flight (FIFO beyond 4, payload marked
   `serial-ok: FIFO tail`) instead of waiting for a barrier it no longer needs. Measured in the
   origin project: one recomputation removed a wave and surfaced two plan gaps one wave earlier.

**Objective, in order:** **fewest workers with disjoint ownership** — each one a whole vertical —
then parallelism (clusters that fit the same wave), then minimise waves (barriers), then small
clusters. Measured in the origin project: 44 of 45 clusters in one feature held a single task, so
43 workers each paid a full warm-up to write one file. When two layouts tie, prefer the one that
hands each worker a complete vertical over the one that starts one more worker sooner.

**Worked example** — 9 tasks over two areas:

```
T1 port          (no deps, domain/ports/a.ts)     T6 component (no deps, x.tsx)
T2 repository    (deps T1, infra/b.repo.ts)       T7 hook      (deps T6, x.hook.ts)
T3 use case      (deps T1 T2, application/c.ts)   T8 route     (deps T7, router.tsx — wiring)
T4 api handler   (deps T3, api/d.controller.ts)   T9 contract  (deps T4, *.contract.ts, openapi.json — exclusive)
T5 module wiring (deps T4, module.ts)
```

- Levels: T1,T6=0 · T2,T7=1 · T3,T8=2 · T4=3 · T5=4 · T9=5
- Verticals, not levels: T1→T5 are one module's slice (port → repository → use case → api →
  wiring last); T6→T8 are the screen's slice (component → hook → route last). The two share no file.
- Wave 1: `C1: T1 → T2 → T3 → T4 → T5` ∥ `C2: T6 → T7 → T8` — **two workers**, each owning a whole
  vertical and running its tasks in order.
- Wave 2: `C3: T9` alone — exclusive.
- Result: **2 waves, 3 clusters — 2 workers plus one exclusive.** Cut by level instead, the same
  graph gives 5 waves and 6 clusters: five workers paying a warm-up each to write one or two files,
  and four barriers with a Build gate apiece.

**Authoring for parallelism** (Tasks phase — this is where clustering is won or lost):

- **One owner per file.** Two tasks editing the same file are one cluster by definition. When a
  file naturally collects many small edits (a DI module file registering providers, a router, a
  barrel-like index, a UI slice's `model/`), give the wiring **its own task** at the end of the
  chain instead of letting five tasks each add a line to it — and that task closes the cluster that
  needed it, never a cluster or a wave of its own.
- **Tests travel with their code** (`Touches` lists the spec file too) — never a shared "tests"
  task that touches every area.
- **Mark exclusivity honestly.** Contract regen, migrations, lockfile, root config, shared `dist`.
  A task that runs the contract regen (e.g. `pnpm contract`) in the middle of a parallel wave
  corrupts everyone's typecheck.
- **Name the whole vertical.** A task that reads or persists data lists its port (`domain/ports/`)
  and repository (`infrastructure/repositories/`) files, tests included; a cross-module read lists
  the owning module's facade method and, when it does not exist yet, that module's port/repo files.
  A `Touches` narrowed to `application/**` + `api/**` stops the worker at its first query
  (tasks.md § 3 *Layer completeness*).
- **≥3 single-task non-exclusive clusters in one wave is an authoring smell**: the vertical was cut
  by layer instead of by area, and three workers pay three warm-ups to write three halves of one
  slice. Merge them into the slice's cluster (wiring last) before presenting. A project may enforce
  this with a hook that warns on it at every write of `tasks.md`.

**Cross-check (mandatory before presenting `tasks.md` — Check 4 in `tasks.md`):**

| Wave | Cluster | Tasks (order) | Files (union of Touches) | Deps outside earlier waves / own cluster? | Files shared with a sibling cluster? | Status |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | C1 | T1 → T2 → T3 → T4 → T5 | `domain/ports/a.ts`, `infra/b.repo.ts`, `application/c.ts`, `api/d.controller.ts`, `module.ts` (+ specs) | none | none | ✅ |

Any ❌ (a dep on a sibling or later cluster, a shared file, an exclusive task with company) →
re-cluster before presenting.

---

## Light Execute (≤3 tasks)

A plan of **1–3 tasks total** — whether it came from Small/Medium auto-sizing or from a formal
`tasks.md` that turned out to hold ≤3 tasks — skips the wave/cluster machinery **and the worker**:
**the planning window implements the plan itself, in order.** No formal `tasks.md` is required for
this path: the inline Execution Plan from `implement.md` § 0 is the plan, and the orchestrator
records task status and commit hashes in `.specs/STATE.md` Handoff (and in `tasks.md` too, if one
already exists).

- **Inline, under the per-task cycle**, one task at a time: tests from the spec → minimal
  implementation → scoped gate → atomic commit. Nothing about the cycle relaxes because there is
  no worker — the tests still come from the spec, the gate still decides, the commit is still
  atomic and pathspec-limited.
- **Gates go through the runner here**, unlike inside a worker: this is the planning window, where
  a heavy command is delegated (the runner role, low tier) so the log never lands in the session's
  most expensive context.
- **Why inline at this size:** a worker pays a full warm-up before its first edit (measured in the
  origin project: a median 21 turns and 94k of context), plus a payload, a summary and
  the orchestrator's turns around it. Spread over a vertical slice of 4–8 tasks that is cheap;
  spread over three tasks the window already has in context, it is the whole cost of the change.
- **One Build gate**, run **once, after the last task** — never per task, and there is no wave to
  gate per-wave; scoped (typecheck + lint + touched-area unit tests) unless the plan touched shared
  code — the Verifier's Final gate that follows is the full run.
- **The Verifier still runs, always** — a fresh Verifier agent, mid tier by default, high only per
  *Model selection*'s P0 criteria: spec-anchored coverage check + Final gate + a **reduced
  discrimination sensor** (1–2 behavior-level mutants on the riskiest AC, instead of the default 3
  / P0 ≥5) + `validation.md`. **Author ≠ verifier holds here too**: the window that implemented
  inline never verifies its own work.
- **Exclusive tasks** (contract regen, migrations, lockfile/root config) need no wave of their own
  here: the work is already sequential, so an exclusive task mixed with ordinary ones in
  the same ≤3-task plan simply runs in its place in the order — there is no parallel sibling for it
  to corrupt.
- Everything else is unchanged: the git protocol applies exactly as in a cluster (pathspec-limited
  commits, never `stash`/`add -A`/a branch op), and `.specs/` stays the orchestrator's to write.
- **Safety valve still holds** (SKILL.md § *Auto-Sizing*): 4+ tasks means clusters and workers, and
  5+ means a formal `tasks.md` with the full wave/cluster plan — never a light mode stretched past
  3 tasks.

---

## Dispatch protocol (orchestrator, per wave)

1. **Pre-flight (once per feature):** confirm the checkout the workers will use — the feature
   worktree path and branch (medium/large) or the main checkout (small); confirm
   `git status --short` there is clean or only carries files you expect; record the test count the
   Verifier will compare against (via the runner, not inline).
2. **Dispatch the wave:** one worker per cluster, **all in a single message**, each with the worker
   payload below and a **tier chosen for that cluster** (*Model selection*). Up to 4 in flight;
   queue the rest FIFO. A project may enforce this with a hook: a second cluster of the same wave
   dispatched more than 2 min after the first is blocked unless 4 are already in flight or
   the payload says `serial-ok: <reason>` (measured in the origin project: 16 of 17 multi-cluster
   waves went out one worker at a time).
3. **Wait for every summary.** Do not start the next wave, do not run the wave gate, do not touch
   `tasks.md` while a cluster of the wave is still running. A summary carrying a `HANDOFF:` block
   means the worker hit its ≈120-turn budget: re-dispatch a fresh worker of the **same type and
   tier** with that block as the first lines of its payload, unchanged ownership and gates, and
   treat it as the same cluster — the wave is not complete until the continuation reports.
4. **Wave gate:** dispatch the **runner** with the Build-level gate command from `tasks.md`
   (typecheck + lint + the unit tests of the areas the wave touched, path-filtered over the wave's
   `Touches`; the full unit suite only for a wave the Wave Plan marks `gate: full-unit` because it
   touched shared code — domain kernel, module wiring, contract, shared package; a config/docs/CI
   wave gets typecheck + lint only). Never e2e/integration and never the full unit suite otherwise:
   those run once, in the Verifier's Final gate. Runs **once per wave, never per task and never
   inside a worker** — parallel workers each running the suite would fight for CPU and pick up
   each other's half-written specs.
5. **Record:** update `tasks.md` (task status, commit hashes) from the summaries. The orchestrator is
   the only writer of `.specs/` during Execute.
6. **Failure in the wave** (a worker STOPPED, or the wave gate failed) → *Failure handling* below,
   before the next wave.
7. **After the last wave:** dispatch the **Verifier** — always, never prompted — at the tier the
   feature's risk calls for (*Model selection*).

Keep the orchestrator's own turns thin: dispatch messages, summaries, one gate result, one
`tasks.md` update per wave. If you find yourself reading source files to "help", stop — that is a
scout's job at the worker's request, not yours.

**Wave order note:** the wave gate is the moment cross-cluster breakage surfaces (cluster A changed a
type cluster B consumes without depending on it). That is a `Touches`/`Depends on` authoring gap —
fix the code through a fix worker *and* correct the plan so the next feature does not repeat it.

---

## Worker payload

**≤ ~150 words, pointers not content, rules never repeated** — the card is the worker's contract;
a payload that restates ownership, git or gate rules is high-tier output paid on every later turn of
the orchestrator (measured in the origin project: 600–900 words per dispatch, mostly rules already
in the card). Template — fill the brackets, add nothing that does not change the work:

```
Feature <name> — checkout <abs path>, branch <branch>. Cluster C<k> of wave <w>: T<a> → T<b>.
Card first, whole: <skill dir>/references/cards/worker.md. Then, ranged: tasks.md "### T<a>",
"### T<b>", "## Test Coverage Matrix", "## Gate Check Commands"; spec.md ACs <ids>; design.md
§ <section> (if any).
Own: <files>. Siblings in flight: C<j> <files>, C<m> <files>.
Gates: quick `<cmd>`, full `<cmd>` (scoped; no Build gate, no project-wide typecheck).
Tier: <low|mid|high> — <reason>. [low: surgical edits, no formatter runs.]
[One-line specifics only if they change the work: decision AD-NNN / context.md item / lesson L-NNN.]
Return: compact summary per the card, ≤1.5 kB.
```

Never paste file contents, spec text or rules into the payload. Payloads, summaries and verdicts
are English in both directions, whatever language the user speaks (SKILL.md Critical Rule 6) —
the worker never sees the user.

**Verifier payload — same discipline (≤ ~120 words):**

```
Verify feature <name> — checkout <abs path>, branch <branch>. Card first, whole:
<skill dir>/references/cards/verifier.md. spec.md (ACs + traceability Proof column) is the truth.
Commit range <first>..HEAD. Test files in scope: <list>. Gate Check Commands: tasks.md
"## Gate Check Commands"; pre-feature test count <n>. Light Execute: <yes|no>. P0: <yes|no>.
Tier: <mid|high> — <reason>. Return: compact verdict per the card, ≤1.5 kB.
```

## Worker rules

**Never Read `SKILL.md`, `implement.md`, `sub-agents.md`, `validate.md` whole from a worker or
Verifier — cards first (`cards/worker.md`, `cards/verifier.md`), then ranged sections.**

0. **Turn budget ≈120.** Running out with tasks left is normal on a long cluster, not a failure:
   commit what is green, then close the compact summary with a `HANDOFF:` block naming the tasks
   done, the next task and its `file:line`, decisions already taken and what remains. The
   orchestrator re-dispatches a fresh worker of the same tier with that block pasted first.
1. **Delegate what you would otherwise paste — and only that.** An open question ("where is…",
   "who uses…", "map of the area") → **scout**. A scoped `grep -n` on files you already know and a
   `Read` with a known `file:line` are the default, not a fallback. **Your gates you run yourself**,
   redirected to a log (rule 5): the runner is the orchestrator's Build gate and the Verifier's
   Final gate, and one more hop for a scoped run costs more turns than it saves.
2. **File ownership is absolute.** Only files in your `Touches` union. Need another file → STOP,
   report `blocked-by-ownership` with the file and why. The orchestrator re-plans; you never widen.
   **Reading a sibling's file is unreliable too** — it may be mid-edit; if your task needs what
   another in-flight task produces, that is a missing dependency: STOP and report it the same way.
3. **Never touch `.specs/`.** `tasks.md`, `spec.md`, `STATE.md` are the orchestrator's; you report,
   it records. Never *read* `STATE.md` either — a decision a task depends on is in `design.md`
   (`AD-NNN`) or arrives as one line in the payload.
4. **Per-task cycle from `implement.md`** — assumptions → tests from spec → minimum implementation →
   scoped gate run by the worker itself → adequacy review → atomic commit → next task. A failing gate is
   fixed, never bypassed; a wrong test is reported, never silently changed.
5. **Scoped gates only, run by you, logged to a file.**
   `LOG=$(mktemp -t ca-run).log; <cmd> > "$LOG" 2>&1; echo exit=$?`, then `grep -n` the
   failing lines or `tail -n 80 "$LOG"` — never cat a whole log into your context. Quick/Full as
   `tasks.md` says, scoped to the files you touched — the
   test runner only compiles what your tests import, so a sibling's half-written file cannot fail
   you. **Never a project-wide typecheck** (the project's typecheck command, e.g. `tsc`, sees the
   whole app and will fail on a sibling's work in progress); lint runs on your own files only. Typecheck and Build are the
   orchestrator's, once per wave.
6. **Git protocol for parallel workers** — the checkout is shared with sibling clusters:

   ```bash
   cd <checkout>
   git add -- <your files>
   git commit -m "<type>(<scope>): <description>" -- <your files>
   ```

   The pathspec on `commit` makes it a **partial commit**: only your paths, even if a sibling has
   other files staged at that moment. If git answers `index.lock … File exists`, a sibling is
   committing — wait 2 s and retry (up to 5×). **Forbidden** in a worker: `git add -A` / `git add .`,
   `git commit -a`, `git stash`, `git checkout`/`switch`/`reset`/`rebase`/`merge`/`clean`, any
   branch operation. Before reporting, `git status --short -- <your files>` must print nothing.
7. **Stop early, report exactly.** A failing gate you cannot fix in 3 attempts, a test that
   contradicts the spec, a needed file you do not own, an ambiguity the spec does not settle → STOP
   at that task and report; the remaining tasks of the cluster stay untouched. Never improvise a
   spec decision.

## Compact summary (worker → orchestrator)

```
Cluster C<k> (wave <w>) — DONE | STOPPED at T<n> (<reason: gate-failed | blocked-by-ownership | spec-ambiguity | test-contradicts-spec>)
- T<a>: <hash> — <n> tests, quick gate exit 0
- T<b>: <hash> — <n> tests, full gate exit 0
- Files touched: <list> (all inside ownership)
- Deviations: none | SPEC_DEVIATION in <file:line> — <one line>
- Blocker (if STOPPED): <task> — <failure verbatim, ≤ 10 lines> — log: <path>
- HANDOFF (only if the turn budget ran out): <done> — next <T<n>> at <file:line> — <decisions, what remains>
```

Nothing else: no narrative, no logs, no diffs. **Cap: 1.5 kB.** Every character lands in the
orchestrator's context for the rest of the session, on every turn until it ends; the Verifier's
verdict block obeys the same cap.

---

## Failure handling

| Signal | Orchestrator does |
| --- | --- |
| Worker STOPPED `gate-failed` | **Resume the same worker** (Claude Code: `SendMessage` to its agent id) with the blocker verbatim + log path and the same ownership — it already holds the task's context — while it is under its turn budget; a fresh fix worker only when it is over budget (`HANDOFF:` in its summary) or gone. Second failure at the same tier → re-dispatch **one tier up**, fresh. Bounded to 3 attempts per cluster, then escalate to the user with the failure. |
| Worker STOPPED `blocked-by-ownership` | The plan is wrong, not the worker: add the file to that task's `Touches`. File owned by nobody in flight → **resume the same worker** (in Claude Code, `SendMessage`) with the expanded grant and the siblings restated — it already holds the task's context (measured in the origin project: four resumptions, four completions, no re-read of card/plan/module). File owned by a sibling in flight → wait for that sibling, then resume the stopped worker (same cluster label). Correct `tasks.md` at wave close so the cross-check holds again. Second `blocked-by-ownership` in the same feature → stop dispatching, run the Touches audit (tasks.md § 3, *Layer completeness* included) over every cluster not yet dispatched, and re-derive the levels (§ *Waves and clusters* step 6); the gap repeats otherwise (measured: the same cluster stopped twice on two different unlisted files). |
| Worker reports DONE with part of its `Touches` unwritten | Not done. A worker that drops a layer with a reason ("dead code until the module exists", "the contract regen is another task's") is resumed with the precedent (the sibling tasks that shipped that layer) and finishes; the orchestrator never accepts a partial delivery as a deviation. |
| Worker STOPPED `spec-ambiguity` / `test-contradicts-spec` | Do not guess on the worker's behalf. Settle it with the user (or from `context.md`/`STATE.md` decisions if already settled), record the decision, re-dispatch. |
| Wave gate FAIL | Dispatch one fix worker owning the failing area with the runner's literal failures; re-run the wave gate through the runner. Bounded to 3 iterations, then escalate. |
| Verifier FAIL | Ranked gaps → fix tasks (clustered like any other tasks) → workers → **re-verify by resuming the same Verifier** (in Claude Code, `SendMessage`: the fix commits' range + which gaps were addressed) while it is under its turn budget — it keeps its evidence file and re-checks only the gap rows, no second Final gate, no new mutants beyond the surviving ones; measured in the origin project, a resumed re-verify cost a fraction of a fresh one. Fresh Verifier with the `HANDOFF:` block only when the first is over budget. Bounded to 3 fix→re-verify iterations, then escalate. |
| A worker returns nothing / dies | Its transcript survives (API error, machine asleep mid-edit): **resume the same agent** first — ask it to diff what landed on disk (`git status` long form + `git diff`) against what its last edit intended, repair, continue. Only when the resume fails: treat as STOPPED at its first unfinished task, check `git log` for what it committed, re-dispatch from there. |

Sibling clusters in the same wave are **not** cancelled by one failure — they finish, then the wave
gate waits for the fix.

---

## Verifier

**Always-on, never prompted — one per feature completion.** A fresh sub-agent dispatched by the
orchestrator after the last wave's gate passed. It is not gated behind anything; do NOT ask the user
whether to run validation.

**Author ≠ verifier:** the workers wrote the code and tests; the Verifier does not inherit their
context, mental model or assumptions. That separation is the gate. It runs alone — no worker is in
flight while it runs — so its scratch mutations cannot collide with anyone.

**What the Verifier receives:**

- `spec.md` for the feature (ACs = source of truth) and the checkout path/branch
- The commit range of the feature (first task commit `..HEAD`)
- The test files in scope (from `tasks.md` `Touches`) and the Gate Check Commands
- `references/cards/verifier.md` as its operating contract — read whole, first. `validate.md` is
  the rationale and template layer behind it: read by section (§ 2 spec-anchored check, § 4 Final
  gate, § 5 sensor, § 9 report + template, § 10 lessons), never whole.

**What the Verifier does (full process in `validate.md`):**

1. **Spec-anchored coverage check** — evidence-or-zero: every AC traced to `file:line` + assertion
   expression, and the asserted value matched against the spec-defined outcome; imprecise spec →
   **spec-precision gap**, never a silent pass. Locating assertions is scout work when the question
   is open; the Verifier keeps the `file:line` answers.
2. **Final gate** — the ONE run of the complete suite (build + lint + all tests incl. e2e/integration)
   in the feature, through the runner.
3. **Discrimination sensor** — injects behavior-level faults, sized by risk (Light 1–2 · default 3
   · P0 ≥5; inject once, run once each) in the real files of the checkout, runs only the scoped
   tests itself with the log on disk, confirms they FAIL, then restores each file from HEAD
   (`git checkout -- <file>` — never `stash`, never a branch operation). Surviving mutants → fix tasks.
4. **Payload/conjunction rule** — fields asserted on value/state, not on the call that produced them.
5. **Writes** `.specs/features/[feature]/validation.md` — PASS/FAIL, per-AC evidence, sensor result,
   gate results, commit range. This is the only file it writes; it never edits code or tests.
6. **Distills lessons** from grounded failures via `scripts/lessons.py` (a clean PASS records
   nothing) — see `lessons.md`.
7. **Returns the compact verdict** to the orchestrator:

```
## Validation: [feature] — [PASS ✅ | FAIL ❌]

**Spec-anchored check**: [N/N ACs matched spec outcome | M spec-precision gaps flagged]
**Gate**: [X passed, 0 failed]
**Sensor**: [N mutations injected, N killed, N survived]
**Report**: `.specs/features/[feature]/validation.md`

**Ranked gaps** (if FAIL):
1. [Gap] — [AC or criterion] — [file:line or "no evidence"]
```

The Verifier is the closing step of Execute. Execute is not done until it reports PASS and the
report file exists.
