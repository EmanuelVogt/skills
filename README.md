# skills

Agent skills for people who build with AI.

| Skill | What it does |
|---|---|
| [`grill-my-idea`](grill-my-idea/SKILL.md) | Interrogate a business idea, then research it for real — TAM/SAM/SOM, competitors at home and abroad, cost to run, break-even, three scenarios — and issue a verdict: GO, VALIDATE-FIRST, PIVOT or KILL. Writes a full dossier to `ideas/<slug>/`. |
| [`debt`](debt/SKILL.md) | Register technical or cognitive debt about AI-written code. Investigates definition, every call site and the design rationale, then writes a structured entry to a personal ledger. |
| [`crash-course`](crash-course/SKILL.md) | Write a study document — history, ELI5, how it works, how *your* project uses it, trade-offs, alternatives, references — about a registered debt or any topic. |
| [`ca-spec-driven`](ca-spec-driven/SKILL.md) | Spec-driven feature work in four auto-sized phases — Specify, Design, Tasks, Execute — with Execute delegated to parallel workers in waves and closed by an independent Verifier. Writes specs, decisions and self-improving lessons to `.specs/`. |
| [`ca-full-cycle`](ca-full-cycle/SKILL.md) | Research → Plan → Implement → Review with ONE human gate before code: collaborative research (grilling + parallel scouts), then autonomous planning, worker waves with a per-wave verifier, an independent Reviewer, and a human QA loop at the end. Writes the brief, plan and review to `.ca-plans/`. |

Each skill stands alone. Install only the one you want.

---

# grill-my-idea

A skeptical business analyst for an idea you are thinking about building.

The expensive failure is a false positive: an encouraging analysis of something that was never going to work. Optimism is the default failure mode of founders and language models alike, so this skill is built as the counterweight. Its default verdict is not "promising".

## Install

```sh
npx skills add EmanuelVogt/skills@grill-my-idea
```

## Use

```
# just describe the idea — the skill triggers on its own
/grill-my-idea a scheduling tool for small pet shops, R$ 149/month
/grill-my-idea                      # then paste the pitch; it grills you in rounds
```

Say *"don't ask me anything, assume what you need"* and it runs end to end on its own, listing every assumption it made on your behalf. Output goes to `ideas/<slug>/` in the working directory.

## How it works

Seven phases. It asks you only what it cannot look up, and looks up everything else.

1. **Intake** — slug, folder, the pitch saved verbatim.
2. **Grill** — the idea becomes a tree of assumptions, worked in rounds of 2–4 questions, each with a recommended answer. Every claim is tagged `[fact]`, `[belief]`, `[assumption]` or `[unknown]`, so you can see which parts of your plan are load-bearing guesses.
3. **Research** — 25–40+ searches across ten dimensions, in parallel: market size, competitors home and abroad, demand evidence, pricing, regulation and tax, cost benchmarks, channels and CAC, and the graveyard of companies that tried this before. PT-BR queries for Brazilian sources, EN for international.
4. **Model** — cost to run, unit economics, break-even and three scenarios, computed by a script, not guessed.
5. **Judge** — tarpit patterns, five forces, red flags by severity, a pre-mortem, and a weighted scorecard with override rules that a fatal weakness cannot be averaged away from.
6. **Go-to-market** — positioning, beachhead, channels with CAC, and a 30/60/90 validation plan with kill criteria.
7. **Compile** — the dossier.

Every number carries `[data]`, `[benchmark]`, `[estimate]` or `[guess]` plus a source. "Not found" is a valid finding; inventing a number is not.

## The dossier

