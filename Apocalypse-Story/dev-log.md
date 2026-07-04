# Apocalypse Story — Dev Log

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
