"""Itinerary agent for creating day-by-day travel plans."""

from google.adk import Agent
from google.adk.tools import google_search

from travel_research.shared_libraries.constants import MODEL

from . import prompt

itinerary_agent = Agent(
    model=MODEL,
    name="itinerary_agent",
    description="Creates a detailed day-by-day travel itinerary using gathered research",
    instruction=prompt.ITINERARY_AGENT_PROMPT,
    output_key="itinerary",
    tools=[google_search],
)
