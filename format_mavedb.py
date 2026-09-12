"""Convert MaveDB HGVS format to ProteinGym-compatible CSVs.

Input:  accession, hgvs_nt, hgvs_splice, hgvs_pro, score
Output: mutant (e.g. M1W), DMS_score
"""
import csv, re, sys
from pathlib import Path

AA3 = {
    'Ala':'A','Arg':'R','Asn':'N','Asp':'D','Cys':'C','Gln':'Q','Glu':'E',
    'Gly':'G','His':'H','Ile':'I','Leu':'L','Lys':'K','Met':'M','Phe':'F',
    'Pro':'P','Ser':'S','Thr':'T','Trp':'W','Tyr':'Y','Val':'V','Ter':'*',
    'Sec':'U',
}

HGVS_RE = re.compile(r'p\.([A-Z][a-z]{2})(\d+)([A-Z][a-z]{2,3})')

def hgvs_to_mutant(hgvs_pro: str) -> str | None:
    m = HGVS_RE.search(hgvs_pro)
    if not m:
        return None
    wt3, pos, mt3 = m.groups()
    wt1 = AA3.get(wt3)
    mt1 = AA3.get(mt3)
    if not wt1 or not mt1:
        return None
    return f"{wt1}{pos}{mt1}"

DATASETS = {
    "SNCA_HUMAN_Newberry_2020": "snca_mavedb_newberry2020.csv",
    "SNCA_HUMAN_Noh_2026_1pct":   "snca_noh2026_conc1.csv",
    "SNCA_HUMAN_Noh_2026_01pct":  "snca_noh2026_conc2.csv",
    "SNCA_HUMAN_Noh_2026_001pct": "snca_noh2026_conc3.csv",
    "SNCA_HUMAN_Noh_2026_0001pct":"snca_noh2026_conc4.csv",
}

SRC = Path.home() / "protein-language-model-experiments-esm2_t33_650M_UR50D/data/pd_variants"
DST = Path("DMS_LewyGym_substitutions")
DST.mkdir(exist_ok=True)

summary = []
for dms_id, fname in DATASETS.items():
    src = SRC / fname
    rows = []
    skipped = 0
    with open(src) as f:
        for row in csv.DictReader(f):
            hgvs = row.get('hgvs_pro', '')
            score = row.get('score', '')
            if not hgvs or not score or score in ('NA', '', 'nan'):
                skipped += 1
                continue
            mutant = hgvs_to_mutant(hgvs)
            if not mutant:
                skipped += 1
                continue
            try:
                rows.append({'mutant': mutant, 'DMS_score': float(score)})
            except ValueError:
                skipped += 1

    out = DST / f"{dms_id}.csv"
    with open(out, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=['mutant', 'DMS_score'])
        w.writeheader()
        w.writerows(rows)
    summary.append((dms_id, len(rows), skipped))
    print(f"  {dms_id}: {len(rows)} variants, {skipped} skipped → {out}")

print(f"\nDone. {sum(r[1] for r in summary)} total variants across {len(summary)} assays.")
