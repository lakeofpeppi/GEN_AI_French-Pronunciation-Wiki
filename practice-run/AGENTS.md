# AGENTS.md — AI Agents LLM Wiki + teaching deck

Read this whole file before doing anything. Written from `discussion.md` (the interview).
Kept short on purpose: Lecture 10 p.34 warns rule files have size limits, so
the step-by-step slide workflow lives in `.agents/workflows/topic-slides.md`.

## 1. What this project is

- An **LLM Wiki** (Karpathy pattern: raw → wiki → rules) about **AI Agents**.
- Readers: **CS students** who can read code but don't know agents, loops or graphs.
- Language: **English**. Keep a Chinese course term in brackets the first time if useful.
- Output: a **teaching HTML slide deck** built only from the wiki.

## 2. Folders

```
raw/sources.md        list of the 5 source PDFs (read-only, I collect them)
raw/text/             extracted page text, ONE FILE PER SLIDE (git-ignored, never commit)
wiki/index.md         catalog: one line per page (read this FIRST)
wiki/log.md           every ingest / query / lint, newest at the bottom
wiki/sources/         one summary page per source
wiki/concepts/        one page per idea
.agents/workflows/    the slide-deck graph (topic-slides.md)
pipeline/             check scripts (python + node)
topic-ai-agents/      one deck run: retrieval, cards, outline, drafts, deck, report
discussion.md         the interview that produced this file
```

## 3. Naming

Lowercase, hyphens, no spaces: `wiki/concepts/tool-use.md`, `wiki/sources/l10-loop-graph.md`.
Links inside the wiki use `[[concept-name]]` (file name without `.md`).

## 4. Citations (from the interview)

- Every factual bullet or sentence ends with `[SOURCE p.N]`, e.g. `[L10 p.21]`.
- SOURCE is one of `L07 L08 L09 L10 TA07`; N is the PDF page number.
- Never cite a page you didn't read. Never invent numbers or quotes.
- If two sources disagree: keep both, each with its citation, under **Disagreements**.

## 5. Page templates

**Source page** (`wiki/sources/`): Title · What it covers (2–3 lines) · Key points
(cited bullets) · Concepts it feeds (`[[links]]`).

**Concept page** (`wiki/concepts/`): One-line definition · Explanation for CS students
(3–6 sentences) · Key points (cited) · Example (code or analogy) · Related (`[[links]]`) ·
Disagreements (only if any).

## 6. Ingest (one source at a time)

1. Read `wiki/index.md`.
2. Write the source page.
3. For each idea: concept exists → **add** cited points (don't rewrite); missing → create it.
   Only link `[[pages]]` listed in `wiki/index.md` and only cite sources already ingested.
   Ideas from a later source wait until that source is ingested.
4. Update `wiki/index.md` and add one line to `wiki/log.md`:
   `YYYY-MM-DD | ingest | <source> | +N concepts, ~M updated`.
5. Run `python3 pipeline/check.py wiki` (lint). Fix until it passes.

## 7. Making a deck

- Follow `.agents/workflows/topic-slides.md` node by node.
- The wiki is the **only** knowledge source. If something isn't in the wiki, stop and
  ingest more; don't fill gaps from memory.
- A node is done only when its **script** passes ("check it" said by the AI doesn't count).

## 8. Stop rules (Lecture 10 p.23)

- Max **3 rounds** for any loop, then stop and report.
- Fewer than **3** relevant wiki pages for a topic → stop before drafting.
- Each round fixes **only** what the check report lists.

## 9. Never

- Never commit PDFs or `raw/text/` (course material).
- Never edit `raw/`.
- Never change a slide's words in the render node (layout only).
- Never let the same conversation that wrote the deck be its only reviewer.

## 10. Code comments (my learning style)

Put a short comment on every complicated line so I can learn from it later.
All lowercase, casual human words, like notes to myself:

```python
failed.append(slide_id)   # this to flag the node so we only redo this slide
state["last"] = node      # remember to mark the recent node
```

No comments on obvious lines, no capital letters, no formal "This function..." style.

## 11. Rule change log

- 2026-11-23 — first version, from `discussion.md`.
- 2026-11-23 — lint failed twice the same way (L07 and L09 ingests linked to pages from a
  later lecture; L09 also cited L10 before it was ingested) → §6 step 3 rule + lint now
  rejects citations to sources not yet ingested.
