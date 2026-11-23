# TA07 — 第七週助教課 (Week 7 TA session: the LLM Wiki in practice)

## What it covers
A hands-on walkthrough of Karpathy's LLM Wiki: the three layers, the three actions,
the two key files, and how good rules are grown from real mistakes.

## Key points
- Three layers: raw/ (sources, read-only), wiki/ (pages the AI writes and links), schema (rules file you and the AI revise) [TA07 p.5]
- Three actions: ingest (one source can update 10–15 pages), query, and lint [TA07 p.6]
- Two key files: index.md (catalog, one line per page) and log.md (dated history of actions) [TA07 p.7]
- Tools that read rules automatically: Claude Code reads CLAUDE.md, Codex/Cursor read AGENTS.md [TA07 p.8]
- Good rules come from real problems, e.g. inconsistent pages → one fixed template per page type [TA07 p.14]

## Concepts it feeds
[[llm-wiki]] · [[rules-file]]
