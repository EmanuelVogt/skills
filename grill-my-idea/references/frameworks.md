# Evaluation & Judgment Frameworks

Read this when moving from research to verdict. It is the rubric that keeps the verdict honest and repeatable: the same idea, scored twice, should land on the same answer. Default posture is skeptical — the burden of proof is on the idea, not on the critic. Attack the idea, never the person.

**Contents**
1. Idea-quality lenses
2. Venture-scale vs. indie business — which game is this?
3. Red flags / green flags by severity
4. Porter's Five Forces — compact scoring
5. Competitive positioning
6. Business-model archetypes
7. Risk taxonomy + pre-mortem protocol
8. Assumption mapping
9. Scorecard → verdict (weights, thresholds, overrides, worked example)

---

## 1. Idea-quality lenses

Run every lens. Each one catches a different way that a plausible-sounding idea dies.

### 1.1 Hair-on-fire vs. vitamin

The single most predictive question: how bad is the status quo *for the person who pays*?

| Signal | Vitamin (nice-to-have) | Painkiller | Hair-on-fire |
|---|---|---|---|
| Status-quo pain, 1–10 as rated by the buyer | ≤4 | 5–7 | 8–10 |
| Current behavior | Nothing; occasional complaint | Workarounds (spreadsheets, WhatsApp groups, an intern) | Already paying for an inferior solution or hiring people to do it |
| Frequency × intensity | Rare or mild | Weekly, annoying | Daily / blocks revenue / legal exposure |
| Budget | None exists; must be created | Exists but contested | Exists and is being spent badly |
| Buyer's questions | "Interesting, send me a deck" | "What does it integrate with?" | "How much, when can we start?" |

Rules that follow from this:
- Apply the **Delta-4 test**: ask what the buyer would rate the current solution (1–10) and what they would rate yours. You need a delta of at least 4 before anyone changes behavior. If incumbents already score 6+, replacing them is a war of attrition (Excel, WhatsApp and iFood all score 7+ for their core job — do not attack them head-on).
- Apply **LUV**: is the problem Large (enough people and spend), Urgent (they will switch), Valuable (they will pay)? Problem size beats market size — a small urgent problem with budget beats a huge vague one.
- "People already paying for inferior solutions" is the strongest pre-launch signal there is. Paying for a worse thing proves budget, urgency and a purchase process all exist. Conversely, **no existing workaround means no felt problem** — if nobody is hacking a fix together today, the pain is below the action threshold.
- Treat *politeness as noise*. "Cool idea" from friends, likes on a post, or investors being enthusiastic are not demand. Demand is urgent questions, time given freely, and money.

### 1.2 Why-now / inflection

Ask "what changed?" because every good idea has been tried before; most attempts sailed off and never came back. A why-now explains why *this* ship floats. Six sources of inflection:

