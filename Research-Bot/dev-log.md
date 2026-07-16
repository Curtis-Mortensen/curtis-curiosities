# Research Bot — Dev Log

## 2026-07-15 — Tuba City Shopping Center case study add-on (complete)

### Plan summary
User provided Street View / satellite / historical context for Tuba City Shopping Center (~1983 Bashas’ Diné Market era): split-face CMU walls, flat reflective commercial roof (likely white TPO), red metal coping. Asked to update the Starlink shopping-list doc with site-specific options and a recommendation.

### Key findings / recommendation
- Walls: ribbed split-face CMU; hollow vs grout-filled cells — use sleeve anchors / Tapcon; avoid wedge anchors unless solid; avoid mortar joints for load attachments.
- Roof: flat parapet commercial; white reflective membrane over likely polyiso + steel deck + bar joists — not a Pivot Mount substrate.
- **Recommend Option A:** Starlink Standard Wall Mount on upper CMU with masonry sleeve anchors + Sikaflex-1a.
- Second: Pipe Adapter on freestanding metal pole. Roof only via pro heat-welded TPO curb. Never DIY Pivot on membrane field.

### Changes made
- Expanded `Research-Bot/starlink-gen3-pivot-mount-roof-shopping-list.html` with §10 case study (site section, 6 options table, recommendation, CMU shopping cart, decision tree); renumbered later sections; updated aims/thesis/conclusion/refs.

### Status
**Complete**

---

## 2026-07-15 — Roomba Plus 505 Combo vs Dual Vac-Mop Competitors (complete)

### Plan summary
User shopping for dual vacuum+mop robots with Roomba Plus 505 Combo as default; asked for cheaper similar-performance competitors, more expensive options with feature/benefit deltas, “Best for:” tags, and personal Worth It rankings (5 stars). Followed Research-Bot README: precursor questions, web research, self-contained HTML with aims/limitations/history/citations/conclusion.

### Precursor / subset questions
1. What does “similar performance” mean at this tier (LiDAR + vac/mop + wash dock)?
2. Street price vs MSRP for the 505 and peers?
3. Spinning pads vs roller mop tradeoffs?
4. How trustworthy are Pa claims vs lab pickup?
5. iRobot post-Chapter 11 / Picea support risk?
6. Hard-floor vs carpet fitness of the 505?

### Key findings
- **505 baseline:** ~$500–$600 street / $999 MSRP; 7,000 Pa; DualClean + PerfectEdge; AutoWash dock; LiDAR + PrecisionVision; strong hard-floor/edge mop; weaker carpet vs Chinese mid-tiers.
- **Cheaper / value peers:** Dreame L10s Ultra Gen 2 (~$400), Eufy Omni C28 (~$450–500; VW Best Budget), Ecovacs T80S Omni (VW July Best Value), Roborock Q Revo sale/refurb, Eufy C20 (~$350 starter).
- **Step-ups:** Curv 2 Flow (~$700–800, best under-$1k upgrade), Max 705 (~$800–900 Roomba path), Shark UV Reveal (~$950 niche), Narwal Flow 2 / Eufy S2 / Dreame X60 / Saros 10R–20 ($1.1k–$1.7k flagships).
- **Worth It favorites vs defaulting to 505:** L10s Gen 2 ★★★★★, C28 ★★★★★, Curv 2 Flow ★★★★★; 505 itself ★★★★☆ for Roomba/Matter/edge mop buyers.

### Changes made
- Created `Research-Bot/roomba-505-dual-vac-mop-competitors.html`
- Updated this dev-log

### Assumptions
- US Amazon/brand street prices mid-July 2026; bands ±$50–$100.
- “Dual vacuum mop” = combo with real mop scrub + auto-maintain dock (not drag-pad-only).
- Worth It stars are shopping opinion relative to keeping the 505, not Vacuum Wars lab ranks.

### Bugs / problems
- Some product pages/Amazon fetches timed out; relied on search snippets + Mashable/Vacuum Wars/Hook Up secondary sources + successful fetches of key brand pages.
## 2026-07-15 — Starlink Gen 3 Pivot Mount Roof Shopping List (complete)

