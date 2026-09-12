---
license: cc0-1.0
task_categories:
- text-classification
- other
language:
- en
tags:
- biology
- protein
- parkinson
- variant-effect-prediction
- deep-mutational-scanning
- bioinformatics
- ESM
- ProteinGym
pretty_name: LewyGym
size_categories:
- 10K<n<100K
---

# LewyGym — Parkinson's Disease Protein Variant Effect Benchmark

ProteinGym-compatible variant effect prediction benchmark for Parkinson's disease proteins.

## Dataset description

LewyGym provides two benchmark tracks for evaluating protein language models on Parkinson's disease variant effect prediction:

**Track 1 — DMS substitution fitness** (Spearman metric, ProteinGym-compatible)
- 5 SNCA (alpha-synuclein) deep mutational scanning assays
- 13,560 total variant-score pairs
- Source: MaveDB (CC0)

**Track 2 — ClinVar pathogenicity classification** (AUROC metric)
- 7 PD genes: LRRK2, GBA, PRKN, PINK1, SNCA, PARK7, VPS35
- 874 classified missense variants (P/LP vs B/LB)
- Source: ClinVar (public domain)

## Usage

```python
from datasets import load_dataset

# DMS track
dms = load_dataset("Tyronita/LewyGym", "substitutions")
# columns: mutant, DMS_score, DMS_id, gene, source

# Pathogenicity track  
path = load_dataset("Tyronita/LewyGym", "pathogenicity")
# columns: mutant, label (1=pathogenic, 0=benign), gene, significance
```

## Scoring with ESM-2

```bash
git clone https://github.com/Tyronita/LewyGym
pip install transformers torch pandas scipy
python score.py --model 650M --assays all
```

## Sources

- Newberry et al. 2020, *Nature Chemical Biology* — SNCA yeast toxicity DMS
- Noh et al. 2026, *Protein Science* — SNCA concentration-dependent DMS  
- Landrum et al., *NAR* — ClinVar
