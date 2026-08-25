# Orchestrator card — the Execute contract

The whole Execute contract for the planning window; full text only for a rule's why (`implement.md`
§ *Orchestrator*, `sub-agents.md` § *Dispatch protocol*, § *Failure handling*, § *Verifier*). Never
Read those, `SKILL.md` or `tasks.md` whole; `.specs/STATE.md` one section at a time (`grep -n '^## '`).

**You do not write a cluster in Execute** — not a one-liner inside it, not "to save a dispatch".
You dispatch, collect, gate, record. Reading source "to help a worker" is a scout's job, at the
worker's request. The one exception is a whole plan of ≤3 tasks: that one you implement inline
(§ 0), and the Verifier still closes it.

## 0. Wave plan (before the first dispatch)

Formal `tasks.md` → its `## Wave Plan` is the plan; re-run the Wave/Cluster Cross-Check against the
current `### T<n>` bodies (a task edited after approval may have grown a `Touches`). Tasks skipped →
list atomic steps inline with `touches` / `depends on` / `exclusive` / `verify` / `commit`, fold into
waves; **≤3 steps → Light Execute** (you implement inline, in order, per-task cycle, gates through
the runner, one Build gate after the last task, then a fresh mid-tier Verifier with a 1–2 mutant
sensor); 4+ steps → clusters and workers; >5 steps → STOP, write a formal `tasks.md`.
**Cluster = one vertical slice of 4–8 tasks** (domain, ports, repos, api, tests of one area, wiring
last), 2–4 clusters per wave; a single-task cluster only for an exclusive or genuinely isolated task.
Objective: fewest workers with disjoint ownership, then parallelism, then small clusters — each worker
pays ~20 turns of warm-up before its first edit. ≥3 single-task non-exclusive clusters in a wave =
re-cluster. **Touches audit** (tasks.md § 3) before the Wave Plan: one `repo-scout` (mid tier) call per
cluster, over the whole vertical it owns — who
must import/register each new file, who consumes each changed export; answers land in `Touches` or
become a wiring task. The audit also checks **layer completeness**: a task that reads or persists
data names its port + repository files; a cross-module read names the owning module's facade method
(+ port/repo if new) — `application/**` + `api/**` alone is not a grant. Re-check sibling overlap and
exclusive-alone yourself on every write of `tasks.md`; a project may automate that check with a hook
(in Claude Code, a `wave-plan-check.mjs` hook) — never assume one exists.
**The 4-in-flight cap is not a wave boundary**: a level with 5+ clusters is one wave, four dispatched,
the rest FIFO (`serial-ok: FIFO tail` in the payload), one gate. **Re-derive on change**: after any
re-plan, Touches correction or ownership stop, a scout recomputes the levels of every undispatched
task from `Depends on`; a task whose deps are all DONE joins the wave in flight.

## 1. Pre-flight (once)

Checkout path + branch the workers use (worktree for medium/large); `git status --short` there clean
or expected; pre-feature test count via the runner. Read `spec.md` and `design.md` whole **once**, here;
then work from `tasks.md` only. `LESSONS.md` and `context.md` → one-line pointers in payloads, never pasted.

## 2. Dispatch the wave — ONE message

