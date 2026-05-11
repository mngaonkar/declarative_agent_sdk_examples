# simple-agent

Minimal example of a declarative agent built with
[declarative_agent_sdk](https://github.com/mngaonkar/declarative_agent_sdk).

The project includes:

- A declarative agent runner (`agent.py`)
- YAML-based agent configuration (`configs/agent.yaml`)
- A reusable skill (`skills/poem-skill/SKILL.md`)

## What this agent does

The configured agent:

- Uses provider `openai` with model `gpt-4o`
- Enables the `tavily_search` tool
- Loads the `poem-skill` skill from `./skills`
- Generates a short poem inspired by current news

## Project structure

```text
simple_agent/
	agent.py
	pyproject.toml
	README.md
	configs/
		agent.yaml
	skills/
		poem-skill/
			SKILL.md
```

## Prerequisites

- Python 3.14+
- [uv](https://docs.astral.sh/uv/) (recommended)

## Install dependencies

From the `simple_agent` directory:

```bash
uv sync
```

The Git dependency is declared in `pyproject.toml`:

```toml
[tool.uv.sources]
declarative-agent-sdk = { git = "https://github.com/mngaonkar/declarative_agent_sdk.git" }
```

## Environment variables

Create a `.env` file in the project root (or export in your shell):

```bash
OPENAI_API_KEY=your_openai_api_key
TAVILY_API_KEY=your_tavily_api_key
```

## Run

Run the declarative agent:

```bash
uv run python agent.py
```

Expected behavior:

- Agent loads from `configs/agent.yaml`
- Agent registers under category `poetry`
- Agent runs with prompt `do your job`
- Final response is printed

## Agent configuration

Current configuration (`configs/agent.yaml`):

- `name`: `simple_agent`
- `description`: writes a poem from current news
- `provider`: `openai`
- `model`: `gpt-4o`
- `tools`: `tavily_search`
- `skills_directory`: `./skills`
- `skills`: `poem-skill`
- `output_key`: `agent_response`

## Troubleshooting

If dependency resolution points to an unexpected local path:

1. Ensure you are running inside this project's environment.
2. Re-sync dependencies:

```bash
uv sync --reinstall
```

3. Verify source resolution:

```bash
uv tree | rg -i declarative-agent-sdk
```

## Notes

- `agent.py` is the actual declarative agent entrypoint.
