# Memory (short-term vs long-term)

**One line:** what an LLM chatbot remembers within one chat vs across chats.

## Explanation
"Short-term memory" is just the current conversation, which disappears next time and can be
lost when the chat gets too long. "Long-term memory" is built outside the model, for example by
saving old conversations in a vector database and retrieving them with RAG.

## Key points
- Short-term memory = the current conversation; forgotten next session, and early parts can drop when it's long [L07 p.32]
- Long-term memory can be made by turning past conversations into a vector database (RAG) [L07 p.33]

## Example
A drink-shop bot that remembers your usual order next visit is using long-term memory.

## Related
[[rag]]
