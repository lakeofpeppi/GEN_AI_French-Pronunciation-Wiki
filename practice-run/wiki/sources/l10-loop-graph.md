# L10 — 把你的工作拆成AI能做的流程 (Breaking your work into flows AI can run)

## What it covers
The last two steps of the course ladder: loop engineering and graph engineering. How to
specify a loop, how to check it with scripts, when to switch to a graph, and how to
prototype a workflow where every stage is a file. Also: building an LLM Wiki "discuss first".

## Key points
- The course ladder ends with loop and graph engineering on the way to AI agents [L10 p.4]
- A loop: the AI makes a version, a check finds a problem, it fixes and redoes [L10 p.5]
- Two engineering habits: use git so every step can be undone, and let scripts, not the AI, decide when work is done [L10 p.14]
- Use one rules file: AGENTS.md is read by most tools; CLAUDE.md can just contain @AGENTS.md [L10 p.15]
- The earliest loop was one line (the "Ralph loop"): feed the same PROMPT.md to the agent again and again [L10 p.19]
- Writing a loop means writing a spec (goal, done-criteria, checks, stop) once and letting it run many rounds [L10 p.20]
- A loop must state five things: goal, limits, done-criteria, stop condition, trigger [L10 p.21]
- Checks come in two kinds: program checks (tests, links, every slide has a source) and AI review in a fresh conversation given only the output and sources [L10 p.22]
- Loops need brakes: a hard limit (max 3 rounds), stop when data is missing, and awareness that loops cost many tokens [L10 p.23]
- Loop vs graph: in a loop the AI decides the next step; in a graph you draw the flow in advance [L10 p.24]
- Prompt, loop and graph are all graphs: a loop adds a "go back" edge, and back-edges can go to any node [L10 p.25]
- Small loops should spin fast; big loops back to the start should be rare. Frequent big loops mean the check should move earlier [L10 p.26]
- Start with a prompt, upgrade to a loop, split into a graph only when problems demand it [L10 p.27]
- Build the wiki "discuss first": the AI asks about 8–10 questions one by one, summarizes, and only creates files after you confirm [L10 p.31]
- The AI should ask about readers, contradictions, language, citation detail, ingest mode, outputs, lint and page types [L10 p.32]
- Keep the rules file short (Antigravity's limit is 12,000 characters) and move details into skills [L10 p.34]
- Loop version of topic → slides: wiki only, 8–15 slides, every slide sourced, fresh-context review, max 3 rounds [L10 p.41]
- Graph version: retrieve → coverage gate → evidence cards → outline → human check → per-slide drafts → slide gate → render → render check [L10 p.43]
- Each node may only see and change specific things; e.g. the render node can't change words [L10 p.44]
- Return routes are designed in advance: a wrong card goes back to card extraction, too many words goes back to that slide's draft [L10 p.45]
- Inside each graph node a small loop does the repeated fixing (e.g. max 2 rounds) [L10 p.46]
- In a workflow prototype, all state lives in files, so every stage can be opened, committed and re-run alone [L10 p.47]
- Saying "check it" isn't verification; write the definition of done first [L10 p.51]

## Concepts it feeds
[[loop]] · [[graph]] · [[checks]] · [[rules-file]] · [[llm-wiki]] · [[delegation]] · [[ai-agent]]
