#!/usr/bin/env python3
"""Build data/bx.json (consumed by build.py) from the Benelux research files in this folder.

Inputs : benelux/projects.csv (research output, one row per project), territory-plan.md,
         sources.md, lilly-katwijk-battlecard.md
Output : data/bx.json  (same schema as data/dach.json, data/it.json, data/ie.json)

Nothing here adds facts: amounts, dates, notes, confidence and sources come from projects.csv; priority text,
roles and stack signals come from the territory plan and the Katwijk battlecard. What this script adds: town
coordinates, province codes, short modality tags for the filter, one numeric euro amount per project where the
CSV gives a project-specific figure (otherwise left empty so totals are not inflated), and offering-fit ratings
derived from each row's "Relevant to Orise" note. The UCB Georgia (USA) row is context only and is not loaded.
"""
import csv, json, pathlib, re
from urllib.parse import urlparse

ROOT = pathlib.Path(__file__).resolve().parent.parent
AS_OF = "October 15, 2026"
OPEN, MON, LATE = "OPEN OPPORTUNITY", "Monitor", "Closed/late"
USD = 0.86  # EUR per USD, same rate as the rest of the dashboard

# One tuple per CSV data row (the UCB Georgia row is dropped first), in file order:
# (lat, lon, province, country, [modality tags], eur|None, amount text, jobs|None, status, start, opportunity, in_window)
ROWS = [
 (50.72, 4.61, "BE-WBR", "Belgium", ["lyophilised vaccines"], 250e6, "€250 million+ (announced Aug 2023)", None, "under construction", "Construction launched Aug 2023; operational H1 or H2 2027 (sources differ); status after the Oct 2026 restructuring not reported", OPEN, True),
 (50.71, 4.53, "BE-WBR", "Belgium", ["vaccine clinical laboratory"], 150e6, "€150 million building plus unspecified automated equipment", None, "operational", "Inaugurated 9 Jun 2026", MON, True),
 (50.72, 4.61, "BE-WBR", "Belgium", ["restructuring (not capex)"], None, "n/a (up to 1,217 jobs threatened)", None, "announced", "Works council 14 Oct 2026; unions blocked Rixensart and Wavre from 15 Oct", MON, True),
 (51.07, 4.29, "BE-VAN", "Belgium", ["sterile fill-finish (isolators)", "mRNA cold storage", "packaging"], 1.2e9, "€1.2 billion+ (announced 8 Dec 2022, over three years)", 250, "under construction", "Three-year programme from Dec 2022; completion by module not found", OPEN, None),
 (51.07, 4.30, "BE-VAN", "Belgium", ["production support (not stated)"], None, "Not found in public sources", None, "announced", "Zoning (RUP) approval hoped for by end 2026", MON, True),
 (51.32, 4.86, "BE-VAN", "Belgium", ["API (Geel)", "drug product (Beerse)"], None, "Not found in public sources for 2026-27 (past: Geel pilot plant €130M, Beerse line €21M)", None, "Not found in sources", "No in-window project found", MON, False),
 (51.65, 5.95, "NL-NB", "Netherlands", ["animal vaccines and medicines (formulation and filling)"], None, "Not disclosed", 80, "under construction", "Kickoff 27 Mar 2025; about three years (~2028); QC lab handed over Apr 2026", OPEN, True),
 (51.76, 5.52, "NL-NB", "Netherlands", ["biotech / oncology (divested)"], None, "n/a (sold to Organon)", None, "divested", "Sale announced 1 Oct 2024; MSD production closed 1 Jul 2025", LATE, False),
 (50.68, 4.37, "BE-WBR", "Belgium", ["gene therapy (clinical production, fill-finish)"], 200e6, "€200 million+", 150, "commissioning", "Inaugurated 24 Apr 2026; first production 2026 or first batches 2027 (sources differ)", OPEN, True),
 (50.68, 4.37, "BE-WBR", "Belgium", ["R&D centre"], None, "€100M or €200M (sources differ; not counted)", 170, "under construction", "Completion 2028", MON, True),
 (50.68, 4.37, "BE-WBR", "Belgium", ["biologics (3 x 10,000 L bioreactors)"], 300e6, "€300 million", 150, "operational", "Inaugurated 26 Apr 2024; room for three more bioreactors (undated)", MON, False),
 (51.02, 3.71, "BE-VOV", "Belgium", ["biologics (outsourced manufacturing)"], None, "n/a (no plant)", None, "n/a", "Lab and office leases only", LATE, False),
 (52.18, 4.42, "NL-ZH", "Netherlands", ["oral solid dose (incl. spray-dried dispersion)"], 2.6e9, "€2.6 billion (about USD 3bn)", 500, "announced", "Announced 3 Nov 2025; council approval 1 Oct 2026; main construction planned autumn 2026; first medicines hoped for 2030; production and wastewater permits pending", OPEN, True),
 (50.71, 3.83, "BE-WHT", "Belgium", ["plasma-derived therapies"], 300e6, "About €300 million (announced 16 Sep 2022)", None, "under construction", "Full production planned by end 2026 (2022 plan); 2025-26 status not found; Renault procedure Apr 2026", OPEN, True),
 (52.18, 4.47, "NL-ZH", "Netherlands", ["CAR-T cell therapy"], None, "Not found in public sources", None, "operational", "Commercial CAR-T for European patients since about Mar 2026", MON, False),
 (52.70, 6.19, "NL-DR", "Netherlands", ["solid dosage forms (tablets, capsules, pellets)"], None, "Not found in public sources", None, "divested", "Astellas announced the sale 25 May 2023; Delpharm release 2 Apr 2024", MON, False),
 (51.16, 4.99, "BE-VAN", "Belgium", ["biologics (hemophilia)"], 120e6, "€120 million (Oct 2022, line due 2024); earlier €300M", None, "operational", "Line due 2024; nothing newer found", MON, False),
 (51.59, 4.78, "NL-NB", "Netherlands", ["biologics packaging / distribution"], None, "Not found in public sources", None, "n/a", "No Dutch capital plan found", LATE, False),
 (50.48, 4.55, "BE-WHT", "Belgium", ["radiopharmaceuticals (CDMO)"], None, "Not found in public sources", None, "under construction", "Hot cells installed early 2027; operational H2 2027", OPEN, True),
 (51.19, 5.12, "BE-VAN", "Belgium", ["actinium-225 (alpha therapy isotope)"], None, "Not found in public sources (€93M Series A, not counted)", None, "under construction", "Operational 2028, commercial supply 2029", OPEN, True),
 (50.60, 5.46, "BE-WLG", "Belgium", ["radiopharmaceuticals"], None, "Not disclosed (acquisition); strategic plan about €40M", 300, "announced", "Announced 19 May 2026; first move-in early 2027; 300 jobs by 2030", OPEN, True),
 (51.05, 3.72, "BE-VOV", "Belgium", ["CAR-T cell therapy (Carvykti)"], 150e6 * USD, "About USD 150 million additional (approved 2025)", None, "announced", "Construction slated H2 2025, completion 2028; 2026 status not confirmed", OPEN, True),
 (52.16, 4.49, "NL-ZH", "Netherlands", ["CAR-T cell therapy (closing)"], None, "n/a (€275M impact booked in 2025)", None, "closing", "Wind-down decided Jan 2026; substantially complete by end Q3 2026", LATE, False),
 (50.45, 4.44, "BE-WHT", "Belgium", ["bioprocess technology, cell and gene CDMO"], None, "n/a (group bankrupt Oct 2025)", None, "bankrupt", "Univercells bankrupt Oct 2025; fate of the Jumet GMP site unknown", LATE, False),
 (51.76, 5.52, "NL-NB", "Netherlands", ["API / pharmaceutical products (lab move)"], None, "Not found in public sources", None, "announced", "Letter of intent with Pivot Park; first staff mid-2027 if on plan", MON, None),
 (51.93, 4.58, "NL-ZH", "Netherlands", ["pharmaceutical compounding / sterile preparations"], None, "About €70 million for 2026 (US and Netherlands combined; not counted)", None, "announced", "Q3 2026 report; named projects are in the US", MON, True),
 (51.84, 5.86, "NL-GE", "Netherlands", ["generics"], None, "Not found in public sources", None, "Not found in sources", "No current project found (the only article is from 2016)", LATE, False),
 (51.00, 3.88, "BE-VOV", "Belgium", ["API / chemistry", "medical devices (Terumo)", "antibiotic API (Centrient)"], None, "Not found in public sources", None, "Not found in sources", "No 2026-27 project found for Ajinomoto, Terumo or Centrient", LATE, False),
]

