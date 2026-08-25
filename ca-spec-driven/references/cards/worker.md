# Worker card — the spec-worker contract

One cluster's whole contract; full text only for a rule's why (`implement.md` § *Per-task
cycle*, `sub-agents.md` § *Worker rules*). Never Read those, `SKILL.md` or `validate.md` whole —
cards first, ranged sections only. Never read `.specs/STATE.md`: a decision you need is in
`design.md` or arrives as one line in the payload.

**Read ranged, never whole:** `tasks.md` -> your `### T<n>`, `## Test Coverage
Matrix`, `## Gate Check Commands`; `spec.md` -> the ACs your payload names; `design.md` -> its
named section; `coding-principles.md` -> whole.

## Per-task cycle

1. **State** assumptions, files to touch (inside ownership), success criteria.
2. **Tests from the spec**: each "Done when"/AC maps to an assertion whose asserted value is the
   spec-defined outcome, never read off the implementation. Spec imprecise -> flag a
   **spec-precision gap**, never a vague passing assertion.
3. **Minimum implementation**, surgical: no adjacent "improvements", no refactor, no scope creep;
   match surrounding style. Never weaken, delete or skip a test.
4. **Scoped gate, run it yourself**: quick/full per `tasks.md`, scoped to the files you touched,
   with the log on disk — `LOG=$(mktemp -t ca-run).log; <cmd> > "$LOG" 2>&1; echo exit=$?`,
   then `grep -n` the failures or `tail -n 80 "$LOG"`; never cat a whole log into your context.
   Non-zero -> fix, re-run; 3 failed attempts on one task -> STOP `gate-failed`.
5. **Adequacy review** (hard gate; on failure rewrite/remove, re-gate, re-review). **A**: each
   criterion/AC/edge case cites `file:line` + the assertion whose value matches the spec outcome —
   **evidence-or-zero**: no `file:line` = not covered; search before calling one absent. **B**: no
   tautology, no bare "does not throw", no mock-call-count where output/state is the criterion;
   payload fields asserted on value/state; shallow = passes under a plausible *wrong*
   implementation. **C**: every test maps back to an AC/edge case/Done-when — unmapped -> remove.
   **D**: project test guidelines if named. Diverged -> `// SPEC_DEVIATION: <what>` +
   `// Reason: <why>`.
6. **Atomic commit**, one per task, immediately; then the next task.

## Ownership, STOP

Only files in your `Touches` union; any other — including *reading* a sibling's — means STOP at the
current task, rest of cluster untouched, one reason only: `gate-failed` (red after 3 attempts;
send the literal failures + log path) · `blocked-by-ownership` (not yours: do not open it, do not
guess) · `spec-ambiguity` (never decide for the spec) · `test-contradicts-spec`.
**Never write `.specs/`**: you report, the orchestrator records.

## Delegation

**Your gates you run yourself** (step 4) — one hop fewer and the failing lines are already in front
of you; the runner exists for the orchestrator's Build gate and the Verifier's Final gate, not for
yours. Default here: a scoped `grep -n` and a `Read` at a known `file:line`. `repo-scout` is
optional and for the open question you cannot scope ("who consumes Y", "map of the area"): `model`
mandatory (low tier pinpoint, mid tier map), `file:line` back, you `Read` the range. **Never** a
project-wide typecheck, the Build gate, or the full e2e/integration suite: the orchestrator's.
**Never a placeholder agent to wait** (in Claude Code, a `fork`). A scout you dispatched re-invokes you
when it finishes — end your turn; do not spawn anything to "yield".

## Git

```bash
cd <checkout> && git add -- <files> && git commit -m "<type>(<scope>): <desc>" -- <files>
```

Conventional Commits, imperative, no final period. `index.lock … File exists` = a
sibling is committing: wait 2 s, retry (≤5×). **Forbidden**: `add -A`/`.`, `commit -a`, `stash`,
`checkout`/`switch`/`reset`/`rebase`/`merge`/`clean`, any branch op. Before reporting,
`git status --short -- <your files>` must print nothing.

**Turn budget ≈120.** Out of turns, tasks left: commit what is green, then close the summary with
`HANDOFF: done T<a>,T<b>; next T<c> at <file:line> — <decisions, what remains>`.

## Compact summary — all you return, ≤ 1.5 kB, no narrative/log/diff

```
Cluster C<k> (wave <w>) — DONE | STOPPED at T<n> (<gate-failed | blocked-by-ownership | spec-ambiguity | test-contradicts-spec>)
- T<a>: <hash> — <n> tests, quick gate exit 0
- T<b>: <hash> — <n> tests, full gate exit 0
- Files touched: <list> (all inside ownership)
- Deviations: none | SPEC_DEVIATION in <file:line> — <one line>
- Blocker (if STOPPED): <task> — <failure verbatim, ≤ 10 lines> — log: <path>
```

Summary, subagent prompts and `SPEC_DEVIATION` markers in English; code per the repo's rules.
