#!/usr/bin/env python3
"""Merge the US, DACH and China datasets into one normalised dataset and inline it
into src/template.html -> Orise-Global-Pharma-Investment-Dashboard.html

Usage: python3 build.py
"""
import json, re, pathlib

ROOT = pathlib.Path(__file__).parent
FX_EUR_PER_USD = 0.86   # same indicative rate the DACH dashboard used (1 USD = 0.86 EUR)
FX_NOTE = "EUR/CHF amounts converted at 1 CHF = 1.07 EUR and 1 USD = 0.86 EUR (indicative, as in the DACH dashboard; Italy uses the same EUR rate); CNY amounts use the USD equivalents from the China dashboard."

MARKETS = [
    {"id": "US", "name": "United States", "short": "US", "file": "us.json"},
    {"id": "DACH", "name": "DACH (Germany · Austria · Switzerland)", "short": "DACH", "file": "dach.json"},
    {"id": "CN", "name": "China", "short": "China", "file": "cn.json"},
    {"id": "IT", "name": "Italy", "short": "Italy", "file": "it.json"},
]

# Optional alias map: account name (lower-case, parenthetical stripped) -> canonical name
ALIASES = {"roche": "Roche", "wuxi apptec": "WuXi AppTec", "johnson & johnson": "Johnson & Johnson Innovative Medicine"}


def canon(name):
    base = re.sub(r"\s*\(.*?\)", "", name).strip()
    base = ALIASES.get(base.lower(), base)
    return base, re.sub(r"[^a-z0-9]+", "-", base.lower()).strip("-")


def main():
    accounts = {}      # canonical id -> {id,name,markets:{M:{...}}}
    sites = []
    regions = {}       # global region code -> {name, market, country}
    gaps = {}
    as_of = {}
    for m in MARKETS:
        d = json.load(open(ROOT / "data" / m["file"]))
        as_of[m["id"]] = d["as_of"]
        gaps[m["id"]] = d["gaps_html"]
        id_map = {}
        for a in d["accounts"]:
            cname, cid = canon(a["name"])
            id_map[a["id"]] = cid
            acc = accounts.setdefault(cid, {"id": cid, "name": cname, "markets": {}})
            acc["markets"][m["id"]] = {
                "tier": a.get("priority_tier"),
                "tier_reason": a.get("priority_reason"),
                "footprint": a.get("us_footprint_summary") or a.get("footprint_summary") or "",
                "strategy": a.get("investment_strategy_summary") or "",
                "ownership": a.get("ownership_note") or "",
                "incumbents": a.get("incumbent_vendors_general") or "",
                "roles": a.get("roles") or "",
                "source_name": a["name"],
            }
        for s in d["sites"]:
            if m["id"] == "US":
                usd, cur, local, country, rcode = s.get("investment_usd"), "USD", s.get("investment_display"), "United States", "US-" + s["state"]
            elif m["id"] == "CN":
                usd, cur, local, country, rcode = s.get("investment_usd"), "CNY/USD", s.get("investment_display"), "China", "CN-" + s["state"]
            else:
                cur = s.get("currency")
                usd = round(s["eur"] / FX_EUR_PER_USD) if s.get("eur") is not None else None
                local, country, rcode = s.get("investment_display"), s.get("country"), s["state"]  # already DE-BY etc.
            regions[rcode] = {"name": d["region_names"].get(s["state"], s["state"]), "market": m["id"], "country": country}
            sites.append({
                "id": m["id"].lower() + "-" + s["id"],
                "market": m["id"],
                "account": id_map[s["account"]],
                "site_name": s["site_name"],
                "site_name_zh": s.get("site_name_zh"),
                "city": s["city"], "country": country, "region": rcode,
                "lat": s["lat"], "lon": s["lon"],
                "project_type": s["project_type"], "modality": s.get("modality") or [],
                "investment_usd": usd, "investment_display": local, "currency": cur,
                "jobs": s.get("jobs"), "status": s.get("status"), "expected_start": s.get("expected_start"),
                "in_window": s.get("in_window"),
                "opportunity_status": s["opportunity_status"],
                "technical_scope": s.get("technical_scope"), "orise_fit": s.get("orise_fit") or [],
                "incumbent_vendors": s.get("incumbent_vendors") or "",
                "sources": s.get("sources") or [], "notes": s.get("notes") or "",
            })
    for r in regions.values():
        pass
    data = {
        "markets": MARKETS, "accounts": sorted(accounts.values(), key=lambda a: a["name"].lower()),
        "sites": sites, "regions": regions, "gaps": gaps, "as_of": as_of, "fx_note": FX_NOTE,
        "offering_areas": [
            "SCADA / process control and automation", "MES implementation and integration",
            "Digitalization / Industry 4.0", "Validation / CSV / data integrity",
            "Legacy system modernization and migration", "Lifecycle support and managed services"],
    }
    logo = (ROOT / "src" / "logo.txt").read_text().strip()
    html = (ROOT / "src" / "template.html").read_text()
    html = html.replace("/*__DATA__*/null", json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/"))
    html = html.replace("__LOGO__", logo)
    html = html.replace("/*__BASEMAP__*/null", (ROOT / "data" / "basemap.json").read_text().strip())
    html = html.replace("/*__LEAFLET_CSS__*/", (ROOT / "src" / "leaflet.css").read_text())
    out = ROOT / "Orise-Global-Pharma-Investment-Dashboard.html"
    out.write_text(html)
    # Claude Artifact variant: body-only page (the platform adds the document skeleton)
    title = re.search(r"<title>.*?</title>", html, re.S).group(0)
    style = re.search(r"<style>.*?</style>", html, re.S).group(0)
    body = re.search(r"<body>(.*)</body>", html, re.S).group(1)
    (ROOT / "dist").mkdir(exist_ok=True)
    (ROOT / "dist" / "artifact.html").write_text(title + "\n" + style + "\n" + body)
    multi = [a["name"] for a in data["accounts"] if len(a["markets"]) > 1]
    print(f"wrote {out.name}: {len(sites)} sites, {len(accounts)} accounts ({len(multi)} in 2+ markets: {', '.join(multi)})")


if __name__ == "__main__":
    main()
