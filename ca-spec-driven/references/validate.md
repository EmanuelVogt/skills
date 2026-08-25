# Execute: Validate & Verify

**Goal**: Verify implementation meets spec AND coding principles. This is NOT a separate phase — verification is part of every task's completion within Execute.

**Reader**: the Verifier does not read this file whole. Its contract is [cards/verifier.md](cards/verifier.md) (≤4 kB, read first); this file is the rationale and template layer behind it, consulted by section — § 2 spec-anchored check, § 4 Final gate, § 5 sensor, § 9 report + the template, § 10 lessons. **Never Read `SKILL.md`, `implement.md`, `sub-agents.md`, `validate.md` whole from a worker or Verifier — cards first, then ranged sections.**

**Language**: `validation.md`, the compact verdict and every lesson distilled from it are English (SKILL.md Critical Rule 6). Interactive UAT talks to the user in the user's language; what it records is English.

**Three levels of verification:**

1. **Per-task verification (always, author self-check):** After implementing each task, verify its "Done when" criteria before committing. This is mandatory and automatic. The implementer runs it.

2. **Feature-level validation (independent Verifier sub-agent, always-on, never prompted):** After the last wave's gate passed, validation runs automatically — the orchestrator dispatches a **fresh Verifier sub-agent** (see [sub-agents.md](sub-agents.md)). Do NOT ask the user whether to run it; it is the safety net, not an opt-in. User interaction is limited to interactive UAT (for user-facing features) and acting on a FAIL verdict ("fix these gaps now?"). The Verifier:
   - Never changes code or tests — sensor mutations are restored from HEAD before it reports (see Discrimination Sensor section); it runs alone, no worker in flight
   - Delegates like a worker: locating assertions and consumers → scout (`file:line` back) when the question cannot be scoped, the **Final gate** → runner (exit code + literal failures back), every other run redirected to a log it greps; its own context holds evidence, not logs
   - Scopes coverage to the feature's **git diff surface** (not the full repository)
   - Re-derives coverage independently using **evidence-or-zero**: every AC must be traced to a `file:line` + assertion expression; a criterion with no `file:line` citation counts as NOT covered
   - Runs the **spec-anchored outcome check** and the **discrimination sensor** (both described below)
   - Writes `.specs/features/[feature]/validation.md` with the full evidence report
   - Returns a compact verdict + ranked gap list to the orchestrator in chat
   - Gaps become **fix tasks** routed back to an implementer; re-verification follows with a maximum of **3 fix→re-verify iterations** before escalating to the user

3. **Interactive UAT (for user-facing features only):** The feature has complex user-facing behavior where human judgment matters (UI flows, interaction patterns, visual design). For backend-only or infrastructure work, automated checks are sufficient.

**Trigger for explicit validation:** "Validate", "verify work", "UAT", "test with me", "walk me through it"

---

## Process

### 1. Check Completed Tasks

Go through tasks.md:

- [ ] All tasks marked done?
- [ ] Any blocked or partial?

### 2. Spec-Anchored Acceptance Criteria Check

For each acceptance criterion in `spec.md`, the Verifier re-derives the **spec-defined expected outcome** and confirms the test's actual assertion matches it:

```markdown
### P1: [Story Title]

**Acceptance Criteria**:

| Criterion (WHEN X THEN Y) | Spec-defined outcome | `file:line` + assertion expression | Result |
| ------------------------- | -------------------- | ---------------------------------- | ------ |
| WHEN [X] THEN [Y]         | [precise value/state from spec] | `path/to/test.ts:42` — `expect(result.field).toBe(expected)` | ✅ PASS / ❌ GAP / ⚠️ Spec-precision gap |
```

**Rules:**

