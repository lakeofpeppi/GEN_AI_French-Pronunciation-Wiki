# L08 — 教AI做事的方法 (Teaching AI how we work: AI Agents and design patterns)

## What it covers
What an AI agent is, why "one shot" prompting is hard, Andrew Ng's four agentic design
patterns, tool calling with JSON, MCP/A2A, and Karpathy's "vibe coding".

## Key points
- Classic definition: an agent perceives its environment through sensors and acts on it through actuators (Russell & Norvig) [L08 p.3]
- Course definition: AI Agent = AI Model + Harness [L08 p.4]
- Writing in one pass without deleting or editing is hard even for humans; we iterate [L08 p.9]
- RAG is already a simple kind of AI agent: the computer finds relevant information itself [L08 p.14]
- Andrew Ng's four design patterns: Reflection, Tool Use, Planning, Multi-agent Collaboration [L08 p.18]
- Reflection: one LLM drafts, another critiques, the first revises; can repeat [L08 p.19]
- Tool Use: call tools for what LLMs are bad at, like precise calculation, real data and web search [L08 p.23]
- Tools are described to the model (e.g. get_menu, quote_order); the tool returns JSON the model answers from [L08 p.25] [L08 p.27]
- MCP standardizes how one agent uses external tools; A2A is about agents talking to each other [L08 p.31]
- Planning: let the LLM think or draft a plan before answering, e.g. chain-of-thought [L08 p.32] [L08 p.34]
- Multi-agent: often a PM-like LLM splits the task and assigns parts to other agents [L08 p.38]
- Vibe coding: describe what you want, accept the AI's code without reading it; fine for weekend projects, not for production [L08 p.46] [L08 p.50] [L08 p.51]

## Concepts it feeds
[[ai-agent]] · [[harness]] · [[reflection]] · [[tool-use]] · [[planning]] · [[multi-agent]] · [[vibe-coding]] · [[rag]]
