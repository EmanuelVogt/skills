# GTM, Marketing and Validation Plan Reference

Use this file when writing the dossier sections **Positioning**, **ICP & beachhead**, **GTM motion & channels** (CAC inputs for unit economics), **First customers**, **Launch & metrics** and **30/60/90 validation plan**. Default market is Brazil; amounts are BRL unless noted. Every cost, CPC and conversion figure here is an indicative 2025–26 range for planning, not a fact about the user's idea: confirm category-specific numbers during the research phase (Google Keyword Planner, Meta Ads Library, competitor pricing pages, Reclame Aqui) and feed the pessimistic end into the pessimistic scenario.

**Contents**
1. Positioning
2. ICP and beachhead selection
3. GTM motions and when each fits
4. Acquisition channel catalog (with Brazil notes and international transfer)
5. First 10 / first 100 customers playbook
6. Validation experiment catalog and signal-quality hierarchy
7. Customer-interview guidance
8. Launch plan skeleton and what to measure
9. 30 / 60 / 90-day validation plan template
10. Dossier output checklist

---

## 1. Positioning

### 1.1 The positioning chain
Work the chain in this order because each step constrains the next. Starting from "market category" produces a me-too pitch; starting from what the customer does today produces a pitch the customer recognises.

1. **Competitive alternatives** — what the ICP would do if the product did not exist. List the real ones, ranked by share of the segment that uses each: incumbent software, an agency or freelancer, the accountant, a spreadsheet, a WhatsApp group plus memory, a paper agenda, doing nothing. For most Brazilian SMB ideas the top two alternatives are a spreadsheet and WhatsApp.
2. **Unique attributes** — what the product has that those alternatives lack: capability, data, business model, distribution, price structure, local compliance, integration with the platform the customer already sells on. Drop any attribute a competitor could copy in one sprint; it is not a position, it is a feature.
3. **Value** — what each attribute lets the customer do that they could not before, in their units: hours/week, R$/month, orders recovered, fines avoided, days of receivables. An attribute with no value line is decoration.
4. **Best-fit segment** — who cares most about that value (pain intensity × frequency × budget). This seeds the ICP in section 2.
5. **Market category** — the frame that makes the value obvious at first hearing. Options: an existing category ("CRM"), a sub-segment of one ("CRM para clínicas"), or a new category. New categories cost years of education; only choose one when a real shift in the world makes the old category inadequate.

### 1.2 Positioning statement template
```
For [best-fit segment] who [trigger / struggling moment],
[product] is a [market category]
that [primary value, in the customer's units].
Unlike [main competitive alternative — including "doing it on WhatsApp"],
it [unique attribute → proof].
```
Compress it to a one-line hook and test it: can a stranger in the ICP repeat it to a peer after hearing it once? If they paraphrase it into a generic category ("ah, it's an app for managing stuff"), the category or the value line is wrong.

### 1.3 Positioning against "do nothing / spreadsheet / WhatsApp"
The status quo wins by default: it is free, already installed, socially accepted and requires no training. Nobody got fired for using WhatsApp. Treat it as the incumbent and position against it explicitly.

- **Quantify the cost of the status quo from interviews.** "Two hours a day reconciling Pix in a spreadsheet", "12% of delivery orders lost to late replies", "R$ 3k/year in multas because the deadline lived in someone's head". If you cannot put a number on the status quo, you have not found a pain yet, and no positioning will fix that.
- **Name the shift.** Something changed that makes the old way newly insufficient: a regulation (reforma tributária, NF-e/NFS-e obligations, LGPD), a platform (WhatsApp Business API, Pix, Pix automático), a behaviour (buyers expect a reply in minutes), a cost (take rates on iFood/Mercado Livre squeezing margins). The shift is the argument; the product is just the vehicle. Leading with features before establishing the shift is the "arrogant doctor" pattern: prescribing before diagnosing.
- **Pick a concrete foil.** "A agenda de papel", "a planilha do sócio", "o grupo de WhatsApp com 300 mensagens por dia". Customers recognise the foil instantly; they have never heard of the competitors in your landscape table.
- **Do not compete on "better organised".** The spreadsheet is already good enough at organising. Compete on something the status quo structurally cannot do: money moving (Pix reconciliation, cobrança automática), accountability across several people, compliance evidence, automation at volume, living inside the platform where the customer already sells.
- **Make switching cost zero.** Import the spreadsheet, work inside WhatsApp, start without a cadastro, coexist with the old way for the first month. The first version should sit beside the status quo, not demand its replacement.
- **Value-vector test.** Finish the sentence "Try to ___ with a spreadsheet" with something the customer will immediately concede is impossible. If no such sentence exists, the idea is a feature of someone else's product.

Flag in the verdict when the idea shows the **better trap** (feature-parity pitch in a crowded category), the **arrogant doctor** (solution before context) or **category vanity** (inventing a category with fewer than 100 customers).

---

## 2. ICP and beachhead selection

### 2.1 What a usable ICP is
A single market segment where (a) the value of solving the problem is roughly the same for everyone in it and (b) everyone in it can be reached the same way. "Pequenas empresas" fails both tests. "Clínicas odontológicas com 2–5 cadeiras em capitais, que atendem convênio e já usam agenda digital" passes both: same pain, same channels (dental associations, dental supply reps, Instagram).

