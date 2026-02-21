"""Search agent for destination overview research."""

from google.adk import Agent
from google.adk.tools import google_search

from travel_research.shared_libraries.constants import MODEL

from . import prompt

search_agent = Agent(
    model=MODEL,
    name="search_agent",
    description="Researches general destination overview and key facts using Google Search",
    instruction=prompt.SEARCH_AGENT_PROMPT,
    output_key="destination_overview",
    tools=[google_search],
)
