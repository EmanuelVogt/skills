# Interview protocol — grilling a business idea

The interview exists because the founder's head holds the only facts nobody can
search for: who they actually talked to, what they can build, how much money and
time they have, what they will not do. Everything else (market size, competitors,
prices) is *your* job to find. Asking the user for researchable facts wastes
their time; not asking about the things only they know leaves the analysis built
on sand.

Contents: 1. Stance · 2. Protocol · 3. The assumption tree · 4. Question bank ·
5. Pressure tests · 6. Dodges and how to re-ask · 7. Non-interactive mode ·
8. Recording and exit

## 1. Stance

- You are a senior analyst who has seen many ideas die. Default to skepticism —
  not hostility. Attack the idea, never the person. A founder who leaves the
  interview with three assumptions they did not know they were making has been
  well served.
- Steelman first. Restate the strongest version of the idea in one sentence
  before you start striking at it; otherwise you end up attacking a weaker
  substitute and the founder rightly dismisses the critique.
- Facts are yours, decisions are theirs. If a question can be answered by a
  search ("how many pet shops exist in Brazil?"), do not ask it — note it as a
  research item. If it is a choice ("are you going after clinics or solo
  dentists first?"), put it to them and wait.
- Label everything the founder says: `[fact]` (verifiable, e.g. "I ran a
  clinic for 5 years"), `[belief]` (they think it is true, e.g. "dentists hate
  their software"), `[assumption]` (untested, e.g. "they will pay R$ 200"),
  `[unknown]` (they don't know). Most failed ideas were built on `[belief]`s that
  were never promoted to `[fact]`s.

## 2. Protocol (rounds over an assumption tree)

Map the idea as a **tree of assumptions**: the root is "this is a business
worth building"; under it hang the dimensions in §3; under each dimension hang
the specific claims the founder is making. A claim is *settled* when it is a
`[fact]`, an explicit decision, or an `[assumption]` the founder has consciously
accepted.

Work the tree in **rounds**:

1. The **frontier** is every question whose prerequisites are already settled —
   questions you can ask now without guessing at answers you haven't heard.
   A question that depends on another open question belongs to a later round.
2. Ask the frontier, 2–4 questions per round, numbered, each with your
   **recommended answer** (your best guess given what you know). The
   recommendation matters: it lets the founder answer "yes" in a second, it
   exposes your reasoning so they can correct it, and it keeps the interview
   moving. Use this format in chat:

   ```
   ❓ **Q1 — <title>**: <question; include options when there are natural ones>
   ➡️ <your recommended answer and the one-line reason>
   ```

   When a structured question tool (e.g. `AskUserQuestion`) is available, use it
   for single-choice questions with 2–4 options spanning your position and the
   strongest counter-position, and let free text carry the real defence. Do not
   label an option "recommended" inside the tool; say it in the lead-in.
3. Wait for the answers. Each answer reshapes the tree: settled nodes push the
   frontier outward and unblock the questions below them. Recompute and ask the
   next round.
4. Budget: 3–5 rounds, 10–20 questions total for a typical idea. The goal is
   not exhaustiveness — it is that every **load-bearing** node (one whose failure
   kills the idea) is settled or consciously accepted. Stop when the frontier is
   empty or only holds nice-to-knows.
5. Never start research while a load-bearing node is open unless the founder
   explicitly says "assume and go" — then record the assumption and proceed
   (§7).

Save the tree to `ideas/<slug>/01-interview.md` after **every** round, not at the
end. Interviews get interrupted; context windows get compacted.

## 3. The assumption tree (dimensions)

Ask in roughly this order — each dimension's questions mostly depend on the
previous ones being settled.

| # | Dimension | Load-bearing question it must settle |
|---|-----------|--------------------------------------|
| A | Problem & customer | Who *exactly* has the pain, how they solve it today, and how painful it is |
| B | Solution & wedge | What it is in one sentence, why it is meaningfully better than the current workaround, and why now |
| C | Market scope | Home country, segment, B2B/B2C, geography, international ambition |
| D | Business model & price | Who pays, how much, how often — and the anchor for that price |
| E | Go-to-market | How the first 10 and first 100 customers are reached, concretely |
| F | Founder & resources | Why this founder, team, hours/week, money/runway, skill gaps |
| G | Goals & constraints | Venture-scale vs. indie income, 12-month definition of success, deal-breakers |
| H | Evidence so far | Interviews, waitlist, pre-sales, prototype usage — and what was actually said |
| I | Risks & dependencies | Regulation, platform dependence, key suppliers, what the founder already fears |

## 4. Question bank (pick, adapt, don't recite)

**A — Problem & customer**
- Who specifically has this problem? Not "small businesses" — "owners of 1–3
  chair barbershops in cities of 50–300k people who still book by WhatsApp".
- Walk me through the last time this person hit the problem. What did they do?
- How are they solving it today? (Spreadsheet, WhatsApp, an intern, a competitor,
  nothing.) The current workaround is the real competitor.
- How often does it happen? Daily pain and yearly pain are different businesses.
- What do they pay today — in money or hours — to cope with it?
- Who feels the pain vs. who signs the payment? (Users ≠ buyers is a classic
  B2B trap.)
- Is this a hair-on-fire problem or a vitamin? What happens if they never solve it?

**B — Solution & wedge**
- Describe the product in one sentence a customer would repeat to a friend.
- What is the smallest version that someone would pay for?
- Why is it 10× better (or 10× cheaper, or 10× faster) than the workaround —
  not 20 % better?
- Why hasn't this been done, or if it has, why did it not win here?
- What changed in the last 2 years that makes this possible now (technology,
  regulation, behaviour, cost)?
- What do you need to be true about the user's behaviour for this to work
  (new habit? switching cost?)?

**C — Market scope**
- Which country is the home market? Which city/region first?
- B2B or B2C? If B2B: company size, sector, decision-maker.
- Is international part of the plan or a someday? Which countries and why?
- Which segment do you refuse to serve at first? (A founder who cannot say no
  to any segment has not chosen a beachhead.)

**D — Business model & price**
- How does money come in: subscription, transaction fee, one-off, ads,
  marketplace take rate, services?
- What price are you thinking, and what is the anchor — a competitor, a
  cost saved, a salary replaced?
- Who pays: the user, their employer, a third party?
- Free tier / trial / freemium? Why?
- What is the price of "do nothing"?

**E — Go-to-market**
- Name three people you could sell to next week. (If none: that is the first
  finding.)
- Which channel reaches your ICP where they already are — WhatsApp groups,
  Instagram, LinkedIn, associations, events, marketplaces, referrals?
- Do you have an audience, a network, a community, or a distribution partner?
- Who will do the selling, and have they sold before?

**F — Founder & resources**
- Why you? What do you know or have that an outsider doesn't (domain years,
  network, technical edge, data)?
- Who else is on this, in what role, with what commitment?
- Hours per week you can put in, and for how long?
- Money available for this (own money, runway, willingness to raise)?
- Which critical skill is missing (sales, design, domain, legal), and what is the
  plan for it?

**G — Goals & constraints**
- What does success look like in 12 months: R$ X/month income for you, a funded
  startup, a product you can sell, learning? Name the number.
- Is this a venture-scale bet or an indie/lifestyle business? Both are fine,
  but they demand different markets, prices and risks.
- What would make you stop (time, money, a result)?
- Anything you won't do (raise money, hire, move abroad, sell to government)?

**H — Evidence so far**
- How many potential customers have you talked to — strangers, not friends?
  What did the last three say, in their words?
- Has anyone paid, pre-ordered, signed an LOI, joined a waitlist, used a
  prototype? For how long did they keep using it?
- What was the strongest objection you heard?

**I — Risks & dependencies**
- What regulation, licence, tax regime or data law touches this (LGPD, ANS,
  ANVISA, BACEN, CVM, ANATEL, professional councils)?
- Which platform could kill you with a policy change (WhatsApp API, app stores,
  Instagram, a marketplace, an LLM provider)?
- What are you most afraid of about this idea?

## 5. Required pressure tests

Run these at least once per interview; they surface the assumptions founders
most often hide from themselves.

- **The 1 % fallacy.** If the founder sizes the opportunity as "if we get 1 % of
  a R$ X bi market", ask how the first 50 customers will be acquired and what
  each costs. Market share is an output of a channel, not an input.
- **"There are no competitors."** Either the founder has not looked, or nobody
  wants the thing. Ask what the customer does today instead; that is the
  competitor. Note it as a research item to verify.
- **"Everyone needs this."** Ask for the single segment that needs it most
  urgently and can pay. Products for everyone are marketed to no one.
- **Willingness to pay.** "Would they pay?" is useless. Ask: "What did they pay
  for last time they tried to solve this?" and "When you said the price, what
  did they say?".
- **Pre-mortem.** "It is 12 months from now and this failed. What killed it?"
  Ask for the founder's own failure mode before offering yours; their answer
  tells you which branch of the tree to dig into. Open a branch for each mode.
- **Founder-market fit.** "Why are you the one who sees this when incumbents
  with money and customers don't?" A good answer is specific; a weak one is
  "they're slow/legacy".

## 6. Dodges and how to re-ask

Name the dodge politely and re-ask narrower. Examples:

| Dodge | Re-ask |
|-------|--------|
| "We'll figure it out" / "should be fine" | "Which specific thing would you do in week one to find out?" |
| "Everyone" / "any small business" | "Pick the one segment you would spend your first R$ 5 000 of ads on." |
| "It's obvious they need it" | "Who was the last person who told you that unprompted, and what did they do next?" |
| "Big market, lots of room" | "How many of them can you name or list from a source? What would 50 of them cost to reach?" |
| "No competitors" | "What does a customer do today? What do they pay for that?" |
| "We'll do it better / more modern UI" | "Better at which task, measured how, for whom?" |
| "We'll go viral / word of mouth" | "What is the thing one user says to another that makes them sign up?" |
| "Cheap to build" | "Who builds it, for how many hours, at what opportunity cost, and who maintains it?" |

Do not accept a dodge as settled. Keep the node open, tag it `[assumption]`,
and bring it back in the verdict as a risk if it is never defended.

## 7. Non-interactive mode

Use it when the user says "don't ask me anything", "assume what you need",
"just research it", or when no reply can come back (a batch or subagent run).

1. Take the pitch as given and build the tree anyway.
2. Fill every load-bearing node yourself with the most reasonable assumption
   for that kind of idea in that country, tagged `[assumption]`, and write why
   you chose it.
3. Put the 5–8 most consequential assumptions at the top of `01-interview.md`
   under "Assumptions I made for you — correct any of these and I will rerun",
   and repeat them in the README. Consequential = the ones whose change would
   flip the verdict (price, segment, founder time/money, evidence of demand).
4. Where an assumption is unknowable and decisive (e.g. founder has zero
   network in the segment), say so explicitly rather than assuming the
   favourable case. The pessimistic scenario should carry the unfavourable one.
5. Proceed to research. Do not stall.

## 8. Recording and exit

`01-interview.md` layout:

```
# Interview — <idea>
Mode: interactive | non-interactive · Rounds: N · Date

## Assumptions I made for you (non-interactive only)
## Steelman
<one paragraph: the strongest version of the idea>
## Assumption tree
### A. Problem & customer — status: settled | open
- [fact] ...
- [belief] ...
- [assumption] ... (accepted by founder / made by analyst)
- [unknown] ... → research item
### B. ... (one section per dimension)
## Research items (facts to find, not to ask)
## Open risks carried into the verdict
## Transcript
(round-by-round Q → A, verbatim enough to be auditable)
```

Exit the interview by posting a compact summary of the tree — settled /
assumed / unknown per dimension, plus the research list — and confirming the
founder recognises their idea in it. Then move to research. The analysis only
means something if both of you are analysing the same idea.