Define the ICP with **three distinguishing attributes** chosen from: vertical, size, geography, role/title, tools already used, trigger event, observable behaviour, business model, psychographic. Add **disqualifiers** (who you will refuse even if they want to pay) and the **trigger event** that starts the search (new hire, fine, lost client, growth past a threshold). For B2C, write the "super-specific who": age band, city and class, identity ("mãe de primeira viagem", "dev em processo seletivo gringo"), daily context, where they already gather, what they already pay for. Identify the high-expectation customer: the most demanding person in the segment. Satisfy them and the rest of the segment follows; satisfy the average and nobody is delighted.

### 2.2 Beachhead scoring table
Score 3–5 candidate segments side by side. Weighted total guides the choice, but a score of 1–2 on pain, reachability or willingness to pay is disqualifying regardless of total, because those three multiply in practice: huge pain in a segment you cannot reach yields zero customers.

| Criterion | Weight | 1 | 3 | 5 |
|---|---|---|---|---|
| Pain intensity | 25% | Nice-to-have, vague | Recognised; workarounds exist | Daily, quantified loss, already spending time/money, getting worse |
| Reachability | 20% | Dispersed; no shared channel | Findable with effort (LinkedIn filters, lists) | Concentrated in a few groups, associations or platforms; list obtainable in a day |
| Willingness & ability to pay | 20% | No budget; expects free | Pays for something adjacent | Already pays an inferior tool, a freelancer or an employee for this |
| Decision speed | 10% | Committee, procurement, > 6 months | Owner decides in weeks | Owner decides on the call and pays by Pix |
| Density / referenceability | 15% | Members do not talk to each other | Some associations and groups | Tight community; peers copy each other; one logo opens ten doors |
| Regulatory friction | 10% | Licensed activity; sensitive data; ANVISA/BACEN/CVM/CFM in the loop | Standard compliance | Nothing beyond NF and LGPD basics |

### 2.3 Why a narrow beachhead beats a broad launch
- Concentration ignites. Hold the match in one place: aim for 30–50% share of the beachhead within 18–24 months, then move to the adjacent segment the first one references ("bowling pins"). Taking any customer who will pay is running the match along the log; it never lights.
- Every decision gets cheaper with a homogeneous segment: one message, one channel, one onboarding, one roadmap. A broad segment forces an average product that nobody loves.
- References compound in dense segments: three happy dentists in one city create pull; thirty scattered SMBs across verticals create nothing.
- A beachhead is an entry point, not a ceiling. Market size lives in the sizing reference; here the only question is "who first".
- Cold-outreach response rate is the honest ICP thermometer. Warm intros carry social bias and say nothing about the segment.
- Very small businesses (MEI, 1–2 people) churn because the business dies, not because the product failed. That produces noisy retention data and low ARPU. Prefer 5–50-employee businesses unless the model is explicitly built for high-churn, low-touch economics.

### 2.4 Good vs bad beachheads

| Bad | Why it fails | Good |
|---|---|---|
| "Restaurantes" | 1M+ establishments, heterogeneous pains, no single channel | Delivery-first restaurants in São Paulo capital with > 500 iFood orders/month; pain is margin under platform take rates; reachable through iFood partner groups and delivery-owner WhatsApp groups |
| "Pequenas empresas com problema financeiro" | Pain and channel vary by vertical | Clínicas de estética with 3–10 professionals who sell parcelado and lose the reconciliation between card, Pix and agenda |
| "Profissionais de saúde" | Doctors, nurses and psychologists share nothing operationally | Psicólogos autônomos with > 20 patients/week who bill by manual Pix and chase no-shows on WhatsApp |
| "Quem quer aprender inglês" | Everyone and no one; no trigger | Brazilian developers interviewing at foreign companies who need interview English in 60 days |
| "Condomínios" | Síndico changes yearly; decision by assembleia | Administradoras with 50–300 condomínios under management in capitals (buys once for all) |
| "Agro" | Crops, sizes and regions differ in everything | Soy producers of 500–3,000 ha in Mato Grosso who sell through cooperative X and already use tool Y |

---

## 3. GTM motions and when each fits