### Plan summary
User researching Starlink Gen 3 Pivot Mount installation; requested Research-Bot explainer with history of roofing/fastening advancements, Home Depot–style universal shopping list (drill bits, fasteners, sealants), and roof-type-specific options with pros/cons.

### Precursor / subset questions
1. What does Starlink ship in the Pivot Mount kit vs what must be bought locally?
2. Which roof types is the Pivot Mount actually designed for?
3. How do fastener choices differ (lag vs roofing screw vs wedge anchor vs seam clamp)?
4. How do sealant chemistries differ by membrane (asphalt, metal, EPDM, TPO, PVC, mod-bit)?
5. When should official alternatives (Wall, Ridgeline, Pipe Adapter) replace Pivot Mount?

### Key findings
- Pivot Mount is designed for **sloped asphalt shingle** roofs: 2× 3/8″×3.5″ lags, 1/4″ pilot, kit butyl tape squares/strips, 9/16″ socket.
- Universal cart: bits (1/4″ required), SS lags, self-drilling metal screws, wedge anchors, Geocel 2300 (shingle/metal/mod-bit), membrane-specific lap sealants for EPDM/TPO/PVC (Geocel 4500 + 45P primer on TPO/PVC).
- **Do not** use generic silicone/asphalt cement on single-ply membranes; Through the Roof! explicitly excludes TPO and warns on EPDM.
- Standing seam: non-penetrating S-5!-type clamps + Pipe Adapter; Ridgeline for no-drill metal/shingle ridge (&lt;45°, ~50 mph wind cap).
- Tile/clay: third-party kits exist; Starlink Ridgeline not recommended for clay; Wall Mount often better.

### Changes made
- Created `Research-Bot/starlink-gen3-pivot-mount-roof-shopping-list.html` — history section, universal buy list, 12-row roof matrix, 12 roof-type deep dives, Starlink mount alternatives, workflow diagram, 26 references.

### Assumptions
- US residential focus; Home Depot / big-box product names as examples.
- User has Gen 3 Standard (Standard 4) dish; Pivot Mount ~$74 from Starlink.
- No site visit; rafter confirmation via attic/stud finder assumed as best practice.
## 2026-07-13 — Edge / Outback / CX-50 Comps vs Vectra Edge (complete)

### Plan summary
User found a Ford Edge at Vectra (~$7k / ~137k miles) and asked for other Ford Edges, Subaru Outbacks, and Mazda CX-50s in the SLC valley from the used dealerships already researched.

### Key findings
- **Vectra Edge sticker:** Fair vs KBB/CarGurus (~$7k for older high-mile Edge); slightly cheaper than SSL peers (Drive In 2017 $8.6k/150k; Zamzam 2015 Titanium $9k/138k). Not a rare underpricing.
- **West Auto Edges:** 2017 SEL $12,325/93k; 2022 SEL $19,407/64k — not $7k peers.
- **Image Auto:** 2020 Edge SEL AWD $10,995/72k **rebuilt title**.
- **Immaculate / Prestman:** No useful $7k Edge shelf in this scan.
- **Outbacks:** West Auto cheapest ~$15.4k (2017); Prestman/Image branded newer $17k–$28k. Budget Outbacks exist at smaller indies: Wild House 2013 $4,899/183k; Auto Empire 2013 $4,988/177k; WVC 2016 Limited ~$8.2k–$8.4k/161k.
- **CX-50:** Not in budget. CarGurus SLC avg ~$30.6k; range ~$20k–$42k. Tim Dahle used stock mid-$20ks+.
- **Buy caveat:** AWD Edge PTU failures; PPI required before calling it a deal.

### Changes made
- Created `Research-Bot/slc-edge-outback-cx50-comps.html`
- Linked from parent survey and $10k follow-up further-questions list
- Updated this dev-log

### Assumptions
- User’s Vectra Edge year/trim/AWD not confirmed online; valuation framed as “older high-mile Edge” band.
- Vectra website inventory filters often empty; relied on buyer report + peer aggregators.

### Bugs / problems
- Cars.com / KSL zip searches and CarGurus HTML often blocked or timed out; used dealer sites + KSL individual listings + AutosToday + CarGurus SERP snippets.
## 2026-07-13 — Utah credit unions vs MACU: out-of-state branches & everyday loans (complete)

