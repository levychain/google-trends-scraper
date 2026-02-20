# Source Curation Guide for 60-Episode WW3 Vertical

## Overview
Each episode has a unique `Source_Packet_ID` mapped to a set of primary and secondary sources. Sources are organized by type and confidence tier.

## Source Types

### Tier 1: Official Sources (Highest Confidence)
- US Government (State Dept, Defense Dept, Congress CRS, CIA declassified)
- Allied Governments (UK FCO, Israeli government, EU official statements)
- International Organizations (UN, NATO, International Court)
- Academic Institutions (Harvard, Stanford think pieces)
- Established Think Tanks (CSIS, CFR, Brookings, RAND, ISW)

### Tier 2: Structured Data & Primary Sources
- Market Data (Polymarket, oil futures, currency markets)
- Government Datasets (ACLED, SIPRI, World Bank)
- News Archives (Reuters, AP, Bloomberg, BBC, FT)
- Academic Papers (peer-reviewed on conflict, economics, policy)

### Tier 3: Expert Commentary & Analysis
- Op-eds by established experts
- Industry analysis (energy, defense, economic)
- Video analysis from credentialed analysts

### Tier 4: General Reference (Use Sparingly)
- News commentary
- Social media analysis (if it's a story about public perception)

## Arc-Based Source Strategy

### Arc 1: Foundations (EP1-10)
**Theme:** Baseline facts about capabilities, doctrine, escalation theory

Source Focus:
- Military capability assessments (Pentagon, NATO, CSIS)
- Doctrine documents (Iranian, Israeli, US)
- Escalation theory (RAND, think tanks)
- Real-time market data (Polymarket)

Key Sources to Prioritize:
- CSIS reports on Iran military
- Council on Foreign Relations Iran analysis
- Congressional Research Service (CRS) briefings
- BloombergNEF energy analysis
- ACLED conflict database

### Arc 2: Military-Intel (EP11-20)
**Theme:** Specific weapons, capabilities, intelligence operations

Source Focus:
- Weapons system specifications (unclassified)
- Defense journals and publications
- Intelligence community analysis (declassified)
- Technical assessments from defense contractors

Key Sources:
- Jane's Defence Weekly
- Center for Strategic and International Studies (CSIS) weapons reports
- Congressional testimony
- ISW (Institute for the Study of War)

### Arc 3: Flashpoints (EP21-30)
**Theme:** Specific crisis scenarios and trigger points

Source Focus:
- News reporting on recent incidents
- Energy market analysis (for Hormuz)
- Trade/commerce impact studies
- Military base assessments

Key Sources:
- Recent news (Reuters, Bloomberg, FT)
- Energy consulting firms
- Port authority reports
- Military readiness assessments

### Arc 4: Global Impact (EP31-40)
**Theme:** Economic and strategic consequences

Source Focus:
- Economic impact models
- Supply chain analysis
- Market projections
- Strategic studies

Key Sources:
- Goldman Sachs, McKinsey economic models
- Industry association reports
- SIPRI (military spending)
- Trade data sources

### Arc 5: Scenarios & Models (EP41-50)
**Theme:** Hypothetical war game scenarios and outcomes

Source Focus:
- Military war games (unclassified summaries)
- Think tank scenario modeling
- Historical parallels (Cuban Missile Crisis, etc.)
- Strategic analysis

Key Sources:
- War game reports (RAND, CSIS, Naval War College)
- Historical case studies
- Academic war gaming literature

### Arc 6: Global Picture & Lookout (EP51-60)
**Theme:** Broader geopolitical context and future outlook

Source Focus:
- Long-term strategic analysis
- Emerging market analysis
- Demographic/trend analysis
- Alternative scenarios

Key Sources:
- McKinsey Global Institute
- Stratfor
- Academic geopolitical analysis
- Future studies research

## Curation Workflow

### Step 1: Assign Sources by Arc
For each episode in an arc, assign sources from that arc's source list.

### Step 2: Verify Source Quality
- Check that links are live and accessible
- Confirm sources support the episode claim
- Verify publication date is recent (within 2-3 years for general analysis, weeks for news)

### Step 3: Rate Confidence
- **TIER_1:** Government/institutional primary sources
- **TIER_2:** News + structured data + academic analysis
- **TIER_3:** Expert commentary + secondary sources
- **PENDING:** Sources not yet curated

### Step 4: Document Curation
Record in `source_packet_registry.json`:
- `confidence_tier`: One of TIER_1, TIER_2, TIER_3, PENDING
- `verified`: Boolean (true if all links checked)
- `curated_by`: Name of person/AI that curated
- `last_updated`: ISO date

## Priority Order for Completion

1. **Critical Path (EP1-10, Foundations Arc)** ← START HERE
   - Establish baseline facts
   - Foundation for all other episodes
   - Sources most likely to be stable

2. **Military-Intel Arc (EP11-20)**
   - High technical content
   - Requires defense policy expertise
   - Sources feed into scenarios

3. **Flashpoints Arc (EP21-30)**
   - Most current/news-based
   - Sources will change frequently
   - Critical for credibility

4. **Global Impact Arc (EP31-40)**
   - Economic analysis focus
   - Sources from consulting/finance
   - More standardized research

5. **Scenarios Arc (EP41-50)**
   - War games and modeling
   - Think tank heavy
   - Can use academic sources

6. **Global Picture Arc (EP51-60)**
   - Long-term analysis
   - Geopolitical strategy
   - Can use broader sources

## Source Categories by Topic

### Iran Military Capability
- Pentagon reports, CSIS Iran military assessments, SIPRI data
- Jane's Defence Weekly, ISW battlefield reports
- Congressional testimony on Iran threats

### Israel-Iran Conflict
- UN Security Council documents, declassified CIA assessments
- Israeli government statements, academic case studies
- Long-form historical analysis (Foreign Affairs, etc.)

### US Military Posture
- Department of Defense official statements
- Congressional Research Service reports
- Base readiness assessments

### Economic Impact
- BloombergNEF energy models
- Goldman Sachs economic forecasts
- Supply chain consulting reports (McKinsey, BCG)

### Cyber Threats
- CISA (Cybersecurity and Infrastructure Security Agency) reports
- Industry security briefings
- Academic cybersecurity research

### Nuclear Escalation
- Nuclear Threat Initiative (NTI)
- SIPRI nuclear data
- Academic nuclear deterrence theory

## Tools & Resources

- **ACLED:** https://www.acleddata.com/ (conflict event database)
- **SIPRI:** https://www.sipri.org/ (military & weapons data)
- **Polymarket:** https://polymarket.com/ (prediction markets)
- **CRS Reports:** https://crsreports.congress.gov/ (Congressional Research Service)
- **CSIS:** https://www.csis.org/ (major think tank)
- **ISW:** https://www.understandingwar.org/ (Institute for the Study of War)
- **CFR:** https://www.cfr.org/ (Council on Foreign Relations)
- **RAND:** https://www.rand.org/ (RAND Corporation reports)

## Quality Checklist for Each Source

- [ ] URL is live and accessible
- [ ] Content actually supports episode claim
- [ ] Publication date is recent enough
- [ ] Source is from Tier 1 or 2 authority (ideally)
- [ ] Not paywalled or subscription-only (unless noting that)
- [ ] At least one source per category when possible

## Current Status

- **Completed:** 5/60 packets (Foundations Arc, partial)
- **In Progress:** Source curation template created
- **Pending:** 55 packets require source assignment

## Next Steps

1. Complete Foundations Arc (EP1-10) — ~2 hours
2. Complete Military-Intel Arc (EP11-20) — ~2 hours
3. Complete remaining arcs in priority order
4. Verify all URLs (quality assurance pass)
5. Export to publishing format for integration

---

Last Updated: 2026-02-19
