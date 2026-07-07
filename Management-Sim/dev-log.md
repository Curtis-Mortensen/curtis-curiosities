# Management Sim — Dev Log

## 2026-07-07 — Question 1: Management Theory Foundations (complete)

### Plan summary
User requested research on business/organizational management theory for a management simulation video game, following the same research methodology as the Apocalypse Story project. Deliver a self-contained HTML research document covering theories, history, influential books, MBA curriculum, empirical evidence on management quality, and ongoing debates (flat orgs, Musk-style management).

### Precursor / subset questions identified
1. What is the difference between management and leadership?
2. Are management principles universal or contingent on context?
3. What outcome metrics define "good management"?
4. What level of analysis applies (individual, team, org, industry)?
5. How does the MBA curriculum map to management knowledge domains?
6. What empirical evidence is causal vs. correlational?
7. What are the tradeoffs of flat vs. hierarchical organizations?
8. How should research translate into game mechanics?

### Key findings
- **Management quality is causal:** Bloom et al. (2013) India RCT showed +17% productivity from management consulting; WMS correlates management scores with profitability across 35 countries.
- **Boss quality is high-leverage:** Lazear et al. (2015) found replacing a bottom-10% boss with top-10% adds more than one worker to a nine-person team.
- **Managers drive engagement:** Gallup (2015) — 70% of engagement variance attributable to direct manager.
- **No universal optimum:** Contingency theory (Lawrence & Lorsch, 1967) is best-supported framework for game design — structure must fit environment.
- **Flat orgs are contingent:** Lee & Edmondson (2021) "myth of the flat start-up" — creativity up, execution down; Holacracy/Zappos largely failed.
- **MBA structure:** 36–60 US credits; core ~50–65% (finance, marketing, strategy, ops, OB, economics, statistics); electives and experiential remainder.
- **45 influential books catalogued** from Smith (1776) to Doerr (2018).

### Deliverable
- `docs/management-theory-research.html` — self-contained research document with CSS, timeline diagram, 20+ tables, limitations, field history, game design implications, 90+ references.
- `README.md` — project overview and agent instructions.

### Design implications for game
- Model management as production input (WMS dimensions: monitoring, targets, incentives)
- Boss quality as team multiplier (Lazear)
- Engagement 70% manager-driven (Gallup)
- Org structure tradeoffs: speed vs. control, innovation vs. execution
- No single winning strategy — environmental fit determines success

### Status
**Complete** — Question 1 research artifact ready for human review.

---

## 2026-07-07 — Question 2: Startup Accelerators & Co-Founder Paths (complete)

### Plan summary
User requested research on: (A) how ~20 college-dropout digital founders met co-founders, and (B) history/development of accelerators and incubators, top US programs, program structure, and success/failure rates. Deliver self-contained HTML in Apocalypse Story / Q1 format.

### Precursor / subset questions identified
1. What counts as "dropout" vs. "left without degree"?
2. Accelerator vs. incubator definitional differences?
3. What metric defines "success" (survival, exit, unicorn)?
4. Selection bias in accelerator outcome data?
5. Co-founder matching platforms — do they work?
6. Survivorship bias in famous founder case studies?

### Key findings — Part A (Co-founder paths)
- **20 case studies** catalogued with meeting channel, college status, and sources.
- **Six channels:** college roommates/classmates (35%), childhood friends (20%), work colleagues (20%), startup coworkers (15%), online (5%), recruited strangers (5%).
- **Dropout myth:** dropping out usually follows traction, not precedes it (Gates tried to return twice).
- **Work underrated:** WhatsApp (Yahoo), Oracle (Ampex), Twitter (Odeo) — professional proximity matters.
- **Accelerators rarely create teams:** Reddit, Airbnb, Dropbox, Stripe had co-founders before YC.

### Key findings — Part B (Accelerators)
- **Incubator origin:** Batavia Industrial Center, 1959 (Mancuso, NY).
- **Accelerator origin:** Y Combinator, March 2005 (Graham et al.); Techstars 2006.
- **YC outcomes:** 84–87% active; ~1.6–5.8% unicorn rate; 18.4% exit by year 5; $600B–$1T portfolio.
- **Comparative:** YC 5.8% unicorn vs. Techstars 2.2%, MassChallenge 1.8%, 500 Global 1.5%.
- **Accelerators improve survival ~23–25%** vs. baseline (Hall et al., 2015); Wharton 2023: +$1.8M funding year 1.
- **Co-founder matching:** YC platform 100K+ matches; free, no equity; thin outcome data.

### Deliverable
- `docs/startup-accelerators-cofounder-paths.html` — 12 sections, 20-founder table, accelerator comparison tables, timeline diagrams, 50+ references.

### Status
**Complete** — Question 2 research artifact ready for human review.
