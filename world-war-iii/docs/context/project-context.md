# Project Context

## Objective
Build a high-cadence, source-backed podcast engine around war/WW3-risk content (especially U.S.–Iran–Israel), using an Epstein-style strategy: depth + volume + connected narrative + keyword ownership.

## Key Strategic Decisions
- Release model:
  - Publish 60 connected "time-capsule" episodes at once.
  - Then publish 2 episodes/day for ~2.5-3 months.
- Product structure:
  - Time-capsule = frozen baseline narrative up to launch moment.
  - Live feed = ongoing updates and escalation analysis.
- Positioning:
  - SEO + editorial balance (query-first titles with narrative continuity).
  - Win by cadence and continuity, not just one-off commentary.

## Important Insights Saved
- Epstein playbook that worked:
  1. High-intent keyword cluster
  2. Unmatched publishing cadence
  3. Connected episode chain
  4. Source-backed evidence
- This same playbook is intended for the war vertical.
- Proven: 64 episodes dumped in one day for Epstein Files. Volume IS the moat.

## SEO Enhancement (2026-02-19)
- All 50 original titles rewritten for provocative, click-through-optimized framing.
- All keywords shifted from head terms (e.g., "world war 3") to ownable long-tail (e.g., "how close to world war 3").
- All hooks rewritten from dry descriptors to specific-stakes framing.
- 10 new episodes added (Ep 51-60) as "Global Picture" arc to fill keyword gaps:
  - WW3 safe countries, Baba Vanga 2026, China-Taiwan, nuclear fallout map, WW3 preparation, wartime investing, Cuban Missile Crisis parallel, NATO Article 5, North Korea, prediction markets.
- These gaps were identified via competitive SEO research showing high demand + low podcast competition in these keyword clusters.

## Timing Validation (2026-02-19)
Hard data confirming the window is open NOW:
- Iran partially closed Strait of Hormuz (Feb 17, 2026)
- Oil jumped 4% after VP Vance said strikes "on the table" (Feb 18, 2026)
- Polymarket: $402M+ traded across 62 active Iran markets
- "US strikes Iran by Dec 31, 2026" hit 83% probability on Polymarket (Jan 2026)
- BloombergNEF projects $91/barrel oil by Q4 if Iran exports disrupted
- Baba Vanga "WW3 in 2026" prediction went viral globally on TikTok/X
- Doomsday Clock at 89 seconds to midnight — new record
- Selective Service auto-registration changed Dec 2025 (18-26 males)

## Competitive Landscape (2026-02-19)
- No dominant WW3-specific podcast exists. The name is unclaimed.
- Adjacent space is stacked with institutional players (War on the Rocks, GZERO, Pod Save the World, CSIS) — credentialed but low-cadence and dry.
- The gap: accessible, anxiety-addressing, general-audience WW3 content. Nobody owns this.
- Independent creators CAN rank for long-tail keywords (proven by MIRA Safety ranking on Google page 1 for "world war 3 2026").

## Tooling and Analysis Status
- Google Trends scraper exists and is operational.
- Repo is live at: https://github.com/levychain/google-trends-scraper
- Initial similarity scoring was found to overstate comparability in some cases.
- Scoring fix applied in `analyzer.py`:
  - Stabilized momentum calculation.
  - Dynamic normalization (removed brittle constant behavior).
  - Added demand-ratio penalty to prevent low-demand terms scoring as highly comparable.
- Post-fix validation:
  - `mortgage rates` vs `Epstein` (US, 3m) now scores low, matching chart intuition.

## Reports/Artifacts Created
- Final keyword report (earlier runs):
  - `output/reports/final_report_2026-02-18.md`
- War vertical competitor/moat analysis:
  - `output/reports/war_vertical_competitive_report_2026-02-18.md`
- War series operating blueprint (sources, cadence, verification):
  - `output/reports/war_series_operating_blueprint_2026-02-18.md`
- 60-episode enhanced spreadsheet CSV:
  - `world-war-iii/data/time-capsule-60-episode-sheet.csv`
- Original 50-episode spreadsheet (archived):
  - `world-war-iii/data/time-capsule-50-episode-sheet.csv`
  - `output/reports/time_capsule_50_episode_sheet.csv`

## Source-of-Truth Direction
Adopt a tiered source model with confidence scoring:
- Tier 1: official/institutional primary sources
- Tier 2: structured event datasets
- Tier 3: regional media and analyst sources (cross-check required)
- On-air claim rule:
  - 1 Tier-1 source OR
  - 2 independent sources across tiers
- Mark uncertain claims as unconfirmed and maintain corrections log.

## Current Execution State
- 60-episode time-capsule sheet is ready (enhanced titles, keywords, hooks + 10 new gap-filler episodes).
- Timing validated by hard market/geopolitical data — window is open.
- Competitive gap confirmed — no dominant player in accessible WW3 podcast space.

## Recommended Immediate Next Steps
1. Attach source packet IDs in the 60-episode sheet to concrete links/doc sets.
2. Build Day 1-Day 14 live-feed calendar (2/day) with AM/PM formats.
3. Finalize source whitelist + confidence rubric as operating policy.
4. Stand up lightweight ingest pipeline for hourly claim collection + scoring.
