# Loop (loop engineering)

**One line:** a spec that makes the agent repeat make → check → fix until done or stopped.

## Explanation
Without a loop, *you* are the loop: you keep noticing problems and typing fixes. Loop
engineering writes that process down once (goal, checks, when to stop) and lets it run
many rounds. In a loop, the AI decides the next step within your spec.

## Key points
- Make a version → a check finds a problem → fix → redo; that's a loop [L10 p.5]
- The first loop was one line: re-feed the same PROMPT.md every round (Ralph loop) [L10 p.19]
- A prompt is written for one round; a loop spec is written once and runs many rounds [L10 p.20]
- Five things to state: goal, limits, done-criteria, stop condition, trigger [L10 p.21]
- Brakes: max 3 rounds, stop when data is missing, watch token cost [L10 p.23]
- In a loop the AI decides the next step [L10 p.24]

## Example
```bash
while :; do cat PROMPT.md | claude ; done   # the original one-line loop
```
A real loop adds a stop: `for round in 1 2 3; do run; check && break; done`

## Related
[[graph]] · [[checks]] · [[delegation]] · [[reflection]]
