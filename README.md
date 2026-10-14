# CSV Report Tool

I made this because real-world spreadsheets are always a mess: dates in three different formats, prices with commas or dots, the same product written two ways, duplicated rows... This script cleans all that up and gives you a simple summary. It only uses plain Python, nothing to install.

**What it deals with**
- Mixed date formats: `2026-01-05`, `05/01/2026`, `02-14-2026`, `12.02.2026`
- Mixed number formats: `1,234.50`, `1.234,50`, `29,90`, `€ 29.90`
- Inconsistent product names (`usb-c hub` / `USB-C Hub`)
- Duplicated rows and invalid rows (reported, not silently dropped)

## Usage
```bash
python3 csv_report.py sample/sales.csv --out report.md --clean cleaned.csv
```

## Example output
```
# Sales report

- Valid orders: **5**
- Rejected rows (invalid or duplicated): **4**
- Total revenue: **2389.30**
```

## Tests
```bash
python3 -m unittest discover tests
```

If you have a spreadsheet that drives you crazy every week, I can build something like this for it. I'm on Fiverr.
