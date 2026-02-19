"""
Configuration defaults for Google Trends Scraper.
"""

import os
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).parent
OUTPUT_DIR = PROJECT_ROOT / "output"
REPORTS_DIR = OUTPUT_DIR / "reports"
DATA_DIR = OUTPUT_DIR / "data"
CACHE_DIR = PROJECT_ROOT / ".cache"

# Ensure directories exist
for d in [REPORTS_DIR, DATA_DIR, CACHE_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# Google Trends defaults
DEFAULT_TIMEFRAME = "today 12-m"  # Last 12 months
DEFAULT_GEO = "US"  # United States
DEFAULT_CATEGORY = 0  # All categories

# Rate limiting (pytrends hits rate limits quickly)
REQUEST_BACKOFF_SECONDS = 60  # Sleep between requests
RETRY_MAX_ATTEMPTS = 3
RETRY_EXPONENTIAL_BASE = 2

# Opportunity scoring weights (sum = 1.0)
OPPORTUNITY_WEIGHTS = {
    "avg_interest": 0.25,        # Average interest over period
    "momentum": 0.25,             # Trend momentum (slope)
    "breakout_queries": 0.20,     # Count of breakout queries
    "breadth": 0.15,              # Related query diversity
    "recency": 0.15,              # Peaked recently?
}

# Thresholds
MIN_AVG_INTEREST = 5  # Ignore keywords with avg interest < 5
MIN_BREAKOUT_QUERIES = 2  # Need at least 2 breakout queries for good score
MIN_RELATED_QUERIES = 5  # Need at least 5 related queries for diversity
RECENT_PEAK_DAYS = 90  # "Recent" = within last N days
MOMENTUM_THRESHOLD = 1.0  # Slope of last 6mo / prior 6mo

# Discovery mode
TRENDING_SEARCHES_LIMIT = 50  # Fetch top 50 trending searches
MIN_DISCOVERY_SCORE = 40  # Only return opportunities with score >= 40

# Pytrends API limits
MAX_KEYWORDS_PER_REQUEST = 5  # Pytrends can compare up to 5 keywords at once

# HTML report
REPORT_TEMPLATE_DIR = PROJECT_ROOT / "templates"
REPORT_TEMPLATE_DIR.mkdir(exist_ok=True)

# Data cache TTL (seconds)
CACHE_TTL_SECONDS = 86400  # 24 hours

# User agent for requests
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"

# SEMrush (optional, for validation)
SEMRUSH_API_URL = "https://api.semrush.com/"
