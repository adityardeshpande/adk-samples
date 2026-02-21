# Travel Research Agent Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a multi-agent travel research system that produces a PDF report with visuals and itinerary for any destination.

**Architecture:** Flat sub-agent composition — root agent orchestrates 5 specialized sub-agents (search, attractions, logistics, itinerary, report) sequentially via prompt-driven routing. Each sub-agent uses google_search for research. The report_agent uses a custom generate_pdf tool (fpdf2) to produce the final PDF.

**Tech Stack:** Python, Google ADK, Gemini 2.5 Flash, google_search tool, fpdf2, FastAPI

---

### Task 1: Project Scaffolding

**Files:**
- Create: `travel_research/__init__.py`
- Create: `travel_research/shared_libraries/__init__.py`
- Create: `travel_research/shared_libraries/constants.py`
- Create: `travel_research/tools/__init__.py`
- Create: `travel_research/sub_agents/__init__.py`
- Create: `pyproject.toml`
- Create: `requirements.txt`
- Create: `.env.example`

**Step 1: Create directory structure**

```bash
cd /Users/adityadeshpande/PycharmProjects/adk-samples/python/agents/travel-research
mkdir -p travel_research/shared_libraries
mkdir -p travel_research/tools
mkdir -p travel_research/sub_agents/search_agent
mkdir -p travel_research/sub_agents/attractions_agent
mkdir -p travel_research/sub_agents/logistics_agent
mkdir -p travel_research/sub_agents/itinerary_agent
mkdir -p travel_research/sub_agents/report_agent
mkdir -p tests
mkdir -p eval
```

**Step 2: Create constants.py**

```python
# travel_research/shared_libraries/constants.py
"""Shared constants for the travel research agent."""

import os

from dotenv import load_dotenv

load_dotenv()

MODEL = os.getenv("MODEL", "gemini-2.5-flash")
DEFAULT_TRIP_DURATION = 3
```

**Step 3: Create shared_libraries/__init__.py**

```python
# travel_research/shared_libraries/__init__.py
"""Shared libraries for travel research agent."""
```

**Step 4: Create tools/__init__.py**

```python
# travel_research/tools/__init__.py
"""Tools for travel research agent."""
```

**Step 5: Create sub_agents/__init__.py**

```python
# travel_research/sub_agents/__init__.py
"""Sub-agents for travel research agent."""
```

**Step 6: Create pyproject.toml**

```toml
[project]
name = "travel-research"
version = "0.1.0"
description = "A multi-agent travel research system that produces PDF reports with visuals and itineraries"
readme = "README.md"
requires-python = ">=3.10,<3.13"

dependencies = [
    "google-cloud-aiplatform[adk,agent-engines]>=1.93.0",
    "google-genai>=1.9.0",
    "pydantic>=2.10.6",
    "python-dotenv>=1.0.1",
    "google-adk>=1.0.0",
    "fpdf2>=2.8.0",
    "requests>=2.31.0",
]

[dependency-groups]
dev = [
    "pytest>=8.3.2",
    "pytest-asyncio>=0.23.7",
    "google-adk[eval]>=1.0.0",
    "nest-asyncio>=1.6.0",
]

[tool.pytest.ini_options]
pythonpath = "."
asyncio_default_fixture_loop_scope = "function"

[tool.agent-starter-pack]
example_question = "Research Tokyo for a 5-day trip"

[tool.agent-starter-pack.settings]
agent_directory = "travel_research"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

**Step 7: Create requirements.txt**

```
google-cloud-aiplatform[adk,agent-engines]>=1.93.0
google-genai>=1.9.0
pydantic>=2.10.6
python-dotenv>=1.0.1
google-adk>=1.0.0
fpdf2>=2.8.0
requests>=2.31.0
```

**Step 8: Create .env.example**

```
GOOGLE_API_KEY=your-api-key-here
GOOGLE_CLOUD_PROJECT=your-project-id-here
MODEL=gemini-2.5-flash
```

**Step 9: Commit**

```bash
git add pyproject.toml requirements.txt .env.example travel_research/shared_libraries/ travel_research/tools/__init__.py travel_research/sub_agents/__init__.py
git commit -m "feat: scaffold travel-research project structure"
```

---

### Task 2: Search Agent

**Files:**
- Create: `travel_research/sub_agents/search_agent/__init__.py`
- Create: `travel_research/sub_agents/search_agent/prompt.py`
- Create: `travel_research/sub_agents/search_agent/agent.py`
- Test: `tests/test_agent.py`

**Step 1: Write the test**

```python
# tests/test_agent.py
"""Tests for travel research agent structure."""