PROVINCE_NAMES = {"BE-WBR": "Walloon Brabant", "BE-VAN": "Antwerp", "BE-WHT": "Hainaut", "BE-WLG": "Liège", "BE-VOV": "East Flanders",
                  "NL-ZH": "South Holland", "NL-NB": "North Brabant", "NL-DR": "Drenthe", "NL-GE": "Gelderland"}

# Account names (the CSV 'Company' column is kept in each site's notes)
NAMES = {"Johnson & Johnson (Innovative Medicine)": "Johnson & Johnson (Innovative Medicine)", "MSD (human health)": "MSD", "MSD Animal Health": "MSD Animal Health",
         "Astellas / Delpharm": "Delpharm (ex-Astellas Meppel)", "IRE (Institut National des Radioéléments)": "IRE", "PanTera (IBA / SCK CEN joint venture)": "PanTera",
         "Legend Biotech / Johnson & Johnson": "Legend Biotech", "Univercells / Exothera / Quantoom": "Univercells", "Aspen Oss": "Aspen",
         "Ajinomoto Bio-Pharma (OmniChem) / Terumo / Centrient": "Ajinomoto Bio-Pharma"}

# (priority reason from the territory plan, stack signals, public roles)
ACCT = {
 "Eli Lilly": ("Rank 0. Largest Benelux greenfield: a €2.6bn oral-medicines plant at Katwijk, with permits and a nitrogen-permit appeal as the timing risk. Start-up roles (OT/IT integration, QA/CSV, IT readiness) are already advertised, so engage while the OT/IT and CSV strategy is being set. See lilly-katwijk-battlecard.md.",
               "From job postings (a hypothesis, not confirmed for Katwijk): corporate postings name Emerson DeltaV; Ireland sites run DeltaV, Syncade and PI. Katwijk posts name DCS, SCADA, MES, historians, PLCs, GAMP 5 and data integrity. Developer RED Company; architect Powerhouse Company; permit consultant DGMR; Jacobs engineering unconfirmed; main contractor and automation integrator not public.",
               "Marco Frenken, general manager / country manager, Lilly Nederland (titles vary by outlet). Nanne de Ru, owner of RED Company (developer). Katwijk site leader, engineering, automation, MES/IT and CSV leads not found publicly."),
 "Takeda": ("Rank 0b. Plasma plant start-up due around end 2026, so CQV, MES and digital integration are due now. At risk: the Renault restructuring (109 jobs, April 2026); confirm who owns the project.", "", ""),
 "IRE": ("Tier 2, rank 1. Company-confirmed GMP radiopharma CDMO: hot cells early 2027, operational H2 2027, so qualification follows within about 12 months. No investment figure.", "",
         "Erich Kollegger, CEO (quoted in the release)."),
 "Legend Biotech": ("Tier 2, rank 2. CAR-T capacity in Ghent to 2028. Confirm the 2026 status of the USD 150M project and how funds are split with J&J.", "", ""),
 "Trasis": ("Tier 2, rank 3. An existing GMP site (former Mithra) being adapted for radiopharma; move-in early 2027. New logo.", "", ""),
 "PanTera": ("Tier 2, rank 4. Actinium-225 plant under construction with permits granted; operational 2028. Permit dates conflict (2025 vs April 2026).", "", ""),
 "UCB": ("Rank 1. Genesis is a new gene-therapy GMP site with a fully robotised filling line and a real-time digital ecosystem; first batches 2026-27, so CQV, MES/eBR and data integrity are live. Arkelia (R&D) and spare bioreactor capacity follow. UCB's biggest new capacity is in the US (USD 2bn, Georgia), which may slow further Belgian adds.", "", ""),
 "GSK": ("Rank 2, at risk. NewLyo (€250M+, freeze-dried vaccines, operational 2027) is exactly Orise's scope, but on 14 Oct 2026 GSK told its works council up to 1,217 Belgian jobs are threatened, and a new CEO reportedly wants only one vaccine among 5-6 priorities. Confirm NewLyo status before investing pursuit effort.", "", ""),
 "Pfizer": ("Rank 3. €1.2bn programme (isolators, mRNA freezer warehouse, packaging) announced Dec 2022 should be in late delivery. Next signal is the 7.5 ha land extension (zoning decision due end 2026).", "", ""),
 "MSD Animal Health": ("Rank 4. Animal-vaccine formulation and filling facility (kickoff March 2025, about three years) with digitalisation and automation stated. Animal health, so confirm it fits Orise's scope.", "",
                       "Darcio Santos, site director (quoted March 2025; verify tenure)."),
 "MSD": ("Divested: the Oss plant was sold to Organon and MSD production closed 1 July 2025. The opportunity moves to Organon; its plans are not found.", "", ""),
 "Johnson & Johnson (Innovative Medicine)": ("Rank 8, watch. Strong digital history (Factory of the Future) but nothing in window found at Beerse or Geel. Dutch-language local press is poorly indexed, so absence is not proof.", "", ""),
 "argenx": ("Rank 9. No manufacturing plant (outsourced); only a possible LIMS or GxP lab-systems angle.", "", ""),
 "Bristol Myers Squibb": ("Built and producing CAR-T commercially, so lifecycle, periodic review, data integrity and MES/eBR optimisation rather than a new build.", "", ""),
 "Delpharm (ex-Astellas Meppel)": ("Same pattern as Oss and Ireland: pursue the CDMO acquirer. Delpharm's plans for the Meppel site are not found.", "", ""),
 "Sanofi": ("Watch: no 2026-27 project found at Geel.", "", ""),
 "Amgen": ("Breda is a packaging and distribution hub; no Dutch capital plan found.", "", ""),
 "Galapagos": ("Closing its Leiden cell-therapy site; possible opportunity only if the GMP assets are sold.", "", ""),
 "Univercells": ("Bankrupt in Oct 2025 (Exothera, Jumet GMP site); watch for a buyer of the site.", "", ""),
 "Aspen": ("Lab consolidation in the Pivot Park 'Hodgkin' building implies LIMS and lab-systems migration; first staff mid-2027 if on plan. Article dates unverified.", "", ""),
 "Fagron": ("Compounding and sterile services; named 2026 projects are in the US.", "", ""),
 "Synthon": ("No current project. A first search summary suggested one, but the fetched article is from 2016.", "", ""),
 "Ajinomoto Bio-Pharma": ("No in-window project found for Ajinomoto (Wetteren), Terumo (Leuven) or Centrient (Delft).", "", ""),
}