| Motion | Fits when | Price threshold (why) | Cost to start | Time to signal | Typical failure |
|---|---|---|---|---|---|
| Founder-led sales | Always, for B2B customers 1–20; it is how you learn objections, pricing and the real workflow | Any price; it is for learning, not scale | Founder time: 10–15 calls/week | 2–6 weeks | Never asking for money; relying only on warm intros |
| Sales-led (SDR + AE) | Multi-stakeholder B2B, demos, integration, security review | Brazil: ACV ≥ R$ 25–40k/yr for inside sales, ≥ R$ 100k for field. A fully loaded Brazilian AE costs R$ 15–30k/month (CLT + encargos + commission) and must close 3–5× her cost in new ARR; at 2–3 closes/month that requires ACV ≥ R$ 25–40k. US: ≥ US$ 10k inside, ≥ US$ 50–100k field | R$ 20–40k/month for one SDR + one AE + tooling | 2–4 months | Hiring reps before the founder has closed 10–20 deals and knows stage conversion rates |
| Product-led (self-serve) | Time-to-value under a day, clear aha moment, user can onboard alone, ARPU too low for humans | ARPU R$ 30–300/month B2B; any consumer price. Below R$ 300/month a human touch per customer destroys margin | Onboarding engineering + analytics; a volume channel (SEO, virality, app store, paid) | 1–3 months for activation; 6+ for retention | PLG with no volume channel; free tier that cannibalises paid |
| Community-led | Audience has an identity (devs, nutricionistas, corretores, síndicos) and benefits from peers | Any | Founder time 5–10 h/week; R$ 0–2k/month | 6–12 months | Building the community before the product; treating it as a broadcast list |
| Partner / channel | A partner already sells to the ICP and has an incentive: contadores, agencies, ERPs, franchisors, cooperatives, associations, Sebrae | Price must leave 20–40% for the partner and still clear CAC | Founder time + enablement material | 3–6 months | Partners who sign and never sell; nobody owns the partner relationship |
| Marketplace / app store | Product extends a platform where the ICP already transacts: App Store/Play, Shopify/Nuvemshop apps, HubSpot, iFood, Mercado Livre, WhatsApp BSPs, Bling/Tiny/Omie integrations | Must absorb a 15–30% platform take | Listing, reviews, ASO | 1–2 months | Platform dependency; rating under 4.5 kills conversion |
| Content / SEO-led | Search demand exists in PT-BR and buyers research before buying | Any; higher ARPU tolerates longer payback | Founder 10 h/week or R$ 1–5k/month outsourced | 4–9 months (faster in PT-BR than English: thinner competition) | Content without search intent; measuring rank instead of leads |
| Paid-led | LTV/CAC ≥ 3 and payback ≤ 12 months already known; creative can be tested cheaply | ARPU high enough that CAC stays under one-third of LTV | R$ 3–10k/month minimum to learn anything | 2–6 weeks for CPL; 3 months for payback | Scaling paid to fix a retention problem |

Sequence motions from cheap and informative to expensive and scalable: founder-led → one targeted low-cost channel (content, community or partner) → paid and brand last. Channels get more expensive along that path and more effective as you understand the customer, so the order is not optional. Do not layer a second motion (PLG on top of sales, or sales on top of PLG) until the first is stable; two half-working motions confuse attribution and the team.

---

## 4. Acquisition channel catalog

| Channel | Best fit | Indicative cost / CAC (BRL) | Effort | Time to signal | Notes |
|---|---|---|---|---|---|
| SEO / content (blog, YouTube) | B2B SaaS, marketplaces, anything with search intent | CAC R$ 50–500 once mature; media R$ 0 | High, sustained | 4–9 months | PT-BR SERPs are thin; YouTube is a search engine in Brazil |
| Google Ads search | High-intent, existing category | CPC: e-commerce R$ 1–3; services/health/education R$ 3–10; B2B software R$ 5–20; finance/insurance/legal R$ 10–40. CPL R$ 20–150 B2C, R$ 100–500 B2B | Medium | 2–4 weeks | No search volume = no category yet; do not force it |
| Meta (Instagram/Facebook) | B2C, SMB owners, infoproducts, local services | CPM R$ 10–40; CPC R$ 0.5–3; CPL R$ 5–40 B2C, R$ 30–200 SMB B2B; paying-customer CAC R$ 80–400 B2C | Medium; creative is the work | 1–3 weeks | Click-to-WhatsApp ads are the best-converting SMB format |
| TikTok | B2C under 35, impulse and education products | CPM R$ 5–25; CPC R$ 0.3–1.5 | Creative-heavy | 1–3 weeks | Organic reach still possible; Brazil is a top-3 market |
| LinkedIn ads | B2B with ACV ≥ R$ 20k | CPC R$ 15–40; CPL R$ 200–800 | Medium | 3–6 weeks | Founder organic posting in PT-BR beats ads before 100 customers |
| Outbound (email, LinkedIn, WhatsApp, phone) | B2B, ACV ≥ R$ 5k, founder-led | Media R$ 0; 50–100 touches per meeting; CAC R$ 500–5,000 when staffed | High | 2–4 weeks | WhatsApp reply rates far exceed email once you have a number; phone still works for SMB owners |
| Partnerships & integrations | SMB B2B; anything SMBs buy through accountant, ERP or platform | Rev-share 15–30% or CAC R$ 200–2,000 | High upfront | 3–6 months | Contadores are the distribution layer of Brazilian SMBs: every CNPJ has one |
| Communities (WhatsApp/Telegram groups, Discord, Facebook groups, forums) | B2C niches, devs, professionals | R$ 0–50 per customer | High, personal | 2–8 weeks | Give for weeks before asking; admins are gatekeepers |
| Influencers / creators | B2C, infoproducts, SMB tools | Micro (10–100k): R$ 500–5k/post or 20–50% affiliate; CAC R$ 30–300 | Medium | 1–4 weeks | Twenty micro creators beat one macro; attribute with cupom/links |
| Referral programs | Products with a social or professional graph, after retention is proven | CAC = incentive, R$ 20–200 | Low once built | 1–3 months | Referrals amplify demand; they never create it |
| App store optimisation | Mobile B2C | CPI R$ 2–8 Android, R$ 8–25 iOS; paying CAC R$ 50–300 | Medium | 1–2 months | Android ≈ 85% of Brazil; iOS users pay more per head |
| Marketplaces (Mercado Livre, Shopee, Amazon, Magalu, TikTok Shop) | Physical goods | Take rate 11–20% + Product Ads (ACoS 5–15%) + frete subsidy | Medium | 2–4 weeks | Traffic without brand; reputation drives ranking; margins thin |
| Infoproduct platforms (Hotmart, Kiwify, Eduzz) | Courses, digital products | ≈ 9–10% + R$ 1–2.5 per sale (verify); affiliates 30–60% | Medium | 2–6 weeks | "Lançamento" cycles and perpetual funnels; 7-day legal refund window |
| Events (trade shows, meetups, Sebrae, associations) | B2B verticals; first 100 customers | Sponsor R$ 2–30k; meetup R$ 0–1k; CAC R$ 500–5k | High, batchy | At event + 4–8 weeks | Attend first, speak second, sponsor last |
| PR / press | Launch moments; B2B credibility | DIY R$ 0; agency R$ 8–20k/month | Medium | 2–6 weeks | Spikes, not a channel |
| Product Hunt / Hacker News | US-facing dev and SaaS products | R$ 0 | One-off | 1 week | Near-zero for Brazilian SMB customers; skip |

