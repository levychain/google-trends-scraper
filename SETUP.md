# Setup Guide

## Prerequisites

- Python 3.9+ (check: `python3 --version`)
- pip (check: `pip3 --version`)

## Installation

### 1. Install Dependencies

```bash
cd "/Users/adamlevy/Google Trends Scraper"
pip install -r requirements.txt
```

This installs:
- `pytrends` — Google Trends data fetching
- `pandas` — Data processing
- `plotly` — Interactive charts
- `jinja2` — HTML templating
- `tenacity` — Retry logic with backoff
- `playwright` — Fallback browser automation (if needed)
- `requests` — HTTP utilities

### 2. Verify Installation

```bash
python3 scraper.py --help
```

You should see the CLI help message. If you get import errors, pip install may not have completed. Try again:

```bash
pip install --upgrade -r requirements.txt
```

## First Run

### Example 1: Research Keywords Similar to Epstein Files

Compare candidate topics against Epstein's search patterns:

```bash
python3 scraper.py \
  --keywords "Theranos,Enron,Panama Papers" \
  --reference "Jeffrey Epstein,Epstein Files" \
  --timeframe "today 12-m" \
  --geo US \
  --report \
  --open
```

This will:
1. Fetch 12 months of Google Trends data
2. Compare your keywords vs. Epstein baseline
3. Show similarity scores and metrics
4. Generate an HTML report with charts
5. Open the report in your browser

**Output:** `output/reports/research_YYYY-MM-DD_HH-MM-SS.html`

### Example 2: Discover Trending Opportunities

Find trending topics with podcast potential:

```bash
python3 scraper.py --discover --geo US --report --open
```

This will:
1. Fetch today's trending searches
2. Score each trend
3. Show top opportunities
4. Generate a discovery report

**Output:** `output/reports/discovery_YYYY-MM-DD_HH-MM-SS.html`

## Rate Limiting

Google Trends rate limits aggressively. This tool:
- **Caches results** for 24 hours (`.cache/` directory)
- **Waits 60 seconds** between requests automatically
- **Retries 3 times** with exponential backoff on failure

First run will be slow. Subsequent runs for the same keywords will be instant.

## Output Files

### HTML Reports
- Location: `output/reports/`
- Open any `.html` file in your browser
- Contains interactive Plotly charts

### CSV/JSON Data
- Location: `output/data/`
- Use `--csv` and `--json` flags to export raw data

## Troubleshooting

### "ModuleNotFoundError: No module named 'pytrends'"
Dependencies not installed. Run:
```bash
pip install -r requirements.txt
```

### "Rate limited by Google Trends"
Wait 10-15 minutes. The tool caches data, so retry with cached data:
```bash
python3 scraper.py --keywords "same keyword" --report
```

### "No data retrieved"
Keyword may have insufficient search volume. Try:
- Different keyword
- Broader timeframe (`today 5-y` instead of `today 12-m`)
- Different region

### Clear cache to force fresh data
```bash
rm -rf .cache/
```

## Project Structure

```
Google Trends Scraper/
├── scraper.py              # Main CLI (entry point)
├── fetcher.py              # pytrends wrapper
├── analyzer.py             # Similarity scoring
├── reporter.py             # HTML report generation
├── config.py               # Configuration
├── requirements.txt        # Dependencies
├── README.md               # User documentation
├── SETUP.md                # This file
├── .cache/                 # Auto-generated cache (24-hour TTL)
└── output/
    ├── reports/            # Generated HTML reports
    └── data/               # CSV/JSON exports
```

## Next Steps

1. **Run first example:** `python3 scraper.py --keywords "test" --geo US --report`
2. **Compare to references:** `python3 scraper.py --keywords "keyword1,keyword2" --reference "Jeffrey Epstein" --report`
3. **Explore discovery:** `python3 scraper.py --discover --geo US --report`
4. **Export data:** `python3 scraper.py --keywords "keyword" --csv --json`

## Questions?

See `README.md` for detailed documentation and examples.
