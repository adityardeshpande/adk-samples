"""Root agent for the travel research multi-agent system."""

from google.adk import Agent

from travel_research.shared_libraries.constants import MODEL

from . import prompt
from .sub_agents.attractions_agent import attractions_agent
from .sub_agents.itinerary_agent import itinerary_agent
from .sub_agents.logistics_agent import logistics_agent
from .sub_agents.report_agent import report_agent
from .sub_agents.search_agent import search_agent

root_agent = Agent(
    model=MODEL,
    name="travel_research_agent",
    description=(
        "A travel research agent that researches destinations and produces "
        "comprehensive PDF reports with visuals and day-by-day itineraries"
    ),
    instruction=prompt.ROOT_AGENT_PROMPT,
    sub_agents=[
        search_agent,
        attractions_agent,
        logistics_agent,
        itinerary_agent,
        report_agent,
    ],
)