### 4.1 Brazil-specific channel realities
- **WhatsApp is the default channel for everything.** Almost every smartphone owner uses it daily and a large share of SMBs run the business inside it. Plan for sales, onboarding, support and cobrança to happen there, and budget a human (or a well-built bot) to answer in **minutes**: a lead left waiting an hour is usually gone. WhatsApp Business (free) covers the first few hundred conversations a month; beyond that use the API through a BSP (Meta direct, Twilio, Zenvia, Take Blip, Z-API and others), where Meta charges per message or conversation (marketing roughly US$ 0.06, utility roughly US$ 0.01; check the current table). Unsolicited blasts get the number blocked and damage its reputation: warm the number, collect opt-in, and send only what the person asked for. Click-to-WhatsApp ads on Meta are the highest-converting format for SMB prospects because they remove the form.
- **Instagram is the SMB storefront.** Owners of clinics, salons, restaurants, stores and studios discover tools on Instagram, judge vendors by their profile, and buy through the DM. A dead Instagram is a trust penalty, even for B2B. "Link na bio", stories with proof, and DM-first selling work for SMB tools in ways that would look odd in the US.
- **Physical goods go through Mercado Livre first.** It holds roughly half of Brazilian e-commerce; Shopee competes on price, Amazon and Magalu follow, TikTok Shop is new. Plan for take rates plus ads plus shipping subsidies, and treat an own-store (Shopify, Nuvemshop, Loja Integrada) with Pix checkout as the margin play that only works once the brand exists.
- **Infoproducts have their own ecosystem.** Hotmart, Kiwify and Eduzz handle checkout, affiliates and co-production; the "lançamento" model (4–6-week launch cycles with a free event then a paid offer) and perpetual funnels dominate. Expect refunds within the legal 7 days and price in "12x de R$ X".
- **Google Ads CPCs are cheaper than US equivalents (often 3–6×) but conversion is lower** on mobile-heavy, lower-income traffic. Pull the category CPC from Keyword Planner during research rather than trusting the table above.
- **LinkedIn is large in Brazil** (top-5 market). Founder posting in Portuguese reaches decision makers organically; Sales Navigator (about R$ 400/month) is worth it for list-building; InMail converts worse than a WhatsApp message once you have the number.
- **YouTube** has one of the largest audiences in the world in Brazil and thin competition for how-to content in PT-BR. It is a search channel with a long tail, not a virality play.
- **Associations, councils and regional bodies gather the ICP in one room.** Sebrae (courses, feiras, partner programs), associações comerciais, sindicatos patronais, professional councils (CRM, CRO, CREA, OAB, CRP — you cannot sell through them, but their events are dense with the ICP), ABRASEL (food service), ABIH (hotels), ABF (franchising), ABComm, ABStartups, FIESP/FIRJAN, agricultural cooperatives, Rotary and Lions for regional owners. Events worth scanning: Web Summit Rio, RD Summit, VTEX Day, Gramado Summit, South Summit Brazil, Febraban Tech, APAS Show, Agrishow, Hospitalar, ABF Expo, Bett Brasil, Feira do Empreendedor.
- **Pix is a conversion lever, not just a payment method.** No card needed, instant, free for the payer, and a large share of adults have no or limited credit card. Pix checkout converts materially better than boleto; Pix automático enables recurring consumer billing. For B2C also offer parcelamento no cartão and price in instalments. For B2B, companies still expect boleto plus nota fiscal, and NF emission is a purchase prerequisite, not a nicety.
- **Reclame Aqui is the trust oracle.** Buyers check it before paying; the RA1000 seal and response rate are signals; competitors' complaint threads are free discovery (mine them for pains and churn reasons). Register the company early and answer every complaint.
- **Trust signals buyers look for:** CNPJ on the site, a WhatsApp number that answers, an active Instagram, a Reclame Aqui page, NF emission, checkout through a known PSP (Mercado Pago, PagSeguro, Stone, Asaas, Pagar.me), association seals.
- **LGPD:** B2B cold outreach with opt-out is defensible under legitimate interest; purchased lists are legally risky and commercially worthless. Consumer data needs consent and a purpose.

