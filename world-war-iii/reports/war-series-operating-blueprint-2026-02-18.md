# War Series Operating Blueprint (50-at-once + 2/day)

Date: 2026-02-18

## Core thesis (saved)
The winning move is not just topic selection. It is:
1. high-intent keyword cluster,
2. unmatched publishing velocity,
3. connected narrative continuity,
4. evidence-backed sourcing.

This is the same structural advantage that worked in your Epstein catalog.

## Release model you defined
- Phase 1: 50 episodes published at once (time-capsule baseline).
- Phase 2: 2 episodes/day for ~75-90 days (live feed).
- Total catalog target over 2.5-3 months: ~200-230 episodes.

## Product architecture
- Episode type A (daily AM, 10-18 min): "What changed in last 12 hours"
- Episode type B (daily PM, 25-45 min): "Escalation analysis + implications"
- Weekly synthesis (optional 1x/week, 45-60 min): compresses narrative and improves bingeability.

## What traditional journalism cannot do (your edge)
Traditional desks optimize for article cycles and limited format depth.
Your edge is a machine that continuously:
- ingests multi-source signals,
- maps claims to an escalation graph,
- reuses context from prior episodes,
- publishes in connected sequence.

## Unique source stack (real-time + legit)
Use source tiers with confidence scoring.

### Tier 1: Primary institutional (highest trust)
- U.S. CENTCOM press releases: https://www.centcom.mil/MEDIA/PRESS-RELEASES/
- U.S. Treasury OFAC press and sanctions updates: https://home.treasury.gov/news/press-releases
- UKMTO maritime warnings: https://www.ukmto.org/ukmto-products/warnings
- EIA weekly petroleum data/release schedule: https://www.eia.gov/petroleum/supply/weekly/
- IAEA news/verification reporting: https://www.iaea.org/news

### Tier 2: Structured conflict/event data
- ACLED API (events + CAST forecasting): https://acleddata.com/api-documentation/getting-started
- ACLED CAST endpoint: https://acleddata.com/api-documentation/cast-endpoint
- GDELT global event/news stream (15-min updates): https://www.gdeltproject.org/data.html

### Tier 3: Geospatial/transport signal layer
- NASA FIRMS active fire/hotspot data: https://firms.modaps.eosdis.nasa.gov/content/active_fire/
- OpenSky (air traffic API/data): https://opensky-network.org/data/
- MarineTraffic APIs (paid/pro): https://support.marinetraffic.com/en/articles/9552659-api-services

### Tier 4: Regional and country-perspective sources (cross-check required)
- Times of Israel briefings: https://www.timesofisrael.com/podcasts/
- The Iran Podcast (Negar Mortazavi): https://anchor.fm/s/3145eda0/podcast/rss
- Iranian state/official media (for regime-position readouts, not stand-alone truth):
  - IRNA: https://www.irna.ir/
  - Tasnim: https://www.tasnimnews.com/en

### Tier 5: Humanitarian ground truth
- OCHA oPt humanitarian situation updates: https://www.ochaopt.org/
- UN OCHA / UNISPAL publication mirror: https://www.un.org/unispal/

## Verification protocol (must-have)
For any claim in script:
- Score source confidence 1-5.
- Require either:
  - one Tier-1 source, OR
  - two independent sources from different tiers.
- Label uncertain claims as "unconfirmed" on-air.
- Keep a public corrections log episode-to-episode.

## Editorial graph model (the moat)
Every claim enters a structured graph:
- Actor: U.S., Israel, Iran, proxies, third-party states
- Domain: military, cyber, maritime, energy, diplomacy, sanctions, humanitarian
- Trigger: event that changed state
- Confidence: 1-5
- Next likely move: 1-3 scenarios

Each new episode updates this same graph. This creates continuity no general-news show maintains.

## 50-episode time-capsule design
Make the 50 episodes a frozen baseline narrative:
1. origins and doctrine
2. proxy architecture
3. escalation ladder and red lines
4. maritime/energy chokepoints
5. nuclear timeline and inspection regime
6. U.S. domestic consequences (prices, markets, cyber risk)

Each episode closes with:
- "State of the board"
- "What would invalidate this analysis"
- "What to watch next"

## 2/day live-feed design (90-day example)
Daily cadence:
- 07:00-09:00 ET ingest and scoring
- 09:30 publish AM update
- 14:00-17:00 deep analysis
- 18:00 publish PM analysis

Weekly rhythm:
- Mon-Fri: 2/day
- Sat/Sun: optional alerts-only (if major movement)

## SEO + continuity packaging
Naming format:
- "US-Iran War Update D12-AM: [query phrase]"
- "US-Iran War Update D12-PM: [scenario phrase]"

Description format:
- Previous episode link
- Next episode placeholder
- Sources list
- Claim confidence notes

## Recommended KPI dashboard
- Search-entry rate (Spotify/YouTube/Apple)
- 24h and 7d episode completion
- Cross-episode continuation rate (E[n] -> E[n+1])
- Returning listener rate (7d/30d)
- Correction rate per 100 claims

## Immediate next step
Build a lightweight "war desk" data pipeline that auto-ingests 10-15 feeds every hour and outputs:
- top 20 new claims,
- confidence scores,
- candidate episode hooks.

That system is the equivalent of your "millions of files" advantage in this vertical.
