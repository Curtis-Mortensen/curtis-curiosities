# Apocalypse Story — Dev Log

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
