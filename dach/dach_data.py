# -*- coding: utf-8 -*-
"""DACH pharma investment dataset (research pass 7 Oct 2026).
All figures are in the ORIGINAL announcement currency. Facts come from web-search result
syntheses (no direct primary-document reads were possible), so confidence is mostly Medium/Low."""

AS_OF = "October 7, 2026"
CHF_EUR = 1.07   # indicative planning rate used ONLY for map shading / combined sort; not market data
USD_EUR = 0.86   # indicative planning rate, same use

SC = "SCADA / process control and automation"
MES = "MES implementation and integration"
DIG = "Digitalization / Industry 4.0"
VAL = "Validation / CSV / data integrity"
LEG = "Legacy system modernization and migration"
LIF = "Lifecycle support and managed services"

ACCOUNTS = [
 # id, name, group, tier, ownership_note, footprint, strategy, reason
 ("roche","Roche (incl. Genentech/Diagnostics)","A","Tier 1","Roche Diagnostics (Penzberg, Mannheim) and Roche Pharma (Basel, Kaiseraugst) are separate buyers inside one group; Genentech has no DACH site.",
  "Largest DACH pharma footprint: Penzberg (biotech + diagnostics raw-materials, ~7,700 staff), Mannheim (diagnostics), Basel and Kaiseraugst (pharma R&D / production), plus Grenzach-Wyhlen and Ludwigshafen-area sites.",
  "Roche says it has invested >EUR 3.5B in German sites since 2020 (about half in Penzberg) and pairs a USD 50B US pledge with continued European R&D builds; Kaiseraugst is being restructured (Rocephin production to end by decade-end, ~230 jobs cut).",
  "Penzberg's EUR 600M+ diagnostics production centre is the single largest Roche investment in Germany and is mid-construction with commissioning 2027-28: a near-term automation/MES/validation entry point."),
 ("lonza","Lonza","A","Tier 1","",
  "Visp (VS) is Lonza's biggest site (biologics, small molecules, ADC bioconjugation); Stein (AG) is adding a commercial aseptic ADC drug-product plant; Basel is HQ.",
  "H1 2026 results were strong and margin guidance was raised; Lonza says its new large-scale mammalian facility in Visp started commercial operation in H1 2026, with the Stein ADC drug-product plant (2027) and Visp bioconjugation facility (2028) under construction.",
  "Three concurrent capital projects at Visp/Stein with 2027-28 start-up dates, at a CDMO that buys automation and MES per suite."),
 ("bayer","Bayer","A","Tier 1","Pharmaceuticals division only; Crop Science/Consumer Health sites excluded.",
  "Pharma production at Bergkamen, Berlin, Leverkusen, Weimar and Wuppertal; Berlin Nordhafen campus hosts cell/gene therapy build-out.",
  "Bayer committed >EUR 1.4B (part of ~EUR 2B) to German pharma technology, new production facilities and digitalization, and is positioning each site as a Centre of Excellence (Bergkamen contrast media/hormones, Leverkusen non-hormonal solids, Wuppertal launch production).",
  "Network-wide modernisation plus a new combined warehouse (ops Q1 2026) and Berlin cell/gene therapy centre (target 2028): multiple site-level digitalization entry points."),
 ("takeda","Takeda","A","Tier 2","",
  "Vienna-Donaustadt (plasma fractionation to packaging), Linz (prefilled syringes / biologics), Orth an der Donau (QC lab); Oranienburg (DE) is a small production site.",
  "Takeda put ~EUR 100M into Linz through 2025 (new syringe line, FY2024 start) and built a new R&D laboratory in Vienna Seestadt; no new 2026 DACH capital project was found.",
  "Main Linz project is completed; follow-on lifecycle/validation work only. No new announcements located."),
 ("merckkgaa","Merck KGaA (Darmstadt)","A","Tier 2","Merck KGaA (Darmstadt; US name EMD) is NOT Merck & Co./MSD. Swiss sites are held via Merck & Cie (Schaffhausen, Altdorf) and Merck Biotech Development Center (Corsier-sur-Vevey).",
  "Darmstadt HQ and production; Swiss API / pharma-chemicals sites in Buchs, Schaffhausen, Altdorf; biotech development centre in Corsier-sur-Vevey (opened June 2023, EUR 250M).",
  "EUR 1B+ Darmstadt investment programme and ~EUR 418M new Swiss production capacity in the last two years; a new quality-control building in Darmstadt was announced. 2026 outlook was raised in May 2026.",
  "Several live projects but amounts, dates and automation scope are only thinly documented in this pass."),
 ("boehringer","Boehringer Ingelheim","A","Tier 2","Privately owned; Animal Health is part of the group.",
  "Ingelheim (HQ/production), Biberach (largest R&D site, ~8,000 staff, biopharma production), Dortmund (production), Vienna (biopharma and R&D).",
  "In June 2026 Boehringer stopped planned German investments of EUR 900M for 2027-2030 (citing health-cost savings law and US pressure) but keeps an EUR 85M QC lab building in Biberach (completion 2027) and an EUR 100M+ Vienna office build.",
  "German capex freeze lowers near-term site-build demand; QC lab (LIMS/validation) in Biberach is the concrete item."),
 ("octapharma","Octapharma","A","Tier 2","Privately held, headquartered in Lachen (SZ).",
  "Vienna-Favoriten (main plasma fractionation), Dessau-Rosslau (DE), Springe (DE), Lachen (CH) HQ.",
  "EUR 200M Vienna expansion (groundbreaking Sept 2023, ~15-month build, inspection/packaging/logistics area more than doubled) plus an earlier EUR 142M production building (2019-2021).",
  "Vienna build is largely complete; expect validation/lifecycle follow-on and further 'planned' expansion stages."),
 ("sandoz","Sandoz","A","Tier 1","Sandoz has been a standalone listed company (SIX: SDZ) since its Novartis spin-off in Oct 2023: the buyer is Sandoz, not Novartis. Hexal AG (Holzkirchen) is a Sandoz subsidiary and is covered here.",
  "Kundl and Schaftenau (Tyrol): antibiotics and biosimilar/biologics finished products; Langkampfen (Tyrol); Germany: Holzkirchen (Hexal HQ and BioTD lab), Barleben, Osterweddingen, Rudolstadt (~3,400 staff).",
  "Standalone Sandoz opened a EUR 200M-package antibiotic plant in Kundl (Mar 2024) and a EUR 150M+ 'BioInject' prefilled-syringe/autoinjector plant in Schaftenau, while closing thyroid-hormone production at Langkampfen/Schaftenau by end-2026.",
  "Active modernisation plus consolidation; spin-off means new standalone IT/OT decisions."),
 ("novartis","Novartis","A","Tier 1","Post-spin-off Novartis no longer includes Sandoz.",
  "Basel Campus (R&D HQ), Stein (AG) sterile and solid dosage production, Schweizerhalle (BL) siRNA/API; Halle (Saale) radioligand plant in Germany.",
  "On 25 Nov 2025 Novartis announced USD 80M for siRNA at Schweizerhalle (+80 jobs by 2028) and USD 26M for sterile dosage forms in Stein while ending solid dosage and sterile packaging there by end-2027 (~550 jobs), and EUR 34.7M for a radioligand site in Halle.",
  "Several modest but concrete production projects with 2027-28 timelines; denominated in USD/EUR."),
 ("gsk","GSK","A","Tier 3","",
  "Marburg (vaccines: MenB, mumps, rabies/FSME, filling and freeze-drying); Dresden flu/hepatitis vaccine plant is being closed by 2028 (~640 jobs).",
  "GSK is concentrating vaccine production in Marburg (MenB EUR 162M, mumps EUR 10M, EUR 13M filling/freeze-dry renewal; announcement dates not confirmed) while exiting Dresden.",
  "Marburg projects appear older than the 2024 window; Dresden closure is a negative signal."),
 ("bbraun","B. Braun","A","Tier 2","Family-owned (B. Braun SE); Aesculap and Hospital Care also covered.",
  "Melsungen (HQ; infusion therapy, dialysis machines), Sempach (CH; disinfectants), Tuttlingen (Aesculap).",
  "Several expansions: EUR 150M new infusion-article plant in Melsungen (opened), EUR 60M expansion for dialysis machines and infusion pumps, and CHF 70M N.I.C.O. disinfectant plant in Sempach.",
  "Mix of device and pharma-liquid manufacturing; exact dates were not confirmed in this pass."),
 ("bachem","Bachem","A","Tier 1","",
  "Bubendorf (BL; HQ, peptides and oligonucleotides), Vionnaz (VS), St. Helens (UK, outside scope).",
  "Bachem guides CHF 350-400M annual capex; 'Building K' in Bubendorf is ramping commercial production in 2026 and a CHF 500M+ greenfield at Sisslerfeld (AG) is planned to start production in 2030; 22 Jul 2026 coverage reports a new large-scale production plant plan.",
  "Fastest-growing peptide CDMO in DACH with a greenfield about to enter detailed design/automation selection."),
 ("biontech","BioNTech","A","Tier 3","BioNTech absorbed CureVac (incl. its Tuebingen sites).",
  "Mainz (HQ) remains; Marburg, Idar-Oberstein and Tuebingen manufacturing sites are being closed (end-2027 to end-2028) after no buyers were found.",
  "Restructuring: ~1,800+ jobs affected, ~EUR 500M annual savings targeted by 2029.",
  "Net negative for new automation; potential decommissioning/data-migration work only."),
 ("msd","MSD (Merck & Co.; incl. Intervet / Animal Health)","A","Tier 3","MSD is the name of Merck & Co., Inc. (Rahway, NJ, USA) outside the US and is a different company from Merck KGaA. Animal Health (Intervet) is part of MSD; its DACH footprint includes Schwabenheim (DE) and a Boxmeer (NL) hub outside scope.",
  "Lucerne (CH HQ; new 'One Roof' building, CHF 60M), Schachen (R&D/biotech site, >CHF 230M invested over 20 years); Intervet Deutschland (Schwabenheim, Unterschleissheim).",
  "No new DACH manufacturing project located; Swiss spend is office/R&D.",
  "Limited manufacturing activity found."),
 ("sanofi","Sanofi","A","Tier 1","",
  "Frankfurt-Hoechst (Industriepark Hoechst, insulin and pharma), plus a Lonza-built dedicated biologics facility in Visp (Ibex Solutions).",
  "Sanofi confirmed a ~EUR 1.3B new insulin plant at Hoechst; the EU approved ~EUR 400M state aid in Sept 2026, with completion targeted around 2029.",
  "Largest single new pharma plant in Germany with state-aid approval just received: engineering/automation partner selection phase."),
 ("vetter","Vetter Pharma","A","Tier 1","Family-owned CDMO (Ravensburg).",
  "Ravensburg and Langenargen (DE), Rankweil (AT, clinical); Skokie (US, outside scope).",
  "Vetter broke ground in Saarlouis in May 2026 (EUR ~480-500M first phase, ops 2031, up to 1,500 jobs, EUR 47M EU state aid) alongside ongoing capacity expansions in Ravensburg/Langenargen under a ~EUR 1.5B programme.",
  "Greenfield aseptic fill-finish site: classic Orise fit across SCADA/MES/validation."),
 ("fresenius","Fresenius Kabi","A","Tier 2","Subsidiary of Fresenius SE.",
  "Graz/Werndorf and Linz (AT), Friedberg (DE), Oberdorf (CH).",
  "EUR ~28M additional investment in Graz (biosimilar filling, up to 2026) after >EUR 60M over the prior three years; no larger new project found.",
  "Incremental Austrian investment; no big new greenfield identified."),
 ("cordenpharma","CordenPharma","A","Tier 1","Owned by International Chemical Investors Group (ICIG).",
  "Plankstadt (DE), Muttenz/Liestal region (CH, new), Brussels and Colorado (outside scope).",
  "CordenPharma is investing ~EUR 1B in peptides, of which ~EUR 500M for a new greenfield plant at Getec Park in Muttenz (construction 2025-2027, commercial operation H1 2028, 300 jobs).",
  "Greenfield peptide plant at the design/build stage in the 2026-27 window."),
 ("abbott","Abbott","A","Tier 3","",
  "Wiesbaden (HQ), Neustadt am Ruebenberge (Creon), Hannover; Baar, Altishofen, Allschwil (CH).",
  "No new DACH production investment announced in the sources found.",
  "No project identified."),
 ("gruenenthal","Gruenenthal","A","Tier 3","Privately owned.",
  "Aachen (HQ/R&D), Stolberg (DE) and a Swiss site; recent big capex is in Latin America (EUR 80M+).",
  "No new DACH investment found; Stolberg production activity reported closed/reduced.",
  "No project identified."),
 ("ucb","UCB","A","Tier 2","UCB Farchim SA is the Swiss subsidiary (Bulle, FR).",
  "Bulle (FR): biologics manufacturing; Monheim (DE) is a Germany-based unit.",
  "UCB is investing CHF 100M+ in Bulle: new production unit for a key biologics compound (relocated from Belgium), operational ~2029, full capacity 2030, +80 jobs; CHF 15M QC lab (mid-2026) and CHF 10M cold unit.",
  "Concrete Swiss project with a long lead time."),
 ("sartorius","Sartorius","A","Tier 2","",
  "Goettingen (HQ, membranes/filters), Freiburg (cell and gene therapy components), Marburg and Ulm.",
  "EUR ~25M membrane production building in Goettingen (6,000 m2) and a EUR 140M+ cell/gene therapy competence centre in Freiburg (2026 coverage); further capacity expansion planned in 2026.",
  "Equipment maker with its own growing production footprint."),
 ("rentschler","Rentschler Biopharma","A","Tier 2","Family-owned; withdrew from cell and gene therapy in early 2025.",
  "Laupheim (DE HQ, microbial/mammalian CDMO); Milford, MA (outside scope).",
  "'Largest single investment' in Laupheim: four-storey buffer media station (construction from spring 2025, operational 2028), 'high double-digit million' euro.",
  "Utility/buffer infrastructure with automation and MES interfaces."),
 ("lilly","Eli Lilly","A","Tier 1","",
  "Alzey (Rhineland-Palatinate) is Lilly's only new DACH production site (Mounjaro/injectables); no pre-existing DACH plant.",
  "Alzey was announced in Nov 2023 at ~EUR 2.3B / 1,000 jobs; in 2026 Lilly cut the remaining investment by about half and the job target to ~500 because of German healthcare-cost measures, but still targets ops end-2027.",
  "Greenfield injectable plant still under construction; scope reduction adds uncertainty."),
 # Group B
 ("finzelberg","Finzelberg","B","Tier 3","Owned by Willy Fischer / family group.","Andernach (DE): plant extracts.","No project found in this pass.","No project identified."),
 ("plbio","PL BioScience","B","Tier 3","Aachen-based startup; Series A EUR 7.8M (Aug 2024).","Aachen (DE): human platelet lysate (GMP).","Expanding Aachen HQ to >1,200 m2 for up to 20,000 L/yr GMP-grade HPL.","Small project; limited automation budget."),
 ("terumo","Terumo","B","Tier 3","Japanese group; Terumo Deutschland in Eschborn is a sales entity.","Eschborn (DE) sales; no DACH manufacturing found.","No DACH production or investment found.","No project identified."),
 ("beiersdorf","Beiersdorf","B","Tier 3","Consumer/cosmetics; sold its Bode Chemie unit to Hartmann.","Hamburg (HQ, R&D), Leipzig (EUR 220M plant), Waldheim closed.","EUR 139M innovation centre in Hamburg (planned completion 2028; R&D, not manufacturing) and Leipzig plant expansion.","Consumer-goods rather than pharma core."),
 ("biospring","BioSpring","B","Tier 1","Frankfurt-based oligonucleotide CDMO.","Frankfurt-Fechenheim (cGMP gRNA/mRNA), Offenbach (new site).",
  "Building a large-scale nucleic acid API plant in Offenbach ('several hundred million euros', ~200 jobs, construction to end of 2027) after a double-digit-million Fechenheim expansion.",
  "Greenfield GMP plant in construction: strong fit."),
 ("ypsomed","Ypsomed","B","Tier 1","SIX-listed; Swiss.","Solothurn, Burgdorf (CH); Schwerin (DE).",
  "CHF ~200M in Solothurn (new production levels, tool shop, high-bay), CHF 21M in Burgdorf, and ~EUR 500M in two phases in Schwerin to the end of the decade (400-500M pens/yr, 1,000 staff).",
  "Autoinjector/pen assembly: high-volume device automation + MES."),
 ("biogen","Biogen","B","Tier 2","","Luterbach/Solothurn (CH): large-scale biologics.","~CHF 1.5B Luterbach plant, operational since 2021; no new 2026 project found.","Mature site; lifecycle support."),
 ("richter","Richter Pharma","B","Tier 3","Veterinary pharma (Wels).","Wels (AT).","EUR 35M+ VetViva production facility opened 2025, ~120 jobs.","Completed in 2025."),
 ("wackerbiotech","Wacker Biotech","B","Tier 2","Division of Wacker Chemie.","Jena (microbial CDMO), Halle (mRNA competence centre).","Wacker expanded Halle (mRNA lines, ~200 hires) and Jena; dates/amount for Halle not confirmed.","Mature; follow-on only."),
 ("rotop","Rotop Pharmaka","B","Tier 2","Backed by GENUI and SHS Capital.","Dresden-Rossendorf (DE).","Two highly automated radiopharmaceutical factories, start from 2028, 'double-digit million' euro programme.","Germany's largest radiopharma project; automated GMP lines."),
 ("merz","Merz Pharma","B","Tier 2","Family-owned; Merz Aesthetics and Merz Therapeutics.","Dessau-Rosslau (DE); Reinheim (DE, closing).","New packaging line opened June 2026; EUR 100M+ planned in Dessau by 2028; Reinheim production consolidating to Dessau.","Consolidation into Dessau drives new lines."),
 ("hexal","Hexal (Sandoz Germany)","B","Tier 2","Hexal AG is a Sandoz subsidiary; see Sandoz.","Holzkirchen (DE).","40-year anniversary in 2026; EUR 25M BioTD lab in Holzkirchen completed Q4 2023.","Covered under Sandoz."),
 ("ferring","Ferring","B","Tier 3","Swiss-HQ (Saint-Prex).","Kiel (DE), Saint-Prex (CH).","EUR ~40M production building in Kiel (undated source); CHF 30M biotech centre in St-Prex (2018).","Older projects."),
 ("bode","Bode Chemie","B","Tier 3","Owned by PAUL HARTMANN AG.","Hamburg (DE).","No project found in this pass.","No project identified."),
 ("siegfried","Siegfried","B","Tier 1","SIX-listed CDMO.","Zofingen (HQ), Evionnaz (CH); Hameln, Minden (DE).",
  "Hameln: two new prefilled syringe/cartridge lines (first revenue 2026, second 2027); Minden new multi-purpose drug-substance plant (nearing completion, first revenue H2 2025); CHF 25M R&D centre in Evionnaz.",
  "Concrete 2026-27 line start-ups."),
 # Group C
 ("abbvie","AbbVie","C","Tier 3","","Ludwigshafen (R&D, ~2,000 staff).","EUR 150M 'LUnA' R&D building, in operation 2027.","R&D lab project."),
 ("csl","CSL / CSL Behring","C","Tier 2","CSL Behring Marburg and Bern; CSL Seqirus not found in DACH.","Marburg (DE), Bern (CH).","CHF 300M immunoglobulin 'Protinus' project in Bern; EUR 31M filling/freeze-drying in Marburg.","Dates not verified."),
 ("catalent","Catalent","C","Tier 3","Owned by Novo Holdings (acquired Dec 2024); three fill-finish sites went to Novo Nordisk.","Eberbach (DE) oral solid dose site.","No project found.","No project identified."),
 ("pfizer","Pfizer","C","Tier 3","","Freiburg (DE): tablets/capsules.","EUR 300M high-containment plant opened 2022; in June 2026 the CEO said German investments are under review.","Completed; risk of freeze."),
 ("jnj","Johnson & Johnson Innovative Medicine","C","Tier 2","Cilag/Janssen.","Schaffhausen (CH; ~2,200 staff), Neuss (DE HQ).","Schaffhausen continues to expand biotherapeutic capacity (>CHF 1B over 25 years); no 2026 project located.","Amount not found."),
 ("astrazeneca","AstraZeneca","C","Tier 3","","Wedel (DE) production.","No DACH investment found.","No project identified."),
 ("kbi","KBI Biopharma","C","Tier 3","JSR subsidiary.","Plan-les-Ouates/Geneva (CH).","Integrated Geneva facility opened Oct 2022; no new investment found.","Mature."),
]

