#!/usr/bin/env python3
"""Italy dataset (first research batch: Novartis, Sanofi, GSK, Eli Lilly, Menarini, Chiesi).

Writes data/it.json (same schema as data/dach.json, consumed by build.py),
italy/projects.csv and italy/sources.md.

Rules followed: no invented figures; every amount/date traces to a listed source;
estimates are flagged and given Low confidence; "Not found in public sources" where unknown.
NOTE: figures below come from search-result summaries of the cited pages. The pages themselves
could not be opened (egress policy blocked the hosts), so they still need a manual spot-check.
"""
import json, csv, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
NF = "Not found in public sources"
AS_OF = "October 14, 2026"
EUR_PER_USD = 0.86

def src(url, publisher, date, conf): return {"url": url, "publisher": publisher, "date": date, "confidence": conf}

ACCOUNTS = [
 dict(id="novartis", name="Novartis", priority_tier="Tier 1",
  footprint_summary="Italian manufacturing at Torre Annunziata (Naples; FDA-certified since 2021, >100M packs/yr) and Ivrea; HQ in Origgio (Varese). The €350M 2023-2025 Italy plan started with Torre Annunziata and Ivrea.",
  investment_strategy_summary="Capacity and innovation space at Torre Annunziata: a €32M expansion approved by the Campania ZES commissioner (reported March 2026), after a >€30M line opened in Feb 2024.",
  priority_reason="Dated, approved brownfield expansion in the window with a 'new technologies' / life-science innovation scope. Amount is small and no digital scope is stated, so held as an entry-level Tier 1 lead; Ivrea not yet researched.",
  incumbent_vendors_general="", ownership_note=""),
 dict(id="sanofi", name="Sanofi", priority_tier="Tier 1",
  footprint_summary="Anagni (biotech, vaccines, enzyme replacement; sterile freeze-dried line), Scoppito (L'Aquila; oral solids, ~€50M 2020-22 + €7.3M in 2024) and Origgio.",
  investment_strategy_summary="Anagni: Invitalia development contract of €47.3M (€17.4M grant) for a new sterile freeze-dried line; plus a 2022 MISE innovation agreement (~€27M, €6.3M grant) for prototype freeze-drying systems. No 2026 announcement found.",
  priority_reason="Sterile lyophilisation and biotech at Anagni is a strong GMP-automation profile, but the projects found pre-date the window and no new 2026-27 programme was found. Monitor until a dated project appears.",
  incumbent_vendors_general="", ownership_note=""),
 dict(id="gsk", name="GSK", priority_tier="Tier 1",
  footprint_summary="Verona (respiratory/oral) and San Polo di Torrile, Parma (ViiV HIV, oncology, autoimmune; supplies >100 markets).",
  investment_strategy_summary="A secondary source reports ~€215M across GSK's Italian sites in 2025-2027, mainly technology upgrades, sustainability and plant modernisation. The split by site is not disclosed.",
  priority_reason="A modernisation programme is exactly the Orise trigger, but it is Italy-wide, from a secondary source, with no site split. Needs the GSK press release to qualify.",
  incumbent_vendors_general="", ownership_note=""),
 dict(id="eli-lilly", name="Eli Lilly", priority_tier="Tier 1",
  footprint_summary="Sesto Fiorentino (Florence): biotech/insulin and, per the new lot, diabetes and obesity medicines; Italy hub.",
  investment_strategy_summary="Over €750M announced for a new production lot at Sesto Fiorentino for diabetes/obesity drugs, with a 2025 horizon; the Lilly Italy president said investments would be fully finalised by end-2025 (Il Sole 24 Ore, 2025).",
  priority_reason="Very large, but the build was due to finish by end-2025, so the window is commissioning and lifecycle rather than a new build. No new 2026 investment announced (Sept 2026 coverage is the 150th anniversary).",
  incumbent_vendors_general="", ownership_note=""),
 dict(id="menarini", name="Menarini", priority_tier="Tier 2",
  footprint_summary="Italian plants at Florence (2), Pisa (2), Pomezia, L'Aquila, Lomagna (Lecco) and Casaletto Lodigiano (Lodi). 2025 revenue €4.887B.",
  investment_strategy_summary="March 2026: approved restructuring of the Florence vial area with a new aseptic line, €14-15M (Lucia Aleotti, results press event). Separate, older €150M Sesto Fiorentino plant coverage (date not verified).",
  priority_reason="A new aseptic line is a clear, dated, in-window brownfield project with CSV, SCADA and MES implications. Amount is modest; L'Aquila and Pisa not yet researched.",
  incumbent_vendors_general="", ownership_note=""),
 dict(id="chiesi", name="Chiesi", priority_tier="Tier 2",
  footprint_summary="Parma (HQ, manufacturing, Biotech Center of Excellence) and, from 2025, Nerviano (Milan), the former Carlo Erba/Farmitalia research site.",
  investment_strategy_summary="€430M at Nerviano over 2025-2030 to convert a 124,000 m² site into a production hub for low-carbon-footprint inhalers and sterile biologics, ~300 jobs by 2029; first activity from 2026, full operation 2030. Linked investments planned at Parma and Blois (France).",
  priority_reason="Largest dated, in-window project found: a multi-year conversion into a regulated manufacturing site, so automation, MES and validation decisions fall in 2026-2029. Highest priority of this batch.",
  incumbent_vendors_general="", ownership_note=""),
]