### Plan summary
User asked for a good Utah credit union with coverage outside Utah, whether any beat MACU, with good willingness to finance everyday uses; branch locations prioritized over complex products. Followed Research-Bot instructions: precursor questions, web research, self-contained HTML with aims/limitations/history/citations/conclusion.

### Precursor / subset questions
1. Owned branches vs Shared Branch vs ATM networks
2. MACU state-by-state footprint
3. America First / Goldenwest / Chartway / mid-size CU comparison
4. Which CUs still use CO-OP Shared Branching
5. Everyday auto + personal loan willingness signals

### Key findings
- MACU ~109 branches (CREHQ): UT 78, ID 12, AZ 12, NV 5, MT 2 → ~31 outside Utah; still top-tier Intermountain owned footprint.
- America First ~123 (CREHQ): UT 94, NV 18, AZ 7, ID 2, CA 1, NM 1 → ~29 outside Utah; beats MACU in Nevada; AZ expanding +8 through 2027.
- MACU no longer participates in Shared Branching; Utah First, Goldenwest, Cyprus, Deseret First still market ~5,000–6,000 shared teller locations nationwide — those beat MACU on true national branch access.
- Everyday lending: MACU + AFCU are regional auto heavyweights; Utah First markets personal loans with “strives to say yes.”

### Changes made
- Created `Research-Bot/utah-credit-unions-vs-macu-branch-coverage.html`
- Dev-log entry

### Assumptions
- CREHQ mid-2026 counts preferred over marketing “100+” language when they conflict mildly.
- AFCU does not clearly market Shared Branch for members (ATMs yes); treated like owned-branch model unless member services says otherwise.
- “Willingness” inferred from products/marketing, not underwriting matrices.

### Bugs / problems
- Exact Shared Branch member-side status for AFCU not confirmed on a dedicated FAQ (unlike MACU’s explicit exit notice).
- Branch counts can differ by a few depending on Walmart/ITM counting conventions.
## 2026-07-14 — Company Scaling Books Overview (complete)

### Plan summary
User asked for a four-part research overview of nine company-building/scaling books (Traction/Wickman, E-Myth/Gerber, Scaling Up/Harnish, High Growth Handbook/Gil, Scaling People/Johnson, Who/Smart, Team Topologies/Skelton, Rocket Fuel/Wickman, High Output Management/Grove), following Research Bot HTML report guidance.

### Precursor / subset questions
1. What lineages of “scaling” philosophy do these books represent historically?
2. What is each book’s publication date, audience, and chapter coverage?
3. What do they advise on first hires, early definition, and growth planning?
4. Where is there consensus vs. disagreement across the set?

### Key findings
- Four lineages: industrial managerial leverage (Grove 1983) → franchise/systems SMB (Gerber 1986/1995) → entrepreneurial OSs for mid-market (Wickman/Harnish/Smart 2007–15) → SV hypergrowth + team-flow (Gil/Skelton/CHJ 2018–23).
- Consensus: structure before personalities; people quality compounds; outcome clarity; cadence; founder role must change; pick one coherent OS.
- Splits: systems-learners vs A-players; EOS simplicity vs Scaling Up breadth; Integrator essential vs optional COO bench; company OS vs team topology; cash/speed assumptions.

### Changes made
- Created `Research-Bot/company-scaling-books-overview.html` (aims, limitations, history, Parts 1–4, conclusion, references).
- Dev-log entry.

### Assumptions
- Used commonly cited editions for chapter lists; relied on publisher pages, archive metadata, and reputable summaries rather than full page-by-page rereads in-session.
- “Scaling People” detailed chapter subheads drawn from publisher/summary TOCs.

### Status
**Complete**

---

## 2026-07-13 — $10k Compact SUV Years/Mileage Add-On (complete)

### Plan summary
User asked which compact SUVs are most popular in the ~$10k range and what years/mileage are reasonable. Added Section 5 to the $10k follow-up report.

