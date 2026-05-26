# declarative_agent_sdk_examples

Example projects built with [declarative_agent_sdk](https://github.com/mngaonkar/declarative_agent_sdk).

This repository contains small, runnable examples that show different ways to build agents with declarative YAML configuration, reusable skills, tool registration, and multi-agent workflows.

## Repository contents

The top-level projects in this repository are:

- `simple_agent`: a single-agent example
- `book_agent`: a multi-agent workflow that generates a book and collates it into a PDF
- `agent_cli_client`: a CLI client for interacting with an agent server over HTTP

## Available agents

### `simple_agent`

Location:
- `simple_agent/`

Type:
- Single agent

Current behavior:
- Loads agent configuration from `simple_agent/configs/agent.yaml`
- Uses provider `openai` with model `gpt-5.4`
- Currently enables the `nasa-image` skill
- Runs with tool approval enabled
- Executes the prompt `download beautiful nebula image`

Available skills in the project:
- `nasa-image`
- `battery-skill`
- `poem-skill`

Use this example when you want the smallest working setup for a declarative agent.

### `book_agent`

Location:
- `book_agent/`

Type:
- Multi-agent workflow

Workflow agents:
- `toc_agent`: generates a table of contents in YAML
- `chapter_agent_parallel`: generates chapter markdown files in parallel
- `collation_agent`: combines TOC and chapters into a final PDF

Current behavior:
- Workflow is defined in `book_agent/configs/agents/book_workflow.yaml`
- Runtime wiring lives in `book_agent/agent_graph.py`
- Generated files are written to `book_agent/workspace/`
- Final output is a PDF path stored in workflow state and written to `workspace/collation_response.pdf`

Use this example when you want to build a graph-style workflow with multiple cooperating agents.

### `agent_cli_client`

Location:
- `agent_cli_client/`

Type:
- Support tool, not an agent

Behavior:
- Connects to an agent server at `http://localhost:8000`
- Streams agent responses
- Handles tool approval prompts interactively

Use this project to test or drive an agent server from the terminal.

## Repository structure

```text
declarative_agent_sdk_examples/
	README.md
	simple_agent/
	book_agent/
	agent_cli_client/
```

## Requirements

- Python 3.14+
- `uv`
- Access to the configured model endpoint for each example
- Required API keys for any enabled tools

## Installation

Each example is managed independently. Install dependencies inside the project you want to run.

Example:

```bash
cd simple_agent
uv sync
```

Or:

```bash
cd book_agent
uv sync
```

All projects currently depend on `declarative-agent-sdk` from GitHub via `pyproject.toml`.

## Running the examples

### Run `simple_agent`

```bash
cd simple_agent
uv run python agent.py
```

### Run `book_agent`

```bash
cd book_agent
uv run python -m agent_graph
```

Or:

```bash
cd book_agent
./run_agent.sh
```

### Run `agent_cli_client`

```bash
cd agent_cli_client
uv run python agent_client.py
```

## Where to look next

- See `simple_agent/README.md` for the single-agent example
- See `book_agent/README.md` for the workflow example
- See `agent_cli_client/agent_client.py` for the streaming client implementation

## Notes

- Project READMEs may describe the intended usage of each example in more detail.
- The root README is intended to help you choose the right example and find the relevant entrypoints quickly.
