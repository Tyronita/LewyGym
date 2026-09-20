<h1 align="center">LewyGym</h1>

<p align="center">
  <strong>A ProteinGym-compatible benchmark for zero-shot variant effect prediction across the Parkinson's disease gene panel</strong>
</p>

<p align="center">
  <a href="https://github.com/Tyronita/LewyGym"><img src="https://img.shields.io/badge/GitHub-LewyGym-black" alt="GitHub"/></a>
  <a href="https://huggingface.co/datasets/Tyronita/LewyGym"><img src="https://img.shields.io/badge/HuggingFace-Datasets-yellow" alt="HuggingFace"/></a>
  <a href="https://creativecommons.org/publicdomain/zero/1.0/"><img src="https://img.shields.io/badge/License-CC0-blue" alt="License: CC0"/></a>
  <img src="https://img.shields.io/github/stars/Tyronita/LewyGym" alt="Stars"/>
  <img src="https://img.shields.io/github/forks/Tyronita/LewyGym" alt="Forks"/>
  <img src="https://img.shields.io/github/last-commit/Tyronita/LewyGym" alt="Last Commit"/>
</p>

<p align="center">
  Named after <strong>Lewy bodies</strong> — the misfolded protein aggregates that define PD pathology.
</p>

<p align="center">
  📄 <a href="lewygym_preprint.pdf"><strong>Preprint PDF</strong></a> · 📊 <a href="lewygym_survey.pdf"><strong>Benchmark Survey</strong></a>
</p>

---

## At a glance

**Protein language models get Parkinson's proteins backwards.**

On SNCA — the hallmark PD protein — ESM-2's conservation signal doesn't just weaken, it **inverts**. Every one of the five DMS assays comes back negative, and **the bigger model makes it worse, not better.**

| Benchmark | ESM-2 mean Spearman ρ |
|---|--:|
| ProteinGym (217 assays) | **+0.419** |
| LewyGym SNCA (ESM-2 8M) | **−0.139** |
| LewyGym SNCA (ESM-2 650M) | **−0.171** |

That gap is the point. PD has two opposing disease mechanisms — gain-of-function aggregation and loss-of-function enzyme collapse — and **no existing benchmark tests whether protein language models handle both across a disease-coherent gene panel.** LewyGym does.

Runs in seconds on CPU for the smoke test. Drop-in ProteinGym format.

---

## Table of Contents

