# LewyGym

**Parkinson's Disease Protein Variant Effect Benchmark**

A ProteinGym-compatible benchmark for zero-shot variant effect prediction across the Parkinson's disease gene panel. Named after Lewy bodies — the misfolded protein aggregates that define PD pathology.

[![GitHub](https://img.shields.io/badge/GitHub-LewyGym-black)](https://github.com/Tyronita/LewyGym)
[![HuggingFace](https://img.shields.io/badge/HuggingFace-Datasets-yellow)](https://huggingface.co/datasets/Tyronita/LewyGym)
[![License: CC0](https://img.shields.io/badge/License-CC0-blue)](https://creativecommons.org/publicdomain/zero/1.0/)

---

## Why LewyGym

[ProteinGym](https://github.com/OATML-Markslab/ProteinGym) (217 assays) contains **zero Parkinson's disease proteins**. PD has a well-characterised genetic architecture spanning two opposing disease mechanisms:

| Mechanism | Genes | Effect |
|---|---|---|
| Gain-of-function | SNCA, LRRK2 | Protein aggregation / kinase hyperactivation |
| Loss-of-function | GBA, PRKN, PINK1, PARK7 | Enzyme/kinase activity lost |

No existing benchmark tests whether protein language models handle both directions across a disease-coherent gene panel. **LewyGym fills that gap.**

---

## Benchmark tracks

### Track 1 — DMS substitution fitness (Spearman, ProteinGym-compatible)

All single-residue missense variants. Format identical to ProteinGym substitutions.

| DMS_id | Gene | Variants | Phenotype | Source |
|---|---|---|---|---|
| SNCA_HUMAN_Newberry_2020 | SNCA | 2,728 | Yeast expression / membrane toxicity | [MaveDB 00000045-k-1](https://www.mavedb.org/experiment/urn:mavedb:00000045-k/) |
| SNCA_HUMAN_Noh_2026_1pct | SNCA | 2,725 | Yeast fitness, 1% galactose induction | [MaveDB 00001249-a-1](https://www.mavedb.org/score-sets/urn:mavedb:00001249-a-1/) |
| SNCA_HUMAN_Noh_2026_01pct | SNCA | 2,733 | Yeast fitness, 0.1% induction | [MaveDB 00001249-a-2](https://www.mavedb.org/score-sets/urn:mavedb:00001249-a-2/) |
| SNCA_HUMAN_Noh_2026_001pct | SNCA | 2,731 | Yeast fitness, 0.01% induction | [MaveDB 00001249-a-3](https://www.mavedb.org/score-sets/urn:mavedb:00001249-a-3/) |
| SNCA_HUMAN_Noh_2026_0001pct | SNCA | 2,643 | Yeast fitness, 0.001% induction | [MaveDB 00001249-a-4](https://www.mavedb.org/score-sets/urn:mavedb:00001249-a-4/) |

**Metric:** Spearman ρ between model log-likelihood delta and experimental fitness score.

### Track 2 — ClinVar pathogenicity classification (AUROC)

ClinVar-classified missense SNVs: Pathogenic/Likely Pathogenic vs Benign/Likely Benign.

| Gene | P/LP | B/LB | Mechanism | Disease relevance |
|---|---|---|---|---|
| GBA | 500 | 6 | LOF — glucocerebrosidase | Largest genetic PD risk factor |
| PRKN | 58 | 30 | LOF — ubiquitin ligase | Most common recessive PD |
| PINK1 | 44 | 22 | LOF — mitophagy kinase | Recessive early-onset PD |
| LRRK2 | 20 | 142 | GOF — kinase hyperactivation | Most common dominant PD |
| SNCA | 10 | 6 | GOF — aggregation | Hallmark PD protein |
| PARK7 | 20 | 6 | LOF — oxidative sensor | Recessive PD |
| VPS35 | 6 | 4 | GOF — retromer dysfunction | Dominant PD |

**Metric:** AUROC. Labels: 1 = P/LP, 0 = B/LB. Source: [ClinVar](https://www.ncbi.nlm.nih.gov/clinvar/), downloaded September 2026.

---

## Quick start

```bash
git clone https://github.com/Tyronita/LewyGym
cd LewyGym
pip install transformers torch pandas scipy numpy

# Smoke test — ESM-2 8M, SNCA Newberry, CPU, ~2 min
python score.py --model 8M --assay SNCA_HUMAN_Newberry_2020

# Full DMS track — ESM-2 650M, all 5 assays
python score.py --model 650M --assays all

# ClinVar pathogenicity track
python score.py --model 650M --track pathogenicity
```

## Or load from HuggingFace

```python
from datasets import load_dataset

# DMS fitness track
dms = load_dataset("Tyronita/LewyGym", "substitutions")

# ClinVar pathogenicity track  
path = load_dataset("Tyronita/LewyGym", "pathogenicity")
```

---

## Baseline results

*(Running — will update)*

| Model | SNCA Newberry ρ | SNCA Noh mean ρ | Mean ρ (DMS) |
|---|---|---|---|
| ESM-2 8M | — | — | — |
| ESM-2 650M | — | — | — |
| ESM-1v | — | — | — |
| AlphaMissense | — | — | — |

---

## Scoring method

**Masked-marginal scoring** (same as ProteinGym):

```
For each position i in wildtype sequence:
  1. Mask position i
  2. One forward pass through model
  3. cache[i] = log_softmax(logits[i])

For each variant (e.g. A53T):
  score = log p(T | context) - log p(A | context)

Multi-mutants: sum per-position deltas
```

Cost: O(L²) tokens per assay. SNCA (L=140) takes ~20,000 tokens — runs in seconds on CPU.

---

## Roadmap

- [x] SNCA DMS — 5 assays, 13,560 variants (MaveDB)
- [x] ClinVar track — 7 PD genes, 874 classified missense variants
- [x] score.py — ESM-2 masked-marginal scoring
- [ ] ESM-2 8M/650M baseline results
- [ ] ESM-1v, AlphaMissense, EVE, ProSST baselines
- [ ] LRRK2 kinase activity dataset (~70 variants, curated from literature)
- [ ] GBA enzyme activity dataset (~50 variants)
- [ ] bioRxiv preprint

---

## Data sources and licences

| Source | Licence | Citation |
|---|---|---|
| MaveDB (Newberry 2020) | CC0 | Newberry et al., *Nature Chemical Biology* 2020. [doi:10.1038/s41589-020-0480-6](https://doi.org/10.1038/s41589-020-0480-6) |
| MaveDB (Noh 2026) | CC0 | Noh et al., *Protein Science* 2026. [doi:10.1002/pro.70456](https://doi.org/10.1002/pro.70456) |
| ClinVar | Public domain | Landrum et al., *Nucleic Acids Research*. [PMID:26582918](https://pubmed.ncbi.nlm.nih.gov/26582918/) |

LewyGym itself is released under CC0 (public domain).

---

## Citation

```bibtex
@misc{lewygym2026,
  title   = {LewyGym: A Parkinson's Disease Protein Variant Effect Benchmark},
  author  = {O'Leary, Niall},
  year    = {2026},
  url     = {https://github.com/Tyronita/LewyGym}
}
```