```
ideas/<slug>/
├── README.md                 verdict, the numbers, the likeliest killer, next 30 days
├── 00-intake.md              your pitch, verbatim
├── 01-interview.md           the assumption tree and what was settled vs. assumed
├── 02-market.md              TAM/SAM/SOM home + international, why-now, regulation
├── 03-competitors.md         landscape, positioning map, what reviews say is missing, the graveyard
├── 04-customer-and-demand.md ICP, jobs-to-be-done, evidence of pain, willingness to pay
├── 05-financial-model.md     cost to run, unit economics, break-even, three scenarios
├── 06-go-to-market.md        positioning, beachhead, channels & CAC, first 100 customers
├── 07-risks-and-verdict.md   red flags, five forces, pre-mortem, scorecard, the verdict
├── 08-validation-plan.md     30/60/90 experiments with go and kill criteria
├── model.json                re-runnable model inputs
├── sources.md                every URL, with access date and a trust tier
└── research/                 raw notes per dimension
```

The README opens with the answer, not a build-up:

```markdown
# Pet-shop grooming SaaS — Verdict: PIVOT
2026-08-22 · Game: indie / lifestyle business · Home market: Brazil

> Not a bad idea — a commodity one. The incumbent already ships your
> differentiator at your price.

| | Pessimistic | Realistic | Optimistic |
|---|---:|---:|---:|
| **When each founder earns R$ 20k/month** | never | month 41 | month 30 |
| Users to break even (sustainable) | 642 | 248 | 185 |
| First profitable month | never | 11 | 6 |
| Cash needed to get there | R$ 680k | R$ 162k | R$ 103k |
```

Two rules make the difference between a report and a decision. Whatever you actually asked — "can I live off this?", "is it worth quitting?" — becomes a row with a number in all three scenarios. And any verdict below GO must name 2–4 escape routes with the model re-run for each, so "no" arrives with the version that does work: *charge 1% of the payments flowing through instead of a flat fee — 830 customers needed drops to ~180.*

## The financial model

`scripts/financial_model.py` — standard library only, so it runs anywhere. You give it a `model.json`; it gives you three scenarios month by month.

```sh
python3 grill-my-idea/scripts/financial_model.py --example > model.json
python3 grill-my-idea/scripts/financial_model.py model.json --md tables.md --out model_output.json
```

It reports break-even four ways, because "how many users do I need" has four different honest answers:

| | Meaning |
|---|---|
| Simple | Users to cover fixed costs, if acquisition were free |
| At planned spend | What the monthly result actually needs, marketing included |
| Sustainable | Fixed costs ÷ (contribution − CAC × churn) — pays to replace churned users too |
| Steady-state ceiling | Where the user count plateaus with the budgeted engine |

It refuses to flatter you. When the ceiling sits below the break-even, or the sustainable break-even exceeds the year-3 SOM, it says so:

```
- [Realistic] sustainable break-even (248) exceeds SOM year 3 (240): the model does not
  close inside the obtainable market.
- [Pessimistic] the acquisition engine as budgeted plateaus at ~250 users, below the 423
  needed to break even at planned spend: raise the budget, cut CAC or churn — and say
  which is believable.
```

## Locale

The default home market is Brazil, so the cost, tax and channel guidance is concrete — CLT vs PJ, Simples Nacional Anexo III vs V and Fator R, Pix/boleto/card fees, WhatsApp Business Platform pricing, IBGE and Receita Federal CNPJ counts, Reclame Aqui as a research source. Name another country and it swaps to that country's registries and rails. The dossier is written in English regardless of the language you write in.

---

# debt · crash-course

Two skills for staying in control of code an AI wrote. They work together: `debt` catalogues, `crash-course` pays.

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

---

# ca-spec-driven

Spec-driven development for agents that ship features, not prose. Four phases — Specify, Design, Tasks, Execute — sized to the feature's real complexity: a three-file change gets a one-liner spec and runs inline; a multi-component feature gets requirement IDs, an architecture pass and a task breakdown. The pipeline decides its own depth; you never fill in ceremony.

