# Eli Lilly Katwijk (Netherlands) battlecard
Prepared 2026-10-15 from public web only, same format as the Ireland battlecards. (S) = seen only in search summaries or aggregator pages. No LinkedIn, no contact details.

## 1. Snapshot
- **What:** new European production facility for **oral solid medicines** (tablets): diabetes, obesity and other cardiometabolic conditions, plus neuroscience, oncology, immunology. Lilly's CEO spoke of "billions of pills". Investment **EUR 2.6bn (about USD 3bn)**, announced 3 Nov 2025.
- **Size:** site about 200,000 m2 (20 ha, former greenhouses) at Zonneveldslaan 17, Valkenburg, municipality of Katwijk, in Zijlhoek-De Woerd next to the Leiden Bio Science Park. Facility about **80,000 m2**, up to 40 m high (39.5 m in one source), with gatehouse and visitor centre, offices, a laboratory, production buildings and storage for raw materials and end products (DGMR). **No large R&D department** will be built (Marco Frenken, per press).
- **Jobs:** about 500 production roles, about 1,500 construction roles.
- **Timeline:** main construction planned for **autumn 2026** (RED Company); first medicines hoped for **2030**; Frenken says most of the time will go into commissioning and certifying the production lines, not erecting the building.
- **Why it matters for Orise:** a greenfield site in the earliest phase, where the OT/IT architecture, MES and CSV strategy are being set.

## 2. Permits and approvals
| Item | Status | Source |
|---|---|---|
| BOPA (buitenplanse omgevingsplanactiviteit) + building application | Submitted by RED Company 3 Apr 2026 | extra.katwijk.nl |
| Provisional binding advice | College decision 12 May 2026; council gave preliminary positive advice in June | extra.katwijk.nl; Omroep West |
| Council definitive binding advice | **1 Oct 2026, 28-4**; referendum rejected | Omroep West, NOS |
| Omgevingsvergunning (building) | Katwijk's project page says **granted** (publication gmb-2026-471169, not found by search); appeal to the **rechtbank** possible | extra.katwijk.nl |
| Zoning | Area re-zoned to industrial activities (DGMR); current plan did not allow production, hence the BOPA | DGMR, 28 Jul 2026 |
| Nature (nitrogen) permit | Granted; **appealed by Stichting MOB**; appeal does not suspend work automatically; MOB can ask a judge for a suspension | RTV Katwijk |
| Environmental / production permit (Province of Zuid-Holland) and **water and wastewater permit (Hoogheemraadschap van Rijnland)** | **Still needed** to produce and discharge | RTV Katwijk |
| Tree felling (71 trees, "Eli Lilly/Mondrian") | Permission published; 6-week objection period for that notice | OmgevingsAlert (S) |
| Seveso | Not a Seveso establishment on the current application, but only just below the threshold (provincial councillor); process changes could change that | RTV Katwijk, 17 Sep 2026 |

- 813 objections (zienswijzen) were filed; 25+ studies by 10+ consultancies. Government and province promised **EUR 72m** (another source says over EUR 100m) for accessibility.
- **Conflict to resolve:** the municipality says the building permit is granted; press says "permits are still missing." These are different permits (building vs nature vs environmental/water). Check officielebekendmakingen.nl for the exact decision and appeal deadline.
- **Utilities:** the grid has no spare capacity, so Lilly plans **its own gas turbines** meanwhile (the alderman says no load on the existing grid). A critical Substack puts gas use at nearly 10m m3 a year - unverified. **Water:** Dunea says supply is possible (up to 778,000 litres a day via Dunea; Lilly wants to reuse 40% or "more than half" of process water - sources differ). No grid-operator source found.

## 3. Contractors and partners
- **Developer:** **RED Company** (owner Nanne de Ru) develops the site and submitted the permits. It also plans another 60,000 m2 of life-sciences space in Zijlhoek-De Woerd.
- **Architect:** **Powerhouse Company** (project name "Mondrian", described as the largest bioscience project in the Netherlands); landscape by **LAP Landscape & Urban Design**.
- **Engineering:** RED Company's own site reportedly says Powerhouse designs **together with Jacobs Engineering** (S, single source, not independently confirmed).
- **Permit and environmental consultant:** **DGMR** (acoustics, air, external safety, fire safety, building physics). Named advisers: Elza van Dam, Antwan van Haaren, Ronald Oldengarm.
- **Main contractor, EPCM, automation integrator, CQV contractor:** **not named in any public source.** Ask RED Company or Lilly.
- Lilly's own global engineering and the corporate automation group (see below) will define the standards.

