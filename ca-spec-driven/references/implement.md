# Execute

**Goal**: The orchestrator dispatches; workers implement ONE task at a time. Surgical changes. Verify. Commit. Repeat.

Two readers, two sections — and neither reads this file whole. The **orchestrator** (the planning window) works from [cards/orchestrator.md](cards/orchestrator.md), which condenses *Orchestrator*, *After the last wave* and the dispatch protocol into ≤4 kB; it opens *Orchestrator* here by section when a rule needs its rationale, and never runs the per-task cycle itself. A **worker** does not read this file whole: its contract is [cards/worker.md](cards/worker.md), which condenses *Per-task cycle* into ≤4 kB — the § below stays as the reference text, consulted by section (`Read` with `offset`/`limit`) when one rule needs its rationale.

**Language**: the inline step list, wave plan, payloads, `tasks.md` updates and `SPEC_DEVIATION` markers are English (SKILL.md Critical Rule 6); only the chat line to the user follows the user's language.

---

## Orchestrator: dispatch, don't implement

**You do not write a cluster in Execute.** Not for a one-liner inside it, not "just this once to save a dispatch". The exception is a whole plan of **≤3 tasks**, which you implement inline (§ 0 → *Light Execute*). The full model — roles, waves and clusters, payload, git protocol, failure handling — is in [sub-agents.md](sub-agents.md); the steps here are the sequence.

### 0. Wave plan (MANDATORY — before the first dispatch)

- **Formal `tasks.md` exists** → its `## Wave Plan` is the plan. Re-run Check 4 (Wave/Cluster Cross-Check, [tasks.md](tasks.md)) against the current task bodies — a task edited after approval may have grown a `Touches` entry that breaks a sibling cluster.
- **Tasks phase was skipped** → list the atomic steps inline, **with the same fields a task would carry**, then fold them into waves and clusters with the algorithm in `sub-agents.md`:

```
## Execution Plan

1. [Step] → touches: [files, tests included] → depends on: [none | step #s] → exclusive: [no|yes] → verify: [how] → commit: [message]
2. …

Wave 1: [C1: 1] ∥ [C2: 3]
Wave 2: [C3: 2 → 4]
```

