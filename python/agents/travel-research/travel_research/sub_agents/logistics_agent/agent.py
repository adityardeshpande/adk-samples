"""Logistics agent for practical travel information research."""

from google.adk import Agent
from google.adk.tools import google_search

from travel_research.shared_libraries.constants import MODEL

from . import prompt

logistics_agent = Agent(
    model=MODEL,
    name="logistics_agent",
    description="Researches weather, costs, visa, safety, transport, and practical travel logistics with image URLs",
    instruction=prompt.LOGISTICS_AGENT_PROMPT,
    output_key="logistics_info",
    tools=[google_search],
)