## 4. Technology environment
Careers.lilly.com listings for Katwijk now show "not accepting applications"; the descriptions below come from search summaries and aggregators.
- **Automation Engineer / Senior Principal - System Integration (OT/IT):** manages and grows the platforms and supports manufacturing teams as systems are added; works with corporate Automation, IT and Information Security; initial 12-month contract with possible permanent offer; salary band EUR 60-99k (S).
- **Senior / Sr Principal Automation Engineer - Quality Assurance:** computer system validation; experience in **DCS, SCADA, MES, historians, PLCs, building management systems, GAMP 5, data integrity** (S).
- **Principal Automation Engineer - Plant Utilities; Senior Principal Process Automation Engineers for OSD (oral solid dose) and SDD (spray-dried dispersion) lines; Data Historian and OT Platforms engineer** (S, last one only on an aggregator).
- **Associate Director IT / IT Systems Delivery Lead (Tech@Lilly Manufacturing & Quality):** IT readiness for start-up and integration: infrastructure, **ERP, warehouse management, MES, data historian and real-time floor tracking, laboratory information management, data integrity, CAPA systems, access security and building monitoring**; leads cGMP IT compliance and inspection readiness; on the site leadership team; reports to the MQ IT Senior Director. The aggregator copy says "new Dry Product site in Leiden, NL" while the header says Katwijk - same project.
- **Associate Director - Operational Readiness:** site start-up leader (S).
- **Corporate:** a Lilly "Associate Director - Global Process Automation and Control Engineering" posting names **Emerson DeltaV** as a required DCS platform and lists the new Katwijk site among those it supports (S). Combined with the Ireland findings (Raheen: DeltaV + Syncade + AVEVA PI + LabVantage), expect a **Lilly global template**: DeltaV DCS, a Syncade or similar MES, PI historian. **Not confirmed for Katwijk.**
- Lilly job posts do not name PAS-X, Syncade or PI for Katwijk; treat the template as a hypothesis to test in discovery.

## 5. Fit map against Orise
| Capability | Fit | Why |
|---|---|---|
| CSV / CQV (OT, QC, IT) | High | QA automation and IT readiness posts; GAMP 5 and data integrity named |
| MES / eBR | High (to confirm vendor) | MES in IT readiness scope |
| SCADA / OT integration | High | OT/IT system integration roles |
| Historian / AVEVA PI | Medium-High | "Data historian" in both IT and automation posts; Lilly Ireland sites are PI houses |
| OT cybersecurity / NIS2 | High | Information Security partnership named; Dutch NIS2 status should be checked |
| LIMS | Medium | "Laboratory information management" in scope |

## 6. Competitors and partners
Lilly runs global standards, so system selection is probably corporate, and local integrators join through Lilly's approved list. Likely competitors are large global automation/CSV firms already on Lilly programmes. Specifics are not public. In Ireland, PM Group is EPCM on Lilly Limerick; whether it or another EPCM is involved in Katwijk is unknown - do not assume.

## 7. Wedge and entry angles
1. **Approved-vendor route:** find out whether Lilly's global procurement allows a new Benelux supplier for OT/IT integration and CSV, and who in Tech@Lilly MQ owns it.
2. **Local CQV and CSV capacity:** commissioning and certifying lines is the long pole (Frenken); offer Dutch-language, GxP-experienced resources that Lilly's 12-month-contract hiring cannot fill quickly.
3. **Permit-delay hedge:** if production and wastewater permits or the nature-permit appeal delay civils, engineering and software design (URS, FAT) can still proceed.
4. Regulatory hooks: Annex 11 and data integrity for MES/historian/QC systems; NIS2 for OT.

## 8. Organisation map (public sources; verify titles and tenure)
| Name | Role as reported | Source |
|---|---|---|
| Marco Frenken | General manager / country manager, Lilly Nederland (titles vary by outlet) | RTV Katwijk, Oegstgeester Courant, Omroep West |
| Dave Ricks | CEO, Eli Lilly | NOS |
| Nanne de Ru | Owner, RED Company (developer) | Property NL, Omroep West |
| Gerard Mostert | Alderman (wethouder), Katwijk | NOS, Omroep West |
| Elza van Dam, Antwan van Haaren, Ronald Oldengarm | DGMR advisers on the permit | DGMR |
**Not found publicly:** Katwijk site leader, head of engineering/capital projects, head of automation, MES/IT lead, CSV lead, procurement. Roles being recruited (above) show where they will sit. These need Sales Navigator; no LinkedIn URLs collected, no emails or phones.

## 9. Discovery questions
1. Who is the project executor (EPCM / main contractor) and when is it appointed?
2. Is the OT/IT, MES and historian stack a Lilly global template (DeltaV / Syncade / PI)? Who owns the template decision?
3. How are CSV and CQV split between Lilly staff, EPCM and third parties?
4. What is the commissioning sequence for the OSD and SDD lines, and where are the long-lead decisions?
5. How do the water, wastewater and nitrogen permits affect the build schedule?
6. Which Dutch cybersecurity (NIS2) requirements will the OT network have to meet?

## 10. Objections to expect
- "We use Lilly's global approved suppliers." Answer: ask how to qualify, and offer local surge capacity.
- "We hire in-house on contracts." Answer: CQV volume peaks above any hiring plan; bridge capacity.
- "Permits are uncertain." Answer: engineering and CSV design work does not depend on civils.

## 11. Next actions
1. Pull the permit decision (gmb-2026-471169) and appeal deadlines on officielebekendmakingen.nl; check the Rechtspraak register for the Stichting MOB case.
2. Ask RED Company/Lilly who the main contractor and EPCM are; check TenderNed for Lilly-related notices.
3. Map Lilly Katwijk leadership and the Tech@Lilly MQ IT leads in Sales Navigator.
4. Compare with the Lilly Ireland battlecard (`ireland/lilly-battlecard.md`) for the global stack and the PM Group relationship.
5. Re-check careers.lilly.com weekly for Katwijk openings; each new post reveals scope.
