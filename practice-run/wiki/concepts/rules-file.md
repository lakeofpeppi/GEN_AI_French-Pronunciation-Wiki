# Rules file (AGENTS.md / CLAUDE.md)

**One line:** a Markdown "employee handbook" the agent reads before every task.

## Explanation
A rules file tells an AI agent how *this* project works: its purpose, folders, naming,
formats and what never to do. Coding agents load it automatically at the start of a session,
so you don't repeat yourself every time. It's part of the agent's harness.

## Key points
- Claude Code reads CLAUDE.md; Codex and Cursor read AGENTS.md [TA07 p.8]
- Good rules grow from real problems: each mistake becomes a new rule [TA07 p.14]
- It's one part of a product's harness, read before each task [L09 p.16]
- Keep one file: most tools read AGENTS.md, and CLAUDE.md can just say @AGENTS.md [L10 p.15]
- Keep it short (Antigravity's limit is 12,000 characters); put details into skills [L10 p.34]

## Example
"Every page uses the same template" was added after pages came out inconsistent.

## Related
[[llm-wiki]] · [[harness]] · [[delegation]]