1. New technology becoming good/cheap enough (LLMs, WebGL, batteries)
2. Adoption inflection of an existing technology (Pix reaching ~80% of Brazilian adults; WhatsApp Business API; smartphones in class C/D)
3. Regulatory change (Open Finance, LGPD, telemedicine regulation post-2022, marco legal das startups, new ANVISA or CVM rules, tax reform)
4. A long-held belief changing (remote work, paying for subscriptions, trusting digital banks)
5. A new distribution channel opening (a platform's app store, WhatsApp catalogs, TikTok Shop)
6. Cost collapse or price-point jump (cloud, AI inference, drones)

Grade the why-now on strength:
- **Level 1 — impossible before**: the product could not have existed without the change (Uber needed GPS phones). Strongest.
- **Level 2 — trend-riding**: could have existed, but the current makes it far easier. Still valuable. Think of markets as currents, not lakes: the stronger the current, the higher the odds. Recent shifts are stronger currents than decade-old trends ("SaaS" is no longer a why-now).
- **Level 0 — none**: possible. Big businesses have been built without one, but the founder must compensate with extraordinary execution, and the verdict should say so.

Self-check: could this company have literally existed five years ago? If yes and it didn't win, what stopped it — and is that reason gone?

### 1.3 Tarpit-idea catalog

A tarpit is an idea that (a) many people independently have, (b) looks like an unsolved problem, (c) gets warm feedback from everyone, and (d) has a graveyard of failed attempts going back to the late 1990s. The warm feedback is the trap — people like the *idea* and never use the *product*. Match the idea against this list before anything else; a match does not auto-kill, but it demands a specific, evidenced answer to "what is different this time?".

| Tarpit | Why it keeps failing |
|---|---|
| Social app for X (neighbors, students, parents, hobbyists) | Value only exists at density; cold-start kills it before density; incumbents (WhatsApp groups, Instagram, Facebook Groups) already host the graph for free |
| "Where are my friends going tonight" / event discovery | Low-frequency use, no retention loop, supply (events) decays daily, ad model never pays CAC |
| Travel planning / itinerary builder | Used twice a year; Google, Booking and TripAdvisor own the funnel; monetization is affiliate crumbs |
| Restaurant / local-business discovery & reviews | Google Maps is free and ubiquitous; restaurants won't pay; reviews have no moat |
| Recipe / meal-planning / fitness / habit / to-do app | Zero switching cost, infinite free substitutes, relies on the user changing a habit with no external pull |
| "Uber for X" without density or urgency | Uber works because trips are frequent, urgent and geographically dense. Dog walking, laundry and car washing are none of those; each city is a separate cold start |
| Two-sided marketplace with no supply strategy | Chicken-and-egg with zero liquidity; both sides churn before matching; disintermediation once they meet (the electrician gives the client his WhatsApp) |
| Consumer app that needs a new habit with no pull | Without an existing desire, every session is a marketing expense; D30 retention collapses |
| Products where the "customer" is the person who won't pay | Students, patients, gig workers, NGOs, small farmers: the user has the pain, someone else has the budget, and that someone has no urgency |
| "Netflix / Spotify for X" subscriptions for niche content | Content cost scales with catalog, audience doesn't; niche willingness to pay is ~R$10–20/mo |
| Generic AI chatbot / "ChatGPT wrapper" for a vertical | No proprietary data or workflow; the model vendor ships the feature next quarter; price goes to zero |
| Crypto/Web3 consumer apps, loyalty/coupon apps, price comparison | Incentives attract mercenary users; merchants don't value them; no retention once incentive stops |
| Email client / note-taking / calendar / personal finance tracker | Crowded, free defaults (Google, Apple, bank apps); users tolerate the default; enormous Delta-4 needed |
| Platform for freelancers / "LinkedIn for X" | Supply is abundant and flighty, demand is sporadic, the platform cannot prevent off-platform deals |
| Hyperlocal delivery / dark stores / "iFood for X" | Unit economics per delivery are negative without extreme density; the incumbent already has the couriers and can add your category in a week |

Brazilian twist: many of these were re-run locally 2015–2023 with "aplicativo de ..." in the name and a Meta-ads-only GTM. Check Reclame Aqui, Crunchbase/Distrito and app-store graveyards for the local attempts before accepting "nobody does this here".

### 1.4 Schlep blindness

The mind filters out ideas that involve tedious, scary work — regulation, fraud, banks, logistics, unions, hospitals — so the best ideas often look unattractive at first glance, and have less competition precisely because everyone else flinched. Payments looked unpleasant for a decade before anyone built Stripe. Flip this into a question: **is the idea hard in a way that protects it, or easy in a way that invites everyone?** An idea that a two-person team can clone in a weekend with no schlep has no moat by construction. An idea whose schlep the founder can actually absorb (licences, integrations, field ops, a sales team) is worth a premium.

### 1.5 Founder–market fit and the earned secret

Ask what the founder knows that the average smart person does not. Sources of an earned secret: having lived the pain at a previous job, having sold into this buyer, having built this internal tool twice, having operated in the industry's underbelly. Fit also means the founder can execute the specific schlep this idea requires and can spend years on it (the decade test: can they imagine ten years on this? They won't do ten, but if they can't imagine it they don't care enough). Score fit low when the founder is building for a community they don't belong to and haven't spent time inside — that is usually where made-up problems come from.

### 1.6 Unfair advantage and moats

A moat is what stops a well-funded copycat in 18 months. Ask which of these the idea *will plausibly earn*, not which it claims:

