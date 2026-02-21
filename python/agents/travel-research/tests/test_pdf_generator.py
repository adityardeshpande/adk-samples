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