from travel_research.sub_agents.search_agent import search_agent


def test_search_agent_exists():
    assert search_agent is not None
    assert search_agent.name == "search_agent"


def test_search_agent_has_google_search_tool():
    assert len(search_agent.tools) > 0
```

**Step 2: Run test to verify it fails**

Run: `cd /Users/adityadeshpande/PycharmProjects/adk-samples/python/agents/travel-research && python -m pytest tests/test_agent.py -v`
Expected: FAIL with ImportError

**Step 3: Create search_agent prompt.py**

```python
# travel_research/sub_agents/search_agent/prompt.py
"""Prompt for the search agent."""

SEARCH_AGENT_PROMPT = """
You are a travel destination research specialist. Your job is to find a comprehensive
overview of a travel destination.

When given a destination, use the google_search tool to research and provide:

1. **Country & Region**: Where the destination is located
2. **Overview**: A 3-5 sentence introduction to the destination
3. **Best Time to Visit**: Ideal months/seasons and why
4. **Language**: Official language(s) and whether English is widely spoken
5. **Currency**: Local currency and typical exchange rate to USD
6. **Time Zone**: Local time zone
7. **Key Facts**: Population, climate type, any notable rankings (e.g., "most visited city")

Perform multiple searches to gather accurate, up-to-date information. Be factual and concise.
Format your response as structured text with clear headings.
"""
```

**Step 4: Create search_agent agent.py**

```python
# travel_research/sub_agents/search_agent/agent.py
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
```

**Step 5: Create search_agent __init__.py**

```python
# travel_research/sub_agents/search_agent/__init__.py
"""Search agent for destination overview research."""

from .agent import search_agent
```

**Step 6: Run test to verify it passes**

Run: `cd /Users/adityadeshpande/PycharmProjects/adk-samples/python/agents/travel-research && python -m pytest tests/test_agent.py -v`
Expected: PASS

**Step 7: Commit**

```bash
git add travel_research/sub_agents/search_agent/ tests/test_agent.py
git commit -m "feat: add search_agent sub-agent"
```

---

### Task 3: Attractions Agent

**Files:**
- Create: `travel_research/sub_agents/attractions_agent/__init__.py`
- Create: `travel_research/sub_agents/attractions_agent/prompt.py`
- Create: `travel_research/sub_agents/attractions_agent/agent.py`
- Modify: `tests/test_agent.py`

**Step 1: Write the test**

Append to `tests/test_agent.py`:

```python
from travel_research.sub_agents.attractions_agent import attractions_agent


def test_attractions_agent_exists():
    assert attractions_agent is not None
    assert attractions_agent.name == "attractions_agent"


def test_attractions_agent_has_google_search_tool():
    assert len(attractions_agent.tools) > 0
```

**Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_agent.py::test_attractions_agent_exists -v`
Expected: FAIL with ImportError

**Step 3: Create attractions_agent prompt.py**

```python
# travel_research/sub_agents/attractions_agent/prompt.py
"""Prompt for the attractions agent."""

ATTRACTIONS_AGENT_PROMPT = """
You are a travel attractions and experiences specialist. Your job is to research
the best things to see, do, and eat at a travel destination.

When given a destination, use the google_search tool to research and provide:

1. **Top Attractions** (5-8): Major landmarks, museums, natural wonders, etc.
   For each: name, brief description (1-2 sentences), estimated visit duration, and an image URL if found.

2. **Food & Dining** (5-8): Must-try local dishes, recommended restaurants, food markets, street food spots.
   For each: name, what it's known for, price range (budget/mid/upscale).

3. **Cultural Experiences** (3-5): Festivals, traditions, performances, workshops.
   For each: name, description, when/where.

4. **Hidden Gems** (3-5): Lesser-known spots that locals recommend.
   For each: name, why it's special.

5. **Image URLs**: For each major attraction, search for and include a publicly accessible image URL.
   Search for "[attraction name] photo" to find image URLs.

Perform multiple searches to be thorough. Be specific with names and locations.
Format your response as structured text with clear headings.
"""
```