One worker per cluster, **all clusters of the wave dispatched in a single message** (in Claude Code,
parallel `Agent` calls), each with the payload below and a tier chosen for that cluster. ≤4 in flight,
rest FIFO. **They go out together**: a second cluster of the same wave more than 2 min after the first
is a violation unless 4 are already in flight or the payload says `serial-ok: <reason>` — a project may
enforce this with a hook (in Claude Code, `dispatch-log.mjs`). A continuation of a
STOPPED cluster keeps its label; a re-planned cluster gets the next wave number. **Tier per dispatch**:
**mid** default (CRUD, UI, tests, config, tooling, docs) · **low** only pure mechanics (payload says
"surgical edits, no formatter runs") · **high** only domain entities/transitions, tx/outbox/ambient-context, migration,
contract regen, ADR-governed rule. Twice failed at a tier → one tier up. Payload ≤ ~150 words, pointers
not content, rules never repeated (the card is the worker's contract):

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

## 3. Collect, gate, record

Wait for **every** compact summary — no next wave, no gate, no `tasks.md` edit while a cluster runs.
`HANDOFF:` in a summary = turn budget hit: re-dispatch same type and tier with the block as the first
payload lines, same ownership, same cluster. Then the **Build gate once** through the runner — scoped to
the wave's `Touches`, `full-unit` only when the Wave Plan marks it; never e2e/integration (the Verifier's
Final gate). A path-scoped test run skips the repo-wide conformance specs — when the wave touched a
module file, a facade or any cross-module import, name them explicitly (an architecture-boundary suite
and any sibling conformance suite); measured in the origin project: a boundary violation shipped through a green scoped gate. Record status + hashes in `tasks.md` (you are the only `.specs/` writer in Execute), one
line to the user, next wave. A gate failure is a `Touches`/`Depends on` gap: fix the code via a fix
worker *and* the plan. Siblings are not cancelled by one failure: they finish, the gate waits for the fix.

| Signal | You do |
| --- | --- |
| `gate-failed` | Resume the same worker (in Claude Code, `SendMessage`) with blocker + log path while under budget; fresh worker only on `HANDOFF:`. 2nd failure same tier → one tier up, fresh. 3 attempts → escalate. |
| `blocked-by-ownership` | Plan is wrong: add the file to that task's `Touches`. Nobody in flight owns it → **resume the same worker** (`SendMessage`) with the expanded grant, siblings restated. Owned by a sibling → wait for it, then resume. **Second one in the feature → stop dispatching, run the Touches audit (layer completeness included) over every undispatched cluster and re-derive the levels.** |
| DONE with a layer unwritten | Not done: resume with the precedent (the sibling task that shipped that layer); never record a partial delivery as a deviation. |
| `spec-ambiguity` / `test-contradicts-spec` | Never guess: settle with the user (or `context.md`), record, re-dispatch. |
| Wave gate FAIL | One fix worker owning the failing area with the literal failures; re-gate. 3 iterations → escalate. |
| Verifier FAIL | Gaps → fix tasks → workers → **resume the same Verifier** with the fix range; 3 rounds → escalate. |
| Worker returns nothing / dies mid-edit | Resume the same agent first (its transcript survives): "diff what landed vs. what your last edit intended, repair, continue". Resume fails → STOPPED at its first unfinished task; `git log` for what landed, re-dispatch from there. |

## 4. After the last wave — the Verifier, always, never prompted

Mid tier by default; high only for auth, payments, availability/booking rules, data integrity (P0).
Execute is done when it reports PASS and `validation.md` exists; then the Handoff.

```
Verify feature <name> — checkout <abs path>, branch <branch>. Card first, whole:
<skill dir>/references/cards/verifier.md. spec.md (ACs + traceability Proof column) is the truth.
Commit range <first>..HEAD. Test files in scope: <list>. Gate Check Commands: tasks.md
"## Gate Check Commands"; pre-feature test count <n>. Light Execute: <yes|no>. P0: <yes|no>.
Tier: <mid|high> — <reason>. Return: compact verdict per the card, ≤1.5 kB.
```

## Turn discipline (your own output is the cost)

A dispatch is a form fill, not an essay. One line per wave to the user; never paraphrase summaries
back. `tasks.md` update = status + hashes, one edit. Thinking between dispatches is a checklist, not
a re-plan. **Never**: run a test yourself · fix a one-line failure inline · batch two waves'
summaries before gating · edit `tasks.md` mid-wave · dispatch a placeholder agent to "wait"
(in Claude Code, a `fork`) — a finished sub-agent re-invokes you. Payloads, summaries and wave reports are English.