def fit(area, strength, reason): return {"area": area, "strength": strength, "reason": reason}
SC, MES, DIG, CSV_, LEG, LIF = ("SCADA / process control and automation","MES implementation and integration","Digitalization / Industry 4.0",
    "Validation / CSV / data integrity","Legacy system modernization and migration","Lifecycle support and managed services")
BASIS = "Assessed from project scope; no public statement about automation or digital scope was found."

SITES = [
 dict(id="chiesi-nerviano", account="chiesi", site_name="Chiesi Nerviano production hub (former Carlo Erba site)", city="Nerviano (Milan)", state="IT-LOM",
  lat=45.55, lon=8.99, project_type="BROWNFIELD", modality=["inhalers / respiratory", "biologics/mAbs (sterile biologics)"],
  eur=430_000_000, investment_display="€430 million over 2025-2030", jobs=300, status="announced",
  expected_start="2025-2030; first activity from 2026, full operation 2030",
  opportunity_status="OPEN OPPORTUNITY",
  technical_scope="Redevelopment of a 124,000 m² industrial area, the former Farmitalia Carlo Erba oncology research centre (founded 1965, closed 2024), into a manufacturing site focused on low-carbon-footprint inhalers, with sterile biological products. Includes a photovoltaic park; tied to Chiesi's Net Zero 2035 goal. About 300 jobs by 2029.",
  orise_fit=[fit(SC,"Strong","New regulated manufacturing site that must be built out and commissioned over 2026-2029. "+BASIS),
             fit(MES,"Strong","New inhaler and sterile biologics production needs batch execution and release flow. "+BASIS),
             fit(CSV_,"Strong","GMP site start-up with sterile biologics brings Annex 11 / data integrity validation. "+BASIS),
             fit(DIG,"Moderate","Greenfield-like conversion allows a connected-plant design from the start. "+BASIS)],
  incumbent_vendors="", digital_signals=NF,
  sources=[src("https://www.fiercepharma.com/manufacturing/chiesi-lays-out-eu430m-revitalize-italian-production-site-inhaler-biologics","Fierce Pharma","2025-03","Medium"),
           src("https://forbes.it/2025/03/27/chiesi-nuovo-stabilimento-nerviano-investimento-430-milioni/","Forbes Italia","2025-03-27","Medium"),
           src("https://www.saronnonews.it/2025/03/27/il-gruppo-chiesi-investe-a-nerviano-300-posti-di-lavoro-nellex-stabilimento-della-carlo-erba/","SaronnoNews","2025-03-27","Medium"),
           src("https://legnanonews.com/aree-geografiche/alto_milanese/2025/03/27/il-gruppo-chiesi-investe-430-milioni-di-euro-a-nerviano-300-nuovi-posti-di-lavoro-nellex-stabilimento-della-carlo-erba/1306353/","LegnanoNews","2025-03-27","Medium")],
  confidence="High", orise_relevance="High",
  notes="Announced March 2025, before the Jan 2026 window, but activity runs through the window. Classed BROWNFIELD because it converts an existing site; functionally a new manufacturing build, so treat as greenfield-equivalent for Orise. No digital or automation statement found."),
 dict(id="novartis-torre-annunziata", account="novartis", site_name="Novartis Torre Annunziata expansion (life-science innovation space)", city="Torre Annunziata (Naples)", state="IT-CAM",
  lat=40.75, lon=14.45, project_type="BROWNFIELD", modality=["finished dosage / packaging (not specified in sources)"],
  eur=32_000_000, investment_display="€32 million", jobs=None, status="announced",
  expected_start="Not found in public sources (approval reported March 2026)",
  opportunity_status="OPEN OPPORTUNITY",
  technical_scope="Expansion of the Torre Annunziata site with a space for development, innovation and new technologies in life sciences, to raise production capacity. Plan approved by the Campania ZES commissioner, Giuseppe Romano. The site was FDA-certified in 2021 and passed 100M packs/yr.",
  orise_fit=[fit(DIG,"Moderate","'New technologies' innovation space and capacity growth at an FDA-audited site. "+BASIS),
             fit(MES,"Moderate","Capacity growth on existing packaging/production lines. "+BASIS),
             fit(CSV_,"Moderate","FDA-certified site, so changes need validated systems. "+BASIS)],
  incumbent_vendors="", digital_signals=NF,
  sources=[src("https://www.ecoseven.net/flash-news/investimenti-da-32-milioni-di-euro-per-il-sito-di-novartis-a-torre-annunziata/","Ecoseven (Adnkronos)","2026-03 (per search snippet; page not opened)","Medium"),
           src("https://www.affaritaliani.it/economia/notizie-aziende/novartis-32-milioni-per-ampliare-il-sito-di-torre-annunziata-846735.html","Affaritaliani","Unverified","Medium")],
  confidence="Medium",
  orise_relevance="Med", notes="Approval date could not be confirmed on a second search; one source cites a different, larger plan (€80M, 300 hires) which seems to be an older, separate plan and is not recorded. Earlier: >€30M line opened Feb 2024 and €350M Italy plan 2023-2025 (not in window)."),
 dict(id="menarini-florence-aseptic", account="menarini", site_name="Menarini Florence vial area restructuring and new aseptic line", city="Florence", state="IT-TOS",
  lat=43.78, lon=11.23, project_type="BROWNFIELD", modality=["sterile fill-finish (vials)"],
  eur=14_000_000, investment_display="€14-15 million (range stated; lower bound used)", jobs=None, status="announced",
  expected_start="Not found in public sources (approved; stated March 2026)",
  opportunity_status="OPEN OPPORTUNITY",
  technical_scope="Restructuring of the vial department at the Florence plant with a new aseptic line, approved and announced by Lucia Aleotti at the 2025 results press event (March 2026).",
  orise_fit=[fit(CSV_,"Strong","A new aseptic line needs qualification and computerised-system validation (Annex 1 / Annex 11). "+BASIS),
             fit(SC,"Moderate","New line control and integration with the existing plant. "+BASIS),
             fit(MES,"Moderate","Vial area batch records and line integration. "+BASIS)],
  incumbent_vendors="", digital_signals=NF,
  sources=[src("https://tg24.sky.it/salute-e-benessere/2026/03/06/gruppo-menarini","Sky TG24","2026-03-06","Medium"),
           src("https://www.lapresse.it/salute/farmaci/2026/03/07/menarini-sfiora-i-49-mld-di-euro-nel-2025-e-punta-su-talenti-e-ai-mentre-nel-pharma-entrano-player-giganti/","LaPresse","2026-03-07","Medium")],
  confidence="Medium", orise_relevance="High",
  notes="The €14-15M figure comes from a search summary of a Fortune Italia piece whose URL implies 2023; the Sky/LaPresse March 2026 pieces cover the same results event. Verify the exact quote."),
 dict(id="lilly-sesto", account="eli-lilly", site_name="Lilly Sesto Fiorentino new production lot (diabetes and obesity)", city="Sesto Fiorentino (Florence)", state="IT-TOS",
  lat=43.83, lon=11.2, project_type="BROWNFIELD", modality=["biologics (insulin / diabetes and obesity drugs)"],
  eur=750_000_000, investment_display="Over €750 million, horizon 2025", jobs=None, status="under construction",
  expected_start="Horizon 2025; 'fully finalised by end of 2025' per Il Sole 24 Ore (2025). Current status not found",
  opportunity_status="Monitor",
  technical_scope="New lot at the Sesto Fiorentino plant (operating since 1959-62) to expand production of drugs for diabetes and obesity. Estimated contribution of €1.5B to Italian GDP and >6,000 jobs in the supply chain (Forbes Italia, Nov 2024).",
  orise_fit=[fit(LIF,"Moderate","Commissioning and ramp-up of a large new lot, then long-term support. "+BASIS),
             fit(CSV_,"Moderate","Ramp-up and validation of new biologics lines. "+BASIS),
             fit(DIG,"Weak","Scale of the new lot suggests data and OT integration needs. "+BASIS)],
  incumbent_vendors="", digital_signals=NF,
  sources=[src("https://www.fortuneita.com/?p=320008","Fortune Italia","Unverified","Medium"),
           src("https://forbes.it/2024/11/27/entro-il-2025-lilly-contribuira-al-pil-italiano-con-15-miliardi-di-euro-e-generera-oltre-6mila-posti-di-lavoro/","Forbes Italia","2024-11-27","Medium"),
           src("https://qds.it/eli-lilly-un-nuovo-patto-con-litalia-da-750-milioni-entro-il-2025/","QdS","Unverified","Low")],
  confidence="Medium", orise_relevance="Med",
  notes="Sources disagree on whether the plan was announced in 2023 or 2024. Not found: whether the lot is complete, and any 2026 follow-on investment (Sept 2026 coverage is the 150th anniversary)."),
 dict(id="sanofi-anagni", account="sanofi", site_name="Sanofi Anagni sterile freeze-dried line and lyophilisation prototype systems", city="Anagni (Frosinone)", state="IT-LAZ",
  lat=41.74, lon=13.15, project_type="BROWNFIELD", modality=["sterile fill-finish (freeze-dried)", "biologics / vaccines / enzyme therapies"],
  eur=47_300_000, investment_display="€47.3 million (Invitalia contract, €17.4M grant); separate ~€27M MISE agreement", jobs=None, status="Not found in public sources",
  expected_start="Not found in public sources (pre-2026 projects)",
  opportunity_status="Monitor",
  technical_scope="New line for sterile freeze-dried products under an Invitalia development contract, plus a 2022 MISE innovation agreement (~€27M, €6.3M grant) for prototype freeze-drying production systems.",
  orise_fit=[fit(LIF,"Moderate","Pre-2026 line already built; support and lifecycle work follow. "+BASIS),
             fit(CSV_,"Weak","Revalidation or change control on a sterile line. "+BASIS)],
  incumbent_vendors="", digital_signals=NF,
  sources=[src("https://www.quotidianosanita.it/?p=34138","Quotidiano Sanità","Unverified","Medium"),
           src("https://www.industriaitaliana.it/industria-farmaceutica-204-milioni-mise-sanofi-gelesis/","Industria Italiana","2022-04","Medium"),
           src("https://www.fortuneita.com/?p=318844","Fortune Italia","Unverified","Low"),
           src("https://www.sanofi.com/it/italia/anagni","Sanofi Italia","Unverified","Medium")],
  confidence="Low", orise_relevance="Low",
  notes="Both projects pre-date the Jan 2026 window; shown as Monitor only. €37M+ investment over the last three years (Mimit, Regione Lazio) is also cited by Sanofi's site page. Scoppito (€7.3M in 2024) not recorded as a project."),
 dict(id="chiesi-parma-biotech", account="chiesi", site_name="Chiesi Parma Biotech Center of Excellence", city="Parma", state="IT-EMR",
  lat=44.80, lon=10.33, project_type="BROWNFIELD", modality=["biologics/mAbs", "enzymes and other proteins"],
  eur=85_000_000, investment_display="€85 million (one source: ~€400M for the whole Parma biotech hub; not reconciled)", jobs=105, status="Not found in public sources",
  expected_start="Was due to be operational from 2024",
  opportunity_status="Monitor",
  technical_scope="Biotech centre inside the existing Parma site for development and production of active ingredients such as monoclonal antibodies, enzymes and other proteins.",
  orise_fit=[fit(LIF,"Moderate","If now operational, lifecycle and expansion support. "+BASIS),
             fit(CSV_,"Weak","Biologics GMP site changes. "+BASIS)],
  incumbent_vendors="", digital_signals=NF,
  sources=[src("https://www.fortuneita.com/?p=292103","Fortune Italia","Unverified","Low")],
  confidence="Low", orise_relevance="Low",
  notes="Pre-window project; the €85M and ~€400M figures conflict. Chiesi also plans related investment at Parma as part of the Nerviano strategy (no amount found)."),
 dict(id="gsk-italy-modernisation", account="gsk", site_name="GSK Italy plant modernisation programme 2025-2027 (Italy-wide)", city="San Polo di Torrile (Parma)", state="IT-EMR",
  lat=44.90, lon=10.40, project_type="BROWNFIELD", modality=["small molecule / oral and respiratory", "HIV / oncology (ViiV)"],
  eur=None, investment_display="~€215 million across GSK Italy 2025-2027 (not site-specific; not counted in totals)", jobs=None, status="announced",
  expected_start="2025-2027 (programme)",
  opportunity_status="Monitor",
  technical_scope="Reported plan to invest about €215M across GSK's Italian sites in 2025-2027, mainly for technology upgrades, environmental sustainability and plant modernisation. Pin placed at San Polo di Torrile as the main GSK plant; the split between Verona and Torrile is not disclosed.",
  orise_fit=[fit(LEG,"Moderate","A technology-upgrade programme often includes legacy control and MES refresh. "+BASIS),
             fit(DIG,"Moderate","Modernisation across plants is a digital trigger. "+BASIS),
             fit(CSV_,"Weak","Upgrades need revalidation. "+BASIS)],
  incumbent_vendors="", digital_signals=NF,
  sources=[src("https://www.ticonsiglio.com/gsk-offerte-lavoro-italia-estero-settore-farmaceutico/","Ticonsiglio","Unverified (about 135 days before search)","Low"),
           src("https://www.larena.it/argomenti/economia/economia-veronese/gsk-innovazione-accessibile-e-verona-resta-strategica-1.12990280","L'Arena","Unverified","Low"),
           src("https://www.aboutpharma.com/business-e-mercato/gsk-italia-800-milioni-investiti-nel-2020-2025-59-in-vaccini/","AboutPharma","Unverified","Medium")],
  confidence="Low", orise_relevance="Med",
  notes="Secondary source only; another source cites €324M across Italian sites. Needs the GSK Italy press release. Torrile's last confirmed project is the 2018 ViiV HIV plant (€30M)."),
 dict(id="menarini-sesto-150", account="menarini", site_name="Menarini Sesto Fiorentino production hub (older coverage)", city="Sesto Fiorentino (Florence)", state="IT-TOS",
  lat=43.83, lon=11.2, project_type="GREENFIELD", modality=["finished dosage (about 100M packs/yr)"],
  eur=150_000_000, investment_display="€150 million (reported)", jobs=None, status="Not found in public sources",
  expected_start="Not found in public sources",
  opportunity_status="Monitor",
  technical_scope="New plant of about 40,000 m² near Florence with capacity of roughly 100 million packs a year, as reported in older press. Date and current status not verified.",
  orise_fit=[fit(LIF,"Weak","If operational, lifecycle support. "+BASIS)],
  incumbent_vendors="", digital_signals=NF,
  sources=[src("https://en.ilsole24ore.com/art/menarini-investe-150-milioni-sesto-fiorentino-ADKah0V","Il Sole 24 Ore","Unverified","Low"),
           src("https://www.italpress.com/?p=155338","Italpress","Unverified","Low")],
  confidence="Low", orise_relevance="Low",
  notes="Probably pre-window. Kept to flag for verification; date not confirmed."),
]

