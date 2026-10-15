#!/usr/bin/env python3
"""Build data/it.json (consumed by build.py) from the Italy research files in this folder.

Inputs : italy/projects.csv (research output, one row per project) + the per-row geo and
         dashboard fields below (coordinates, region, short modality tags, numeric amount).
Output : data/it.json  (same schema as data/dach.json)

Nothing here adds facts: amounts, dates, notes, confidence and sources come from projects.csv.
What this script adds: coordinates of the named town, region code, short modality tags for the
filter, and a numeric euro amount where the CSV gives one project-specific figure. Where the CSV
gives only a plan-wide, group-wide or retrospective figure the numeric amount is left empty so
it does not inflate the totals (the text is still shown).
"""
import csv, json, pathlib, re
from urllib.parse import urlparse

ROOT = pathlib.Path(__file__).resolve().parent.parent
AS_OF = "October 15, 2026"
USD_PER_EUR = 1 / 0.86

# One tuple per CSV row, in file order:
# (lat, lon, region, [modality tags], eur_number|None, amount_text, jobs|None, status, start, opportunity, in_window)
OPEN, MON, LATE = "OPEN OPPORTUNITY", "Monitor", "Closed/late"
ROWS = [
 (45.55, 8.99, "IT-LOM", ["inhalers / respiratory", "biologics/mAbs"], 430e6, "€430 million, 2025-2030", 300, "announced", "Announced Mar 2025; first activity possibly 2026, full operation by 2030", OPEN, True),
 (44.80, 10.33, "IT-EMR", ["biologics/mAbs", "enzymes / proteins"], 85e6, "€85 million (initial investment)", None, "operational", "Build began Nov 2022; operational from 2024 per company", MON, False),
 (43.83, 11.20, "IT-TOS", ["biologics (insulin / diabetes and obesity)"], 750e6, "€750 million, announced Oct 2023 for 2 years", None, "under construction", "Phase 1 built; second tirzepatide line started (Apr 2026). Phase 2 not confirmed by Lilly", OPEN, True),
 (44.90, 10.40, "IT-EMR", ["specialty sterile / oral", "oncology / HIV"], 170e6, "€170 million planned 2025-2027 (€240M invested 2022-2024)", None, "announced", "Planned 2025-2027; no project breakdown public", OPEN, True),
 (43.25, 11.20, "IT-TOS", ["vaccines"], 215e6, "€215 million planned 2025-2027 (plant and Siena research campus together)", None, "announced", "Planned 2025-2027; no breakdown", OPEN, True),
 (43.81, 11.17, "IT-TOS", ["oral solid dose"], 150e6, "€150 million (announced 2020)", None, "Not confirmed in sources", "Zoning approved Apr 2022; no 2023-2026 source found", OPEN, None),
 (43.78, 11.23, "IT-TOS", ["sterile fill-finish (vials)"], 14e6, "€14-15 million (search summary only; lower bound used)", None, "announced", "Approved per Lucia Aleotti; date not confirmed", MON, True),
 (40.75, 14.45, "IT-CAM", ["solid oral / packaging"], 80e6, "€80 million authorised (ZES unica, Sep 2024); €32M first phase (Mar 2023)", None, "under construction", "New area opened Feb 2024; authorisation said build planned by 2025", OPEN, None),
 (45.47, 7.88, "IT-PIE", ["radioligand / R&D and production"], None, "€350 million Italy plan to 2025 (site split not found; not counted)", None, "ended 2025", "Announced Nov 2023, deadline 2025; no follow-up found", MON, False),
 (41.74, 13.15, "IT-LAZ", ["biotech injectables", "sterile lyophilised", "vaccines"], 13.4e6, "€13.4 million (2025)", None, "operational", "2025 spend; no individual 2026-27 project found", OPEN, None),
 (42.37, 13.27, "IT-ABR", ["high-potency oral solid dose"], 7e6, "Over €7 million (2025); Columbus €23.6M already built", None, "operational", "2025 spend; further 2026 scope not found", OPEN, None),
 (41.74, 13.15, "IT-LAZ", ["sterile fill-finish (syringes, vials, cartridges)"], 1e9, "Over €1 billion (announced as €2.0-2.2B in Mar 2025; second billion reported frozen)", 400, "permits in progress", "Permit issued Dec 2025; conferenza di servizi outcome not found", OPEN, True),
 (41.09, 16.78, "IT-PUG", ["sterile fill-finish (isolator syringes)", "biotech / fertility"], 56e6, "€56 million syringe line (€228M modernisation plan since 2015)", None, "under construction", "Announced 26 Jan 2026; isolator validation pending", OPEN, True),
 (43.72, 10.40, "IT-TOS", ["plasma-derived therapies"], None, "€350 million invested over 5 years, Pisa and Rieti (past spend; not counted)", None, "operational", "No planned 2026-27 project found", MON, False),
 (41.50, 12.92, "IT-LAZ", ["ADC (bioconjugation + sterile fill-finish)"], 400e6, "About €400 million across four Invitalia contracts since 2015 (verified); other figures unverified", None, "under construction", "Four contracts since 2015; newest build status not found", OPEN, None),
 (42.85, 13.58, "IT-MAR", ["oral solid packaging"], 70e6, "€70 million over 2 years (2023 statement; snippet)", None, "operational", "Past; no in-window project", MON, False),
 (37.50, 15.09, "IT-SIC", ["sterile injectables"], 27e6, "€27 million 2022-2024", None, "operational", "2022-2024; no in-window project", MON, False),
 (41.57, 12.65, "IT-LAZ", ["biologics assembly / packaging"], 30e6 * 0.86, "USD 30 million (Sep 2019)", None, "operational", "2019 announcement; nothing for 2025-27", LATE, False),
 (41.42, 12.93, "IT-LAZ", ["oral solid dose"], 58e6, "€58 million (Oct 2020 to end 2021)", None, "operational", "Completed about 2021; nothing newer found", LATE, False),
 (44.08, 10.43, "IT-TOS", ["plasma fractionation"], 150e6, "€150 million (about €120M building + €30M efficiency)", 300, "under construction", "Presented 11 May 2026; construction ends end 2026, validation 2027, FDA targeted 2028, full capacity 2031", OPEN, True),
 (45.58, 9.52, "IT-LOM", ["sterile fill-finish (PFS, vials, cartridges)", "CDMO"], 80e6, "€80 million multi-year (includes €13M property purchase)", None, "announced", "Release 10 Sep 2026; isolator lines complete mid-2027 and 2028", OPEN, True),
 (41.67, 12.50, "IT-LAZ", ["oral solid dose"], 40e6, "Over €40 million 2026-2027 (COO later cited almost €50M)", None, "announced", "Announced 20 Jul 2026; period 2026-2027", OPEN, True),
 (45.58, 9.27, "IT-LOM", ["sterile fill-finish", "CDMO"], 100e6, "€50M Monza (2025) + €50M Ferentino planned; two new plants planned at each site", None, "announced", "Il Giorno 27 Jul 2025; no dates for new plants", OPEN, None),
 (45.55, 11.55, "IT-VEN", ["multi-form incl. sterile liquid / lyophilised"], 70e6, "€70 million over five years (whole Vicenza plant)", None, "commissioning", "Final tests Oct 2024; clearance expected Q4 2025; opening not confirmed", MON, None),
 (42.35, 13.40, "IT-ABR", ["oral liquids / syrups"], 50e6, "Over €50 million in the last 5 years (completed); €1B 2026-28 is group-wide, not counted", None, "operational", "Last tranche finished Sep 2026", MON, False),
 (45.82, 13.28, "IT-FVG", ["API (contrast media)"], 120e6, "€120 million total (Progetto Galileo €60M), 2021", None, "operational", "Industry 4.0 department inaugurated 8 Oct 2021; pre-window", LATE, False),
 (45.31, 9.50, "IT-LOM", ["hyaluronic-acid prefilled syringes"], 13.5e6, "€13.5 million (plant, inaugurated Oct 2026)", None, "operational", "Inaugurated early Oct 2026", LATE, True),
 (41.57, 12.65, "IT-LAZ", ["chemical API"], 20.7e6, "€20.7 million PP&E 2025 (Milan and Campoverde)", None, "operational", "Redundancy accord reached; investment plans unspecified", MON, None),
 (45.47, 9.34, "IT-LOM", ["ADC payloads / linkers", "HPAPI"], None, "Not found in public sources", None, "announced", "Main ADC expansion is in France (end 2026 / early 2027)", MON, None),
]

