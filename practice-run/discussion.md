# discussion.md — "discuss first, generate after"

Lecture 10 (p.31–33) says: before creating any file, the AI should interview me,
summarize my needs, wait for my confirmation, and only then write `AGENTS.md`
and the folders. This file is the record of that step.

## 1. The interview (2026-11-23)

The AI asked these questions before generating anything. Lecture 10 p.32 lists what
it should ask: readers, contradictions, language, citation detail, ingest mode,
outputs, lint checks and page types.

| # | Question | My answer |
|---|---|---|
| 1 | Who reads the wiki and the slide deck? | **CS students** who know code but not AI agents, loops or graphs |
| 2 | What language? | **English**; key course terms can keep the Chinese in brackets |
| 3 | How detailed should citations be? | **Source + slide number**, e.g. `[L10 p.21]`, checkable by a script |
| 4 | What if two sources disagree? | **Show both and flag it** in a "Disagreements" section; never pick one silently |
| 5 | Topic? | **AI Agents**: what they are, the design patterns, and how loops/graphs make them reliable |
| 6 | What sources? | 5 course PDFs: Lectures 07, 08, 09, 10 and the Week 7 TA session |
| 7 | Ingest one at a time or in a batch? | One at a time, in lecture order, so later sources can reuse concepts |
| 8 | What will the wiki be used to produce? | A teaching HTML slide deck, "What is an AI Agent?" |
| 9 | What should lint check? | Every claim has a citation, citations point to real pages, no orphan concept pages, no broken `[[links]]` |
| 10 | Page types? | `sources/` (one summary per source) and `concepts/` (one page per idea) |

## 2. Requirement summary (written by the AI, then confirmed)

- Build an LLM Wiki on **AI Agents** from 5 course sources, in English, for CS students.
- Every factual line in the wiki ends with a citation `[SOURCE p.N]`.
- Disagreements are kept side by side and flagged.
- The wiki is the **only** knowledge source for the slide deck.
- The deck is made by a workflow graph whose checks are **scripts** (Lecture 10 p.14:
  "done" is decided by the script, not by the AI saying so).
- PDFs and extracted text are **not** committed (course material); only the list of sources is.

**Confirmed by me (Angelie) before generation.** → `AGENTS.md` was written from this summary.

## 3. Check: does AGENTS.md contain everything in the summary? (Lecture 10 p.33)

| Summary item | Where in AGENTS.md |
|---|---|
| Topic, audience, language | §1 |
| Citation format | §4 |
| Disagreements | §4, §5 |
| Wiki is the only source for slides | §7 |
| Checks are scripts | §7, §8 |
| PDFs not committed | §9 |