### Key findings
- Popular names: CR-V, RAV4, Forester, Escape, Rogue, Equinox, Sportage/Tucson (Jeep Patriot/Cherokee common on budget lots).
- Typical years: ~2008–2015 for Honda/Toyota/Subaru; Escape/Rogue often 2011–2016.
- Reasonable miles: ~100k–140k sweet spot; 140k–180k OK with records+PPI; >180k budget-lot risk.
- Local examples: Escape Titanium AWD ~$9,990/85k; Escape SE private $7,300/114k; Rogue $4k–$7k at Vectra with wide mileage spread.

### Changes made
- Expanded `Research-Bot/slc-10k-used-cars-mpg-loan-math.html` with compact SUV section, mileage bands, local snapshots, refs 19–28.
- Updated aims, TOC, quick verdict, conclusion, further questions.
## 2026-07-13 — Tour map under-$1k budget filter (complete)

### Plan summary
User asked for prices on the proximity tour stops; anything over $1,000 should be crossed out but kept for reference.

### Under-$1k still live (tour priority)
- Parkway multiplexes 2BR ~$835–$925
- Lakecrest 2BR ~$950–$995
- Lake Park ~$885 only if old RPM ad still live (current Nestwell ~$1,050+ struck)
- Enclave 1BR from ~$999 (higher plans struck)
- The Redwood studio ~$849–$899 / 1BR ~$949 (upper 1BR ~$1,069 struck)
- Decker Lake complex: list rents struck; promo effective ~$993 only if still offered

### Over $1k (kept, struck)
H2O (~$1,495+), Decker Station (~$1,075+), Lake Park Cir (~$1,200), 4168 W 3280 S (~$1,095), Shadowbrook (~$1,099+)

### Changes made
- Tour §7A price column + strike-through CSS / over-budget rows; under-$1k loop callout; diagram + tip refreshed.
- Dev-log entry.

### Status
**Complete**

---

## 2026-07-11 — $10k Band Follow-Up: Lots, MPG & Loan Math (complete)

### Plan summary
Follow-up expansion to the first-time used-car survey: focus on ~$10k cars near West Jordan/West Valley—which lots have the best range/deals; which models win on gas mileage at that price; hypothetical monthly payments and lifetime interest at scores 600/650/700/750 comparing CU vs dealer rates and 0% vs 10% down across typical terms (~20-row table).

### Precursor / subset questions
1. Who actually stocks under-$12k inventory on Redwood Rd?
2. How do Vectra / West Auto / Immaculate / franchise / KSL compare in that band?
3. Which sedan/hatch models maximize EPA MPG near $10k?
4. Which published CU sheet and dealer survey map cleanly onto scores 600/650/700/750?
5. How much does 10% down change payment vs interest when APR is held constant?

### Key findings
- **Best $10k density:** Vectra Auto Sales (WVC) — iSeeCars avg price ~$8,231; high miles (~153k avg); examples Fiesta $5,499, Versa $5,500, Elantra Sport $6,999.
- **West Auto** states ~$10k average but featured web inventory often sits mid-teens; still a key ask-for-budget-stock destination.
- **MPG winners:** Prius (~48–50) ≫ Civic/Corolla (~33–36) ≫ Versa/Fiesta (~31) ≫ Elantra/Impreza (~28–32).
- **Loan math on $10k / 60 mo:** Utah First–like CU at 750 + 10% down ≈ $164/mo and ~$824 interest; dealer-typical 15.93% at 600 + 0 down ≈ $243/mo and ~$4,569 interest; 72 mo at that dealer rate ≈ $5,590 interest.

### Changes made
- Created `Research-Bot/slc-10k-used-cars-mpg-loan-math.html`
- Linked follow-up from parent `slc-west-jordan-first-time-used-car-buyer.html`

### Assumptions
- Utah First grade bands mapped 750→A+, 700→A, 650→B, 600→C.
- Dealer APRs = MFP Utah used dealer averages by score (flat across terms).
- 0% vs 10% down uses same APR (principal-only effect) unless underwriting overlays apply.

### Bugs / problems
- KSL zip search and Cars.com max-price search timed out; used iSeeCars dealer pages + individual KSL listing fetches.
- Vectra own inventory URL returned empty “not found” shell; relied on iSeeCars + KSL.
## 2026-07-13 — Tour-day proximity map near Decker Lake (complete)

