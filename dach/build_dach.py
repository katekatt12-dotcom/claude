# -*- coding: utf-8 -*-
"""Builds the DACH dashboard HTML, CSV and sources file from dach_data.py, reusing the US dashboard as the template."""
import json, csv, os, sys, collections
sys.path.insert(0, os.path.dirname(__file__))
import dach_data as D

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE = os.path.join(ROOT, "Orise-US-Pharma-Investment-Dashboard.html")
OUT_HTML = os.path.join(ROOT, "Orise-DACH-Pharma-Investment-Dashboard.html")
OUT_CSV = os.path.join(ROOT, "dach-projects-2026-10.csv")
OUT_SRC = os.path.join(ROOT, "dach-sources-2026-10.md")

RATE = {"EUR": 1.0, "CHF": D.CHF_EUR, "USD": D.USD_EUR}
COUNTRY = {"DE": "Germany", "AT": "Austria", "CH": "Switzerland"}

sites = []
for s in D.S:
    x = dict(s)
    x["country"] = COUNTRY[s["state"][:2]]
    x["eur"] = round(s["investment"] * RATE[s["currency"]]) if s["investment"] else None
    sites.append(x)

# ---- accounts, with tiers computed from the data ----
by_acc = collections.defaultdict(list)
for s in sites: by_acc[s["account"]].append(s)
W = {"Strong": 3, "Moderate": 2, "Weak": 1}
accounts = []
for (aid, name, grp, _tier, own, foot, strat, reason) in D.ACCOUNTS:
    ss = by_acc.get(aid, [])
    opens = [s for s in ss if s["opportunity_status"] == "OPEN OPPORTUNITY"]
    win_open = [s for s in opens if s["in_window"]]
    strong_win = [s for s in win_open if any(f["strength"] == "Strong" for f in s["orise_fit"])]
    if strong_win: tier = "Tier 1"
    elif opens or any(s["opportunity_status"] == "Monitor" and any(f["strength"] in ("Moderate", "Strong") for f in s["orise_fit"]) for s in ss): tier = "Tier 2"
    else: tier = "Tier 3"
    rule = (f"{len(opens)} open opportunit{'y' if len(opens)==1 else 'ies'}, {len(win_open)} in the 2026-27 window, "
            f"{len(strong_win)} with a Strong fit. ")
    accounts.append(dict(id=aid, name=name, group=grp, ownership_note=own, footprint_summary=foot,
        investment_strategy_summary=strat, priority_tier=tier, priority_reason=rule + reason, incumbent_vendors_general=""))
tier_order = {"Tier 1": 0, "Tier 2": 1, "Tier 3": 2}

