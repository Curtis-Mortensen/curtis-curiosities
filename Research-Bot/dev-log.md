# Apocalypse Story — Dev Log

## 2026-07-09 — Slavic Baptist Hymnals & Russian Worship on Apple Music (complete)

### Plan summary
User attends a Slavic Baptist Church, wants more Russian hymns on Apple Music, and does not have a printed hymnal. Research standard hymnal(s), searchable song list, and top traditional + contemporary Russian worship per Research-Bot instructions.

### Precursor / subset questions identified
1. Is there one canonical hymnal or several coexisting editions?
2. How do diaspora (US) hymnals differ from post-Soviet standard books?
3. What is the relationship between Песнь Возрождения and Prokhanov’s Гусли/Десятисборник?
4. How do Slavic Baptist hymns differ from Russian Orthodox liturgical chant?
5. What is actually findable on Apple Music vs lyrics-only apps?
6. Which contemporary artists serve Slavic evangelical churches?

### Key findings
- **Standard hymnal:** *Песнь Возрождения* (Song of Revival); 3,300-hymn edition most common digitally; numbers 1–830 stable across editions.
- **Diaspora:** *Russian-American Hymnal* (1994, Daniel Jasko, RU-Ukrainian Baptist Union USA).
- **Related but distinct:** *Гимны веры христиан* (Slavic Pentecostal); official 1956 VSEKhB book largely superseded.
- **Apple Music:** No single official PV album; search Russian titles or artists (Sharikov Family Band, Moscow Worship Band, NG Worship, RussiaWorship/SDG, M.Worship, Veselov, Nikitin).
- **Free hymnal substitute:** pesnvozrozhdeniya.com, hvalite.com, PV iOS apps, Internet Archive MP3 collections.

### Changes made
- Created `Research-Bot/slavic-baptist-russian-hymns-apple-music.html` — full report with hymnal history, thematic index, 55+ searchable songs, traditional/contemporary lists, Apple Music workflow, 29 references.

### Assumptions
- User’s church is Slavic Baptist or closely related evangelical (not Orthodox); Orthodox tradition noted separately for clarity.
- “Top” contemporary list based on ministry catalogs and platform presence, not chart data.

### Bugs / problems
- None during research or document creation.
## 2026-07-10 — Idaho Falls → SLC Cheap Sunday Transport (complete)

### Plan summary
User needs cheapest options to get from Idaho Falls to Salt Lake City on Sunday (interpreted as 2026-07-12), open to Turo and any other solutions including Allegiant discounts/coupons/bundles. Delivered as Research-Bot self-contained HTML per README instructions.

### Precursor / subset questions identified
1. Need a car in SLC, or only transport IDA→SLC?
2. Airport vs town pickup?
3. Same-day one-way vs multi-day?
4. Allegiant flyer status / partner rate eligibility?
5. Costco/AAA/USAA/BJ’s memberships?
6. Bus/shuttle or ride-board viable?
7. Can Turo do true one-way ~190 miles?

### Key findings
- **Cheapest if no car needed in SLC:** Salt Lake Express IDA→SLC Airport from ~$42 (book direct; Greyhound resells higher).
- **Best car path:** Traditional one-way rental (Enterprise/Alamo/National via Allegiant or Costco; Hertz stack via AAA). Drop fee dominates; Allegiant discount is base-rate only and does not waive one-way charges.
- **Turo:** Poor fit for true one-way — cannot select different return city at booking; host must approve later within delivery radius (SLC is far outside typical IDA radius).
- **Allegiant:** Partners Alamo/Enterprise/National; does not fly IDA→SLC (Delta does).
- **Gas floor:** ~$35 one-way if borrowing/owning a car (Travelmath, 217 mi).

### Changes made
- Created `Research-Bot/idaho-falls-slc-cheap-car-sunday.html` — ranked options, decision tree, Allegiant/Turo/discount deep dives, 28 references.

### Assumptions
- “Sunday” = next Sunday after research day Friday 2026-07-10 → 2026-07-12.
- Live Kayak/Expedia one-way checkout totals were not scrapable this session; used policy pages + aggregator secondary ranges.
- One-time Research-Bot question (not Apocalypse-Story series).