AREAS = [
 ("SCADA / process control and automation", r"SCADA|automat|OT\b|control system|PLC|robot"),
 ("MES implementation and integration", r"\bMES\b|eBR|batch record|LIMS"),
 ("Digitalization / Industry 4.0", r"digital|Industry 4\.0|\bAI\b|IT/OT|IT-OT|historian|serializ|traceab"),
 ("Validation / CSV / data integrity", r"CSV|validation|CQV|C&Q|Annex|data.integrity|qualification|GAMP"),
 ("Legacy system modernization and migration", r"moderni[sz]|legacy|migration|upgrade"),
 ("Lifecycle support and managed services", r"lifecycle|periodic review|support|optimi[sz]ation|ramp"),
]
STRENGTH = {"High": "Strong", "Med-High": "Moderate", "Med": "Moderate", "Low-Med": "Weak", "Low": "Weak"}


def relevance_level(text):
    m = re.match(r"\s*(High|Med-High|Low-Med|Med|Low|Out of scope)\b", text)
    return m.group(1) if m else "Low"


def fits(rel, digital):
    level = relevance_level(rel)
    strength = STRENGTH.get(level, "Weak")
    hay = rel + " " + (digital if not digital.lower().startswith(("not found", "none", "not mentioned", "n/a", "not applicable")) else "")
    reason = "From the Benelux research notes: " + rel.split(" - ", 1)[-1].strip()
    out = [{"area": a, "strength": strength, "reason": reason} for a, pat in AREAS if re.search(pat, hay, re.I)]
    if not out:  # no offering area named: general fit, capped at Moderate
        cap = "Moderate" if strength == "Strong" else strength
        out = [{"area": a, "strength": cap, "reason": reason + " (no specific offering area named)"} for a in (AREAS[3][0], AREAS[5][0])]
    return out[:4]


