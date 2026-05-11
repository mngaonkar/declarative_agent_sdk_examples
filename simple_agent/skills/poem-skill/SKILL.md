---
name: poem-skill
description: Generate a short poem based on current top news headlines. Use when the user asks to write a poem, verse, or creative piece inspired by today's news or current events.
category: agent
---

# Poem Skill

Fetches current top news headlines and composes a short, creative poem based on them.

## Behavior

- Searches for today's top news using the `tavily_search` tool
- Selects a relevant headline or theme from the results
- Writes a concise poem inspired by the news content

## Output

Returns a short poem as plain text.