# ---- gaps / methodology ----
n_open = sum(1 for s in sites if s["opportunity_status"] == "OPEN OPPORTUNITY")
skipped = "".join(f"<li><b>{k}</b> &mdash; {v}</li>" for k, v in D.SKIPPED.items())
zero = [a["name"] for a in accounts if not by_acc.get(a["id"])]
GAPS = f"""
<h4 style="margin-top:0;">How this dashboard was built</h4>
<p>This is a fresh research pass (7 Oct 2026) on the listed accounts using web search across company newsrooms, wire services, regional business and trade press, and state/cantonal investment agencies, in German and English. Each record carries source links and a confidence rating (High = company or official source; Medium = reputable trade or regional press; Low = single or undated/indirect source). The layout, filters, fit-matrix logic and record structure follow the US dashboard.</p>
<h4>Known limitations &mdash; please read</h4>
<ul>
<li><b>Search-synthesis only.</b> This build could not open primary documents (annual reports, press-release PDFs, Handelsregister, state-aid decisions). Facts come from search-result summaries and snippets, so most items are Medium/Low confidence and many <b>dates are &ldquo;Unverified&rdquo;</b>. Confirm before customer-facing use.</li>
<li><b>Reference files not available.</b> The earlier DACH CSV/sources/territory plan, the earlier DACH dashboard, the corrected US CSV and the PowerPoint template were not in this build environment, so nothing from the earlier DACH research was reused and brand colours/fonts are taken from the US dashboard's CSS. The official Orise logo (black wordmark, inverted to white on the teal header) is embedded.</li>
<li><b>Currencies.</b> Amounts are shown in the announcement currency (EUR, CHF; two Novartis items are announced in USD). The KPI row shows EUR, CHF and USD totals separately. Only the map shading by &ldquo;Investment&rdquo; converts to euro-equivalents using <b>indicative planning rates of 1 CHF = {D.CHF_EUR} EUR and 1 USD = {D.USD_EUR} EUR (set 7 Oct 2026, not live market rates)</b>; replace them in <code>dach_data.py</code> if needed.</li>
<li><b>Totals are a floor.</b> {sum(1 for s in sites if not s['investment'])} of {len(sites)} records have no disclosed amount; network programmes (e.g. Bayer &gt;EUR 1.4B, Roche CHF 1.2B Basel programme) are not split across sites. Several records bundle older projects (pre-2024) kept for footprint context and marked Monitor / Closed.</li>
<li><b>Inferred figure.</b> Lilly Alzey (EUR ~1.15B) is inferred as half of the original EUR 2.3B after a reported 2026 cut; confirm directly.</li>
<li><b>Greenfield vs brownfield.</b> Greenfield = new stand-alone site or plant on previously undeveloped land; brownfield = new building, line or expansion at an existing site.</li>
<li><b>Opportunity status.</b> Open = in design, build, commissioning or ramp-up with a clear automation/MES need; Monitor = completed, R&amp;D/non-manufacturing or too early; Closed/late = completed before the window, or site closure. The &ldquo;2026-27 window&rdquo; flag marks projects with construction, commissioning or start-up in 2026-2027.</li>
<li><b>Tiers are computed:</b> Tier 1 = at least one open opportunity in the 2026-27 window with a Strong fit; Tier 2 = other open opportunities or Monitor items with Moderate fit; Tier 3 = none identified. Fit ratings are analyst judgement from project scope, not confirmed buying intent. Incumbent vendors were not researched (empty).</li>
<li><b>Coordinates</b> are city-level approximations.</li>
<li><b>Map.</b> Equal-size tiles for 16 German L&auml;nder, 9 Austrian Bundesl&auml;nder and 26 Swiss cantons (Liechtenstein: no site).</li>
</ul>
<h4>Ownership and structure checks</h4>
<ul>
<li><b>Sandoz</b> is a standalone company since the Oct 2023 spin-off from Novartis; <b>Hexal</b> is a Sandoz subsidiary and its Holzkirchen record sits under Sandoz.</li>
<li><b>MSD</b> is Merck &amp; Co. (USA) outside North America, including Intervet/Animal Health, and is unrelated to <b>Merck KGaA</b> (Darmstadt; EMD in the US).</li>
<li><b>Catalent</b> is owned by Novo Holdings (deal closed Dec 2024). <b>BioNTech</b> absorbed CureVac. <b>Bode Chemie</b> belongs to PAUL HARTMANN AG (bought from Beiersdorf). <b>KBI Biopharma</b> is a JSR company. <b>Takeda</b> acquired Shire/Baxalta plasma assets (Vienna, Linz).</li>
</ul>
<h4>Accounts with no project found in this pass</h4>
<ul><li>{', '.join(zero)}</li></ul>
<h4>Group C accounts skipped (no DACH manufacturing or R&amp;D site found)</h4>
<ul>{skipped}</ul>
<h4>Notable thin or negative signals</h4>
<ul>
<li><b>Boehringer Ingelheim</b> froze EUR 900M of German investments for 2027-30 (June 2026). <b>Eli Lilly</b> halved the Alzey plan. <b>Pfizer</b> says German investment is under review. <b>BioNTech</b> is closing three German sites; <b>GSK</b> is closing Dresden; <b>Novartis</b> is ending solid-dose production in Stein by end-2027. Expect German health-cost measures to keep affecting site decisions.</li>
<li><b>Roche Kaiseraugst</b> CHF 500M+ headline and <b>Merck KGaA</b> Darmstadt QC building could not be confirmed beyond a single headline each.</li>
<li><b>Takeda</b> Oranienburg, <b>Octapharma</b> Dessau/Springe, <b>Fresenius Kabi</b> Friedberg/Oberdorf, <b>CordenPharma</b> Plankstadt, <b>Abbott</b>, <b>Gr&uuml;nenthal</b> and <b>AstraZeneca</b> Wedel: no investment found &mdash; absence in this pass is not proof of absence.</li>
</ul>
"""

