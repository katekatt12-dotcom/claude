#!/usr/bin/env python3
"""Build data/ie.json (consumed by build.py) from the Ireland research files in this folder.

Inputs : ireland/projects.csv (research output, one row per project; a blank row is skipped)
         ireland/territory-plan.md (priority grades, roles) and ireland/sources.md (stack evidence)
Output : data/ie.json  (same schema as data/dach.json and data/it.json)

Nothing here adds facts: amounts, dates, notes, confidence and sources come from projects.csv; account
priority text, roles and stack signals come from the territory plan and sources log. What this script adds:
coordinates of the named town, county code, short modality tags for the filter, one numeric euro amount
per project (USD amounts are converted at the dashboard rate), and offering-fit ratings derived from the
plan's overall grade. Plan-wide, acquisition-price or already-counted figures are left out of the numeric
total so they do not inflate it; the text is still shown.
"""
import csv, json, pathlib, re
from urllib.parse import urlparse

ROOT = pathlib.Path(__file__).resolve().parent.parent
AS_OF = "October 15, 2026"
OPEN, MON, LATE = "OPEN OPPORTUNITY", "Monitor", "Closed/late"
USD = 0.86  # EUR per USD, same rate as the rest of the dashboard

# One tuple per CSV data row, in file order:
# (lat, lon, county, [modality tags], eur|None, amount text, jobs|None, status, start, opportunity, in_window, plan grade)
ROWS = [
 (54.00, -6.40, "IE-LH", ["vaccines (drug substance + drug product)"], 500e6, ">€500 million (USD 520M) purchase price of the former WuXi Vaccines plant (acquisition, not capex)", 150, "operational", "Handover H1 2025; +150 staff by end-2025; ramp and integration through 2026-2027", OPEN, True, "A-"),
 (52.84, -6.93, "IE-CW", ["vaccines / biologics / sterile / small molecule"], None, "No single figure (about 1,000 jobs across 8 Irish sites)", None, "announced", "Announced Jan 2025; 'over coming years'", MON, True, "-"),
 (53.42, -6.47, "IE-MH", ["biologics (drug substance)"], None, "€1 billion combined with Carlow (2023; context only)", None, "operational", "Opened Sept 2023, outside the window", LATE, False, "-"),
 (52.64, -8.67, "IE-LK", ["biologics (monoclonal antibodies, drug substance)"], 2e9 * USD, "About USD 2 billion (€400M initial + USD 1bn expansion Sept 2024 + reported extra USD 500M)", 450, "under construction", "Production start targeted for 2026 (no confirmation found)", OPEN, True, "A+"),
 (51.71, -8.52, "IE-CO", ["sterile / drug product (tirzepatide)"], 800e6 * USD, "USD 800 million (part of the USD 1.8bn Sept 2024 package)", None, "operational", "Making medicines since 2025; ramp active 2026-2027", OPEN, True, "A"),
 (53.32, -6.43, "IE-D", ["biologics (drug substance, mAbs)"], 1.2e9, "€1.2 billion (USD 1.26bn)", 500, "under construction", "Construction since 2023; final commissioning 2027", OPEN, True, "A+"),
 (51.83, -8.32, "IE-CO", ["clinical / development API"], None, "Part of the €1.2bn package (not counted again)", None, "announced", "Tied to the Grange Castle programme", MON, None, "-"),
 (51.83, -8.32, "IE-CO", ["biopharma drug substance / API"], 150e6, "€150 million (2022 expansion, likely complete)", 180, "operational", "2022 to about 2024; land purchases signal a later expansion", MON, None, "Watch"),
 (53.32, -6.43, "IE-D", ["cell therapy"], 36e6, "€36 million", 100, "commissioning", "Announced about 2023-24; ramp and qualification active into 2026", OPEN, True, "B"),
 (51.91, -8.26, "IE-CO", ["sterile / aesthetics"], 60e6, "€60-63 million", 70, "operational", "Construction from 2023; operational from 2025; ramp 2025-2026", OPEN, True, "B-"),
 (53.40, -6.30, "IE-D", ["manufacturing services hub"], 23e6, "€23 million", None, "announced", "Establishment phase", MON, None, "-"),
 (53.29, -6.14, "IE-D", ["aseptic fill-finish (vials, lyophilisation)"], 407e6 * USD, "USD 407 million (€353M) capex 2023-2024", None, "operational", "Installation and testing 2023-24; active; workforce to about 2,888 by 2035", OPEN, True, "A-"),
 (52.64, -8.67, "IE-LK", ["biologics (bulk drug substance)", "R&D / process science"], 100e6, "€100 million confirmed (Oct 2025; about €200M programme reported, not reconciled)", 300, "under construction", "Process Science building built; larger admin/lab building filed; a construction-compound permission was refused on appeal (Sept 2025)", OPEN, True, "B+"),
 (51.83, -8.32, "IE-CO", ["small molecule API"], None, "n/a (site divested to Sterling Pharma Solutions)", None, "divested", "Transfer agreed 2022, completed 2023; campus acquisition finalising about 2026", LATE, False, "Neg"),
 (51.91, -8.26, "IE-CO", ["oral solids / packaging"], 45e6, "About €45 million (2023 reports)", None, "operational", "No new 2026-27 project found", MON, False, "Watch"),
 (51.83, -8.37, "IE-CO", ["biologics (DS, DP, fill-finish)", "QC / process development lab"], 90e6, "€60 million lab + more than €30 million packaging", 40, "under construction", "Active 2025-2027; exact go-live not confirmed", OPEN, True, "B"),
 (54.00, -6.41, "IE-LH", ["ADC / conjugation", "biologics"], 325e6, "€325 million (original campus); new conjugation lines inside it", None, "commissioning", "Conjugation DS and DP lines to start GMP manufacturing in 2026", OPEN, True, "B"),
 (53.39, -6.38, "IE-D", ["biologics (bulk drug substance)"], 65e6, "€65 million (IDA); USD 360M (€326M) is the wider AstraZeneca Irish programme", 105, "operational", "Planning granted May 2023; IDA reported the facility opened in April 2026 (page not read)", OPEN, True, "B+"),
 (52.26, -7.11, "IE-WD", ["biologics / rare disease (haemophilia)"], 44e6, "€44 million (campus); extension recently permitted", None, "under construction", "Extension permitted 2024-25", OPEN, None, "B-"),
 (52.65, -7.25, "IE-KK", ["medtech / diagnostics (not biopharma GMP)"], 440e6, "€440 million (Kilkenny + Donegal)", 1000, "operational", "Kilkenny opened Nov 2024; ramping 2025-2026", MON, None, "C"),
 (51.80, -8.33, "IE-CO", ["small molecule API"], None, "n/a (site divested to Thermo Fisher)", None, "divested", "No new in-window GSK build found", LATE, False, "Neg"),
 (53.42, -7.97, "IE-RN", ["oral solid dose (oral GLP-1 tablets)"], 432e6, "€432 million (USD 506M)", 260, "under construction", "Announced 2 Mar 2026; construction begun; completes end-2027 through 2028", OPEN, True, "A"),
 (52.82, -8.97, "IE-CE", ["former API site (remediation, sale)"], None, "n/a (€207.56M cumulative remediation spend; not a build)", None, "closed", "Plant closed 2016; first tranche of the 88-acre site available late 2027", MON, False, "Neg"),
 (51.91, -8.26, "IE-CO", ["bioprocessing consumables (membranes, filtration)"], 440e6, "€440 million (€290M Carrigtwohill + €150M Blarney)", 370, "under construction", "Blarney opened Sept 2025; Carrigtwohill first output 2026; programme completes 2027", OPEN, True, "B+"),
 (53.39, -6.38, "IE-D", ["small molecule API (oncology)"], 67e6, "€52 million delivered + €15 million more to 2026", None, "operational", "€15M planned through 2026", MON, True, "C+"),
 (52.80, -6.16, "IE-WW", ["oral solid dose", "CDMO"], None, "Not found in public sources (last major capex €184M, 2006)", None, "Not confirmed in sources", "No 2026-27 project found", MON, None, "Watch"),
 (52.27, -9.70, "IE-KY", ["sterile fill-finish (aseptic drug product)"], 330e6, "€330 million (earlier commitment); second-line cost not disclosed", None, "under construction", "Second aseptic line announced 14 Sep 2026; opening date contested (Q3 2027 vs 2028 vs early 2027); capacity targeted by 2029", OPEN, True, "High"),
 (53.35, -6.26, "IE-D", ["packaging (injectables, OSD)", "CDMO"], None, "Not found for Ireland (group-wide USD 365M)", None, "operational", "CityNorth due to begin Q3 2025; Dundalk operational", MON, False, "Low"),
 (53.40, -6.43, "IE-D", ["elastomer components (supplier)"], None, "Not found in public sources", 330, "operational", "Opened late March 2026", MON, True, "Low"),
]