### Bugs / problems
- Aggregator search pages returned empty/JS shells; documented as methodology limitation rather than inventing locked prices.

### Status
**Complete**

---

## 2026-07-07 — Radio Repeater Technology Research (complete)

### Plan summary
User requested detailed research on radio repeater technology: Meshtastic/LoRa, GMRS, ham radio, and related bands — with Amazon makes/models, power draw, solar viability, DIY kits, popular guides, and cost comparisons sorted by category, range, and price. Initial response was chat-only; user asked to commit to Research-Bot.

### Precursor / subset questions identified
1. What legally counts as a "repeater" on each band (Meshtastic mesh vs. full-duplex voice)?
2. Which license-free bands prohibit repeaters (MURS, CB)?
3. Which Amazon hardware is community-validated vs. marketing hype?
4. What solar power budgets apply to nRF52840 vs. ESP32 Meshtastic nodes vs. GMRS RT97L?
5. When does DIY (Surecom controller + duplexer + mobiles) beat turnkey RT97L on cost?

### Key findings
- **Meshtastic:** RAK4631 solar relay (~$100–180) is cheapest credible hilltop node; height beats antenna gain (Avramut field data).
- **GMRS:** RT97L (~$535 Amazon) beats most DIY builds; draws up to 72 W on TX — needs 100–200 W solar for off-grid moderate use.
- **MURS/CB:** Repeaters explicitly illegal under FCC Part 95.
- **Ham:** SvxLink on Raspberry Pi remains dominant DIY path; Amazon strong for controllers/duplexers, weak for commercial repeaters.

### Changes made
- Created `Research-Bot/radio-repeater-technology.html` — self-contained HTML report with taxonomy, Amazon ASIN tables, solar sizing, DIY BOM comparisons, decision tree, 25 references.

### Assumptions
- US-centric (FCC, Amazon.com). Prices representative of 2025–2026 listings.
- Apocalypse Story relevance noted but not primary scope (one-time research question, not Apocalypse-Story series).

### Bugs / problems
- Prior chat response was never committed; corrected in this session.

### Status
**Complete**

---

## 2026-07-05 — Mesa Fireworks Viewing Guide (complete, updated for July 4 MST)

### Plan summary
User in Mesa, AZ asked where to drive tonight to see fireworks in Mesa, Tempe, Apache Junction, or Phoenix — ranked by display scale and parking difficulty. Initial draft used UTC date (July 5); user corrected that it is still July 4, ~8 PM in Arizona.

### Key finding
All major city-sponsored fireworks are happening TONIGHT (Saturday, July 4, 2026). At 8 PM MST from Mesa, best options: downtown Mesa Celebration of Freedom (fireworks 9:35 PM) or Tempe Diablo Stadium (~9:15 PM). Apache Junction (8:30 PM) and Hurricane Harbor (~8:45 PM) likely too late.

### Changes made
- Created `docs/mesa-fireworks-july-4-2026.html` — full research brief with go-now urgency guide at 8 PM, ranked catalog, venue profiles, drive times, 20 citations.
- Updated from July 5 "shows already over" to July 4 "leave now" guidance.

### Assumptions
- User departure point: central Mesa. Drive times are estimates.
- Fireworks/parking scores are editorial judgments from official sources and local media.

### Bugs / problems
- Initial version incorrectly assumed July 5 due to UTC/server timezone. Corrected per user feedback.

---

## 2026-07-04 — Question 6: Simulation Software (complete)

### Plan summary
Research open-source repositories and academic tools for simulating epidemic-driven societal collapse scenarios per README Question 6. Deliver self-contained HTML with two comparison tables, limitations, field history, and citations.

### Precursor / subset questions identified
1. What modeling paradigms exist (compartmental vs ABM vs hybrid vs infrastructure graph)?
2. Which tools are US-population-grounded vs global?
3. Which tools couple disease to infrastructure or social behavior?
4. What technology stacks dominate (Python/SciPy, C++/HPC, Julia, Rust, LLM APIs)?
5. What peer-reviewed software papers and surveys exist post-COVID?

### Changes made
- Created `docs/question-06-simulation-software.html` — full research report with:
  - Table 1: 42 open-source repositories compared
  - Table 2: 28 academic tools/methods compared
  - Taxonomy diagram, limitations, field history, Apocalypse Story mapping
  - 57 numbered references

