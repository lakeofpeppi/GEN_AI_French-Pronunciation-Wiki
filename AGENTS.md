# AGENTS.md — French Pronunciation LLM Wiki + teaching deck

Read this whole file before doing anything. Written from `discussion.md` (the interview).
Kept short on purpose (Lecture 10 p.34: rule files have size limits); the step-by-step
deck workflow lives in `.agents/workflows/topic-slides.md`.

## 1. What this project is

- An **LLM Wiki** (Karpathy pattern: raw → wiki → rules) on **French pronunciation basics**.
- Readers: **total beginners**, English speakers who know zero French.
- Language: **English** explanations, **French** example words.
- Output: a **teaching HTML deck** built only from the wiki, showing every example word with
  an English-style respelling, IPA in small print, and a 🔊 button.

## 2. Folders

```
raw/sources.md        the 6 sources (S1–S6); PDFs + raw/text/ stay local, never committed
raw/text/S#/full.txt  extracted text of each source (what quotes are checked against)
wiki/index.md         catalog, one line per page (read this FIRST)
wiki/log.md           every ingest / lint / query, newest at the bottom
wiki/sources/         one summary page per source
wiki/concepts/        one page per pronunciation idea
.agents/workflows/    the deck graph (topic-slides.md)
pipeline/             check scripts: check.py (python), render_check.js (node)
topic-pronunciation/  one deck run: retrieval, cards, outline, drafts, deck, report
practice-run/         the earlier AI Agents practice run (kept for the reflection)
```

## 3. Naming

Lowercase, hyphens, no spaces: `wiki/concepts/nasal-vowels.md`. Wiki links: `[[nasal-vowels]]`.

## 4. Citations and quotes (from the interview)

Every key point ends with a citation **and** a short verbatim quote from that section:

```
- Many speakers merge un and in. [S1 §Oral and nasal vowels] «Many speakers merge the last two sounds»
```

- The section name must exist in the source; the quote must be **copied** from the source text
  (`raw/text/S#/full.txt`), at least 6 characters. Never type a quote from memory.
- Quote **prose only, never tables**: PDF text splits table columns apart.
- Copy section names exactly as written (curly quotes are treated as straight by the checker).
- If sources disagree: keep both, each cited, under **Disagreements**.

## 5. Page templates

**Source page**: title · what it covers · key points (cited + quoted) · concepts it feeds.
**Concept page**: one-line definition · explanation for beginners (3–6 sentences) ·
key points (cited + quoted) · examples (`word` ≈ respelling /IPA/) · related · disagreements.

## 6. Ingest (one source at a time)

1. Read `wiki/index.md`.
2. Write the source page.
3. For each idea: concept exists → **add** points (don't rewrite); missing → create it.
   Only link pages already in `wiki/index.md`; only cite sources already ingested.
4. Update `wiki/index.md`; add a line to `wiki/log.md`:
   `YYYY-MM-DD | ingest | S# | +N concepts, ~M updated`.
5. Run `python3 pipeline/check.py wiki`. Fix until it passes, and log any failure.

## 7. Making a deck

- Follow `.agents/workflows/topic-slides.md` node by node.
- The wiki is the **only** source. If something's missing, stop and ingest more.
- A node is done only when its **script** passes.

## 8. Stop rules (Lecture 10 p.23)

- Max **3 rounds** per loop, then stop and report.
- Fewer than **3** relevant wiki pages → stop before drafting.
- Each round fixes **only** what the check report lists.

## 9. Never

- Never commit PDFs or `raw/text/`. Never edit `raw/`.
- Never change a slide's words in the render node (layout only).
- Never let the conversation that wrote the deck be its only reviewer.

## 10. Code comments (my learning style)

Put a short comment on every complicated line so I can learn from it later.
All lowercase, casual human words, like notes to myself:

```python
failed.append(slide_id)   # this to flag the node so we only redo this slide
state["last"] = node      # remember to mark the recent node
```

No comments on obvious lines, no capital letters, no formal "This function..." style.

## 11. Rule change log

- 2026-11-23 — carried over from the practice run (AI Agents):
  - lint failed twice for linking/citing sources before they were ingested → §6 step 3.
  - the card gate failed 6/31 quotes, passing only on round 3 → quotes now stored and
    checked **at ingest** (§4), so the check sits next to the source.
  - a fix shortened a quote to 2 characters to pass → quotes must be ≥ 6 characters (§4).
- 2026-11-23 — first version for French, from `discussion.md`.
- 2026-11-23 — S2 lint: 10 section names failed only because of curly vs straight quotes →
  checker now ignores quote style (formatting, not evidence); 2 quotes came from a table
  the PDF scrambles → new rule: quote prose, never tables (§4).
- 2026-11-23 — deck run: the card node silently copied only 1 of N points per page and G2
  still passed (it checked quotes, not completeness) → G2 now counts items vs the wiki;
  and every gate is tested once on planted errors before its PASS is trusted.
- 2026-11-23 — 🔊 test: G5 counted buttons but never pressed one; with no French voice the
  button was silent with no warning → G5 now clicks 🔊 and fails on a silent button.
  Scripts can't judge how a word *sounds*, so the human check (H) now means look **and listen**.
