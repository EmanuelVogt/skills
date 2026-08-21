# skills

Agent skills for people who build with AI and want to stay in control of what got built.

| Skill | What it does |
|---|---|
| [`debt`](debt/SKILL.md) | Register technical or cognitive debt about AI-written code. Investigates definition, every call site and the design rationale, then writes a structured entry to a personal ledger. |
| [`crash-course`](crash-course/SKILL.md) | Write a study document — history, ELI5, how it works, how *your* project uses it, trade-offs, alternatives, references — about a registered debt or any topic. |

## Why

AI writes code faster than you can understand it. Two things pile up:

- **Tech debt** — shortcuts you know about: no tests, magic numbers, a hack that works today.
- **Cognitive debt** — code that may be fine, but you couldn't explain it. Paying it means *understanding*, not rewriting.

`debt` catalogues both. `crash-course` pays the cognitive kind.

## Install

```sh
npx skills add EmanuelVogt/skills@debt
npx skills add EmanuelVogt/skills@crash-course
```

## Use

```
/debt src/billing/retry.ts          # register — the skill investigates, you confirm
/debt list                          # open entries
/debt pay DEBT-007                  # mark as paid, keeps history
/crash-course DEBT-007              # study material from a registered debt
/crash-course event sourcing        # or any topic
```

Everything is written to `.learning/` at the project root — personal, added to `.gitignore` automatically.

## Ledger entry

```markdown
## DEBT-007 · cog · open · 2026-08-21

**Concept:** exponential backoff with jitter
**Where:** src/billing/retry.ts:40-88
**Usages:**
- src/billing/charge.ts:112 — retry around Stripe charge
- src/jobs/invoice.ts:58 — retry around email send (questionable usage: not idempotent)

**What the AI did:** wraps a call in up to 5 retries, waiting base × 2^n with random jitter.
**Why it was done this way:** Stripe returns 429 under end-of-month load _(source: commit 3f2a1c)_
**Why it is debt:** nobody on the team can justify base=200ms / max=5 or predict behaviour under load.
**To pay:** read crash course, answer self-test, then either document the limits or tune them.
**Paid when:** rationale lives next to the constants, or limits changed with a load test.
**Crash course:** —
```

## Crash course structure

Ten fixed sections, ordered by depth — a non-technical reader stops at 3, a junior dev at 6, a senior reads to the end:

1. In one sentence · 2. Real-world analogy · 3. Why this exists in YOUR project · 4. History · 5. How it works, step by step · 6. Reading the project code · 7. Trade-offs · 8. Alternatives not used · 9. Self-test questions · 10. References

## License

MIT