# Row indices classed greenfield (the CSV has no such column): Lilly Raheen, Pfizer DS2, Abbott Kilkenny, Astellas Tralee
GREENFIELD = {3, 5, 19, 26}

COUNTY_NAMES = {"IE-D": "Dublin", "IE-CO": "Cork", "IE-LK": "Limerick", "IE-LH": "Louth", "IE-MH": "Meath", "IE-CW": "Carlow", "IE-WD": "Waterford",
                "IE-KK": "Kilkenny", "IE-RN": "Roscommon", "IE-CE": "Clare", "IE-WW": "Wicklow", "IE-KY": "Kerry"}

# Priority tier from the plan's own grouping (section 2): Tier 1 anchors, Tier 2 mid-large, Tier 3 focused builds, Tier 4 watch / other domain / divesting.
TIER = {"MSD (Merck & Co.)": 1, "Eli Lilly": 1, "Pfizer": 1, "Novo Nordisk": 1,
        "Merck KGaA (MilliporeSigma / Life Science)": 2, "Amgen": 2, "Regeneron": 2, "Astellas": 2,
        "Alexion (AstraZeneca)": 3, "BioMarin": 3, "Takeda": 3, "AbbVie": 3, "Sanofi (Genzyme)": 3, "Ipsen": 3, "WuXi Biologics": 3,
        "Abbott": 4, "Gilead Sciences": 4, "Johnson & Johnson (Innovative Medicine / Janssen)": 4, "Servier": 4, "Novartis": 4, "GSK": 4, "Roche": 4,
        "PCI Pharma Services": 4, "West Pharmaceutical Services": 4}

