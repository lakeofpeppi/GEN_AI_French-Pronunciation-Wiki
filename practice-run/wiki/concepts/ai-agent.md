# AI agent

**One line:** an AI model plus the "harness" that lets it plan, use tools, and act for you.

## Explanation
A plain chatbot answers once. An agent works more like an employee: given a goal, it plans,
gathers information, calls tools, checks its work and iterates until the task is done.
In this course the formula is AI Agent = AI Model + Harness: the model thinks, the harness
does things in the real world.

## Key points
- AI Agent = AI Model + Harness [L08 p.4]
- An agent does the work you'd otherwise do yourself: planning, collecting data, iterating [L08 p.13]
- Even RAG counts as a simple agent: the computer finds the information itself [L08 p.14]
- Four design patterns: Reflection, Tool Use, Planning, Multi-agent [L08 p.18]
- The model thinks; the harness acts and reports back [L09 p.14]
- The course ladder: prompt → context → harness → loop → graph engineering, leading to AI agents [L10 p.4]

## Example
"Book me the cheapest train to Taipei tomorrow": the agent plans (search → compare → book),
calls a timetable tool, checks prices, and reports back.

## Related
[[harness]] · [[reflection]] · [[tool-use]] · [[planning]] · [[multi-agent]] · [[rag]] · [[loop]] · [[graph]]

## Disagreements
Two definitions appear on consecutive slides. They don't contradict, but they frame agents differently:
- General AI textbook: anything that perceives its environment through sensors and acts through actuators [L08 p.3]
- This course: AI Model + Harness, i.e. "teaching AI how we work" [L08 p.4]
