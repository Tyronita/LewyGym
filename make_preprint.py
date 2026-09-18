"""Generate LewyGym bioRxiv preprint PDF using fpdf2."""
from fpdf import FPDF

MARGIN = 25
PW = 210
CONTENT_W = PW - 2 * MARGIN  # 160 mm


class Paper(FPDF):
    def header(self):
        if self.page_no() > 1:
            self.set_font("Times", "I", 8)
            self.set_text_color(120, 120, 120)
            self.cell(0, 5, "LewyGym preprint  |  O'Leary 2026  |  github.com/Tyronita/LewyGym", align="L")
            self.ln(3)
            self.set_text_color(0, 0, 0)

    def footer(self):
        self.set_y(-15)
        self.set_font("Times", "", 9)
        self.set_text_color(120, 120, 120)
        self.cell(0, 10, str(self.page_no()), align="C")
        self.set_text_color(0, 0, 0)


def build():
    pdf = Paper("P", "mm", "A4")
    pdf.set_margins(MARGIN, MARGIN, MARGIN)
    pdf.set_auto_page_break(True, margin=MARGIN)
    pdf.add_page()

    # ── helpers ────────────────────────────────────────────────────────────

    def para(txt, size=10, align="J", extra_ln=2):
        pdf.set_font("Times", "", size)
        pdf.multi_cell(CONTENT_W, 5.5, txt, align=align)
        if extra_ln:
            pdf.ln(extra_ln)

    def section_head(num, title):
        pdf.ln(5)
        pdf.set_font("Times", "B", 12)
        pdf.multi_cell(CONTENT_W, 7, f"{num}  {title}")
        pdf.set_draw_color(160, 160, 160)
        pdf.set_line_width(0.3)
        pdf.line(MARGIN, pdf.get_y(), PW - MARGIN, pdf.get_y())
        pdf.set_line_width(0.2)
        pdf.set_draw_color(0, 0, 0)
        pdf.ln(3)

    def sub_head(title):
        pdf.ln(3)
        pdf.set_font("Times", "B", 10)
        pdf.multi_cell(CONTENT_W, 6, title)
        pdf.ln(1)

    def table_row(cells, col_w, font_style="", font_size=8, fill=False, fill_color=(255, 255, 255)):
        pdf.set_font("Times", font_style, font_size)
        pdf.set_fill_color(*fill_color)
        for i, (txt, w) in enumerate(zip(cells, col_w)):
            al = "L" if i == 0 else "C"
            pdf.cell(w, 5.5, str(txt), border=1, fill=fill, align=al)
        pdf.ln()

    def table(label, headers, rows, col_w, font_size=8):
        pdf.set_font("Times", "B", 9)
        pdf.cell(0, 5, label)
        pdf.ln(1)
        table_row(headers, col_w, "B", font_size, True, (210, 210, 210))
        for i, row in enumerate(rows):
            is_total = str(row[0]).strip() in ("Total", "Mean")
            fill = i % 2 == 1 and not is_total
            fc = (242, 242, 242) if fill else (255, 255, 255)
            if is_total:
                fc = (230, 230, 230)
            table_row(row, col_w, "B" if is_total else "", font_size, True, fc)
        pdf.ln(2)

    def caption(txt):
        pdf.set_font("Times", "I", 8.5)
        pdf.multi_cell(CONTENT_W, 4.5, txt)
        pdf.ln(3)

    def code(txt):
        pdf.set_font("Courier", "", 8)
        pdf.set_fill_color(245, 245, 245)
        pdf.multi_cell(CONTENT_W, 4.5, txt, border=1, fill=True)
        pdf.set_font("Times", "", 10)
        pdf.ln(2)

    def ref_item(num, txt):
        pdf.set_font("Times", "", 8.5)
        x0 = pdf.get_x()
        pdf.cell(9, 5, f"[{num}]", align="R")
        pdf.set_x(MARGIN + 10)
        pdf.multi_cell(CONTENT_W - 10, 4.8, txt)
        pdf.ln(0.5)

    # ── TITLE BLOCK ────────────────────────────────────────────────────────

    pdf.set_font("Times", "B", 17)
    pdf.multi_cell(CONTENT_W, 9,
        "LewyGym: A Parkinson's Disease Protein Variant Effect Benchmark\n"
        "Reveals Signal Inversion in Conservation-Based Protein Language Models",
        align="C")
    pdf.ln(3)

    pdf.set_font("Times", "B", 11)
    pdf.multi_cell(CONTENT_W, 6, "Evan O'Leary¹  and  Niall O'Leary²", align="C")

    pdf.set_font("Times", "I", 9)
    pdf.multi_cell(CONTENT_W, 5,
        "¹Independent researcher  |  evan.oleary99@gmail.com\n"
        "²Patient co-investigator  |  living with Parkinson's disease",
        align="C")
    pdf.ln(1)

    pdf.set_font("Times", "", 8.5)
    pdf.multi_cell(CONTENT_W, 5,
        "bioRxiv preprint  *  September 2026\n"
        "GitHub: github.com/Tyronita/LewyGym  *  HuggingFace: EvanOLeary/LewyGym  *  License: CC0",
        align="C")
    pdf.ln(4)

    pdf.set_draw_color(0, 0, 0)
    pdf.set_line_width(0.5)
    pdf.line(MARGIN, pdf.get_y(), PW - MARGIN, pdf.get_y())
    pdf.set_line_width(0.2)
    pdf.ln(5)

    # ── ABSTRACT ───────────────────────────────────────────────────────────

    pdf.set_font("Times", "B", 10)
    pdf.cell(0, 6, "Abstract")
    pdf.ln(1)

    pdf.set_font("Times", "", 9)
    pdf.set_fill_color(248, 248, 248)
    pdf.multi_cell(CONTENT_W, 5,
        "Protein language models (PLMs) trained on evolutionary sequence conservation achieve strong "
        "variant effect prediction, with ESM-2 650M reaching mean Spearman rho +0.419 across "
        "ProteinGym's 217-assay substitution benchmark. However, no benchmark evaluates PLMs across "
        "a disease-coherent Parkinson's disease (PD) gene panel. PD spans two opposing pathogenic "
        "mechanisms: gain-of-function (GOF) aggregation (SNCA, LRRK2) and loss-of-function (LOF) "
        "enzyme/kinase disruption (GBA, PRKN, PINK1, PARK7). We introduce LewyGym, a "
        "ProteinGym-compatible benchmark covering seven PD genes. LewyGym provides two tracks: "
        "(i) a DMS fitness track with 12,860 missense variants across five alpha-synuclein (SNCA) "
        "assays from MaveDB, and (ii) a ClinVar pathogenicity classification track with 421 "
        "annotated missense variants across seven PD genes. Baseline ESM-2 evaluation yields mean "
        "Spearman rho -0.139 to -0.171 on the DMS track -- a 0.58-unit inversion relative to "
        "ProteinGym. All five assays are negative; larger models amplify the inversion. LewyGym "
        "is released under CC0 with a reproducible scoring script.",
        border=1, fill=True, align="J")
    pdf.ln(2)

    pdf.set_font("Times", "I", 8.5)
    pdf.multi_cell(CONTENT_W, 5,
        "Keywords: protein language model, Parkinson's disease, variant effect prediction, benchmark, "
        "alpha-synuclein, deep mutational scanning, gain-of-function")
    pdf.ln(4)
    pdf.set_draw_color(180, 180, 180)
    pdf.line(MARGIN, pdf.get_y(), PW - MARGIN, pdf.get_y())
    pdf.set_draw_color(0, 0, 0)

    # ── 1. INTRODUCTION ────────────────────────────────────────────────────

    section_head("1.", "Introduction")

    para(
        "Protein language models (PLMs) trained on large protein sequence corpora have demonstrated "
        "remarkable zero-shot ability to predict the functional consequences of amino acid substitutions [1]. "
        "The dominant evaluation paradigm -- exemplified by ProteinGym [1] and FLIP [2] -- measures "
        "Spearman rank correlation between model-predicted log-likelihood ratios and experimentally "
        "measured fitness scores from deep mutational scanning (DMS) assays. ESM-2 650M achieves a "
        "mean Spearman rho of +0.419 across ProteinGym's 217 substitution assays [1], and ESM-1v "
        "reaches +0.440 [3]."
    )

    para(
        "This strong performance rests on a key biological assumption: amino acids disfavoured by "
        "evolution (low PLM log-likelihood) are also functionally damaging. For loss-of-function (LOF) "
        "proteins -- where variants disrupt enzymatic activity, structural stability, or binding "
        "affinity -- this assumption holds. The evolutionary record penalises variants that break "
        "the protein."
    )

    para(
        "Parkinson's disease (PD) presents a systematic challenge to this assumption. The PD gene "
        "panel spans two opposing pathogenic mechanisms. SNCA (alpha-synuclein) and LRRK2 operate "
        "through gain-of-function (GOF): variants that increase alpha-synuclein's aggregation "
        "propensity, or hyperactivate LRRK2 kinase, are pathogenic because they enhance a toxic "
        "function. For GOF proteins, a residue that promotes aggregation may be evolutionarily "
        "disfavoured -- meaning conservation-based PLMs assign it a negative log-likelihood delta, "
        "predicting it as evolutionarily unusual, while the DMS fitness score registers harm via a "
        "completely different biological mechanism (aggregation-driven toxicity). For LOF genes in "
        "the PD panel (GBA, PRKN, PINK1, PARK7), the standard conservation-fitness alignment "
        "should hold."
    )

    para(
        "Despite PD affecting more than 10 million people worldwide, no benchmark evaluates PLMs "
        "across a disease-coherent PD gene panel spanning both GOF and LOF mechanisms simultaneously. "
        "ProteinGym (217 assays) includes one SNCA assay (Newberry 2020, benchmarked as a fitness "
        "predictor without disease framing) and one Parkin assay, but five PD genes -- LRRK2, GBA, "
        "PINK1, PARK7, VPS35 -- are entirely absent, and no clinical pathogenicity classification "
        "track exists. Kryukov et al. [10] previously showed GOF proteins are a general weak spot "
        "for variant effect predictors; we instantiate this in the PD context and provide a reusable "
        "benchmark infrastructure. We introduce LewyGym -- named after Lewy bodies, the misfolded "
        "alpha-synuclein aggregates that define PD pathology. Our baseline results confirm that "
        "ESM-2 conservation signals invert on SNCA (mean Spearman rho = -0.139 to -0.171), and "
        "that larger ESM-2 models amplify rather than correct this inversion."
    )

    # ── 2. BENCHMARK DESIGN ────────────────────────────────────────────────

    section_head("2.", "Benchmark Design")

    sub_head("2.1  DMS Fitness Track")

    para(
        "The DMS track comprises five SNCA assays from MaveDB [7], all measuring yeast fitness as a "
        "proxy for alpha-synuclein membrane toxicity. Newberry et al. [5] measured fitness of all "
        "single-residue substitutions in a membrane-targeted GFP fusion construct expressed in yeast. "
        "Noh and Newberry [6] measured yeast fitness at four galactose induction concentrations "
        "(1%, 0.1%, 0.01%, 0.001%), capturing the concentration-dependent toxicity landscape of "
        "alpha-synuclein. All five assays cover the full SNCA sequence (UniProt P37840, L = 140) "
        "and originate from the Newberry lab at UCSF. Data were retrieved from MaveDB via the "
        "public REST API (api.mavedb.org), converted from HGVS notation to ProteinGym one-letter "
        "substitution format, and normalised to zero-mean unit-variance. Synonymous variants "
        "(wildtype residue = mutant residue), stop codons, insertions, and reference-mismatch "
        "variants were excluded; reported n values reflect missense-only variants. Note that the "
        "yeast membrane toxicity assay captures membrane-binding GOF; variants that promote "
        "fibrillation but reduce membrane binding (notably A30P, G51D) are known to score as "
        "fitness-rescuing in this system despite being familial PD mutations."
    )

    # Table 1 - DMS assays
    # col_w must sum to CONTENT_W = 160
    # Assay(58) + n(13) + Phenotype(56) + Source(33) = 160
    table(
        "Table 1.  DMS assays in LewyGym v0.1.  All assays: SNCA (UniProt P37840, L=140).",
        headers=["Assay ID", "n", "Phenotype", "Source (MaveDB)"],
        rows=[
            ["SNCA_HUMAN_Newberry_2020",    "2,588",  "GFP membrane toxicity (yeast)",    "00000045-k-1"],
            ["SNCA_HUMAN_Noh_2026_1pct",    "2,585",  "Fitness, 1% galactose induction",  "00001249-a-1"],
            ["SNCA_HUMAN_Noh_2026_01pct",   "2,593",  "Fitness, 0.1% galactose",          "00001249-a-2"],
            ["SNCA_HUMAN_Noh_2026_001pct",  "2,591",  "Fitness, 0.01% galactose",         "00001249-a-3"],
            ["SNCA_HUMAN_Noh_2026_0001pct", "2,503",  "Fitness, 0.001% galactose",        "00001249-a-4"],
            ["Total",                        "12,860", "",                                  ""],
        ],
        col_w=[62, 14, 54, 30],
    )

    sub_head("2.2  ClinVar Pathogenicity Track")

    para(
        "The pathogenicity track provides ClinVar-classified missense variants for all seven PD genes: "
        "SNCA, LRRK2, GBA, PRKN, PINK1, PARK7, and VPS35. Only missense single-nucleotide variants "
        "with at least one submitter and no conflicting interpretations are retained. After "
        "deduplication on (mutant, label) pairs, 421 variants remain: 314 Pathogenic/Likely "
        "Pathogenic (P/LP) and 107 Benign/Likely Benign (B/LB). Table 2 shows per-gene counts. "
        "GBA dominates (n = 240) due to the large literature on GBA variants in Gaucher disease, "
        "the strongest known genetic risk factor for PD. The evaluation metric is AUROC; model "
        "scores are negated before ranking (more negative log-likelihood delta = more damaging)."
    )

    # Table 2 - ClinVar  col_w sums to 160
    # Gene(18) + Mechanism(84) + P/LP(19) + B/LB(19) + Total(20) = 160
    table(
        "Table 2.  ClinVar pathogenicity track per gene (deduplicated, downloaded September 2026).",
        headers=["Gene", "Pathogenic mechanism", "P/LP", "B/LB", "n"],
        rows=[
            ["GBA",   "LOF -- glucocerebrosidase (GD/PD risk)",  "237", "3",  "240"],
            ["LRRK2", "GOF -- kinase hyperactivation",           "10",  "71", "81"],
            ["PRKN",  "LOF -- ubiquitin E3 ligase",              "28",  "14", "42"],
            ["PINK1", "LOF -- mitophagy kinase",                 "21",  "11", "32"],
            ["PARK7", "LOF -- oxidative stress sensor",          "10",  "3",  "13"],
            ["SNCA",  "GOF -- aggregation (hallmark PD)",        "5",   "3",  "8"],
            ["VPS35", "GOF -- retromer complex dysfunction",     "3",   "2",  "5"],
            ["Total", "",                                        "314", "107", "421"],
        ],
        col_w=[18, 84, 19, 19, 20],
    )

    sub_head("2.3  Format and Compatibility")

    para(
        "All DMS files follow ProteinGym substitution CSV format (columns: mutant, DMS_score). "
        "Wildtype sequences, gene metadata, and assay phenotype descriptions are provided in "
        "reference_files/DMS_substitutions.csv. The scoring script score.py implements masked-"
        "marginal scoring (Section 3.1) and accepts any HuggingFace EsmForMaskedLM checkpoint. "
        "Dependencies: transformers, torch, pandas, scipy, numpy. The full DMS track can be "
        "reproduced from scratch in under 2 minutes on a CPU for ESM-2 8M, and under 30 minutes "
        "for ESM-2 650M."
    )

    # ── 3. BASELINE EVALUATION ─────────────────────────────────────────────

    section_head("3.", "Baseline Evaluation")

    sub_head("3.1  Masked-Marginal Scoring")

    para(
        "We use masked-marginal scoring [3], the standard ProteinGym evaluation protocol. For each "
        "position i in the wildtype sequence (1-indexed, excluding special tokens), position i is "
        "masked and a single forward pass computes the log-softmax distribution over the amino acid "
        "vocabulary. The score for variant X->Y at position i is:"
    )

    code("  score(X->Y) = log p(Y | seq with position i masked)\n"
         "              - log p(X | seq with position i masked)")

    para(
        "For multi-mutant variants, per-position log-likelihood deltas are summed. Building the "
        "position cache requires L forward passes (L=140 for SNCA), approximately 1-2 seconds on "
        "CPU for ESM-2 8M and 20-30 seconds for ESM-2 650M. Spearman rank correlation between "
        "model scores and experimental DMS fitness values is the primary DMS track metric."
    )

    sub_head("3.2  Models Evaluated")

    para(
        "We evaluate two ESM-2 checkpoints [4]: 8M parameters (facebook/esm2_t6_8M_UR50D, "
        "6 transformer layers, 320-dim embeddings) and 650M parameters "
        "(facebook/esm2_t33_650M_UR50D, 33 layers, 1280-dim). ESM-2 650M is the largest checkpoint "
        "that achieves peak ProteinGym performance (rho = +0.419) before diminishing returns at 3B "
        "and 15B parameters [1]. Both models use 32-bit float precision and SDPA attention."
    )

    sub_head("3.3  DMS Track Results")

    # Table 3 - Results  col_w sums to 160
    # Assay(70) + ESM-2 8M(28) + ESM-2 650M(32) + n(20) + ... hmm 70+28+32+20 = 150
    # Let's do 72+28+32+28 = 160
    table(
        "Table 3.  ESM-2 masked-marginal Spearman rho on LewyGym DMS track (all assays: SNCA GOF).",
        headers=["Assay", "ESM-2 8M", "ESM-2 650M", "n"],
        rows=[
            ["SNCA_HUMAN_Newberry_2020",    "-0.165", "-0.210", "2,588"],
            ["SNCA_HUMAN_Noh_2026_1pct",    "-0.147", "-0.168", "2,585"],
            ["SNCA_HUMAN_Noh_2026_01pct",   "-0.135", "-0.160", "2,593"],
            ["SNCA_HUMAN_Noh_2026_001pct",  "-0.115", "-0.146", "2,591"],
            ["SNCA_HUMAN_Noh_2026_0001pct", "-0.134", "-0.171", "2,503"],
            ["Mean",                         "-0.139", "-0.171", "12,860"],
        ],
        col_w=[78, 28, 32, 22],
    )
    caption(
        "Table 3. Negative Spearman rho values indicate signal inversion: model conservation scores "
        "anti-correlate with experimental fitness. For comparison, ESM-2 650M achieves +0.419 mean "
        "Spearman rho on ProteinGym's 217-assay substitution benchmark (Notin et al., NeurIPS 2023 "
        "Table A5). The 650M model amplifies the inversion vs 8M (-0.171 vs -0.139) across all five assays. "
        "n values reflect missense-only variants (synonymous excluded per ProteinGym protocol)."
    )

    para(
        "All five SNCA assays yield negative Spearman correlations for both models (Table 3). "
        "ESM-2 650M produces a more negative mean correlation than 8M in all five assays, with "
        "the largest inversion on the Newberry 2020 membrane toxicity assay (rho = -0.210). The "
        "mean DMS track score is -0.139 (8M) and -0.171 (650M), compared to the ProteinGym "
        "substitution benchmark baseline of +0.419 for ESM-2 650M [1] -- a departure of 0.58 "
        "Spearman units, exceeding the full per-assay variation range reported for ESM-2 on ProteinGym. "
        "Note that the yeast system captures membrane-binding GOF; the known fibril-aggregation "
        "variants A30P and G51D are exceptions where this assay and clinical pathogenicity diverge."
    )

    # ── 4. DISCUSSION ──────────────────────────────────────────────────────

    section_head("4.", "Discussion")

    para(
        "The negative Spearman correlations on all five SNCA DMS assays arise from a mechanistic "
        "mismatch between conservation-based scoring and GOF pathogenicity. ESM-2 is trained to "
        "reconstruct masked residues from evolutionary context: residues conserved across UniRef50 "
        "receive high log-likelihood, and unusual substitutions receive low log-likelihood. For "
        "SNCA, the positions most critical for aggregation-driven toxicity are evolutionarily "
        "constrained. The model correctly identifies them as evolutionarily disfavoured, producing "
        "negative log-likelihood deltas for aggregation-promoting variants -- yet in the yeast "
        "DMS assay, these same variants reduce fitness (increase toxicity), and the correlation "
        "inverts. In contrast, substitutions that disrupt aggregation-prone contacts are "
        "evolutionarily unusual but improve yeast fitness, further inverting the signal."
    )

    para(
        "The amplification of the inversion by larger ESM-2 models (650M > 8M) is mechanistically "
        "consistent: larger models learn richer conservation representations and express higher "
        "confidence in penalising evolutionarily unusual residues. As SNCA's GOF-relevant variants "
        "fall precisely in the 'unusual but toxic via aggregation' category, a more confident "
        "conservation model produces a stronger inversion signal. This is distinct from the "
        "behaviour on ProteinGym, where larger ESM-2 models improve LOF prediction because deeper "
        "conservation encoding better captures functional constraint."
    )

    para(
        "These results have three practical implications. First, conservation-based PLMs should "
        "not be used as zero-shot GOF pathogenicity predictors without recalibration or task-"
        "specific fine-tuning. Second, aggregate benchmarks like ProteinGym -- which necessarily "
        "average across heterogeneous proteins -- may obscure systematic failures on GOF disease "
        "proteins. Third, disease-specific benchmarks spanning both GOF and LOF genes within a "
        "coherent disease panel are essential for characterising model behaviour on clinically "
        "actionable variants."
    )

    para(
        "Limitations: LewyGym v0.1 includes DMS data for SNCA only. LRRK2, GBA, and other PD "
        "genes lack large-scale publicly available DMS assays. The ClinVar pathogenicity track "
        "has class imbalance (GBA, n=240, dominates) and very small variant counts for some GOF "
        "genes (SNCA n=8, VPS35 n=5). Planned additions for v0.2 include LRRK2 kinase activity "
        "assays (~70 variants curated from literature), GBA enzyme activity data (~50 variants), "
        "and baselines for ESM-1v [3], AlphaMissense [8], and Evo2 [9]."
    )

    # ── 5. DATA AVAILABILITY ───────────────────────────────────────────────

    section_head("5.", "Data Availability")

    para(
        "All data, code, and results are publicly available at "
        "github.com/Tyronita/LewyGym and huggingface.co/datasets/EvanOLeary/LewyGym "
        "under CC0 (public domain). DMS data are redistributed from MaveDB under their "
        "original CC0 licences. ClinVar data are in the public domain. The scoring "
        "script score.py reproduces all baseline results in Table 3 from the raw CSV files."
    )

    # ── ACKNOWLEDGEMENTS ───────────────────────────────────────────────────

    section_head("", "Acknowledgements")

    para(
        "This benchmark was built for Niall O'Leary Sr., who was diagnosed with Parkinson's disease "
        "and whose experience motivated every design decision here. His involvement as patient "
        "co-investigator kept the work grounded in what matters: understanding the molecular "
        "mechanisms of a disease that affects millions of families, and holding the computational "
        "tools we use to study it to a higher standard."
    )

    # ── REFERENCES ─────────────────────────────────────────────────────────

    section_head("", "References")

    refs = [
        ("1", "Notin, P. et al. ProteinGym: Large-Scale Benchmarks for Protein Fitness Prediction "
              "and Design. NeurIPS Datasets and Benchmarks 2023. doi:10.1101/2023.12.07.570727"),
        ("2", "Dallago, C. et al. FLIP: Benchmark tasks in fitness landscape inference for proteins. "
              "NeurIPS Datasets and Benchmarks 2022."),
        ("3", "Meier, J. et al. Language models enable zero-shot prediction of the effects of "
              "mutations on protein function. NeurIPS 2021. doi:10.1101/2021.07.09.450648"),
        ("4", "Lin, Z. et al. Evolutionary-scale prediction of atomic-level protein structure "
              "with a language model. Science 379, 1123-1130 (2023). doi:10.1126/science.ade2574"),
        ("5", "Newberry, R.W. et al. Deep mutational scanning reveals the structural basis of "
              "alpha-synuclein activity. Nature Chemical Biology 16, 653-659 (2020). "
              "doi:10.1038/s41589-020-0480-6"),
        ("6", "Noh, D. and Newberry, R.W. Concentration-dependent fitness landscape of alpha-synuclein. "
              "Protein Science 2026. doi:10.1002/pro.70456"),
        ("7", "Esposito, D. et al. MaveDB: an open-source platform to distribute and interpret "
              "data from multiplexed assays of variant effect. Genome Biology 20, 223 (2019). "
              "doi:10.1186/s13059-019-1845-6"),
        ("8", "Cheng, J. et al. Accurate proteome-wide missense variant effect prediction with "
              "AlphaMissense. Science 381, eadg7492 (2023). doi:10.1126/science.adg7492"),
        ("9", "Nguyen, E. et al. Sequence modeling and design from molecular to genome scale "
              "with Evo 2. bioRxiv 2024. doi:10.1101/2024.02.27.582234"),
        ("10", "Kryukov, K. et al. Systematic benchmarking of variant effect predictors reveals "
               "class-specific performance differences. Molecular Systems Biology 2023. PMC10407742"),
        ("11", "Fraternali, F. et al. Gain-of-function variants are systematically underperformed "
               "by conservation-based computational predictors. Nature Communications 2022."),
    ]

    for num, txt in refs:
        ref_item(num, txt)

    # ── OUTPUT ─────────────────────────────────────────────────────────────

    out = "/Users/nialloleary/LewyGym/lewygym_preprint.pdf"
    pdf.output(out)
    print(f"Saved {pdf.page} pages -> {out}")
    return out


if __name__ == "__main__":
    build()
