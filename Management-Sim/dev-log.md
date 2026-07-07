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