# (priority reason, stack signals from job postings, public roles)
ACCT = {
 "Pfizer": ("Rank 1 (A+). DS2 biologics build underway, final commissioning 2027, so automation, CSV, MES and historian spend is committed in 2026-27. Engage capital projects and automation now.",
            "Job postings: DeltaV DCS, Honeywell, package PLCs, SCADA; AVEVA PI with Rockwell PLCs and FactoryTalk View. Earlier case study: GE Historian. Delivery partners on site: PM Group, PJ Hegarty, Jones Engineering, NeoDyne.",
            "Julien Deneve, Site Leader, Grange Castle (public source; confirm current)."),
 "Eli Lilly": ("Ranks 2 and 4 (A+, A). Raheen biologics API starts production in 2026 (qualification now) and Kinsale is ramping tirzepatide. One Lilly Ireland relationship covers both sites.",
               "Postings (Medicine Foundry): DeltaV, Rockwell, Syncade, LabVantage, OSI PI.",
               "Dave Riordan, General Manager, Limerick (quoted in expansion press)."),
 "Novo Nordisk": ("Rank 3 (A). Announced 2 March 2026; construction live to 2028; oral solid dose means serialization, MES and CSV. Move early, before line vendors lock scope.",
                  "Postings: DeltaV, Rockwell and Siemens PLC, Syncade and PAS-X MES, OSI PI / iBatch, SQL. Novo Nordisk Engineering is the captive EPCM.",
                  "Tom Quinn, VP & Site General Manager, NN Production Ireland (Mar 2026). Dilek Dogan Gurluk, General Manager, NN Ireland (commercial)."),
 "MSD (Merck & Co.)": ("Rank 6 (A-). Integrating an acquired vaccine plant: IT/OT convergence, historian migration and CSV of inherited systems. The €1bn Carlow and Dunboyne builds opened in 2023.", "", ""),
 "Amgen": ("Rank 5 (A-). Aseptic fill line install and test means live CSV, serialization and historian work. A March 2026 planning application points to further growth.",
           "Dún Laoghaire postings: Allen-Bradley, Siemens and B&R PLC, iFix / InTouch / Zenon SCADA, FactoryTalk Batch, OSIsoft PI, Körber MES.",
           "Cathal Elliott, listed principal of Amgen Technology (Ireland) UC (confirm site title)."),
 "Regeneron": ("Rank 7 (B+). Bulk biologics plus a new admin/lab building. The €100M and ~€200M figures are not reconciled, and a drainage appeal refused one permission.",
               "Raheen postings: DeltaV (ISA-88), Rockwell PLC; an automation infrastructure role covers historian and data integration.",
               "Niall O'Leary, VP & Site Head, IOPS Limerick (reported 2020; verify). Dan Van Plew, EVP & GM, IOPS (corporate)."),
 "Merck KGaA (MilliporeSigma / Life Science)": ("Rank 8 (B+). New membrane and filtration lines reach commercial output 2026-27. A different Irish API plant is to be mothballed by end-2028 (site not identified).", "", ""),
 "Alexion (AstraZeneca)": ("Rank 9 (B+). APICOM drug-substance facility; IDA reported it opened in April 2026, so the angle shifts from commissioning to lifecycle, historian and expansion. Modality wording still to confirm.",
                           "APICOM MES Specialist posting: Körber PAS-X MES, DeltaV, eMBR, LIMS, SAP S/4HANA; OSI / AVEVA PI historian.",
                           "Maureen Larkin, Executive Director & Site Lead, College Park. Shane Doyle (SVP Global Ops & Sustainability) and Sylvia Kiely (VP Global Supply Chain), corporate."),
 "BioMarin": ("Rank 10 (B). End-to-end biologics; the new QC / process-development lab suits LIMS and historian, packaging suits serialization.",
              "Shanbally Sr Manager Automation & MES posting: DeltaV, Siemens PLC, OSI PI, OEE, BAS, MES, CSV.",
              "Conor Delaney (VP Ops & Site Leader) and Geraldine Cregan (Exec Director & Quality Site Head), reported 2023; confirm current."),
 "Takeda": ("Rank 11 (B). Cell therapy is a premium technical fit; small capex.", "", ""),
 "AbbVie": ("Rank 12 (B-). New sterile lines ramping at Carrigtwohill; the North Dublin hub is lower fit.", "", ""),
 "Sanofi (Genzyme)": ("Rank 13 (B-). Biologics site with a planning-permitted extension; an FDA citation over Altuviiio points to a data-integrity / CSV remediation angle.", "", "Cian O'Brien, Site Head (appointed 2024)."),
 "WuXi Biologics": ("Rank 14 (B, with caveat). ADC conjugation lines reach GMP in 2026, a strong modality fit, but US BIOSECURE uncertainty affects WuXi's commercial stability.", "", ""),
 "Ipsen": ("Rank 15 (C+). Small oncology API upgrade; mid-market entry.", "", ""),
 "Astellas": ("Added in the Oct 2026 refresh, not on the starter list. High fit: the Tralee facility opens early 2027 to 2028, so CQV, MES/eBR and CSV decisions are live; a second aseptic line adds scope to 2029. Automation scope and integrator not found.", "", ""),
 "Abbott": ("Domain call for you: a €440M medtech / diagnostics build with automation, MES and serialization needs, but not GMP biopharma.", "", ""),
 "Gilead Sciences": ("Watch: significant oral-solids site, but no in-window capital confirmed.", "", ""),
 "Johnson & Johnson (Innovative Medicine / Janssen)": ("Watch: €150M 2022 expansion likely complete; land banking signals a later build. On 13 Oct 2026 J&J said it intends to spin off DePuy Synthes (about 1,700 staff at Ringaskiddy); orthopaedics, not pharma, but shared site IT/OT could be affected.", "", ""),
 "Servier": ("Watch: large oral-solids and CDMO site with no in-window project found.", "", ""),
 "Novartis": ("Divested. Ringaskiddy API moved to Sterling Pharma Solutions (CDMO); target Sterling instead. Novartis Ireland is now mainly commercial.", "", ""),
 "GSK": ("Divesting. The Cork API plant is being acquired by Thermo Fisher; target Thermo Fisher instead.", "", ""),
 "Roche": ("Not a Roche opportunity. Clarecastle closed in 2016; whoever buys the 88-acre site (first tranche late 2027) could be a greenfield lead from 2027-28.", "", ""),
 "PCI Pharma Services": ("Tier 2 CDMO addition (snippets only). Likely operating now; lifecycle and packaging-line serialization only.", "", ""),
 "West Pharmaceutical Services": ("Component maker for injectables; borderline scope, low priority.", "", ""),
}