REGION_NAMES = {"IT-LOM": "Lombardy", "IT-EMR": "Emilia-Romagna", "IT-TOS": "Tuscany", "IT-CAM": "Campania", "IT-LAZ": "Lazio",
                "IT-ABR": "Abruzzo", "IT-PUG": "Apulia", "IT-MAR": "Marche", "IT-SIC": "Sicily", "IT-VEN": "Veneto",
                "IT-FVG": "Friuli-Venezia Giulia", "IT-PIE": "Piedmont"}

# Account display names (the CSV 'Company' column is kept in each site's notes)
NAMES = {"Dompe": "Dompé", "Merck KGaA (EMD)": "Merck KGaA (EMD)", "Johnson & Johnson (Janssen)": "Johnson & Johnson (Janssen)",
         "Thermo Fisher (Patheon)": "Thermo Fisher (Patheon)", "BSP Pharmaceuticals": "BSP Pharmaceuticals"}

# Account-level text, taken from italy/territory-plan.md (ranking, entry angle) and accounts-stack-and-roles.md
ACCT = {
 "Chiesi": ("Largest confirmed in-window project: a multi-year conversion of a 124,000 m² site, so systems architecture is still open. Entry before vendors are locked.", "",
            "Postings at Nerviano (Sterile Supervisor: URS, FAT/SAT, commissioning and qualification; Technology SME; Site Plant Controller Lead) show the start-up phase. No site director named publicly."),
 "Eli Lilly": ("Phase 1 is running; phase 2 (+300 jobs per the Tuscany Region) is not confirmed by Lilly and depends on pricing and access policy. Pursue lifecycle now, watch phase 2.",
               "MES Architect posting (site unconfirmed): PharmaSuite, PAS-X, Syncade, DeltaV, Annex 11 / GAMP 5 (snippet; page now 404).", ""),
 "GSK": ("Largest planned Italian spend, but no project breakdown is public. Ask for the 2025-27 project list at Parma.", "No Italian stack found (US and Ireland postings name DeltaV, Rockwell, AVEVA; not transferable).", ""),
 "Menarini": ("Smart-manufacturing brief at Sesto (€150M) but construction status is unresolved; the Florence vials line is small and unverified.", "No automation or MES stack found.", ""),
 "Novartis": ("FDA-approved site growing; €80M authorised via ZES unica. Fit-out, qualification and lifecycle are the live angle. No digital detail in the sources.",
              "OT Automation Engineer postings (Italy, city not stated) name SCADA, Historian, MES, OPC, MQTT and GxP.", ""),
 "Sanofi": ("Explicit digital ambition at Anagni (fully digital management, biologics transition). Scoppito is already paper-free, so the angle is lifecycle and data integrity.",
            "Group stack (US postings, Italian sites not confirmed): Siemens Opcenter, Koerber PAS-X, PI, Ignition.", ""),
 "Novo Nordisk": ("Largest Italian project found (fill-finish, ex-Catalent Anagni), but the amount is contested (€1B vs €2B) and the final authorisation outcome is not found. Start the relationship now, size the deal later.",
                  "No stack named. An Anagni/Frosinone aseptic automation posting asks for PLC and SCADA (snippet).",
                  "No site head named. Position through local integrators or validation support; Novo uses central engineering for global fill-finish builds."),
 "Merck KGaA (EMD)": ("Isolator syringe line under construction with validation pending; about €10M of the plan is for digitalisation.", "No stack named.",
                      "Annalisa Calvano, Site Director (2019 appointment; Site Head per Jan 2026 press; verify). Best buyer role: 'Operation Technology, Digital & Data Associate Director' posting."),
 "Takeda": ("Past spend only; no in-window project found. Ask Takeda for the 2026-28 capex plan before investing effort.", "", ""),
 "BSP Pharmaceuticals": ("ADC expansion backed by Invitalia, 2026 ISPE Facility of the Year award; a sophisticated digital buyer. Verify the current build.", "'One unified set of batch records'; platform not named.", ""),
 "Pfizer": ("Watch account: past spend, shrinking sites, no in-window project public.", "", ""),
 "AbbVie": ("Watch account: 2019 announcement only.", "", ""),
 "Johnson & Johnson (Janssen)": ("Watch account: 2020-21 upgrade only.", "", ""),
 "Kedrion": ("Best timing fit in the territory: construction ends end 2026, qualification and validation in 2027. The company names cybersecurity and AI as priorities. Approach before validation scope is awarded.", "No stack named.",
             "Massimiliano Barberis, COO (quoted on the Bolognana timeline); CEO Ugo Di Francesco. 'Director IT' listed by an aggregator is unverified."),
 "CordenPharma": ("CDMO with isolator lines completing mid-2027 and 2028; data-integrity and validation exposure. Entry via the CSV specialist and QA compliance roles.", "Equipment named (Bausch+Stroebel isolator, Syntegon line); no software stack.",
                  "No site head found. A Computer System Validation Specialist posting at Caponago."),
 "Alfasigma": ("EUR 40-50M oral solid dose plan 2026-27 plus insourcing; no digital scope stated.", "", ""),
 "Thermo Fisher (Patheon)": ("Large CDMO sterile sites; figures rest on one 2025 newspaper article. Ask which planned plants are funded.", "", ""),
 "Zambon": ("New department was in final testing in Oct 2024; opening unconfirmed. Lifecycle angle only.", "", ""),
 "Dompe": ("Last L'Aquila phase finished Sep 2026; the €1B plan is group-wide. Low priority.", "", ""),
 "Bracco": ("Progetto Galileo is a 2021 project (pre-window). Watch the reported larger plan.", "", ""),
 "IBSA": ("New Lodi plant just inaugurated; lifecycle only.", "", ""),
 "Recordati": ("Restructuring at Campoverde; watch account.", "", ""),
 "Olon": ("ADC payload and linker capability; main expansion is in France.", "", ""),
}