# ---------------- HTML ----------------
html = open(TEMPLATE, encoding="utf-8").read()
lines = html.split("\n")

def jd(o): return json.dumps(o, ensure_ascii=False)
def replace_line(prefix, new):
    for i, l in enumerate(lines):
        if l.startswith(prefix):
            lines[i] = new; return
    raise SystemExit("missing line " + prefix)

replace_line("const ACCOUNTS =", "const ACCOUNTS = " + jd(accounts) + ";")
replace_line("const SITES =", "const SITES = " + jd(sites) + ";")
replace_line("const GAPS_HTML =", "const GAPS_HTML = " + jd(GAPS) + ";")
replace_line("const AS_OF =", f'const AS_OF = "{D.AS_OF}";')
replace_line("const STATE_GRID =", "const STATE_GRID = " + jd(D.GRID) + ";\nconst CHF_EUR = %s, USD_EUR = %s;" % (D.CHF_EUR, D.USD_EUR))
replace_line("const STATE_NAMES =", "const STATE_NAMES = " + jd(D.REGIONS) + ";")
html = "\n".join(lines)

def rep(old, new, count=None):
    global html
    n = html.count(old)
    if n == 0: raise SystemExit("not found: " + old[:80])
    if count is not None and n != count: raise SystemExit(f"count {n} != {count}: " + old[:80])
    html = html.replace(old, new)

# titles / copy
rep("<title>Orise US Pharma Investment Dashboard</title>", "<title>Orise DACH Pharma Investment Dashboard</title>")
rep("<h1>US Pharma Investment Landscape</h1>", "<h1>DACH Pharma Investment Landscape</h1>")
rep("Manufacturing capital projects across 25 target accounts &mdash; where Orise's automation, MES and digitalization offerings fit.",
    f"Germany, Austria and Switzerland: manufacturing capital projects across {len(accounts)} target accounts &mdash; where Orise's automation, MES and digitalization offerings fit.")
rep("<h2>US Investment Map</h2>", "<h2>DACH Investment Map</h2>")
rep("State tiles shaded by pharma manufacturing activity. Each state is shown as an equal-size tile (grid map) so small but strategically important states remain easy to see and click. Click a state for its site list, or click a marker for full opportunity detail.",
    "Tiles for the 16 German L&auml;nder, 9 Austrian Bundesl&auml;nder and 26 Swiss cantons, shaded by pharma manufacturing activity. Equal-size tiles keep small cantons and city-states easy to see and click. Click a tile for its site list; investment shading uses euro-equivalents at indicative rates (1 CHF = " + str(D.CHF_EUR) + " EUR, 1 USD = " + str(D.USD_EUR) + " EUR; see Methodology).")
rep('<button class="seg-btn" data-shade="investment">Investment $</button>', '<button class="seg-btn" data-shade="investment">Investment (&euro;-equiv.)</button>')
rep("US manufacturing footprint, capital projects and Orise entry points for each of the 25 target accounts.", "DACH manufacturing footprint, capital projects and Orise entry points for each target account (including accounts with no project found).")
rep("<h3>Select a state or marker</h3>", "<h3>Select a region or marker</h3>")
rep("Hover a tile for a quick summary, or click a tile to see its sites and opportunities here.", "Hover a tile for a quick summary, or click a tile to see its sites and opportunities here.")
rep("placeholder=\"Search account, site, city, state, modality...\"", "placeholder=\"Search account, site, city, region, country, modality...\"")

