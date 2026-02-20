# Google Trends Scraper

Find keywords with search patterns comparable to **The Epstein Files** scale.

This tool uses Google Trends data to identify keywords with:
- Similar average search interest
- Similar momentum/trend trajectory
- Similar breadth of related queries (= episode angles)
- Similar geographic distribution

## Installation

```bash
cd "/Users/adamlevy/Google Trends Scraper"
pip install -r requirements.txt
```

## Documentation

- `docs/getting-started/quick-start.txt` — quick command reference
- `docs/getting-started/setup.md` — installation and first-run setup
- `docs/implementation/implementation-summary.md` — architecture and implementation notes
- `world-war-iii/README.md` — World War III topic workspace (context, reports, data)

## Quick Start

### Research Mode: Compare Specific Keywords

Find keywords similar to your reference benchmarks:

```bash
# Compare keywords against Jeffrey Epstein-scale benchmarks
python scraper.py \
  --keywords "Harvey Weinstein,Theranos,Enron" \
  --reference "Jeffrey Epstein,Jeffrey Epstein Files" \
  --timeframe "today 12-m" \
  --geo US \
  --report \
  --open
```

This will:
1. Fetch 12-month Google Trends data for the keywords
2. Calculate similarity scores vs. your reference keywords
3. Generate an HTML report with charts
4. Open the report in your browser

### Discovery Mode: Find Trending Opportunities

Automatically analyze this week's trending searches:

```bash
python scraper.py --discover --geo US --report --open
```

This will:
1. Fetch trending searches for your region
2. Score each trend
3. Rank by opportunity potential
4. Generate a discovery report

## CLI Reference

### Keywords Research

```bash
python scraper.py --keywords "keyword1,keyword2,keyword3"
```

**Options:**
- `--keywords TEXT` — Comma-separated keywords (max 5 per request)
- `--reference TEXT` — Reference keywords for comparison (e.g., "Jeffrey Epstein")
- `--timeframe TEXT` — Timeframe (default: `today 12-m`)
  - `now 1-d` — Last 24 hours
  - `now 7-d` — Last 7 days
  - `today 1-m` — Last month
  - `today 12-m` — Last 12 months (default)
  - `today 5-y` — Last 5 years
- `--geo COUNTRY` — Country code (default: `US`)
  - Examples: `US`, `GB`, `CA`, `AU`
- `--report` — Generate HTML report (default: enabled)
- `--open` — Open report in browser
- `--csv` — Export data as CSV
- `--json` — Export data as JSON

### Discovery Mode

```bash
python scraper.py --discover --geo US
```

**Options:**
- `--discover` — Enable discovery mode (analyze trending searches)
- `--geo COUNTRY` — Country code (default: `US`)
- `--report` — Generate HTML report
- `--open` — Open report in browser

## Output

### HTML Reports

Located in `output/reports/`:
- **Summary Table** — Keywords ranked by similarity score
- **Interest Over Time** — Interactive line chart of search volume
- **Related Queries** — Top rising queries per keyword (episode ideas)
- **Regional Heat Map** — Where is interest concentrated?
- **Detailed Metrics** — Avg interest, momentum, breakout queries, etc.

### Data Exports

Located in `output/data/`:
- **CSV** — Raw interest and regional data
- **JSON** — Metrics summary for each keyword

## Metrics Explained

### Similarity Score (0-100)
Measures how similar a keyword is to your reference benchmarks:
- **70+** — Highly comparable (very similar scale)
- **50-70** — Moderately comparable
- **<50** — Less comparable

### Key Metrics per Keyword

| Metric | Meaning |
|--------|---------|
| **Avg Interest** | Average search volume (0-100 scale) over timeframe |
| **Max Interest** | Peak search volume during timeframe |
| **Momentum** | Trend direction: <1 = declining, 1 = flat, >1 = growing |
| **Related Queries** | Number of related search queries (breadth for episodes) |
| **Rising Queries** | Queries with recent upward momentum |
| **Breakout Queries** | Queries with sudden spike in interest |
| **Recent Peak** | Did interest peak in last 90 days? |

## Examples

### Example 1: Find Keywords at Epstein Files Scale

```bash
python scraper.py \
  --keywords "Hunter Biden Laptop,Crypto Collapse,FTX Scandal" \
  --reference "Jeffrey Epstein,Epstein Files" \
  --timeframe "today 12-m" \
  --geo US \
  --report \
  --open
```

This compares your candidate keywords against Epstein's search patterns over 12 months.

### Example 2: Discover Trending Opportunities This Week

```bash
python scraper.py --discover --geo US --report --open
```

Shows which trending searches have enough breadth for a long-form series.

### Example 3: Deep Dive on a Single Keyword

```bash
python scraper.py \
  --keywords "Theranos" \
  --timeframe "today 5-y" \
  --geo US \
  --csv \
  --json \
  --report
```

Exports 5-year data for detailed analysis + report.

## Rate Limiting

Google Trends enforces rate limits. This tool:
- **Caches results** — Subsequent runs use cached data (24-hour TTL)
- **Backoffs between requests** — 60-second sleep between API calls
- **Retries on failure** — Exponential backoff up to 3 attempts

If you hit a rate limit, wait a few minutes and try again. Cached data will be used if available.

## Caching

Data is cached in `.cache/` with a 24-hour TTL:
- Each keyword/timeframe/geo combo is cached separately
- Delete `.cache/` to force fresh data fetch
- Cache is read-only (no data loss risk)

## Known Limitations

1. **Max 5 keywords per request** — pytrends API limit. Tool batches larger requests.
2. **Google Trends data is aggregated** — Not absolute search counts, but relative (0-100) scale
3. **Some trending data is incomplete** — Not all regions/categories available
4. **Regional data** — Only available for single keyword comparisons

## Troubleshooting

### "Rate limited by Google Trends"
Wait 10-15 minutes, then retry. Use `--no-report` to skip slow operations.

### "No data retrieved"
- Keyword may not have enough search volume
- Try a broader timeframe (e.g., `today 5-y`)
- Try a different region

### Cache is stale
Delete the cache and refetch:
```bash
rm -rf .cache/
python scraper.py --keywords "keyword" --report
```

## Project Structure

```
Google Trends Scraper/
├── scraper.py        # Main CLI entry point
├── fetcher.py        # pytrends wrapper with rate limiting
├── analyzer.py       # Similarity scoring engine
├── reporter.py       # HTML report generator
├── config.py         # Configuration defaults
├── requirements.txt  # Python dependencies
├── docs/             # Project documentation and context
│   ├── getting-started/
│   ├── implementation/
│   └── context/
├── .cache/           # Cached API responses (auto-generated)
├── output/           # Generated reports and data exports
│   ├── reports/      # HTML reports
│   └── data/         # CSV/JSON exports
└── README.md         # This file
```

## Future Enhancements

- [ ] SEMrush integration for competition data
- [ ] Episode idea generation from related queries
- [ ] Playbook-style recommendation engine
- [ ] Batch processing (100+ keywords)
- [ ] Google Search Console integration
- [ ] Trending topic clustering by category

## License

Not specified. Use freely.