# Offering areas and keywords in the research notes that signal them
AREAS = [
 ("SCADA / process control and automation", r"SCADA|automat|OT\b|control system|PLC"),
 ("MES implementation and integration", r"\bMES\b|eBR|batch record|LIMS"),
 ("Digitalization / Industry 4.0", r"digital|Industry 4\.0|\bAI\b|IT/OT|IT-OT|historian|serializ|traceab"),
 ("Validation / CSV / data integrity", r"CSV|validation|CQV|C&Q|Annex|data.integrity|qualification|GAMP"),
 ("Legacy system modernization and migration", r"moderni[sz]|legacy|migration|upgrade"),
 ("Lifecycle support and managed services", r"lifecycle|periodic review|support|optimi[sz]ation|ramp"),
]
GRADE_STRENGTH = {"A+": "Strong", "A": "Strong", "A-": "Strong", "High": "Strong", "B+": "Moderate", "B": "Moderate", "B-": "Moderate",
                  "C+": "Weak", "C": "Weak", "Watch": "Weak", "Neg": "Weak", "Low": "Weak", "-": "Weak"}


def fits(grade, notes, modality, name):
    strength = GRADE_STRENGTH[grade]
    hay = notes + " " + modality
    why_prefix = f"From the Ireland research (plan grade {grade}): " if grade not in ("-", "Neg", "Low", "Watch", "High") else "From the Ireland research notes: "
    reason = why_prefix + re.split(r"(?<=[.!?])\s", notes.strip())[0][:260]
    out = [{"area": a, "strength": strength, "reason": reason} for a, pat in AREAS if re.search(pat, hay, re.I)]
    if not out:
        cap = "Moderate" if strength == "Strong" else strength
        out = [{"area": a, "strength": cap, "reason": reason + " (no specific offering area named)"} for a in (AREAS[3][0], AREAS[5][0])]
    return out[:4]