### 4.2 Going international: what transfers
- **Transfers:** self-serve PLG, LinkedIn outbound (the standard B2B channel in US/EU), app stores, SEO/content (English is 5–10× more competitive, so niche down harder), creators/YouTube, integration marketplaces (Shopify, HubSpot, Slack, Zapier), review sites (G2/Capterra play the Reclame Aqui role for US B2B buyers), Product Hunt/Hacker News/Reddit/Indie Hackers for dev and SaaS.
- **Does not transfer:** WhatsApp as a B2B sales channel in the US (email, SMS, LinkedIn instead; WhatsApp works in LatAm, Spain, Italy, India), Instagram-DM selling to businesses, Pix, boleto, "12x sem juros" framing, lançamento-style launches, phone cold-calling in the EU (regulated and culturally rejected).
- **LatAm (Mexico, Colombia, Chile, Argentina):** WhatsApp, Mercado Libre, Hotmart and Instagram all transfer; localise to Spanish properly; each country has its own rails (OXXO and SPEI in Mexico, Mercado Pago in Argentina) and currency volatility.
- **EU:** GDPR stricter than LGPD, VAT OSS, cookie consent, works councils for HR tooling; English works in the Nordics and the Netherlands, local language is required in DE/FR/IT/ES.
- **US:** CPCs 3–6× higher, willingness to pay 3–5× higher, SMB sales cycles shorter, Stripe and credit card expected, timezone and English fluency as real costs. Pricing in USD raises ARPU enough that a sales-led motion becomes viable with far fewer customers.

---

## 5. First 10 / first 100 customers playbook

### 5.1 B2B: first 10
1. **Map the warm network in concentric circles.** Fifty names in three rings: people who know you and feel the pain; second-degree contacts reachable by intro; strangers in the ICP. Work outward, but start cold outreach in parallel from week one because its reply rate is the only unbiased ICP signal.
2. **Ask for advice, not a sale.** "Estou construindo X para [segmento]; você vive isso? Tem 20 minutos?" People give advice readily and ignore pitches. A meeting booked as advice converts to a pilot once they describe their own pain out loud.
3. **Run 10–15 conversations a week yourself.** Nobody else can learn the objections, the real workflow and the price ceiling for you. At the end of a good call, make the ask: "o que precisaria acontecer para começarmos semana que vem?" Asking for money is the validation; discovery without an ask is theatre.
4. **Sign 3–5 design partners, paid.** They get weekly access to you, influence on the roadmap and a 30–50% discount for 6–12 months; you get a signed agreement, weekly calls, usage data and a case study. Charge something, because free partners skip the calls.
5. **Price pilots.** Time-boxed (60–90 days), paid (a R$ 1 invoice with nota fiscal tests procurement in a way R$ 0 never does), with written success criteria and the post-pilot price agreed upfront.
6. **Onboard by hand.** Install it for them, on a call or on site; import their spreadsheet; be the support line on WhatsApp. This is unscalable on purpose: it shows what the product must automate next.
7. **Use pre-sales and LOIs when the product does not exist yet.** An LOI is a signed, non-binding letter stating intent to buy at a price when criteria are met; use it for ACV above R$ 20k. Below R$ 5k, ask for pre-payment or a deposit instead; a deposit is a far stronger signal than any letter.
8. **Read cold reply rates as a thermometer.** A specific, relevant message that gets ≥ 5–10% positive replies indicates real pain; under 2% after two message variants means wrong segment or wrong problem.
9. **Hold the segment.** Do not expand until ten paying customers share the same three ICP attributes.

### 5.2 B2B: 10 → 100
Repeat exactly what closed the first ten and write it down: trigger, message, objections, proof, close. Add one cheap channel that matches the ICP (contador or agency partners, content built from customer problems, vertical events). Ask for referrals at the moment of first value, not at signup. Hire the first SDR only after the founder has closed 20–30 deals and knows conversion rates per stage; before that a rep inherits a process that does not exist.

### 5.3 B2C: first 100 → 1,000
- **Density first.** One city, one campus, one condomínio, one WhatsApp group, one subreddit. Visible local usage creates pull; scattered users create nothing.
- **Communities.** Be useful in 5–10 groups for weeks before asking anything; recruit admins as ambassadors.
- **Creators.** Ten to thirty micro creators (5–50k followers) on affiliate or cupom terms; track signups per creator; keep the three that convert.
- **Manual seeding.** Founders recruit users one by one, onboard them over WhatsApp and watch them use the product.
- **Referral loop in the core action** (share the result, invite a collaborator). Build it only after week-4 retention is visible; referral on top of churn just burns the network.
- **Waitlist with effort.** Counts only if people act: share, answer a survey, pay a deposit. A passive email list is not demand.