### Coding decisions and assumptions
- **Scope:** Included epidemic ABMs, disaster/resilience platforms, and emerging civilization/LLM social sims because no single repo covers full collapse chain; noted integration gap explicitly.
- **Apocalypse fit ratings:** Subjective ★ scale based on US relevance, mortality/hospital modeling, and infrastructure/behavior coupling — documented as editorial judgment.
- **EpiSimdemics:** Listed in academic table as research/HPC tool without public GitHub repo (lab distribution).
- **Commercial tools:** AnyLogic noted in academic table only (not open source).
- **Stars/currency:** GitHub star counts mentioned only where stable; prioritized peer-reviewed citations over popularity.

### Bugs / problems
- None during document creation.
- Detached HEAD at conversation start; branched from `main` for PR.

### Status
**Complete** — Question 6 research artifact ready for human review.
## 2026-07-04 — Question 5: Definitive Predictions (Complete)

### Task
Research Question 5 from `README.md`: credible institutional predictions and frameworks for extreme crisis; rank reports and books by credibility/specificity.

### Precursor / subset questions identified
1. What counts as a "prediction" in this domain? (scenario vs. forecast)
2. Do governments have statutory frameworks?
3. Which bodies are best funded?
4. Which outputs are most specific to pandemic-driven societal collapse?
5. How do academic models differ from government reports?
6. Which popular books shape public expectations?
7. Can any framework be validated against real events?

### Key findings
- **No institution produces definitive point predictions** of societal collapse. Credible work uses scenario planning, reasonable worst-case analysis, stress testing, and strategic foresight.
- **Tier 1 (highest credibility):** RAND GCR Assessment (GCRMA 2022 mandate), UK NRR 2025, RAND biodefense "silent/fast/saturating" scenarios, GPMB 2019, Clade X, Dark Winter, FEMA THIRA, US National Planning Scenarios.
- **Tier 2:** OECD Emerging Critical Risks Framework, NIC Global Trends 2040, EU JRC NRA, UNDRR GRAF, GPMB 2025.
- **Tier 3:** Gambhir polycrisis framework (Nature Communications 2025), Cascade Institute PCM v2.5, SPARS, RAND synthetic pandemics.
- **For Apocalypse Story premise** (dormant 2–3 days, vomiting-stage spread, >50% mortality): RAND "silent scenario" is the closest institutional match. No Tier 1 source models 50–90% population loss in developed nations as a planning assumption.
- **Books:** Limits to Growth (~30M copies), Diamond's Collapse, Tainter, Ord's Precipice rank highest on combined academic respect and reach.

### Deliverable
- `docs/q5-definitive-predictions.html` — self-contained research document with CSS, diagrams, ranked tables (25 reports, 25 scenario exercises, 20 books), limitations, field history, 43 references.

### Assumptions
- Ranking criteria are composite (authority + methodology + specificity + validation); another agent might weight differently.
- Some exercises (Crimson Contagion, Event 201, Exercise Cygnus) included from secondary sources without deep primary-document review in this pass.
- WEF Global Risks Report included despite methodological criticism because of its high visibility and funding.

### Bugs / problems
- None encountered during research or document creation.

### Further research suggested (in document)
- Classified vs. public fatality estimates
- Reinsurance catastrophe models for pandemic tail risk
- COG plans under extreme personnel loss
- East Asian national risk frameworks

---

## 2026-07-04 — Q5 Follow-Up: Extinction-Level Synthesis (Complete)

### Task
Follow-up to Q5: deep-dive RAND GCR Assessment (asteroid, nuclear, pandemic extinction risks), summarize Precipice / Silent Scenario / Dark Winter / five books, synthesize agreement and disagreement.

### Deliverable
- `docs/q5-followup-extinction-synthesis.html` — synthesis overview of 8 sources
- README updated to mark follow-up complete