# filters
rep('<div class="msel" data-filter="state"><button class="msel-btn" type="button">State</button><div class="msel-panel"></div></div>',
    '<div class="msel" data-filter="country"><button class="msel-btn" type="button">Country</button><div class="msel-panel"></div></div>\n      <div class="msel" data-filter="state"><button class="msel-btn" type="button">Region (Land / Kanton)</button><div class="msel-panel"></div></div>\n      <div class="msel" data-filter="window"><button class="msel-btn" type="button">2026&ndash;27 window</button><div class="msel-panel"></div></div>')
rep("offering_area:new Set(), state:new Set() };", "offering_area:new Set(), state:new Set(), country:new Set(), window:new Set() };")
rep("  if(filters.state.size && !filters.state.has(s.state)) return false;",
    "  if(filters.state.size && !filters.state.has(s.state)) return false;\n  if(filters.country.size && !filters.country.has(s.country)) return false;\n  if(filters.window.size && !filters.window.has(s.in_window?'yes':'no')) return false;")
rep("    state: [...new Set(SITES.map(s=>s.state))].sort().map(v=>({v,l:(STATE_NAMES[v]||v)+\" (\"+v+\")\"}))",
    "    state: [...new Set(SITES.map(s=>s.state))].sort().map(v=>({v,l:(STATE_NAMES[v]||v)+\" (\"+v+\")\"})),\n    country: [\"Germany\",\"Austria\",\"Switzerland\"].map(v=>({v,l:v})),\n    window: [{v:\"yes\",l:\"In 2026\\u201327 window\"},{v:\"no\",l:\"Outside window\"}]")

# money helpers
rep("const fmtUSD = n => {", """const CUR_SYM = {EUR:"\\u20ac", CHF:"CHF ", USD:"$"};
const fmtAmt = (n,cur) => {
  if(n===null||n===undefined||isNaN(n)) return "\\u2014";
  const p = CUR_SYM[cur]||"";
  if(n>=1e9) return p+(n/1e9).toFixed(n%1e9===0?0:2).replace(/\\.?0+$/,"")+"B";
  if(n>=1e6) return p+(n/1e6).toFixed(n%1e6===0?0:1).replace(/\\.0$/,"")+"M";
  if(n>=1e3) return p+(n/1e3).toFixed(0)+"K";
  return p+n;
};
const fmtMoney = s => (s.investment===null||s.investment===undefined) ? "n/d" : fmtAmt(s.investment, s.currency);
const regName = c => STATE_NAMES[c] || c;
const regShort = c => String(c).split("-")[1];
const fmtUSD = n => {""")
rep("fmtUSD(s.investment_usd)", "fmtMoney(s)")
rep("fmtUSD(r.investment_usd)", "fmtMoney(r)")
rep("fmtUSD(st.invest)", "fmtAmt(st.invest,'EUR')+' (\\u20ac-equiv.)'")
rep("esc(s.investment_display) || fmtUSD(s.investment_usd)", "esc(s.investment_display) || fmtMoney(s)") if "esc(s.investment_display) || fmtUSD(s.investment_usd)" in html else None
rep("(typeof s.investment_usd==='number'?s.investment_usd:0)", "(typeof s.eur==='number'?s.eur:0)") if "(typeof s.investment_usd==='number'?s.investment_usd:0)" in html else None
rep("sum+(typeof s.investment_usd==='number'?s.investment_usd:0)", "sum+(typeof s.eur==='number'?s.eur:0)") if "sum+(typeof s.investment_usd==='number'?s.investment_usd:0)" in html else None