### 5.4 What "traction" means at each step

| Stage | You are proving | Traction looks like | Not traction |
|---|---|---|---|
| 0 → 10 (B2B) | Someone outside your network pays | 10 paying, ≥ 5 from cold or second-degree, same ICP, weekly usage | Free pilots; friends' companies; logos without usage |
| 10 → 100 (B2B) | A channel plus a message converts at a known rate | CAC known; ≥ 20% win rate on qualified demos; ≥ 3 referrals; logo churn < 3%/month | Growth only through the founder's personal network |
| 0 → 100 (B2C) | People come back unprompted | Week-4 retention at threshold (section 8); ≥ 30% of signups organic/referral; users explain it to each other | Downloads; waitlist size; likes |
| 100 → 1,000 (B2C) | A loop works | k-factor > 0.3 or one paid channel with payback < 6 months; retention curve flattens | Launch spike decaying to zero |

---

## 6. Validation experiment catalog

| Experiment | Cost (BRL) | Time | Tests | Pass | Fail | How people fool themselves |
|---|---|---|---|---|---|---|
| Landing page + ads smoke test | R$ 500–3,000 ads + R$ 0–300 page | 1–2 weeks | Problem resonance, message, rough CPL | Visitor → email ≥ 10% on targeted traffic, ≥ 3–5% on cold; CPL within economics | < 2%, or CPL > 30% of expected monthly ARPU | Sending friends; counting clicks not emails; copy so vague everyone "likes" it; no segment targeting |
| Fake door | R$ 0–500 | 1–2 weeks | Demand for a feature or product within existing traffic | ≥ 5–10% of exposed users click and leave an email | < 2% | Placing the door where curiosity clicks are free; never following up with interviews |
| Concierge / Wizard-of-Oz | R$ 0–2,000 + founder time | 2–6 weeks | Whether the outcome is valued, the real workflow, WTP | ≥ 5 of 10 clients continue past week 2 and pay something (R$ 50–500) | Clients stop replying | Delivering more than the product ever will; not charging |
| Pre-sale / deposit | R$ 0–1,000 (page + Pix/Stripe link) | 2–4 weeks | Willingness to pay at a real price | ≥ 5% of targeted traffic, or ≥ 20–30% of interviewed "interested" prospects, pay | < 1%, or zero of the interviewed | Discounting into a different product; ignoring refunds; family buying |
| Letter of intent (B2B) | R$ 0 | 2–6 weeks | Intent at a written price | ≥ 3 signed of 10–15 pitched, with price and criteria | "Manda a proposta" forever | LOIs with no price; counting verbal yes |
| 20-interview sprint | R$ 0–3,000 incentives | 2–3 weeks | Pain existence, frequency, current spend, trigger | ≥ 60% tell a specific recent story unprompted; ≥ 30% already spend money or hours; ≥ 3 ask to buy or try | Pain appears only after you describe it | Leading questions; interviewing friends; pitching |
| Fake pricing page | R$ 0–300 | 1–2 weeks | Price sensitivity, plan preference | ≥ 3–5% of ICP visitors click a paid plan (then "em breve" + email) | Clicks only on free | Traffic outside the ICP |
| Community poll | R$ 0 | 1–3 days | Direction between two options; recruiting | Use only to choose between messages or to find interviewees | Treating it as validation | Everything: polls measure opinions, not behaviour |
| Waitlist with referral | R$ 300–3,000 | 2–6 weeks | Desire strong enough to act | ≥ 20% of signups refer ≥ 1; ≥ 30% answer a 5-question survey | Signups that never open an email | Prizes unrelated to the product; vanity counts |
| Paid pilot (B2B) | R$ 0 | 30–90 days | Will they pay to try, and keep paying | Paid, weekly usage, ≥ 50% convert at the pre-agreed price | Free pilots with "vamos ver" | Calling unpaid usage a pilot |

### 6.1 Signal-quality hierarchy
Rank every piece of evidence on this ladder and say the rung out loud in the dossier. Higher rungs cost the customer something; that cost is what makes them informative.

1. **Money paid** — pre-sale, deposit, paid pilot, a subscription that renews.
2. **Signed commitment with a cost** — LOI with a price, contract, deposit.
3. **Repeated usage of a rough version** — weekly, unprompted, they complain when it breaks.
4. **Effortful action without money** — waitlist plus referral plus survey, a 30-minute interview, sharing their own data.
5. **Verbal interest from a stranger in the ICP** — especially urgent, practical questions: "quanto custa", "quando posso usar", "integra com X".
6. **Verbal interest from your network.**
7. **Likes, compliments, poll votes, "que legal".**

Friends and family sit at rungs 6–7 because honesty has a social cost for them, they rarely have the pain, they will not pay, and they confirm whatever framing you used. Treat their input as a source of interview candidates two hops away, never as evidence. A useful tell that fit is near: the tone of calls shifts from polite to impatient — prospects stop asking what it does and start asking when they can have it.