- [Why LewyGym](#why-lewygym)
- [Quick start](#quick-start)
- [Benchmark tracks](#benchmark-tracks)
- [Baseline results](#baseline-results)
- [Scoring method](#scoring-method)
- [Roadmap](#roadmap)
- [Data sources and licences](#data-sources-and-licences)
- [Related Resources](#related-resources)
- [Built With](#built-with)
- [Citation](#citation)
- [License](#license)

---

## Why LewyGym

[ProteinGym](https://github.com/OATML-Markslab/ProteinGym) (217 assays) contains one SNCA assay (Newberry 2020, benchmarked as a fitness predictor with no disease framing) and one Parkin assay — but **no disease-coherent PD panel**. Five PD genes (LRRK2, GBA, PINK1, PARK7, VPS35) are missing entirely. No benchmark frames PD data around the two opposing disease mechanisms, and no clinical pathogenicity track exists for PD proteins.

PD has a well-characterised genetic architecture spanning two opposite directions of effect:

| Mechanism | Genes | Effect |
|---|---|---|
| Gain-of-function | SNCA, LRRK2 | Protein aggregation / kinase hyperactivation |
| Loss-of-function | GBA, PRKN, PINK1, PARK7 | Enzyme/kinase activity lost |

**LewyGym fills that gap** — a single benchmark that tests both directions on a coherent panel of PD genes.

---

## Quick start

```bash
git clone https://github.com/Tyronita/LewyGym
cd LewyGym
pip install transformers torch pandas scipy numpy
```

```bash
# Smoke test — ESM-2 8M, SNCA Newberry, CPU, ~2 min
python score.py --model 8M --assay SNCA_HUMAN_Newberry_2020

# Full DMS track — ESM-2 650M, all 5 assays
python score.py --model 650M --assay all

# ClinVar pathogenicity track
python score.py --model 650M --track pathogenicity
```

### Or load straight from HuggingFace

```python
from datasets import load_dataset

# DMS fitness track
dms = load_dataset("Tyronita/LewyGym", "substitutions")

# ClinVar pathogenicity track
path = load_dataset("Tyronita/LewyGym", "pathogenicity")
```

---

## Benchmark tracks

### Track 1 — DMS substitution fitness (Spearman, ProteinGym-compatible)

All single-residue missense variants. Format identical to ProteinGym substitutions.

| DMS_id | Gene | Variants | Phenotype | Source |
|---|---|--:|---|---|
| SNCA_HUMAN_Newberry_2020 | SNCA | 2,728 | Yeast expression / membrane toxicity | [MaveDB 00000045-k-1](https://www.mavedb.org/experiment/urn:mavedb:00000045-k/) |
| SNCA_HUMAN_Noh_2026_1pct | SNCA | 2,585 | Yeast fitness, 1% galactose induction | [MaveDB 00001249-a-1](https://www.mavedb.org/score-sets/urn:mavedb:00001249-a-1/) |
| SNCA_HUMAN_Noh_2026_01pct | SNCA | 2,593 | Yeast fitness, 0.1% induction | [MaveDB 00001249-a-2](https://www.mavedb.org/score-sets/urn:mavedb:00001249-a-2/) |
| SNCA_HUMAN_Noh_2026_001pct | SNCA | 2,591 | Yeast fitness, 0.01% induction | [MaveDB 00001249-a-3](https://www.mavedb.org/score-sets/urn:mavedb:00001249-a-3/) |
| SNCA_HUMAN_Noh_2026_0001pct | SNCA | 2,503 | Yeast fitness, 0.001% induction | [MaveDB 00001249-a-4](https://www.mavedb.org/score-sets/urn:mavedb:00001249-a-4/) |

**Metric:** Spearman ρ between model log-likelihood delta and experimental fitness score.

### Track 2 — ClinVar pathogenicity classification (AUROC)

ClinVar-classified missense SNVs: Pathogenic/Likely Pathogenic vs Benign/Likely Benign.

| Gene | P/LP | B/LB | Mechanism | Disease relevance |
|---|--:|--:|---|---|
| GBA | 500 | 6 | LOF — glucocerebrosidase | Largest genetic PD risk factor |
| PRKN | 58 | 30 | LOF — ubiquitin ligase | Most common recessive PD |
| PINK1 | 44 | 22 | LOF — mitophagy kinase | Recessive early-onset PD |
| LRRK2 | 20 | 142 | GOF — kinase hyperactivation | Most common dominant PD |
| SNCA | 5 | 3 | GOF — aggregation | Hallmark PD protein (n=8; qualitative only) |
| PARK7 | 7 | 6 | LOF — oxidative sensor | Recessive PD |
| VPS35 | 3 | 2 | GOF — retromer dysfunction | Dominant PD (n=5; qualitative only) |

**Metric:** AUROC. Labels: 1 = P/LP, 0 = B/LB. Source: [ClinVar](https://www.ncbi.nlm.nih.gov/clinvar/), downloaded September 2026.

---

## Baseline results

**DMS track — Spearman ρ (higher = better; all models run zero-shot)**

| Model | Newberry 2020 | Noh 2026 mean | Mean ρ (all 5) |
|---|--:|--:|--:|
| ESM-2 8M | −0.165 | −0.133 | **−0.139** |
| ESM-2 650M | −0.210 | −0.161 | **−0.171** |
| ESM-1v | pending | pending | pending |
| AlphaMissense | pending | pending | pending |

> **Key finding:** ESM-2's conservation signal **inverts** on SNCA — mean ρ = −0.139 to −0.171 (individual assay range −0.115 to −0.210) — versus **+0.419** on ProteinGym's 217-assay substitution benchmark (Notin et al., NeurIPS 2023). All five assays are negative, and larger models amplify rather than correct the inversion.
>
> Note: yeast toxicity captures membrane-binding GOF but is known to fail for fibril-aggregation variants (A30P, G51D).

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

Cost is O(L²) tokens per assay. SNCA (L=140) takes ~20,000 tokens — runs in seconds on CPU.

---

## Roadmap

- [x] SNCA DMS — 5 assays, 13,560 variants (MaveDB)
- [x] ClinVar track — 7 PD genes, 874 classified missense variants
- [x] `score.py` — ESM-2 masked-marginal scoring
- [x] ESM-2 8M/650M baseline results (ρ = −0.139 / −0.171)
- [x] Preprint + survey PDF
- [ ] ESM-1v, AlphaMissense, EVE, ProSST baselines
- [ ] LRRK2 kinase activity dataset (~70 variants, curated from literature)
- [ ] GBA enzyme activity dataset (~50 variants)
- [ ] bioRxiv preprint

---

## Data sources and licences

| Source | Licence | Citation |
|---|---|---|
| MaveDB (Newberry 2020) | CC0 | Newberry et al., *Nature Chemical Biology* 2020. [doi:10.1038/s41589-020-0480-6](https://doi.org/10.1038/s41589-020-0480-6) |
| MaveDB (Noh and Newberry 2026) | CC0 | Noh and Newberry, *Protein Science* 2026. [doi:10.1002/pro.70456](https://doi.org/10.1002/pro.70456) |
| ClinVar | Public domain | Landrum et al., *Nucleic Acids Research*. [PMID:26582918](https://pubmed.ncbi.nlm.nih.gov/26582918/) |

LewyGym itself is released under **CC0** (public domain).

---

## Related Resources

- [ProteinGym](https://github.com/OATML-Markslab/ProteinGym) — the 217-assay benchmark LewyGym is compatible with.
- [MaveDB](https://www.mavedb.org/) — source of the deep mutational scanning assays.
- [ClinVar](https://www.ncbi.nlm.nih.gov/clinvar/) — source of the clinical pathogenicity labels.

---

## Built With

- **Python** — scoring pipeline and data processing.
- [**Transformers**](https://github.com/huggingface/transformers) + [**PyTorch**](https://pytorch.org/) — ESM-2 inference and masked-marginal scoring.
- [**HuggingFace Datasets**](https://huggingface.co/datasets/Tyronita/LewyGym) — dataset hosting and loading.

---

## Citation

```bibtex
@misc{lewygym2026,
  title   = {LewyGym: A Parkinson's Disease Protein Variant Effect Benchmark},
  author  = {O'Leary, Evan and O'Leary, Niall},
  year    = {2026},
  url     = {https://github.com/Tyronita/LewyGym}
}
```

---

## License

Released under **CC0 1.0 Universal** (public domain) — see [LICENSE](LICENSE).

---

<p align="center">
  If you find <strong>LewyGym</strong> useful, please consider starring the repository!<br>
  Your support helps others discover the benchmark.
</p>
