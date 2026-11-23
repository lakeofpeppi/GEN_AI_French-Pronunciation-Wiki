# Graph (graph engineering)

**One line:** a workflow you draw in advance: fixed nodes, fixed checks, fixed "go back" routes.

## Explanation
A graph is like a school application process: department → college → registrar, no
skipping, and a problem sends you back to a specific office. Each node has a narrow job and
limited inputs; checks sit between nodes; failures go back to the node nearest the error.
Small loops can still run *inside* each node.

## Key points
- In a graph, you draw the flow in advance (in a loop, the AI decides) [L10 p.24]
- Prompt, loop and graph are all graphs; back-edges can return to any node [L10 p.25]
- Fix errors close to where they start; frequent big loops mean a check should move earlier [L10 p.26]
- Only add as much structure as your problems need: prompt → loop → graph [L10 p.27]
- Example slide graph: retrieve → coverage gate → evidence cards → outline → human check → drafts → slide gate → render → render check [L10 p.43]
- Each node sees and changes only specific inputs [L10 p.44]
- Return routes are designed in advance [L10 p.45]
- Small loops live inside nodes (e.g. draft → check sources → fix, max 2 rounds) [L10 p.46]
- All state is files, so each stage can be inspected and re-run alone [L10 p.47]

## Example
```
retrieve → (coverage ok?) → cards → (quotes ok?) → outline → drafts → (slide ok?) → render
                                ↑ fail: redo that card          ↑ fail: redo only that slide
```

## Related
[[loop]] · [[checks]] · [[multi-agent]]