### Key synthesis findings
- RAND GCR: extinction possible from large asteroids, nuclear war, engineered pandemics; increasing risk is human-driven; asteroids best-quantified
- Silent Scenario: presymptomatic spread = hardest pandemic; vital-worker survival is the planning frame
- Dark Winter: healthcare/governance collapse in 13 days from moderate smallpox
- Books split: Ord (existential probability), Limits (overshoot), Diamond (preventable choices), Tainter (complexity economics), Wallace-Wells (climate cascades)
- Agreement: cascades matter, human decisions dominate, preparation lags
- Disagreement: extinction likelihood, whether collapse is rational, which threat dominates

### Assumptions
- "Five books" interpreted as Precipice + Limits to Growth + Collapse + Tainter + Uninhabitable Earth (top-ranked from Q5)
- RAND GCR PDF used via mirror (main RAND page shows "temporarily withdrawn")

---

## 2026-07-04 — Question 4: Breakdown of Law and Order

### Task
Research Question 4 from README: How quickly does law and order break down after crisis? Psychological studies, disaster vs. protest behavior, BLM lessons, case studies from developed nations (past 250 years).

### Precursor / subset questions identified
1. What counts as "breakdown" (looting vs. survival taking vs. riot)?
2. Disaster vs. catastrophe vs. civil disturbance distinction
3. Mass panic vs. elite panic
4. Do crime rates actually rise post-disaster?
5. Media/rumor role in perceived breakdown
6. Pre-existing conditions that predict breakdown
7. Escalation speed: riots (hours) vs. disasters (days)

### Research approach
- Web search across disaster sociology (Quarantelli, Dynes, DRC), crowd psychology (Drury, Reicher), ACLED protest data, econometric crime studies, and historical journalism
- Compiled 43 case studies from developed nations
- Synthesized into self-contained HTML report with embedded CSS

### Key findings (summary)
- **Typical disasters:** Prosocial behavior dominates; verified looting rare; crime often decreases
- **Riots/civil disturbances:** Escalation in hours; collective selective looting; grievance-driven
- **Catastrophes:** Breakdown possible in 24–72 hrs when infrastructure + governance fail together with pre-existing inequality
- **BLM 2020:** 94–95% peaceful; violence localized; agent provocateurs and disproportionate policing documented
- **Elite panic:** Authorities often cause more disruption than civilians (Tierney, Solnit, Clarke & Chess)

### Deliverable
- `docs/q4-breakdown-law-and-order.html` — full research report

### Assumptions
- "Developed nations" interpreted as industrialized, urbanized societies per disaster sociology literature
- Some case studies (Haiti 2010) included as comparative catastrophes despite not being "developed" — noted in document
- Events #29, #33–34, #37–38, #40–42 rely on secondary journalism where peer-reviewed field studies unavailable; flagged in case study table

### Bugs / problems
- None during research or document generation

### Status
Complete

---

---

## 2026-07-04 — Question 3: Human Inter-Reliance (Complete)

### Task
Research Question 3 from README: How many people in the US would likely die without care, medical attention, or medicine? What do disaster preparedness plans state? What has the US military and other institutions war-gamed?

### Deliverable
- `docs/question-3-human-inter-reliance.html` — self-contained research report with CSS, tiered acuity framework, 35 case studies, exercise summary table, scenario synthesis, and 67 references.

### Precursor / subset questions documented
- Definition of medical dependency (Rx vs DME vs facility vs skilled care)
- Time horizon (hours → years without care)
- Partial vs total infrastructure collapse
- Informal caregiver substitution
- Population overlap / double-counting

### Key findings (synthesis)
- No federal agency publishes a single "deaths without care" national estimate.
- HHS emPOWER tracks ~4.6M Medicare at-risk beneficiaries (electricity-dependent DME + essential home services); ~194M US adults have ≥1 chronic condition.
- High-acuity populations (dialysis ~517k, insulin-dependent ~2.1M+ Type 1, nursing homes ~1.24M, DME users) overlap substantially.
- Preparedness plans (NHSS, ASPR TRACIE, FEMA functional-needs guidance) emphasize surge and continuity of care, not total-collapse mortality modeling.
- Exercises (Dark Winter, Crimson Contagion, Clade X) model hundreds of thousands to millions of direct pathogen deaths and confirm zero surge capacity; they do not isolate care-disruption mortality.
- Real disasters (Maria, Katrina, Irma, Uri, COVID care avoidance) repeatedly show 20–33% of excess deaths linked to interrupted care.
- Defensible planning bracket for story work: additional 5–15% mortality among medically dependent survivors within 6 months if care/supply chains fail — highly scenario-sensitive.

