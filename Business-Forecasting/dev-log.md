# Dev log — Business-Forecasting

## 2026-07-04 — Forecasting approaches research doc

### Task
User requested a thorough research document (not software) comparing pricing structures, revenue/cost/growth models, and three forecasting approaches: roll-your-own script architecture vs. two open-source tools. Focus: subscription retention, viral growth, churn, win-back.

### Deliverable
- `forecasting-approaches.html` — self-contained HTML review (no external JS/CSS deps)

### Approaches documented
1. **Custom forecasting script** — cohort state machine architecture with module breakdown and monthly loop pseudocode
2. **Theseus Growth** — MIT Python library for retention profiles and forward DAU/cohort projection
3. **Tidemill** — subscription analytics engine (MRR, churn, retention, LTV) from Stripe/billing events

### Assumptions
- No `Business-Forecasting` folder existed; created new project folder per user request
- User explicitly said not to implement forecasting software — research HTML only
- Honorable mentions included (Burnless, lucius-ltv, etc.) but not as primary comparison pillars

### Open questions for user
- Which billing system (if any) is in use — affects whether Tidemill is the right backward-looking layer
- Whether viral loops are product-native (invites) or marketing-only (word of mouth lumped into organic)