def sources_for(urls, conf):
    out = []
    for u in [x.strip() for x in re.split(r"\s\|\s", urls) if x.strip()]:
        u = re.sub(r"\s*\(.*$", "", u).strip()
        out.append({"url": u, "publisher": urlparse(u).netloc.replace("www.", ""), "date": "", "confidence": conf})
    return out


def main():
    rows = [r for r in csv.DictReader(open(ROOT / "ireland" / "projects.csv", encoding="utf-8")) if r["Company"].strip()]
    assert len(rows) == len(ROWS), (len(rows), len(ROWS))
    sites, by_company = [], {}
    for i, (r, g) in enumerate(zip(rows, ROWS)):
        lat, lon, county, mods, eur, amount, jobs, status, start, opp, in_win, grade = g
        company = r["Company"]
        by_company.setdefault(company, []).append(r)
        conf = r["Confidence (High/Med/Low)"].strip()
        city = re.sub(r"\s*\(.*?\)", "", r["Site/Location"]).split(" + ")[0].strip()
        scope = f'{r["Project name"]}. Modality: {r["Modality/tech"]}. Manufacturing-related: {r["Manufacturing-related? (Y/N)"]}.'
        sites.append({
            "id": re.sub(r"[^a-z0-9]+", "-", (company + " " + r["Project name"]).lower()).strip("-")[:70],
            "account": company, "site_name": r["Project name"], "city": city, "state": county, "lat": lat, "lon": lon,
            "project_type": "GREENFIELD" if i in GREENFIELD else "BROWNFIELD",
            "modality": mods, "eur": round(eur) if eur else None, "investment_display": amount, "jobs": jobs, "status": status,
            "expected_start": start, "opportunity_status": opp, "in_window": in_win,
            "technical_scope": scope, "orise_fit": fits(grade, r["Notes"], r["Modality/tech"], company),
            "incumbent_vendors": "", "sources": sources_for(r["Source URL(s)"], conf),
            "notes": f'Confidence in research file: {conf}. Status/timeline: {r["Status/timeline"]} Notes: {r["Notes"]}',
            "country": "Ireland", "currency": "USD" if amount.startswith(("About USD", "USD")) else "EUR",
        })
    accounts = []
    for company, rs in by_company.items():
        reason, stack, roles = ACCT[company]
        accounts.append({
            "id": company, "name": company, "priority_tier": f"Tier {TIER[company]}",
            "footprint_summary": "Sites in this research: " + "; ".join(r["Site/Location"] for r in rs) + ".",
            "investment_strategy_summary": " ".join(f'{r["Project name"]}: {r["Investment size (EUR)"]}.' for r in rs),
            "priority_reason": reason, "incumbent_vendors_general": ("From job postings (platform evidence, not a confirmed site stack): " + stack) if stack else "",
            "ownership_note": "", "roles": roles,
        })
    gaps = """<h4 style="margin-top:0">About the Ireland data</h4>
<p>Built from the Ireland research files (29 records, 24 accounts; main pass 2 July 2026, refresh 15 October 2026): <code>ireland/projects.csv</code>, <code>territory-plan.md</code> and <code>sources.md</code>. Amounts, dates, notes and confidence are as written there. The county coordinates, the Orise fit ratings, the opportunity status and the account tiers were added when loading: fit strength follows the plan's overall grade (A+ to A- Strong, B+ to B- Moderate, C and watch Weak) and the areas are matched from the wording of each note. Tiers follow the plan's own groupings (Tier 1 anchors, Tier 2 mid-large, Tier 3 focused builds, Tier 4 watch, divesting or other domain). Open means grades A- to B or a high-fit refresh item; Closed/late marks divested sites and completed pre-window builds.</p>
<ul><li><b>Totals are a floor.</b> The MSD Dundalk figure is an acquisition price; the Pfizer Ringaskiddy facility is part of the €1.2bn package; MSD's network jobs, Novartis, GSK, Roche, Servier, PCI and West have no counted amount. USD amounts are converted at 1 USD = 0.86 EUR.</li>
<li><b>Figures that disagree in the files:</b> Alexion is €65M (IDA) in the plan but a USD 360M programme in the CSV (the €65M is counted); MSD Dundalk is ">€500M" while USD 520M converts to about €447M; Regeneron is €100M confirmed against about €200M reported (€100M counted); Novo Athlone appears as €432M in the plan and as USD 372.5M in one source.</li>
<li><b>Greenfield / brownfield</b> was not in the CSV. I classed Lilly Raheen, Pfizer DS2, Abbott Kilkenny and Astellas as greenfield and everything else as brownfield; check this.</li></ul>
<h4>Gaps and next steps (from the territory plan)</h4>
<ol><li>IDA Ireland press-release pages return 403 to the research tools. Open them in a browser to confirm quotes and figures (Pfizer, Alexion, Novo, MSD, Amgen, Abbott, AbbVie, Astellas).</li>
<li>Alexion APICOM: confirm the April 2026 opening wording and whether the facility is API or biologics drug substance.</li>
<li>Lilly Raheen: confirm whether biologics production started in 2026. Pfizer: confirm the current phase (design, construction or C&amp;Q).</li>
<li>Astellas: automation and MES scope, EPC and integrator, and contacts. The referenced <code>astellas-battlecard.md</code> was not in the files provided.</li>
<li>Planning portals (An Coimisiún Pleanála and the county registers) for J&amp;J Ringaskiddy land, Sanofi Waterford, Pfizer Ringaskiddy and Regeneron's main building.</li>
<li>Add Sterling Pharma Solutions (ex-Novartis Ringaskiddy) and Thermo Fisher (ex-GSK Cork) as formal targets once their modernisation plans are researched. APC (Dublin) and other emerging CDMOs were not found.</li>
<li>Earnings-call transcripts (MSD, Lilly, Pfizer, J&amp;J, Takeda, AbbVie) for Ireland capex commentary; Amgen's ex-Horizon divestment and the Merck KGaA mothballed API plant need site-level clarification.</li>
<li>Decide whether Orise pursues device and diagnostics manufacturing (Abbott €440M) or biopharma GMP only.</li>
<li>Technical buyers (automation and MES managers, CSV leads, historian owners) still need LinkedIn mapping; no emails, phone numbers or LinkedIn URLs were collected.</li></ol>"""
    out = {"accounts": accounts, "sites": sites, "gaps_html": gaps, "as_of": AS_OF, "region_names": COUNTY_NAMES}
    (ROOT / "data" / "ie.json").write_text(json.dumps(out, ensure_ascii=False, indent=0))
    print("ok", len(sites), "sites", len(accounts), "accounts")


main()