### Assumptions made
- Used most recent available statistics (2022–2025 sources).
- Scenario mortality ranges in Section 9 are author synthesis, clearly labeled, not official forecasts.
- Living transplant recipient total (~400–500k) estimated from USRDS kidney transplant count + OPTN annual volumes; exact cumulative living recipient count not found in a single published figure.

### Bugs / problems
- None during document production.
- Git started in detached HEAD at d6a0d12; checked out `main` before branching.

### Coding decisions
- HTML/CSS only per README agent instructions; no build tooling.
- Placed report under `docs/` subdirectory (new) to keep README clean.
- Did not modify README or AGENTS.md.
## 2026-07-04 — Question 2: Psychology Under Existential Threat (COMPLETE)

### Plan summary
Research and document how humans react to existential danger, widespread panic, invasion, and flight — per README Question 2. Deliverable: self-contained HTML research report with diagrams, 20–50 case examples, field history, limitations, and conclusion.

### Precursor / subset questions identified
- Definitional: what counts as "panic" vs. rational flight, crush, or institutional failure
- Temporal: sudden vs. invisible/delayed threats (bomb vs. epidemic)
- Spatial: localized vs. diffuse threats
- Informational: trust in authorities and rumor dynamics
- Social: attachment figures and family clustering
- Institutional: organized vs. spontaneous evacuation

### Changes made
- Created `docs/question-2-psychology-existential-threat.html` — full research report (~42 case studies, 265 years, 70+ references)
- Created this `dev-log.md`

### Key findings (for cross-agent reference)
- Mass panic (irrational antisocial flight) is empirically rare per 60+ years of disaster sociology (Quarantelli/DRC)
- Default response: prosocial mutual aid, affiliative clustering, bounded rational flight
- Hiroshima/Nagasaki: shock, numbness, orderly "Ghost March" — not mass panic
- Cities facing invasion: denial → spontaneous mass flight; worst outcomes when infrastructure absent
- Epidemics: cognitive inertia → panic buying → selective migration (not stampedes)
- For the story's epidemic premise: expect inertia (days 1–3), hoarding/clustering (4–7), urban exodus (7–14), numbing + mutual aid (14+)

### Assumptions
- US-focused implications drawn from global evidence; gun ownership and political polarization noted as US-specific factors without deep research (flagged for Q4/Q5)
- 50%+ mortality epidemic has no exact historical parallel; 1918 and COVID extrapolated with explicit caveat

### Bugs / problems
- None during research or document creation

### Status
Complete

---

## 2026-07-04 — Question 4.1: Medium-Term Catastrophe Law and Order

### Task
Follow-up to Q4: medium/long-term breakdown and re-establishment of law and order after catastrophe; Haiti 2010 deep case study; violence under resource competition; prosocial factors; group consolidation dynamics. Cross-reference Q1 (pending) and Q4.

### Deliverables
- `docs/q4-1-catastrophe-law-order-medium-term.html` — full Q4.1 report
- Updated `README.md` follow-ups section
- Cross-link added in Q4 doc

### Key findings
- Five-phase model: Shock → Vacuum → Fragmentation → Competing authority → Reconsolidation/collapse
- Haiti: literal state collapse (27/28 govt buildings); 90%+ aid bypassed ministries; baz → gangs → federations → de facto rulers by 2021–24
- Prosocial behavior real but erodes 12–18 months without prosecution, fair aid, and state security
- Violence escalates when armed groups capture distribution, impunity total, political patrons arm factions
- Re-establishment requires legitimate monopoly on force — external intervention alone insufficient (MINUSTAH 2004–2017 failed to consolidate)

### Q1 cross-reference
Linked to `docs/q1-historical-parallels.html` — compound catastrophe lens; Haitian Revolution (#44), Thirty Years' War, Caribbean collapse parallels noted in Q4.1 comparative table.

### Assumptions
- Medium-term = months to 15+ years
- Haiti treated as primary catastrophe case despite not being "developed nation" — most complete modern dataset for state physical destruction + long follow-up

### Status
Complete
