# Research Playbook

Deep-research procedure that runs after the interview and before the financial model and verdict.
The goal is not "a report": it is a set of defensible numbers and evidence the next phase can plug in,
with every number tagged by how much to trust it. Default home market is Brazil; the Brazil-specific
parts swap for the equivalent national sources when the user names another country.

**Contents**
1. Before searching: build the vocabulary and the plan
2. Research dimensions, minimum searches, and what "done" looks like
3. Parallel split into subagents
4. Query templates (PT-BR + EN) per dimension
5. Source hierarchy and trust rules (including the press-release trap)
6. Brazil source catalog
7. International source catalog
8. Competitor research technique
9. Demand-signal techniques
10. Research hygiene
11. Research output contract

---

## 1. Before searching: build the vocabulary and the plan

Brazilian customers, press and regulators name categories differently from the US. A search for the
English category name in Brazil returns foreign results and misses the local market entirely, so do
this first, in under five minutes:

- Write a **vocabulary list**: 3–6 PT-BR terms and 3–6 EN terms for the category, the problem, and the
  buyer (e.g. "controle de estoque / gestão de estoque / inventory management"; "clínica / consultório /
  medical practice"). Pull terms from the interview, then refine after the first competitor search — the
  way competitors describe themselves is the vocabulary customers search for.
- Fix the **market definition** from the interview: who pays, what unit is sold (seat, transaction,
  unit, month), which geography first. Everything below is sized against this definition; a vague
  definition is how TAMs get inflated.
- Note the **current date** and use the current and previous year in queries (reports lag 6–18 months).
- Create `ideas/<slug>/research/` and an empty `ideas/<slug>/sources.md` now, so incremental saving has
  a target.

Order of operations when running sequentially: competitors → demand → market size → pricing and costs →
channels → regulation → analogues → trends. Competitors go first because they teach the category
vocabulary and price anchors that every other dimension depends on.

## 2. Research dimensions, minimum searches, and what "done" looks like

Budget 25–40+ searches for the whole job; the minimums below sum to roughly 30–36. A search counts
only if its result was read (snippet or fetched page) and at least one fact or "nothing found" was
logged. Save raw notes to `ideas/<slug>/research/<file>.md` as you go.

| # | Dimension | File | Min searches (BR / intl) | Done when |
|---|---|---|---|---|
| a | Market size, national and international | `market-size.md` | 3 / 2 | One primary **count** for the bottom-up base (IBGE, CNPJ, ANS, INEP…); one top-down figure for Brazil and one global; the two reconciled into a stated range; a growth rate with source |
| b | Competitors, national and international | `competitors.md` | 4 / 3 | ≥5 Brazil-relevant and ≥5 international players profiled with pricing; each international player rated for likelihood of entering Brazil; ≥2 review sources mined per top-3 competitor; positioning gaps named |
| c | Demand evidence / problem validation | `demand.md` | 3 / 1 | ≥3 independent signal types (trends, complaints, workarounds, ads density, job posts) each rated weak/moderate/strong; verbatim customer quotes captured with URL |
| d | Customer and ICP evidence | `customers.md` | 2 / 0–1 | Segment count from a quantitative source; who uses vs who pays; buying trigger; budget owner; what they spend today on the problem |
| e | Pricing and business-model benchmarks | `pricing.md` | 2 / 1 | Price matrix of ≥5 competitors in BRL (converted where needed); dominant model in the category; low / median / high price anchor; any willingness-to-pay evidence |
| f | Regulation, tax and legal | `regulation.md` | 2 / 0–1 | Regulator(s) named; licences, registrations or certifications with time and cost; tax regime assumption; LGPD and consumer-law implications; showstoppers flagged explicitly |
| g | Trends and why-now | `trends.md` | 1 / 1 | ≥2 why-now drivers with evidence; ≥1 counter-trend or headwind; fad check on a 5-year Google Trends view |
| h | Cost-to-run benchmarks | `costs.md` | 3 / 0 | Salary table for key roles (CLT vs PJ); cloud/tool/API costs; payment and platform fees; accounting and legal; a monthly fixed-cost estimate for the first 12 months |
| i | Acquisition channels and CAC | `channels.md` | 2 / 1 | CPC/CPM for the core terms; ≥2 benchmark CACs from comparable companies or reports; channels ranked with reasoning; the channel where the ICP already congregates identified |
| j | Analogues and the graveyard | `analogues.md` | 2 / 2 | ≥3 analogues: at least one failure or shutdown, one survivor, one other-country version; for each, the outcome and the stated cause |

Stop a dimension when it is "done" or when two consecutive searches add nothing new; then write its
contract block (section 11) and move on. Diminishing returns are real: the 9th competitor search rarely
changes the verdict, the first analogue shutdown often does.

## 3. Parallel split into subagents

When subagents are available, run 4–6 in parallel. Give each one: the interview summary (idea, ICP,
geography, business model, price hypothesis), the vocabulary list, the slug, its file path(s), the
query templates for its dimensions, the source rules (section 5), and the contract format (section 11).
Each subagent writes its raw file(s) and returns its contract block(s) inline; the parent merges the
blocks into `research/summary.md` and the bibliographies into `sources.md` (dedupe by URL, renumber).

| Subagent | Dimensions | Returns |
|---|---|---|
| `market-sizer` | a, d | Bottom-up count table (segment × count × source), top-down figures, reconciliation range, ICP evidence; ≥7 searches |
| `competitor-scout-br` | b (national + international players already in or entering Brazil) | Competitor table (≥5), Brazil-presence check per foreign player, review-mining themes with quotes; ≥7 searches |
| `competitor-scout-intl` | b (international), j | Competitor table (≥5), analogue/graveyard table with causes; ≥7 searches |
| `demand-miner` | c, i (where the audience congregates) | Demand-signal table, workaround inventory, ads-density note, Trends read-out; ≥6 searches |
| `economics-bencher` | e, h, i (CAC benchmarks) | Price matrix, cost-to-run table, CAC and channel benchmarks; ≥7 searches |
| `rules-and-winds` | f, g | Regulatory checklist with showstoppers, tax-regime note, why-now evidence and headwinds; ≥5 searches |

With only four subagents, merge `competitor-scout-intl` into `competitor-scout-br` and `rules-and-winds`
into `economics-bencher`. With none, run the sequence from section 1 and save after every 3–5 searches.

## 4. Query templates (PT-BR + EN) per dimension

Replace `[categoria]`, `[problema]`, `[cliente]`, `[concorrente]`, `[ano]` with the vocabulary list.
Run each template with at least two synonyms. Operators that pay off: quotes for exact phrases,
`site:`, `filetype:pdf`, `-site:` to exclude report mills, `OR` for synonyms, `before:`/`after:` for
recency. If the search tool ignores an operator, rewrite it as plain keywords ("reclameaqui
[concorrente]" instead of `site:reclameaqui.com.br`). Brazilian sources need PT-BR queries; an EN query
returns almost nothing about Brazil.

**a. Market size**
- PT: `"[categoria]" mercado Brasil [ano] faturamento` · `quantas empresas de [segmento] existem no Brasil` · `IBGE [segmento] número de estabelecimentos` · `"[categoria]" relatório [ano] filetype:pdf` · `[segmento] CNAE quantidade empresas ativas` · `[categoria] "bilhões" Brasil [ano] -site:prnewswire.com`
- EN: `[category] market size [year] -marketsandmarkets -grandviewresearch` · `number of [customers] worldwide` · `[category] revenue 10-K segment` (SEC) · `[category] market Latin America Brazil share` · `"[category]" TAM bottom-up`

**b. Competitors**
- PT: `[categoria] software Brasil` · `melhor [categoria] para [cliente]` · `alternativa ao [concorrente]` · `[concorrente] vs [concorrente]` · `[concorrente] preço OR planos OR "quanto custa"` · `[categoria] startup Brasil rodada OR investimento` · `site:b2bstack.com.br [categoria]` · `site:capterra.com.br [categoria]` · `[concorrente] CNPJ` (checks legal entity, porte, capital social)
- EN: `[category] alternatives` · `best [category] [year]` · `[competitor] pricing` · `site:g2.com [category]` · `site:producthunt.com [category]` · `site:crunchbase.com [category]` · `site:ycombinator.com/companies [category]` · `[competitor] Brazil OR "Latin America" expansion` · `site:linkedin.com/jobs [competitor] Brazil`

**c. Demand / problem validation**
- PT: `"[problema]" reclamação OR reclamações` · `site:reclameaqui.com.br [categoria OR concorrente]` · `"como resolver" [problema]` · `"planilha de" [problema] grátis` · `[cliente] "perde tempo" OR "dor de cabeça" [problema]` · `[problema] grupo whatsapp OR telegram` · `site:reddit.com [problema] brasil` · `site:jusbrasil.com.br [problema]` (legal-flavoured pain)
- EN: `site:reddit.com [problem] "anyone else"` · `[problem] "I built a spreadsheet"` · `site:indiehackers.com [category]` · `[customer] biggest challenges [year] survey` · `"looking for a tool" [problem]`

**d. Customers / ICP**
- PT: `perfil [cliente] Brasil pesquisa [ano]` · `quantos [profissionais] existem no Brasil` (CFM, OAB, CRC, CREA, CRM-type registries) · `[cliente] "gasta" OR "orçamento" [categoria]` · `Sebrae [segmento] perfil` · `Cetic TIC Empresas [tecnologia]`
- EN: `[customer] demographics [category] report` · `how [customers] choose [product category]` · `[customer] budget [category] percent of revenue`

**e. Pricing / business model**
- PT: `[categoria] preço mensal` · `[concorrente] planos` · `quanto custa [serviço] no Brasil` · `[categoria] "por usuário" OR "por transação" OR "comissão"` · `[categoria] tabela de preços [ano]`
- EN: `[category] pricing comparison [year]` · `[category] pricing page` · `[category] average contract value` · `[category] take rate benchmark` · `[category] freemium conversion rate`

**f. Regulation, tax, legal**
- PT: `[atividade] precisa de licença OR autorização OR registro` · `ANVISA RDC [produto]` · `Banco Central resolução [atividade]` · `CVM resolução [atividade]` · `ANS [atividade] regulamentação` · `Resolução CFM [atividade]` · `[atividade] LGPD` · `[atividade] Simples Nacional anexo` · `[atividade] reforma tributária IBS CBS impacto` · `[atividade] projeto de lei [ano]`
- EN: `[activity] regulation Brazil` (catches law-firm briefings) · `[activity] licensing requirements [country]` · `[category] regulatory risk [year]`

**g. Trends / why-now**
- PT: `tendências [setor] [ano] Brasil` · `[setor] relatório anual [ano] filetype:pdf` · `Think with Google Brasil [setor]` · `McKinsey OR BCG OR Bain Brasil [setor]` · `[setor] "cresceu" OR "caiu" [ano]`
- EN: `[industry] trends [year]` · `[technology] adoption rate [year]` · `[industry] "state of" report [year]` · `why now [category]`

**h. Cost-to-run**
- PT: `salário [cargo] [ano] Brasil` · `site:glassdoor.com.br [cargo] salário` · `custo funcionário CLT cálculo` · `[ferramenta] preço Brasil` · `taxa Pix OR boleto OR cartão [PSP]` · `Mercado Livre OR Shopee OR iFood comissão [ano]` · `contador online preço Simples Nacional`
- EN: `[role] salary Brazil [year]` · `AWS sa-east-1 pricing vs us-east-1` · `[API/tool] pricing` · `[category] gross margin benchmark`

**i. Channels / CAC**
- PT: `[termo] CPC Google Ads Brasil` · `CAC [categoria] Brasil benchmark` · `Meetime "Inside Sales Benchmark"` · `RD Station "Panorama de Marketing"` · `[categoria] "custo de aquisição"` · `[cliente] onde compra OR como escolhe [categoria]`
- EN: `[category] CAC benchmark [year]` · `[category] CPC [year]` · `[category] "payback period" SaaS benchmark` · `how [competitor] acquires customers`

**j. Analogues and graveyard**
- PT: `[categoria] startup "encerra" OR "fechou" OR "descontinuado" OR "pivotou"` · `[categoria] "foi adquirida" OR "fusão"` · `[concorrente] demissões OR "layoffs"` · `[categoria] startup Brasil "não deu certo"`
- EN: `[category] startup shut down` · `site:failory.com [category]` · `[category] "post-mortem" startup` · `[category] startup Mexico OR Colombia OR India OR Indonesia` (similar-income analogues) · `[competitor] acquired OR "ceased operations"` · `site:layoffs.fyi [category]`

### 4.1 When search is unavailable or exhausted

A session's web-search budget is finite and may already be spent. Probe with one query before fanning out; if it fails, do not let four subagents each rediscover it. Search is not the only way to reach a fact:

| Instead of searching | Do this |
|---|---|
| Competitor pricing | `WebFetch` the pricing page directly — vendors keep them at predictable URLs (`/precos`, `/pricing`, `/planos`) |
| Install base, ratings, verbatim reviews | Browser automation of the Chrome Web Store, Play Store, App Store, G2 or Capterra listing pages. These render live counts that search snippets do not carry |
| Country statistics | Public APIs via `curl` from Bash: World Bank, IBGE SIDRA, BACEN SGS, and other open endpoints return JSON without a search engine. One API call can replace an entire dimension of guesses |
| Company existence, size, filings | CNPJ lookup pages, SEC EDGAR full-text search, LinkedIn company pages by direct URL |
| Category listings | Directory URLs you can construct: `g2.com/categories/<slug>`, `b2bstack.com.br/categoria/<slug>`, `ycombinator.com/companies?query=` |

Two dimensions degrade badly without search and you must say so rather than pad them: the **graveyard** (finding companies that died needs discovery, not fetching) and **demand signals** (Reddit and forum aggregation — expect 403s and CAPTCHAs on direct fetch). When they come up empty, set the evidence grade accordingly, leave the quote bank empty, and make the validation plan test exactly those gaps. A dossier that admits an empty quote bank is worth more than one that invents quotes.

Record in the dossier which dimensions ran without search. The quality bar's "25+ searches" is an input metric; a run that reached better evidence by other means has not failed, but the reader has to know which route was taken.

## 5. Source hierarchy and trust rules

Rank sources by how close they are to the thing counted. Closer wins when numbers conflict.

| Tier | What | Why it ranks here |
|---|---|---|
| 1 · Primary data | IBGE/SIDRA, PNAD, Censo, BACEN, Receita Federal CNPJ dumps, CAGED/RAIS, dados.gov.br, CVM/B3 filings, ANS, ANVISA, ANATEL, DATASUS, INEP; SEC EDGAR, Census, Eurostat, OECD, World Bank; company pricing pages; app-store listings | Counts, not estimates; methodology published; reproducible |
| 2 · Sector associations and ecosystem reports | Sebrae, ABStartups, Distrito, Liga Ventures, Sling Hub, Abecs, Febraban, Abrasel, Abimaq, Neotrust/NIQ Ebit, Abcomm, Cetic.br, Abrainc, Cepea, IESS | Close to members' real data; some self-interest in looking big |
| 3 · Analyst houses | Statista, Gartner, IDC, Forrester, McKinsey, CB Insights, PitchBook, Crunchbase, Dealroom | Real analysts, but global definitions and paywalled methodology; Brazil is often a footnote of "LatAm" |
| 4 · Press | Valor, Exame, Folha, Estadão, Brazil Journal, NeoFeed, Pipeline, Startupi, Startups.com.br; TechCrunch, Reuters, Bloomberg | Good for events (funding, shutdowns, regulation), weak for sizes — they quote tier 5 |
| 5 · Blogs and press-release market reports | Grand View Research, MarketsandMarkets, Mordor, Fortune Business Insights, Technavio, Research and Markets and their PR Newswire / GlobeNewswire / openPR syndications; vendor blogs | Marketing for paid reports; treat as a weak [estimate] |

**The "USD X billion at CAGR Y%" trap.** Report-mill numbers are produced to sell reports: the market
is defined as broadly as possible (the global "pet care market" when the idea is a dog-walking app in
São Paulo), the methodology is not published, forecasts are straight-line extrapolations, and the
publishers copy each other, so "three sources agree" is frequently one number repeated. Brazilian press
reprinting a foreign report is the same number in disguise. Rules:
- Never use a tier-5 figure as TAM. Log it as `[estimate]` with confidence L and keep it only as an
  upper-bound sanity check.
- Triangulate every headline number with a **bottom-up count**: `number of target customers × price ×
  frequency`, each factor from tier 1–2 sources. Then check against a third angle: the sum of the
  known competitors' revenues (CVM/SEC filings, funding-implied revenue) is a floor for the served market.
- If top-down and bottom-up differ by more than ~3×, the definition is wrong, not the arithmetic. Narrow
  the definition until they reconcile and report the narrower number (the same rule the financial model
  applies).
- Prefer a 2-year-old primary count over a fresh tier-5 forecast. Age the old count with the published
  growth rate and inflation (IBGE IPCA calculator or BACEN "Calculadora do Cidadão") and tag it `[estimate]`.
- Quote currencies as published. State the BRL/USD rate and date used for any conversion; never mix
  nominal years without saying so.

**Transferring foreign benchmarks to Brazil.** Do not scale a US number by GDP ratio. Adjust with
customer counts (tier 1), willingness to pay (SMB SaaS ARPU in Brazil is typically a fraction of US
ARPU — verify per category), card and internet penetration (Cetic.br TIC surveys), informality share,
and regional concentration (São Paulo and the Southeast carry a disproportionate share of spend). Write
the adjustment down as an `[estimate]` with the multipliers shown.

## 6. Brazil source catalog

| Purpose | Source | What to pull |
|---|---|---|
| Demographics, households | IBGE Censo 2022 (censo2022.ibge.gov.br), SIDRA (sidra.ibge.gov.br) | Population by age, municipality, income bracket; household counts |
| Labour, income, purchasing power | IBGE PNAD Contínua via SIDRA; POF (household budget survey); ABEP Critério Brasil (abep.org/criterio-brasil); Cielo ICVA; Serasa/SPC default rates | Workers by occupation, income distribution, share of spend by category, class cut-offs |
| Businesses by CNAE, size, region | Receita Federal CNPJ open data (dados.gov.br → "Cadastro Nacional da Pessoa Jurídica"); Mapa de Empresas (gov.br/empresas-e-negocios); IBGE CEMPRE; free lookups casadosdados.com.br, cnpj.biz; Econodata counts | Active CNPJs by CNAE × porte × UF; openings/closures; a single competitor's porte, capital social and Simples opt-in |
| Formal employment flows | Novo CAGED and RAIS (pdet.mte.gov.br); salario.com.br (derived from CAGED) | Hires by CNAE and municipality; median salaries by CBO occupation |
| Macro, credit, payments | BACEN SGS time series (www3.bcb.gov.br/sgspub), Pix statistics page, Relatório de Economia Bancária; Abecs card stats; Febraban banking-tech survey | Pix volumes, card TPV, credit stock and rates, Selic, FX |
| E-commerce and retail | Neotrust/NIQ Ebit "Webshoppers", Abcomm forecasts, Mercado Livre "Tendências" (tendencias.mercadolivre.com.br), ABRAS, ABF (franchising), Abrasce | GMV by category, ticket size, share of marketplaces, franchise counts |
| Fintech and payments | Distrito Fintech Report, ABFintechs, BACEN authorised-institution lists, CVM open data (dados.cvm.gov.br) | Player counts, licence types, public-company revenue |
| Health | ANS (beneficiaries by plan and region), DATASUS TabNet and CNES (establishments), CFM Demografia Médica, IESS, Anahp, Abramed, Interfarma | Counts of clinics, hospitals, physicians, insured lives; spend |
| Education | INEP Censo Escolar and Censo da Educação Superior, e-MEC (emec.mec.gov.br), Abed (EAD), Semesp | Schools, students, institutions by type and region; online-education share |
| Agro | IBGE Censo Agropecuário, Cepea/Esalq agribusiness GDP, CNA, Conab, Embrapa, Radar Agtech | Farms by size and crop, prices, agtech counts |
| Real estate and construction | FipeZap index, Abrainc, CBIC, Secovi-SP, Abecip (mortgage), DataZAP | Prices, launches, financing volumes, inventory |
| Telecom and digital adoption | ANATEL open data (informacoes.anatel.gov.br), Cetic.br TIC Domicílios and TIC Empresas | Connections, device usage, SMB software adoption |
| SMB statistics | Sebrae / DataSebrae (datasebrae.com.br), Portal do Empreendedor (MEI) | MEI and SMB counts, survival rates, sector profiles |
| Startup funding and ecosystem | Sling Hub, Distrito Dataminer, Liga Ventures maps, ABStartups mapping, LAVCA, ABVCAP, Crunchbase; press: Brazil Journal, NeoFeed, Startupi, Startups.com.br, Pipeline | Rounds, valuations, player lists per vertical, shutdowns and M&A |
| Consumer complaints | Reclame Aqui (reclameaqui.com.br), consumidor.gov.br (open data by company and sector), Procon rankings | Complaint volume and themes per competitor; response and resolution rates |
| Software reviews | B2B Stack (b2bstack.com.br), Capterra.com.br, GetApp BR, Google Play / App Store BR | Ratings, review counts, "dislike" themes |
| App rankings | Google Play and App Store top charts (BR), Similarweb app rankings, AppBrain, Sensor Tower / AppFigures free tiers | Category rank, download bands, rating counts |
| Salary benchmarks | Glassdoor BR, salario.com.br, Robert Half Guia Salarial, Catho, Revelo and Gupy tech reports, LinkedIn Salary | CLT ranges by role and seniority; PJ rates from Workana/99Freelas |
| Cloud, tools, fees | AWS/GCP/Azure pricing calculators (region sa-east-1 vs us-east-1); Stripe BR, Pagar.me, Asaas, Mercado Pago, Vindi, iugu pricing pages; Mercado Livre, Shopee, Amazon BR, iFood, Hotmart fee pages; Locaweb/Hostinger/Magalu Cloud for BRL-billed hosting | Per-transaction and percentage fees, boleto cost, anticipation rates, hosting premium for the São Paulo region |
| Consumer behaviour | Opinion Box, Datafolha, Think with Google Brasil, Kantar/Ipsos BR, Comscore BR | Surveys on usage, channels, purchase drivers |
| Law and regulators | gov.br portals of ANVISA, ANS, ANATEL, BACEN, CVM, SUSEP, ANPD; Planalto legislation; Jusbrasil; law-firm briefings (Mattos Filho, Pinheiro Neto, Demarest, BMA) | Texts of resolutions, licence requirements, timelines, pending bills |

Brazil specifics to keep in mind while using these: a large share of workers and micro-businesses are
informal, so CNPJ counts understate demand for consumer-ish SMB products and overstate "companies with
budgets"; filter CNPJs by `situação cadastral = ATIVA` and by porte; the MEI revenue ceiling and the
Simples Nacional ceiling (check current values) bound what very small businesses can pay; WhatsApp is
the default sales and support channel; installments ("parcelado") and Pix shape willingness to pay and
cash flow; Pix Automático (recurring Pix) matters for subscriptions because card-failure churn is high.
For costs: a CLT hire costs roughly 1.5–2.0× gross salary once charges, 13th salary and vacation are
loaded (lower under Simples Nacional, which waives the employer INSS share for most service annexes),
while a PJ contractor costs close to the invoiced amount — state which you assumed; USD-billed cloud,
APIs and tools add FX exposure, IOF on international card payments and usually no nota fiscal, so check
whether a BRL-billed alternative exists before modelling them at today's rate.

**Other home countries.** Swap the table for the equivalent: national statistics office, central bank,
company registry and tax authority open data, consumer-complaints platform, startup association and
the dominant local marketplaces and review sites. Keep the international catalog as is.

## 7. International source catalog

| Purpose | Source |
|---|---|
| Public-company revenue and segments | SEC EDGAR (10-K, S-1), investor-relations pages, Companies House (UK) |
| Official counts and macro | US Census and BLS, Eurostat, OECD, World Bank, IMF, UN Comtrade, national statistics offices |
| Funding, players, shutdowns | Crunchbase, Dealroom, PitchBook (snippets), CB Insights research, YC company directory, Sifted (EU), Tracxn/Inc42 (India), Tech in Asia, Contxto/LatamList (LatAm), Failory cemetery, Layoffs.fyi, Wayback Machine for dead companies |
| Reviews and alternatives | G2, Capterra, GetApp, TrustRadius, AlternativeTo, Product Hunt, Trustpilot, Reddit |
| Traffic and apps | Similarweb, Sensor Tower / data.ai, App Store and Play charts by country |
| Benchmarks (SaaS, marketplaces) | Bessemer State of the Cloud, KeyBanc/Sapphire SaaS survey, OpenView, ChartMogul, SaaS Capital, Paddle/ProfitWell, a16z marketplace 100, Acquire.com listings (real small-company multiples and margins) |
| Pricing and compensation | Competitors' pricing pages, Levels.fyi, Glassdoor |
| Trends | Google Trends, Exploding Topics, Gartner Hype Cycle summaries, McKinsey/Bain/BCG free insights |
| Academic and legal | Google Scholar, SSRN, regulator sites (FDA, FTC, EU Commission) |

## 8. Competitor research technique

**Find them, widest net first.** Start with category searches in both languages, then "alternatives to
[leader]" and "[leader] vs", then directories: B2B Stack and Capterra BR categories, G2 and Capterra
categories, YC directory, Crunchbase/Dealroom category and "Brazil" filters, Product Hunt, LinkedIn
company search by keyword and country, app-store category charts, Reclame Aqui category rankings, and
for physical products the Mercado Livre / Amazon / Shopee search results sorted by sales. Add the
incumbents that customers use today even if they are not "competitors" (ERPs, WhatsApp, spreadsheets,
a cousin who does it). Stop at 8–12 candidates and profile the 5–7 that matter.

**Capture per competitor** (one row each in `competitors.md`):

| Field | Notes |
|---|---|
| Name, URL, HQ country, founded | — |
| Stage and funding | Amount, date, investors; "bootstrapped" is a data point too |
| Pricing and model | Tiers in original currency and BRL; per seat / usage / take rate / one-off; free tier? |
| Target segment | Who they say they serve vs who reviews say uses them |
| Channels | Self-serve, sales-led, partners (e.g. accountants, franchises), marketplaces, ads, influencers |
| Traction proxies | Headcount and 12-month growth (LinkedIn), open roles, Similarweb visits, app downloads band and rating count, customers claimed, review count |
| Strengths | From their own positioning and from positive reviews |
| Weaknesses | Only from reviews and complaints, with quotes |
| Brazil presence | None / PT-BR site / BRL pricing / Pix-boleto / local entity (CNPJ) / local hiring |
| Threat level 1–5 and why | — |

**Estimate traction and revenue from proxies**, always tagged `[estimate]` with the arithmetic shown:
- Revenue ≈ headcount × revenue-per-employee for the category (look up a benchmark; software
  companies in Brazil run well below US figures), cross-checked with pricing × estimated customers.
- Customers ≈ review count ÷ typical review rate, or app rating count ÷ typical rating rate; use the
  relative ordering between competitors more than the absolute numbers.
- Funding-implied revenue: a round's size and stage bound the ARR investors believed in.
- Brazilian shortcut: the CNPJ record's `porte` (ME / EPP / Demais) and Simples Nacional opt-in cap
  revenue at the respective ceiling; `capital social` hints at seriousness; the CNAE confirms the
  activity. Listed incumbents publish revenue in CVM filings.
- Job postings: sales and customer-success roles signal a GTM push; a "Country Manager Brasil" or
  PT-BR support role at a foreign company signals imminent entry.
- Reclame Aqui complaint volume is a rough customer-base proxy within a category; compare competitors
  against each other, not across categories.

**International players likely to enter Brazil.** Rate each foreign competitor on: PT-BR site or docs,
BRL pricing, Pix/boleto acceptance, a Brazilian legal entity (search "[name] Brasil Ltda" on a CNPJ
lookup), Brazilian hiring on LinkedIn, Brazilian case studies, LatAm expansion news, and recent large
rounds (money looks for new geographies). Also list well-funded Brazilian incumbents in adjacent
categories who could extend horizontally; in Brazil this "platform creep" is a more common killer than
foreign entry.

**Read reviews for unmet needs.** Pull the 1–2★ reviews (why people leave) and the 4★ reviews ("love
it, but…" is where feature gaps live) from G2 "What do you dislike?", Capterra cons, app stores sorted
by most recent and most critical, Reclame Aqui "principais problemas" tags plus response and resolution
rates, and Reddit or PT-BR searches such as "saí do [concorrente]", "[concorrente] cobrança indevida",
"[concorrente] cancelar", "alternativa ao [concorrente]". Count themes, keep 3–5 verbatim quotes per
competitor with dates and URLs, and separate "product gap" themes (opportunity) from "category
inherent" themes (you will have them too).

## 9. Demand-signal techniques

Each signal is weak alone; three independent types together are evidence. Rate each weak / moderate /
strong and say why.

- **Google Trends** (trends.google.com, `geo=BR`, 5 years, then compare against US/world): rising
  interest is why-now evidence; a 2021 spike that decayed is a fad warning; "related queries → rising"
  reveals the vocabulary and adjacent problems. Compare the category term against a competitor name to
  see whether the category or the brand is searched.
- **Keyword volume and CPC**: Google Keyword Planner, Ubersuggest, Semrush or Ahrefs free tiers for
  the PT-BR terms. Volume is demand; CPC is money. Run the core term on google.com.br and count ads:
  paid ads on the query mean someone already makes money from it; zero ads in an "obvious" category is
  a warning that either nobody pays or the channel is not search.
- **Community complaints**: Reclame Aqui and consumidor.gov.br for incumbents; Reddit (r/brasil,
  r/brdev, r/investimentos, niche subs) and international subs; Facebook groups and WhatsApp/Telegram
  group names found via search; Discord servers; Indie Hackers; sector forums (e.g. contabeis.com.br
  for accountants, Jusbrasil for legal pain); YouTube comments under "como fazer [X]" tutorials.
- **Job postings that describe the pain**: LinkedIn Jobs, Gupy, Indeed BR, Catho for "[role] responsável
  por [manual task]". Companies paying a salary for a person to do X manually have a budget for X; the
  salary is a willingness-to-pay anchor.
- **Existing workarounds**: searches for "planilha de [X] grátis", "modelo [X] Excel", YouTube view
  counts on "como controlar [X] no Excel", Google Forms and Notion templates, WhatsApp-based processes.
  Heavy workaround usage is demand; it is also the incumbent you must beat (free and familiar).
- **People already paying for an inferior solution**: paid spreadsheets and courses on Hotmart or
  Mercado Livre, consultants and freelancers on Workana/99Freelas/GetNinjas (and Upwork/Fiverr
  internationally), agencies, "sistema caseiro" anecdotes. Log the prices: they are the real price anchor.
- **Adjacent-market pull**: foreign products with Brazilian users complaining about no PT-BR, no Pix,
  USD pricing or no nota fiscal — a localisation gap is a demand signal.

Record for every signal: the quote or number, URL, date, and whether it is about the problem (good),
about a competitor (better), or about people paying (best).

## 10. Research hygiene

- Tag every number: `[data]` quoted from a tier 1–3 source as published; `[benchmark]` an industry
  range from a report or from the skill's references; `[estimate]` derived by stated arithmetic from
  data; `[guess]` no data, informed judgement. Add confidence H/M/L, source ID,
  URL, date accessed, data year, geography, and currency. A number without a tag is not allowed into
  the model.
- When sources conflict, present the range, say which you trust and why (tier, recency, definition
  match), and carry the range forward rather than picking the flattering end.
- Never invent a number or a URL. If nothing is found after the minimum searches, write "not found",
  then estimate bottom-up with explicit assumptions and tag the result `[estimate]` or `[guess]`. Only
  cite URLs that a search returned or you fetched; mark `[snippet]` when you did not open the page.
- Fetch the page for any number that matters to the verdict; snippets truncate and drop caveats. When
  a site blocks fetching (LinkedIn, Similarweb, Crunchbase often do), keep the snippet and say so.
- Save incrementally: append to `ideas/<slug>/research/<dimension>.md` after every 3–5 searches, and
  write the dimension's contract block the moment it is done. Context can run out mid-job; files do not.
- Keep `ideas/<slug>/sources.md` (dossier root, so readers find it) as a numbered bibliography:
  `[S12] Title — Publisher, data year — URL — accessed YYYY-MM-DD — tier`. Reference IDs from the
  dimension files. Subagents return their own lists; the parent merges, dedupes by URL and renumbers.
- Log search counts per dimension and the queries that returned nothing; empty results are evidence of
  a thin market or the wrong vocabulary, and the next phase needs to know which.
- Keep currency and time consistent: BRL for Brazil, USD for international, stated FX rate and date
  for conversions, nominal year noted; age old figures explicitly.
- Separate what the source says from what you infer; put inference in a "Reading" line under the fact.

## 11. Research output contract

Every dimension ends with this block at the top of its file and copied into `research/summary.md`.
The financial model and the verdict read only these blocks and the model-inputs table, so a finding
that is not in the block does not exist for them.

```markdown
## Contract: <dimension>   (status: complete | partial | not-found)
headline: one sentence with the key number or finding
key_numbers:
  - name: <what> | value: <n> | unit: <R$ / US$ / count / %> | geo: BR|global|<country> | year: <yyyy> | tag: [data|estimate|guess] | conf: H|M|L | src: [Sx]
findings:            # 3–6 bullets, each ending with a tag and [Sx]
range_and_conflicts: # "A says X [S3], B says Y [S7]; trust A because …"
model_inputs:        # variables this dimension feeds (names from the table below)
gaps:                # what was not found + the assumption used instead
searches_run: <n>    # plus the queries that returned nothing
```

Consolidated `model_inputs` table in `summary.md`, one row per variable, with value or range, unit,
tag, confidence, source IDs and the consumer:

| Variable | Fed by | Consumed by |
|---|---|---|
| `n_target_total` (count of target customers/users, BR) and `n_target_intl` | a, d | TAM |
| `sam_filters` (geographic, product-fit, readiness %, each with rationale) | a, b, d | SAM |
| `market_growth_pct` | a, g | Scenarios |
| `price_anchor_low / median / high` (BRL) and `dominant_model` | e, b | ARPU, SOM |
| `arpu_pess / real / opt` | e, d | Revenue, break-even |
| `gross_margin_benchmark_pct` | e, h | Unit economics |
| `payment_fee_pct`, `platform_take_pct` | h | Unit economics |
| `tax_regime` and `effective_tax_pct` | f, h | Unit economics, cost-to-run |
| `cac_range_by_channel`, `cpc_cpm_core_terms`, `conversion_benchmarks` | i, c | CAC, break-even, scenarios |
| `churn_monthly_range` or `retention_benchmark` | e, b, j | LTV, scenarios |
| `fixed_costs_monthly` (loaded salaries CLT/PJ, cloud, tools, accounting, legal, office) | h | Cost-to-run, break-even |
| `variable_cost_per_unit` (COGS, support, API/LLM, logistics) | h | Unit economics |
| `one_off_costs` (licences, certification, entity, compliance) and `time_to_market_months` | f | Cost-to-run, scenarios |
| `competitor_table` with threat levels and `positioning_gaps` | b | Verdict |
| `demand_strength` (weak/moderate/strong per signal type) with quotes | c | Verdict |
| `analogues` (name, country, outcome, cause) | j | Verdict, scenarios |
| `why_now_drivers` and `headwinds` | g | Verdict |
| `kill_risks` (regulatory or legal showstoppers, platform dependence, single-channel risk) | f, b, i | Verdict |

A dimension may leave a variable empty only with a `gaps` entry explaining the assumption that will be
used instead. The verdict phase treats a `[guess]` on `n_target_total`, `price_anchor` or `cac_range`
as a reason to lower the confidence of the whole analysis, so spend the extra searches there first.
