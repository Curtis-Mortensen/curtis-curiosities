# Dev Log — Apocalypse Story

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
# Apocalypse Story — Dev Log

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