The distinctive part is Execute. From four tasks up, the window that planned the feature never implements — it becomes an orchestrator that dispatches cheap workers over vertical clusters, waves of them in parallel, one atomic commit per task, a build gate per wave. After the last wave a fresh, independent Verifier (author ≠ verifier, always on, never prompted) checks outcomes against the spec's acceptance criteria with evidence-or-zero and writes the validation report. Tests derive from the spec, never from the implementation.

Derived from **TLC Spec-Driven 3.2.0** by [Felipe Rodrigues](https://github.com/felipfr) (CC-BY-4.0); this fork adds the delegation model — worker waves, cluster parallelism over vertical slices, tier-per-dispatch model selection, English-only artifacts — hardened in production use.

## Install

```sh
npx skills add EmanuelVogt/skills@ca-spec-driven
```

The delegation model works best with the four role templates in [`ca-spec-driven/agents/`](ca-spec-driven/agents/) — worker, verifier, scout, runner — copied into your project's `.claude/agents/` (restart the session; Claude Code loads agents at start). Without them the skill says so and runs the same protocol inline, degraded but honest.

## Use

```
# it triggers on its own phrases — just talk
specify a cancellation-fee feature
design it
break it into tasks
implement
validate
pause work            # snapshot to .specs/STATE.md
resume work           # picks up from the handoff
```

## What it leaves behind

```
.specs/
├── STATE.md            project memory: decisions log + handoff snapshot
├── LESSONS.md          self-improving playbook, distilled from verified failures
└── features/<slug>/    spec.md · context.md · design.md · tasks.md · validation.md
```

Everything under `.specs/` is written in English regardless of the language you chat in — agents are the only readers, and English artifacts cost ~30–40% fewer tokens per re-read.

---

# ca-full-cycle

`ca-spec-driven`'s lean sibling: the same delegation machinery, one human gate instead of four.

Research → Plan → Implement → Review. The human appears exactly twice: at **Research**, where a raw concept is
stress-tested first (evidence of the problem, the do-nothing baseline, the simpler alternative —
it can recommend not building) and the grill runs in rounds (each question grounded in what the
code scouts found, each with a recommended answer) until one brief — problem, context map, decisions, acceptance criteria with
proofs — is confirmed; and at **QA**, where you test the shipped feature against a generated QA
script and every finding is triaged (broken vs. brief → fix wave; new behavior → delta research;
works as specified → your call). Everything between the two runs alone: a top-tier plan over the
mapped context, workers in parallel waves with a fresh verifier closing every wave, and an
independent Reviewer (author ≠ reviewer, evidence-or-zero, mutation sensor) closing the feature.

The economics are the design: scouts are cheap and disposable while every important fact lands in
the main window; the expensive window plans and orchestrates but never types; workers are tiered
per dispatch (haiku for mechanics, sonnet by default, opus where domain rules live); the one
high-tier fresh read comes at the end, where a wrong answer is most expensive.

## Install

```sh
npx skills add EmanuelVogt/skills@ca-full-cycle
```

No agent templates required — it dispatches generic sub-agents with role cards. If
`ca-spec-driven`'s templates are installed, it uses them.

## Use

```
/ca-full-cycle the export button generates a broken CSV when filters are active
research this and implement it end to end
resume full-cycle
qa: item 2 failed, the date column is still ISO
```

## What it leaves behind

```
.ca-plans/
├── DECISIONS.md        cross-run project decisions — lean AD log
├── RUNS.md             one entry per run: size, wall time, tokens by tier, estimated cost
└── <slug>/
    ├── research.md     the brief: problem, context map, decisions, ACs with proofs
    ├── plan.md         tasks, wave plan, gate commands, live statuses (the resume point)
    └── review.md       Reviewer report: per-AC evidence, sensor result + the QA log
```

English artifacts, same rationale as `ca-spec-driven`: agents are the only readers.

---

## License

MIT — except [`ca-spec-driven/`](ca-spec-driven/) and [`ca-full-cycle/`](ca-full-cycle/), which are CC-BY-4.0 as derivatives of TLC Spec-Driven by Felipe Rodrigues.