# Skipped Group C: Novo Nordisk (no DACH manufacturing/R&D found), Regeneron, Amgen (HQ/commercial only),
# FUJIFILM Biotechnologies, Curia, National Resilience, Amneal, Avid Bioservices (no DACH site found).
SKIPPED = {
 "Novo Nordisk":"Only a commercial HQ in Mainz found; its European capex goes to Denmark/France.",
 "Amgen":"European HQ in Zug/Rotkreuz is commercial; no production or R&D investment found.",
 "Regeneron":"No DACH site found.","FUJIFILM Biotechnologies":"No DACH site found.","Curia":"No DACH site found.",
 "National Resilience":"No DACH site found.","Amneal":"No DACH site found.","Avid Bioservices":"No DACH site found."}

def src(url, pub, date="Unverified", conf="Medium"):
    return dict(url=url, publisher=pub, date=date, confidence=conf)

def fit(*items):
    return [dict(area=a, strength=s, reason=r) for a, s, r in items]

M_BIO="biologics/mAbs"; M_FF="fill-finish/sterile injectables"; M_SM="small molecule/API"; M_CGT="cell & gene therapy"
M_PEP="GLP-1/peptides"; M_DEV="devices/combination products"; M_VAC="mRNA/vaccines"; M_OSD="oral solid dose"
M_PLA="plasma-derived"; M_RAD="radiopharmaceuticals"; M_OLI="oligonucleotides/nucleic acids"; M_OTH="other (R&D / consumer)"

