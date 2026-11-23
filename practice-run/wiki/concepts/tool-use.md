# Tool use (工具使用)

**One line:** let the LLM call functions for things it's bad at.

## Explanation
LLMs are weak at exact arithmetic, live data and searching. So you describe some functions
to the model; when it needs one, it outputs a call (function name + arguments), your code
runs it, and the JSON result goes back to the model, which writes the final answer.

## Key points
- Use tools for what LLMs aren't good at: precise calculation, real data, web search [L08 p.23]
- The model is told which tools exist, e.g. get_menu and quote_order [L08 p.25]
- The tool returns structured JSON, which the model turns into an answer [L08 p.27]
- MCP is a standard for connecting an agent to external tools and data [L08 p.31]
- Products give agents built-in tools: read/write files, terminal, browser, web search [L09 p.16]

## Example
```json
{"ok": true, "item_name": "麥茶", "quantity": 20, "unit_price": 30, "total": 600}
```
The model then answers: "No problem, 20 cups is 600 TWD." (drink-shop example [L08 p.27])

## Related
[[ai-agent]] · [[harness]]
