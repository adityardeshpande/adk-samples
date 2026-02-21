"""Tests for travel research agent structure."""

from travel_research.sub_agents.search_agent import search_agent


def test_search_agent_exists():
    assert search_agent is not None
    assert search_agent.name == "search_agent"


def test_search_agent_has_google_search_tool():
    assert len(search_agent.tools) > 0


from travel_research.sub_agents.attractions_agent import attractions_agent


def test_attractions_agent_exists():
    assert attractions_agent is not None
    assert attractions_agent.name == "attractions_agent"


def test_attractions_agent_has_google_search_tool():
    assert len(attractions_agent.tools) > 0


from travel_research.sub_agents.logistics_agent import logistics_agent


def test_logistics_agent_exists():
    assert logistics_agent is not None
    assert logistics_agent.name == "logistics_agent"


def test_logistics_agent_has_google_search_tool():
    assert len(logistics_agent.tools) > 0


from travel_research.sub_agents.itinerary_agent import itinerary_agent


def test_itinerary_agent_exists():
    assert itinerary_agent is not None
    assert itinerary_agent.name == "itinerary_agent"


def test_itinerary_agent_has_google_search_tool():
    assert len(itinerary_agent.tools) > 0


from travel_research.sub_agents.report_agent import report_agent


def test_report_agent_exists():
    assert report_agent is not None
    assert report_agent.name == "report_agent"


def test_report_agent_has_pdf_tool():
    tool_names = [t.__name__ if callable(t) else str(t) for t in report_agent.tools]
    assert any("generate_pdf" in name for name in tool_names)


from travel_research.agent import root_agent


def test_root_agent_exists():
    assert root_agent is not None
    assert root_agent.name == "travel_research_agent"


def test_root_agent_has_five_sub_agents():
    assert len(root_agent.sub_agents) == 5


def test_root_agent_sub_agent_names():
    names = {sa.name for sa in root_agent.sub_agents}
    expected = {"search_agent", "attractions_agent", "logistics_agent", "itinerary_agent", "report_agent"}
    assert names == expected