---

## 7. Customer-interview guidance

### 7.1 Recruiting 15–20 strangers in the ICP (Brazil)
- **LinkedIn:** filter by title, company size and region; open with one specific observation about them, ask for 20 minutes of advice, and name the pain. Expect 5–15% replies when the message is specific; a Sales Navigator trial unlocks the filters.
- **Instagram DMs:** for SMB owners and professionals (clínicas, salões, restaurantes, creators). Comment meaningfully on two posts first, then DM, then move the call to WhatsApp.
- **WhatsApp and Telegram groups:** professional groups (ask the admin), Sebrae cohorts, association groups. Post once, then go one-to-one.
- **Associations, councils, cooperatives:** ask the secretariat for five introductions; attend one event and book calls on the spot.
- **Cold outreach:** email followed by WhatsApp; 100 touches yield roughly 10–15 calls.
- **Pay for time:** R$ 50–200 by Pix or gift card (iFood, Amazon) for most professionals; R$ 200–500 or a donation for doctors, lawyers and executives. Paid strangers are worth more than free friends.
- **Snowball:** end every interview with "quem mais vive isso?" and ask for two names.
- **Screen:** must match the ICP's three attributes and have faced the trigger in the last 90 days. Plan for two sub-segments of ten each so the synthesis can show where the pain concentrates.

### 7.2 Question structure (30 minutes)
- **Warm-up (3 min):** role, what a typical week looks like.
- **The last time (10 min):** "Me conta a última vez que [situação]." What happened before, who was involved, which tools, how long it took, what went wrong, what it cost. Follow the timeline; ask "e depois?" and "por quê?" up to three times.
- **Current solution (5 min):** "Como você resolve isso hoje?", "Qual foi a última coisa que você pagou nessa área?", "O que você já tentou que não funcionou?"
- **Magnitude (5 min):** how often it happens, what happens if nothing changes, what they would give up to have it solved.
- **Close (5 min):** ask for the commitment appropriate to the stage (another call, intro to two peers, a pilot, a pre-payment) and for more names.

Rules that keep the data honest: ask about the past, not the future ("você usaria?" yields nothing); ask about their life, not your idea; no pitch until the final three minutes; listen 80% of the time; treat strong emotion as data and compliments as noise; seek the counterfactual on purpose (interview two people you expect to disagree).

### 7.3 Synthesising into evidence
- One row per interview: ICP attributes, trigger, story summary, current solution, spend (R$/month and hours/week), severity 1–5, asked to buy or try (Y/N), best quote.
- Tally: % with unprompted recent pain, % spending today, median spend, % asking for the product. Split by sub-segment; where the pain concentrates is the refined ICP.
- Grade for the dossier: **A** = ≥ 12 of 20 strangers with an unprompted recent story, ≥ 5 with current spend, ≥ 3 commitments; **B** = pain confirmed, spend unclear; **C** = pain only when prompted; **D** = fewer than 10 interviews or mostly network. Always write the counterfactuals: what you heard that argues against the idea.
- Stop at 15–20 per segment. Past that, interviews repeat unless the segment changes.

---

## 8. Launch plan skeleton and what to measure

### 8.1 Skeleton
- **Pre-launch (4–8 weeks).** Positioning locked word for word. ICP list of 200–500 names. Landing page, WhatsApp number and Instagram alive and answering. 10–20 design partners or beta users with quotable results. Assets: a 60–90-second demo, three proof points, one case. Audience warmed by founder posts three times a week and a waitlist with effort. Instrumentation live before day one: signup, activation event, week-1 and week-4 retention, payment, source attribution. Checkout tested with Pix and cartão, NF emission working. A one-page brief with goal, audience, creative, channels, stakeholders and explicit non-goals, so the launch does not grow features.
- **Launch (1–2 weeks).** Manual push to the list in order: WhatsApp one-to-one, email, social. Partner co-posts, community posts, one to three creators, press only if there is something remarkable to say. Product Hunt only for a US audience. Founder answers every WhatsApp within 15 minutes and watches activation daily.
- **Post-launch (weeks 2–8).** Measure the baseline after the spike; the spike is marketing, the baseline is fit. Interview every churned or inactive user within 48 hours. Ship fixes weekly. Turn the best customer into a case. Choose the one channel that produced paying customers and double down. Keep ten customer conversations a week.

### 8.2 What to measure, with early-stage thresholds

