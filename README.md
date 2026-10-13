# Orise Global Pharma Investment Dashboard

One dashboard for the US, DACH and China pharma investment landscapes. Pick a **market** and an **account** at the top; the map, KPIs, fit matrix, account detail, table and CSV export all follow the selection. Selection is kept in the URL hash (`#market=DACH&account=roche`).

## Files
- `data/us.json`, `data/dach.json`, `data/cn.json` – raw datasets extracted from the three single-market dashboards
- `build.py` – merges and normalises them (one account per pharma customer across markets, USD investment, region codes) and inlines the result into the template
- `src/template.html`, `src/logo.txt` – app UI (Leaflet map, vanilla JS)
- `Orise-Global-Pharma-Investment-Dashboard.html` – generated single-file app (`python3 build.py`)

## Refreshing data
Edit or replace a file in `data/`, then run `python3 build.py`. FX rates are in `build.py` (`FX_EUR_PER_USD`).