Each step is ONE deliverable, independently verifiable, independently committable. **≤3 steps** → [Light Execute](sub-agents.md#light-execute-3-tasks): you implement the plan inline, in order, under the per-task cycle — no worker, no wave/cluster split, gates through the runner, Verifier as always. **4+ steps or complex dependencies**, fold into waves/clusters with the algorithm in `sub-agents.md`; if listing reveals >5 steps, STOP and create a formal `tasks.md` — the Tasks phase was wrongly skipped.

### 1. Pre-flight (once)

Confirm the checkout the workers will use (feature worktree path + branch, or the main checkout for a small change), that `git status --short` there carries nothing unexpected, and note the pre-feature test count through the runner. Read `LESSONS.md` confirmed lessons that apply and `context.md` decisions — these go into the worker payload as one-line pointers, never as pasted content.

### 2. Dispatch the wave

One worker per cluster, all clusters in **one message**, each with the worker payload from `sub-agents.md` and a **tier chosen for that cluster** by what it touches (`sub-agents.md` § *Model selection* — mechanics low, mid the default for everything else, domain/contract/migration/ADR-governed high). ≤4 in flight; the rest queue FIFO. Say which tier each cluster got in the wave report. For a ≤3-task plan there is no dispatch at all: implement it inline — see `sub-agents.md` § *Light Execute*.

### 3. Collect, gate, record

Wait for every compact summary. Run the **Build gate once** through the runner — scoped to the wave's touched areas, or `full-unit` when the Wave Plan marks the wave so (shared code touched); the full suite otherwise runs once, at the Verifier's Final gate. Update `tasks.md` (status, hashes) — you are the only `.specs/` writer during Execute. Report the wave to the user in one line. On STOPPED or gate FAIL, apply *Failure handling* in `sub-agents.md` before the next wave. Then step 2 for the next wave.

### 4. After the last wave

Dispatch the Verifier (see *After the last wave* at the end of this file). Execute is not done until it reports PASS.

**Anti-patterns for the orchestrator:** reading source files "to help a worker" (that is a scout's job, at the worker's request); running a test yourself; fixing a one-line gate failure inline; batching two waves' summaries before running the gate; editing `tasks.md` while a cluster is still running.

### Turn discipline (the orchestrator's own output is the cost)

Once Execute is delegated, the planning window grows mostly from what it writes itself — measured
in the origin project: ≈990 tokens of own output per turn (35 % thinking) against
≈240 of tool results. So:

- **Read `spec.md` and `design.md` whole once**, at pre-flight; from then on work from `tasks.md`
  only — the `## Wave Plan` and the `### T<n>` bodies of the wave being dispatched. Do not re-open
  the spec to write a payload; the payload points at AC ids, it does not quote them.
- **A dispatch is a form fill, not an essay**: payload ≤ ~150 words from the template in
  `sub-agents.md`; the tier line is one clause. No re-deriving the wave plan after Check 4 passed;
  no restating rules the card carries.
- **One line per wave to the user** (clusters + tiers dispatched / done, gate exit) — never a
  per-task narration, never a summary of the summaries. The compact summaries already sit in the
  context; do not paraphrase them back.
- **Record, don't rewrite**: the `tasks.md` update per wave is status + hashes, one edit.
- Thinking between dispatches is a checklist (all summaries in? gate exit? next wave's clusters?),
  not a re-plan.

---

## Per-task cycle (worker)

You were dispatched with a cluster: an ordered list of tasks, a checkout path, the files you own, and pointers into `tasks.md`/`spec.md`/`design.md`. Read those by section. Read [coding-principles.md](coding-principles.md). Then, for each task in order, run steps 3–9 below. Your rules — nesting, ownership, git protocol, when to STOP, the compact summary — are in [sub-agents.md](sub-agents.md) § *Worker rules*; the cycle here is the craft.

**Before each task, state:**

1. **Assumptions** — What am I assuming? Any uncertainty?
2. **Files to touch** — ONLY files this task requires, all inside your ownership
3. **Success criteria** — How will I verify this works?

⚠️ Do not proceed without stating these explicitly.

**Dependencies:** everything your tasks depend on is either an earlier wave (already committed in the checkout) or an earlier task in your own cluster. If a task turns out to need something that is not — a file you don't own, a symbol from a sibling cluster — STOP and report `blocked-by-ownership`; do not work around it.

### 3. State Implementation Plan

Before writing code:

```
Files: [list]
Approach: [brief description]
Success: [how to verify]
```

### 4. Write Tests (derived from spec, not from implementation)

If the task includes tests (per the Tests field and **Test Coverage Matrix** in tasks.md):

1. Write the test file(s) covering the task's acceptance criteria.
2. Tests MUST be derived from the task's "Done when" criteria and `spec.md` ACs — **not** from the implementation. Each test encodes what the spec requires; never write tests by reading the code and asserting what it currently does.
3. Each acceptance criterion from "Done when" maps to at least one test assertion whose asserted value matches the **spec-defined expected outcome**. Where the spec does not define a precise outcome, note it as a **spec-precision gap** rather than writing a vague assertion and passing silently.
4. Edge cases from spec.md that apply to this task get test cases too.

**HARD CONSTRAINTS (test integrity — never violate):**

- Do NOT weaken assertions (making them less specific to pass more easily)
- Do NOT delete or skip test cases
- Do NOT use the test framework's skip/disable/pending mechanism to bypass failing tests

If a test is genuinely wrong (tests the wrong behavior per spec), STOP the cluster and report
`test-contradicts-spec` — the orchestrator settles it with the user. Never silently change a test.

If the task does NOT include tests (e.g., entity-only, config-only), skip to Step 4b.

### 4b. Implement

Write the minimum implementation needed to satisfy the task's success criteria: pass all relevant tests (when present) and meet the defined verification/gate checks when there are no direct tests.

**HARD CONSTRAINTS:**

- Do NOT modify tests except to fix a genuinely wrong assertion (STOP and report `test-contradicts-spec` first). The tests are the spec — implementation conforms to them.
- Do NOT weaken assertions (making them less specific to pass more easily)
- Do NOT delete or skip test cases
- Do NOT use the test framework's skip/disable/pending mechanism to bypass failing tests
- Minimum code to pass — save structural improvements for a refactor task

Follow [coding-principles.md](coding-principles.md):

- Simplest code that works
- Touch ONLY listed files
- No scope creep

### 5. Gate Check (VERIFY)

Run the gate check command from the task definition **yourself, with the log on disk** — the log never enters your context, only the lines you ask for. This is MANDATORY — not "if applicable."

```bash
LOG=$(mktemp -t ca-run).log; cd <checkout> && <gate command> > "$LOG" 2>&1; echo exit=$?
grep -n "FAIL\|✕\|error TS" "$LOG"   # or: tail -n 80 "$LOG"
```

1. Look up the command for the task's Gate level (quick/full) in the **Gate Check Commands** section of tasks.md and scope it to the files you touched
2. Non-zero exit code = STOP. Fix the failure. Re-run. Do not proceed until it passes. Three failed attempts on the same task → STOP the cluster and report `gate-failed` with the literal failures from the log, plus its path.

The runner — the `shell-runner` template under this skill's `agents/` directory — stays for the two gates whose log is genuinely too big for the caller: the orchestrator's Build gate, once per wave, and the Verifier's Final gate. A hop for a scoped run costs more turns than the log it saves (measured in the origin project: more than a third of worker→runner dispatches had to be escalated to the mid tier just to slice a red log).
3. Confirm the test count matches expectations (no tests were silently deleted or skipped)

**Tiered gates (from the Gate Check Commands section of tasks.md):**

| Task includes                    | Gate level | What runs                |
| -------------------------------- | ---------- | ------------------------ |
| Unit tests only                  | Quick      | Unit test command (scoped to the touched area) |
| E2E or integration tests         | Full       | Unit command + ONLY the e2e/integration specs the task created or touched (scoped run via test-runner path filter) |
| No tests (config, entities, etc) | Lint-only  | Lint on the touched files only — typecheck waits for the wave's Build gate |
| *(orchestrator, once per wave)*  | Build      | Typecheck + lint + unit tests of the touched areas (path filter over the wave's `Touches`); full unit suite only for a wave marked `gate: full-unit` (shared code) — **never inside a worker** |

**Never run the complete e2e/integration suite per task or per wave.** It runs exactly once per feature — the Final gate executed by the Verifier (see validate.md). Failures that only surface there are fixed together in a closing pass. And never run the Build gate — nor a project-wide typecheck — from a worker: sibling clusters are writing in the same checkout, `tsc` sees the whole app and will fail on a sibling's half-written file, and a full unit run picks up their half-written specs and competes for CPU with their scoped gates. A worker's gates are the ones that only see what it imports: the scoped test run and lint on its own files.

The gate check is deterministic. The test runner decides if the code is correct,
not the agent's self-assessment.

### 6. Post-Gate Review

After the gate check passes:

1. Verify test count: Are there at least as many test cases as before? (prevents silent deletion)
2. Verify no SPEC_DEVIATION: If implementation diverged from spec/design, add a marker:

```
// SPEC_DEVIATION: [what diverged]
// Reason: [why the deviation was necessary]
```

3. Quick complexity check: "Would senior engineer flag this as overcomplicated?"
   - Yes → Simplify, re-run gate
   - No → Proceed

4. **Test Adequacy Review (MANDATORY — hard gate).**

   A task cannot be committed or marked done until all four checks below pass. Tests must be both **necessary** (every test traces to a requirement) and **sufficient** (every requirement is covered). The scope boundary is the feature spec — do not test beyond it.

   **Check A — Sufficient coverage (per-layer depth).** Build and output this table:

   | Done-when criterion / spec AC / listed edge case | `file:line` + assertion expression | Spec-defined outcome | Covered? |
   | ------------------------------------------------- | ---------------------------------- | -------------------- | -------- |
   | [criterion from task or spec] | `path/to/test.ts:42` — `expect(result.field).toBe(expected)` | [expected value from spec] | ✅ Yes / ❌ No / ⚠️ Spec-precision gap |

   **Evidence-or-zero rule:** Each covered cell MUST cite the exact `file:line` where the assertion lives AND reproduce the assertion expression (not just the `describe`/`it` name). A criterion with no located `file:line` evidence counts as **NOT covered**; the task cannot be marked done. Do not declare a criterion absent without first searching the test files — show the search before concluding it is missing (mirror: evidence or zero, never a guess).

   **Spec-anchored outcome check:** For each covered criterion, derive the expected outcome from `spec.md` (or the task's "Done when" field) and confirm the test's asserted value matches it — not just that an assertion exists. Where the spec defines a precise outcome (e.g., a specific status code, a specific field value, a specific error message), the test assertion MUST target that exact outcome. Where the spec does not define a precise outcome, mark the cell as **⚠️ Spec-precision gap** and add a note; do NOT silently pass a vague assertion as if it were covered.

   Every "Done when" criterion, every spec.md acceptance criterion, and every listed edge case that applies to this task must map to at least one concrete test assertion. Enforce the layer's Coverage Expectation from the Test Coverage Matrix:

   - Domain / service layer: assertions map 1:1 to spec ACs; every listed edge case has a dedicated test.
   - Route / controller / e2e layer: every route the task adds or modifies must have a happy-path test, a test for each listed edge case, and a test for each documented error/failure path.

   No criterion left unverified.

   **Check B — Non-shallow litmus.** Reject each of the following shallow patterns:
   - Assertion-free tests or `expect(true)` / `expect(1).toBe(1)` style tautologies
   - "No error thrown" as the only assertion — unless not-throwing IS the specified behavior
   - Asserting only on mock call counts when the actual output/state is what the criterion demands
   - Happy-path only when the task's "Done when" or spec.md lists edge cases

   **Payload/conjunction rule.** For each named field in an emitted event, returned object, or persisted record, apply a separate check:
   1. Open the constructed object at its `file:line` and confirm the field is present in the assertion.
   2. Confirm the assertion targets the field's **value or state**, not just the call that produced it.
   3. A present `emit(...)` / `return ...` / `save(...)` call does NOT prove the field — only an assertion on the result does.
   4. Asserting a method was called (spy/mock) != asserting the resulting state. Both may be needed; neither substitutes for the other.

   Apply this check to every payload-bearing criterion before marking it covered.

   **Stack-agnostic litmus:** An assertion is shallow if it would still pass under a plausible *wrong* implementation. If so, strengthen it before committing.

   **Check C — Necessary (no tests beyond the spec).** Reverse-map every test back to a spec AC, a listed edge case, or a "Done when" criterion. Build this table:

   | `file:line` + assertion expression | Maps to (AC / edge case / Done-when criterion) | Keep? |
   | ---------------------------------- | ---------------------------------------------- | ----- |
   | `path/to/test.ts:42` — `expect(result.field).toBe(expected)` | [requirement ID or criterion text] | ✅ Keep / ❌ Remove |

   Any test that maps to nothing → remove it. A test with no requirement is scope creep — it proves nothing about the feature and expands scope beyond the spec. Do not write speculative "what if" tests, do not test framework or library behavior, and do not duplicate an assertion that is already covered at another layer for the same scenario.

   **Check D — Guideline conformance.** If project quality/testing guidelines were found in step 0 of tasks.md step 1.5, verify this task's tests conform to them (naming conventions, file locations, coverage thresholds, etc.). Note the guideline file followed.

   **Bound:** Tests prove the work; they do not expand it. Thoroughness is scoped to the feature + spec. Repo depth is a floor (never less thorough than existing tests for the same layer); the spec is the ceiling. Do not invent requirements or tests that have no spec anchor.

   **Anti-patterns — known verification cheats (treat any of these as an automatic Check failure):**

   | Anti-pattern | Why it fails |
   | ------------ | ------------ |
   | Committing before the gate check passes | Skips the deterministic verifier — the gate is not optional |
   | Asserting call count / spy invocation instead of the resulting state | Proves the method ran, not that it did the right thing |
   | Marking a criterion covered without a `file:line` citation | Violates evidence-or-zero; suspicion of coverage is not coverage |
   | Weakening an assertion (making it less specific) to force a pass | Moves the goalposts instead of fixing the code |
   | Deleting or skipping a test to make the suite pass | Destroys coverage permanently; a failing test is a signal, not noise |
   | "Tested elsewhere" deferral without citing where | Coverage gaps hide behind vague claims; cite the file:line or it doesn't count |
   | Speculative "what if" tests with no spec anchor | Expands scope beyond the ceiling; remove them in Check C |
   | Testing framework or library behavior | Tests a dependency, not the feature; remove them in Check C |

   **On any failure** → rewrite or remove the affected test(s), re-run the gate, then re-run this review.

   *Honest caveat:* This is an inspection-based review (model judgment), complementary to — not a replacement for — the deterministic gate. The gate confirms the test suite runs; the feature-level discrimination sensor (step 10) confirms the tests can detect regressions. This review confirms the suite is meaningful and bounded.

   Add the two mapping tables and a one-line adequacy verdict to the Execution Template's Post-Gate section.

### 7. Atomic Git Commit

Each task gets its own commit immediately after verification. Never batch multiple tasks into one commit.

**Parallel-safe form (sibling clusters share the checkout):**

```bash
cd <checkout>
git add -- <files of this task>
git commit -m "<type>(<scope>): <description>" -- <files of this task>
```

The pathspec on `commit` makes it a partial commit — only your paths, whatever a sibling has staged. `index.lock … File exists` means a sibling is committing: wait 2 s, retry (≤5×). Never `git add -A`/`.`, `git commit -a`, `git stash`, `checkout`/`switch`/`reset`/`rebase`/`merge`/`clean`, or any branch operation. Before reporting the cluster, `git status --short -- <your files>` must print nothing.

**Format ([Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/)):**

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

**Types:**

| Type       | When to use                                             |
| ---------- | ------------------------------------------------------- |
| `feat`     | New feature or capability                               |
| `fix`      | Bug fix                                                 |
| `refactor` | Code change that neither fixes a bug nor adds a feature |
| `docs`     | Documentation only                                      |
| `test`     | Adding or correcting tests                              |
| `style`    | Formatting, missing semicolons, etc. (no code change)   |
| `perf`     | Performance improvement                                 |
| `build`    | Build system or external dependencies                   |
| `ci`       | CI configuration files and scripts                      |
| `chore`    | Maintenance tasks that don't modify src or test files   |

**Scope:** Feature name or module area, lowercase, e.g., `auth`, `cart`, `api`

**Description rules:**

- Imperative mood ("add", not "added" or "adds")
- Lowercase first letter
- No period at the end
- Complete the sentence: "If applied, this commit will _[your description]_"

**Breaking changes:** Append `!` after type/scope AND add `BREAKING CHANGE:` footer:

```
feat(api)!: change authentication endpoint response format

BREAKING CHANGE: login endpoint now returns JWT in body instead of cookie
```

**Examples:**

```
feat(auth): add email validation to login form
```

```
fix(cart): prevent negative quantity on item decrement
```

```
refactor(api): extract token refresh logic into service

Move token refresh from inline handler to dedicated AuthTokenService
for reuse across multiple endpoints.
```

**Rules:**

- One task = one commit
- Description references what was DONE, not what was planned
- Include only files listed in the task — never sneak in "while I'm here" changes
- If tests are part of the task, include them in the same commit

### 8. Scope Guardrail

During implementation, you will notice things that could be improved, refactored, or added. **Do not act on them.** Instead:

- If it's a bug: surface it to the user (or capture it as a separate task)
- If it's an improvement: add it to the feature's `context.md` under "Deferred Ideas" (or surface it to the user if there is no `context.md`)
- If it's related to the current task: only include it if it's in the "Done when" criteria

**The heuristic:** "Is this in my task definition?" If no, don't touch it.

### 9. Report, don't record

Workers never write to `.specs/`. Note the task's commit hash and test count for the compact summary; move to the next task of the cluster. When the cluster is done (or STOPPED), return the compact summary from [sub-agents.md](sub-agents.md) — nothing else. The orchestrator marks tasks complete in `tasks.md` and updates requirement traceability in `spec.md`.

---

## After the last wave (orchestrator)

### 10. Feature-Level Validation (MANDATORY, always runs)

When the last wave's summaries are in and its Build gate passed, you MUST dispatch the Verifier before reporting the work as done. **This is not optional and is never prompted — it runs automatically.** Do not stop at the final task's commit.

**Author ≠ verifier rationale.** The workers are the authors of the code and tests. An author checking their own work applies the same mental model that may have produced any gaps. The Verifier is a fresh sub-agent that re-derives coverage from the spec independently — it does not inherit the workers' assumptions. This separation is the quality gate, not just a style preference.

**Layering:**
- Per-task adequacy self-check (steps 5–6): cheap, always runs, the worker does it, confirms each task in isolation.
- Wave gate: one Build-level run per wave, catches cross-cluster breakage early.
- Feature-level validation (step 10): one trustworthy independent gate at completion, always-on, Verifier sub-agent does it.

**How to delegate to the Verifier:**
Dispatch a fresh sub-agent following the **Verifier** role described in [sub-agents.md](sub-agents.md). Provide it with:
- `spec.md` (ACs = source of truth) and the checkout path/branch
- The commit range for this feature (first task commit `..HEAD`)
- The test files in scope (from `Touches`) and the Gate Check Commands
- `validate.md` as its operating checklist

**What the Verifier does (full description in [validate.md](validate.md) and [sub-agents.md](sub-agents.md)):**
1. **Spec-anchored coverage check** — re-derives coverage evidence-or-zero; confirms each test's asserted value matches the spec-defined outcome; flags spec-precision gaps.
2. **Discrimination sensor** — injects a small behavior-level fault (flip a condition, change a return value, off-by-one) in the real file, runs only the scoped tests itself with the log on disk, confirms they kill the mutant, then restores the file from HEAD (`git checkout -- <file>`, never `stash`). Reports killed/survived; surviving mutants become fix tasks.
3. **Persisted report** — writes `.specs/features/[feature]/validation.md` with PASS/FAIL, per-AC evidence (`file:line` + assertion + spec outcome), gate exit results, sensor result, and the diff/commit range covered.
4. **Chat return** — returns a compact verdict + ranked gap list to the orchestrator in chat; the orchestrator surfaces it and routes gaps to fix tasks.

The Verifier never changes code or tests — every mutation is restored from HEAD before it reports. It does NOT fix. It runs alone: no worker is in flight while it runs.

If the Verifier returns FAIL, the orchestrator turns the ranked gaps into fix tasks (clustered and dispatched to workers like any other wave), then re-verifies by **resuming the same Verifier** (`sub-agents.md` § *Failure handling*: send it the fix range and the gaps addressed — in Claude Code, `SendMessage` — while it is under its turn budget; fresh only when over budget) — bounded to a max of **3 fix→re-verify iterations** before escalating to the user.

If you are unsure whether more tasks remain, check `tasks.md`: if every task is marked complete, dispatch the Verifier now.

---

## Execution Template

```markdown
## Implementing T[X]: [Task Title]

**Reading**: task definition from tasks.md
**Dependencies**: [All done? ✅ | Blocked by: TY]
**Tests**: [unit/e2e/integration/none]
**Gate**: [quick/full/build]

### Pre-Implementation (MANDATORY)

- **Assumptions**: [state explicitly]
- **Files to touch**: [list ONLY these]
- **Success criteria**: [how to verify]

### Tests: Write tests derived from spec ACs

- Test file(s): [paths]
- Test count: [N test cases]
- Spec-derived: each test's asserted value maps to spec-defined outcome (or gap flagged)

### Implement

[Write minimum code to pass tests]

- Tests modified: None
- Tests skipped/deleted: None

### VERIFY: Gate Check

- Command: [gate check command]
- Result: [X passed, 0 failed]
- Test count: [N — matches planned test count]

### Post-Gate

- [x] No SPEC_DEVIATION (or markers added)
- [x] No unnecessary changes made
- [x] Matches existing patterns

**Test Adequacy Review:**

*Check A — Sufficient (coverage mapping):*

| Done-when criterion / spec AC / listed edge case | `file:line` + assertion expression | Spec-defined outcome | Covered? |
| ------------------------------------------------- | ---------------------------------- | -------------------- | -------- |
| [criterion] | `path/to/test.ts:42` — `expect(result.field).toBe(expected)` | [spec value] | ✅ Yes / ⚠️ Gap |

*Check C — Necessary (reverse mapping):*

| `file:line` + assertion expression | Maps to (AC / edge case / Done-when criterion) | Keep? |
| ---------------------------------- | ---------------------------------------------- | ----- |
| `path/to/test.ts:42` — `expect(result.field).toBe(expected)` | [requirement or criterion text] | ✅ Keep |

- [ ] Check A: every criterion covered with `file:line` evidence; spec-defined outcomes matched or gap flagged; per-layer depth met
- [ ] Check B: no shallow assertions; payload/conjunction rule applied to every payload-bearing criterion
- [ ] Check C: every test maps to a requirement — no speculative or unclaimed tests
- [ ] Check D: guideline conformance — [guideline file followed, or "none — strong defaults applied"]

**Verdict**: [All criteria covered, spec outcomes matched, no shallow assertions, all tests necessary] / [Rewritten: describe what was fixed]

**Status**: ✅ Complete | ❌ Blocked | ⚠️ Partial
```

**After the LAST wave (orchestrator):** dispatch the Verifier sub-agent (see step 10 and [sub-agents.md](sub-agents.md)) for independent feature-level validation, including the spec-anchored check and discrimination sensor. Validation always runs automatically — never prompted. Execute is not done until the Verifier reports PASS and the validation report is written.

---

## Tips

- **One task at a time (per worker)** — Focus prevents errors; parallelism lives between clusters, never inside one
- **Keep the noise out of context** — a worker that pastes a whole test log into itself loses the task; gates run redirected to a file, the scout answers the question you cannot scope
- **Tools matter** — Wrong MCP = wrong approach
- **Reuses save tokens** — Copy patterns, don't reinvent
- **Check before commit** — Verify all criteria, then commit
- **Stay surgical** — Touch only what's necessary, and only what you own
- **Commit per task, pathspec-limited** — Clean git history enables bisect and rollback, and siblings never end up in your commit
- **Never "while I'm here"** — Scope creep during implementation is the #1 quality killer
- **Stop early, report exactly** — a blocker reported at task 2 costs one re-dispatch; a guessed spec decision costs a re-verify loop
- **Don't stop at the last commit** — Feature-level validation (step 10) is the final step of Execute, not optional

---

## Pause / End of Session

When work is interrupted, paused, or a session ends before the feature is complete:

1. Open `.specs/STATE.md`.
2. Locate the `## Handoff` section.
3. **Replace only that section's body** with the current snapshot (feature, phase/task, completed, in-progress `file:line`, next step, blockers, uncommitted files, branch). See [memory.md](memory.md) for the exact format.
4. Do NOT touch the `## Decisions` section above it — decisions are written only during Design.

**Section-scoped write (critical):** Replace the content between the `## Handoff` header and the next `##` header (or end of file). Never overwrite the full file — doing so silently destroys the Decisions log.
