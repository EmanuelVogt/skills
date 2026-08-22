# Financial model reference

How to turn a grilled idea into defensible numbers — market size, cost to run, price, unit economics, break-even and three scenarios — and how to encode them in `model.json` for `scripts/financial_model.py`. The script does the arithmetic; this file is about choosing inputs you can defend.

## Contents

1. Ground rules and evidence labels
2. Market sizing (TAM / SAM / SOM)
3. Cost to run (Brazil, plus an international variant)
4. Pricing and ARPU
5. Unit economics
6. Break-even, peak cash and runway
7. Three scenarios
8. Filling `model.json` step by step
9. Reading the script output into the report

## 1. Ground rules and evidence labels

- Every input carries a label, written into `notes` and repeated in the report: `[data]` (a cited figure: IBGE, Receita, a competitor's pricing page, a filing, an association report), `[benchmark]` (an industry range, from this file or from research), `[estimate]` (arithmetic on sources and benchmarks), `[guess]` (no evidence beyond intuition). Labels make the model attackable one assumption at a time, which is the point.
- Magnitude beats precision. The question is whether this is a R$ 10k/month, R$ 100k/month or R$ 1M/month business and how much cash it eats before paying for itself — not the third significant digit.
- Bottom-up is the spine; top-down is the sanity check. A top-down number borrows someone else's denominator and hides every assumption inside it; a bottom-up count exposes each assumption.
- The realistic case is the one you defend line by line. Pessimistic and optimistic are alternative worlds with their own stories, never an error bar around the base.
- Brazilian rates (taxes, fees, salaries) drift yearly and the 2026–2033 tax reform (CBS/IBS replacing PIS/COFINS/ISS/ICMS) is in transition. Treat every BR figure here as a 2025–2026 range to verify, and say so in the report when the verdict hinges on one.

## 2. Market sizing (TAM / SAM / SOM)

### 2.1 Definitions, in customers and in money

| Layer | Question it answers | Schema field | Annual revenue |
|---|---|---|---|
| TAM | Everyone with the problem who could conceivably pay, across the geography you will ever serve | `tam_users` | `tam_users × arpu_monthly × 12` |
| SAM | The slice your product, channel, language, price band and compliance can reach within ~3 years | `sam_users` | `sam_users × arpu_monthly × 12` |
| SOM | What you can win from SAM by year 3 given competition and your GTM capacity | `sam_users × som_share_year3` | `SOM users × arpu_monthly × 12` |

Always state all three as a customer count and as BRL per year. Investors think in money, the sales plan thinks in customers, and the break-even check (§6) needs the count.

### 2.2 Three methods

**Top-down.** Category size from a report (Statista, ABES, Abstartups, ABComm, Sebrae, IBGE, Banco Central, analyst notes) × geographic share × segment share × capturable share. Fast and citable, and almost always too large: the category includes buyers who will never consider you, and vendor-sponsored forecasts lean generous.

**Bottom-up (preferred for SAM and SOM).**

```
TAM_revenue = Σ over segments (count of potential customers × ARPU × 12)
SAM         = TAM filtered by geography, segment, size band, channel reach,
              tech prerequisites, regulation, price band
SOM         = SAM × share obtainable by year 3
```

Counts come from IBGE (CEMPRE, PNAD, Censo), the Receita Federal CNPJ base filtered by CNAE and porte, Sebrae, professional councils (CFM, CRO, CREFITO, OAB, CREA, CRC), association reports, merchant counts (Shopify, Nuvemshop, VTEX, Tray), app-store install counts, LinkedIn Sales Navigator filters, and Google Maps density samples extrapolated by city. Discount CNPJ counts by 30–40 % for dormant registrations.

**Value theory (new categories).**

```
value per customer per year = cost of the problem today × share your solution removes
price                       = 10–30 % of that value (B2B); consumer anchors on adjacent habits
TAM                         = customers × price
```

Use it when no category exists yet, then check that the implied price survives contact with the competitor list (§4.1).

### 2.3 Worked example (BRL)

> The numbers below exist to show the *arithmetic* — the filter chain, the reconciliation ratio, the SOM share. Do not carry any of them into a live analysis, even if the idea looks similar; count your own segment.

Idea: agenda + cobrança automática para clínicas de fisioterapia, R$ 99/month.

- Bottom-up TAM: ~25,000 fisioterapia clinics/consultórios with active CNPJ (CNAE 8650-0/04 cross-checked with CREFITO registrations) `[data]` × R$ 99 × 12 = R$ 1,188/yr → **TAM ≈ 25,000 clinics, R$ 30M/yr**.
- SAM filters: ≥ 2 professionals and some digital scheduling today (40 %), not locked into a vertical ERP contract (80 %), reachable through Instagram/Google Ads plus CREFITO partnerships (70 %) → 25,000 × 0.40 × 0.80 × 0.70 ≈ **5,600 clinics, R$ 6.7M/yr** `[estimate]`.
- SOM year 3 at 3 % of SAM → **~170 clinics, ~R$ 200k/yr** `[estimate]`.
- Top-down check: a "software de gestão para saúde no Brasil" report at R$ 1.2B; physiotherapy ≈ 4 % of health establishments → R$ 48M. Ratio 48 ÷ 30 = 1.6×: consistent, bottom-up stands.

### 2.4 Reconciliation rule

When top-down and bottom-up differ by more than 3×, do not average them; find which is wrong and say why in the report.

- Top-down too big is the common case: the report's category is broader than yours (includes enterprise, hardware, services, all of LatAm) or is a vendor forecast.
- Bottom-up too small: you counted only customers who look like the first design partner, or priced without expansion/upsell, or used a single tier.
- Bottom-up too big: inactive CNPJs, MEIs without activity, or a US price applied to Brazil.

State the chosen figure, the discarded one, and the reason. Prefer bottom-up for SAM and SOM; use top-down only as the TAM ceiling.

### 2.5 Realistic SOM shares

| Horizon | Share of SAM | Mechanism that justifies it |
|---|---|---|
| Year 1 | 0.1–1 % | Founder-led sales, one channel, one segment |
| Year 2 | 0.5–3 % | A repeatable channel with a measured CAC |
| Year 3 | 1–5 % | Two channels, referrals, some brand |
| Above 10 % | Needs a named mechanism | Exclusive distribution deal, regulatory mandate, incumbent exit, viral loop with measured k > 0.5, or a SAM so small you can call everyone in it |

Second grounding: take the closest incumbent's public revenue ÷ customer count and ask how many years and how much capital it took them to reach your year-3 number. If they needed six years and R$ 20M, a three-year SOM of R$ 500k on R$ 200k of cash needs an explanation.

### 2.6 Confidence

Report each of TAM, SAM and SOM with a confidence: **high** (registry counts and a competitor-anchored price), **medium** (one side estimated), **low** (both estimated, or the category is new). A low-confidence SOM must be mirrored by a wider pessimistic scenario (§7) — it is dishonest to show a tight range on a number nobody counted.

## 3. Cost to run

`fixed_costs_monthly` is everything that does not scale with users; `cogs_per_user_monthly` is everything that does; `one_time_costs` is what is paid before month 1. Ranges below are BRL, 2025–2026, early stage.

### 3.1 Team

| Role (Brazil) | CLT gross R$/month | PJ R$/month | Notes |
|---|---|---|---|
| Dev júnior | 4,000–7,000 | 5,000–8,000 | |
| Dev pleno | 7,000–12,000 | 9,000–15,000 | |
| Dev sênior / tech lead | 12,000–20,000 | 15,000–30,000 | Seniors working remotely for US firms ask 25–40k |
| Product / UX designer | 6,000–14,000 | 7,000–16,000 | Freelance R$ 80–200/h |
| SDR / pré-vendas | 3,000–5,000 + variable | — | Variable 30–50 % of OTE |
| Closer / AE | 5,000–10,000 + variable | — | |
| CS / suporte | 2,500–5,000 | 3,000–6,000 | |
| Marketing generalist | 5,000–10,000 | 6,000–12,000 | |

Employer cost on top of CLT gross salary:

- Under Simples Nacional (no 20 % INSS patronal, no terceiros): FGTS 8 % + 13º + férias + 1/3 + termination provisions ≈ **1.35–1.5×**, plus benefits (VR/VA, plano de saúde, VT) R$ 800–2,000/month.
- Outside Simples (Lucro Presumido/Real): add INSS patronal 20 % + RAT 1–3 % + terceiros ~5.8 % → **1.7–2.0×** with benefits.
- PJ: the invoice is the cost; the contractor pays their own tax. Add 5–10 % if you supply equipment and tools. Treating a de-facto employee as PJ is a labor-law liability; price that risk if the long-term team is all-PJ.
- Founders: pay at least pró-labore at the minimum wage (R$ 1,518 in 2025, R$ 1,621 in 2026; 11 % INSS withheld). Book **opportunity cost** separately in the report — what each founder forgoes elsewhere (R$ 8–25k/month for a senior dev or PM). Leave it out of `fixed_costs_monthly` for the bootstrapped view, but the verdict must say how many months of forgone salary the plan consumes.

### 3.2 Infrastructure, tools, services

| Item | Lean (R$/month) | Growth (R$/month) | Notes |
|---|---|---|---|
| Cloud / hosting | 0–500 | 1,500–8,000 | Vercel / Supabase / Railway / Fly free tiers → AWS/GCP. Move per-user hosting into COGS once it exceeds ~R$ 1/user |
| LLM / API usage (AI products) | 100–1,000 | 5–30 % of revenue | Variable; belongs in `cogs_per_user_monthly`. The most common way an AI idea fails the margin test |
| SaaS stack | 300–1,000 | 2,000–6,000 | Google Workspace, GitHub, Figma, Notion, Slack, CRM (Pipedrive / RD Station / HubSpot), helpdesk, analytics, Sentry |
| Messaging | 0–300 | 500–5,000 | WhatsApp Business API R$ 0.05–0.40 per message/conversation by category; SMS R$ 0.08–0.15; transactional e-mail near zero |
| Contador | 300–600 (online, Simples) | 800–1,500 (Presumido, payroll) | Plus R$ 500–1,500 one-time to open the company |
| Legal / IP (one-time) | 2,000–8,000 | 10,000–30,000 | Contrato social, termos de uso and privacidade (LGPD), INPI trademark (fees ~R$ 150–750 + R$ 1–3k honorários), acordo de sócios with vesting |
| Coworking / office | 0–1,500 | 3,000–10,000 | |
| Support | founders | 1 CS per 150–400 SMB accounts | Variable share goes to COGS |
| Contingency | +15–25 % of fixed | | Costs are underestimated systematically; add it as a line, not as hope |

### 3.3 Payment processing (variable, goes into COGS)

| Rail | Typical fee | Notes |
|---|---|---|
| Cartão de crédito (Stripe BR, Pagar.me, Asaas, Mercado Pago; Vindi / Iugu for recurrence) | 2.5–5 % + R$ 0.30–0.50 | Stripe BR ≈ 3.99 % + R$ 0.39 domestic; international cards +1–2 %; split/marketplace features add fees |
| Parcelamento (installments) | +1.5–3 % per month anticipated | Consumers expect "12×"; the seller funds it |
| Pix | 0.5–1.5 % or R$ 0.50–2 flat | Cheapest rail, no chargeback, no native recurrence yet (Pix Automático rolling out) |
| Boleto | R$ 1.50–4 per boleto issued | 20–40 % go unpaid in consumer segments; settlement D+1 |
| Infoproduct platforms (Hotmart, Kiwify, Eduzz) | 8–10 % + R$ 2.49 per sale | Replaces checkout, affiliates and tax handling |
| App stores (Apple / Google) | 15–30 % | Applies to consumer apps billed in-app |
| Chargebacks, refunds, inadimplência | 1–5 % of revenue | Put into COGS or as a haircut on ARPU |

Rule: `cogs_per_user_monthly ≥ processing % × ARPU + fixed fee + hosting per user + API usage per user + variable support`. For a R$ 99 card subscription that is already ~R$ 4.30 before hosting.

### 3.4 Taxes on revenue (`tax_rate_on_revenue`)

| Regime | Effective rate on gross revenue | When it applies |
|---|---|---|
| MEI | ~R$ 80/month flat DAS | Cap R$ 81k/yr, one employee, most software and consulting CNAEs not allowed; fine for a side project, useless beyond |
| Simples Nacional, Anexo III | 6 % up to R$ 180k/yr; ~8.6 % at R$ 360k; ~11 % at R$ 720k; ~14 % at R$ 1.8M; ~17.5 % at R$ 3.6M (ceiling R$ 4.8M) | Services including software **when Fator R ≥ 28 %** (payroll + pró-labore + encargos ÷ gross revenue, trailing 12 months) |
| Simples Nacional, Anexo V | 15.5 % up to R$ 180k; ~16.8 % at R$ 360k; ~18 % at R$ 720k; ~19.5 % at R$ 1.8M | Software development and licensing when Fator R < 28 % — where a lean, automated SaaS lands |
| Lucro Presumido (services) | ≈ 11.3 % federal (IRPJ 4.8 % + CSLL 2.9 % + PIS/COFINS 3.65 %) + ISS 2–5 % municipal ≈ **13.3–16.3 %**; IRPJ surcharge of up to +3.2 % once presumed profit exceeds R$ 60k/quarter (~R$ 187k revenue/quarter) | Above the Simples ceiling, foreign shareholders, or activities barred from Simples |
| Lucro Real | ~34 % on profit + 9.25 % PIS/COFINS non-cumulative | Rarely relevant before R$ 10M+ revenue |

Practical rule: two founders on minimum pró-labore with automated delivery usually fail Fator R and pay **15.5 %**; a payroll-heavy or services-heavy company passes and pays **6–11 %**. Model the regime the cost structure implies and test the other one in the pessimistic scenario. The reform transition (CBS 0.9 % + IBS 0.1 % test rates in 2026, PIS/COFINS extinguished in 2027, ISS/ICMS phased out 2029–2033) changes Presumido and Real; Simples keeps its own regime but can opt into CBS/IBS to pass credits to B2B clients. Confirm with a contador before a rate goes into a verdict.

### 3.5 One-time costs (`one_time_costs`)

| Item | Range |
|---|---|
| MVP by the founders | R$ 0 cash; 3–6 months of opportunity cost |
| MVP by freelancer or no-code/low-code (Bubble, FlutterFlow, Lovable + Supabase) | R$ 10,000–40,000 |
| MVP by a Brazilian software house / agency | R$ 60,000–250,000 over 3–6 months |
| MVP by a US/EU agency | US$ 50,000–250,000 |
| Company setup, legal, IP | R$ 3,000–15,000 |
| Launch marketing, brand, site | R$ 5,000–30,000 |
| Equipment, licenses | R$ 5,000–20,000 |
| Contingency | +20 % |

### 3.6 Monthly fixed burn by configuration (BRL; excludes marketing budget and COGS)

| Configuration | Team | Fixed burn / month | Comment |
|---|---|---|---|
| Lean solo | 1 technical founder, PJ, no salary | R$ 1,500–5,000 | Tools, cloud, contador, domain; opportunity cost of R$ 10–25k/month is hidden |
| Small team | 2 founders on pró-labore mínimo + 1 dev PJ pleno + freelance design | R$ 18,000–40,000 | The default realistic case for a Brazilian pre-seed |
| Funded team | 5–8 people (2 devs, design, 1–2 sales, CS), coworking, full tooling | R$ 80,000–200,000 | R$ 1–2.4M/yr: a seed round |

### 3.6b Brazilian founder selling abroad in USD

A common shape, and the Brazilian tables above mostly do not apply to the revenue side. Model these explicitly:

| Item | What to assume | Why it matters |
|---|---|---|
| Merchant of record (Paddle, Lemon Squeezy, Polar) vs. a plain gateway (Stripe) | MoR ≈ 5 % + fixed per transaction; Stripe 2.9 % + US$ 0.30 (+1 % currency conversion, +1.5 % international cards) | An MoR handles global sales tax/VAT for you, which is worth real money for a solo founder — but on a **low ticket the fixed fee dominates**: US$ 0.50 on an US$ 8 charge is 6.25 %, and combined with the percentage the effective take can pass 11 %. Always express the fee as a % of *your* price, not as the headline rate. |
| Free tier | Cost per free user × free-to-paid ratio | On AI products the free tier is a real COGS line: 10 free users per payer at US$ 0.10 each is US$ 1.00 of COGS on every paying customer. Put it in `cogs_per_user_monthly`, not in a footnote. |
| Receiving USD in Brazil | Wise/Husky/Nomad or a PJ invoice; spread + IOF on FX (rates change — verify) | The rate you model is not the rate you receive. |
| Tax on exported services | Simples Nacional still applies to the revenue; PIS/COFINS and ISS generally do not apply to exported services, subject to conditions | Effective tax can be materially below the domestic case — confirm with a contador before it drives the verdict. |
| Building the product in BRL, earning in USD | Costs in the §3.1–3.6 tables, revenue in USD | This is the structural advantage of the shape and should be stated: a US price with a Brazilian cost base. FX moves both ways; put an adverse rate in the pessimistic scenario. |

Set `currency` to `USD` and keep every cost in USD for consistency; note the FX rate and date used to convert the Brazilian cost base.

### 3.7 International variant (US entity)

Delaware LLC or C-corp via Stripe Atlas / Firstbase / Clerky (~US$ 500 one-time) + registered agent US$ 100–300/yr + Delaware franchise tax (US$ 300 LLC; US$ 225–450+ C-corp plus annual report) + US accountant and filings US$ 1,500–5,000/yr (a C-corp with foreign owners files Form 5472 and tends to the top) + Mercury/Brex banking (free) + Stripe 2.9 % + US$ 0.30 (+1.5 % international cards, +1 % currency conversion) + SaaS sales tax in 20+ states once nexus is reached. Team in USD: LatAm remote contractor dev US$ 6,000–15,000/month; US-based US$ 12,000–25,000. Small-team fixed burn US$ 8,000–30,000/month. A Brazilian founder invoicing the US entity from a Brazilian PJ pays Brazilian tax on exported services (Simples; PIS/COFINS/ISS export exemptions may apply). US prices run 2–3× the Brazilian list (§4.3) — which is the reason to go international at all.

## 4. Pricing and ARPU

### 4.1 Three ways to land a price

1. **Value-based.** Quantify what the customer gains: hours saved × hourly cost, revenue recovered, no-shows avoided, fines avoided. Charge 10–30 % of it for B2B. For consumers, anchor on what they already pay for the adjacent habit (academia, streaming, delivery, a course).
2. **Competitor-anchored.** List every alternative with its public price, including "a spreadsheet" at R$ 0 and "hire someone" at a salary. Place yourself relative to the closest substitute and say why (more value, narrower niche, cheaper to serve).
3. **Cost-plus, as a floor only.** `price ≥ (cogs_per_user + cac × churn) ÷ 0.6` keeps gross margin at or above 60 % while covering replacement of churned users. If the floor sits above competitors, the business does not exist at this cost structure — that is a finding, not a pricing problem.

The right price passes all three: above the cost floor, defensible beside competitors, clearly below the value delivered.

### 4.2 Structure

- **Tiers.** Two to four plans; the middle one is the anchor and should hold 50–70 % of buyers. Gate on a value metric that grows with the customer's success (seats, units, messages, transactions), not on crippled features.
- **Thresholds.** R$ 49 / 97 / 197 / 497 in Brazil; US$ 9 / 29 / 99 / 499 in the US.
- **Freemium vs trial.** A 7–14 day trial converts 10–25 % and suits products whose value shows within days; freemium converts 2–5 % and pays off only when free users are cheap to serve and bring others (virality, network effects, content). Freemium is risky for Brazilian SMB tools: the free tier becomes the product for a price-sensitive segment.
- **Annual prepay.** 15–25 % discount. In Brazil the usual substitute is "12× no cartão": no discount, but the seller absorbs 1.5–3 %/month of anticipation. Annual plans improve cash and cut churn; monthly-equivalent ARPU falls by the discount.
- **Marketplace take rates.** Payments 1–3 %; B2B supplies 3–10 %; goods 8–20 % (Mercado Livre ~11–19 %); services and freelance 10–25 %; food delivery 12–27 %; infoproducts 8–10 % + fixed; real-estate and job leads flat per lead. A take rate above the category norm needs a reason (you carry risk, logistics or payments).
- **Transactional / usage.** Price per event (message, document, query, GB) with a minimum monthly commitment; ARPU = events per customer per month × unit price.

### 4.3 Brazil vs US willingness to pay

- Brazilian SaaS list prices run 30–60 % of the US list for the same category; SMB buyers compare against a salary, not against US tools.
- Brazil ARPU ranges: micro/solo R$ 29–99; SMB R$ 99–499; mid-market R$ 500–3,000; enterprise R$ 5,000+/month. B2C subscriptions R$ 9.90–49.90; prosumer R$ 29–99.
- US ranges: consumer US$ 5–15; prosumer US$ 10–30; SMB US$ 50–500; mid-market US$ 500–5,000; enterprise US$ 5,000+/month.
- Charging Brazilians in USD adds IOF (~3.4–3.5 % on international card spend; the rate keeps changing), FX anxiety and lower conversion. Charge in BRL locally, USD abroad.
- Brazilian SMBs churn on price faster and pay late more often; put inadimplência into ARPU or COGS, never into hope.

### 4.4 Landing on `arpu_monthly`

```
arpu_monthly = Σ (tier_share × tier_price_monthly_equivalent) × (1 − avg_discount) × (1 − payment_failure_rate)
```

Annual plans enter at annual price ÷ 12. Model-specific mappings of "one user = one active paying customer":

- **Marketplace:** set `gmv_per_user_monthly` and `take_rate` in `base` instead of `arpu_monthly` — the script derives ARPU and, crucially, puts the **take rate into the sensitivity table**, which is the one lever a marketplace founder actually controls. Add `payment_fee_pct_of_gmv` and the script charges it on gross volume; keep `cogs_per_user_monthly` for the non-payment costs. The "user" is the side you bill and acquire (seller for B2B, buyer for consumer); the other side's acquisition goes into `fixed_costs_monthly` (a supply team) or is blended into `cac`.

  **The fee-on-GMV trap — check this before anything else in a marketplace.** Costs that scale with gross volume are `1 ÷ take_rate` times worse than they look against the revenue you keep. At a 15 % take, a 1 % payment fee on GMV eats **6.7 %** of your revenue; at a 5 % take it eats 20 %. Run the arithmetic explicitly:

  ```
  take 15%, GMV R$ 88/user/month  → revenue R$ 13.20
  payment fee 1% of GMV           → R$ 0.88 = 6.7% of revenue
  refunds/chargebacks 2% of GMV   → R$ 1.76 = 13.3% of revenue
  ```

  Low-take, low-ticket marketplaces frequently die here and nowhere else: 15 % of a R$ 22 seat is R$ 3.30, and R$ 3.30 has to fund payments, trust-and-safety, support and refunds before it funds the product. Also check the **price the take rate adds to the end user** — if it pushes your product above the substitute (the bus, the free WhatsApp group), the fee destroys the value proposition *and* fails to fund the business, which is a KILL, not a pricing tweak.

  **What the script cannot model:** the two-sided cold start. There is no supply side, no fill rate and no liquidity in the schema — `organic_new_users_monthly` silently assumes supply is always there. State that limitation in the dossier, cap `sam_users` at what the supply side can actually serve, and treat liquidity per corridor/city/category as a risk in `07-risks-and-verdict.md`, not as a number in the model.
- **Transactional / usage:** `events per month × unit price`; churn = customers who stop transacting.
- **Ads:** user = monthly active user; `arpu_monthly = sessions per MAU × impressions per session × eCPM ÷ 1000` (BR display eCPM R$ 1–10; video/rewarded R$ 10–40); churn = MAU decay; CAC = cost per install ÷ activation rate.
- **Services / agency:** user = active client on retainer; COGS = delivery labor per client (50–70 % of the retainer).
- **One-time purchase or infoproduct:** `arpu_monthly = price` and `monthly_churn = 1.0` — every buyer leaves after one month, LTV collapses to a single purchase, and the model shows honestly why one-off products need a very low CAC or a back-end subscription.

Do not use the top tier as ARPU; do not net out taxes (the script applies `tax_rate_on_revenue`); do not net out processing fees (they belong in COGS). Write the anchors in `notes.arpu_monthly`: competitor names and prices, tier mix assumed.

## 5. Unit economics

Per active paying user per month, matching the script:

```
contribution    = arpu_monthly × (1 − tax_rate_on_revenue) − cogs_per_user_monthly
gross_margin    = contribution ÷ arpu_monthly
lifetime_months = 1 ÷ monthly_churn, capped at `ltv_cap_months` (script default 60; set 36 in `base` for SMB/consumer, 60 for enterprise)
LTV             = contribution × lifetime_months
LTV/CAC         = LTV ÷ cac
payback_months  = cac ÷ contribution
```

Cap the lifetime because 1 ÷ churn at 1 % claims 100 months for a company that is zero months old: no cohort has been observed that long, products get replaced, and cash now is worth more than cash in year eight.

The script treats `organic_new_users_monthly` as free, so the blended CAC it implies is `marketing_budget ÷ (organic + marketing_budget ÷ cac)`. Report paid CAC and blended CAC side by side; blended flatters the model exactly as long as organic holds up, which is the uncertain part.

### 5.1 Benchmarks (ranges to validate, not targets)

| Metric | Healthy | Watch | Broken |
|---|---|---|---|
| Gross margin, SaaS | 70–85 % | 50–70 % | < 50 % (AI-heavy products often live here) |
| Gross margin, marketplace (on net revenue) | 60–70 % | 40–60 % | < 40 % |
| Gross margin, services / agency | 30–50 % | 20–30 % | < 20 % |
| LTV/CAC | ≥ 3 | 2–3 | < 2 (< 1 loses money on every customer) |
| CAC payback, B2B | ≤ 12 months | 12–18 | > 18 |
| CAC payback, SMB / consumer | ≤ 6 months | 6–12 | > 12 |
| Monthly churn, consumer subscriptions | 5–10 % | 10–12 % | > 12 % |
| Monthly churn, SMB SaaS | 3–7 % (Brazil leans to the top) | 7–8 % | > 8 % |
| Monthly churn, mid-market | 1–2 % | 2–3 % | > 3 % |
| Monthly churn, enterprise | < 1 % | 1–1.5 % | > 1.5 % |
| Monthly churn, marketplace active buyers | 10–20 % | | |

### 5.2 Conversion funnel benchmarks

| Step | Range |
|---|---|
| Landing page visit → signup / lead | 2–5 % (cold paid traffic 1–3 %; warm or referral 5–10 %) |
| Trial → paid | 10–25 % (card-upfront trials 40–60 %, with far fewer trials) |
| Freemium → paid | 2–5 % |
| Lead → demo (B2B) | 10–20 % |
| Demo → close (SMB B2B) | 20–40 %; sales cycle 15–60 days |
| Outbound cold e-mail reply | 1–5 %; LinkedIn / WhatsApp reply 5–15 %; 1–3 meetings per 100 contacts |
| Waitlist → paying at launch | 5–15 % |

### 5.3 CAC by channel (fully loaded: media + tools + people time ÷ paying customers)

| Channel | Brazil | US | Notes |
|---|---|---|---|
| Paid search | CPC R$ 1–8; SMB SaaS CAC R$ 300–1,500 | CPC US$ 2–15; CAC US$ 400–2,000 | Intent-driven; test first |
| Paid social (Meta, TikTok) | CPM R$ 10–40; consumer CPI R$ 2–10; consumer CAC R$ 30–150; SMB CAC R$ 400–2,000 | CPM US$ 8–20; consumer CAC US$ 20–100; SMB CAC US$ 500–3,000 | Degrades as spend scales |
| Content / SEO | R$ 50–500 per customer after a 6–12 month lag | US$ 100–800 | Looks free, costs a writer |
| Outbound (SDR) | R$ 1,000–4,000 per SMB deal; R$ 5,000–20,000 mid-market | US$ 3,000–15,000 | One SDR closes 8–20 deals/month at best |
| Partnerships / channels | 10–30 % revenue share, or 0.5–1× ARPU per referral | same | Slow to start, cheap at scale |
| Referrals / word of mouth | R$ 0–100 | US$ 0–50 | Modeled as organic; counts only once measured |
| Events / communities | R$ 200–2,000 | US$ 500–5,000 | |

The realistic `cac` is the weighted average of the channels the founders will actually run in year 1 (typically one paid channel plus founder outbound). A base-case CAC under R$ 150 for B2B or under R$ 20 for consumer needs a measured funnel behind it.

## 6. Break-even, peak cash and runway

Let `c` = contribution per user per month, `F` = `fixed_costs_monthly`, `M` = `marketing_budget_monthly`, `CAC` = `cac`, `churn` = `monthly_churn`, and `n` = new users per month = `organic + M ÷ CAC`.

| Quantity | Formula | Meaning |
|---|---|---|
| Break-even users, static | `N_static = F ÷ c` | Users needed if acquisition were free; the floor |
| Break-even users, at planned spend | `N_plan = (F + M) ÷ c` | What the script's monthly profit line actually needs |
| Break-even users, sustainable | `N_sust = F ÷ (c − CAC × churn)` | Counts only the spend that replaces churned users; a denominator ≤ 0 means LTV < CAC and no scale ever closes the model |
| Steady-state ceiling | `N_max = n ÷ churn` | Where the user count plateaus with the planned acquisition; if `N_max < N_plan`, the budgeted engine never reaches break-even |
| Months after launch to reach N | `t = ln(1 − N ÷ N_max) ÷ ln(1 − churn)` | Closed form for constant `n` and churn; the script gives the exact month |
| Peak cash need | Largest negative value of cumulative cash, including `one_time_costs` | The number to raise or to have in the bank |
| Runway | cash on hand ÷ average net burn until break-even | Months before the idea dies without more money |

Worked on the schema's base case: `c = 99 × 0.94 − 8 = 85.06`; `N_static = 18,000 ÷ 85.06 ≈ 212`; `N_plan = 24,000 ÷ 85.06 ≈ 283`; `N_sust = 18,000 ÷ (85.06 − 250 × 0.05) ≈ 249`; `n = 15 + 6,000 ÷ 250 = 39`; `N_max = 39 ÷ 0.05 = 780`, comfortably above 283. Months after launch to reach 283: `ln(1 − 283 ÷ 780) ÷ ln(0.95) ≈ 9`, so break-even near month 12 with launch at month 3. Cash: three pre-launch months at R$ 24k plus R$ 40k one-time = R$ 112k, plus roughly R$ 85k of post-launch losses → peak need ≈ R$ 200k; with a 25 % buffer, R$ 250k to attempt the realistic case. The script's table is authoritative; use this arithmetic to check it.

### 6.1 Sanity checks before trusting a break-even

- `N_plan ÷ sam_users` must sit well below `som_share_year3`. If break-even needs more users than the year-3 SOM, the model does not close: the price, the cost base or the market definition is wrong, and the verdict says so.
- `N_plan` above ~30 % of SOM users means viability only at the edge of plausible share — fragile.
- `N_max < N_plan`: the acquisition engine as budgeted cannot reach break-even. Raise `M`, lower CAC or cut churn, and say which change is believable.
- Break-even later than month 24 in the realistic case means the founders need funding or a day job; state which.
- Peak cash need beyond what the founders can assemble is a financing finding, not a model detail. Brazilian reference points: own savings and friends/family R$ 50–300k; anjos R$ 100k–1M; pré-seed R$ 500k–3M; seed R$ 2–10M.
- Users at the end of the horizon versus SOM: far above SOM means the acquisition assumptions outrun the market; far below means SOM is decorative and the real constraint is the engine.

## 7. Three scenarios

Scenarios are alternative assumption sets, each with a story about the world, not base × (1 ± 30 %). The realistic case is the anchor, defended line by line with benchmarks and sources. Pessimistic asks "what if the ordinary startup failures happen together"; optimistic asks "what if the thesis is right and one channel really works". Never derive the realistic case as the average of the other two — that makes the anchor depend on two stories instead of on evidence.

| Lever | Pessimistic default | Optimistic default | What would have to be true |
|---|---|---|---|
| `monthly_churn` | × 1.5 | × 0.7 | Pess: nice-to-have, cut in the first slow month. Opt: beta retention ≥ 90 % at 3 months, measured |
| `cac` | × 1.5–2 | × 0.7 | Pess: paid channel saturates, competitors bid on your keywords. Opt: one channel with proven CAC plus a referral loop |
| `arpu_monthly` | × 0.8 | × 1.15 | Pess: discounts to close, bottom tier dominates. Opt: mid tier holds, annual plans, upsell |
| `organic_new_users_monthly` | × 0.5 | × 2 | Pess: no word of mouth. Opt: content or community compounds; partners deliver |
| `launch_month` | + 3 months | same | Pess: the MVP slips, as it always does |
| `fixed_costs_monthly` | × 1.2 | same | Pess: an extra hire, tooling creep, a legal surprise |
| `tax_rate_on_revenue` | Anexo V or Presumido (0.155 / 0.15) | Anexo III via Fator R (0.06–0.11) | Depends on payroll share; a lean automated SaaS carries the higher rate already in the realistic case |
| `one_time_costs` | × 1.3 | same | Pess: a rebuild, compliance work, agency overrun |
| `cogs_per_user_monthly` | × 1.3 for AI/API-heavy products | × 0.8 | Pess: usage per user higher than planned |

Rules:

- Pessimistic stays plausible: the P10–P20 world, not the apocalypse. If the idea survives it with a path to profit, that is the strongest sentence in the verdict.
- Optimistic is the P80–P90 world with an explicit mechanism; no "viral" without a measured k-factor or a named distribution partner.
- Each scenario ends with one sentence: *"For this to happen, [mechanism] must be true; we will know by [signal] within [months]."*
- When an input is `[guess]`, widen the pessimistic side for that lever (churn × 2 instead of × 1.5, for example) rather than narrowing the optimistic one. Uncertainty is asymmetric for a business that does not exist yet.

## 8. Filling `model.json` step by step

The script reads one file. `base` is the realistic case. `scenarios.pessimistic` and `scenarios.optimistic` are override dictionaries applied on top of `base`, so list only the keys that change. `marketing_budget_monthly` accepts a number or an array with one value per month — use the array to ramp spend or to start marketing at launch instead of month 0. `launch_month` is the first month with paying users; before it only costs accrue. `one_time_costs` hits cash at month 0. `notes` is free-form, one entry per input, stating the source or benchmark and its label.

```json
{
  "idea": "slug-da-ideia",
  "currency": "BRL",
  "horizon_months": 36,
  "one_time_costs": 40000,
  "base": {
    "arpu_monthly": 99,
    "cogs_per_user_monthly": 8,
    "fixed_costs_monthly": 18000,
    "cac": 250,
    "marketing_budget_monthly": 6000,
    "organic_new_users_monthly": 15,
    "monthly_churn": 0.05,
    "launch_month": 3,
    "tax_rate_on_revenue": 0.06,
    "tam_users": 500000,
    "sam_users": 80000,
    "som_share_year3": 0.03
  },
  "scenarios": {
    "pessimistic": { "monthly_churn": 0.08, "cac": 400, "arpu_monthly": 79, "organic_new_users_monthly": 5, "launch_month": 6, "fixed_costs_monthly": 22000 },
    "optimistic":  { "monthly_churn": 0.035, "cac": 180, "arpu_monthly": 119, "organic_new_users_monthly": 40 }
  },
  "notes": { "arpu_monthly": "anchored on competitor X plan at R$89 and Y at R$129", "monthly_churn": "SMB SaaS benchmark 3–7%/mo" }
}
```

1. **`idea`, `currency`, `horizon_months`.** The dossier slug; `BRL` unless the product sells abroad; 36 months by default, 24 for consumer products with fast feedback, 48–60 for enterprise sales cycles.

**Optional fields beyond the core schema** — all valid in `base` and in a scenario override:

| Field | Effect |
|---|---|
| `founder_income_target_monthly` + `founders` | Computes the month each founder actually earns that much (sustained three months, not touched once) and prints it as the **first row** of the summary — the row `report-template.md` requires. Set it to whatever the founder said their goal was. |
| `ltv_cap_months` | Caps the lifetime used for LTV (default 60). Use 36 for SMB/consumer. |
| `gmv_per_user_monthly` + `take_rate` | Marketplace mode: derives ARPU and makes the take rate a sensitivity lever. Replaces `arpu_monthly`. |
| `payment_fee_pct_of_gmv` | Marketplace mode: charges the fee on gross volume, added on top of `cogs_per_user_monthly`. See §4.4. |
| `one_time_costs` | Valid inside a scenario, not only at the top level — a pessimistic case usually should carry a higher one. |
2. **Choose the unit and map the model** (§4.4). "User" means one active paying customer. Decide which side you bill, what one month of that customer is worth, and what it costs to serve them.
3. **`arpu_monthly`** from §4.4, blended across tiers, net of discounts and payment failures, gross of tax and processing. Note the competitor anchors and the tier mix.
4. **`cogs_per_user_monthly`** from §3.3 plus hosting, API and support per user. For AI products, estimate tokens per active user per month × price and write the assumption down.
5. **`fixed_costs_monthly`** from §3.1–3.2 and the §3.6 configuration. List the line items in the note, including contador, tools, cloud floor, pró-labore and contingency.
6. **`cac`** from §5.3, weighted by the year-1 channel mix, fully loaded with people time.
7. **`marketing_budget_monthly`**: what the founders will actually spend; an array if it ramps. `M ÷ cac` is the paid acquisition rate — check it against sales capacity (one founder closes 5–15 SMB deals a month at most; the array should not imply more).
8. **`organic_new_users_monthly`** from founder network, waitlist, SEO and referrals. Start small — B2B 3–15, consumer 20–200 — unless an audience already exists and can be counted.
9. **`monthly_churn`** from §5.1 by segment; Brazilian SMB realistic is 5–7 %.
10. **`launch_month`**: months until the first invoice, not until the MVP "is ready". Add 1–2 months to whatever the founder says.
11. **`tax_rate_on_revenue`** from §3.4; the regime the cost structure implies, with the Fator R assumption noted. The schema example's 0.06 is only right if payroll clears 28 % of revenue.
12. **`tam_users`, `sam_users`, `som_share_year3`** from §2, as counts of customers, with the filter chain in the note.
13. **`scenarios`** from §7: only the keys that change, and the story for each in `notes`.
14. **`notes`**: one line per input, for example `"cac": "[benchmark] Google Ads BR SMB SaaS R$ 300–1,500; founder outbound ~R$ 400/deal in time; weighted 250"`.

When data is missing: build a bottom-up estimate from whatever can be counted (maps, registries, app-store reviews, competitor follower counts, job postings), label it `[guess]`, widen the pessimistic override for that input, and put it at the top of the report's assumptions-to-validate list. Never leave an input blank and never paste a US benchmark unconverted: convert prices by the 30–60 % rule and costs by the Brazilian ranges above.

Sanity pass before running the script: gross margin ≥ 50 % or an explanation; LTV/CAC ≥ 3 in base; payback within the segment benchmark; `N_plan < SOM users`; `N_max > N_plan`; the pessimistic tax regime considered.

## 9. Reading the script output into the report

The script prints: a market block (TAM/SAM/SOM in customers and annual revenue), a scenario summary (users and MRR at months 12/24/36, ARR at the end, first profitable month, cash-positive month, peak cash need, cumulative cash), unit economics (contribution, gross margin, lifetime, LTV, LTV/CAC, payback), a break-even block (`N_static` as "simple", `N_plan` as "at planned spend", `N_sust` as "sustainable", `N_max` as "steady-state ceiling", and the sustainable break-even as % of SAM and of SOM), a projection table per scenario at months 3/6/12/18/24/30/36, a ±20 % sensitivity table on each lever, the assumptions table with your `notes`, and warnings. Map them into the dossier (`05-financial-model.md` and the README) as follows.

**"The numbers" (pessimistic / realistic / optimistic).** One table, three columns: users at months 12/24/36; MRR at 12/24/36; first profitable month (or "not within N months"); peak cash need; LTV/CAC; payback; cumulative cash at the end of the horizon. Below it, the one-sentence "what has to be true" for each scenario (§7). If the pessimistic case never breaks even, state how much cash it burns over the horizon and what the kill signal is (for example: fewer than X paying customers by month Y).

**"Cost to run."** The fixed-cost table with line items for the chosen configuration (§3.6), the one-time costs, the variable cost per user with its composition, the tax regime assumed, and the founders' opportunity cost as a separate line totaled over the months to break-even. Give the pre-launch monthly burn and the average net burn until break-even.

**"Users to break even."** `N_plan` (users to cover fixed costs plus the planned marketing), `N_sust` (users at which the business sustains itself including churn replacement), `N_max` (the ceiling the budget can reach), months to get there, and the ratio to SAM and SOM with the §6.1 verdict. Express it three ways: customers, MRR at that point, and cash consumed to get there.

**Verdict inputs.** The critical verdict quotes gross margin, LTV/CAC, payback, realistic break-even month, peak cash need (realistic and pessimistic), `N_plan ÷ SOM users`, and the two or three inputs the outcome is most sensitive to — almost always price, churn and CAC.

Honest caveats to include every time:

- Benchmarks are ranges from comparable businesses, not measurements of this one; the first 90 days of real funnel data outrank everything in this file.
- Brazilian tax, fee and salary figures are 2025–2026 values subject to change; the regime and Fator R need a contador's confirmation.
- The model is linear: constant new users per month, constant churn, no seasonality, no expansion revenue, no price increases. Real cohorts churn more in months 1–3 and less later; real marketing has diminishing returns; real revenue arrives late (boleto, 30-day B2B terms), so cash is worse than the table shows.
- Organic growth is an assumption until measured; if the pessimistic case does not already do it, show a run with `organic_new_users_monthly = 0`.
- TAM and SAM are ceilings, not forecasts; the SOM share is a judgment.
- A model that closes is a necessary condition, not proof. A model that does not close at any plausible setting is close to a disproof — and that is a useful result.
