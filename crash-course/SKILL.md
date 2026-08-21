---
name: crash-course
description: Write a crash course — a study document, like a short documentary — about a concept, either one registered as debt in `.learning/DEBT.md` (e.g. "/crash-course DEBT-007") or any topic the user names ("/crash-course event sourcing", "explain properly what this backoff you added actually is", "make me study material on this", "I want to really understand what's going on in this module", "explain this to my co-founder who doesn't code"). Covers history, who created it, ELI5, how it works, how it is used in THIS project, trade-offs, alternatives, references. Use whenever the user wants to *study* or *deeply understand* something, not just get a quick answer. Saves to `.learning/crash-courses/`.
---

# Crash course

The user asked for study material, not an answer. The output is a document someone reads in 10-20 minutes to go from "I don't know what this is" to "I could explain it and argue about its trade-offs". The audience ranges from a non-technical person to a senior dev, so the document is ordered by **increasing depth**: a non-technical reader stops at section 3, a junior dev at section 6, a senior reads to the end. Nobody needs to skip around.

Output lives in `.learning/crash-courses/<slug>.md`, a personal gitignored folder (create `.learning/` and the `.gitignore` entry if missing, same as the `debt` skill does).

## 1. Resolve what to teach

Ask only what the project cannot answer. One question per round, `AskUserQuestion`, never a questionnaire. After two rounds still ambiguous → generate with the most likely reading, stated in the header.

| Input | What you do |
|---|---|
| No argument | Read `.learning/DEBT.md`; offer open entries (id + concept) as options, plus "another topic". |
| `DEBT-NNN` | Load the entry. Concept, location, usages and rationale are already there — use them, do not re-investigate unless the entry looks stale (file moved, symbol gone). |
| Free text | `rg` the project first. One clear match → confirm in a line and go. Two or more plausible matches (e.g. "cache" → Redis client, `useMemo` sprinkled around, HTTP headers) → offer them with file + one line of context so the user can pick without knowing the technical name. Zero matches → generic topic; sections 3 and 6 become N/A and you say so before writing. |

**Audience**: infer when you can. Coming from a `cog` debt a dev registered → dev. "For my co-founder", "for someone who doesn't code" → non-technical. Otherwise one question: "for you, or for someone who doesn't code?". Audience changes how heavy section 6 is and how much jargon survives sections 1-5; it does not change the structure.

## 2. Research before writing

- Read the project code involved (definition + call sites). Section 6 annotates *real* lines, never a generic example, whenever the topic exists in the project.
- Verify history and attribution (who, when, where it came from). Use web search when available; if you cannot verify a claim, drop it or mark it "unverified". A wrong origin story is worse than a short one.
- References must be real, checked URLs or canonical works (paper, RFC, official doc, the widely cited blog post). No made-up links.

## 3. Structure

Fixed: same ten sections, same order, always. A section with little relevant content becomes one line — it never disappears and is never padded. The reader must always know where they are. Use `assets/template.md`.

1. **In one sentence** — the whole idea, no jargon.
2. **Real-world analogy** — one concrete analogy, carried through the rest of the document when it helps.
3. **Why this exists in YOUR project** — where, who calls it, the actual problem it solves here, what would break without it. Comes *before* history because the motivation to study is "what is this doing in my code"; history without that anchor reads like Wikipedia.
4. **History** — when, who, what problem they were solving. Short and verified.
5. **How it works, step by step** — numbered ELI5: concrete actors (client, server, queue), observable actions, explicit causation (`→`). Translate each technical term the first time it appears.
6. **Reading the project code** — the real excerpt, annotated. Magic numbers explained, or marked "choice without documented rationale" (pull this from the debt entry when there is one).
7. **Trade-offs** — what you pay for what you get; where it bites in this project specifically.
8. **Alternatives not used** — two to four, each with one line on when it would be the better choice.
9. **Self-test questions** — three to five questions. Answering them all is the objective criterion that a cognitive debt is paid. Make them about this project's code when possible, not trivia.
10. **References** — verified.

Header carries: source (`DEBT-NNN` or "free topic"), files, date, estimated reading time, prerequisites, intended audience.

## 4. Close the loop

When the course came from a debt entry, set its `**Crash course:**` field to the file path. Do not mark the debt as paid — reading and answering section 9 is the user's job.

## Tone

Plain, concrete, no filler, no cheerleading. Explain why, not just what. Assume the reader is smart and busy, not an expert. ELI5 means short sentences and concrete actors, not condescension.