# Orise offering areas and the keywords in the research text that signal them
AREAS = [
 ("SCADA / process control and automation", r"SCADA|automat|OT |control system|PLC"),
 ("MES implementation and integration", r"\bMES\b|eBR|batch record|LIMS"),
 ("Digitalization / Industry 4.0", r"digital|Industry 4\.0|\bAI\b|smart manufacturing|connect"),
 ("Validation / CSV / data integrity", r"CSV|validation|CQV|Annex|data.integrity|qualification|FAT/SAT"),
 ("Legacy system modernization and migration", r"moderni[sz]|legacy|upgrade"),
 ("Lifecycle support and managed services", r"lifecycle|periodic review|support"),
]
STRENGTH = {"High": "Strong", "Med-High": "Moderate", "Med": "Moderate", "Low-Med": "Weak", "Low": "Weak"}


def relevance_level(text):
    m = re.match(r"\s*(High|Med-High|Low-Med|Med|Low)\b", text)
    return m.group(1) if m else "Low"


def fits(rel, digital):
    level = relevance_level(rel)
    strength = STRENGTH[level]
    hay = rel + " " + (digital if not digital.lower().startswith(("not found", "none", "not mentioned")) else "")
    out = []
    for area, pat in AREAS:
        if re.search(pat, hay, re.I):
            out.append({"area": area, "strength": strength,
                        "reason": "From the Italy research notes: " + rel.split(" - ", 1)[-1].strip()})
    if not out:  # no offering area named in the text: general fit, capped at Moderate
        why = "From the Italy research notes (no specific offering area named): " + rel.split(" - ", 1)[-1].strip()
        cap = "Moderate" if strength == "Strong" else strength
        out = [{"area": a, "strength": cap, "reason": why} for a in (AREAS[3][0], AREAS[5][0])]
    return out[:4]


