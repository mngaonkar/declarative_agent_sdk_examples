---
name: battery-skill
description: Retrieve current battery status and health information on macOS. Use when the user asks about battery life, charge percentage, time remaining, or battery health.
category: agent
---

# Battery Skill

Fetches current battery status, charge level, and health information on macOS systems.

## Behavior

- Uses `exec_command` builtin tool to execute `pmset -g batt` for battery state
- Parses battery percentage and remaining time from command output
- Optionally uses `exec_command` to run `system_profiler SPPowerDataType` for detailed battery health
- Returns formatted battery information

## Tools Used

- **exec_command**: Execute shell commands to retrieve battery information from macOS system utilities. Returns exit code, stdout, stderr, and execution status.

## Output

Returns structured battery data including:

- Current charge percentage
- Battery state (charging, discharging, charged)
- Time remaining (if on battery)
- Cycle count (if available)
- Battery health status

## Example Output

```
Battery Information:
├─ Charge: 85%
├─ State: discharging
├─ Time Remaining: 4 hours 23 minutes
├─ Cycle Count: 127
└─ Health: Normal
```

## Available Builtin Tools Reference

The declarative_agent_sdk provides these builtin tools:

| Tool | Purpose |
|------|---------|
| `exec_command` | Execute shell commands with timeout, working directory, and output capture |
| `exec_async` | Asynchronous execution of commands and processes |
| `read_file` | Read file content from filesystem |
| `write_file` | Write or append content to files |
| `tavily_search` | Search the web using Tavily search engine API |

## Notes

- Requires macOS system
- No API keys needed
- Can be used to monitor system health or alert on low battery conditions
- Import tools: `from declarative_agent_sdk.builtin_tools import exec_command, read_file, write_file`
