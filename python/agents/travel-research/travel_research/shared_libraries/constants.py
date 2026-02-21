"""Shared constants for the travel research agent."""

import os

from dotenv import load_dotenv

load_dotenv()

MODEL = os.getenv("MODEL", "gemini-2.5-flash")
DEFAULT_TRIP_DURATION = 3
