# Keyword Engine — Multi-Series Research Guide

The Keyword Engine has been expanded to support all NBN podcast series using YAML configuration files. Each series has its own config with customized keywords, intent domains, and research parameters.

## Quick Start

### 1. War Desk — Geopolitical Research

```bash
cd "Google Trends Scraper"
source venv/bin/activate

# Discovery mode (analyze trends, no report)
python3 run_mvp.py --config configs/wardesk.yaml --discovery-only

# Full analysis with HTML report
python3 run_mvp.py --config configs/wardesk.yaml --open
```

**Intent Domain:** Geopolitics, military strategy, international relations, NATO, sanctions, nuclear threats

**Seed Keywords:** Iran conflict, Ukraine war, China military, Middle East tension, NATO expansion, nuclear threat, trade sanctions, defense spending, military intelligence, geopolitical crisis

---

### 2. Neurodivergent — Psychology & Neurodiversity Research

```bash
python3 run_mvp.py --config configs/neurodivergent.yaml --discovery-only

python3 run_mvp.py --config configs/neurodivergent.yaml --open
```

**Intent Domain:** Neurodiversity, ADHD, autism spectrum disorder, dyslexia, mental health, learning differences, neuroscience

**Seed Keywords:** ADHD, autism, Elon Musk neurodivergent, Alex Karp autism, Lady Gaga mental health, neurodivergent entrepreneur, ADHD diagnosis adult, autism spectrum, executive function, dyslexia, hyperfocus, sensory processing

**Notable Figures:** Elon Musk, Alex Karp, Lady Gaga, Bill Gates, Albert Einstein, Steve Jobs

---

### 3. The First Yes — Startup & VC Research

```bash
python3 run_mvp.py --config configs/firstyes.yaml --discovery-only

python3 run_mvp.py --config configs/firstyes.yaml --open
```

**Intent Domain:** Startups, founders, venture capital, entrepreneurship, Series A, product-market fit, angel investors

**Seed Keywords:** Startup funding, venture capital, founder story, Series A funding, startup pitch, product market fit, angel investor, tech startup, startup ecosystem, early stage startup, startup success, entrepreneur

---

## Understanding the Output

When you run a discovery analysis, the Keyword Engine will:

1. **Fetch data** from Google Trends for seed keywords
2. **Score opportunities** based on:
   - Average interest (how much search volume)
   - Momentum (slope of trend over time)
   - Breakout queries (sudden spikes in related searches)
   - Breadth (diversity of related queries)
   - Recency (did the peak happen recently?)

3. **Report results** ranked by opportunity score

```
📊 Opportunity Scores for War Desk:
────────────────────────────────────────────────────────────────
  Ukraine war                                      Score: 78.3
  China military                                   Score: 72.1
  Iran conflict                                    Score: 65.4
  Middle East tension                              Score: 61.2
  NATO expansion                                   Score: 58.9
────────────────────────────────────────────────────────────────
Found 5 opportunities with score >= 40
```

### Interpreting Scores

- **80+:** High-velocity trend, strong momentum, trending globally
- **60–80:** Good opportunity, solid search volume, rising interest
- **40–60:** Emerging opportunity, niche interest, potential growth
- **Below 40:** Low velocity, not recommended for immediate production

---

## Configuration Format

Each config file (`.yaml`) contains:

```yaml
series: "Series Name"                    # Display name
description: "..."                        # Short description
anchors: [keyword1, keyword2]            # Primary search anchors
intent_domain: "..."                     # Semantic intent for relevance
trending_categories: [3, 14]             # Google Trends category IDs
seed_keywords: [...]                     # Keywords to research
reference_keywords: [...]                # Comparison benchmarks
min_momentum: 1.5                        # Minimum trend velocity
min_avg_interest: 8                      # Minimum search volume
discovery_limit: 50                      # Max trending searches to analyze
```

To customize a config, edit the `.yaml` file directly. Changes take effect on the next run.

---

## Daily Workflow (How to Use Keyword Engine)

### Each Day:

1. **Pick a series** (War Desk, Neurodivergent, The First Yes)

2. **Run discovery** to see what's trending:
   ```bash
   python3 run_mvp.py --config configs/wardesk.yaml --open
   ```

