# Reflection (反思)

**One line:** draft → critique → revise, repeated.

## Explanation
Instead of trusting the first answer, one LLM call writes a draft, another call (acting as a
critic) reviews it and suggests fixes, and the first revises. It mirrors how people write:
nobody writes a perfect essay in one pass without editing.

## Key points
- Writing in one pass without editing is hard even for humans, so we iterate [L08 p.9]
- First LLM drafts, second evaluates and suggests improvements, first revises; repeatable [L08 p.19]
- The critic can be a different model [L08 p.21]

## Example
```python
draft = llm("write a function that ...")
for _ in range(3):
    review = critic("find bugs in:\n" + draft)
    draft = llm("fix these issues:\n" + review + "\n" + draft)
```

## Related
[[ai-agent]] · [[planning]] · [[checks]]
