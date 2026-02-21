# Travel Research Agent — Design Document

**Date:** 2026-02-21
**Status:** Approved

## Overview

A Google ADK-based multi-agent system that researches travel destinations using Google Search and produces a comprehensive PDF report with visuals and a day-by-day itinerary.

## Tech Stack

- Python + Google ADK
- Google Gemini 2.5 Flash (LLM)
- FastAPI (serving)
- google_search tool (built-in ADK tool)
- fpdf2 (PDF generation)

## Architecture

Flat sub-agent composition with prompt-driven sequential routing.

```
Root Agent ("travel_research_agent")
│  Model: gemini-2.5-flash
│  Role: Greet user, gather destination + trip duration,
│        orchestrate sub-agents in sequence, deliver final output
│
├── search_agent
│   Model: gemini-2.5-flash
│   Tool: google_search
│   Role: Search for general destination overview and key facts
│   Output key: "destination_overview"
│
├── attractions_agent
│   Model: gemini-2.5-flash
│   Tool: google_search
│   Role: Research top attractions, restaurants, experiences + image URLs
│   Output key: "attractions_info"
│
├── logistics_agent
│   Model: gemini-2.5-flash
│   Tool: google_search
│   Role: Research weather, costs, visa, transport, safety + image URLs
│   Output key: "logistics_info"
│
├── itinerary_agent
│   Model: gemini-2.5-flash
│   Tool: google_search
│   Role: Build day-by-day itinerary (default 3 days, user-configurable)
│   Output key: "itinerary"
│
└── report_agent
    Model: gemini-2.5-flash
    Tool: generate_pdf (custom)
    Role: Compile all research into a styled PDF with images
    Output key: "final_report"
```

## File Structure

```
travel-research/
├── pyproject.toml
├── requirements.txt
├── .env.example
├── README.md
├── CLAUDE.md
├── travel_research/
│   ├── __init__.py
│   ├── agent.py
│   ├── prompt.py
│   ├── shared_libraries/
│   │   ├── __init__.py
│   │   └── constants.py
│   ├── tools/
│   │   ├── __init__.py
│   │   └── pdf_generator.py
│   └── sub_agents/
│       ├── __init__.py
│       ├── search_agent/
│       │   ├── __init__.py
│       │   ├── agent.py
│       │   └── prompt.py
│       ├── attractions_agent/
│       │   ├── __init__.py
│       │   ├── agent.py
│       │   └── prompt.py
│       ├── logistics_agent/
│       │   ├── __init__.py
│       │   ├── agent.py
│       │   └── prompt.py
│       ├── itinerary_agent/
│       │   ├── __init__.py
│       │   ├── agent.py
│       │   └── prompt.py
│       └── report_agent/
│           ├── __init__.py
│           ├── agent.py
│           └── prompt.py
├── tests/
│   └── test_agent.py
└── eval/
    └── eval_data.json
```

## Data Flow

```
User: "Research Tokyo for a 5-day trip"
  │
  ▼
Root Agent
  │ Extracts: destination="Tokyo", duration=5
  │
  ├─→ search_agent
  │     Uses google_search to find destination overview
  │     Stores → state["destination_overview"]
  │
  ├─→ attractions_agent
  │     Uses google_search for attractions, food, experiences
  │     Gathers image URLs for key attractions
  │     Stores → state["attractions_info"]
  │
  ├─→ logistics_agent
  │     Uses google_search for weather, costs, visa, transport
  │     Gathers image URLs for transport options
  │     Stores → state["logistics_info"]
  │
  ├─→ itinerary_agent
  │     Reads state["attractions_info"] + state["logistics_info"]
  │     Builds N-day itinerary
  │     Stores → state["itinerary"]
  │
  └─→ report_agent
        Reads all state keys
        Calls generate_pdf tool with compiled content + image URLs
        Returns PDF file path to user
```

## PDF Report Structure

- Destination header with hero image
- Overview section
- Top Attractions with photos (2-column image layout)
- Practical Info: weather, costs, visa, transport (with transport images)
- Day-by-day itinerary
- Tips and recommendations

## Key Decisions

- **Flat sub-agents** over AgentTool or nested hierarchy for simplicity
- **google_search only** — no raw HTTP scraping, Gemini handles retrieval
- **fpdf2** for PDF — lightweight, simple API, good image support
- **State passing via output_key** — each agent writes structured JSON to state
- **Default 3-day itinerary** — accepts user-specified duration
- **Sequential routing** — search → attractions → logistics → itinerary → report