- Where the spec defines a precise outcome (specific status code, field value, error message, state), the test assertion MUST target that exact outcome — not just that an assertion exists.
- Where the spec does NOT define a precise outcome, mark as **⚠️ Spec-precision gap** and flag it in the report. Do NOT silently pass a vague assertion.
- Evidence-or-zero: a criterion with no `file:line` citation counts as NOT covered.
- **Check the proof the spec declared** (traceability table, `Proof` column — `test` | `gate` |
  `probe: <command>`), nothing else. `test` → locate the assertion. `gate` → the Final gate's exit
  code is the evidence; do not build a second proof for it. `probe` → run the named command once
  yourself, redirected to a log, and record its output. An AC with no proof, or a `probe` with no command in
  `spec.md`/`tasks.md`/`design.md`, is a **⚠️ spec-precision gap** in the report — the Verifier
  never invents a probe (a 265-turn Verifier once spent ~100 turns building resolver probes for
  ACs the design had already declared proven by CI).

### 3. Check Edge Cases

From spec.md edge cases:

- [ ] [Edge case 1] handled correctly
- [ ] [Edge case 2] handled correctly

### 4. Run Final Gate Check (MANDATORY)

Run the Final gate check from the **Gate Check Commands** section in tasks.md (fall back to the Build gate if the feature's tasks.md predates the Final level). This is the ONE place in the whole feature where the complete e2e/integration suite runs. This is NOT optional.

1. Run, through the runner: `[Final gate command from the Gate Check Commands section in tasks.md]` — keep the exit code, the printed counts and the literal failures; the log path goes in the report
2. Non-zero exit code = STOP. Do not proceed to Code Quality Check.
3. Record results:
   - Total test count: [N]
   - Passed: [N]
   - Failed: [list]
   - Skipped: [list — each skip must be justified]

**Test Integrity Check:**

- Compare current test count against the count before this feature was implemented
- If test count DECREASED: investigate why. Tests should only be deleted with explicit justification.
- If assertions were weakened (less specific than before): flag as potential regression

### 5. Discrimination Sensor (MANDATORY — always runs after gate check passes)

The sensor provides the empirical guarantee that the tests can actually detect regressions. Every mutation is temporary — the file is restored from HEAD before the next step, and the tree is clean when the Verifier reports.

**How it works:**

1. **Confirm a clean start.** `git status --short` in the checkout shows nothing for the files you will mutate (everything is committed — the Verifier only runs after the last wave). Never `git stash`, never create a branch or worktree: the checkout is shared, and `stash` moves other people's state.
2. **Inject a behavior-level fault** into the new code introduced by this feature, editing the real file in place. Choose a mutation proportional to the code's risk:
   - Flip a boolean condition (`if (x)` → `if (!x)`, `>` → `>=`)
   - Change a return value (return a wrong status code, wrong field, zero instead of a computed value)
   - Off-by-one (shift a loop bound, change a slice index)
   - Remove a required side effect (delete a method call that the spec requires)
3. **Run the tests** that cover the mutated code — only those, using the scoped Quick or Full gate command from tasks.md, run directly with the log on disk (`LOG=$(mktemp -t ca-run).log; <cmd> > "$LOG" 2>&1; echo exit=$?`, then `grep -n`/`tail -n 80`). Never run the complete e2e/integration suite per mutation.
4. **Confirm the mutant is killed** (tests FAIL). Then **restore the file from HEAD**: `git checkout -- <file>`, and confirm `git status --short -- <file>` prints nothing before the next mutation.
5. **If a mutant survives** (tests still pass after the fault), the tests are not discriminating for that behavior — add a fix task to strengthen the assertion.

**Inject once, run once.** One injection and one scoped run per mutant, then restore. If the exit code or the counts got lost (a truncated answer, a dropped notification), **read the log file** — never re-inject the same fault and never re-run the suite to "check again". A mutation run is the most expensive thing the Verifier does; repeating it burns the budget that the report needs, and a second injection on a file already restored can silently mutate the wrong line.

**Tiering — fixed by risk, not by mood (inject once, run once each):**

| Context | Sensor depth |
| ------- | ------------ |
| Light Execute (≤3-task plan) | **1–2** mutants on the riskiest AC |
| Default (every other feature — Medium and Large, tooling/CI/docs included) | **3** targeted behavior-level mutants on the highest-risk new code — not more; a tooling feature once got 5 mutants + 2 re-runs |
| P0 / critical paths (payment, auth, availability/booking rules, data integrity) | **≥5** covering all branches; language-appropriate mutation tooling if available (Stryker, mutmut, cargo-mutants, pitest) |

**Stack-agnostic:** The sensor targets behavior-level semantics (what the code does), not a specific tool. Any language, any framework.

**Report:** Record killed/survived for each mutation attempt. Surviving mutants → create fix tasks before marking the feature done.

### 6. Code Quality Check (MANDATORY)

For each changed file, verify against [coding-principles.md](coding-principles.md):

| Check                                | Pass? |
| ------------------------------------ | ----- |
| No features beyond what was asked    |       |
| No abstractions for single-use code  |       |
| No unnecessary "flexibility" added   |       |
| Only touched files required for task |       |
| Didn't "improve" unrelated code      |       |
| Matches existing patterns/style      |       |
| Would senior engineer approve?       |       |
| Tests map to acceptance criteria and are non-shallow (spot-check one story) | |
| Spec-anchored outcome check: each test's asserted value matches the spec-defined outcome (or gap flagged) | |
| Per-layer Coverage Expectation met: domain logic has 1:1 AC mapping; routes/e2e cover happy + edge + error paths for every route in scope | |
| Every test in scope maps to a spec AC, listed edge case, or Done-when criterion (no unclaimed tests) | |
| Documented project quality/testing guidelines followed (cite guideline file, or "none — strong defaults applied") | |

❌ Any "No"? → Fix before marking complete.

### 7. Interactive UAT (if user-facing feature)

For each testable deliverable, present one test at a time:

```
Test [N]: [Test Name]

Expected: [What should happen — specific and observable]

→ Does this work? Describe what you see.
```

Wait for user response:

| User says                      | Interpret as            |
| ------------------------------ | ----------------------- |
| "yes", "pass", "works", "next" | ✅ Pass                 |
| "skip", "can't test", "n/a"    | ⏭️ Skip                 |
| Anything else                  | ❌ Issue — log verbatim |

**Severity inference (never ask the user for severity):**

| User description contains               | Inferred severity |
| --------------------------------------- | ----------------- |
| crash, error, exception, fails, broken  | Blocker           |
| doesn't work, wrong, missing, can't     | Major             |
| slow, weird, off, minor, small          | Minor             |
| color, font, spacing, alignment, visual | Cosmetic          |
| (unclear)                               | Major (default)   |

### 8. Generate Fix Plans (if issues found)

For each issue found during UAT or from the Verifier:

1. **Diagnose** — Analyze the codebase to find root cause
2. **Create fix task** — Write a task definition with:
   - What: The specific fix
   - Where: File paths
   - Verify: How to prove the fix works
   - Done when: Acceptance criteria for the fix
3. **Present fix plan** — Show all fix tasks to user for approval

Fix tasks follow the same format as regular tasks and can be executed with the implement phase.

**Guardrail:** Maximum 3 diagnostic iterations per issue. If root cause isn't found after 3 attempts, flag for human investigation. The same 3-iteration bound applies to the Verifier's fix→re-verify cycle: if gaps persist after 3 rounds, escalate to the user rather than continuing to loop.

### 9. Write Validation Report File + Return Chat Summary (MANDATORY)

After all checks complete, the Verifier MUST:

1. **Write the persisted report** to `.specs/features/[feature]/validation.md` (see template below). This file is the evidence artifact — it survives the session and can be referenced by CI, reviewers, or future agents. Sections with nothing to report (UAT not performed, no fix plans, no edge cases beyond the AC table) are **omitted**, not filled with placeholders; the Requirement Traceability update is the orchestrator's, not the Verifier's.
2. **Return a compact summary in chat** to the orchestrator (see Compact Chat Summary section below), **≤ 1.5 kB**. The orchestrator surfaces it to the user and routes any ranked gaps to fix tasks.

**One-shot report — accumulate, then write once.** Every finding (AC row, gate counts, mutant result, quality check, lesson candidate) goes into a **scratch evidence file** as it is produced — in the scratch directory, never into `validation.md` directly. At the very end, `validation.md` is produced by a **single `Write`** from that accumulated evidence. No incremental `Edit`s, no re-reading it to improve the wording, no polish pass: a Verifier once spent a third of its cost on 13 `Edit`s of an already-finished report at 225k context, none of which changed a verdict. The report is a record, not a draft — an awkward sentence stays awkward.

**Turn budget ≈120, and the handoff.** Validation legitimately needs two spawns: the first covers § 1–4 (task check, spec-anchored coverage, edge cases, Final gate), the second §§ 5–10 (sensor, quality check, report, lessons). Ending a spawn with work left, return the compact verdict block plus a `HANDOFF:` line naming the scratch evidence file, the gate's exit code/counts and log path, and the sensor targets still to inject — e.g. `HANDOFF: steps 1-2 done — evidence <path>; gate exit 0 (412 passed), log <path>; next: sensor on <file:line>, then report — resume at step 3.` The orchestrator re-dispatches a fresh Verifier of the **same tier** with that block as the first lines of the payload; it is the same verification run, not a second one. The continuation reads only the evidence file and `cards/verifier.md`, and **never re-runs the Final gate** — the gate ran once, its numbers are in the evidence file.

### 10. Distill Lessons (MANDATORY when validation.md has signal)

This is the closing action of validation — not a separate phase. Immediately after the report is written, turn its grounded failures into reusable, project-local guidance by following [lessons.md](lessons.md). In short: for each surviving mutant, spec-precision gap, failed/uncovered AC, or `// SPEC_DEVIATION`, record one terse general lesson via `python3 scripts/lessons.py add` (the script enforces grounding and owns all bookkeeping). A clean PASS with no signal → record nothing. Run the self-check: if there was signal but no lesson was recorded, say so in chat. See [lessons.md](lessons.md) for the exact commands, phrasing rules, scope discipline, and the no-script fallback.

---

## Compact Chat Summary (returned in chat after validation)

The Verifier returns this block to the orchestrator after completing all checks:

```markdown
## Validation: [Feature] — [PASS ✅ | FAIL ❌]

**Spec-anchored check**: [N/N ACs matched spec outcome | M spec-precision gaps flagged]
**Gate**: [X passed, 0 failed]
**Sensor**: [N mutations injected, N killed, N survived]
**Report**: `.specs/features/[feature]/validation.md`

**Ranked gaps** (if FAIL):
1. [Gap description] — [AC or criterion] — [file:line or "no evidence"]
2. ...
```

---

## Validation Report Template (`.specs/features/[feature]/validation.md`)

```markdown
# [Feature] Validation

**Date**: [YYYY-MM-DD]
**Spec**: `.specs/features/[feature]/spec.md`
**Diff range**: [commit range or branch..HEAD]
**Verifier**: independent sub-agent (author ≠ verifier)

---

## Task Completion

| Task | Status     | Notes   |
| ---- | ---------- | ------- |
| T1   | ✅ Done    | -       |
| T2   | ✅ Done    | -       |
| T3   | ⚠️ Partial | [Issue] |

---

## Spec-Anchored Acceptance Criteria

| Criterion (WHEN X THEN Y) | Spec-defined outcome | `file:line` + assertion | Result |
| ------------------------- | -------------------- | ----------------------- | ------ |
| WHEN X THEN Y             | [precise value/state from spec] | `path/to/test.ts:42` — `expect(result.field).toBe(expected)` | ✅ PASS |
| WHEN A THEN B             | [expected value]     | `path/to/test.ts:88` — `expect(res.status).toBe(400)` | ✅ PASS |
| WHEN C THEN D             | not precisely defined in spec | — | ⚠️ Spec-precision gap |

**Status**: ✅ All ACs covered / ❌ Gaps present / ⚠️ Spec-precision gaps flagged

---

## Discrimination Sensor

| Mutation | File:line | Description | Killed? |
| -------- | --------- | ----------- | ------- |
| 1        | `src/service.ts:42` | Flipped condition `x > 0` → `x >= 0` | ✅ Killed |
| 2        | `src/service.ts:88` | Changed return value `status: 'active'` → `status: 'inactive'` | ✅ Killed |
| 3        | `src/handler.ts:15` | Removed side-effect call to `notify()` | ❌ Survived → fix task created |

**Sensor depth**: [lightweight / P0-full]
**Result**: [N/N killed] — [PASS ✅ | FAIL ❌]

---

## Interactive UAT Results (if performed)

| #   | Test        | Result   | Details                                         |
| --- | ----------- | -------- | ----------------------------------------------- |
| 1   | [Test name] | ✅ Pass  | -                                               |
| 2   | [Test name] | ❌ Issue | [Verbatim user response] — Severity: [inferred] |
| 3   | [Test name] | ⏭️ Skip  | [Reason]                                        |

---

## Code Quality

| Principle        | Status |
| ---------------- | ------ |
| Minimum code     | ✅     |
| Surgical changes | ✅     |
| No scope creep   | ✅     |
| Matches patterns | ✅     |
| Spec-anchored outcome check (asserted values match spec) | ✅ |
| Per-layer Coverage Expectation met (domain 1:1 ACs; routes happy+edge+error) | ✅ |
| Every test maps to a spec requirement — no unclaimed tests | ✅ |
| Documented guidelines followed: [file(s) or "none — strong defaults applied"] | ✅ |

---

## Edge Cases

- [x] Edge case 1: Handled correctly
- [ ] Edge case 2: NOT handled - needs fix

---

## Gate Check

- **Gate command**: [Final gate command from the Gate Check Commands section in tasks.md]
- **Result**: [X] passed, [Y] failed, [Z] skipped
- **Test count before feature**: [N]
- **Test count after feature**: [M]
- **Delta**: [+(M - N) new tests]
- **Skipped tests**: [list with justification for each]
- **Failures**: [list with details]

---

## Fix Plans (if issues found)

### Fix 1: [Issue description]

- **Root cause**: [What's actually wrong]
- **Fix task**: [Task definition]
- **Priority**: [Blocker/Major/Minor/Cosmetic]

---

## Requirement Traceability Update

Update spec.md requirement statuses:

| Requirement | Previous Status | New Status   |
| ----------- | --------------- | ------------ |
| [FEAT]-01   | Implementing    | ✅ Verified  |
| [FEAT]-02   | Implementing    | ❌ Needs Fix |

---

## Summary

**Overall**: ✅ Ready | ⚠️ Issues | ❌ Not Ready

**Spec-anchored check**: [N/N ACs matched spec outcome | M spec-precision gaps]
**Sensor**: [N/N mutations killed]
**Gate**: [X passed]

**What works**: [List]

**Issues found**: [Issue 1: How to fix]

**Next steps**: [Action]
```

---

## Tips

- **Validation is never prompted** — it always runs after the last task; do not ask the user whether to run it
- **Spec-anchored, not just covered** — "there is an assertion" is not enough; the assertion must target the spec-defined outcome
- **Sensor leaves no trace** — mutate in place, run the scoped tests yourself with the log on disk, restore from HEAD (`git checkout -- <file>`); never `stash`, never a branch
- **Keep the noise out of context** — an open question goes to a scout, the Final gate to the runner, every other run to a log file you grep; the Verifier's context holds `file:line` evidence, not logs
- **Surviving mutants are fix tasks** — do not mark the feature done if the sensor found weak tests
- **P1 first** — MVP must work before P2/P3
- **WHEN/THEN = Test** — Each criterion is a test case
- **Be specific** — "Doesn't work" isn't helpful
- **Recommend fixes** — Don't just report problems, create fix tasks
- **Quality check is mandatory** — Not optional
- **Infer severity** — Never ask the user "how bad is this?"
- **Max 3 diagnostic iterations** — Prevents infinite investigation loops
- **Update traceability** — Every verified requirement updates spec.md status
- **Always write the report file, once** — accumulate evidence in a scratch file, then a single `Write` of `.specs/features/[feature]/validation.md`; never polish it with `Edit`s
- **Inject once, run once** — lost the mutation's exit code? read the log file, never re-inject and never re-run the suite
- **Distill after writing** — turn grounded failures into lessons via `scripts/lessons.py` ([lessons.md](lessons.md)); clean PASS → no lesson
