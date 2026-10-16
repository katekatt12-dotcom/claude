# Benelux Pharma - Territory Plan (Batch 1: GSK, J&J, Pfizer, MSD, UCB, argenx)

Draft of 2026-10-15. Built from `projects.csv` and `sources.md` in this folder. Public web only; no LinkedIn or paid databases. Nothing here has been checked against planning portals.

## 1. Executive summary

- **The standout in-window project is UCB Genesis (Braine-l'Alleud, Belgium):** EUR 200m+ gene-therapy site opened 24 April 2026, fully robotised fill-finish, "real-time digital ecosystem", first production in 2026-27. CQV, MES/eBR and data-integrity work are live now.
- **GSK is the biggest and most uncertain account.** NewLyo in Wavre (EUR 250m+, freeze-dried vaccines, operational H1/H2 2027) is exactly Orise's scope, but on 14 October 2026 GSK told its works council that up to 1,217 Belgian jobs are threatened, with a rumoured future question over Rixensart and a new CEO who wants only one vaccine among five or six priorities. Do not drop NewLyo, but confirm its status before investing pursuit effort.
- **Pfizer Puurs (EUR 1.2bn, announced Dec 2022)** should be in late delivery; the next signal is a 7.5-hectare land extension awaiting zoning (RUP) approval by end 2026.
- **MSD Animal Health Boxmeer (Netherlands)** is building a new animal-vaccine formulation and filling facility (construction from March 2025, about three years, about 80 jobs) with digitalisation and automation stated. Animal health, so check scope fit.
- **Quiet or negative:** J&J (nothing in window found), MSD Oss (sold to Organon, closure 1 July 2025), argenx (no manufacturing).
- **Remaining Tier 1 pass (2026-10-15):** the largest new find is **Eli Lilly Katwijk (Netherlands), a EUR 2.6bn greenfield oral-medicines plant** (council approval 1 Oct 2026; production and wastewater permits still pending; first medicines hoped for 2030). Lilly is already advertising OT/IT system-integration, utilities, QA/CSV and operational-readiness automation roles. **Takeda Lessines** (EUR 300m plasma plant, full production due end 2026) is mid-restructuring (109 jobs, April 2026). **BMS Leiden** CAR-T plant is built and producing (lifecycle only). **Astellas Meppel** was sold to Delpharm (2023-24), and Sanofi Geel and Amgen Breda show nothing in window. Baxter, Novartis, AbbVie, AstraZeneca and Roche: nothing found.
- **Tier 2 pass (2026-10-15): radiopharma is the Benelux Tier 2 story.** **IRE Fleurus** is building a GMP radiopharmaceutical CDMO (hot cells early 2027, operational H2 2027), **PanTera (IBA/SCK CEN)** is constructing an actinium-225 plant at Mol (operational 2028) and **Trasis** bought Mithra's old 17,000 m2 GMP site at Flémalle (move-in early 2027, 300 jobs by 2030). **Legend Biotech/J&J** is adding about USD 150m of CAR-T capacity in Ghent (to 2028). On the negative side, **Galapagos** is closing its Leiden cell-therapy site and **Univercells/Exothera** went bankrupt. Synthon, Aspen Oss, Fagron, Ajinomoto, Terumo and Centrient show nothing material in window. **Correction:** an early search summary suggested Synthon was reconsidering an expansion; the fetched article is from 2016, so there is no current Synthon project.
- Sources are thin on digital scope: no MES, SCADA or historian vendor was found for any account. Lilly Katwijk's job posts are the only strong stack hints.

### Investment by company (EUR m, announced/planned; not all in window)

```
Pfizer Puurs            1,200+ |########################################  (announced Dec 2022)
UCB biologics centre      300 |##########                                (opened Apr 2024)
GSK Wavre NewLyo          250+ |########                                  (ops 2027)
UCB Genesis               200+ |#######                                   (opened Apr 2026)
UCB Arkelia             100-200 |###-#######                              (100m or 200m - sources differ; due 2028)
GSK Rixensart lab         150 |#####                                     (opened Jun 2026)
MSD Boxmeer                n/d | (not disclosed)
J&J, argenx, MSD Oss       n/a | (no in-window project)
```

### Projects by country

| Country | Site | Company | Greenfield / Brownfield |
|---|---|---|---|
| Belgium | Wavre | GSK (NewLyo) | Brownfield |
| Belgium | Rixensart | GSK (clinical lab) | New building on existing site |
| Belgium | Puurs | Pfizer (1.2bn; 7.5 ha land) | Brownfield; greenfield land |
| Belgium | Braine-l'Alleud | UCB (Genesis, Arkelia, biologics centre) | Brownfield |
| Belgium | Beerse / Geel | J&J | none found |
| Belgium | Ghent (Zwijnaarde) | argenx | none (no plant) |
| Netherlands | Boxmeer | MSD Animal Health | Brownfield |
| Netherlands | Oss | MSD to Organon | Divestment |
| Luxembourg | - | none in this batch | - |

## 2. Project detail

- **GSK Wavre NewLyo:** renovation of a 9,000 m2 building plus a 7,200 m2 extension; lyophilised vaccines (shingles, RSV); several tens of millions of doses a year from 2027; "digitalisation and robotisation" promised. Operational H1 2027 (Medi-Sphere) or H2 2027 (L'Avenir). No progress report found.
- **GSK Rixensart:** 6,000 m2 clinical vaccine laboratory opened 9 June 2026 (EUR 150m building plus automated equipment). Lab, not production.
- **Pfizer Puurs:** Isolator Facility Centre (two production modules), Flexible Freezer Warehouse (mRNA cold storage), 16 more packaging cabins; 250 jobs. Which modules are complete is not public.
- **UCB Genesis:** 17,000 m2 gene-therapy building; clinical production suites, QC and process-development labs, robotised filling line; Leuven activities moving in by end 2026; aim 15 batches a year.
- **MSD Animal Health Boxmeer:** extension of formulating and filling lines for animal vaccines shipped to about 140 countries; new QC lab handed over April 2026 (contractor article).

## 3. Priority ranking (against Orise: MES, LIMS, SCADA, CSV, OT security, PI, lifecycle)

My judgement, not sourced. No value estimates because no source supports one.

| Rank | Account / site | Fit | Timing | Why |
|---|---|---|---|---|
| 0 | Eli Lilly Katwijk (NL) | High | Permits 2026; build 2026-2030 | Largest Benelux greenfield; start-up roles already advertised; permits and a nitrogen-permit appeal are the timing risk. Engage now while OT/IT and CSV strategy is set |
| 0b | Takeda Lessines (BE) | Med-High, at risk | End 2026 start-up | Plasma plant start-up due now; Renault restructuring means confirm who still owns the project |
| T2-1 | IRE Fleurus radiopharma CDMO (BE) | High | Hot cells early 2027, ops H2 2027 | Company-confirmed, GMP CDMO, qualification phase ahead; no investment figure |
| T2-2 | Legend Biotech / J&J Ghent (BE) | High | Build to 2028 | CAR-T capacity; confirm 2026 status of the USD 150m project |
| T2-3 | Trasis Flémalle (BE) | Med-High | Move-in early 2027 | Existing GMP site being adapted for radiopharma; new logo |
| T2-4 | PanTera Mol (BE) | Med-High | Ops 2028 | Ac-225 plant under construction; permits granted |
| 1 | UCB Braine-l'Alleud (Genesis) | High | Now to 2027 | New gene-therapy GMP site, digital ecosystem stated, first batches imminent |
| 2 | GSK Wavre (NewLyo) | High but at risk | 2026-27 | Greenfield-scale vaccine build; verify project status after the Oct 2026 restructuring |
| 3 | Pfizer Puurs | Med-High | 2026-27 | Large sterile/isolator programme; CQV tail and a possible new land phase |
| 4 | MSD Animal Health Boxmeer | Med-High | 2025-2028 | Digitalisation stated, long build; confirm animal-health fit |
| 5 | UCB Arkelia / biologics centre | Med | 2026-28 | R&D centre and bioreactor headroom |
| 6 | GSK Rixensart | Low-Med | Opened | Lab only; site future uncertain |
| 7 | Organon Oss (ex-MSD) | Unknown | Unknown | New owner; research Organon's plans |
| 8 | J&J Beerse/Geel | Low (watch) | - | Strong digital history; no project found |
| 9 | argenx | Low | - | No plant |

## 4. Customer approach (hooks)

- **Annex 11 / data integrity and CSV:** lead at UCB Genesis (new GMP unit) and GSK NewLyo (new freeze-drying lines), where systems are being commissioned.
- **NIS2:** relevant in Belgium (national law in force) and the Netherlands (implementation status should be checked); position OT security at newly connected sites like Genesis and Boxmeer.
- **GSK:** ask first what is happening to NewLyo; the buyer set may be reshuffled by redundancies concentrated on management and employees.
- **UCB:** campus of about 3,000 people with 50 buildings; start with Genesis, then Arkelia and bioreactor expansion.
- **Pfizer Puurs:** go through project and CQV leadership for the isolator and packaging scope; cold chain adds a historian angle.
- **MSD Boxmeer:** vaccine formulation/fill lines with digitalisation and automation named; site director quoted in March 2025 was Darcio Santos (verify tenure).
- Tech stacks for all six sites were **not researched**.

## 5. Customer organisation

Not researched in this batch. No names, titles or LinkedIn URLs beyond the one site director above (press-quoted, not verified). Roles to map via Sales Navigator for each priority site: site head, engineering/capital projects lead, automation/OT lead, MES/LIMS owner, CSV lead, procurement. No emails or phone numbers will be fabricated.

## 6. Gaps and next steps

1. **GSK Wavre:** confirm NewLyo schedule and scope after the 14 Oct 2026 works council; watch for the final social plan and any project pause.
2. **UCB:** resolve Arkelia 100m vs 200m; confirm Genesis first-batch timing (2026 vs 2027).
3. **Pfizer Puurs:** find which Isolator Facility Centre / freezer modules are complete; watch the RUP outcome and the Omgevingsloket for new applications.
4. **MSD Boxmeer:** find the investment amount and the EPC/contractors; MSD Oss: find Organon's plans.
5. **J&J:** search the J&J Belgium press room and Omgevingsloket; check the reported Ghent cell-therapy site.
6. **Permitting:** Omgevingsloket (Flanders), permis unique (Wallonia), officielebekendmakingen.nl (NL), Luxembourg commodo-incommodo - not reachable via my tools, needs a browser.
7. **Agencies and trade press** (FIT, AWEX, BioWin, NFIA, pharma.be, BioVox): not yet read.
8. **Lilly Katwijk:** track the nature-permit appeal and the production/wastewater permits; get the construction start date and the EPC/contractor (not found); map the site leadership in Sales Navigator. **Takeda Lessines:** confirm whether the new plant is operating. **Delpharm Meppel and Organon Oss:** research the new owners' plans.
9. **Remaining accounts (Tier 1 searched but nothing found, re-check with paid tools or company contact):** Baxter, Novartis, AbbVie, AstraZeneca, Roche. **Tier 2 done on 2026-10-15 except Rousselot and Eurofins Luxembourg (nothing found); remaining open items:** IRE and Trasis project values and automation scope; Galapagos Leiden site buyer; Univercells Jumet site; Legend 2026 capex status. **Original Tier 2 list for reference:** Galapagos, Univercells/Exothera, Ajinomoto Bio-Pharma/OmniChem, IBA/IRE, Mithra, Synthon, Centrient, Aspen Oss, Fagron, Terumo, Eurofins, Rousselot.
9. **Tech stacks and contacts:** your Sales Navigator and paid tools.