REGION_NAMES = {"IT-LOM": "Lombardy", "IT-CAM": "Campania", "IT-TOS": "Tuscany", "IT-LAZ": "Lazio", "IT-EMR": "Emilia-Romagna"}

GAPS = """<h4 style="margin-top:0">Status of the Italy research</h4>
<p><b>First batch only:</b> Novartis, Sanofi, GSK, Eli Lilly, Menarini and Chiesi. Remaining Tier 1 (Roche, Merck KGaA, MSD, Pfizer, AbbVie, BMS, Bayer, Takeda, Amgen, AstraZeneca, J&amp;J/Janssen, Novo Nordisk) and Tier 2 (Angelini, Recordati, Italfarmaco, Zambon, Dompé, Alfasigma, Bracco, Kedrion, Catalent, Thermo Fisher/Patheon, BSP, CordenPharma, Olon, IBSA, Fareva) are not researched yet.</p>
<h4>How reliable the figures are</h4>
<ul><li>Amounts and dates come from <b>search-result summaries</b> of the cited pages. The pages themselves could not be opened in this environment, so each figure needs a quick manual check against the linked source before it is quoted to a customer.</li>
<li>Only Chiesi Nerviano is confirmed by several independent outlets (High). Others are Medium or Low; the reason is in each record's notes.</li>
<li>No site shows a public statement about MES, CSV or Industry 4.0 scope. The Orise fit ratings are assessed from project scope and are labelled that way.</li></ul>
<h4>Not yet searched</h4>
<ul><li>Permitting signals: VIA/VAS, AIA, SUAP and regional BUR notices; Invitalia and regional agency listings.</li>
<li>Trade press: NCF, AboutPharma, Pharmaceutical Technology Europe, BioProcess International; ISPE Italy and AFI.</li>
<li>Sanofi Scoppito, Novartis Ivrea and Origgio, Menarini L'Aquila and Pisa, Verona (GSK).</li></ul>
<h4>For you to fill</h4>
<ul><li>Paywalled and login sources (Industrial Info, IIR, LinkedIn) were not used. Contacts by role (site director, engineering/capital projects, automation or IT-OT lead, procurement) need your LinkedIn network.</li>
<li>Incumbent vendors per site (PAS-X, AVEVA PI, SCADA) are not public; internal knowledge needed.</li>
<li>EUR amounts are shown in USD at 1 USD = 0.86 EUR on the dashboard.</li></ul>"""

