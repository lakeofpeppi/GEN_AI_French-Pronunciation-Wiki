# Harness

**One line:** everything around the model that lets it actually do things.

## Explanation
The model only produces text. The harness turns that text into actions (open a file, run
code, search the web), feeds results back, and gives the model rules and a workspace.

## Key points
- The second half of the course formula: AI Agent = AI Model + Harness [L08 p.4]
- Model = brain (understand, plan, decide); harness = equipment that executes and reports results back [L09 p.14]
- Built by hand in the homework: system prompt, Python functions as tools, error handling and retries [L09 p.15]
- Product harness parts: workspace (sandbox), skills (SKILL.md), tools (files, terminal, browser, search), rules file [L09 p.16]
- Models are similar; the harness decides how useful the agent is [L09 p.17]

## Example
Model: "I want to read data.csv." Harness: actually opens the file and returns its contents.

## Related
[[ai-agent]] · [[tool-use]] · [[rules-file]]
