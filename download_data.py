"""Download raw DMS data from MaveDB and write to DMS_LewyGym_substitutions/.

Usage:
    python download_data.py

MaveDB accessions:
    SNCA Newberry 2020:       urn:mavedb:00000045-k-1
    SNCA Noh & Newberry 2026: urn:mavedb:00001249-a-1  (1%   galactose)
                              urn:mavedb:00001249-a-2  (0.1% galactose)
                              urn:mavedb:00001249-a-3  (0.01% galactose)
                              urn:mavedb:00001249-a-4  (0.001% galactose)
"""
import csv
import json
import re
import urllib.request
from pathlib import Path

API = "https://api.mavedb.org/api/v1"
OUT = Path(__file__).parent / "DMS_LewyGym_substitutions"
OUT.mkdir(exist_ok=True)

ACCESSIONS = {
    "SNCA_HUMAN_Newberry_2020":    "urn:mavedb:00000045-k-1",
    "SNCA_HUMAN_Noh_2026_1pct":    "urn:mavedb:00001249-a-1",
    "SNCA_HUMAN_Noh_2026_01pct":   "urn:mavedb:00001249-a-2",
    "SNCA_HUMAN_Noh_2026_001pct":  "urn:mavedb:00001249-a-3",
    "SNCA_HUMAN_Noh_2026_0001pct": "urn:mavedb:00001249-a-4",
}

HGVS_RE = re.compile(r"p\.([A-Z][a-z]{2})(\d+)([A-Z][a-z]{2}|Ter)")

AA3 = {"Ala":"A","Arg":"R","Asn":"N","Asp":"D","Cys":"C","Gln":"Q","Glu":"E",
       "Gly":"G","His":"H","Ile":"I","Leu":"L","Lys":"K","Met":"M","Phe":"F",
       "Pro":"P","Ser":"S","Thr":"T","Trp":"W","Tyr":"Y","Val":"V","Ter":"*"}


def hgvs_to_mutant(hgvs: str) -> str | None:
    m = HGVS_RE.match(hgvs)
    if not m:
        return None
    wt, pos, mt = m.group(1), m.group(2), m.group(3)
    wt1 = AA3.get(wt); mt1 = AA3.get(mt)
    if not wt1 or not mt1:
        return None
    return f"{wt1}{pos}{mt1}"


def fetch_json(url: str):
    with urllib.request.urlopen(url, timeout=30) as r:
        return json.load(r)


for name, acc in ACCESSIONS.items():
    print(f"Fetching {name} ({acc})...")
    urn_enc = acc.replace(":", "%3A")
    data = fetch_json(f"{API}/score-sets/{urn_enc}/scores")
    rows = []
    for entry in data.get("data", []):
        hgvs = entry.get("hgvs_pro", "")
        score = entry.get("score")
        if score is None:
            continue
        mutant = hgvs_to_mutant(hgvs)
        if mutant is None:
            continue
        rows.append({"mutant": mutant, "DMS_score": score})
    out_path = OUT / f"{name}.csv"
    with open(out_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["mutant", "DMS_score"])
        w.writeheader()
        w.writerows(rows)
    print(f"  -> {out_path} ({len(rows)} rows)")

print("\nDone.")