| Moat | What it looks like when real | Common fake version |
|---|---|---|
| Network effects | Each new user makes the product better for existing ones (liquidity, data, content) | "The more users we have, the more users we'll get" (that's virality, not a moat) |
| Switching costs | Data, integrations, workflows, trained staff, contracts | "Our UX is so good they won't leave" |
| Proprietary data | Data others can't buy, generated by the product's own use, compounding in value | Scraped public data, or data the customer owns and can export |
| Brand | Customers pay a premium or default to you without comparing | A nice logo and a domain |
| Distribution | Exclusive channel, partnership, community, audience the founder already owns | "We'll do content marketing and SEO" |
| Regulatory | Licences, certifications, approvals that take years (Banco Central authorization, ANVISA, CFM) | "Compliance is a feature" |
| Cost structure / scale | Structurally lower unit cost (vertical integration, tech replacing labor) | Being cheaper by under-pricing |

Apply the **60% gross-margin stress test**: ask why the idea cannot start at 60% gross margin. The answer usually reveals the true competitive alternative (an offshore agency at 20%, an incumbent bundling it free). If the margin cannot be defended now or in two years, expect compression.

### 1.7 Polarizing-signal test

Disruptive products split people: some love them, some call them a toy, stupid, or "I don't get it". A bell curve of mild approval ("nice", "makes sense") is the signature of an incremental product. When early users are lukewarm across the board, the idea is probably a feature, not a company. Haters are fine as long as the lovers don't run out — measure intensity of the lovers (would they be *very* disappointed if it disappeared? ≥40% is the classic bar), not the count of the indifferent.

---

## 2. Venture-scale vs. indie business — which game is this?

Both games are legitimate. Most ideas are not venture-scale, and that is not a failure — it is a different set of rules. The verdict must declare which game the idea is playing, because "good" is different in each, and the commonest mistake is applying venture expectations (and venture burn) to an indie-sized opportunity.

**Quick classification test** (answer honestly; three "yes" means venture game, otherwise indie):
1. Does the math reach R$100M+/year (or US$100M globally) in ~10 years? Write the equation: customers × price. If the TAM is under a few billion reais, the answer is no.
2. Is status-quo pain ≥8/10 for a large, reachable group? (4–5 pain cannot sustain venture growth.)
3. Does the model scale through software rather than people, buildings or hardware — does each extra real of capital unlock disproportionate growth, or merely keep the lights on?
4. Is 2–3× year-over-year growth plausible for several years?
5. Is there a reason a cash injection would accelerate it (a channel that works, a product gap to close), rather than just extend runway?

| | Indie / calm business | Venture-scale |
|---|---|---|
| Revenue ceiling that counts as a win | R$30k–R$500k MRR, profitable | Path to R$100M–1B+/year |
| Growth expectation | Steady; 20–50%/yr is great | 2–3×/yr early, then 100%+ |
| Capital | Bootstrapped or one small cheque; profitable within 12–18 months | Rounds; burn justified by land-grab; break-even 3–5 years out |
| Competition posture | Niche where big players don't bother; "fish where the fish are and nobody else is" | Win a large market before others do |
| Founder payoff | Salary 3–10× market + ownership + freedom | Equity outcome; high variance |
| Failure mode | Founder burnout, never leaving services mode | Running out of money before PMF |
| Examples | Vertical SaaS for a local trade, productized agency, niche tool with 2k paying users | Fintech, marketplaces with national density, platforms |

Brazilian note: local VC math is smaller — a credible path to R$50–100M ARR and an exit in the hundreds of millions of reais is venture-scale for most Brazilian seed funds, even if it is not for Sand Hill Road. State which investor universe the idea fits.

A venture-scale idea run as an indie business (no capital, slow) loses to a funded competitor. An indie idea run as a venture (burn, hiring, paid growth) dies of cost. Say which it is and size the plan accordingly.

---

## 3. Red flags / green flags by severity

Severity answers "what does this flag do to the verdict?" — see overrides in section 9.

### BLOCKER — cannot proceed until resolved
- Illegal, or no plausible regulatory path (lending without a licence or a BaaS partner; health claims without ANVISA; practicing a regulated profession without the council).
- The user of the product is not the payer, and the payer has no budget, urgency, or mandate.
- The founder cannot name 10 specific people/companies with this problem.
- Nobody currently tries to solve the problem at all — no workaround, no spend, no complaints.
- Contribution margin is negative at scale (each extra customer loses money even after fixed costs are ignored).
- Tarpit match with no evidenced "what's different now".
- The founder cannot afford the time or money the idea needs (and no plan to change that).

### MAJOR — verdict must address it; usually caps at VALIDATE-FIRST
- Crowded market where incumbents are rated 7+/10 by their users and no ignored segment exists.
- Only credible acquisition channel is paid ads (Meta/Google) with no organic or owned channel.
- Single-platform dependence (WhatsApp, Instagram, App Store, Mercado Livre, a bank's API) with no fallback.
- B2B sales cycle over 6 months while the founder has under 12 months of runway.
- Two-sided marketplace with no supply-side strategy or no density plan by city/category.
- Gross margin below 40% with no path to 60%.
- "We have no competitors" (means no market or no research). "We just need 1% of the market" (means no GTM).
- Habit change required with no external trigger or mandate.
- Founder building for a community they don't belong to and haven't observed.
- Needs regulatory approval with a 12+ month timeline and no bridge revenue.

### MINOR — note it, fix it later
- Pricing not yet set; brand/name; tech stack choices; website quality; a feature list that is too long; a pitch that takes more than two sentences to explain.

### Green flags — upgrade confidence
- People already pay for an inferior solution, or hire a human to do it.
- Strangers (not friends; ≥20 of them) describe the problem back in their own words, unprompted.
- A manual/concierge version has been sold and the buyers loved it.
- Community is actively complaining (forums, Reclame Aqui, WhatsApp groups, G2 one-star reviews with a consistent theme).
- Prospects ask urgent questions about price and start date; a company gives the founder its people's time for free.
- Reactions are polarized, not lukewarm; some people call it a toy.
- The founder has an earned secret or unique access to the audience.
- Level-1 why-now.
- The buyer and the user are the same person, with their own budget.

---

## 4. Porter's Five Forces — compact scoring

Score each force 1 (weak — favorable to a new entrant) to 5 (strong — hostile). Sum 5–25.

| Force | 1 — weak / favorable | 5 — strong / hostile | Evidence to look for |
|---|---|---|---|
| Rivalry | Few players, fast-growing category, differentiated products | Many similar players, flat market, price wars, high exit barriers | Number of funded competitors, pricing page convergence, discounting, churn-swap between vendors |
| Buyer power | Many small buyers, high switching costs, differentiated product | Few large buyers, easy switching, commoditized offer, price-sensitive budgets | Customer concentration, procurement habits, how often they switch tools, whether they can do it in-house |
| Supplier power | Many interchangeable suppliers, low switching cost | One critical supplier (a model vendor, a payments processor, a data provider, WhatsApp) that can raise prices or cut you off | Terms of service, platform fee history, alternative suppliers, forward-integration threat |
| Threat of substitutes | No good alternative; product embedded in workflow | Cheap, good-enough alternatives (spreadsheets, a human, doing nothing) | What customers use today and how much they hate it — the status quo is the main substitute |
| Threat of new entrants | Licences, capital, data, network effects, brand protect incumbents (and you, once in) | Weekend-clone territory; no barriers; attractive margins invite everyone | Time and cost to replicate the product, regulatory hurdles, whether incumbents can bundle it |

Interpretation: ≤10 attractive structure; 11–17 moderate, win through positioning; ≥18 hostile — only enter with a moat or a strong why-now. For pre-launch ideas, buyer power and substitutes usually decide the outcome; supplier power matters most when the idea sits on one platform or model vendor. Write one line per force on the *trend*: is it getting stronger or weaker?

---

## 5. Competitive positioning

List competitors in four rings; the inner rings are usually the ones founders ignore:

1. **Do-nothing / status quo** — spreadsheets, WhatsApp, a freelancer, tolerating the pain. Usually the real competitor; wins by default because switching has a cost and inertia is free.
2. **Substitutes** — a different category solving the same job (an accountant instead of bookkeeping software).
3. **Indirect** — same problem, different approach or segment (a horizontal tool used for this vertical).
4. **Direct** — same solution, same buyer. Include international players that could enter Brazil and local copies.

For each: price, segment, what users love and hate (reviews, Reclame Aqui, G2/Capterra, app-store 1-star themes), funding and apparent growth, and the gap.

**Positioning-map axes that tend to reveal room** (pick the two that matter): price vs. specialization; self-serve vs. sales-led; horizontal vs. vertical; DIY tool vs. done-for-you outcome; SMB vs. enterprise; local/compliance-aware vs. global-generic; integrated suite vs. best-of-breed. Plot the rings on them; the idea needs an empty quadrant with buyers in it, not just an empty quadrant.

**Crowded = validated demand vs. crowded = no room.** A crowded category is evidence that budget exists. It becomes "no room" when all of the following hold: incumbents are rated 7+/10 by their own users; there is no segment they ignore (too small, too local, too regulated, too low-ticket for their sales model); there is no why-now they cannot adopt; and the founder's Delta-4 is below 4. If incumbents are hated (low NPS, one-star themes, PE-owned and stagnant), crowded is an opportunity — the classic play is to find the incumbent customers hate and build the modern replacement. If incumbents are loved, pick a different segment or a different job.

---

## 6. Business-model archetypes

| Archetype | The one metric | Typical failure mode | Minimum viable scale (indie → venture) |
|---|---|---|---|
| B2B SaaS — SMB | Monthly logo churn (<3%) and NRR | SMB mortality (MEI/ME businesses close), low ACV vs. sales effort, churn outruns acquisition | ~100 paying customers at R$150–500/mo → 5k+ customers or move upmarket |
| B2B SaaS — mid-market/enterprise | Sales efficiency (new ARR ÷ S&M) and cycle length | Pilot purgatory, 9–18 month cycles burn runway, single-customer dependence | 3–5 referenceable logos paying → R$10M+ ARR with repeatable sales motion |
| Marketplace | Liquidity: fill rate (>80%) / time-to-match per city or category | Cold start, disintermediation, take rate too low to fund both-sided CAC, each city restarts from zero | One dense geography/vertical liquid → multi-city with ≥15% take rate |
| Consumer subscription / app | D30 retention (curve flattens) and free→paid conversion (≥2–5%) | No habit, CAC on Meta exceeds LTV, churn after the first month, R$10–20/mo ceiling | 1k paying subscribers with flat retention → 100k+ with organic growth loop |
| Services / agency / productized service | Gross margin per engagement (≥50%) and utilization | Founder is the bottleneck, feast-or-famine, no leverage, cannot raise prices | 5–10 retainers → indie by nature; venture only if productized into software |
| Infoproduct / creator | Audience size × conversion (1–3% of an engaged list) | No audience, one-launch business, platform-dependent reach, refund waves | 2–5k engaged list → rarely venture; a great indie business |
| Fintech (lending, payments, BaaS-based) | Cost of risk (default/fraud) and regulatory path | Regulation (Banco Central, CVM), fraud, CAC, thin spread after funding cost | Licence or BaaS partner + positive unit economics after losses → almost always venture |
| Hardware / physical product | Gross margin after COGS, import tax and logistics (≥40%) and inventory turns | Cash trapped in inventory, Brazilian import duties, returns, one bad batch | One production run sold profitably → scale needs capital; venture only with software attach |
| Local / physical business | Payback on capex per unit (12–24 months) and same-unit contribution margin | Location, rent, labor, seasonality, owner dependence | One unit profitable in 12–18 months → replicable playbook/franchise |

Blend models carefully: marketplaces that become SaaS, services that become software, and consumer apps that become B2B are common, legitimate paths — but the verdict should score the model the founder will actually run in the first 12 months.

---

## 7. Risk taxonomy + pre-mortem protocol

### Risk taxonomy

| Category | Core question | Watch for (Brazil) |
|---|---|---|
| Market | Is the problem real, frequent, and big enough for the game chosen? | Polite feedback; sizing by top-down 1%; demand concentrated in SP capital only |
| Product | Can it be built and will it be 4+ points better? | Unreliable third-party APIs; "AI will do it" without a data plan |
| Execution | Can this team ship and sell it in time? | Solo non-technical founder; no sales experience for a sales-led model |
| Regulatory / legal | Is it allowed, and what does compliance cost? | LGPD and sensitive data (health, minors), Banco Central, ANVISA, CFM/CRM, consumer law (CDC), labor law if using contractors as workers, tax regime (Simples vs. Lucro Presumido) |
| Financial | Do unit economics work; how long to break-even; who funds the gap? | High CAC on Meta, boleto/Pix churn, card installments eating margin, FX on foreign tooling |
| Timing | Is the why-now real and not yet over? | Riding a 2021 trend in 2026; regulation that may be reversed |
| Platform dependence | What happens if the platform changes terms? | WhatsApp API pricing, Instagram reach, app-store fees, Mercado Livre policy, one model vendor |
| Key-person | What breaks if one person leaves or burns out? | Co-founder with no vesting; a single contractor who holds the codebase; founder with a day job |

### Pre-mortem protocol

Run this after research, before scoring. It forces concrete failure modes instead of generic "risk".

1. Set the scene: "It is 12 months from now. The idea is dead. What killed it?" Write at least five distinct modes as "Died because ___", each specific and falsifiable ("died because clinics would not pay more than R$79/mo and CAC was R$900", not "market risk").
2. Triage each mode: **Tiger** (real, evidenced, keeps you up at night), **Paper tiger** (sounds scary, unlikely — record why), **Elephant** (nobody is discussing it; investigate before dismissing). Default to Tiger when unsure.
3. Rate each Tiger: likelihood 1–3 × impact 1–3. Anything scoring ≥6 is a verdict-level risk; list its mitigation, owner and a date or kill criterion.
4. Name **the single likeliest killer** in one sentence. It goes into the verdict verbatim, next to the cheapest experiment that would expose it.
5. Honesty rule: a pre-mortem that only lists survivable risks is a failed pre-mortem. If the founder cannot supply their own failure mode, the idea has not been thought through.

---

## 8. Assumption mapping

A plan is a stack of guesses. Find the load-bearing ones, rank them, and attach the cheapest test to each.

1. **Extract claims.** From the grilling and the research, list every "we believe that…": about the customer, the pain, willingness to pay, price, channel, the mechanism, costs, regulation, the team. Tag each with a category: desirability (they want it), viability (it makes money), feasibility (we can build it), GTM (we can reach them), legal/ethical, team.
2. **Keep only load-bearing claims** — those that, if false, kill the plan. Cosmetic assumptions are not worth testing.
3. **Steelman, then attack.** Write the strongest case that the assumption is true, then write the failure condition as "Fails if ___".
4. **Rank by importance × uncertainty** (1–3 each). Importance: what happens if it's wrong. Uncertainty: how much real evidence exists (founder conviction counts as zero). Test the top of the list first — high importance, high uncertainty, cheap to test is the whole point.
5. **Attach the cheapest experiment that moves belief**, with a kill criterion and a time box.

| Ladder (cheap → expensive) | Tests | Typical kill criterion |
|---|---|---|
| Desk research | Existing spend, competitor pricing, complaints, regulation | No evidence anyone pays for anything adjacent |
| 10–20 stranger interviews (Mom-Test style, no pitching) | Problem exists, frequency, current workaround | <30% describe the problem unprompted |
| Landing page / waitlist / smoke test with a price | Interest at a stated price | <2% conversion from a qualified audience |
| Presale, LOI, deposit, or paid pilot | Willingness to pay | Fewer than 3 of 10 say yes with money or signature |
| Concierge / manual version | Value delivered, cost to serve, retention | Customers do not come back or renew |
| Pilot in one segment/city | Unit economics and liquidity at small scale | CAC payback > 12 months (indie) / LTV:CAC < 3 |

Validation happens through selling, not building. Any assumption about willingness to pay should be tested with a transaction (or the closest thing to one) before code is written. Ten conversations and three payers is the minimum bar for "validated demand" on a pre-launch idea.

---

## 9. Scorecard → verdict

Score every dimension 1–5 using the anchors. Multiply by weight, sum, divide by 100 to get a 1–5 weighted score. Then apply the override rules — they exist because a fatal weakness cannot be averaged away by strengths elsewhere.

### 9.1 Dimensions and weights

| # | Dimension | Weight | 1 | 3 | 5 |
|---|---|---|---|---|---|
| 1 | Problem severity | 20 | Vitamin; no workaround; pain ≤4/10 | Workarounds exist; pain 5–7; some spend | People pay for inferior solutions; pain 8–10; urgent |
| 2 | Market size / SOM (for the declared game) | 15 | SOM can't sustain the game (indie: <R$20k MRR; venture: no path to R$100M/yr) | Indie: R$50–200k MRR reachable; venture: path to R$50–100M with adjacent markets | Indie: R$200k+ MRR in a niche nobody serves; venture: clear math to R$100M+/yr, TAM in billions |
| 3 | Why-now | 10 | None, and the idea has failed before | Level-2 trend-riding | Level-1: impossible before the change |
| 4 | Competition & moat | 10 | Incumbents rated 7+, no ignored segment, no moat; or a tarpit | Crowded but incumbents hated, or a segment they ignore; moat plausible later | Empty quadrant with buyers, plus an earnable moat (data, distribution, regulatory, switching costs) |
| 5 | Unit economics | 15 | Negative contribution margin or LTV:CAC < 1 in the realistic scenario | LTV:CAC 2–3, payback 12–18 months, margin 40–60% | LTV:CAC ≥ 3, payback < 12 months, gross margin ≥ 60% (SaaS ≥ 70%) |
| 6 | Founder fit | 10 | Outsider to the market, can't build or sell it, can't fund the time | Adjacent experience; can build or sell, not both | Earned secret, lived the pain, can build and sell, can absorb the schlep |
| 7 | GTM feasibility | 12 | Paid ads only; no access to buyers; sales cycle longer than runway | One credible channel; some access | Owned audience, partnership, or an untapped channel; first 10 customers nameable |
| 8 | Regulatory & execution risk | 8 | Blocking regulation or unbuildable in 12 months | Manageable compliance (LGPD, a partner licence); standard build risk | No regulatory exposure; buildable by the team in under 3 months |

Weights sum to 100. Problem severity carries the most weight because the market wins over team and product: a great team in a vitamin market loses. Unit economics and market size come next because they decide whether the game is even playable. Why-now, moat and founder fit are modifiers — they raise odds, they rarely create them.

### 9.2 Thresholds

| Weighted score | Verdict |
|---|---|
| ≥ 4.0 | **GO** — build the smallest sellable version now |
| 3.0 – 3.9 | **VALIDATE-FIRST** — run the named experiments before building |
| 2.2 – 2.9 | **PIVOT** — the problem or the market deserves a different angle; propose 2–3 |
| < 2.2 | **KILL** — do not spend more time; say what would have to change |

### 9.3 Override rules (apply after the score, in this order)

1. Any **BLOCKER** red flag → cap at VALIDATE-FIRST. If the blocker is structural and unfixable (illegal with no path, customer will never be the payer) → KILL.
2. Problem severity scored 1 → cap at PIVOT. A vitamin cannot be rescued by a moat or a great founder.
3. Unit economics that never break even in the *realistic* scenario within the game's horizon (indie: 18 months; venture: 36 months) → cap at PIVOT.
4. Two or more dimensions scored 1 → KILL, regardless of average.
5. Tarpit match without an evidenced "what's different" → cap at PIVOT.
6. Two or more **MAJOR** flags unaddressed → cap at VALIDATE-FIRST.
7. GO requires evidence, not projection: at least one paying/pre-paying customer, or ≥3 LOIs/deposits, or clear proof that the target buyer already pays for an inferior solution. Without it, cap at VALIDATE-FIRST with the presale as the first experiment.
8. A mismatch between the game declared and the plan (venture idea with no capital plan; indie idea with venture burn) → downgrade one level and say why.

The verdict block must state: the game (indie / venture, and which investor universe if venture), the weighted score and each dimension's score, which overrides fired, the single likeliest killer from the pre-mortem, and the top three experiments from the assumption map with kill criteria.

**Answer the founder's actual question.** Founders rarely ask "what is my weighted score" — they ask "can I live off this?", "can this reach R$ 1M ARR?", "should I quit my job?". Restate their question as a metric and answer it with a number in all three scenarios ("R$ 20k/month each: never / month 41 / month 30"). A verdict that is technically complete but never answers the question in the founder's own words has not done its job.

**Quantify the escape routes.** For any verdict below GO, name 2–4 concrete changes — different segment, price, revenue mechanism, or wedge — and re-run the model for each so the founder sees what the change is worth ("charge ~1% of the payments flowing through instead of a flat fee: 830 customers needed → ~180"). Naming a pivot without re-costing it is advice; re-costing it is analysis. The most valuable sentence in a PIVOT verdict is usually the one that shows the version of the idea that does close.

### 9.4 Worked mini-example

> **Read this for the mechanics, not for the answer.** The example is deliberately far from the ideas this skill usually sees — mid-market, hardware-attached, sales-led, high ACV, and it scores a GO. If the idea in front of you is a low-ticket SMB subscription, none of these scores transfer; a worked example that resembles the live idea is an anchoring hazard, so score from your own evidence and let the number land where it lands.

Idea: sensor kit plus software that predicts loom and dyeing-line failures for mid-size textile plants in Brazil, R$2,800/month per plant on an annual contract. Founder spent twelve years as a maintenance engineer in the sector; three plants have signed LOIs at that price.

| Dimension | Score | Reasoning |
|---|---|---|
| Problem severity | 5 | Unplanned downtime stops a line at a known hourly cost; plants already pay overtime crews and carry spare-part inventory to cope. They are spending today |
| Market / SOM (indie game) | 3 | ~4,000 plants in the size band; 120 customers = R$336k MRR. A strong indie or a small-fund venture, not a R$100M path |
| Why-now | 4 | LTE-M coverage plus sensor cost collapse made per-machine instrumentation affordable in the last two years; close to level 1 |
| Competition & moat | 4 | Enterprise MES suites cost 10× and ignore this size band; failure signatures accumulate into a data moat the incumbent cannot buy |
| Unit economics | 5 | ACV R$33.6k, CAC ~R$8k via association events, churn <1%/mo, gross margin 72% after hardware amortisation → LTV:CAC ≈ 4.2, payback ≈ 5 months |
| Founder fit | 5 | Twelve years doing the job, an earned secret about which failures are predictable, and can both spec and sell |
| GTM feasibility | 4 | Three LOIs, a named association channel, and a segment dense enough to reference |
| Regulatory & execution | 3 | NR-12 machine-safety adjacency; hardware install and field support are real execution risk |

Weighted: (20×5 + 15×3 + 10×4 + 10×4 + 15×5 + 10×5 + 12×4 + 8×3) / 100 = 422/100 = **4.22** → GO.
Overrides: no BLOCKER; no MAJOR unaddressed; rule 7 needs evidence and three signed LOIs at the real price supply it. No change.

Verdict: **GO, indie game** (target R$300k+ MRR, bootstrapped on annual prepay, profitable inside 12 months). Likeliest killer: this is a hardware archetype wearing SaaS clothes — cash trapped in sensor inventory and field installs, so growth consumes cash even at a healthy margin; a bad batch or a slow install queue stalls it. Experiments: (1) convert the three LOIs to paid annual contracts with 50% upfront — kill if fewer than two convert in 45 days; (2) instrument one line and predict a real failure before it happens — kill if no true positive in 60 days; (3) price the install and support of plant four end to end — kill if gross margin lands under 50% once field time is loaded.

### 9.5 Consistency rules

- Score from evidence gathered in the research phase, not from the founder's pitch. Where evidence is missing, score 2, not 3 — absence of evidence is a finding.
- Never round up to GO because the founder is enthusiastic, and never round down to KILL because the idea is unglamorous. Boring niches with paying customers are where most good indie businesses live.
- When two dimensions conflict (great economics, weak problem), trust problem severity — customers who don't feel the pain will not stay long enough for the economics to matter.
- Write every verdict so that a second analyst, given the same dossier, would reach the same score within ±0.3. If you can't justify a score in one sentence with a piece of evidence, you don't have that score.
