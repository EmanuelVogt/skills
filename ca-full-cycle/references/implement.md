# Implement — dispatch, collect, verify per wave

**Goal:** the orchestrator (the window that researched and planned) turns `plan.md` into commits —
through workers. It dispatches, collects, records, routes failures. On the clustered path it never
edits code and never runs a test; any command it must run itself (light-path gates, pre-flight
counts, the closing gate) uses the worker card's log-on-disk pattern — output to a file,
`grep`/`head` back the ≤30 lines that matter, never the log raw. Chat: one line per wave.

## 0. Pre-flight (once)

- **Branch:** on the repo's default branch → create `feat/[feature]` first; otherwise stay. One
  worktree may be used if the project already works that way — never required.
- `git status --short` clean or only expected files. Record the pre-run test counts — **passed
  AND skipped** — via the test framework's list/collect mode (e.g. `--listTests`,
  `--collect-only`; discovered from the repo, never invented), run with the log pattern, and
  write counts + command into `plan.md`'s header. Skipped matters: a later `.skip` hides inside a
  stable total.
- Re-read nothing: `research.md` and `plan.md` are already resident from Plan. On a resumed
  session, read both once, whole, here — then work from `plan.md` statuses only.

## 1. Dispatch the wave — one message

One worker per cluster — **up to 4 clusters of the wave in one message of parallel `Agent` calls,
the rest queued FIFO and dispatched as summaries return** — each with a tier chosen for that
cluster and this payload — ≤ ~150 words, pointers not content,
rules never repeated (the card is the contract; measured in the parent's origin project: dispatches
averaged 600–900 words, mostly rules the card already carried):

```
Feature <slug> — checkout <abs path>, branch <branch>. Cluster C<k> of wave <w>: T<a> → T<b>.
Card first, whole: <skill dir>/references/cards/worker.md. Artifacts: <abs>/.ca-plans/<slug>/.
Then, ranged: plan.md "### T<a>"…, "## Gate Commands"; research.md ACs <ids> [+ D-nn ids].
Own: <Touches union>. Siblings in flight: C<j> <files>.
Gates: quick `<cmd>`, full `<cmd>` (scoped; never project-wide typecheck, never the full suite).
Tier: <low|mid|high> — <reason>. [low: surgical edits, no formatter runs.]
Return: compact summary per the card, ≤1.5 kB.
```

≤4 in flight; a 5th+ cluster of the same wave queues FIFO — the cap limits concurrency, never wave
membership (never split a level into two waves for it).

Before the dispatch message goes out, one `plan.md` edit: the wave's clusters → `running`, the
wave row → its start HEAD (`git rev-parse HEAD` — the verifier's commit range and resume both
need it), the header → `Status: Implementing (wave <w>/N)`. That single write is what makes a
mid-wave crash recoverable — resume reconciles `running` rows against `git log` instead of
guessing what was in flight.

## 2. Collect

Wait for **every** compact summary — no verifier, no `plan.md` edit, no next wave while a cluster
runs. A summary ending in `HANDOFF:` is a turn-budget expiry, not a failure: re-dispatch a fresh
worker, same tier, the block pasted as the payload's first lines, same cluster label.

## 3. Close the wave — the wave verifier

Dispatch ONE fresh **wave verifier**, alone — no worker in flight; mid tier, high for a P0 or
exclusive wave:

```
Verify wave <w> of <slug> — checkout <abs path>, branch <branch>. Card first, whole:
<skill dir>/references/cards/wave-verifier.md. plan.md "## Wave Plan" row wave <w> + its "### T<n>"
bodies; research.md ACs <ids touched by this wave>. Commit range <wave start>..HEAD.
Wave gate: `<wave|full-unit cmd>`. [Known flaky: <tests this wave's summaries flagged>.]
Return: verdict per the card, ≤1 kB.
```

