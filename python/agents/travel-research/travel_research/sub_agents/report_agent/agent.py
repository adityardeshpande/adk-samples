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