**Step 4: Create attractions_agent agent.py**

```python
# travel_research/sub_agents/attractions_agent/agent.py
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
```

**Step 5: Create attractions_agent __init__.py**

```python
# travel_research/sub_agents/attractions_agent/__init__.py
"""Attractions agent for destination experiences research."""

from .agent import attractions_agent
```

**Step 6: Run tests**

Run: `python -m pytest tests/test_agent.py -v`
Expected: ALL PASS

**Step 7: Commit**

```bash
git add travel_research/sub_agents/attractions_agent/ tests/test_agent.py
git commit -m "feat: add attractions_agent sub-agent"
```

---

### Task 4: Logistics Agent

**Files:**
- Create: `travel_research/sub_agents/logistics_agent/__init__.py`
- Create: `travel_research/sub_agents/logistics_agent/prompt.py`
- Create: `travel_research/sub_agents/logistics_agent/agent.py`
- Modify: `tests/test_agent.py`

**Step 1: Write the test**

Append to `tests/test_agent.py`:

```python
from travel_research.sub_agents.logistics_agent import logistics_agent


def test_logistics_agent_exists():
    assert logistics_agent is not None
    assert logistics_agent.name == "logistics_agent"


def test_logistics_agent_has_google_search_tool():
    assert len(logistics_agent.tools) > 0
```

**Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_agent.py::test_logistics_agent_exists -v`
Expected: FAIL with ImportError

**Step 3: Create logistics_agent prompt.py**

```python
# travel_research/sub_agents/logistics_agent/prompt.py
"""Prompt for the logistics agent."""

LOGISTICS_AGENT_PROMPT = """
You are a travel logistics and practical information specialist. Your job is to research
all the practical details a traveler needs to know about a destination.

When given a destination, use the google_search tool to research and provide:

1. **Weather & Climate**: Monthly temperature ranges, rainy/dry seasons, what to pack.

2. **Estimated Costs** (per day in USD):
   - Budget traveler: accommodation, food, transport, activities
   - Mid-range traveler: accommodation, food, transport, activities
   - Luxury traveler: accommodation, food, transport, activities

3. **Visa Requirements**: Requirements for US passport holders (and note if different for other nationalities).
   Include processing time and fees.

4. **Safety**: Overall safety rating, areas to avoid, common scams, emergency numbers.

5. **Local Transport**:
   - Getting from the airport to city center (options and costs)
   - Public transit overview (metro, bus, etc.)
   - Taxis/rideshare availability and typical costs
   - Search for image URLs of local transport options (metro maps, etc.)

6. **Connectivity**: SIM card options, WiFi availability, power plug type.

7. **Health**: Required/recommended vaccinations, water safety, travel insurance notes.

Perform multiple searches for accurate, current information. Include image URLs for transport options.
Format your response as structured text with clear headings.
"""
```

**Step 4: Create logistics_agent agent.py**

```python
# travel_research/sub_agents/logistics_agent/agent.py
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
```

**Step 5: Create logistics_agent __init__.py**

```python
# travel_research/sub_agents/logistics_agent/__init__.py
"""Logistics agent for practical travel information."""

from .agent import logistics_agent
```

**Step 6: Run tests**

Run: `python -m pytest tests/test_agent.py -v`
Expected: ALL PASS

**Step 7: Commit**

```bash
git add travel_research/sub_agents/logistics_agent/ tests/test_agent.py
git commit -m "feat: add logistics_agent sub-agent"
```

---

### Task 5: Itinerary Agent

**Files:**
- Create: `travel_research/sub_agents/itinerary_agent/__init__.py`
- Create: `travel_research/sub_agents/itinerary_agent/prompt.py`
- Create: `travel_research/sub_agents/itinerary_agent/agent.py`
- Modify: `tests/test_agent.py`

**Step 1: Write the test**

Append to `tests/test_agent.py`:

```python
from travel_research.sub_agents.itinerary_agent import itinerary_agent


