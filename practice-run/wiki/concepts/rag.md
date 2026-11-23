# RAG (Retrieval-Augmented Generation)

**One line:** search your own documents first, then give the matching pieces to the LLM.

## Explanation
Documents are cut into chunks, each chunk becomes a vector (an embedding), and the user's
question becomes a vector too. The chunks closest to the question are retrieved and pasted
into the prompt, so the model answers from real text instead of memory. For a CS student:
it's nearest-neighbour search over vectors, followed by string templating into a prompt.

## Key points
- A method to reduce errors by giving the model correct information [L07 p.3]
- Documents are split into chunks, e.g. 500 characters with a 50-character overlap [L07 p.11]
- Chunks can carry metadata (source, page, author, date) for filtering [L07 p.15]
- Question and chunks are embedded; the closest chunks are retrieved [L07 p.18] [L07 p.20]
- The final prompt combines the retrieved chunks and the question [L07 p.24]
- RAG already counts as a simple AI agent, since the computer finds the information itself [L08 p.14]

## Example
```python
chunks = top_k(embed(question), index, k=3)   # nearest vectors
prompt = f"answer using only: {chunks}\nquestion: {question}"
```

## Related
[[context-engineering]] · [[memory]] · [[llm-wiki]] · [[ai-agent]]
