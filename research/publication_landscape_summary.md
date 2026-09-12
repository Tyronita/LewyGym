# Publication Landscape Research — LewyGym
## Deep research run: 110 agents, 27 sources, 120 claims, 17 confirmed, 8 killed

---

## Verified findings (adversarially confirmed)

### 1. Best venues for a protein variant benchmark paper

| Venue | Format | Why |
|---|---|---|
| **NeurIPS Datasets & Benchmarks** | Conference paper | ProteinGym published here 2023 (confirmed 3-0) |
| **ICML** | Conference paper | FLIP2 accepted as Oral 2026 — top 0.7% (confirmed 2-1) |
| **Bioinformatics (Oxford)** | Application Notes — 4 pages | Fastest route, code on GitHub *required* at submission (confirmed 3-0) |
| **Nature Methods** | Research article | Top-tier, longer review |
| **NAR** | Database/web server | Strong for datasets and benchmarks |

### 2. GitHub — safe, Bioinformatics *requires* it (confirmed 3-0)
- GitHub code/data before submission: does NOT void peer review
- Bioinformatics mandates code at stable URL (e.g. GitHub) at submission time
- Logical conclusion: GitHub-first is not only safe but mandatory for Bioinformatics

### 3. arXiv / bioRxiv — safe at all journals (all confirmed 3-0)

| Journal | Policy |
|---|---|
| Nature Methods | "preprints may be posted at any time during peer review. Not considered prior publication." |
| NAR | Explicitly allows arXiv/bioRxiv; update preprint record upon acceptance |
| Bioinformatics | Permits preprints; offers bioRxiv direct-transfer integration |
| PLOS Comp Bio | "Deposition of manuscripts with preprint servers does not impact consideration" |

**Bottom line: post to bioRxiv immediately. It helps, does not hurt.**

### 4. Scale norms — no hard minimums, but field norms

| Metric | Low end (published) | High end (ProteinGym) |
|---|---|---|
| Models evaluated | 23 (VenusMutHub 2025) | 70+ (ProteinGym leaderboard) |
| DMS assays | ~5 (focused) | 217 |
| Variants | thousands | 2.7M+ |

No journal specifies numerical minimums. Quality + reproducibility > scale.
**For LewyGym v1: evaluate 5 models minimum — ESM-2 8M, ESM-2 650M, ESM-1v, AlphaMissense, EVE.**

### 5. Fastest publication route
1. **Bioinformatics Application Notes** — 4 pages (~2,600 words), code on GitHub, no extended narrative
2. **bioRxiv first** — post immediately while under review
3. **NeurIPS D&B** — highest impact if timing works (deadline usually May/June)

---

## Refuted claims (killed by adversarial verification)

- "ProteinGym benchmarks over 40 models at publication" — 0-3 killed (leaderboard grew post-publication)
- "ProteinGym was GitHub-first before peer review" — 0-3 killed (could not be confirmed from sources)
- "FLIP2 code on GitHub pre-publication voids NeurIPS submission" — 1-2 killed
- "GigaByte Journal has no APC for first 6 months" — 0-3 killed

---

## Open questions not resolved

1. Impact factors / acceptance rates for each journal — not confirmed by adversarial verification
2. Genome Biology and Briefings in Bioinformatics preprint policies — not fetched
3. Exact reviewer criteria at Nature Methods vs Bioinformatics for "biological insight" threshold
4. Whether ProteinGym was specifically GitHub-first (claims refuted, not definitively answered)

---

## Recommended publication plan for LewyGym

```
Immediate:  bioRxiv preprint — post now
Week 1-2:   Run ESM-2 8M + 650M + ESM-1v + AlphaMissense → get Spearman/AUROC numbers
Week 3:     Write 4-page Bioinformatics Application Note
Week 3:     Submit to Bioinformatics + post bioRxiv simultaneously
Stretch:    NeurIPS D&B submission if results are strong
```

---

## Full raw research output
See `deep_research_publication_landscape.json` in this folder (27,950 bytes, full agent outputs).

## Session gist (backup)
https://gist.github.com/Tyronita/d6a09d88279960aa2289a35c51ce1ede
