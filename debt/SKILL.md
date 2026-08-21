---
name: debt
description: Register technical or cognitive debt about something AI implemented in the project, as a personal pending item in `.learning/DEBT.md`. Use whenever the user explicitly asks to record, log, note or flag a debt — "/debt", "log this as debt", "note this as tech debt", "I don't understand what you did here, flag it for me to review", "leave this pending for me to study later", "this is a hack, write it down", "tech debt", "cog debt", "cognitive debt". Also use for "pay DEBT-NNN", "resolve DEBT-NNN", "list debts", "what's pending in the ledger". Do NOT trigger proactively after finishing an implementation; only the user decides what is debt.
---

# Debt ledger

The user works with AI and ends up with two kinds of leftovers:

- **tech debt** — the code has a known shortcut: no tests, magic numbers, coupling, a hack that works today.
- **cog debt** (cognitive debt) — the code may even be fine, but the user does not understand what was built. Paying it means *understanding*, not necessarily changing code.
- **cog+tech** — both at once. Common: an AI-generated regex parser that is fragile *and* unreadable.

Your job is to **investigate and catalogue**, not to hand the user a form. Someone with cognitive debt cannot answer "where is this used and why" — that is exactly what they are missing. You find it.

Everything lives in `.learning/`, which is personal and gitignored. Never suggest sharing it.

## Subcommands

| Input | Action |
|---|---|
| `/debt <target>` or a phrase pointing at code | Register a new entry (main flow below) |
| `pay DEBT-NNN` / "mark as resolved" | Set status to `paid`, add resolution date + one line on how. Never delete entries — history is the point. |
| `list` / "what's pending" | Print open entries: id · type · concept · where. Nothing else. |

## Registering a debt

### 1. Bootstrap (first run only)

If `.learning/` does not exist at project root: create it, create `.learning/DEBT.md` from `assets/ledger-header.md`, and append `.learning/` to `.gitignore` (create `.gitignore` if missing). Tell the user in one line that the folder is personal and ignored by git.

### 2. Locate the target

The target can be precise (`src/billing/retry.ts`, `withRetry()`) or vague ("that retry thing you did yesterday", "the cache part"). Resolve it with `rg` and, when it was built in this session, with what you remember. If two or more plausible matches exist, ask once with the candidates (file + one line of context each) — never guess between them.

### 3. Investigate

This is where the value is. Do not skip steps because the user only named one file.

- **Definition**: read the full unit (function/class/module), not just the lines cited.
- **All call sites**: `rg` for the symbol across the project. The user usually knows one usage; the ledger must list all of them, each with one line on what that caller is doing. Flag usages that look questionable (e.g. retry wrapping a non-idempotent operation).
- **Why it was done this way** (design rationale): look in order at code comments, adjacent code, `git log -S"<symbol>"` / `git log -p` on the file, and your own memory if you wrote it this session. Mark the source of each claim. If you find nothing, write "rationale not found — inferred from <X>" and keep the inference short. A confident-sounding invented rationale is worse than none: it will be fed to a crash course later and become "truth".
- **Why it is debt**: name what is missing concretely — test, understanding, coupling, magic value, undocumented invariant. For cog debt, say what the user would need to be able to explain.
- **Concept**: the general topic this code is an instance of (e.g. "exponential backoff with jitter", "optimistic locking", "JWT refresh rotation"). One line. This field is what `/crash-course DEBT-NNN` will teach, so keep it to one concept; if the code mixes three, register three entries or pick the one the user actually pointed at and mention the others as candidates.

### 4. Classify

Decide `cog`, `tech` or `cog+tech` from what the user said plus what you found. "I don't get this" → cog. "This is a hack" → tech. Unreadable hack → cog+tech. If the user's phrasing and your findings disagree, go with the user's and note your observation in "Why it is debt".

### 5. Show, confirm, write

Render the entry using `assets/entry-template.md`, show it, and write only after the user confirms or edits. Next id = highest existing `DEBT-NNN` + 1, zero-padded to 3 digits. Append to the end of `DEBT.md`.

### 6. Candidates (optional, one line each)

If during investigation you found *other* suspicious code clearly related to the target, list it at the end as "candidates" — do not register it. The user decides.

## Entry fields, and why each exists

- `Concept` — single topic; the hook for crash-course.
- `Where` — definition location with line range.
- `Usages` — every call site; this is what the user cannot produce alone.
- `What the AI did` — what was built, 1-3 lines, plain language.
- `Why it was done this way` — design rationale with source marked.
- `Why it is debt` — what is missing.
- `To pay` — concrete action. For cog: usually "read crash course + answer the self-test questions" or "re-derive X and write it down". For tech: the code change.
- `Paid when` — an observable condition, so "done" is not a feeling.
- `Crash course` — empty at registration; `/crash-course` fills it with the file path.

## Tone

The ledger is the user's private notebook. Write it the way a careful colleague would leave a note: direct, concrete, no hedging, no praise of the code. The reader is the same person months later with zero context.