# regions in text
rep("${esc(s.city)}, ${esc(s.state)}", "${esc(s.city)}, ${esc(regName(s.state))}")
rep("${esc(s.site_name)}, ${esc(s.city)} ${esc(s.state)}", "${esc(s.site_name)}, ${esc(s.city)} (${esc(regName(s.state))})")
rep("<td>${esc(s.state)}</td>", "<td>${esc(regName(s.state))}</td>")
rep("<td>${esc(r.state)}</td>", "<td>${esc(r.country)} &middot; ${esc(regName(r.state))}</td>")
rep("{key:'state', label:'State'},", "{key:'state', label:'Country / Region'},")
rep("{key:'investment_usd', label:'Investment'},", "{key:'eur', label:'Investment (original currency)'},")
rep("{key:'opportunity_status', label:'Opportunity'},\n];", "{key:'win_str', label:'2026\\u201327'},\n  {key:'opportunity_status', label:'Opportunity'},\n];")
rep("    modality_str: (s.modality||[]).join('; ')\n", "    modality_str: (s.modality||[]).join('; '),\n    win_str: s.in_window ? 'Yes' : ''\n")
rep("const hay = [r.account_name,r.site_name,r.city,r.state,r.modality_str,r.status].join(' ').toLowerCase();",
    "const hay = [r.account_name,r.site_name,r.city,r.country,regName(r.state),r.modality_str,r.status].join(' ').toLowerCase();")
rep("      <td>${oppStatusTag(r.opportunity_status)}</td>\n    </tr>`).join('');", "      <td>${r.win_str}</td>\n      <td>${oppStatusTag(r.opportunity_status)}</td>\n    </tr>`).join('');")
rep("<th>Site</th><th>State</th>", "<th>Site</th><th>Region</th>")
rep("<div class=\"kv\"><b>Location</b>${esc(s.city)}, ${esc(regName(s.state))}</div>", "<div class=\"kv\"><b>Location</b>${esc(s.city)}, ${esc(regName(s.state))}, ${esc(s.country)}</div>")
rep("      <div class=\"kv\"><b>Jobs</b>${s.jobs??'—'}</div>", "      <div class=\"kv\"><b>Currency</b>${esc(s.currency)}</div>\n      <div class=\"kv\"><b>2026\u201327 window</b>${s.in_window?'Yes':'No'}</div>\n      <div class=\"kv\"><b>Jobs</b>${s.jobs??'—'}</div>")
rep("US Footprint Summary", "DACH Footprint Summary")
rep("acc.us_footprint_summary", "acc.footprint_summary")
rep("US Sites &amp; Projects", "DACH Sites &amp; Projects")
rep("${allAccSites.length} US site(s)", "Group ${esc(acc.group)} &middot; ${allAccSites.length} DACH site(s)")
rep("'<tr><td colspan=\"8\" style=\"color:var(--ink-soft);\">No sites currently match filters.</td></tr>'", "'<tr><td colspan=\"8\" style=\"color:var(--ink-soft);\">No project located in this research pass (or none matches current filters).</td></tr>'")
rep("accts.sort((a,b)=> a.name.localeCompare(b.name));", "accts.sort((a,b)=> a.name.localeCompare(b.name));")
rep("No sites match the current filters in this state.", "No sites match the current filters in this region.")
rep("${st.count} site(s) &middot; ${st.opps} open opportunit${st.opps===1?'y':'ies'} &middot; ${fmtAmt(st.invest,'EUR')+' (\\u20ac-equiv.)'} tracked investment", "${st.count} site(s) &middot; ${st.opps} open opportunit${st.opps===1?'y':'ies'} &middot; ${fmtAmt(st.invest,'EUR')} (\\u20ac-equiv.) tracked") if False else None

