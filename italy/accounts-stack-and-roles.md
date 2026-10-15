# Tech stacks and public roles - top 5 accounts (2026-10-15)

Public web only. No LinkedIn, no paywalled databases, no emails or phone numbers. Almost nothing about Italian MES/SCADA/historian vendors is published for these sites, so most "stack" findings are **inferences from equipment and job posts** and are labelled that way. Job-board pages are aggregator copies; dates are unreliable.

## Summary

| Account | Confirmed stack | Best-fit buyer role found | Named person (public) | Confidence |
|---|---|---|---|---|
| Merck KGaA Modugno-Bari | None named | **Operation Technology, Digital & Data Associate Director** (posting) | Annalisa Calvano, Site Director (2019 appointment; Site Head per Jan 2026 press) | Medium |
| Kedrion Bolognana | None named | Not found | Massimiliano Barberis, COO; Ugo Di Francesco, CEO | Low-Med |
| CordenPharma Caponago | Bausch+Stroebel isolator, Syntegon high-speed line (equipment, not software) | Computer System Validation Specialist (posting) | None found | Medium |
| Chiesi Nerviano | None named | Site Plant Controller Lead (posting), Sterile Supervisor | No site director named | Low |
| Novo Nordisk Anagni | None named | Not found | No site head named (commissioner is the Lazio president, a government role) | Low |