# site tuple: key fields. region codes: DE-xx, AT-x, CH-xx
S = []
def site(acc, name, city, region, lat, lon, ptype, modality, cur, amt, disp, jobs, status, start, window, opp, scope, fits, sources, notes="", vendors=""):
    S.append(dict(account=acc, site_name=name, city=city, state=region, lat=lat, lon=lon, project_type=ptype, modality=modality,
        currency=cur, investment=amt, investment_display=disp, jobs=jobs, status=status, expected_start=start, in_window=window,
        opportunity_status=opp, technical_scope=scope, orise_fit=fits, incumbent_vendors=vendors, sources=sources, notes=notes))

site("roche","Roche Diagnostics Production Centre (raw materials)","Penzberg","DE-BY",47.7508,11.3764,"BROWNFIELD",[M_BIO,M_OTH],"EUR",600000000,"EUR 600M+ (largest single Roche investment in Germany)",200,"under construction","2027-12 (completion); production 2028",True,"OPEN OPPORTUNITY",
 "New production centre on the Penzberg biotech campus for diagnostic raw materials (enzymes, antibodies, nucleotides). Groundbreaking 28 Nov 2024; completion planned 2027, then qualification, production from 2028 with ~200 initial staff.",
 fit((SC,"Strong","Highly automated GMP-like raw-material production must be commissioned 2027 and qualified before 2028 start."),(MES,"Strong","New batch production and release flow for a new product family needs MES/recipe and data integration."),(VAL,"Moderate","Qualification phase follows completion in 2027."),(DIG,"Moderate","Campus-scale data/OT integration in a EUR 3.5B+ German programme.")),
 [src("https://www.bionity.com/de/news/1188095/roche-eroeffnet-neues-hightech-innovationszentrum-fuer-300-millionen-euro-in-bayern.html","Bionity","2026-02","Medium"),src("https://www.aerzteblatt.de/nachrichten/156068/Roche-legt-Grundstein-fuer-600-Millionen-Investition","Aerzteblatt","2024-11","Medium"),src("https://www.onvista.de/news/2026/06-09-roche-haelt-trotz-berliner-sparpaket-an-millionen-investition-fest-0-20-26519960","onvista","2026-06-09","Medium")],
 "Roche reaffirmed the investment in June 2026 despite the German savings package.")
site("roche","Roche Diagnostics Innovation Centre","Penzberg","DE-BY",47.7520,11.3740,"BROWNFIELD",[M_OTH],"EUR",300000000,"EUR ~300M",None,"operational","Opened Feb 2026",True,"Monitor",
 "23,000 m2 development/laboratory building opened Feb 2026; ~1,000 of 7,700 site staff moved in. Lab/R&D rather than manufacturing.",
 fit((DIG,"Weak","Lab data/OT integration; no manufacturing scope."),(LIF,"Weak","Post-opening support of building systems and labs.")),
 [src("https://www.ingenieur.de/technik/fachbereiche/bau/durchgetaktet-bis-zum-letzten-gewerk-so-entstand-roches-hightech-labor/","ingenieur.de","2026-02-25","Medium"),src("https://www.pharmazeutische-zeitung.de/roche-eroeffnet-neues-diagnostik-innovationszentrum-162786/","Pharmazeutische Zeitung","2026-02","Medium")])
site("roche","Roche Basel Building 12 (research and development)","Basel","CH-BS",47.5596,7.6009,"BROWNFIELD",[M_OTH],"CHF",500000000,"CHF ~500M",None,"under construction","Completion 2029",False,"Monitor",
 "Flexible R&D building for up to 450 early-development researchers; groundbreaking Oct 2025, completion 2029. Laboratory scope, long lead.",
 fit((DIG,"Weak","Lab automation/data platforms in 2028-29; too early for automation vendors.")),
 [src("https://www.roche.ch/en/media-switzerland/informationen/med-ch-2025-10-29","Roche Switzerland","2025-10-29","High"),src("https://www.roche.ch/en/stories/groundbreaking-building12","Roche Switzerland","2025-10","High")],"CHF 1.2B Basel programme (research buildings and production renovation) runs to 2030.")
site("roche","Roche Kaiseraugst Production Site Restructuring","Kaiseraugst","CH-AG",47.5340,7.7230,"BROWNFIELD",[M_SM,M_BIO],"CHF",500000000,"CHF 500M+ (headline per Moneycab title; details unverified)",None,"announced","Unverified",False,"Monitor",
 "Moneycab reports a CHF 500M+ investment at Kaiseraugst while Roche ends Rocephin production by the end of the decade and cuts ~230 jobs. Scope of new capital items not confirmed.",
 fit((LEG,"Weak","Restructuring may require system consolidation/migration."),(LIF,"Weak","Ongoing support during product transfers.")),
 [src("https://www.moneycab.com/?p=1071859","Moneycab","Unverified","Low"),src("https://www.moneycab.com/schweiz/roche-baut-die-produktion-in-kaiseraugst-um/amp/","Moneycab","Unverified","Medium")],"Headline figure not independently confirmed; treat as Low confidence.")
site("roche","Roche Mannheim diagnostics expansion","Mannheim","DE-BW",49.4875,8.4660,"BROWNFIELD",[M_OTH],"EUR",400000000,"EUR 400M+ across five construction projects",None,"under construction","Unverified",False,"Monitor",
 "Five projects at the Mannheim diagnostics site: laboratory, distribution and production buildings, chilled-water storage and IT infrastructure; plus an instrument launch centre.",
 fit((DIG,"Moderate","Facility/IT infrastructure build-out."),(MES,"Weak","Diagnostics production lines may need MES.")),
 [src("https://www.bionity.com/de/news/1157476/400-millionen-euro-roche-baut-mannheimer-standort-aus.html","Bionity","Unverified","Medium")],"Date of the five-project programme not confirmed.")
site("lonza","Lonza Visp large-scale mammalian facility (Ibex Solutions)","Visp","CH-VS",46.2940,7.8820,"BROWNFIELD",[M_BIO],"CHF",None,"Amount not disclosed in sources found",None,"commissioning","Commercial operation from H1 2026",True,"OPEN OPPORTUNITY",
 "Large-scale mammalian biologics plant at Ibex Solutions started commercial operation in H1 2026 and is in ramp-up; it includes a dedicated Sanofi facility. Ramp-up and tech-transfer support.",
 fit((MES,"Moderate","Ramp-up of multi-customer suites typically needs MES recipe/batch work."),(VAL,"Moderate","CSV and data-integrity for newly commissioned suites."),(LIF,"Moderate","Early-life support and managed services.")),
 [src("https://www.pharmamanufacturing.com/sector/contract-manufacturing/article/55378861/lonzas-large-scale-mammalian-site-in-visp-switzerland-continues-ramp-up-process","PharmaManufacturing","Unverified","Medium"),src("https://www.bluewin.ch/en/news/lonza-invests-in-production-and-remains-on-target-li.3224385","blue News","2026","Medium"),src("https://new.1815.ch/news/wallis/aktuell/neue-arbeitsplaetze-fuer-visp","1815.ch","Unverified","Low")])
site("lonza","Lonza Visp large-scale bioconjugation (ADC) facility","Visp","CH-VS",46.2950,7.8840,"BROWNFIELD",[M_BIO,M_SM],"CHF",None,"Amount not found (3,000 m2, three suites to 1,200 L)",None,"under construction","Operations 2027 (dedicated suite) / 2028",True,"OPEN OPPORTUNITY",
 "New 3,000 m2 bioconjugation plant with three large-scale suites (up to 1,200 L): one dedicated to a global partner for commercial ADC, two multi-purpose. Construction progressing per Lonza H1/Q1 2026.",
 fit((SC,"Strong","High-containment conjugation suites need process control from design through commissioning in 2027."),(MES,"Strong","Multi-purpose suites require recipe-driven MES and eBR."),(VAL,"Moderate","Commissioning-qualification in 2027-28.")),
 [src("https://live.deutsche-boerse.com/news/LonzaDelivers-Strong-Performance-in-Q1-2026-in-Line-with-Expectations-and-Confirms-Full-Year-Outlook-2026-330ea2f2-33b8-4bd2-9769-3081c8ae07cb","Lonza via Deutsche Boerse","2026","High"),src("https://www.dcatvci.org/supplier-news/lonza-investing-in-large-scale-biomanufacturing-bioconjugation-drug-product-manufacturing/","DCAT","Unverified","Medium")])
site("lonza","Lonza Stein aseptic ADC drug-product facility","Stein","CH-AG",47.5410,7.9460,"BROWNFIELD",[M_FF,M_BIO],"CHF",None,"Amount not found (115 jobs at peak)",115,"under construction","Operations 2027",True,"OPEN OPPORTUNITY",
 "Commercial-scale, high-containment aseptic fill-finish for ADCs, operational 2027 (construction progressing as of H1 2026).",
 fit((SC,"Strong","Aseptic fill lines, isolators and HVAC/utilities need integrated control."),(MES,"Strong","Commercial-scale fill-finish needs eBR and equipment integration."),(VAL,"Strong","Validation of new sterile process ahead of 2027.")),
 [src("https://live.deutsche-boerse.com/news/LonzaDelivers-Strong-Performance-in-Q1-2026-in-Line-with-Expectations-and-Confirms-Full-Year-Outlook-2026-330ea2f2-33b8-4bd2-9769-3081c8ae07cb","Lonza via Deutsche Boerse","2026","High"),src("https://www.europeanpharmaceuticalreview.com/news/lonza-to-enhance-commercial-antibody-drug-conjugate-supply-capacity/187684.article","European Pharmaceutical Review","Unverified","Medium")])