# tile rendering: country labels, short codes, custom rows
rep("grid.style.gridTemplateRows = `repeat(${maxRow}, 1fr)`;", "grid.style.gridTemplateRows = 'auto 1fr 1fr auto 1fr auto 1fr 1fr 1fr';")
rep('<span class="st-code" style="color:${txtColor};">${code}</span>', '<span class="st-code" style="color:${txtColor};">${regShort(code)}</span>')
rep("  grid.innerHTML = Object.entries(STATE_GRID).map(", "  const lbl = (txt,row)=>`<div class=\"country-lbl\" style=\"grid-column:1/-1;grid-row:${row};\">${txt}</div>`;\n  grid.innerHTML = lbl('Germany &mdash; 16 L\\u00e4nder',1)+lbl('Austria &mdash; 9 Bundesl\\u00e4nder',4)+lbl('Switzerland &mdash; 26 cantons',6)+Object.entries(STATE_GRID).map(")
rep(".us-grid{\n  display:grid;grid-template-columns:repeat(13,1fr);", ".country-lbl{font-size:11.5px;font-weight:800;color:var(--teal);letter-spacing:0.6px;text-transform:uppercase;padding:6px 0 2px;}\n.us-grid{\n  max-width:640px;display:grid;grid-template-columns:repeat(9,1fr);")
rep(".us-grid{grid-template-columns:repeat(13,minmax(20px,1fr));}", ".us-grid{grid-template-columns:repeat(9,minmax(20px,1fr));}")
rep(".state-tile .st-count{font-size:9px;", ".state-tile .st-code{font-size:12px;}\n.state-tile .st-count{font-size:9px;") if False else None

# KPIs
start = html.index("function renderKPIs(){")
end = html.index("/* ============================================================\n   MAP")
new_kpis = r"""function renderKPIs(){
  const all = SITES;
  const tot = {EUR:0, CHF:0, USD:0};
  all.forEach(s=>{ if(typeof s.investment==='number') tot[s.currency]+=s.investment; });
  const siteCount = all.length;
  const openOpps = all.filter(s=>s.opportunity_status==="OPEN OPPORTUNITY").length;
  const winOpen = all.filter(s=>s.opportunity_status==="OPEN OPPORTUNITY" && s.in_window).length;
  const gf = all.filter(s=>s.project_type==="GREENFIELD").length;
  const bf = all.filter(s=>s.project_type==="BROWNFIELD").length;
  const gfPct = siteCount? Math.round(gf/siteCount*100):0;
  const bfPct = 100-gfPct;
  const byC = c=>all.filter(s=>s.country===c).length;
  const el = document.getElementById('kpi-row');
  el.innerHTML = `
    <div class="kpi-card" style="border-top-color:var(--teal);">
      <div class="kpi-value">${fmtAmt(tot.EUR,'EUR')} <span style="font-size:15px;color:var(--ink-soft);">+</span> ${fmtAmt(tot.CHF,'CHF')}</div>
      <div class="kpi-label">Announced Investment (EUR + CHF, not summed)</div>
      <div class="kpi-sub">+ ${fmtAmt(tot.USD,'USD')} in USD-denominated items &middot; ${ACCOUNTS.length} accounts &middot; floor, many amounts undisclosed &middot; &asymp; ${fmtAmt(tot.EUR+tot.CHF*CHF_EUR+tot.USD*USD_EUR,'EUR')} at 1 CHF=${CHF_EUR} EUR, 1 USD=${USD_EUR} EUR (indicative)</div>
    </div>
    <div class="kpi-card" style="border-top-color:var(--blue);">
      <div class="kpi-value">${siteCount}</div>
      <div class="kpi-label">DACH Sites / Projects Tracked</div>
      <div class="kpi-sub">DE ${byC('Germany')} &middot; AT ${byC('Austria')} &middot; CH ${byC('Switzerland')} &middot; ${[...new Set(all.map(s=>s.state))].length} of 51 regions</div>
    </div>
    <div class="kpi-card" style="border-top-color:var(--aubergine);">
      <div class="kpi-value">${openOpps}</div>
      <div class="kpi-label">Open Opportunities</div>
      <div class="kpi-sub">${winOpen} with activity in the 2026&ndash;27 window</div>
    </div>
    <div class="kpi-card" style="border-top-color:var(--grey);">
      <div class="kpi-value">${gf} / ${bf}</div>
      <div class="kpi-label">Greenfield / Brownfield</div>
      <div class="kpi-split"><span class="gf" style="width:${gfPct}%;"></span><span class="bf" style="width:${bfPct}%;"></span></div>
      <div class="kpi-legend-row"><span><i style="background:var(--aubergine);"></i>Greenfield ${gfPct}%</span><span><i style="background:var(--blue);"></i>Brownfield ${bfPct}%</span></div>
    </div>
  `;
}

"""
html = html[:start] + new_kpis + html[end:]

