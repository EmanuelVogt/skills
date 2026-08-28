# Research — the human phase

**Goal:** the user and the pipeline converge on ONE artifact — the brief (`research.md`) — that is
good enough to plan from without asking anything else. The human's only pre-execution job happens
here: making the problem understood. Spend the questions here or pay for them as rework later.

**Language:** grill in the user's language; write `research.md` in English (SKILL.md Rule 6).

## Process

### 1. Intake, slug, classification

Take the user's statement as-is. Read `.ca-plans/DECISIONS.md` first if it exists — every `active`
AD-nn is a standing constraint: the brief conforms to it or explicitly supersedes it (mark the old
line `superseded by AD-mm`, append the new one), never silently ignores it; ground scouts and grill
questions on the ADs that touch this feature. Then create `.ca-plans/[feature]/` (short English
kebab-case slug) and start two files: `research.md` from the template below with
`Status: Research`, and the `plan.md` stub — `Status: Research`, `Started: <ISO datetime>`, brief
pointer — so the run is discoverable by resume from minute one. One line to the user: the slug and
what happens next (scouts + questions in parallel).

**Classify the input before the first question — concept or defined.** *Defined*: reproducible
behavior, a named flow/file, a precise expected outcome → straight to § 2 + § 3. *Concept*: a
solution named without its problem ("I want a notifications system"), no observable outcome, no
failure case the user can cite, no boundary → route through § 2.5 first. One judgement, stated in
the intake line; the user can shortcut it ("it's defined, converge"). Misreading defined as
concept costs an annoying interrogation; misreading concept as defined costs the whole run — when
in doubt, stress.

### 2. Scout fan-out — immediately, before the first question

Dispatch 2–4 scouts **in one message, in parallel with the grilling below** — do not wait for the
user's answers to start mapping. In Claude Code use the native `Explore` agent (or `repo-scout` if
installed); low tier for a pointed question, mid for an area map. Each scout's contract goes in its
payload:

```
Question: <one open question about the code, not a command>
Return: file:line + one-line facts only. Never file content, never code blocks. ≤1.5 kB.
```

What to map (pick what the problem needs, not all of it):

- **Entry points and the vertical** — where the affected behavior lives today: routes/handlers,
  services/use-cases, domain, persistence, UI. `file:line` per layer.
- **Patterns to copy** — the nearest existing feature that does something structurally similar;
  its file layout is the plan's template.
- **Test conventions and commands** — where tests live per layer, which runner, and the actual
  commands from the repo's own manifests/CI (`package.json`, `Makefile`, `pyproject.toml`,
  workflows…). Never invent a command; these become `plan.md`'s Gate Commands.
- **Risk surface** — migrations, contracts/codegen, shared packages, auth/payment paths the change
  might touch (these decide `Exclusive` tasks and the P0 flag later).

**Concept input → the first mission inverts:** before mapping the vertical, scouts hunt the
**evidence of the problem** — the current workaround, the TODO/FIXME trail, the error-handling
gap, the duplicated hack — and the blast radius a change would have. That is the ammunition § 2.5
grills with; a concept whose problem leaves no trace in the repo or in the user's memory is the
strongest kill signal there is.

Scout answers land in the brief's **Context Map** as `file:line` facts. The main window may follow
up with at most a couple of targeted ranged `Read`s on `file:line` the scouts named — the map is
facts in the main context, not file dumps.

### 2.5. Stress the concept (concept inputs only)

Converging on an unvalidated premise is the most expensive failure this pipeline has — everything
downstream verifies conformance to the brief; nothing verifies the brief. So before refining HOW,
attack WHETHER — 1–2 rounds, adversarial, grounded in what the scouts found:

