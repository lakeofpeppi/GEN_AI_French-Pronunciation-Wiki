# discussion.md ; "discuss first, generate after"

Lecture 10 (p.31–33): before creating any file, the AI interviews me, summarizes my needs,
and only builds after I confirm. This is the record of that step for this wiki.

## 1. The interview (2026-11-23)

| # | Question (Lecture 10 p.32 checklist) | My answer |
|---|---|---|
| 1 | Topic? | **Learning French**: I'm learning it myself, from English |
| 2 | Which slice of it? ("learning French" is too big for one deck) | **Pronunciation basics** |
| 3 | Who reads the deck? | **Total beginners**: English speakers who know zero French |
| 4 | Language? | **English explanations + French example words** |
| 5 | How to show sounds? | **Both**: simple English respelling on the slide, IPA in small print, and a 🔊 button to hear each word |
| 6 | How detailed are citations? | **Source ID + section**, e.g. `[S3 §Nasal vowels]` |
| 7 | If sources disagree? | **Show both and flag it** under "Disagreements"; never pick one silently |
| 8 | Sources? | The AI proposes, I approve and save them as PDFs: 6 sources (S1–S6, see `raw/sources.md`) |
| 9 | Ingest mode? | One at a time, so later sources can add to existing concept pages |
| 10 | What should lint check? | Citations point to a real section, every key point has a verbatim quote that is really in the source, no broken links, no orphan pages |

## 2. Requirement summary (written by the AI, confirmed by me)

- LLM Wiki on **French pronunciation basics**, English, for total beginners.
- 6 sources, ingested one at a time; PDFs stay local (`raw/` is never committed except `sources.md`).
- Every key point ends with `[S# §Section] «short verbatim quote»`.
- Disagreements kept side by side and flagged.
- The wiki is the **only** knowledge source for the deck; the deck is built by the graph in
  `.agents/workflows/topic-slides.md`, with scripts as gates.
- Deck shows respelling + IPA + 🔊 audio for example words.

**Confirmed by me (Angelie).** → `AGENTS.md` was written from this summary.

## 3. What I learned from the practice run, applied here

Before choosing French I started a practice run on "AI Agents" (kept in `practice-run/`).
Its evidence-card node failed most: 6 of 31 quotes weren't found in the source text, and it
only passed on round 3 of 3. The problem started at **ingest**, long before cards were made.
So in this wiki the quote check runs **at ingest** (lint), not only at the card gate.