### Plan summary
User touring today; asked for next-closest housing after Decker Lake so they can hit multiple nearby stops. Added proximity-ranked tour map with addresses/phones and a suggested driving loop.

### Key tour stops (nearest first)
1. H2O Townhomes (2882 S Big Wave) — across street from park; premium ~$1,495+
2. Decker Station (3058 Decker Lake Dr) — TRAX adjacent
3. Apartments at Decker Lake (2184 W 3100 S) — booked tour likely
4–8. Lakecrest / Lake Park / Parkway multiplexes — cheapest near-park whole units; Nestwell (801) 396-9288, RPM (801) 363-7368
9–11. Enclave → Shadowbrook → The Redwood on Redwood Rd south

### Changes made
- Updated `decker-lake-west-valley-housing-prices.html` with §7A tour-day proximity map + phones + refs.
- Dev-log entry.

### Status
**Complete**

---

## 2026-07-11 — Decker Lake housing update: IF/Mesa trends + second deal pass (complete)

### Plan summary
Follow-up: rents feel high vs Idaho Falls and Mesa. Add lighter historical average-rent comparison across WVC/SLC, Idaho Falls, and Mesa; note SLC drivers. Second listing pass for better deals; Tooele too far; Magna/South Jordan etc OK; ~20 min acceptable, closer ideal. Update near + further sections in existing HTML.

### Key findings (update)
- **ZORI 2026:** WVC ~$1,575 ≈ Mesa ~$1,554; Idaho Falls ~$1,315 (~$260 cheaper). IF 1BR avg ~$850 vs WVC ~$1,150–$1,250.
- **SLC drivers:** Silicon Slopes demand, structural shortage, 2022 spike, then multifamily oversupply cooling into 2025–26; pipeline shrinking → possible rent re-acceleration.
- **Second-pass deals:** Lakecrest Chesterfield 2BR ~$950–$995 (near park); Magna 2BR duplex ~$1,095; Lake Park now ~$1,050–$1,095 (earlier $885 likely gone). Magna $800–$850 and The Redwood ~$849 still best expanded floors. South Jordan averages higher (ZORI ~$1,913) — not a bargain direction.

### Changes made
- Updated `Research-Bot/decker-lake-west-valley-housing-prices.html` — new §5 three-city trends, tightened to ~20 min, second-pass section, refreshed rankings/conclusion/refs.
- Updated this dev-log.

### Status
**Complete**

---

## 2026-07-11 — SLC West Jordan / West Valley First-Time Used Car Buyer Survey (complete)

### Plan summary
User researching first-time car buying near West Jordan / West Valley City: which businesses sell used cars; reputation for price vs reliability; middle options between dealership upcharge and junkyards; one popular sedan/compact-SUV price baseline per major location; financing (% down, rates, bank vs dealer credit) compared across 3–5 credit-score bands. Delivered as Research-Bot self-contained HTML per README.

### Precursor / subset questions identified
1. What seller tiers exist between franchise retail and as-is junkyards in Utah?
2. Which named businesses sit in West Jordan, West Valley, and adjacent south-valley destinations first-time buyers actually use?
3. How do review/aggregator signals (Google, iSeeCars, BBB) map to price vs reliability?
4. What are Utah rebuilt/branded-title specialists (Prestman, Image Auto) vs salvage auctions vs private KSL?
5. What sample non-truck listings exist right now as price baselines?
6. What down-payment norms do local lots publish vs personal-finance guidance (10–20%)?
7. How do Experian used-car APRs by credit tier compare to Utah CU sheets and MFP Utah dealer/CU/bank surveys?
8. When must a buyer use their own bank/CU (private party) vs dealer F&I / BHPH?

