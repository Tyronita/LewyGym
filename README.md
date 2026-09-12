# PDGym — Parkinson's Disease Variant Effect Benchmark

A ProteinGym-compatible benchmark for zero-shot variant effect prediction across the Parkinson's disease gene panel.

## Why

ProteinGym (217 assays, Spearman leaderboard) is the standard benchmark for protein language models but contains **no Parkinson's disease proteins**. PD has a well-characterised genetic architecture spanning gain-of-function (SNCA, LRRK2) and loss-of-function (GBA, PRKN, PINK1) mechanisms — a test no existing benchmark makes.

PDGym fills this gap.

## Structure

```
PDGym/
  DMS_PDGym_substitutions/     # DMS fitness scores — Spearman metric (ProteinGym-compatible)
  pathogenicity/               # ClinVar P/LP vs B/LB labels — AUROC metric
  reference_files/             # Metadata, wildtype sequences
  score.py                     # Run ESM-2 masked-marginal scoring
```

## Substitution benchmark (DMS track)

All single-residue missense variants scored. Format identical to ProteinGym substitutions.

| DMS_id | Gene | Variants | Phenotype | Source |
|---|---|---|---|---|
| SNCA_HUMAN_Newberry_2020 | SNCA | 2,728 | Yeast expression / membrane toxicity | MaveDB `00000045-k-1` |
| SNCA_HUMAN_Noh_2026_1pct | SNCA | 2,725 | Yeast fitness, 1% induction | MaveDB `00001249-a-1` |
| SNCA_HUMAN_Noh_2026_01pct | SNCA | 2,733 | Yeast fitness, 0.1% induction | MaveDB `00001249-a-2` |
| SNCA_HUMAN_Noh_2026_001pct | SNCA | 2,731 | Yeast fitness, 0.01% induction | MaveDB `00001249-a-3` |
| SNCA_HUMAN_Noh_2026_0001pct | SNCA | 2,643 | Yeast fitness, 0.001% induction | MaveDB `00001249-a-4` |

**Metric:** Spearman correlation between model log-likelihood deltas and DMS fitness scores.  
**Scoring strategy:** masked-marginal (same as ProteinGym; wt-marginals give lower Spearman).

## Pathogenicity benchmark (ClinVar track)

ClinVar-classified missense SNVs (Pathogenic/Likely Pathogenic vs Benign/Likely Benign).

| File | Gene | P/LP | B/LB | Disease mechanism |
|---|---|---|---|---|
| clinvar_lrrk2_missense.csv | LRRK2 | 20 | 142 | GOF — kinase hyperactivation |
| clinvar_gba_missense.csv | GBA | 500 | 6 | LOF — lysosomal enzyme deficiency |
| clinvar_prkn_missense.csv | PRKN | 58 | 30 | LOF — ubiquitin ligase |
| clinvar_pink1_missense.csv | PINK1 | 44 | 22 | LOF — mitophagy kinase |
| clinvar_snca_missense.csv | SNCA | 10 | 6 | GOF — aggregation |
| clinvar_park7_missense.csv | PARK7 | 20 | 6 | LOF — oxidative stress sensor |
| clinvar_vps35_missense.csv | VPS35 | 6 | 4 | GOF — retromer dysfunction |

**Metric:** AUROC. Labels: 1 = Pathogenic/Likely Pathogenic, 0 = Benign/Likely Benign.

## Quick start

```bash
git clone https://github.com/Tyronita/PDGym
cd PDGym
pip install transformers torch pandas scipy numpy

# Score SNCA with ESM-2 8M (fast, CPU)
python score.py --model 8M --assay SNCA_HUMAN_Newberry_2020

# Score all DMS assays with ESM-2 650M
python score.py --model 650M --assays all

# Score ClinVar pathogenicity (AUROC)
python score.py --model 650M --track pathogenicity
```

## Data sources

- **MaveDB** — [mavedb.org](https://www.mavedb.org) — open repository for multiplexed variant effect assays
- **ClinVar** — [ncbi.nlm.nih.gov/clinvar](https://www.ncbi.nlm.nih.gov/clinvar) — NCBI variant pathogenicity database, downloaded September 2026
- All data is open access. MaveDB data is CC0 (public domain).

## Citation

If you use PDGym, please also cite the original assay publications:

- Newberry et al. (2020) *Nature Chemical Biology* — SNCA yeast toxicity DMS. doi:10.1038/s41589-020-0480-6
- Noh et al. (2026) *Protein Science* — SNCA concentration-dependent DMS. doi:10.1002/pro.70456
- Landrum et al. — ClinVar. *Nucleic Acids Research*.

## Roadmap

- [ ] LRRK2 kinase activity dataset (curated from literature, ~70 variants)
- [ ] GBA enzyme activity dataset (curated from Gaucher literature, ~50 variants)
- [ ] PINK1 kinase activity dataset (~20 variants)
- [ ] LRRK2 kinase domain DMS (wet lab, in progress)
- [ ] Leaderboard with ESM-2, ESM-1v, AlphaMissense, EVE, ProSST baselines
- [ ] HuggingFace Datasets integration