## Merck KGaA, Modugno-Bari
- **Role to target:** the "Operation Technology, Digital & Data Associate Director" posting (Glassdoor aggregator) describes the exact buyer: owns the site digital roadmap, holds OT and digital **opex and capex**, keeps computerised systems compliant with EU and FDA requirements, and acts as SME in inspections. Asks for Industry 4.0, connectivity and industrial automation knowledge. Source: [Glassdoor listing](https://www.glassdoor.it/job-listing/operation-technology-digital-data-associate-director-merck-kgaa-JV_IC2812372_KO0,52_KE53,63.htm?jl=1010094423005). Whether filled is unknown.
- Also posted: Operational Excellence Site Leader (one-line description only).
- **Site Director:** Annalisa Calvano. [Daily Health Industry, 8 Apr 2019](https://www.dailyhealthindustry.it/merck-biofarma-italia-annalisa-calvano-nuovo-direttore-stabilimento-di-modugno-ID13173.html) (industrial management engineer, joined 2009, previously Manufacturing Operations Director); January 2026 press ([Oblo](https://oblo.it/farmaceutica-merck-nel-sito-di-modugno-bari-nuova-linea-per-farmaci-iniettabili-in-siringa/)) calls her Site Head. Verify current title.
- **Stack:** not named. Isolator line since 2021 and the 2026 syringe line mean validated aseptic equipment and a ~EUR 10m digitalisation line item (see `projects.csv`). Ask what MES/eBR and historian the site runs.
- **Angle:** validation support for the isolator syringe line plus the digital roadmap; the OT/Digital director is the likely sponsor.

## Kedrion, Bolognana
- **Stack:** nothing public. The 2026 plan says cybersecurity and AI are priorities ([NCF](https://www.notiziariochimicofarmaceutico.it/2026/05/13/kedrion-investe-nel-made-in-italy-150-milioni-per-triplicare-la-capacita-produttiva/)).
- **Postings seen:** a Quality Control Software Technician at Bolognana asks for URS/protocol validation documents and LIMS knowledge ([JobAdvisor](https://jobadvisor.it/p/offerte-lavoro/91633/kedrion-biopharma/qc-data-analyst-internship)) - a LIMS/CSV hint, not a stack. The automation engineer posting found is at the **US** site (Melville, NY), not Italy.
- **People:** Massimiliano Barberis is COO and quoted on the Bolognana timeline ([Sanita33](https://www.sanita33.it/mercato/7539/kedrion-investe-150-milioni-in-toscana-per-triplicare-la-produzione-di-plasmaderivati.html), [NCF](https://www.notiziariochimicofarmaceutico.it/2026/05/13/kedrion-investe-nel-made-in-italy-150-milioni-per-triplicare-la-capacita-produttiva/)); he previously ran Takeda's Italian plants (Pisa/Rieti), per a 2020 AboutPharma item (so he knows plasma sites). CEO: Ugo Di Francesco. A ZoomInfo page lists "Nuncio Tucci, Director IT" - aggregator data, treat as a lead to verify only.
- **Angle:** go through the COO's project office before the validation and automation scope is awarded (construction ends end 2026). Ask who owns MES/OT and who the EPC/integrator is - not published.

## CordenPharma, Caponago
- **Equipment (company release, 10 Sep 2026):** Bausch+Stroebel combined isolator line (PFS/vials/cartridges), Syntegon high-speed PFS/cartridge line (500k+ units/day), automated secondary packaging, four more aseptic fill lines planned ([PR Newswire](https://www.prnewswire.com/news-releases/cordenpharma-porte-sa-capacite-de-remplissage-et-de-conditionnement-aseptiques-a-500-millions-dunites-injectables-steriles-par-an-302875435.html)). These are machine OEMs; their PLC/HMI layers are not stated.
- **Roles:** a Computer System Validation Specialist posting at Caponago (Glassdoor, truncated: LIMS-type competencies). A public profile of a Caponago QA validation specialist describes validating **SCADA and laboratory instruments** with IQ/OQ/PQ ([LinkedIn profile, Luca Dell'Oro](https://www.linkedin.com/in/luca-delloro/)) - one person's public self-description; current employer unverified. Site also lists Project Manager and Quality System & Compliance Manager roles.
- **Compliance frame:** the site states EU GMP Volume 4 and ICH Q10 ([CordenPharma](https://cordenpharma.com/facilities/caponago/)) - Annex 11 sits inside Volume 4.
- **Not found:** site head, engineering director, MES.
- **Angle:** CDMO customers audit data integrity; offer CSV and SCADA/lab-system validation for the new isolator lines (mid-2027, 2028). Entry via the CSV specialist and QA compliance manager.

## Chiesi, Nerviano
- **Postings:** Site Plant Controller Lead (works with "the site director", unnamed), Warehouse Manager (prefers experience with automated material handling and AMRs; start-up of the warehouse), Sterile Supervisor (URS definition, layout review, **FAT/SAT, commissioning and qualification for sterile biologics lines**), SME Technology, HSE Specialist, Technical Documentation ([Indeed](https://it.indeed.com/q-chiesi-farmaceutici-l-nerviano,-lombardia-offerte-lavoro.html), [biopharma-careers](https://biopharma-careers.com/jobs/warehouse-manager-nerviano-site-milano-it-chiesi-farmaceutici-258822), [Jooble](https://it.jooble.org/jdp/-7702639375568536421)). This confirms a **start-up phase now** and that the site is hiring operators before automation roles.
- **Stack:** not named. No automation/MES/CSV job found. A separate, unrelated company also uses "Nerviano Site" (SIMIS/NMS Group campus) - do not mix them up.
- **People:** no Nerviano site director named in public sources.
- **Angle:** get in before automation and quality-systems roles are filled; Sterile Supervisor and Technology SME are the likely technical stakeholders for URS and FAT/SAT.

## Novo Nordisk, Anagni
- **Stack:** not named. Press describes "advanced automation and robotics" and says hiring will include automation, validation and MES-skilled engineers ([Ticonsiglio](https://www.ticonsiglio.com/novo-nordisk-anagni-assunzioni-nuovo-piano-industriale/)). A separate Novo posting for an Anagni/Frosinone aseptic automation engineer asks for PLC and SCADA (found in an earlier search; page not re-opened).
- **People:** no site head named. Francesco Rocca (Lazio region president) is the government's extraordinary commissioner, not a company contact ([Regione Lazio](https://www.regione.lazio.it/notizie/innovazione-farmaceutica-rocca-commissario-per-linvestimento-novo-nordisk-ad-anagni)).
- **Angle:** the group uses central Novo engineering for global fill-finish builds; expect a corporate/global partner list. Position through local integrators or validation support rather than direct site sales. Needs a LinkedIn pass for site leadership.

## What you need to source yourself
1. LinkedIn / Sales Navigator: site heads, engineering and capital-projects leads, automation/OT leads, MES/eBR owners, CSV leads, procurement - for all five. I did not use LinkedIn.
2. Current status of the Merck OT/Digital Director and Computer System Validation posts (filled or open) on the companies' own career portals.
3. MES/SCADA/historian vendor per site: ask in discovery; nothing public.
4. Contractors/EPC firms: none named for Kedrion, Chiesi or Novo Anagni.
5. Contact details: none collected; none fabricated.