### Key findings
- **Middle ground:** independent lots (West Auto Sales WVC, Immaculate WJ, Peterson Midvale) and licensed rebuilt/branded specialists (Prestman SLC, Image Auto WJ)—not DIY Copart bids or U-Pull yards.
- **Reputation:** West Auto strong on price + review volume; CarMax strong on process predictability; Prestman strong branded-title track record; franchise Ken Garff/LHM stronger on CPO/service networks and often higher stickers/doc fees; BHPH easiest approval, highest effective cost risk.
- **Utah doc fees:** no state cap; samples ~$299–$499 (avgs ~$424–$443); CarMax $499; Prestman $489.
- **Baselines (2026-07-11 snapshots):** West Auto 2019 Corolla LE ~$18,207; Immaculate 2024 Outback Premium ~$24,345; LHM 2018 CR-V Touring ~$24,633; CarMax 2020 Escape SE ~$16,998; Prestman 2025 Civic Hybrid Sport Touring ~$25,489 (branded).
- **Financing:** most lots finance; private KSL usually needs bank/CU; West Auto $0–$500 down by credit; BHPH often ~$500; aim 10–20% when possible.
- **Rates:** Experian used APRs ~7.70% (781–850) → 21.85% (300–500); Utah First CU sheet 3.50%–16.75% by grade; America First / MACU as low as 4.99%; MFP Utah shows dealers cheapest at 750+ then worst below ~700—CUs more consistent.

### Changes made
- Created `Research-Bot/slc-west-jordan-first-time-used-car-buyer.html` — spectrum diagram, business survey, reputation matrix, baseline price table, financing + 5-tier rate comparison, first-time playbook, 35 references.

### Assumptions
- “Near West Jordan or West Valley” includes adjacent South Jordan (CarMax), Sandy Automall (LHM), Midvale (Peterson/Fast Start), and SLC Prestman as realistic west-side shopping destinations.
- Baseline cars intentionally unmatched on year/miles to illustrate channel pricing, not identical comps.
- Hard-pull personal APR quotes not obtained; used published Experian, MFP Utah, and CU rate sheets.

### Bugs / problems
- Ken Garff Used inventory URL 404/timeout; Image Auto homepage timed out—profiled from secondary sources and brand pages.
- CarMax Utah search returned network-wide listings; used Escape/Camry as representative fixed-price samples and noted fee exclusions.
## 2026-07-11 — Decker Lake / West Valley Housing Price Comparison (complete)

### Plan summary
User looking at SLC housing near a friend who works by Decker Lake Park (West Valley City). Requested: (1) cheapest whole apartments (not rooms) as close as possible to the park — studio or 2BR OK, duplex/split/multiplex OK; (2) compare with apartments within ~30 min driving distance and whether a larger radius finds better deals / cheapest rates. Delivered as Research-Bot self-contained HTML per README.

### Precursor / subset questions identified
1. Exact park location / ZIP / TRAX anchors for “near”?
2. Whole unit vs room filter criteria?
3. Studio / 1BR / 2BR and duplexes in scope?
4. WVC market averages as “cheap” benchmark?
5. Which cities fall inside ~30 min (Magna, Kearns, Taylorsville, etc.) vs outside (Tooele ~37 min)?
6. Do concessions / included utilities change rankings?
7. Are cheapest listings income-restricted?
8. Is expanding radius worth the commute in $/month?

### Key findings
- **Closest reliable complexes:** Apartments at Decker Lake 1BR ~$1,062–$1,147 (promo effective sometimes ~$993); Decker Station studios ~$1,075+, 1BR ~$1,149–$1,445, 2BR ~$1,515+.
- **Cheapest near-park whole units:** Parkway Blvd / Lake Park Dr multiplex 2BRs ~$835–$925 / $885 — scarce; several showed uncertain availability.
- **Inside 30 min better deals:** Yes for studios/small 1BRs — Magna ~$800–$850; The Redwood studios ~$849–$899, 1BRs ~$949–$1,069.
- **Absolute cheapest:** Tooele studios ~$650–$799, but ~37 min (outside strict 30-min ring).
- **2BR trade-off:** Rare near-park outliers beat most expanded-radius 2BRs; otherwise Magna multiplex ~$1,175–$1,395 vs Decker Lake complex ~$1,315+.

### Changes made
- Created `Research-Bot/decker-lake-west-valley-housing-prices.html` — self-contained HTML with proximity tiers, 30-min comparison, ranked cheapest rates, decision tree, field history (HUD FMR), 41 references.
- Updated this dev-log entry.

### Assumptions
- “Apartments, not rooms” = whole leased unit with private kitchen; duplex/4-plex/multiplex included.
- Drive times from published city-pair estimates, not live rush-hour Google Maps from the park gate.
- Income-restricted properties noted separately (Coppertree, Tuscany Cove).
- One-time Research-Bot question (base folder HTML; no new docs/ subfolder).