def sources_for(urls, conf):
    out = []
    for u in [x.strip() for x in re.split(r"\s;\s|;\s(?=https?)", urls) if x.strip()]:
        u = re.sub(r"\s*\(.*$", "", u).strip()
        out.append({"url": u, "publisher": urlparse(u).netloc.replace("www.", ""), "date": "", "confidence": conf})
    return out


def main():
    rows = [r for r in csv.DictReader(open(ROOT / "benelux" / "projects.csv", encoding="utf-8")) if r["Company"].strip() and "Gwinnett" not in r["Site/Location (city, country)"]]
    assert len(rows) == len(ROWS), (len(rows), len(ROWS))
    sites, by_company = [], {}
    for r, g in zip(rows, ROWS):
        lat, lon, prov, country, mods, eur, amount, jobs, status, start, opp, in_win = g
        company = NAMES.get(r["Company"], r["Company"])
        by_company.setdefault(company, []).append(r)
        conf = r["Confidence (High/Med/Low)"].strip()
        gb = r["Greenfield / Brownfield"].strip()
        city = re.sub(r"\s*\(.*?\)", "", r["Site/Location (city, country)"]).split(", ")[0].strip()
        scope = f'{r["Project name"]}. Modality: {r["Modality/tech"]}. Digital / automation signals: {r["Digital/automation signals"]}.'
        sites.append({
            "id": re.sub(r"[^a-z0-9]+", "-", (company + " " + r["Project name"]).lower()).strip("-")[:70],
            "account": company, "site_name": r["Project name"], "city": city, "state": prov, "lat": lat, "lon": lon,
            "project_type": "GREENFIELD" if gb.lower().startswith("greenfield") else "BROWNFIELD", "modality": mods,
            "eur": round(eur) if eur else None, "investment_display": amount, "jobs": jobs, "status": status,
            "expected_start": start, "opportunity_status": opp, "in_window": in_win,
            "technical_scope": scope, "orise_fit": fits(r["Relevant to Orise? (High/Med/Low + why)"], r["Digital/automation signals"]),
            "incumbent_vendors": "", "sources": sources_for(r["Source URL(s)"], conf),
            "notes": f'Confidence in research file: {conf}. Company in research file: {r["Company"]}. Status/timeline: {r["Status/timeline"]} Notes: {r["Notes"]} Greenfield/brownfield in research file: {gb}.',
            "country": country, "currency": "USD" if amount.startswith("About USD") else "EUR",
        })
    accounts = []
    for company, rs in by_company.items():
        reason, stack, roles = ACCT[company]
        tier = re.match(r"\s*(\d)", rs[0]["Tier (1/2)"]).group(1)
        accounts.append({
            "id": company, "name": company, "priority_tier": f"Tier {tier}",
            "footprint_summary": "Sites in this research: " + "; ".join(r["Site/Location (city, country)"] for r in rs) + ".",
            "investment_strategy_summary": " ".join(f'{r["Project name"]}: {r["Investment size (EUR)"].strip()}.' for r in rs),
            "priority_reason": reason, "incumbent_vendors_general": stack, "ownership_note": "", "roles": roles,
        })
    gaps = """<h4 style="margin-top:0">About the Benelux data</h4>
<p>Built from the Benelux research files (28 records on the map, 23 accounts, researched 15 October 2026): <code>benelux/projects.csv</code>, <code>territory-plan.md</code>, <code>sources.md</code> and <code>lilly-katwijk-battlecard.md</code>. Amounts, dates, notes and confidence are as written there. The town coordinates, the Orise fit ratings and the opportunity status were added when loading: fit areas are matched from the wording of each row's "Relevant to Orise" note and the strength follows its High / Med / Low rating. Open means High and Med-High in or near the window; Monitor means Med, Low and watch items; Closed/late means divested, closed or bankrupt sites and nothing in window. No project was found in Luxembourg.</p>
<ul><li><b>Totals are a floor.</b> Many projects have no disclosed amount (MSD Boxmeer, IRE, PanTera, Trasis). UCB Arkelia is €100M or €200M depending on the source, so neither is counted; Fagron's €70M is US and Netherlands combined; Galapagos's €275M is a wind-down charge, not capex. USD amounts are converted at 1 USD = 0.86 EUR.</li>
<li><b>Left out:</b> the UCB US biologics campus (Georgia, USD 2bn) is in the CSV as context only and is not shown or counted.</li>
<li><b>Dates that differ by source:</b> GSK NewLyo operational H1 or H2 2027; UCB Genesis first production 2026 or first batches 2027; Lilly Katwijk's municipality says the building permit is granted while press says permits are still missing (these are different permits: building, nature, environmental and water); PanTera permits dated 2025 or April 2026; BMS Leiden completion 2024 or 2025.</li>
<li><b>Greenfield / brownfield</b> follows the CSV: Lilly Katwijk, BMS Leiden, PanTera and the Pfizer Puurs land are greenfield; the Chiesi-style conversions and expansions are brownfield. Rows with no project (n/a) default to brownfield.</li>
<li><b>Account merging:</b> MSD and MSD Animal Health share the existing "Merck &amp; Co." card; J&amp;J Innovative Medicine shares the J&amp;J card; Astellas Meppel is shown under its new owner Delpharm.</li></ul>
<h4>Gaps and next steps (from the territory plan)</h4>
<ol><li>GSK Wavre: confirm NewLyo schedule and scope after the 14 Oct 2026 works council; watch the final social plan and any pause.</li>
<li>UCB: resolve Arkelia €100M vs €200M and Genesis first-batch timing.</li>
<li>Pfizer Puurs: find which isolator and freezer modules are complete; watch the RUP outcome and the Omgevingsloket.</li>
<li>MSD Boxmeer: investment amount and contractors. MSD Oss: Organon's plans. J&amp;J: Belgian press room and Omgevingsloket; check the reported Ghent cell-therapy site.</li>
<li>Permitting: Omgevingsloket (Flanders), permis unique (Wallonia), officielebekendmakingen.nl (NL) and Luxembourg commodo-incommodo were not reachable by the research tools; a browser is needed.</li>
<li>Lilly Katwijk: permit decision (gmb-2026-471169) and appeal deadlines, the nitrogen-permit appeal, the main contractor and EPCM, and site leadership. The battlecard refers to <code>ireland/lilly-battlecard.md</code>; that Ireland battlecard was not in the files provided.</li>
<li>Takeda Lessines: is the new plant operating? Delpharm Meppel and Organon Oss: new owners' plans. IRE and Trasis: project values and automation scope. Legend: 2026 capex status. Galapagos Leiden and Univercells Jumet: buyers of the sites.</li>
<li>Baxter, Novartis, AbbVie, AstraZeneca, Roche: nothing found in Belgium or the Netherlands; re-check with paid tools or company contact. Rousselot and Eurofins Luxembourg: nothing found.</li>
<li>Agencies and trade press (FIT, AWEX, BioWin, NFIA, pharma.be, BioVox) were not read. Tech stacks and contacts beyond Lilly Katwijk are not researched; no emails, phone numbers or LinkedIn URLs were collected.</li></ol>"""
    out = {"accounts": accounts, "sites": sites, "gaps_html": gaps, "as_of": AS_OF, "region_names": PROVINCE_NAMES}
    (ROOT / "data" / "bx.json").write_text(json.dumps(out, ensure_ascii=False, indent=0))
    print("ok", len(sites), "sites", len(accounts), "accounts")


main()
