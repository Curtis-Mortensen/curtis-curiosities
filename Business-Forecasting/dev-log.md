# Dev log — Business-Forecasting

## 2026-07-04 — Forecasting workbench research (rewrite)

### Task
Rewrite research doc with data-science framing: experimental workbench for scenario number-crunching in ~1 week with **no existing data**. Plug in competitor/case-study benchmarks, test retention curve fit, compare Python vs R libraries. Open source as toolbelt, not monolithic adoption.

### Deliverable
- `forecasting-approaches.html` — reframed around workbench architecture, week-1 plan, benchmark YAML, fit testing

### Key changes from v1
- **Theseus**: corrected to original `ESeufert/theseus_growth` (~214 stars); deep dive on strengths, weaknesses, completion, learning curve; warned about unrelated facebookresearch/theseus and stale fork
- **Tidemill**: demoted — 0 stars, wrong phase (needs billing data)
- **Python toolbelt**: pandas, theseus_growth, scipy, pymc-marketing, lifetimes/btyd, lifelines, lucius-ltv, streamlit
- **R toolbelt**: BTYD, BTYDplus, CLVTools, survival/flexsurv, Shiny
- **LOC estimates**: ~300–450 LOC with libraries vs ~450–650 from scratch
- **OSS projects** reframed as inspiration to steal patterns from, not adopt

### Assumptions
- User wants predictions/scenarios before having product telemetry
- Week-1 UI = Jupyter first, optional Streamlit
- Benchmark sources = public SaaS reports, S-1s, Seufert/Mobile Dev Memo retention points

### Next step (when user asks to build)
- Scaffold `workbench/` with YAML benchmarks, fit_retention.py, simulate_monthly.py, run_scenario.py, notebook