def main():
    data = {"accounts": ACCOUNTS, "sites": [], "gaps_html": GAPS, "as_of": AS_OF, "region_names": REGION_NAMES}
    for s in SITES:
        s = dict(s); s["country"] = "Italy"; s["currency"] = "EUR"; s["in_window"] = None
        s["technical_scope"] = s["technical_scope"]
        data["sites"].append(s)
    (ROOT / "data" / "it.json").write_text(json.dumps(data, ensure_ascii=False, indent=0))
    tier = {a["id"]: a["priority_tier"].replace("Tier ", "") for a in ACCOUNTS}
    name = {a["id"]: a["name"] for a in ACCOUNTS}
    cols = ["Company","Tier (1/2)","Site/Location (city)","Project name","Greenfield / Brownfield","Investment size (€)","Project type","Relevant to Orise? (High/Med/Low + why)","Modality/tech","Digital/automation signals","Status/timeline","Source URL(s)","Confidence (High/Med/Low)","Notes"]
    with open(ROOT / "italy" / "projects.csv", "w", newline="") as f:
        w = csv.writer(f); w.writerow(cols)
        for s in SITES:
            ptype = "New build / conversion" if s["id"] == "chiesi-nerviano" else ("Modernization" if "modernis" in s["site_name"].lower() else "Expansion")
            why = "; ".join(f"{x['area']} ({x['strength']})" for x in s["orise_fit"])
            w.writerow([name[s["account"]], tier[s["account"]], s["city"], s["site_name"], s["project_type"].title(),
                        (f"{s['eur']:,}" if s["eur"] else s["investment_display"]), ptype, f"{s['orise_relevance']} - {why}",
                        "; ".join(s["modality"]), s["digital_signals"], f"{s['status']}; {s['expected_start']}",
                        " | ".join(x["url"] for x in s["sources"]), s["confidence"], s["notes"]])
    lines = ["# Italy research: sources consulted", "", "Search engine summaries only; individual pages could not be opened (network policy). Confidence is per source.", ""]
    for a in ACCOUNTS:
        lines.append(f"## {a['name']}")
        for s in [x for x in SITES if x["account"] == a["id"]]:
            lines.append(f"### {s['site_name']} - {s['city']}")
            for x in s["sources"]: lines.append(f"- [{x['publisher']}]({x['url']}) - {x['date']} - Confidence: {x['confidence']}")
        lines.append("")
    lines += ["## Searches with no usable result", "- Sanofi Anagni/Scoppito 2026 announcements: none found",
              "- GSK Verona / San Polo di Torrile 2026 project: none found", "- Menarini L'Aquila and Pisa: none found", "- Chiesi Parma 2026 update: none found"]
    (ROOT / "italy" / "sources.md").write_text("\n".join(lines) + "\n")
    print("ok", len(SITES))

main()