### Bugs / problems
- apartments.com often blocked direct curl (Access Denied); recovered pricing via WebFetch / search snippets / property sites.
- Some cheap Parkway listings showed “Check Back Soon for Upcoming Availability” while still displaying prices — flagged as availability-uncertain.
- Cross-aggregator ranges for Decker Station disagreed by ~$50–$150; reported as ranges.

### Status
**Complete**

---

## 2026-07-08 — CompTIA A+ Mesa, Arizona Research (complete)

### Plan summary
User (employed IT tech ~1 year, Mesa AZ) asked for CompTIA A+ exam cost, discount/subsidy/grant programs, local proctoring centers, summer 2026 availability, and free/low-cost paths. Research followed Research-Bot README guidelines.

### Precursor / subset questions identified
1. Exam structure: how many vouchers, current codes (220-1201/220-1202)?
2. Retail vs. partner vs. academic vs. military pricing?
3. WIOA / Per Scholas / Garcia scholarship eligibility for employed workers?
4. Which Pearson VUE centers serve East Valley Mesa?
5. Summer 2026 center hours vs. Pearson on-demand scheduling?
6. Exam-only path vs. $2,195+ training bundles for experienced techs?
7. Hidden costs: retakes, CE renewal, study materials?
8. Employer reimbursement and military spouse (SpouseWorks/MyCAA) paths?

### Key findings
- **Retail (post–June 1, 2026):** $274/exam, $548 for both A+ cores.
- **Best likely path for employed tech:** authorized partner vouchers ~$476 total + free self-study; ask employer first.
- **WIOA / Per Scholas:** can be $0 but require unemployment, dislocation, low income, or full-time training commitment — less likely if steadily employed.
- **Garcia Family Foundation:** up to $2,500 + 2 A+ vouchers via MCC/SCC pathway; need-based.
- **Nearest centers:** MCC Southern & Dobson (Bldg 38), Rio Salado Tempe, Pearson Chandler; OnVUE from home same voucher.
- **Summer 2026:** MCC Mon–Thu 8am–6pm; Rio Mon–Thu 8am–7pm with holiday closures Jun 18–19 and Jul 2–5.

### Changes made
- Created `Research-Bot/comptia-a-plus-mesa-arizona-2026.html` — self-contained HTML report with cost tables, 30-program discount catalog, 10 test-center profiles, summer hours, decision tree, 48 references.

### Assumptions
- User is Maricopa County resident outside City of Phoenix (Mesa) for ARIZONA@WORK office mapping.
- "Copier A+" interpreted as CompTIA A+.
- Pearson VUE live seat inventory not queried (requires voucher + login); center hours only.
- Employed status makes WIOA/Per Scholas lower probability; flagged in matrix.

### Bugs / problems
- CompTIA store product page did not render per-exam price in automated fetch; cross-verified via Total Seminars June 2026 price-increase post and CompTIA blog sources.
## 2026-07-08 — 2015 Passat TDI Spare Tire & Wheel Interchange (complete)

### Plan summary
User has a 2015 Volkswagen Passat TDI with factory 235/45R18 tires and needs a full-size spare (not a donut). Junkyards often lack VWs; user had a prior list of “matching” cars including SUVs and Audi models. Requested double-check of tire/wheel interchange, bolt pattern (lug location), brake clearance, and forum evidence. Research per Research-Bot README specs.

### Precursor / subset questions identified
1. What are the exact wheel specs for 2015 Passat TDI (PCD, bore, offset, lug seat)?
2. Which alternative tire sizes stay within ±2% rolling diameter?
3. Which vehicles share 235/45R18 but have incompatible bolt patterns?
4. Which Audi/VW Group wheels need hub rings vs direct fit?
5. Do 312 mm front brakes limit spare wheel choice?
6. Will a full-size 235/45R18 fit in the Passat trunk?
7. What have TDIClub / VW Vortex owners actually swapped?

