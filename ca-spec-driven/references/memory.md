# Memory Layer

**File:** `.specs/STATE.md`

A single file with two section-scoped parts. Each section has its own lifecycle; writes are always targeted — never whole-file overwrites.

**Language:** English, both sections, always (SKILL.md Critical Rule 6). This is the file most exposed to drift — a decision discussed with the user in their own language gets recorded here, and it is then re-read at every Design and every resume for the life of the project. Record the decision in English; quote the original language only for a product string or a domain term with no English equivalent. When you touch an older entry written in another language (supersede, correct), translate the entry you touch.

---

## Sections

### `## Decisions` — append-only log

Records **project-level** decisions only: conventions, patterns, constraints, or cross-cutting technology choices that future features must follow or supersede.

**Not project-level → stays in the feature's `design.md` Tech Decisions table.**  
Heuristic: would a different feature need to know about this? If yes → project-level. If no → feature-local.

**Format** (one entry per decision):

```markdown
## Decisions

### AD-001
- **Decision**: [what was decided — one sentence]
- **Reason**: [why this option was chosen]
- **Trade-off**: [what was given up]
- **Scope**: [which features / packages / layers this governs]
- **Date**: YYYY-MM-DD
- **Status**: active | superseded by AD-NNN
```

**Supersession rule:** When a new decision replaces an old one, append a new `AD-NNN` entry and update the old entry's `status` field to `superseded by AD-NNN`. Never delete old entries — the history is the audit trail.

---

### `## Handoff` — pause snapshot (~500 tokens per open feature, overwritten each pause)

Captures mid-task / in-flight state so work can resume without re-reading the full task history. This is the sole position tracker; it complements `tasks.md` by recording state that `tasks.md` does not capture.

**Open work only.** The Handoff is re-read whole on every resume for the life of the project, so it never carries closed features. At closeout the feature's entries leave the Handoff for `.specs/features/done/[feature]/handoff-archive.md` (verbatim; a short pointer line may stay for a closed-but-unpushed merge). What is left, not what was done: finished-work narrative belongs in `validation.md`.

**Readers.** The orchestrator (planning window) reads and writes it. Workers, scouts, runners and the Verifier **never read `STATE.md`**: `design.md` carries the `AD-NNN` decisions a task depends on, and the orchestrator pastes any other needed decision as one line in the payload.

**Format:**

```markdown
## Handoff

- **Feature**: [feature name / .specs path]
- **Wave / Cluster / Task**: [e.g., wave 2 / C3 / T4 — implement repository layer]
- **Completed**: [comma-separated task IDs or "none"]
- **In-flight clusters**: [e.g., C3 (T2 → T4) dispatched, no summary yet | none]
- **In-progress** (file:line): [e.g., `src/billing/subscription.service.ts:88` — mid-write]
- **Next step**: [one sentence — exactly what to do next]
- **Blockers**: [none | description]
- **Uncommitted files**: [list or "none"]
- **Branch**: [git branch name]
```

---

## File shape

```markdown
# STATE

## Decisions

[AD-NNN entries…]

## Handoff

[latest snapshot…]
```

If the file does not yet exist, create it with both section headers and empty bodies.

---

## Read / Write Triggers

| Trigger | Section | Operation |
| ------- | ------- | --------- |
| Design phase, Step 1 (Load Context) | `## Decisions` | **Read** — conform to active decisions or supersede |
| Design phase, Tech Decisions step | `## Decisions` | **Append** — only for project-level decisions |
| Pause work / end of session | `## Handoff` | **Replace** — overwrite Handoff section only |
| Resume work / start of session | `## Handoff` | **Read** — load snapshot, propose next step |
| Resume work / start of session | `## Decisions` | **Read** — re-confirm active constraints before designing |
| Closeout (after Verifier PASS + local merge) | `## Handoff` | **Move** the feature's entries to `.specs/features/done/[feature]/handoff-archive.md`; keep only open work |
| Execute (workers, scouts, runners, Verifier) | both | **Never read** — decisions arrive as one line in the payload |

---

## Section-scoped write rule (critical)

One file holds two lifecycles. Writes MUST target their section only:

- **Design appends** to `## Decisions`. It MUST NOT touch `## Handoff`.
- **Pause replaces** `## Handoff`. It MUST NOT rewrite, reorder, or drop any entry in `## Decisions`.

The correct technique: locate the target section header, replace only the content between it and the next `##` header (or end of file). Never overwrite the full file.

Violating this rule causes one of two failures:
1. A pause write clobbers the decisions log → decisions are silently lost.
2. A design append touches the handoff snapshot → mid-task state is corrupted.

Both are silent data loss. The section-scoped write rule is the single correctness invariant of this memory layer.

---

## Pause / Resume Procedure

### Pause

1. Locate the `## Handoff` section in `.specs/STATE.md`.
2. Replace its body (everything between `## Handoff` and the next `##` or EOF) with the current snapshot.
3. Do NOT modify anything above or before `## Handoff`.
4. Wait for any in-flight cluster to report before pausing (or record it as in-flight); commit what is finished. Never `stash` — the checkout is shared with workers, and stashing moves their state.

### Resume

1. Read `.specs/STATE.md` — both sections.
2. Re-confirm active decisions from `## Decisions` — nothing superseded since last session?
3. Read `## Handoff` — identify feature, phase/task, next step, blockers, uncommitted files, branch.
4. Propose the next step to the user before writing any code.

---

## AD-NNN numbering

- Numbers are sequential, project-scoped, and permanent — never reused.
- The counter starts at `AD-001`. Check existing entries before assigning the next number.
- If `.specs/STATE.md` does not exist, the first decision is `AD-001`.