# CSV export
s0 = html.index("async function exportCSV(){")
s1 = html.index("  const csvLines")
new_csv = r"""async function exportCSV(){
  const cols = ['Account','Site Name','City','State','Latitude','Longitude','Project Type','Modality','Investment (original currency)','Jobs','Status','Expected Start','Opportunity Status','Technical Scope','Orise Offering Fit','Incumbent Vendors','Sources','Notes','Country','Currency','In 2026-27 Window'];
  const rows = filteredSites().map(s=>{
    const acc = accountById(s.account);
    const fit = (s.orise_fit||[]).map(f=>`${f.area} (${f.strength})`).join(' | ');
    const src = (s.sources||[]).map(x=>`${x.publisher||''} ${x.date||''} ${x.url||''} [${x.confidence||''}]`).join(' | ');
    return [acc?acc.name:s.account, s.site_name, s.city, regName(s.state), s.lat, s.lon, s.project_type, (s.modality||[]).join('; '), s.investment??'', s.jobs??'', s.status, s.expected_start||'', s.opportunity_status, s.technical_scope||'', fit, s.incumbent_vendors||'', src, s.notes||'', s.country, s.currency, s.in_window?'Yes':'No'];
  });
"""
html = html[:s0] + new_csv + html[s1:]
rep("filename: 'us-projects.csv'", "filename: 'dach-projects.csv'")
rep("a.download = 'us-projects.csv'", "a.download = 'dach-projects.csv'")

rep('margin:-34px auto 28px auto;','margin:18px auto 28px auto;')
# logo already embedded in the (patched) US template header
# map legend note about shading etc. already in desc. Fallbacks for leftover 'US'
open(OUT_HTML, "w", encoding="utf-8").write(html)

# ---------------- CSV ----------------
cols = ['Account','Site Name','City','State','Latitude','Longitude','Project Type','Modality','Investment (original currency)','Jobs','Status','Expected Start','Opportunity Status','Technical Scope','Orise Offering Fit','Incumbent Vendors','Sources','Notes','Country','Currency','In 2026-27 Window']
name = {a["id"]: a["name"] for a in accounts}
with open(OUT_CSV, "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f); w.writerow(cols)
    for s in sites:
        w.writerow([name[s["account"]], s["site_name"], s["city"], D.REGIONS[s["state"]], s["lat"], s["lon"], s["project_type"], "; ".join(s["modality"]),
            s["investment"] if s["investment"] is not None else "", s["jobs"] if s["jobs"] is not None else "", s["status"], s["expected_start"] or "", s["opportunity_status"],
            s["technical_scope"], " | ".join(f"{x['area']} ({x['strength']})" for x in s["orise_fit"]), s["incumbent_vendors"],
            " | ".join(f"{x['publisher']} {x['date']} {x['url']} [{x['confidence']}]" for x in s["sources"]), s["notes"], s["country"], s["currency"], "Yes" if s["in_window"] else "No"])

# ---------------- sources md ----------------
with open(OUT_SRC, "w", encoding="utf-8") as f:
    f.write(f"# DACH sources (research pass {D.AS_OF})\n\nAll URLs were returned by web searches in this pass; most pages were not opened directly (see dashboard methodology).\n\n")
    for a in sorted(accounts, key=lambda a: a["name"]):
        f.write(f"## {a['name']} ({a['priority_tier']}, group {a['group']})\n")
        ss = by_acc.get(a["id"], [])
        if not ss: f.write("- No project located.\n")
        for s in ss:
            f.write(f"- **{s['site_name']}** ({s['city']}, {D.REGIONS[s['state']]})\n")
            for x in s["sources"]: f.write(f"  - [{x['publisher']}]({x['url']}) — {x['date']} — {x['confidence']}\n")
        f.write("\n")

print("sites", len(sites), "accounts", len(accounts), "open", n_open)
print(collections.Counter(a["priority_tier"] for a in accounts))
for a in accounts: print(a["priority_tier"], a["name"])