def test_itinerary_agent_exists():
    assert itinerary_agent is not None
    assert itinerary_agent.name == "itinerary_agent"


def test_itinerary_agent_has_google_search_tool():
    assert len(itinerary_agent.tools) > 0
```

**Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_agent.py::test_itinerary_agent_exists -v`
Expected: FAIL with ImportError

**Step 3: Create itinerary_agent prompt.py**

```python
# travel_research/sub_agents/itinerary_agent/prompt.py
"""Prompt for the itinerary agent."""

ITINERARY_AGENT_PROMPT = """
You are a travel itinerary planning specialist. Your job is to create a detailed
day-by-day itinerary for a trip to a destination.

You have access to research already gathered about the destination:
- Destination overview: {destination_overview}
- Attractions and experiences: {attractions_info}
- Logistics and practical info: {logistics_info}

The trip duration is {trip_duration} days. If not specified, default to 3 days.

Using the research above and the google_search tool for any additional details, create:

**Day-by-Day Itinerary:**

For each day, provide:
- **Day N: [Theme]** (e.g., "Day 1: Historic City Center")
- **Morning** (2-3 activities): What to do, estimated time, tips
- **Lunch**: Restaurant or food recommendation with location
- **Afternoon** (2-3 activities): What to do, estimated time, tips
- **Dinner**: Restaurant recommendation with cuisine type and price range
- **Evening** (optional): Nightlife, shows, or relaxation suggestions

**Planning Notes:**
- Group nearby attractions together to minimize travel time
- Include transport suggestions between locations
- Note any attractions that require advance booking
- Balance popular sites with hidden gems
- Consider opening hours and best times to visit

Be specific with names, addresses, and practical details.
Format as structured text with clear day-by-day headings.
"""
```

**Step 4: Create itinerary_agent agent.py**

```python
# travel_research/sub_agents/itinerary_agent/agent.py
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
```

**Step 5: Create itinerary_agent __init__.py**

```python
# travel_research/sub_agents/itinerary_agent/__init__.py
"""Itinerary agent for day-by-day travel planning."""

from .agent import itinerary_agent
```

**Step 6: Run tests**

Run: `python -m pytest tests/test_agent.py -v`
Expected: ALL PASS

**Step 7: Commit**

```bash
git add travel_research/sub_agents/itinerary_agent/ tests/test_agent.py
git commit -m "feat: add itinerary_agent sub-agent"
```

---

### Task 6: PDF Generator Tool

**Files:**
- Create: `travel_research/tools/pdf_generator.py`
- Create: `tests/test_pdf_generator.py`

**Step 1: Write the test**

```python
# tests/test_pdf_generator.py
"""Tests for the PDF generator tool."""

import json
import os

from travel_research.tools.pdf_generator import generate_pdf_report


def test_generate_pdf_creates_file(tmp_path):
    report_data = {
        "destination": "Tokyo, Japan",
        "overview": "Tokyo is the capital of Japan, a vibrant metropolis blending tradition and modernity.",
        "attractions": [
            {"name": "Senso-ji Temple", "description": "Ancient Buddhist temple in Asakusa."},
            {"name": "Shibuya Crossing", "description": "The world's busiest pedestrian crossing."},
        ],
        "logistics": {
            "weather": "Mild springs, hot summers, cool autumns, cold winters.",
            "costs": "Budget: $80/day, Mid-range: $200/day, Luxury: $500+/day",
            "visa": "US citizens: 90-day visa-free entry.",
            "transport": "Excellent metro system. Suica card recommended.",
        },
        "itinerary": [
            {
                "day": 1,
                "theme": "Historic Tokyo",
                "activities": "Visit Senso-ji Temple, explore Asakusa, lunch at Nakamise-dori.",
            },
            {
                "day": 2,
                "theme": "Modern Tokyo",
                "activities": "Shibuya Crossing, Harajuku, Meiji Shrine, dinner in Shinjuku.",
            },
        ],
        "tips": [
            "Get a Suica card for easy transit.",
            "Carry cash - many places don't accept cards.",
        ],
        "image_urls": [],
    }

    output_path = str(tmp_path / "test_report.pdf")
    result = generate_pdf_report(json.dumps(report_data), output_path)
    assert os.path.exists(result)
    assert result.endswith(".pdf")
    assert os.path.getsize(result) > 0
```

**Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_pdf_generator.py -v`
Expected: FAIL with ImportError

**Step 3: Create pdf_generator.py**

```python
# travel_research/tools/pdf_generator.py
"""PDF report generator tool for travel research agent."""

import json
import os
import tempfile
from io import BytesIO

import requests
from fpdf import FPDF


class TravelReportPDF(FPDF):
    """Custom PDF class for travel reports."""

    def header(self):
        self.set_font("Helvetica", "B", 12)
        self.set_text_color(60, 60, 60)
        self.cell(0, 10, "Travel Research Report", align="C", new_x="LMARGIN", new_y="NEXT")
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")

    def add_section_title(self, title):
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(30, 80, 140)
        self.ln(5)
        self.cell(0, 10, title, new_x="LMARGIN", new_y="NEXT")
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(3)

    def add_subsection_title(self, title):
        self.set_font("Helvetica", "B", 12)
        self.set_text_color(50, 50, 50)
        self.ln(3)
        self.cell(0, 8, title, new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

    def add_body_text(self, text):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(40, 40, 40)
        self.multi_cell(0, 6, text)
        self.ln(2)

    def add_bullet_point(self, text):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(40, 40, 40)
        self.cell(5)
        self.cell(5, 6, chr(8226))
        self.multi_cell(0, 6, text)
        self.ln(1)

    def add_image_from_url(self, url, width=80):
        try:
            response = requests.get(url, timeout=10, stream=True)
            response.raise_for_status()
            content_type = response.headers.get("content-type", "")
            if "image" not in content_type:
                return
            img_data = BytesIO(response.content)
            ext = "jpg"
            if "png" in content_type:
                ext = "png"
            tmp = tempfile.NamedTemporaryFile(suffix=f".{ext}", delete=False)
            tmp.write(img_data.read())
            tmp.close()
            self.image(tmp.name, w=width)
            self.ln(3)
            os.unlink(tmp.name)
        except Exception:
            pass


def generate_pdf_report(report_data_json: str, output_path: str = "") -> str:
    """Generate a PDF travel report from structured data.

    Args:
        report_data_json: JSON string with keys: destination, overview, attractions,
            logistics, itinerary, tips, image_urls
        output_path: Optional path for the output PDF. If empty, generates in temp dir.

    Returns:
        The file path of the generated PDF.
    """
    data = json.loads(report_data_json)
    destination = data.get("destination", "Unknown Destination")

    if not output_path:
        output_path = os.path.join(
            tempfile.gettempdir(),
            f"travel_report_{destination.replace(' ', '_').replace(',', '')}.pdf",
        )

    pdf = TravelReportPDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=20)

    # Title
    pdf.set_font("Helvetica", "B", 24)
    pdf.set_text_color(20, 60, 120)
    pdf.ln(10)
    pdf.cell(0, 15, destination, new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.ln(5)

    # Hero image
    image_urls = data.get("image_urls", [])
    if image_urls:
        pdf.add_image_from_url(image_urls[0], width=120)

    # Overview
    overview = data.get("overview", "")
    if overview:
        pdf.add_section_title("Overview")
        pdf.add_body_text(overview)

    # Attractions
    attractions = data.get("attractions", [])
    if attractions:
        pdf.add_section_title("Top Attractions")
        for attr in attractions:
            name = attr.get("name", "")
            desc = attr.get("description", "")
            img = attr.get("image_url", "")
            pdf.add_subsection_title(name)
            pdf.add_body_text(desc)
            if img:
                pdf.add_image_from_url(img, width=80)

    # Logistics
    logistics = data.get("logistics", {})
    if logistics:
        pdf.add_section_title("Practical Information")
        for key, value in logistics.items():
            pdf.add_subsection_title(key.replace("_", " ").title())
            pdf.add_body_text(str(value))

    # Itinerary
    itinerary = data.get("itinerary", [])
    if itinerary:
        pdf.add_section_title("Day-by-Day Itinerary")
        for day in itinerary:
            day_num = day.get("day", "")
            theme = day.get("theme", "")
            activities = day.get("activities", "")
            pdf.add_subsection_title(f"Day {day_num}: {theme}")
            pdf.add_body_text(activities)

    # Tips
    tips = data.get("tips", [])
    if tips:
        pdf.add_section_title("Tips & Recommendations")
        for tip in tips:
            pdf.add_bullet_point(tip)

    pdf.output(output_path)
    return output_path
```

**Step 4: Run test to verify it passes**

Run: `python -m pytest tests/test_pdf_generator.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add travel_research/tools/pdf_generator.py tests/test_pdf_generator.py
git commit -m "feat: add PDF generator tool with fpdf2"
```

---

### Task 7: Report Agent

**Files:**
- Create: `travel_research/sub_agents/report_agent/__init__.py`
- Create: `travel_research/sub_agents/report_agent/prompt.py`
- Create: `travel_research/sub_agents/report_agent/agent.py`
- Modify: `tests/test_agent.py`

**Step 1: Write the test**

Append to `tests/test_agent.py`:

```python
from travel_research.sub_agents.report_agent import report_agent


def test_report_agent_exists():
    assert report_agent is not None
    assert report_agent.name == "report_agent"


def test_report_agent_has_pdf_tool():
    tool_names = [t.__name__ if callable(t) else str(t) for t in report_agent.tools]
    assert any("generate_pdf" in name for name in tool_names)
```

**Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_agent.py::test_report_agent_exists -v`
Expected: FAIL with ImportError

**Step 3: Create report_agent prompt.py**

```python
# travel_research/sub_agents/report_agent/prompt.py
"""Prompt for the report agent."""

REPORT_AGENT_PROMPT = """
You are a travel report compiler. Your job is to take all the research gathered by
other agents and compile it into a comprehensive, well-structured PDF travel report.

You have access to the following research in the conversation state:
- Destination overview: {destination_overview}
- Attractions and experiences: {attractions_info}
- Logistics and practical info: {logistics_info}
- Day-by-day itinerary: {itinerary}

Your task:
1. Parse all the gathered research into a structured format
2. Call the generate_pdf_report tool with a JSON string containing these keys:
   - "destination": The destination name (e.g., "Tokyo, Japan")
   - "overview": A concise destination overview paragraph
   - "attractions": A list of objects with "name", "description", and optionally "image_url"
   - "logistics": An object with keys "weather", "costs", "visa", "transport" (string values)
   - "itinerary": A list of objects with "day" (number), "theme" (string), "activities" (string)
   - "tips": A list of practical tip strings
   - "image_urls": A list of image URL strings for hero images (extracted from the research)

3. Return the PDF file path to the user with a brief summary of what's included.

Be thorough in extracting all relevant information from the research. Include all image URLs
found by the attractions and logistics agents.
"""
```

**Step 4: Create report_agent agent.py**

```python
# travel_research/sub_agents/report_agent/agent.py
"""Report agent for compiling research into a PDF report."""

from google.adk import Agent

from travel_research.shared_libraries.constants import MODEL
from travel_research.tools.pdf_generator import generate_pdf_report

from . import prompt

report_agent = Agent(
    model=MODEL,
    name="report_agent",
    description="Compiles all gathered research into a structured PDF travel report with visuals",
    instruction=prompt.REPORT_AGENT_PROMPT,
    output_key="final_report",
    tools=[generate_pdf_report],
)
```

**Step 5: Create report_agent __init__.py**

```python
# travel_research/sub_agents/report_agent/__init__.py
"""Report agent for PDF report compilation."""

from .agent import report_agent
```

**Step 6: Run tests**

Run: `python -m pytest tests/test_agent.py -v`
Expected: ALL PASS

**Step 7: Commit**

```bash
git add travel_research/sub_agents/report_agent/ tests/test_agent.py
git commit -m "feat: add report_agent sub-agent with PDF generation"
```

---

### Task 8: Root Agent & Orchestration

**Files:**
- Create: `travel_research/prompt.py`
- Create: `travel_research/agent.py`
- Create: `travel_research/__init__.py`
- Modify: `tests/test_agent.py`

**Step 1: Write the test**

Append to `tests/test_agent.py`:

```python
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
```

**Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_agent.py::test_root_agent_exists -v`
Expected: FAIL with ImportError

**Step 3: Create root prompt.py**

```python
# travel_research/prompt.py
"""Prompts for the root travel research agent."""

ROOT_AGENT_PROMPT = """
You are a Travel Research Agent. You help users research travel destinations and produce
a comprehensive PDF travel report with visuals and a day-by-day itinerary.

When a user asks about a destination, follow these steps in order:

<Step 1: Gather Input>
Extract the destination name from the user's message.
If a trip duration is specified (e.g., "5-day trip"), note it.
If no duration is specified, default to 3 days.
Confirm the destination with the user before proceeding.
</Step 1>

<Step 2: Destination Overview>
Transfer to search_agent to research the destination overview and key facts.
Wait for the search_agent to complete its research.
</Step 2>

<Step 3: Attractions Research>
Transfer to attractions_agent to research top attractions, dining, cultural experiences,
and hidden gems, along with image URLs.
Wait for the attractions_agent to complete its research.
</Step 3>

<Step 4: Logistics Research>
Transfer to logistics_agent to research weather, costs, visa requirements, safety,
transport options, and practical information with image URLs.
Wait for the logistics_agent to complete its research.
</Step 4>

<Step 5: Itinerary Planning>
Transfer to itinerary_agent to create a detailed day-by-day itinerary based on
the gathered research. The itinerary should cover {trip_duration} days.
Wait for the itinerary_agent to complete the itinerary.
</Step 5>

<Step 6: Report Generation>
Transfer to report_agent to compile all gathered research into a polished PDF report
with images. The report_agent will call the generate_pdf_report tool.
Wait for the report_agent to complete the PDF.
</Step 6>

<Step 7: Delivery>
Present the PDF file path to the user and provide a brief summary of the report contents.
Ask if they'd like to research another destination.
</Step 7>

Important:
- Always follow the steps in order (1 through 7)
- Do not skip any step
- Each sub-agent handles its own Google Search queries
- Wait for each agent to finish before moving to the next
"""
```

**Step 4: Create root agent.py**

```python
# travel_research/agent.py
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
```

**Step 5: Create __init__.py**

```python
# travel_research/__init__.py
"""Travel Research Agent: Multi-agent travel destination research with PDF reports."""

import os

from dotenv import load_dotenv

load_dotenv()

from . import agent  # noqa: E402
```

**Step 6: Run tests**

Run: `python -m pytest tests/test_agent.py -v`
Expected: ALL PASS

**Step 7: Commit**

```bash
git add travel_research/__init__.py travel_research/agent.py travel_research/prompt.py tests/test_agent.py
git commit -m "feat: add root agent with orchestration of 5 sub-agents"
```

---

### Task 9: Run Full Test Suite & Verify

**Step 1: Run all tests**

Run: `cd /Users/adityadeshpande/PycharmProjects/adk-samples/python/agents/travel-research && python -m pytest tests/ -v`
Expected: ALL PASS

**Step 2: Verify agent can be imported**

Run: `cd /Users/adityadeshpande/PycharmProjects/adk-samples/python/agents/travel-research && python -c "from travel_research.agent import root_agent; print(f'Agent: {root_agent.name}'); print(f'Sub-agents: {[sa.name for sa in root_agent.sub_agents]}')"`
Expected: Prints agent name and 5 sub-agent names

**Step 3: Final commit if any fixes needed**

```bash
git add -A
git commit -m "fix: resolve any test/import issues"
```
