from google.adk.sessions import InMemorySessionService
from google.genai import types
from google.genai.types import ThinkingConfig, GenerateContentConfig
from dotenv import load_dotenv
from google.adk.tools import google_search
from google.adk.planners import PlanReActPlanner
from google.adk.code_executors import BuiltInCodeExecutor
from google.adk.agents.sequential_agent import SequentialAgent
import logging
from declarative_agent_sdk import AgentState
from declarative_agent_sdk import AIAgent
from declarative_agent_sdk.utils import save_to_file
from skills.collation.scripts.create_pdf_file import create_pdf_file
from declarative_agent_sdk.tool_registry import ToolRegistry
from declarative_agent_sdk.agent_factory import AgentFactory
from declarative_agent_sdk.agent_registry import AgentRegistry

logger = logging.getLogger(__name__)

AGENT_NAME = "collation_agent"
INSTRUCTION_FILE_PATH = AGENT_NAME + "/SKILL.md"
OUTPUT_PDF_LOCATION = "workspace/collation_response.pdf"

def create_collation_agent(name: str) -> AIAgent:
    ToolRegistry.register("create_pdf_file", create_pdf_file)
    agent = AgentFactory.from_yaml_file('collation_agent/configs/collation_agent.yaml')
    AgentRegistry.register(agent, category='collation')
    logger.info(f"Collation agent '{name}' created from YAML config.")

    return agent


async def run_query_and_collect_full_stream(agent: AIAgent, query: str) -> str:
    """Collect final response text without terminating the underlying stream early."""
    final_response = ""
    async for event in agent.run_query(query):
        if (
            event.is_final_response()
            and not event.long_running_tool_ids
            and event.content
            and event.content.parts
        ):
            final_response = event.content.parts[0].text or ""
    return final_response

agent = create_collation_agent("collation_agent")
logger.info("Collation agent initialized.")

async def collation_agent(state: AgentState) -> AgentState:
    """Collate chapter content into a single PDF file."""
    chapter_locations = state.get("agents_output", {}).get("chapter_agent", [])
    assert chapter_locations, "Chapter locations missing in state['agents_output']['chapter_agent']"

    toc_location = state.get("agents_output", {}).get("toc_agent", "")
    assert toc_location, "TOC location missing in state['agents_output']['toc_agent']"

    ca = create_collation_agent(name="collation_agent")
    user_prompt = f"""Create a PDF book from the following inputs:
    - toc_location: Table of Contents location: {toc_location}
    - chapter_locations: Chapter markdown files: {chapter_locations}

    Use the create_pdf_file tool with both the chapter_locations list and toc_location."""

    collation_response = await run_query_and_collect_full_stream(ca, user_prompt)
    logger.info(f"Collation agent response: {collation_response}")

    save_to_file(collation_response, OUTPUT_PDF_LOCATION)
    logger.info(f"Collation agent response saved to {OUTPUT_PDF_LOCATION}")

    state["final_answer"] = OUTPUT_PDF_LOCATION
    return state