3. **Review the report** — topics with scores 60+ are greenlit for production

4. **Create episode** based on highest-scoring opportunity

5. **Publish episode** — metadata system ensures it ranks when shared on social

6. **Track in dashboard** — SEO keywords flow back to inform next research cycle

---

## API Budget & Rate Limits

Google Trends uses **unauthenticated requests** via pytrends. Be aware:

- **Rate limits:** 1 request per ~60 seconds per IP
- **Backoff:** Script automatically waits when limited
- **Cache:** Results cached locally for 24 hours to reduce API calls
- **Discovery mode:** Most expensive (hits API for each keyword)

### Tips:

- Use `--discovery-only` during development (skips expensive report generation)
- Run once per day per series (results are cached)
- Stagger series runs to avoid rate limit exhaustion

---

## Creating New Series Configs

To add research for a new NBN series:

1. **Create new YAML file:**
   ```bash
   cp configs/wardesk.yaml configs/my-series.yaml
   ```

2. **Edit the config** with your series' intent domain, keywords, and benchmarks

3. **Test it:**
   ```bash
   python3 run_mvp.py --config configs/my-series.yaml --discovery-only
   ```

4. **Commit the config** so the team can run it

---

## Technical Details

### Architecture

- **run_mvp.py** — Main entry point, loads YAML configs
- **scraper.py** — Google Trends fetcher and analyzer (original)
- **fetcher.py** — Cached API calls with rate limiting
- **analyzer.py** — Keyword scoring and opportunity ranking
- **reporter.py** — HTML report generation

### Data Flow

```
YAML Config
    ↓
run_mvp.py (parse config)
    ↓
CachedFetcher (fetch from Google Trends / use cache)
    ↓
KeywordAnalyzer (score opportunities)
    ↓
HTMLReporter (generate dashboard)
    ↓
Browser (view results)
```

### Cache Location

Results cached in `.cache/` directory (24-hour TTL). To force a fresh fetch:

```bash
rm .cache/*.json
```

---

## Troubleshooting

### "Rate limit backoff: sleeping X seconds"

Normal behavior. The script automatically waits. Don't interrupt it.

### "No data retrieved from Google Trends"

Possible causes:
- Keyword too niche or misspelled
- Geographic region has no data for that keyword
- API rate limited multiple times

**Solution:** Try with broader keywords or wait a few hours before retrying.

### "Config file not found"

Make sure you're running from the Google Trends Scraper directory:

```bash
cd "/Users/adamlevy/Google Trends Scraper"
```

And config file path is relative to current directory:

```bash
python3 run_mvp.py --config configs/wardesk.yaml
```

### "ModuleNotFoundError: No module named 'yaml'"

Install PyYAML:

```bash
source venv/bin/activate
pip install pyyaml
```

---

## Next: Integration with NBN Site

Once the Keyword Engine identifies trending opportunities:

1. **Create episode** with Keyword Engine insight
2. **Generate episode content** (NotebookLM, scripts, etc.)
3. **Publish to Buzzsprout** — episode URL generated
4. **SEO system activates** — per-page metadata ensures ranking
5. **Redeploy NBN site** — sitemap updates with new episode
6. **Social sharing works** — episode-specific OG tags (via prerender)

The full loop: **Keyword Engine → Production → Metadata System → Search Rankings → Traffic**

---

## Files

```
Google Trends Scraper/
├── run_mvp.py                          ← Main multi-series runner (NEW)
├── configs/
│   ├── wardesk.yaml                    ← War Desk config (NEW)
│   ├── neurodivergent.yaml             ← Neurodivergent config (NEW)
│   └── firstyes.yaml                   ← The First Yes config (NEW)
├── scraper.py                          ← Google Trends fetcher
├── analyzer.py                         ← Keyword scoring
├── reporter.py                         ← HTML report generation
├── fetcher.py                          ← Cached API client
├── config.py                           ← Generic defaults
├── requirements.txt                    ← Dependencies (updated with pyyaml)
└── .cache/                             ← Cached results (24hr TTL)
```

---

## Questions?

Check the original `README.md` for more details on Google Trends API, caching, or report interpretation.