site("bayer","Bayer Bergkamen Centre of Excellence and Combined Warehouse","Bergkamen","DE-NW",51.6180,7.6330,"BROWNFIELD",[M_SM,M_OSD],"EUR",None,"Part of >EUR 1.4B German pharma programme (not split by site)",None,"commissioning","Warehouse ops Q1 2026",True,"OPEN OPPORTUNITY",
 "Bergkamen becomes the Centre of Excellence for contrast media and hormone products with additional therapeutics capacity; a climate-neutral combined warehouse for Bergkamen and Wuppertal API started operations in Q1 2026.",
 fit((DIG,"Moderate","Part of a network digitalization programme."),(SC,"Moderate","Technology upgrades/new production facilities."),(LIF,"Moderate","Commissioning of the new warehouse and logistics automation.")),
 [src("https://www.pharmazeutische-zeitung.de/bayer-investiert-milliarden-betrag-in-biotechnologie-sparte-132304/","Pharmazeutische Zeitung","Unverified","Medium"),src("https://www.fiercepharma.com/manufacturing/bayer-earmarks-22-billion-upgrade-drug-manufacturing-shedding-some-facilities","Fierce Pharma","Unverified","Medium"),src("https://www.bayer.com/media/download/d423c37e-df47-495a-bcf4-5bfec99a647c/2025-0026.pdf","Bayer","2025","High")],"The EUR 2B programme dates from 2022; per-site amounts are not public.")
site("bayer","Bayer Leverkusen Supply Centre (non-hormonal solids)","Leverkusen","DE-NW",51.0300,6.9840,"BROWNFIELD",[M_OSD],"EUR",None,"Part of >EUR 1.4B programme",None,"under construction","Unverified",False,"Monitor",
 "Leverkusen is being built into the Centre of Excellence for non-hormonal solid dosage forms.",
 fit((DIG,"Weak","Network digitalization initiatives."),(LEG,"Weak","Consolidation of legacy lines.")),
 [src("https://www.pharmazeutische-zeitung.de/bayer-investiert-milliarden-betrag-in-biotechnologie-sparte-132304/","Pharmazeutische Zeitung","Unverified","Medium")])
site("bayer","Bayer Wuppertal launch production and new technologies","Wuppertal","DE-NW",51.2562,7.1508,"BROWNFIELD",[M_BIO,M_SM],"EUR",None,"Part of >EUR 1.4B programme",None,"under construction","Unverified",False,"Monitor",
 "Wuppertal focuses on launch production and new production technologies within the EUR 2B programme.",
 fit((DIG,"Weak","Launch-site digitalization."),(SC,"Weak","New technology introduction.")),
 [src("https://www.morningstar.co.uk/uk/news/AN_1648718658294881600/bayer-to-invest-eur2-billion-to-strengthen-pharmaceutical-division.aspx","Morningstar","Unverified","Medium")])
site("bayer","Bayer Berlin Centre for Gene and Cell Therapies","Berlin","DE-BE",52.5420,13.3560,"BROWNFIELD",[M_CGT],"EUR",None,"Amount not found",None,"under construction","Target operation 2028",False,"OPEN OPPORTUNITY",
 "Translation centre with GMP production area on the Bayer Nordhafen campus with Charite; construction from 2025, planned operation 2028.",
 fit((MES,"Moderate","Small-batch cell/gene therapy GMP needs electronic batch records."),(VAL,"Moderate","GMP qualification for a new suite."),(DIG,"Weak","Data capture for translation workflows.")),
 [src("https://www.bayer.com/media/aufbau-von-translationszentrum-fuer-gentherapien-und-zelltherapien-in-berlin-beginnt/","Bayer","2025","High"),src("https://chemanager-online.com/en/node/440896","CHEManager","2025","Medium")])
site("takeda","Takeda Linz prefilled syringe and biologics site","Linz","AT-OO",48.3069,14.2858,"BROWNFIELD",[M_FF,M_BIO,M_DEV],"EUR",100000000,"EUR ~100M by 2025",None,"operational","Production FY2024",False,"Monitor",
 "New prefilled-syringe line at Takeda's global centre for prefilled syringes and self-medication biologics; announced May 2023.",
 fit((LIF,"Weak","Post-start-up support."),(VAL,"Weak","Continued line qualification.")),
 [src("https://industriemagazin.at/chemie/wiener-pharma-konzern-takeda-mit-neuer-fuehrung/","Industriemagazin","2023-05","Medium")])
site("takeda","Takeda Vienna R&D laboratory (Seestadt)","Vienna","AT-W",48.2200,16.5000,"GREENFIELD",[M_BIO,M_PLA],"EUR",None,"Three-digit million EUR (exact figure not stated)",250,"operational","From 2025",False,"Monitor",
 "New R&D building in Vienna Seestadt for ~250 researchers (from 2025). Laboratory, no manufacturing.",
 fit((DIG,"Weak","Lab informatics only.")),
 [src("https://investinaustria.at/en/news-events-press/global-player-takeda-is-building-a-research-and-development-laboratory-in-vienna-donaustadt/","Invest in Austria","Unverified","Medium")])
site("merckkgaa","Merck KGaA Darmstadt QC building and investment programme","Darmstadt","DE-HE",49.8728,8.6512,"BROWNFIELD",[M_SM,M_BIO],"EUR",None,"EUR 1B+ programme; QC building amount not found",None,"announced","Unverified",False,"Monitor",
 "Aerzteblatt reports Merck investing in a new quality-control building at Darmstadt; Merck also runs an EUR 1B+ Darmstadt investment programme including a EUR 300M+ research centre (older).",
 fit((VAL,"Weak","QC/LIMS and data integrity in a new lab building."),(DIG,"Weak","Site digitalization.")),
 [src("https://www.aerzteblatt.de/news/merck-investiert-in-darmstadt-in-neues-gebaeude-fuer-qualitaetskontrolle-85f3f5ae-a93b-4e37-8f17-47cfed920609","Aerzteblatt","Unverified","Low"),src("https://www.chemie.de/news/1160203/merck-investiert-1-mrd-in-den-standort-darmstadt.html","Chemie.de","Unverified","Medium")],"Dates not confirmed.")
site("merckkgaa","Merck Swiss production network (Buchs / Schaffhausen / Altdorf)","Schaffhausen","CH-SH",47.6970,8.6340,"BROWNFIELD",[M_SM],"EUR",418000000,"EUR ~418M new Swiss production capacity in last two years",None,"operational","Unverified",False,"Monitor",
 "Merck states ~EUR 418M new production capacity across Swiss operations (APIs, intermediates, reference materials).",
 fit((LIF,"Weak","Support of newly commissioned capacity.")),
 [src("https://www.s-ge.com/invest/de/artikel/success-stories/merck-die-schweiz-bietet-attraktive-und-stabile-rahmenbedingungen-fuer","S-GE","Unverified","Medium")],"Time window of the EUR 418M not confirmed.")
site("merckkgaa","Merck Biotech Development Center","Corsier-sur-Vevey","CH-VD",46.4630,6.8550,"GREENFIELD",[M_BIO],"EUR",250000000,"EUR 250M",None,"operational","Opened June 2023",False,"Closed/late",
 "Clinical-manufacturing biotech centre (250 staff) opened June 2023: outside the Jan 2024 window.",
 [],[src("https://endpts.com/?p=249831","Endpoints","Unverified","Medium"),src("https://www.pharmaceutical-technology.com/?p=91715","Pharmaceutical Technology","Unverified","Medium")])
site("boehringer","Boehringer Biberach QC laboratory building","Biberach","DE-BW",48.0960,9.7900,"BROWNFIELD",[M_BIO],"EUR",85000000,"EUR 85M",None,"under construction","Completion 2027",True,"OPEN OPPORTUNITY",
 "Quality-assurance laboratory building at Biberach, completing 2027; survived the June 2026 freeze on EUR 900M of 2027-30 German investments.",
 fit((VAL,"Moderate","LIMS and data-integrity validation for new QC labs."),(DIG,"Moderate","Lab/OT data integration.")),
 [src("https://www.pharmazeutische-zeitung.de/boehringer-ingelheim-zieht-investitionen-zurueck-165764/","Pharmazeutische Zeitung","2026-06","Medium"),src("https://www.schwaebische.de/wirtschaft/boehringer-ingelheim-waechst-kraeftig-stoppt-aber-investitionen-in-deutschland-4720079","Schwaebische Zeitung","2026","Medium")],"Wider German capex freeze (EUR 900M) lowers odds of new plant projects.")
site("boehringer","Boehringer Vienna administration building","Vienna","AT-W",48.2300,16.4000,"BROWNFIELD",[M_OTH],"EUR",100000000,"EUR 100M+",990,"under construction","Completion 2027",True,"Monitor",
 "New administrative building (~990 staff); no manufacturing scope.",
 fit((DIG,"Weak","Building/IT only.")),
 [src("https://www.drweb.de/100-millionen-fuer-wien-87-milliarden-fuer-die-usa-boehringers-zoll-kalkuel/","drweb.de","2026","Low")])
site("octapharma","Octapharma Vienna-Favoriten plasma production expansion","Vienna","AT-W",48.1700,16.3800,"BROWNFIELD",[M_PLA],"EUR",200000000,"EUR 200M (incl. earlier EUR 142M building)",60,"operational","Build completed ~Dec 2024",False,"Monitor",
 "Extension started Sept 2023 and finished in ~15 months: inspection, packaging and logistics area more than doubled (2,800 to 6,300 m2); further stages planned.",
 fit((LIF,"Moderate","Post-start-up lifecycle/validation."),(MES,"Weak","Packaging/logistics MES interfaces.")),
 [src("https://www.tt.com/artikel/14899556/plasmaproduzent-octapharma-baut-wiener-standort-um-142-mio-euro-aus","Tiroler Tageszeitung","Unverified","Medium"),src("https://investinaustria.at/en/news-events-press/octapharma-is-further-expanding-its-viennese-facility-and-investing-eur-200-million","Invest in Austria","Unverified","Medium")])
