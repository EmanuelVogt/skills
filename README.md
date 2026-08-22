# skills

Agent skills for people who build with AI: deciding what is worth building, and staying in control of what got built.

| Skill | What it does |
|---|---|
| [`grill-my-idea`](grill-my-idea/SKILL.md) | Interrogate a business idea, then research it for real — TAM/SAM/SOM, competitors at home and abroad, cost to run, break-even, three scenarios — and issue a verdict: GO, VALIDATE-FIRST, PIVOT or KILL. Writes a full dossier to `ideas/<slug>/`. |
| [`debt`](debt/SKILL.md) | Register technical or cognitive debt about AI-written code. Investigates definition, every call site and the design rationale, then writes a structured entry to a personal ledger. |
| [`crash-course`](crash-course/SKILL.md) | Write a study document — history, ELI5, how it works, how *your* project uses it, trade-offs, alternatives, references — about a registered debt or any topic. |

## Why

AI makes it cheap to build the wrong thing, and then hard to understand the thing you built.

- **Before the code** — the cost of an idea is months of your life, and the expensive failure is a false positive: an encouraging analysis of something that was never going to work. `grill-my-idea` is the counterweight. Its default verdict is not "promising".
- **Tech debt** — shortcuts you know about: no tests, magic numbers, a hack that works today.
- **Cognitive debt** — code that may be fine, but you couldn't explain it. Paying it means *understanding*, not rewriting.

`grill-my-idea` decides whether to start. `debt` catalogues what starting cost you. `crash-course` pays the cognitive kind.

## Install

```sh
npx skills add EmanuelVogt/skills@grill-my-idea
npx skills add EmanuelVogt/skills@debt
npx skills add EmanuelVogt/skills@crash-course
```

## Use

```
# just describe the idea — the skill triggers on its own
/grill-my-idea a scheduling tool for small pet shops, R$ 149/month
/grill-my-idea                      # then paste the pitch; it grills you in rounds
```

```
/debt src/billing/retry.ts          # register — the skill investigates, you confirm
/debt list                          # open entries
/debt pay DEBT-007                  # mark as paid, keeps history
/crash-course DEBT-007              # study material from a registered debt
/crash-course event sourcing        # or any topic
```

`grill-my-idea` writes to `ideas/<slug>/` in the working directory. `debt` and `crash-course` write to `.learning/` at the project root — personal, added to `.gitignore` automatically.

## How grill-my-idea works

Seven phases. It asks you only what it cannot look up, and looks up everything else.

1. **Intake** — slug, folder, the pitch saved verbatim.
2. **Grill** — the idea becomes a tree of assumptions, worked in rounds of 2–4 questions, each with a recommended answer. Every claim is tagged `[fact]`, `[belief]`, `[assumption]` or `[unknown]`. Say "don't ask me" and it fills the tree itself, then lists the assumptions it made on your behalf.
3. **Research** — 25–40+ searches across ten dimensions, in parallel: market size, competitors home and abroad, demand evidence, pricing, regulation and tax, cost benchmarks, channels and CAC, and the graveyard of companies that tried this before. PT-BR queries for Brazilian sources, EN for international.
4. **Model** — cost to run, unit economics, break-even and three scenarios, computed by a script, not guessed.
5. **Judge** — tarpit patterns, five forces, red flags by severity, a pre-mortem, and a weighted scorecard with override rules.
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

Locale: the default home market is Brazil, so the cost, tax and channel guidance is concrete — CLT vs PJ, Simples Nacional Anexo III vs V and Fator R, Pix/boleto/card fees, WhatsApp Business Platform pricing, IBGE and Receita Federal CNPJ counts, Reclame Aqui as a research source. Name another country and it swaps to that country's registries and rails. The dossier is written in English regardless of the language you write in.

## License

MIT