### Key findings
- **Non-negotiable wheel specs:** 5×112 PCD, 57.1 mm center bore (or 66.6 mm + rings), M14×1.5 ball-seat lug bolts, ET40–48 on 18×8 typical.
- **TDI brakes:** 312 mm front / 272 mm rear rotors — 18″ full-size clears; min theoretical wheel 16″ for 312 mm rotors.
- **Tire alternatives confirmed:** 225/45R18 (−1.3%), 245/45R18 (+1.4%), 245/40R18 (−1.7%) within ±2%; 235/40R18 (−3.1%) less ideal.
- **Tier A junkyard targets (direct fit):** Passat 2011–2018, CC, Golf/Jetta/Beetle 18″, Audi A3 8P/8V, older A4/A6/Q3/TT 8J, Seat/Skoda MQB siblings.
- **Tier B (rings required):** Audi A4 B8+, A6, Q5, VW Atlas — 66.6 mm bore.
- **Tier C traps (same tire, wrong wheel):** Ford Fusion (5×108), Hyundai/Kia/Toyota/Honda/Nissan (5×114.3), BMW (5×120), Mk1 TT (5×100).
- **Forum:** TDIClub 2015 Passat TDI owner fit full-size 235/45R18 in trunk with foam trim; VW Vortex warns 18″ donut spares may not clear big front brakes on GTI/R.

### Changes made
- Created `Research-Bot/2015-passat-tdi-spare-tire-wheel-interchange.html` — self-contained HTML report with 50-vehicle tier tables, fitment flow diagram, forum synthesis, 35 references.

### Assumptions
- US-market 2015 Passat TDI with 18″ upgrade package (sticker confirms 235/45R18).
- No physical test fit performed; junkyard inventory varies by region.
- User’s prior compiled list not in repo — report rebuilt from OEM catalogs, fitment DBs, and forums.

### Bugs / problems
- Wheel-Size.com full tire-size vehicle list timed out on fetch; supplemented via WheelsSize.com and Wheelfitment.eu.

### Status
**Complete**

---

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

## 2026-07-08 — Arcosanti & Cosanti Foundation Current State Research (complete)

### Plan summary
User visited Arcosanti, spoke with a resident reporting hard times (~30 full-time residents), foundation blame post-Soleri, and recalled a Not So Native podcast (thought 2021/2023) about 2018 grey-water work and partnership-seeking over money. Requested comprehensive web research on foundation leadership, marketing head, residents, and current situation.

### Precursor / subset questions identified
1. What happened after Paolo Soleri died (2013)?
2. Was 2018 grey-water the last major infrastructure project?
3. Who was on the Not So Native podcast — same person still in marketing?
4. Who runs the Cosanti Foundation board and staff today?
5. Can we identify the ~30 current residents?
6. Is the foundation discouraging residency?
7. What is the most accurate picture as of mid-2026?

### Key findings
- Podcast was **Nov 21, 2019** (Not So Native S4), guest **Tim Bell** (Director of Communications) — not 2021/2023; Bell no longer in role.
- 2018 grey-water (East Crescent + ASU EPICS) well-documented; last major building completed 1989.
- CEO succession: Stein → McWhortor → Martin-Malikian (resigned Sept 2023) → Fritz interim → David Turnbull (~2024).
- 2025 crisis (Wikipedia, NLRB): 80%+ layoffs reported, workshops ended 2024, volunteers eliminated Fall 2025, board strategic pause through 2026.
- Resident count: downward from 75 (2020) → ~45 (website) → ~38 (press) → ~30 (visitor testimony); no public full roster.
- No documented "discourage residency" policy; structural changes (employment-only, program cuts) explain resident perception.

### Changes made
- Created `Research-Bot/arcosanti-cosanti-foundation-current-state.html` — self-contained HTML report with timeline, leadership tables, resident partial list, financials, contradictions section, 29 references.

### Assumptions
- User meant "accurate" not "inaccurate" in final request.
- Wikipedia 2025 layoff claims treated as reported but not fully independently verified (paywalled/local sources inaccessible).
- Research date: July 8, 2026.

### Bugs / problems
- Bloomberg Oct 2025 article and Daily Independent paywalled — could not retrieve full text.
- Foundation website partially stale vs. Wikipedia crisis reporting.
- FY2024 990 leadership listing inconsistent across aggregators (Turnbull vs. Fritz).

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