site("sandoz","Sandoz Kundl antibiotic plant","Kundl","AT-T",47.5069,12.0124,"BROWNFIELD",[M_SM],"EUR",200000000,"EUR 200M package",None,"operational","Opened Mar 2024",False,"Monitor",
 "Enzymatic amoxicillin process plant opened March 2024 under a EUR 200M investment package supported by the Austrian government. Mothballed lines follow.",
 fit((LIF,"Moderate","Post-start-up support at a standalone Sandoz.")),
 [src("https://www.novartis.com/at-de/stories/sandoz-modernisiert-antibiotika-produktion-kundl","Novartis Austria","2021","Medium"),src("https://industriemagazin.at/chemie/sandoz-tirol-naechste-stilllegung-nach-kundl/","Industriemagazin","Unverified","Medium")])
site("sandoz","Sandoz Schaftenau BioInject prefilled-syringe plant","Schaftenau","AT-T",47.5390,12.1530,"BROWNFIELD",[M_FF,M_DEV,M_BIO],"EUR",150000000,"EUR 150M+",None,"operational","Unverified",False,"Monitor",
 "Prefilled syringe and autoinjector line for biosimilars and biologics.",
 fit((LIF,"Moderate","Lifecycle and line expansion support."),(MES,"Weak","Device assembly/packaging integration.")),
 [src("https://www.aerztezeitung.de/Wirtschaft/Sandoz-ruestet-sich-fuer-den-weltweiten-Wettbewerb-248042.html","Aerzte Zeitung","Unverified","Low")],"Opening date not confirmed.")
site("sandoz","Sandoz / Hexal Holzkirchen BioTD laboratory","Holzkirchen","DE-BY",47.8780,11.6990,"BROWNFIELD",[M_BIO],"EUR",25000000,"EUR 25M",None,"operational","Q4 2023",False,"Monitor",
 "Biopharma technical development lab (biosimilars) at Hexal's Holzkirchen HQ. Hexal is part of Sandoz.",
 fit((LIF,"Weak","Lab systems support.")),
 [src("https://www.pharmaceutical-tech.com/projects/sandoz-plans-to-invest-25-million-to-expand-its-biopharma-technical-development-capabilities-in-holzkirchen-germany","Pharmaceutical Technology","2022","Medium")])
site("novartis","Novartis Schweizerhalle siRNA manufacturing","Schweizerhalle (Muttenz)","CH-BL",47.5460,7.6900,"BROWNFIELD",[M_OLI,M_SM],"USD",80000000,"USD 80M (USD-denominated announcement)",80,"announced","Jobs by end 2028",True,"OPEN OPPORTUNITY",
 "Expansion of siRNA manufacturing for cardiovascular/renal/metabolic therapies, announced 25 Nov 2025; 80 new positions by end-2028.",
 fit((SC,"Moderate","New siRNA production capacity needs control-system build."),(MES,"Moderate","New GMP process steps need batch execution."),(VAL,"Moderate","Qualification of new capacity.")),
 [src("https://www.novartis.com/ch-de/news/media-releases/novartis-passt-produktionsaktivitaeten-der-schweiz-und-investiert-innovative-herstelltechnologien","Novartis","2025-11-25","High"),src("https://www.europeanpharmaceuticalreview.com/news/novartis-adjusts-manufacturing-strategy-in-switzerland-to-secure-competitiveness/268209.article","European Pharmaceutical Review","2025-11","Medium")],"Announcement in USD; subject to consultation process.")
site("novartis","Novartis Stein sterile dosage form production","Stein","CH-AG",47.5420,7.9460,"BROWNFIELD",[M_FF],"USD",26000000,"USD 26M (USD-denominated)",None,"announced","By end 2027",True,"OPEN OPPORTUNITY",
 "USD 26M for sterile dosage forms while solid dosage and sterile packaging end by end-2027 (~550 jobs); more automation targeted.",
 fit((SC,"Moderate","Further automation of sterile lines."),(LEG,"Moderate","Transfers and line closures involve legacy system migration.")),
 [src("https://www.novartis.com/ch-de/news/media-releases/novartis-passt-produktionsaktivitaeten-der-schweiz-und-investiert-innovative-herstelltechnologien","Novartis","2025-11-25","High"),src("https://www.moneycab.com/schweiz/novartis-baut-550-stellen-in-stein-ab/amp/","Moneycab","2025-11","Medium")])
site("novartis","Novartis Halle (Saale) radioligand therapy facility","Halle (Saale)","DE-ST",51.4820,11.9700,"GREENFIELD",[M_RAD],"EUR",34700000,"EUR 34.7M",None,"under construction","Completion Q4 2027",True,"OPEN OPPORTUNITY",
 "New radioligand therapy production site in Saxony-Anhalt, completion Q4 2027.",
 fit((SC,"Moderate","Automated radiopharma synthesis/dispensing lines."),(MES,"Moderate","Short-shelf-life batch release needs MES."),(VAL,"Moderate","GMP qualification.")),
 [src("https://www.pharmazeutische-zeitung.de/novartis-investiert-in-neuen-standort-160672/","Pharmazeutische Zeitung","Unverified","Medium")])
site("gsk","GSK Marburg vaccine production","Marburg","DE-HE",50.8100,8.7700,"BROWNFIELD",[M_VAC],"EUR",162000000,"EUR 162M (MenB) + EUR 10M (mumps) + EUR 13M (filling)",None,"operational","Unverified",False,"Monitor",
 "MenB vaccine building (EUR 162M), mumps facility (EUR 10M) and EUR 13M filling/freeze-drying renewal; announcement years not confirmed (likely pre-2024).",
 fit((LIF,"Weak","Mature site.")),
 [src("https://www.aerztezeitung.de/Wirtschaft/GlaxoSmithKline-baut-Marburger-Werk-aus-304215.html","Aerzte Zeitung","Unverified","Low"),src("https://www.apotheke-adhoc.de/nachrichten/detail/markt/gsk-meningokokken-in-marburg/","apotheke adhoc","Unverified","Low")])
site("gsk","GSK Dresden vaccine plant (closing)","Dresden","DE-SN",51.0500,13.7400,"BROWNFIELD",[M_VAC],"EUR",None,"Not applicable (closure by 2028, ~640 jobs)",None,"operational","Closure by 2028",False,"Closed/late",
 "Influenza/hepatitis vaccine plant to close by 2028.",
 [],[src("https://borncity.com/news/grippeimpfstoff-krise-gsk-schliesst-dresdner-werk-bis-2028/","Born City","Unverified","Medium"),src("https://www.apotheke-adhoc.de/nachrichten/detail/markt/gsk-schliesst-impfstoffwerk-in-dresden/print.html","apotheke adhoc","Unverified","Medium")])
site("bbraun","B. Braun Sempach N.I.C.O. disinfectant plant","Sempach","CH-LU",47.1330,8.1960,"BROWNFIELD",[M_OTH],"CHF",70000000,"CHF 70M",None,"under construction","Unverified",False,"OPEN OPPORTUNITY",
 "New factory doubling disinfectant production capacity at B. Braun's disinfection competence centre.",
 fit((SC,"Moderate","Process automation for liquid production."),(MES,"Weak","Batch tracking/serialisation.")),
 [src("https://lucerne-business.com/en/news/b-braun-expands-production-in-sempach-2981","Lucerne Business","Unverified","Medium")],"Date not confirmed.")
site("bbraun","B. Braun Melsungen infusion article production","Melsungen","DE-HE",51.1300,9.5500,"BROWNFIELD",[M_FF,M_DEV],"EUR",150000000,"EUR ~150M",None,"operational","Opened (date unverified)",False,"Monitor",
 "New production facility for infusion articles, opened by the Hessian state premier.",
 fit((LIF,"Weak","Post-start-up support.")),
 [src("https://www.hessenschau.de/wirtschaft/150-millionen-investition-b-braun-eroeffnet-neues-werk-in-melsungen-v1,fertigungsstandort-b-braun-100.html","hessenschau","Unverified","Medium")])
site("bbraun","B. Braun Melsungen dialysis/pump plant expansion","Melsungen","DE-HE",51.1310,9.5510,"BROWNFIELD",[M_DEV],"EUR",60000000,"EUR ~60M",None,"under construction","Unverified",False,"Monitor",
 "Expansion for dialysis machines and infusion pumps.",
 fit((SC,"Weak","Device assembly automation (device scope).")),
 [src("https://www.aerzteblatt.de/news/b-braun-investiert-60-millionen-euro-in-werkserweiterung-d7992e5b-ce9b-4ed0-8c44-45cb8042090e","Aerzteblatt","Unverified","Medium")])
site("bachem","Bachem Bubendorf Building K (peptides/oligonucleotides)","Bubendorf","CH-BL",47.4400,7.7300,"BROWNFIELD",[M_PEP,M_OLI],"CHF",None,"Part of CHF 350-400M annual capex (CHF 148.4M in H1 2026)",None,"commissioning","Commercial ramp-up 2026",True,"OPEN OPPORTUNITY",
 "Large-scale peptide/oligonucleotide plant at HQ; ramp-up through 2026 with start-up costs hitting H1 margin.",
 fit((MES,"Strong","Ramp of a new large-scale plant needs batch/eBR and data integration."),(VAL,"Strong","Commissioning, CSV and data integrity during ramp."),(SC,"Moderate","Upgrades of process control during ramp-up.")),
 [src("https://www.cash.ch/news/top-news/bachem-steigert-umsatz-und-gewinn-umsatzmilliarde-2026-wird-nicht-erwahnt-917794","cash.ch","2026","Medium"),src("https://www.boerse-express.com/news/articles/bachem-aktie-milliardenmarkt-peptid-fertigung-882685","boerse-express","2026","Medium")])
site("bachem","Bachem Sisslerfeld greenfield peptide plant","Sisslerfeld (Eiken)","CH-AG",47.5390,7.9840,"GREENFIELD",[M_PEP],"CHF",500000000,"CHF 500M+",None,"announced","Production from 2030",False,"OPEN OPPORTUNITY",
 "Greenfield peptide manufacturing site; production planned from 2030; 22 Jul 2026 coverage reports a large-scale plant plan.",
 fit((SC,"Strong","Design-stage selection of automation in 2026-28."),(MES,"Strong","Greenfield MES architecture."),(DIG,"Moderate","Data/OT backbone."),(VAL,"Moderate","Qualification 2029-30.")),
 [src("https://chemanager-online.com/de/news/bachem-plant-den-bau-einer-grossmengen-produktionsanlage","CHEManager","2026-07-22","Medium"),src("https://www.s-ge.com/invest/de/artikel/news/bachem-investiert-neue-grossanlage-im-sisslerfeld","S-GE","Unverified","Medium")])
