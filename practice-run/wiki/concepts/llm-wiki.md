# LLM Wiki

**One line:** a personal Wikipedia that an LLM writes and maintains from your sources.

## Explanation
Instead of searching raw documents every time (RAG), the LLM reads each source once and
"compiles" it into linked Markdown pages: summaries and concept pages. You collect sources;
the LLM writes and updates the pages; both of you edit the rules.

## Key points
- The LLM compiles raw sources into a set of .md pages with summaries and backlinks [L07 p.39]
- With ~100 articles, an index plus short summaries was enough for Q&A without complex RAG [L07 p.41]
- The LLM runs "lint" health checks to find inconsistencies and missing data [L07 p.43]
- Three layers: raw/ (read-only sources), wiki/ (AI-written pages), schema (the rules file) [TA07 p.5]
- Three actions: ingest, query, lint; one ingest can touch 10–15 pages [TA07 p.6]
- index.md is the catalog the AI reads to find pages; log.md is the dated history [TA07 p.7]
- Build it "discuss first": the AI interviews you (~8–10 questions), summarizes, and only creates files after you confirm [L10 p.31]
- The interview should cover readers, contradictions, language, citations, ingest mode, outputs, lint, page types [L10 p.32]

## Example
`raw/` (PDFs) → `wiki/` (pages like this one) → rules file telling the AI how to write them.

## Related
[[rag]] · [[context-engineering]] · [[rules-file]]