- What problem does this solve? When did it last actually happen, to whom?
- What happens if we build nothing? (the do-nothing baseline is a real competitor)
- What is the simplest alternative that solves 80%? (name one yourself, from the scouts' map)
- What would make you kill this feature a month from now?
- Is this the right layer/place in the system for it?

Three exits, each said plainly:

1. **Sharpened** — the premise survives with a concrete problem + evidence → § 3, converge.
2. **Pivot** — the real problem is a different one → restate it in one line, get a nod, then § 3
   on the restated problem.
3. **Kill** — do-nothing or the simpler alternative wins → say so, with the evidence, and
   recommend not running the pipeline. The user decides (Research is the human phase); a stress
   test that cannot conclude "don't build" is theatre. A kill rationale, or a rejected alternative
   that will hold for future runs, → one AD-nn line in `.ca-plans/DECISIONS.md`.

Defined inputs skip this section entirely — a reproducible bug does not need its premise attacked.

### 3. Grill the user — rounds, grounded in the code

While scouts run (and after they return) — for a concept input, only once § 2.5 settled the
premise — work in **rounds of 2–4 pointed questions, each with a
recommended answer**, in the user's language. One round at a time; the answers shape the next
round. Ground questions in what the scouts found ("today X happens at `file:line` — keep or
change?") — grounded questions get real answers, abstract ones get vibes.

Cover, when the feature has the dimension at all (skip what plainly does not apply):

| Dimension | The question behind it |
| --- | --- |
| Outcome | What does done look like, observably? What would you demo? |
| Boundary | What is explicitly OUT? (record it — it is the anti-scope-creep anchor) |
| Behavior grays | User-facing choices that could go multiple ways (layout, errors, tone, formats) |
| Failure/partial states | Timeouts, partial saves, retries, duplicates |
| Auth & limits | Who may call this; rate/permission boundaries |
| State & concurrency | Transitions, ordering, races |
| Data lifecycle | TTL, deletion, migration of existing rows |

Rules of the grill:

- **Challenge vagueness.** "Good", "simple", "users" — make them concrete: "walk me through it".
- **Recommend, don't poll.** Every question carries your recommended answer and why; the user
  corrects or confirms. "You decide" is a valid answer — it becomes an Assumption, owned by you.
- **Scope is sacred.** New capability mid-grill → one line to Out of Scope ("noted, out of this
  run"), never absorbed.
- **Stop when saturated.** When another round would only produce Assumptions you can own, stop
  asking and write the brief. Unanswered grays become Assumptions with your chosen default and
  rationale — never silent gaps.

### 4. Verify what you claim (knowledge chain)

Any technical claim in the brief walks, in order: **codebase → project docs → Context7 MCP → web
search → flagged as uncertain**. Never fabricate an API, pattern or behavior — a flagged "I don't
know" beats a cascading failure through plan → implementation. Uncertain items land in Assumptions,
flagged.

### 5. Write the brief

## Template: `.ca-plans/[feature]/research.md`

```markdown
# [Feature] — Brief

**Status:** Research | Confirmed
**Base:** [HEAD hash at confirmation — resume diffs against it to spot Context Map drift]
**P0:** yes/no — [auth, payments, money movement, availability/booking, data integrity — or "no"]

## Problem
[≤5 lines: the pain, why now, what done looks like.]
[Evidence: `file:line` or a concrete account — who hit this, when. A problem with no trace is an
assumption, not a fact.]
[Why this and not <simplest rejected alternative> — one line. Mandatory for concept inputs.]

## Context Map
[file:line facts from scouts — the vertical today, the pattern to copy, the risk surface. One line
each. This section is why Plan needs no re-discovery.]
- `src/…/handler.ts:42` — current entry point for X
- `src/…/similar-feature/` — structural template to copy
- gate commands: unit `<cmd>`, e2e `<cmd>`, typecheck `<cmd>`, lint `<cmd>`

## Decisions
[One line per settled gray, from the grill. D-01, D-02… Workers receive these as payload pointers.]

## Acceptance Criteria
[Numbered, WHEN/THEN, each with a precise outcome and a proof the Reviewer will check.]
- AC-01 — WHEN [event] THEN [system] SHALL [precise outcome]. Proof: test
- AC-02 — … Proof: gate   (build/typecheck/lint-class outcomes ONLY — a behavioral AC marked
  `gate` passes on any green suite; it needs a `test` or a `probe`)
- AC-03 — … Proof: probe: `<command>`   (≤3 probes; a 4th means it should be a test)

## Edge Cases
[Each edge case IS an AC: numbered in the same AC-nn sequence, with a proof — listed here for
readability. An edge case outside the AC numbering is invisible to every verifier downstream.]
- AC-07 — WHEN [boundary/error] THEN SHALL [handling]. Proof: test

## Out of Scope
| What | Why out |

## Assumptions
| Assumption | Chosen default | Rationale |
[Everything unanswered or flagged-uncertain lands here. Nothing is silently unclear.]

## Segments
[Only when Plan segments the run (plan.md § 0): one line per segment — `plan-01 · AC-01..05 ·
Done` — updated at each segment close. Single-plan runs omit this section.]
```

Cap ≤ ~8 kB. Measurements, long grep output, survey narrative — do not belong here; keep the
`file:line` and drop the rest.

### 6. The gate — the one confirmation

Present in chat (user's language): problem in one line, the decisions taken, the ACs, what is out,
and the assumptions you chose. Then the contract, explicit:

> "Confirming this brief starts the autonomous stretch: plan, implementation in waves, independent
> review. Next time I need you is QA."

- User corrects → fold in, re-present only the changed lines.
- User confirms → set `Status: Confirmed`, record `Base: <current HEAD>` in the brief, flip the
  `plan.md` stub to `Status: Planning`. A settled decision that binds future runs, not just
  this feature, is appended to `.ca-plans/DECISIONS.md` as the next AD-nn (one line). Recommend
  the tier switch if applicable (SKILL.md § *Model Economics*, one line, never blocking), and go
  straight to [plan.md](plan.md). No further permission exists between here and QA.