site("biontech","BioNTech Marburg manufacturing (closing)","Marburg","DE-HE",50.8000,8.7500,"BROWNFIELD",[M_VAC],"EUR",None,"Not applicable (closure early 2028)",None,"operational","Closure early 2028",False,"Closed/late",
 "Closing in a staggered programme after no buyer was found.",
 [],[src("https://www.pharmamanufacturing.com/facilities/article/55408341/biontech-to-shutter-three-german-manufacturing-sites-after-failing-to-secure-buyers","PharmaManufacturing","2026-05","Medium"),src("https://ms-aktuell.de/welt/biontech-werke-schliessung-28-09-2026/","MS aktuell","2026-09-28","Medium")])
site("biontech","BioNTech Idar-Oberstein manufacturing (closing)","Idar-Oberstein","DE-RP",49.7140,7.3090,"BROWNFIELD",[M_VAC],"EUR",None,"Not applicable (closure end 2028)",None,"operational","Closure end 2028",False,"Closed/late",
 "Closing end-2028; Tuebingen (ex-CureVac) closes end-2027.",
 [],[src("https://chemanager-online.com/de/news/igbce-kritisiert-stellenabbau-bei-biontech","CHEManager","2026-05-07","Medium")])
site("msd","MSD Lucerne HQ and Schachen R&D","Lucerne","CH-LU",47.0410,8.3100,"BROWNFIELD",[M_OTH],"CHF",60000000,"CHF 60M (HQ); >CHF 230M over 20 years (R&D)",750,"operational","Opened 22 May (year unverified)",False,"Monitor",
 "'One Roof' headquarters for 750 staff and the Schachen R&D/biotech centre; not manufacturing.",
 [],[src("https://www.s-ge.com/invest/en/articles/news/msd-opens-new-swiss-headquarters","S-GE","Unverified","Medium"),src("https://www.lucerne-business.com/en/news/msd-looks-back-on-50-years-of-its-schachen-site-18418","Lucerne Business","Unverified","Medium")])
site("sanofi","Sanofi Frankfurt-Hoechst insulin plant","Frankfurt (Hoechst)","DE-HE",50.0970,8.5420,"BROWNFIELD",[M_BIO,M_FF],"EUR",1300000000,"EUR ~1.3B (EU state aid ~EUR 400M approved Sept 2026)",None,"announced","Completion ~2029",True,"OPEN OPPORTUNITY",
 "New 36,000 m2 human-insulin production plant at the Industriepark Hoechst BioCampus; only human-insulin plant in the EEA; at least 1.1 t/yr by 2042; several hundred jobs.",
 fit((SC,"Strong","Greenfield-type process automation for a biologic drug substance/product plant."),(MES,"Strong","Highly regulated; MES/eBR from day one."),(DIG,"Strong","'Highest automation standards' stated."),(VAL,"Moderate","Qualification phase before 2029.")),
 [src("https://www.frankfurt-main.ihk.de/presse/pressemeldungen2026/gruenes-licht-fuer-neue-sanofi-insulinproduktion-7168032","IHK Frankfurt","2026-09","High"),src("https://www.hessenschau.de/wirtschaft/insulin-aus-frankfurt-eu-genehmigt-400-millionen-euro-fuer-sanofi-v1,sanofi-insulin-frankfurt-102.html","hessenschau","2026-09","Medium"),src("https://www.fiercepharma.com/manufacturing/sanofi-ends-speculation-confirms-it-will-spend-eu13b-build-new-insulin-plant-germany","Fierce Pharma","Unverified","Medium")],"One source states completion by end-2032; most say ~2029.")
site("vetter","Vetter Saarlouis commercial fill-finish site","Saarlouis","DE-SL",49.3140,6.7510,"GREENFIELD",[M_FF,M_DEV],"EUR",480000000,"EUR ~480-500M (first phase)",1500,"under construction","Operational 2031",True,"OPEN OPPORTUNITY",
 "New site on the former Ford plant: 50,000 m2 production building with three aseptic cleanrooms (two PFS, one vial) initially; spade turned 13 May 2026; EUR 47M EU state aid approved Dec 2025.",
 fit((SC,"Strong","Greenfield aseptic fill-finish: building automation, utilities and line control."),(MES,"Strong","Customer-facing commercial supply needs MES/eBR."),(VAL,"Strong","Full qualification program."),(DIG,"Moderate","Smart-factory design.")),
 [src("https://www.vetter-pharma.com/media/content/Downloads/Presse/2026/260513_Vetter_startet_Bau_des_neuen_Produktionsstandorts_in_Saarlouis.pdf","Vetter","2026-05-13","High"),src("https://www.bionity.com/de/news/1188700/vetter-investiert-knapp-500-millionen-euro-in-neuen-produktionsstandort.html","Bionity","2026","Medium"),src("https://www.onvista.de/news/2026/05-13-pharmafirma-vetter-beginnt-bau-von-werk-in-saarlouis-0-10-26511786","onvista","2026-05-13","Medium")])
site("vetter","Vetter Ravensburg / Langenargen capacity expansion","Ravensburg","DE-BW",47.7820,9.6120,"BROWNFIELD",[M_FF,M_DEV],"EUR",None,"Part of ~EUR 1.5B ongoing programme",None,"under construction","Unverified",True,"OPEN OPPORTUNITY",
 "Ongoing capacity expansions at Vetter's home sites alongside Saarlouis; 2024 press release mentions Germany and US capacity growth.",
 fit((SC,"Moderate","Line and utility expansions."),(MES,"Moderate","Integration into existing MES."),(LIF,"Moderate","Ongoing support.")),
 [src("https://www.vetter-pharma.com/media/content/Downloads/Presse/2024/240606_Pressemitteilung_Vetter_baut_Kapazit%C3%A4ten_in_Deutschland_und_den_USA_aus.pdf","Vetter","2024-06-06","High"),src("https://www.dcatvci.org/supplier-news/vetter-outlines-major-expansion-plan-for-commercial-clinical-fill-finish/","DCAT","2024","Medium")])
site("fresenius","Fresenius Kabi Graz biosimilar/sterile expansion","Graz","AT-ST",47.0707,15.4395,"BROWNFIELD",[M_FF,M_BIO],"EUR",28000000,"EUR ~28M to 2026 (+ >EUR 60M prior)",None,"under construction","Through 2026",True,"Monitor",
 "Strategic expansion at Graz/Werndorf for biopharma drug substances and 160M+ filled units a year.",
 fit((LIF,"Weak","Incremental site investments.")),
 [src("https://investinaustria.at/en/news-events-press/fresenius-kabi-invests-eur-28-million-in-its-facility-in-graz","Invest in Austria","2023-09","Medium"),src("https://fresenius-kabi.com/en-at/news/fresenius-kabi-continues-to-expand-its-operations-in-graz","Fresenius Kabi","Unverified","High")])
site("cordenpharma","CordenPharma Muttenz greenfield peptide plant","Muttenz","CH-BL",47.5230,7.6430,"GREENFIELD",[M_PEP],"EUR",500000000,"EUR ~500M (CHF-region project)",300,"under construction","Commercial operation H1 2028",True,"OPEN OPPORTUNITY",
 "New peptide plant at Getec Park near Basel with small-, medium- and large-scale lines (GLP-1 and non-GLP-1); construction/qualification 2025-2027; part of a EUR 1B peptide programme.",
 fit((SC,"Strong","Construction and qualification across 2025-27."),(MES,"Strong","Multi-line peptide production."),(VAL,"Strong","Qualification before 2028 start."),(DIG,"Moderate","Site digital backbone.")),
 [src("https://www.fiercepharma.com/manufacturing/cordenpharma-build-eu500m-swiss-peptide-plant-generate-300-new-jobs","Fierce Pharma","2024","Medium"),src("https://www.pharmamanufacturing.com/all-articles/article/55284445/cordenpharma-to-boost-peptide-production-capacity-with-1-billion-investment","PharmaManufacturing","2024","Medium")],"Announced in EUR.")
site("ucb","UCB Bulle biologics production unit","Bulle","CH-FR",46.6190,7.0570,"BROWNFIELD",[M_BIO],"CHF",100000000,"CHF 100M+ (+ CHF 15M QC lab, CHF 10M cold unit)",80,"announced","Operational ~2029; full 2030",False,"OPEN OPPORTUNITY",
 "New production unit for a key biologics compound relocated from Belgium; QC lab (CHF 15M) expected mid-2026.",
 fit((SC,"Moderate","New unit control in 2027-28."),(VAL,"Moderate","Qualification and tech transfer."),(MES,"Weak","Integration into Bulle MES.")),
 [src("https://ggba.swiss/en/ucb-invests-over-chf-100-million-to-expand-its-biopharmaceutical-site-in-bulle/","GGBA","2025","Medium"),src("https://bioalps.org/ucb-farchim-invests-over-chf-100-million-and-creates-80-new-jobs-in-bulle/","BioAlps","2025","Medium")])
site("sartorius","Sartorius Freiburg cell and gene therapy competence centre","Freiburg","DE-BW",47.9990,7.8420,"BROWNFIELD",[M_CGT],"EUR",140000000,"EUR 140M+",None,"operational","Opened 2026",True,"Monitor",
 "Development and production of quality-critical materials for cell and gene therapy; opened.",
 fit((LIF,"Weak","Post-opening support.")),
 [src("https://www.boerse-online.de/dpa-afx/eqs-news-sartorius-eroeffnet-neues-kompetenzzentrum-fuer-zell-und-gentherapie-komponenten-in-freiburg-deutsch-526541.html","EQS/boerse-online","2026","Medium")])
site("sartorius","Sartorius Goettingen membrane building","Goettingen","DE-NI",51.5360,9.9260,"BROWNFIELD",[M_OTH],"EUR",25000000,"EUR ~25M",None,"operational","Inaugurated (date unverified)",False,"Monitor",
 "6,000 m2 building for polyethersulfone membrane production, labs and offices for 120+ staff.",
 fit((LIF,"Weak","Support of new lines.")),
 [src("https://www.industrial-production.de/wirtschaft---unternehmen/sartorius-weiht-neues-membrangebaeude-ein-490157.htm","industrial-production.de","Unverified","Medium")])
site("rentschler","Rentschler Laupheim buffer media station","Laupheim","DE-BW",48.2250,9.8780,"BROWNFIELD",[M_BIO],"EUR",None,"'High double-digit million' EUR",None,"under construction","Operational 2028",True,"OPEN OPPORTUNITY",
 "Four-storey, 34,000 m2 (per source) buffer/media preparation building; construction from spring 2025; operational 2028; company's largest single investment in Germany.",
 fit((SC,"Strong","Buffer prep automation and utilities."),(MES,"Moderate","Integration with upstream/downstream MES."),(VAL,"Moderate","Qualification before 2028.")),
 [src("https://drug-dev.com/rentschler-biopharma-announces-largest-single-investment-at-its-headquarters-in-germany/","Drug Development","2024-10","Medium"),src("https://www.stuttgarter-zeitung.de/wirtschaft/biopharmahersteller-rentschler-steht-vor-groesster-investition-im-inland-79024511.html","Stuttgarter Zeitung","2024","Medium")],"The 34,000 m2 figure in the source seems large for a buffer building: treat as unverified.")