| Metric | Definition | Early threshold | Why it matters |
|---|---|---|---|
| Activation | % of signups reaching the aha action within N days | B2B SaaS 30–50%; B2C 20–40%; marketplace first transaction 10–20% | Below this, retention numbers are measuring onboarding, not value |
| Week-4 retention | % of activated users active in week 4 | B2C social/content 25–40%; B2C utility 15–30%; B2B SaaS ≥ 60%; marketplace buyers 20–30% | The curve must flatten; a curve sliding toward zero cannot be fixed by acquisition |
| PMF survey | % answering "very disappointed" if the product disappeared | ≥ 40% among users with ≥ 2 sessions in the last 2 weeks, n ≥ 40 | Segment the 40%; their shared attributes are the real ICP |
| NPS | Promoters minus detractors | B2B ≥ 30, B2C ≥ 20; noisy under n = 50 | The comments matter more than the number |
| Free → paid / trial → paid | Conversion to a paying plan | Self-serve free ≥ 3–5%; opt-in trial ≥ 15–25%; qualified demo → close ≥ 20% | Under 5% free-to-paid, paid acquisition cannot work |
| CAC payback | Months of gross margin to recover CAC | SMB B2B ≤ 12 months; consumer subscription ≤ 6; bootstrapped in Brazil ≤ 6–9 given the cost of capital | Payback, not LTV/CAC, decides whether you survive growth |
| Organic share | % of new signups from referral, direct or organic | ≥ 30% by month 3 after launch | Distinguishes pull from paid push |
| Logo churn | % of paying customers lost per month | SMB B2B ≤ 3%; consumer subs ≤ 8% early | Above this, growth is refilling a bucket |
| WhatsApp response time | Median first reply in business hours | < 15 minutes | In Brazil this is a conversion metric, not a support metric |

---

## 9. 30 / 60 / 90-day validation plan template

Tie every window to the load-bearing assumptions the dossier identified (typically A1 the pain exists and is frequent, A2 the ICP will pay price P, A3 the ICP is reachable through channel C at acceptable CAC, A4 users return/repeat). Pre-commit the go and kill rules before spending anything, because after the money is spent every result looks like "almost". "Kill" means stop this version of the idea (change segment, price or problem), not necessarily quit.

| Window | Goal | Experiments | Go criteria | Kill criteria | Budget |
|---|---|---|---|---|---|
| Days 0–30 — problem and segment (A1, A3) | Confirm the pain exists in one reachable segment | 20-interview sprint across two sub-segments; landing page with R$ 500–2,000 of ads; competitor and Reclame Aqui mining; 100 cold touches | ≥ 12 strangers with unprompted recent pain; ≥ 30% spend today; cold reply ≥ 5%; landing ≥ 10% on targeted traffic; one sub-segment clearly stronger | < 6 of 20 with unprompted pain; nobody spends; cold reply < 2% after two message variants; landing < 2% | R$ 1,000–4,000 |
| Days 31–60 — willingness to pay and solution (A2) | Confirm someone pays at price P for the core workflow | Concierge/Wizard-of-Oz with 5–10 clients; pre-sale or LOI at the real price; fake pricing page; design-partner agreements; prototype of the single core workflow | ≥ 3 payments (any amount) or ≥ 3 LOIs with price; ≥ 50% of concierge clients continue to week 4; pricing page ≥ 3% paid-plan clicks; CAC estimate ≤ 1/3 of modelled LTV | Zero payments after asking ≥ 15 qualified prospects; concierge clients ghost; only "free" gets clicked; CAC estimate > LTV | R$ 3,000–8,000 |
| Days 61–90 — repeatability and retention (A3, A4) | Show one channel and one cohort behave as the model assumes | MVP with 10–30 users; one primary channel run properly (R$ 3–8k ads, or 300 outbound touches, or 3 partner intros/week); referral ask; PMF survey if n ≥ 40; weekly cohort retention | 10 paying B2B or 100 active B2C; week-4 retention at section 8 threshold; channel CAC within model; ≥ 3 referrals; ≥ 40% very disappointed or an unmistakable shift to pricing/implementation questions | Retention sliding to zero; CAC > 2× modelled; users return only with manual prodding; growth only from the founder's network | R$ 5,000–15,000 |

Total: roughly R$ 10,000–27,000 plus about 300 founder hours (25 h/week). Larger budgets before fit do not buy better signal; they buy false confidence and a bigger ad bill. Scale the budget down for a pure B2B founder-led test (interviews and outreach cost time, not money) and up only for B2C ideas that need paid traffic to find strangers.

Template block for the dossier:
```
## Validation plan (30/60/90)
Load-bearing assumptions: A1 … | A2 … | A3 … | A4 …
| Window | Assumption | Experiment | Metric and threshold | Go | Kill | Budget (R$) | Owner |
| D0–30  | A1, A3 | … | … | … | … | … | … |
| D31–60 | A2     | … | … | … | … | … | … |
| D61–90 | A3, A4 | … | … | … | … | … | … |
Decision at day 30 / 60 / 90: continue | pivot (segment, price, problem) | stop.
Evidence grade today (section 7.3): A/B/C/D. Highest rung of evidence (section 6.1): …
```

---

## 10. Dossier output checklist
Before closing the GTM sections, make sure the dossier contains: a filled positioning statement with a named foil and a quantified status-quo cost; an ICP with three attributes, disqualifiers and trigger, plus the beachhead scoring table for at least three candidate segments; the chosen motion with the price-threshold reasoning; two or three channels with CAC ranges (pessimistic end fed into the pessimistic scenario); the first-10 playbook adapted to the idea; the interview recruiting plan; the measurement table with thresholds; and the 30/60/90 table with budget and pre-committed kill rules. If any of these cannot be filled from the conversation and research, say so explicitly rather than inventing numbers.
