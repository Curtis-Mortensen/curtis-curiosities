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