site("lilly","Lilly Alzey injectable and device plant","Alzey","DE-RP",49.7480,8.1130,"GREENFIELD",[M_FF,M_PEP,M_DEV],"EUR",1150000000,"EUR ~1.15B implied (original ~EUR 2.3B cut by about half in 2026)",500,"under construction","Plant start end-2027",True,"OPEN OPPORTUNITY",
 "Greenfield Mounjaro/injectable plant 30 km south of Mainz. Original EUR 2.3B / 1,000 jobs; 2026 coverage says the remaining investment was halved and jobs reduced to ~500; construction has begun and start-up remains end-2027.",
 fit((SC,"Strong","Greenfield plant approaching 2027 start-up."),(MES,"Strong","Lilly global MES standard likely; local integration."),(VAL,"Moderate","Qualification in 2027."),(DIG,"Moderate","Site OT/IT backbone.")),
 [src("https://www.boerse-online.de/dpa-afx/roundup-pharmariese-eli-lilly-baut-werk-in-alzey-boomgeschaeft-abnehmspritze-330367.html","dpa-AFX","Unverified","Medium"),src("https://goldesel.de/aktien/news/eli-lilly-mit-q2-boost-und-alzey-schnitt-umsatzziel-8587-mrd-werkstart-bleibt-2027","goldesel.de","2026-08","Low"),src("https://www.boerse-express.com/news/articles/eli-lilly-kuerzt-deutschland-investition-axsome-loest-patentstreit-biotech-im-umbruch-914097","boerse-express","2026","Low")],"EUR 1.15B is an inference (half of EUR 2.3B); confirm with Lilly.")
site("plbio","PL BioScience Aachen headquarters expansion","Aachen","DE-NW",50.7750,6.0840,"BROWNFIELD",[M_CGT,M_OTH],"EUR",None,"Amount not disclosed",None,"announced","Unverified",False,"Monitor",
 "Expanding HQ to >1,200 m2 with GMP production for up to 20,000 L/yr of human platelet lysate; second GMP facility.",
 fit((MES,"Weak","Small GMP production."),(VAL,"Weak","GMP validation.")),
 [src("https://www.bionity.com/de/news/1186842/pl-bioscience-erweitert-deutschen-standort-am-firmensitz-in-aachen.html","Bionity","Unverified","Medium"),src("https://pharmamanufacturing.com/industry-news/news/55307197/pl-bioscience-to-expand-headquarters-and-double-gmp-grade-hpl-output","PharmaManufacturing","Unverified","Medium")])
site("beiersdorf","Beiersdorf Hamburg Innovation Centre","Hamburg","DE-HH",53.5900,9.9650,"BROWNFIELD",[M_OTH],"EUR",139000000,"EUR 139M",None,"under construction","Completion 2028",False,"Monitor",
 "R&D innovation centre (~14,000 m2) at HQ; foundation stone June 2025.",
 [],[src("https://www.beiersdorf.com/newsroom/press-information/all-press-releases/2025/06/20-beiersdorf-lays-foundation-stone-for-its-innovation-center-in-hamburg","Beiersdorf","2025-06-20","High")])
site("biospring","BioSpring Offenbach large-scale nucleic acid API site","Offenbach","DE-HE",50.1060,8.7600,"GREENFIELD",[M_OLI],"EUR",None,"'Several hundred million euros' (not stated)",200,"under construction","Construction to end 2027",True,"OPEN OPPORTUNITY",
 "Large-scale oligonucleotide/nucleic-acid API plant on an innovation campus in Offenbach, tonne-scale, ~200 jobs; construction to end of 2027.",
 fit((SC,"Strong","New GMP plant in construction through 2027."),(MES,"Strong","Greenfield MES."),(VAL,"Strong","Qualification 2027-28.")),
 [src("https://www.pharmamanufacturing.com/industry-news/news/55301809/biospring-to-build-large-scale-nucleic-acid-api-site-in-germany","PharmaManufacturing","Unverified","Medium"),src("https://www.bionity.com/de/news/1174484/biospring-errichtet-hightech-wirkstoffproduktion-auf-innovationscampus.html","Bionity","Unverified","Medium")])
site("biospring","BioSpring Frankfurt-Fechenheim gRNA/mRNA expansion","Frankfurt (Fechenheim)","DE-HE",50.1230,8.7500,"BROWNFIELD",[M_OLI,M_VAC],"EUR",None,"Double-digit EUR millions",None,"operational","2024",False,"Monitor",
 "New cGMP capacity for guide RNA and mRNA.",
 fit((LIF,"Weak","Support of new capacity.")),
 [src("https://chemanager-online.com/de/news/biospring-erweitert-cgmp-produktionskapazitaeten-fuer-guide-rna-und-mrna","CHEManager","2024-11-06","Medium")])
site("ypsomed","Ypsomed Schwerin pen and autoinjector expansion","Schwerin","DE-MV",53.6355,11.4010,"BROWNFIELD",[M_DEV],"EUR",500000000,"EUR ~500M in two phases to end of decade",1000,"under construction","Phases to ~2030",True,"OPEN OPPORTUNITY",
 "Fully automated high-bay warehouse done; two construction phases take capacity to 400-500M pens/year and staff above 1,000.",
 fit((SC,"Strong","Fully automated assembly and warehouse."),(MES,"Strong","High-volume device traceability."),(DIG,"Moderate","Smart-factory data.")),
 [src("https://www.apotheke-adhoc.de/nachrichten/detail/markt/infusionssets-ypsomed-investiert-weiter-in-schwerin/print.html","apotheke adhoc","Unverified","Medium"),src("https://www.moneycab.com/?p=1652931","Moneycab","Unverified","Low")])
site("ypsomed","Ypsomed Solothurn / Burgdorf production and tool shop","Solothurn","CH-SO",47.2088,7.5323,"BROWNFIELD",[M_DEV],"CHF",200000000,"CHF ~200M (Solothurn) + CHF 21M (Burgdorf)",None,"under construction","Unverified",True,"OPEN OPPORTUNITY",
 "New production levels, tool shop and high-bay warehouse in Solothurn; lab/tool/offices in Burgdorf.",
 fit((SC,"Moderate","Production-level automation."),(MES,"Moderate","Line traceability.")),
 [src("https://kildare.luzernerzeitung.ch/solothurn/kanton-solothurn/ypsomed-meldet-rekordzahlen-in-solothurn-wird-weiter-investiert-ld.4171900","Solothurner Zeitung","Unverified","Medium"),src("https://www.ypsomed.com/en/news-insights/news/press-releases/news-reader-detail-page/ypsomed-opens-new-tool-manufacturing-facility-in-solothurn","Ypsomed","Unverified","High")])
site("biogen","Biogen Luterbach biologics plant","Luterbach","CH-SO",47.2000,7.5700,"GREENFIELD",[M_BIO],"CHF",1500000000,"CHF ~1.5B",500,"operational","Operational since 2021",False,"Monitor",
 "Large-scale biologics plant (about 500 staff), triples Biogen's biologics capacity; no 2026 project located.",
 fit((LIF,"Moderate","Mature site; lifecycle support.")),
 [src("https://www.greaterzuricharea.com/en/news/biogen-driving-solothurn-economy","Greater Zurich Area","Unverified","Medium")])
site("richter","Richter Pharma VetViva Wels facility","Wels","AT-OO",48.1570,14.0210,"BROWNFIELD",[M_FF],"EUR",35000000,"EUR 35M+",120,"operational","Opened 2025",False,"Closed/late",
 "Veterinary pharma production opened in 2025; ~10M vials/yr.",
 [],[src("https://www.tips.at/nachrichten/wels/wirtschaft-politik/697519-35-millionen-euro-investiert-richter-pharma-startet-hochmoderne-produktionsanlage","Tips.at","2025","Medium")])
site("wackerbiotech","Wacker Halle mRNA competence centre","Halle (Saale)","DE-ST",51.4900,11.9700,"BROWNFIELD",[M_VAC,M_OLI],"EUR",None,"Amount not found",200,"operational","Unverified",False,"Monitor",
 "Four-storey mRNA active-ingredient building with four production lines; groundbreaking 2022.",
 fit((LIF,"Weak","Mature after start-up.")),
 [src("https://www.chemie.de/news/73945/wacker-erweitert-produktion-fuer-biopharmazeutika-am-standort-jena.html","Chemie.de","Unverified","Low"),src("https://www.wacker.com/cms/media/de/documents/pressrelease-pdf/pm2022/32_spatenstich_mrna_kompetenzzentrum_halle_de.pdf","Wacker","2022","High")])
site("rotop","Rotop radiopharmaceutical factories Dresden-Rossendorf","Dresden","DE-SN",51.0600,13.9500,"BROWNFIELD",[M_RAD],"EUR",None,"Double-digit EUR millions (~2x annual revenue)",None,"under construction","Gradual start from 2028",True,"OPEN OPPORTUNITY",
 "Two highly automated factories for diagnostic and therapeutic radiopharmaceuticals; groundbreaking by Dresden's mayor; Germany's largest radiopharma project under way.",
 fit((SC,"Strong","Highly automated GMP synthesis and dispensing."),(MES,"Moderate","Short-shelf-life release."),(VAL,"Moderate","Qualification before 2028.")),
 [src("https://www.aerzteblatt.de/news/rotop-weitet-produktion-von-radiopharmaka-aus-db218f5a-e0de-4164-854f-c039a3592ac5","Aerzteblatt","Unverified","Medium"),src("https://medienservice.sachsen.de/medien/news/1061401/download_pdf","Sachsen Medienservice","Unverified","High")])
site("merz","Merz Dessau-Rosslau expansion and packaging line","Dessau-Rosslau","DE-ST",51.8300,12.2400,"BROWNFIELD",[M_FF,M_DEV],"EUR",100000000,"EUR 100M+ by 2028",25,"under construction","Through 2028; packaging line opened June 2026",True,"OPEN OPPORTUNITY",
 "New packaging centre opened June 2026; >EUR 100M to Dessau by 2028; Reinheim production consolidates into Dessau.",
 fit((MES,"Moderate","Packaging/serialization integration."),(SC,"Moderate","New lines in 2026-28."),(LEG,"Moderate","Reinheim transfer.")),
 [src("https://www.invest-in-saxony-anhalt.com/press-dates/detail/merz-eroeffnet-neues-verpackungszentrum-in-dessau-und-staerkt-produktionsstandort","Invest in Saxony-Anhalt","2026-06","High"),src("https://www.volksstimme.de/sachsen-anhalt/tetesept-und-merz-spezial-dragees-produktion-nur-noch-in-dessau-pharmakonzern-merz-schliesst-werk-in-hessen-3851942","Volksstimme","Unverified","Medium")])
