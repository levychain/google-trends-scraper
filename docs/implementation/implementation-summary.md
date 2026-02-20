# Google Trends Scraper - Implementation Summary

## Overview

A command-line tool to **find keywords with search patterns comparable to The Epstein Files scale**.

Instead of finding "low-competition" keywords, this tool finds keywords that:
- Have similar **average search interest**
- Show similar **momentum/trend trajectory**
- Have similar **related-query breadth** (= episode potential)
- Are distributed in similar **geographic patterns**

Helps you identify the next long-form podcast opportunity before everyone else does.

---

## What Was Built

### Core Modules

| Module | Purpose |
|--------|---------|
| **scraper.py** | CLI entry point. Routes to research or discovery mode. |
| **fetcher.py** | pytrends wrapper with rate limiting, retries, and 24-hour caching. |
| **analyzer.py** | Similarity scoring engine. Compares keywords to reference benchmarks. |
| **reporter.py** | HTML report generation with interactive Plotly charts. |
| **config.py** | Configuration defaults (timeframes, thresholds, API limits). |

### Supporting Files

| File | Purpose |
|------|---------|
| **requirements.txt** | Python dependencies (pytrends, pandas, plotly, etc.) |
| **README.md** | User documentation with examples and CLI reference |
| **SETUP.md** | Installation and first-run guide |
| **output/** | Directory for reports and data exports (auto-created) |

---

## Key Features

### 1. Research Mode: Compare Keywords to Reference Benchmarks
```bash
python3 scraper.py \
  --keywords "Harvey Weinstein,Theranos,Enron" \
  --reference "Jeffrey Epstein,Epstein Files" \
  --timeframe "today 12-m" \
  --geo US \
  --report \
  --open
```

**What it does:**
- Fetches 12 months of Google Trends data
- Extracts metrics: avg interest, momentum, related queries, breakout signals
- Scores each keyword on similarity to reference benchmarks (0-100)
- Generates HTML report with interactive charts
- Outputs CSV/JSON exports

**Output:** `output/reports/research_[timestamp].html`

### 2. Discovery Mode: Find Trending Opportunities
```bash
python3 scraper.py --discover --geo US --report --open
```

**What it does:**
- Fetches today's trending searches
- Scores each trend for podcast potential
- Ranks by opportunity
- Generates discovery report

**Output:** `output/reports/discovery_[timestamp].html`

### 3. Data Export
```bash
python3 scraper.py --keywords "keyword" --csv --json
```

**What it does:**
- Exports raw metrics as JSON
- Exports time-series as CSV (for Sheets, Excel, etc.)

**Output:**
- `output/data/keyword_[timestamp].json`
- `output/data/keyword_[timestamp]_interest.csv`
- `output/data/keyword_[timestamp]_regions.csv`

---

## Similarity Scoring Algorithm

Each keyword is scored on 3 dimensions compared to reference benchmarks:

| Dimension | Weight | Calculation |
|-----------|--------|-------------|
| **Interest** | 35% | How close is avg search interest to reference? |
| **Momentum** | 35% | How similar is trend trajectory? |
| **Breadth** | 30% | How many related queries (episode angles)? |

**Score ranges:**
- **70+** — Highly comparable (strong podcast potential)
- **50-70** — Moderately comparable
- **<50** — Less similar to reference

Example:
- Jeffrey Epstein: avg_interest=62, momentum=1.2x, related_queries=847
- Theranos: avg_interest=58, momentum=1.1x, related_queries=823
- **Result:** 78/100 similarity → Strong match

---

## Rate Limiting & Caching

**Problem:** Google Trends rate limits after ~5 requests per minute.

**Solution:**

1. **24-hour cache** — Results cached to `.cache/` directory
2. **60-second backoff** — Automatic 60-second sleep between requests
3. **Exponential retry** — Up to 3 retries with backoff on 429/503 errors

**First run:** 5-10 seconds per keyword (depends on batch size)
**Subsequent runs:** <1 second (uses cache)

---

## Metrics Explained

### Per-Keyword Metrics

| Metric | Meaning | Range |
|--------|---------|-------|
| **avg_interest** | Average search volume | 0-100 |
| **max_interest** | Peak search volume | 0-100 |
| **momentum** | Trend direction (last 6mo / prior 6mo) | -∞ to +∞ |
| **related_queries** | Count of related search queries | 0-1000+ |
| **rising_queries** | Queries with upward momentum | 0-1000+ |
| **breakout_queries** | Queries with sudden spike | 0-100 |
| **recent_peak** | Peaked in last 90 days? | Yes/No |

### HTML Report Sections

1. **Summary Table** — Keywords ranked by similarity score
2. **Interest Over Time** — Interactive line chart (Plotly)
3. **Related Queries** — Top 10 rising queries per keyword (episode ideas)
4. **Regional Heat Map** — Where is interest concentrated?
5. **Detailed Metrics** — Full breakdown for each keyword

---

## CLI Reference

### Research Mode

```bash
python3 scraper.py --keywords "KEYWORDS" [OPTIONS]
```

**Options:**
- `--keywords TEXT` (required) — Comma-separated keywords (max 5)
- `--reference TEXT` — Reference keywords for comparison
- `--timeframe TEXT` — Timeframe (default: `today 12-m`)
  - `now 1-d` — Last 24 hours
  - `now 7-d` — Last 7 days
  - `today 1-m` — Last month
  - `today 12-m` — Last 12 months
  - `today 5-y` — Last 5 years
- `--geo COUNTRY` — Country code (default: `US`)
- `--report` — Generate HTML report (default: on)
- `--no-report` — Skip HTML report
- `--open` — Open report in browser
- `--csv` — Export data as CSV
- `--json` — Export data as JSON

### Discovery Mode

```bash
python3 scraper.py --discover [OPTIONS]
```

**Options:**
- `--geo COUNTRY` — Country code (default: `US`)
- `--report` — Generate HTML report
- `--open` — Open report in browser

---

## Installation & First Run

### 1. Install Dependencies
```bash
cd "/Users/adamlevy/Google Trends Scraper"
pip install -r requirements.txt
```

### 2. Verify Installation
```bash
python3 scraper.py --help
```

### 3. Run First Example
```bash
python3 scraper.py \
  --keywords "Theranos" \
  --reference "Jeffrey Epstein" \
  --geo US \
  --report \
  --open
```

---

## Project Structure

```
Google Trends Scraper/
├── scraper.py                    # Main CLI (entry point)
├── fetcher.py                    # pytrends wrapper + caching
├── analyzer.py                   # Similarity scoring engine
├── reporter.py                   # HTML report + chart generation
├── config.py                     # Configuration & defaults
├── requirements.txt              # Python dependencies
├── README.md                     # User documentation
├── SETUP.md                      # Installation guide
├── IMPLEMENTATION_SUMMARY.md     # This file
├── .cache/                       # Auto-generated: 24-hour cache
└── output/                       # Auto-created: output directory
    ├── reports/                  # HTML reports (.html)
    └── data/                     # CSV/JSON exports
```

---

## Examples

### Example 1: Find Alternatives to Theranos

```bash
python3 scraper.py \
  --keywords "Elizabeth Holmes Trial,Biomimicry Fraud,Medical Startup Scandal" \
  --reference "Theranos" \
  --timeframe "today 5-y" \
  --geo US \
  --report \
  --open
```

### Example 2: Deep Dive on Current Trending Topics

```bash
python3 scraper.py --discover --geo US --report --open
```

### Example 3: Compare Multiple Reference Topics

```bash
python3 scraper.py \
  --keywords "Wirefraud Case,Corporate Embezzlement,Financial Crime" \
  --reference "Jeffrey Epstein,Harvey Weinstein,Enron" \
  --timeframe "today 3-y" \
  --geo US \
  --csv \
  --json \
  --report
```

---

## Dependencies

All in `requirements.txt`:

| Package | Purpose |
|---------|---------|
| `pytrends` | Official Google Trends data fetching |
| `pandas` | DataFrame processing |
| `plotly` | Interactive HTML charts (no server required) |
| `jinja2` | HTML templating |
| `tenacity` | Retry logic with exponential backoff |
| `playwright` | Fallback browser automation |
| `requests` | HTTP utilities |

---

## Known Limitations

1. **Max 5 keywords per request** — pytrends API limit
   - Tool automatically batches larger requests
2. **Google Trends data is relative** — 0-100 scale, not absolute counts
3. **Rate limiting** — Google blocks after ~5 requests/minute
   - Tool handles with 60-second backoff + retries
4. **Regional data incomplete** — Not all regions have granular data
5. **Real-time trends lag** — Data is typically 24-48 hours behind

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'pytrends'"
**Solution:** Install dependencies
```bash
pip install -r requirements.txt
```

### "Rate limited by Google Trends"
**Solution:** Wait 10-15 minutes, then retry (uses cached data)
```bash
python3 scraper.py --keywords "same" --no-report
```

### "No data retrieved"
**Solution:** Try different keyword/timeframe/region
```bash
python3 scraper.py --keywords "keyword" --timeframe "today 5-y" --report
```

### Clear cache to force fresh data
```bash
rm -rf .cache/
python3 scraper.py --keywords "keyword" --report
```

---

## Next Steps

1. Install dependencies: `pip install -r requirements.txt`
2. Run a test: `python3 scraper.py --keywords "Theranos" --geo US --report`
3. Explore examples in `README.md`
4. Compare keywords to your reference benchmarks
5. Export data for deeper analysis

---

## Files

- **User docs:** `README.md`, `SETUP.md`
- **Code:** `scraper.py`, `fetcher.py`, `analyzer.py`, `reporter.py`, `config.py`
- **Dependencies:** `requirements.txt`
