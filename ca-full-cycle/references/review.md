# Review + QA — independent close, human judgement

Two closes, in order: the **Reviewer** (AI, fresh, independent — the last machine check) and
**QA** (the human — the first human contact since the brief). Neither is optional; the Reviewer is
never prompted, QA is never skipped on the pipeline's own judgement.

## 1. The Reviewer — always, fresh, author ≠ reviewer

After the last wave verifier passes, set `Status: Review` in `plan.md` and dispatch ONE fresh
Reviewer. Tier: **high by default** — with
no human plan gate upstream, this is the only deep independent read before a person sees the work;
mid only for a light (≤3-task) non-P0 run. It runs alone, nothing in flight.

```
Review feature <slug> — checkout <abs path>, branch <branch>. Card first, whole:
<skill dir>/references/cards/reviewer.md. research.md (ACs + proofs) is the truth; plan.md
"## Wave Plan" for the task map. Commit range <first>..HEAD. Final gate: `<final cmd>`;
pre-run test count <n>. P0: <yes|no>. Light: <yes|no>.
[Known flaky: <file:line list from worker summaries — evidence from these counts as zero>.]
[Already probed: <per wave: T<n> file:line, killed> — aim the sensor where no verifier looked.]
Tier: <high|mid> — <reason>. Return: compact verdict per the card, ≤1.5 kB.
```

The card holds the process (AC evidence check, self-run Final gate, discrimination sensor,
single write of `review.md`, scope containment). The orchestrator only routes the outcome:

- **PASS with no commit after the Final gate** → set `Status: QA` in `plan.md`, go to § 2.
- **PASS reached after fix rounds** → one closing Final-gate run first (the orchestrator,
  directly, log-on-disk): green → `Status: QA`; red → the failures are new gaps and the loop
  continues (they count toward the 3). Without this, everything committed after the last full run
  ships to the human on a stale green.
- **FAIL** → ranked gaps become fix tasks, clustered and dispatched like any wave (wave verifier
  included, every fix cluster a new `running` row in the Wave Plan), then **resume the same
  Reviewer** with the fix range — it re-checks gap rows only; the closing gate above replaces its
  Final-gate re-run. Bounded to 3 fix→re-review rounds, then escalate with the verdict.
- **A verdict ending in `HANDOFF:` is not final** — dispatch a continuation Reviewer with the
  evidence-file path (card § *Turn budget*); never route a partial verdict to QA.

## 2. QA handoff — the human returns

Announce completion in ONE compact block (user's language): what shipped (per AC, one line), the
Reviewer's verdict line, then the **QA script** — generated from the ACs, not from the
implementation:

```
QA — [feature]
Setup: [commands/state needed once, if any]
1. [user action] → expected: [observable outcome]        (AC-01)
2. …
Not in this run: [Out of Scope, one line — resets expectations before they become findings]
Reply "qa ok" to close, or the item numbers that failed + what you saw.
```

Rules: only human-observable ACs become steps (machine-proved ones — `gate`, internal `test` — are
already evidenced in `review.md`; do not ask a human to re-prove them). All ACs machine-proved,
nothing observable → there is no script: present the per-AC evidence summary instead and ask for
the explicit close — "qa ok" still closes. Steps are concrete actions
with concrete expected outcomes; a step the user cannot execute from the script alone is a bad
step. ≤10 steps — past that, group by flow.

## 3. Correction loop — triage every finding, one route each

| Finding | Route |
| --- | --- |
| **Broken vs. an AC** (the brief promised it, it fails) | Fix task(s) → worker (resume the owning one) or inline if trivial, every fresh fix cluster a new Wave Plan `running` row → wave verifier on the fix → resumed Reviewer re-checks the affected AC rows → re-issue only the affected QA steps. |
| **New or changed behavior** (the brief never promised it) | Delta research: 1 round of grill questions max → append D-nn / AC-nn to `research.md` → mini-plan (usually ≤3 tasks, light path) → implement → Reviewer resumed on the new ACs. Never absorb it silently as a "fix" — it is scope, and it gets the same machinery scope gets. |
| **Works as specified but the user dislikes it** | Show the AC + `review.md` evidence in one line; the user chooses: keep, or route as a change (row above). Never relitigate silently, never defend the code. |

Fix machinery inherits every Implement rule (bounded 3 attempts per fix, tier escalation, git
protocol). QA rounds themselves are unbounded — the human closes the loop, not a counter. Log each
round in `review.md` under `## QA Log` (round, findings, route taken, fix commits) — one line per
finding, orchestrator writes it.

## 4. Closeout — on "qa ok"

1. Any fix commit since the last full-suite run → ONE closing Final gate (log-on-disk); red →
   back to § 3, the finding is real.
2. `plan.md` header → `Status: Done`; `review.md` QA Log closed with the final round.
3. **Run report** — append one entry to `.ca-plans/RUNS.md` from what the run already recorded
   (wave-row metrics + `Started:`); a number the harness never surfaced is `n/a`, never invented:

   ```
   ## <slug>[ · plan-NN] — Done <date>
   Wall: <start> → <end> (<duration>) · waves <n> · clusters <n> · tasks <n> · fix rounds <n> · QA rounds <n>
   Sub-agents: <k> dispatches — low <n> (~<tok>) · mid <n> (~<tok>) · high <n> (~<tok>)
   Main window: <tok | n/a> · Est. cost: ~$<x> [est — from current public prices]
   ```

4. Segmented run (`research.md` § Segments): mark this segment's line, then author the next
   segment's plan (plan.md § 0) — the confirmed brief is the standing authorization; the next
   human contact is that segment's QA.
5. One closing line: commit range, AC count delivered, anything consciously left in Assumptions or
   Out of Scope that the user may want as a next run.

Nothing moves, nothing renames. Merging/pushing stays the user's call — finished work is not
permission to push (offer only if the project's own flow says so).