site("ferring","Ferring Kiel production building","Kiel","DE-SH",54.3230,10.1360,"GREENFIELD",[M_FF,M_BIO],"EUR",40000000,"EUR ~40M (undated)",None,"operational","Unverified",False,"Monitor",
 "15,000 m2 production building; date not confirmed.",
 [],[src("https://www.apotheke-adhoc.de/nachrichten/detail/markt/ferring-investiert-40-millionen-euro-in-kiel-neuer-produktionsstandort/","apotheke adhoc","Unverified","Low")])
site("siegfried","Siegfried Hameln fill-finish expansion (PFS/cartridges)","Hameln","DE-NI",52.1040,9.3560,"BROWNFIELD",[M_FF,M_DEV],"EUR",None,"Amount not found",None,"under construction","First line revenue 2026; second 2027",True,"OPEN OPPORTUNITY",
 "Two new manufacturing lines for prefilled syringes and cartridges.",
 fit((SC,"Strong","New fill lines in start-up window."),(MES,"Moderate","Line integration."),(VAL,"Strong","Line qualification.")),
 [src("https://siegfried.ch/?p=1567","Siegfried","Unverified","Medium"),src("https://www.finanzen.at/nachrichten/aktien/siegfried-on-track-to-deliver-profitable-growth-1035059761","finanzen.at","Unverified","Low")])
site("siegfried","Siegfried Minden multi-purpose drug-substance plant","Minden","DE-NW",52.2890,8.9160,"BROWNFIELD",[M_SM],"EUR",None,"Amount not found",None,"commissioning","First revenue H2 2025",False,"Monitor",
 "New large-scale multi-purpose DS plant, nearing completion per source.",
 fit((LIF,"Moderate","Post-commissioning support.")),
 [src("https://www.finanzen.at/nachrichten/aktien/siegfried-on-track-to-deliver-profitable-growth-1035059761","finanzen.at","Unverified","Low")])
site("siegfried","Siegfried Evionnaz R&D centre for drug substances","Evionnaz","CH-VS",46.1740,7.0260,"BROWNFIELD",[M_SM],"CHF",25000000,"CHF up to 25M",100,"operational","Unverified",False,"Monitor",
 "Global R&D centre for drug substances, 100+ specialists.",
 [],[src("https://www.siegfried.ch/siegfried-begins-construction-of-a-new-global-rd-center-for-drug-substances-in-evionnaz/","Siegfried","2023-04-25","High")])
site("abbvie","AbbVie Ludwigshafen LUnA R&D building","Ludwigshafen","DE-RP",49.4770,8.4450,"BROWNFIELD",[M_OTH],"EUR",150000000,"EUR ~150M",None,"under construction","In operation 2027",True,"Monitor",
 "Six-floor lab building housing ~1/3 of 1,000+ researchers (oncology, neurology, immunology).",
 fit((DIG,"Weak","Lab data/OT only.")),
 [src("https://www.aerzteblatt.de/news/pharmakonzern-abbvie-investiert-in-ludwigshafen-eef9596c-f19f-42a5-8480-3b034726ab57","Aerzteblatt","Unverified","Medium"),src("https://www.dcatvci.org/top-industry-news/abbvie-to-build-160-m-rd-facility-in-germany/","DCAT","Unverified","Medium")])
site("csl","CSL Behring Bern Protinus immunoglobulin plant","Bern","CH-BE",46.9480,7.4470,"BROWNFIELD",[M_PLA],"CHF",300000000,"CHF 300M",None,"commissioning","Process qualification of Module V (year unverified)",False,"Monitor",
 "Immunoglobulin production facility (Project Protinus), staged modules at Bern/Wankdorf.",
 fit((VAL,"Moderate","Module qualification."),(LIF,"Weak","Ongoing support.")),
 [src("https://www.dcatvci.org/?p=3470","DCAT","Unverified","Low")],"Dates not verified.")
site("csl","CSL Behring Marburg filling and freeze-drying","Marburg","DE-HE",50.8100,8.7800,"BROWNFIELD",[M_PLA,M_FF],"EUR",31000000,"EUR 31M (+ EUR 20M hemophilia B)",None,"operational","Unverified",False,"Monitor",
 "Filling/freeze-drying facility raising capacity by 50-60%.",
 [],[src("https://www.aerztezeitung.de/Wirtschaft/CSL-Behring-staerkt-Standort-Marburg-mit-neuer-Anlage-341367.html","Aerzte Zeitung","Unverified","Low")],"Dates not verified.")
site("pfizer","Pfizer Freiburg high-containment plant","Freiburg","DE-BW",47.9990,7.8420,"BROWNFIELD",[M_OSD],"EUR",300000000,"EUR ~300M",None,"operational","Opened 2022",False,"Closed/late",
 "High-containment solids plant opened 2022; CEO said in June 2026 German investments under review.",
 [],[src("https://www.bionity.com/de/news/1176277/300-millionen-euro-investition-pfizer-eroeffnet-high-containment-werk-in-freiburg.html","Bionity","2022","Medium"),src("https://www.t-online.de/nachrichten/deutschland/innenpolitik/id_101291258/pfizer-chef-sagt-merz-ab-und-stellt-investitionen-in-frage.html","t-online","2026-06","Medium")])
site("jnj","J&J Schaffhausen biotherapeutics production","Schaffhausen","CH-SH",47.6960,8.6350,"BROWNFIELD",[M_BIO,M_SM],"CHF",None,">CHF 1B over 25 years (not new)",2200,"operational","Ongoing",False,"Monitor",
 "J&J says Schaffhausen is being developed further to expand capacity; no specific new project amount located.",
 [],[src("https://www.jnj.com/CH/latest-news/90-jahre-innovation-in-schaffhausen-von-cilag-zu-johnson-johnson","J&J Switzerland","2026","Medium"),src("https://www.s-ge.com/en/article/news/johnson-johnson-erweitert-schaffhauser-biotech-anlage","S-GE","Unverified","Medium")])
site("kbi","KBI Biopharma Geneva integrated facility","Plan-les-Ouates (Geneva)","CH-GE",46.1650,6.1170,"GREENFIELD",[M_BIO],"CHF",None,"Not disclosed",None,"operational","Opened Oct 2022",False,"Closed/late",
 "Integrated mammalian CDMO site with Selexis; first FIH batch March 2023; no new investment found.",
 [],[src("https://www.businesswire.com/news/home/20230321005069/en/KBI-Biopharma-Inc.-Releases-Inaugural-FIH-Manufacturing-Batch-at-Integrated-Switzerland-Facility-Five-Months-After-Opening","Business Wire","2023-03-21","High")])

# ids
import re
def slug(t): return re.sub(r'[^a-z0-9]+','-',t.lower()).strip('-')
for s in S:
    s["id"] = slug(s["account"]+"-"+s["site_name"])[:90]

REGIONS = {
 # DE
 "DE-SH":"Schleswig-Holstein","DE-HH":"Hamburg","DE-MV":"Mecklenburg-Vorpommern","DE-BB":"Brandenburg","DE-BE":"Berlin","DE-ST":"Sachsen-Anhalt","DE-SN":"Sachsen","DE-TH":"Thueringen","DE-NI":"Niedersachsen",
 "DE-HB":"Bremen","DE-NW":"Nordrhein-Westfalen","DE-HE":"Hessen","DE-RP":"Rheinland-Pfalz","DE-SL":"Saarland","DE-BW":"Baden-Wuerttemberg","DE-BY":"Bayern",
 # AT
 "AT-V":"Vorarlberg","AT-T":"Tirol","AT-S":"Salzburg","AT-OO":"Oberoesterreich","AT-NO":"Niederoesterreich","AT-W":"Wien","AT-B":"Burgenland","AT-ST":"Steiermark","AT-K":"Kaernten",
 # CH
 "CH-GE":"Genf","CH-VD":"Waadt","CH-VS":"Wallis","CH-FR":"Freiburg","CH-NE":"Neuenburg","CH-JU":"Jura","CH-BE":"Bern","CH-SO":"Solothurn","CH-BL":"Basel-Landschaft",
 "CH-BS":"Basel-Stadt","CH-AG":"Aargau","CH-LU":"Luzern","CH-ZG":"Zug","CH-ZH":"Zuerich","CH-SZ":"Schwyz","CH-NW":"Nidwalden","CH-OW":"Obwalden","CH-UR":"Uri",
 "CH-TG":"Thurgau","CH-SH":"Schaffhausen","CH-SG":"St. Gallen","CH-AR":"Appenzell AR","CH-AI":"Appenzell IR","CH-GL":"Glarus","CH-GR":"Graubuenden","CH-TI":"Tessin",
}
# grid [col,row] (0-based); rows: 0 DE label,1-2 DE,3 AT label,4 AT,5 CH label,6-8 CH
GRID = {}
for i,c in enumerate(["DE-SH","DE-HH","DE-MV","DE-BB","DE-BE","DE-ST","DE-SN","DE-TH","DE-NI"]): GRID[c]=[i,1]
for i,c in enumerate(["DE-HB","DE-NW","DE-HE","DE-RP","DE-SL","DE-BW","DE-BY"]): GRID[c]=[i,2]
for i,c in enumerate(["AT-V","AT-T","AT-S","AT-OO","AT-NO","AT-W","AT-B","AT-ST","AT-K"]): GRID[c]=[i,4]
for i,c in enumerate(["CH-GE","CH-VD","CH-VS","CH-FR","CH-NE","CH-JU","CH-BE","CH-SO","CH-BL"]): GRID[c]=[i,6]
for i,c in enumerate(["CH-BS","CH-AG","CH-LU","CH-ZG","CH-ZH","CH-SZ","CH-NW","CH-OW","CH-UR"]): GRID[c]=[i,7]
for i,c in enumerate(["CH-TG","CH-SH","CH-SG","CH-AR","CH-AI","CH-GL","CH-GR","CH-TI"]): GRID[c]=[i,8]
assert set(GRID)==set(REGIONS) and len(GRID)==51, (len(GRID), set(REGIONS)^set(GRID))
