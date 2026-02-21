"""Attractions agent for researching things to see, do, and eat."""

from google.adk import Agent
from google.adk.tools import google_search

from travel_research.shared_libraries.constants import MODEL

from . import prompt

attractions_agent = Agent(
    model=MODEL,
    name="attractions_agent",
    description="Researches top attractions, restaurants, cultural experiences, and hidden gems with image URLs",
    instruction=prompt.ATTRACTIONS_AGENT_PROMPT,
    output_key="attractions_info",
    tools=[google_search],
)
