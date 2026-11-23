# L07 — 讓AI看懂你的世界 (Making AI understand your world)

## What it covers
How to give an LLM the right information: context engineering, RAG (retrieval with
embeddings), memory, and Karpathy's LLM Wiki as an alternative way to organize knowledge.

## Key points
- RAG is presented as a method to reduce LLM errors [L07 p.3]
- Good prompting is really about giving correct information plus clear instructions ("content engineering") [L07 p.5]
- Classic RAG splits documents into fixed-size chunks (e.g. 500 characters with 50 overlapping) [L07 p.11]
- Each chunk can carry metadata such as source, page, title, author and date [L07 p.15]
- An embedding model turns the question and each chunk into vectors; the closest chunks are retrieved [L07 p.18] [L07 p.20]
- Retrieved chunks are pasted into a new prompt together with the question [L07 p.24]
- Long-term memory for chatbots can be built by storing past conversations as a vector database (RAG) [L07 p.33]
- Karpathy's LLM Wiki: the LLM "compiles" raw sources into a linked set of .md pages it maintains itself [L07 p.37] [L07 p.39]
- At ~100 articles the LLM can answer questions by reading its own index, without complex RAG [L07 p.41]
- The LLM also runs "health checks" (linting) on the wiki to find inconsistencies and gaps [L07 p.43]

## Concepts it feeds
[[context-engineering]] · [[rag]] · [[memory]] · [[llm-wiki]]