def sources_for(urls, conf):
    out = []
    for u in [x.strip() for x in re.split(r"\s;\s", urls) if x.strip()]:
        u = re.sub(r"\s*\(.*$", "", u).strip()
        host = urlparse(u).netloc.replace("www.", "")
        out.append({"url": u, "publisher": host, "date": "", "confidence": conf})
    return out


def main():
    rows = list(csv.DictReader(open(ROOT / "italy" / "projects.csv", encoding="utf-8")))
    assert len(rows) == len(ROWS), (len(rows), len(ROWS))
    by_company = {}
    sites = []
    for r, g in zip(rows, ROWS):
        lat, lon, region, mods, eur, amount_text, jobs, status, start, opp, in_win = g
        company = r["Company"]
        name = NAMES.get(company, company)
        by_company.setdefault(company, []).append(r)
        conf = r["Confidence"].strip()
        pt = "GREENFIELD" if r["Greenfield / Brownfield"].lower().startswith("greenfield") else "BROWNFIELD"
        city = re.sub(r"\s*\(.*?\)", "", r["Site/Location"]).strip()
        scope = f'{r["Project name"]}. Modality: {r["Modality/tech"]}. Digital / automation signals: {r["Digital/automation signals"]}.'
        notes = r["Notes"] + (f' Project type in research file: {r["Project type"]}. Greenfield/brownfield note: {r["Greenfield / Brownfield"]}.')
        sites.append({
            "id": re.sub(r"[^a-z0-9]+", "-", (company + " " + r["Project name"]).lower()).strip("-")[:70],
            "account": company, "site_name": r["Project name"], "city": city, "state": region,
            "lat": lat, "lon": lon, "project_type": pt, "modality": mods,
            "eur": round(eur) if eur else None, "investment_display": amount_text, "jobs": jobs,
            "status": status, "expected_start": start, "opportunity_status": opp, "in_window": in_win,
            "technical_scope": scope, "orise_fit": fits(r["Relevant to Orise? (High/Med/Low + why)"], r["Digital/automation signals"]),
            "incumbent_vendors": "", "sources": sources_for(r["Source URL(s)"], conf),
            "notes": f'Confidence in research file: {conf}. Status/timeline: {r["Status/timeline"]} {notes}',
            "country": "Italy", "currency": "USD" if "USD" in amount_text and company == "AbbVie" else "EUR",
        })
    accounts = []
    for company, rs in by_company.items():
        reason, stack, roles = ACCT[company]
        accounts.append({
            "id": company, "name": NAMES.get(company, company), "priority_tier": f"Tier {rs[0]['Tier']}",
            "footprint_summary": "Sites in this research: " + "; ".join(r["Site/Location"] for r in rs) + ".",
            "investment_strategy_summary": " ".join(f'{r["Project name"]}: {r["Investment size (EUR)"]}.' for r in rs),
            "priority_reason": reason, "incumbent_vendors_general": stack, "ownership_note": "", "roles": roles,
        })
    gaps = """<h4 style="margin-top:0">About the Italy data</h4>
<p>Built from the Italy research files (29 projects, 23 accounts, researched 14-15 October 2026): <code>italy/projects.csv</code>, <code>sources.md</code>, <code>territory-plan.md</code> and <code>accounts-stack-and-roles.md</code>. Amounts, dates, notes and confidence are as written there. The coordinates and the Orise fit ratings on the dashboard were added when loading: fit areas are matched from the wording of each row's "Relevant to Orise" note, and the strength follows its High / Med / Low rating. They are research judgement, not sourced facts.</p>
<ul><li><b>Opportunity status</b> follows the same rating: High and Med-High in or near the window are Open; Med, Low and watch accounts are Monitor; completed or pre-window projects are Closed/late.</li>
<li><b>Totals are a floor.</b> Plan-wide, group-wide and retrospective figures (for example Takeda €350M over five years, Novartis €350M Italy plan, Dompé €1B group plan, GSK-style plans without a site split) are shown in text but not added to totals. A few single-source figures are marked Low confidence.</li>
<li><b>Replaces my first batch.</b> An earlier version of this view used figures from search summaries that these files correct: Novartis Torre Annunziata €32M dates from March 2023 (the €80M authorisation is Sept 2024), the Menarini vials figure is unverified, and the GSK figures are €170M Parma and €215M Tuscany.</li></ul>
<h4>Gaps and next steps (from the territory plan)</h4>
<ol><li>Menarini Sesto: construction or start-up status unresolved (last milestone April 2022).</li>
<li>Unverified: GSK Parma GBP 80M line (2022), Menarini €14-15M vials line, Lilly 200-staff move in 2027. Sources that returned 403 include Fierce Pharma, fedaiisf and FirenzeToday.</li>
<li>Permits not reachable by the research tools: Nerviano albo/SUE, Regione Lombardia VIA/AIA, Tuscany BUR.</li>
<li>Invitalia and MIMIT award lists are not indexed by search; check concession decrees manually.</li>
<li>Lilly phase 2 depends on the Tuscany pricing dispute. Novo Anagni: find the conferenza di servizi outcome and the real capex.</li>
<li>Roche, MSD, Bayer, BMS, Amgen and AstraZeneca: no Italian manufacturing capex found by web search; confirm with a paid database or direct contact. Italfarmaco, Angelini, Fareva and Corden Sermoneta: nothing found.</li>
<li>Tech stacks and contacts: only five accounts have a first public-web pass (Merck Bari, Kedrion, CordenPharma, Chiesi Nerviano, Novo Anagni). LinkedIn buyer mapping is on your side; no emails or phone numbers were collected.</li>
<li>Check Orise's PAS-X capability before using it as a hook; check each company's NIS2 scope in Italy before leading with it.</li></ol>"""
    out = {"accounts": accounts, "sites": sites, "gaps_html": gaps, "as_of": AS_OF, "region_names": REGION_NAMES}
    (ROOT / "data" / "it.json").write_text(json.dumps(out, ensure_ascii=False, indent=0))
    print("ok", len(sites), "sites", len(accounts), "accounts")


main()
