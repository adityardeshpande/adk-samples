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
        self.cell(5, 6, "-")
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