- **PASS** → record in `plan.md` (statuses + hashes + the wave's dispatch metrics — tokens and
  duration from the completion notifications, the run report's raw data — one edit), one chat
  line, next wave.
- **Gaps** → fix dispatches to the owning workers (resume the same worker via `SendMessage` — it
  holds the context; fresh only if over budget or dead), **every fresh fix cluster appended to
  the Wave Plan as a new `running` row before dispatch** — resume must be able to explain every
  commit; then the verifier **re-checks the gap rows only** (resume it). Bounded to 3 rounds per
  wave, then escalate to the user with the literal failure.

## 4. Failure handling (condensed; the routes that get invented wrong)

| Signal | Orchestrator does |
| --- | --- |
| `gate-failed` | FIRST intersect the failing paths/import chain with sibling Touches: clusters are file-disjoint, not import-disjoint — a sibling's mid-edit shared module reds an innocent gate. Overlap → wait for that sibling's commit, resume the stopped worker, **no strike**. Otherwise: resume the same worker with the blocker + log path. 2nd failure at that tier → fresh worker one tier up. 3 attempts → escalate. |
| `blocked-by-ownership` | The plan is wrong, not the worker: add the file to that task's `Touches`; unowned → resume the worker with the expanded grant; owned by a sibling → wait, then resume. 2nd one in the run → stop dispatching, re-audit Touches over every undispatched cluster. |
| DONE with a Touches layer unwritten | Not done — resume with the precedent; never record a partial delivery. |
| `spec-ambiguity` / `test-contradicts-spec` | Rule-1 escalation: settle with the user (or an existing D-nn), record the decision in `research.md`, re-dispatch. Never guess on a worker's behalf. |
| Worker silent / died | Resume the same agent first ("diff what landed vs. intended, repair, continue"); only then treat as STOPPED and re-dispatch from `git log`. |
| Summary carries a `Flaky:` line | Not a stop. Record it in the wave's `plan.md` row and pass it as `Known flaky` in every later wave-verifier and Reviewer payload — a flaky test proves nothing. If it is an AC's declared proof, a deflake fix task ships before Review. |
| Plan proven structurally wrong (wrong decomposition, missed vertical — beyond a Touches fix) | Surgical repair, never a restart: one scout over the invalidated area only, re-derive only the undispatched waves, log the delta in `plan.md` ("Re-planned waves k..N: <reason>"). The brief is unchanged, so no gate is owed. A brief invalidated → Rule-1 escalation, as always. |

Sibling clusters are never cancelled by one failure — they finish; the wave verifier waits for the
fix.

## Light path (≤3 tasks)

The planning window implements inline, in order, under the worker card's per-task cycle (tests
from ACs → minimal implementation → scoped gate → pathspec commit). Gates run directly, with the
card's log-on-disk pattern — the log stays on disk, only the grepped ≤30 lines enter the window;
a dispatch here would pay an agent spin-up per gate to return the same lines. One wave verifier
after the last task; then Review. Everything else (test integrity, atomic
commits, ownership honesty) holds unchanged.

## Git protocol (shared checkout — binding for workers and the light path alike)

```bash
cd <checkout> && git add -- <files> && git commit -m "<type>(<scope>): <desc>" -- <files>
```

Conventional Commits, imperative, ≤72 chars, no AI attribution of any kind. The pathspec makes it a
partial commit — only your paths, whatever a sibling staged. `index.lock … File exists` → a sibling
is committing: wait 2 s, retry ≤5×. **Forbidden:** `add -A`/`.`, `commit -a`, `stash`,
`checkout`/`switch`/`reset`/`rebase`/`merge`/`clean`, any branch op (the orchestrator made the
branch in pre-flight).

## Turn discipline (the orchestrator's own output is the cost)

A dispatch is a form fill, not an essay. Never: paraphrase summaries back · run a test yourself ·
fix a one-line failure inline · edit `plan.md` mid-wave · dispatch a placeholder agent to wait (a
finished sub-agent re-invokes you). After the last wave's verifier passes →
[review.md](review.md), immediately and unannounced (Rule 5).

## Pause / blocked — the run-level handoff

Write a `## Handoff` section at the end of `plan.md` in exactly two situations: the user pauses
the run, or a Rule-1 escalation leaves it blocked on an answer. ≤10 lines:

```
## Handoff
Paused: <date> — <by user | blocked: <reason, verbatim>>
Phase: <Status value> · wave <w>: C<k> done <hash> · C<j> running (last commit <hash>)
Blocker: <the question waiting on the user | none>
Next: <the single next action on resume>
```

Commits are the real snapshot (atomic per task); the Handoff carries only what git cannot say —
the blocker and the next action. On resume, act on it, then delete the section: it describes a
moment, not the run. Never write one mid-flow "just in case" — statuses already cover the healthy
path. The same format serves a pause in any phase (Research through QA); before Implement there
are no cluster lines, only `Phase`, `Blocker`, `Next`.
