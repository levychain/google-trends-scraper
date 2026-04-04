# LLM Handoff Context

## Project
`/Users/adamlevy/Google Trends Scraper`

## Primary Goal
Launch a podcast content machine in the war/WW3-risk vertical (especially U.S.–Iran–Israel) using an Epstein-style strategy:
- depth
- high volume
- connected narrative chain
- keyword ownership

## User-Defined Publishing Model
- Publish **60 episodes at once** as a connected "time-capsule" baseline.
- Then publish **2 episodes/day** for ~2.5-3 months as a live feed.
- Time-capsule = snapshot of all relevant context up to launch.
- Live feed = rolling aggregation/analysis of new information.
- **Proven model:** User dumped 64 Epstein Files episodes in one day. Volume is the moat. Do not second-guess this strategy.

## Critical Strategy Notes (must preserve)
- Success pattern (from Epstein experience):
  1. pick high-intent keyword cluster
  2. out-publish competitors on cadence
  3. keep episodes connected and cumulative
  4. back claims with sources
- Objective is not generic commentary; objective is to own a content vertical via continuity + volume.

## SEO Approach (Updated 2026-02-19)
- All titles are provocative/click-optimized (specific claims, numbers, personal-stakes hooks).
- Keywords shifted from unwinnable head terms to ownable long-tail.
- Hooks written as specific stakes, not dry descriptors.
- 6 arcs: Foundations, Military-Intel, Flashpoints, U.S. Decision Room, Futures, Global Picture.
- Global Picture arc (Ep 51-60) fills keyword gaps: safe countries, Baba Vanga, China-Taiwan, nuclear fallout map, WW3 prep, wartime investing, Cuban Missile Crisis, NATO Article 5, North Korea, prediction markets.

## Timing Validation (2026-02-19)
- Iran partially closed Strait of Hormuz (Feb 17, 2026)
- Oil jumped 4% on Vance "strikes on the table" statement (Feb 18, 2026)
- Polymarket: $402M+ across 62 active Iran markets
- "US strikes Iran by Dec 31, 2026" hit 83% probability (Jan 2026)
- BloombergNEF projects $91/barrel oil by Q4 if Iran exports disrupted
- Baba Vanga "WW3 in 2026" viral on TikTok/X globally
- Doomsday Clock at 89 seconds — new record
- Selective Service auto-registration changed Dec 2025

## Competitive Landscape (2026-02-19)
- No dominant WW3 podcast exists. Name is unclaimed.
- Institutional players (War on the Rocks, GZERO, CSIS) are credentialed but low-cadence and dry.
- Gap: accessible, anxiety-addressing, general-audience WW3 content.
- Independent creators can rank for long-tail (MIRA Safety proven on Google page 1).

## Technical Status
- Repo: `https://github.com/levychain/google-trends-scraper`
- Scoring bug was discovered and fixed in `analyzer.py`.
- Fixes applied:
  - momentum computation stabilized
  - dynamic normalization replaced brittle constant behavior
  - demand-ratio penalty added to prevent false "comparability"
- Post-fix sanity checks align better with user Google Trends screenshots.

## Key Artifacts Already Created
- `world-war-iii/docs/context/project-context.md` (high-level project summary)
- `world-war-iii/data/time-capsule-60-episode-sheet.csv` (enhanced 60-episode plan — CURRENT)
- `world-war-iii/data/time-capsule-50-episode-sheet.csv` (original 50-episode plan — ARCHIVED)
- `output/reports/final_report_2026-02-18.md`
- `output/reports/war_vertical_competitive_report_2026-02-18.md`
- `output/reports/war_series_operating_blueprint_2026-02-18.md`
- `output/reports/time_capsule_60_enhanced.csv` (copy in output/reports)
- `output/reports/time_capsule_50_episode_sheet.csv` (original copy in output/reports)

## Source-of-Truth Direction
Use tiered sourcing + confidence scoring:
- Tier 1: official/institutional primary sources
- Tier 2: structured event datasets
- Tier 3: regional media/analysts (cross-check required)

Claim policy:
- Publish as confirmed only if:
  - 1 Tier-1 source, or
  - 2 independent sources across tiers
- Otherwise mark as unconfirmed.
- Maintain a corrections trail.

## Competitive Positioning (already analyzed)
- Existing shows are strong in either:
  - high-frequency brief updates, or
  - expert interview/deep dive formats.
- White space identified:
  - connected investigative escalation narrative with high cadence and explicit source confidence.

## Recommended Next Actions for the Next LLM
1. Attach source packet IDs in `time-capsule-60-episode-sheet.csv` to concrete links/doc sets.
2. Build Day 1-Day 14 live-feed plan (2/day):
   - AM update template (10-18 min)
   - PM analysis template (25-45 min)
3. Draft source whitelist policy document (`SOURCES_POLICY.md`) and confidence rubric table.
4. Implement lightweight ingest pipeline spec (feeds -> claims -> confidence -> episode hooks).

## Constraints / Preferences
- User wants practical output, minimal fluff.
- User prefers aggressive execution and volume.
- User wants editorial depth + SEO balance (query-first titles, connected storytelling).
- Do NOT give generic podcast advice. User has a proven non-standard strategy. Respect it.
