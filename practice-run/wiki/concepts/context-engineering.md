# Context engineering

**One line:** deciding what information and instructions go into the model's input.

## Explanation
An LLM only knows what's in its weights plus what you put in the prompt. Context engineering
is the job of putting the *right* facts, background and output format into that input, so
the model doesn't have to guess. In this course it sits between prompt engineering and harness
engineering on the path to AI agents.

## Key points
- Two ingredients: correct information, and clear instructions on what to do and in what format [L07 p.5]
- The model doesn't know the background in your head, so you must state data and conditions [L08 p.11]

## Example
Instead of "summarize this", send: the document, who the summary is for, the length limit,
and the format (e.g. 3 bullets in English).

## Related
[[rag]] · [[ai-agent]]
