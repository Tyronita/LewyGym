"""Generate genetic model landscape survey PDF."""
from fpdf import FPDF
import json, textwrap

MARGIN = 22
PW = 210
CONTENT_W = PW - 2 * MARGIN  # 166

class Survey(FPDF):
    def header(self):
        if self.page_no() > 1:
            self.set_font("Times", "I", 8)
            self.set_text_color(120)
            self.cell(0, 5, "O'Leary & O'Leary (2026)  |  Foundational Genetic Language Models: Survey", align="L")
            self.ln(3)
            self.set_text_color(0)
    def footer(self):
        self.set_y(-14)
        self.set_font("Times", "", 9)
        self.set_text_color(120)
        self.cell(0, 8, str(self.page_no()), align="C")
        self.set_text_color(0)

def build():
    pdf = Survey("P", "mm", "A4")
    pdf.set_margins(MARGIN, MARGIN, MARGIN)
    pdf.set_auto_page_break(True, margin=20)
    pdf.add_page()

    def para(txt, size=10, align="J", ln_after=2):
        pdf.set_font("Times", "", size)
        pdf.multi_cell(CONTENT_W, 5.5, txt, align=align)
        if ln_after: pdf.ln(ln_after)

    def section(num, title):
        pdf.ln(5)
        pdf.set_font("Times", "B", 12)
        pdf.multi_cell(CONTENT_W, 7, f"{num}  {title}")
        pdf.set_draw_color(140)
        pdf.set_line_width(0.3)
        pdf.line(MARGIN, pdf.get_y(), PW-MARGIN, pdf.get_y())
        pdf.set_line_width(0.2)
        pdf.set_draw_color(0)
        pdf.ln(3)

    def subsection(title):
        pdf.ln(3)
        pdf.set_font("Times", "B", 10)
        pdf.multi_cell(CONTENT_W, 6, title)
        pdf.ln(1)

    def caption(txt):
        pdf.set_font("Times", "I", 8)
        pdf.multi_cell(CONTENT_W, 4.5, txt)
        pdf.ln(3)

    def bullet(txt, indent=5, size=9.5):
        pdf.set_font("Times", "", size)
        pdf.set_x(MARGIN + indent)
        pdf.cell(4, 5.5, "-")
        pdf.set_x(MARGIN + indent + 4)
        pdf.multi_cell(CONTENT_W - indent - 4, 5.5, txt, align="J")
        pdf.set_x(MARGIN)
        pdf.ln(0.5)

    # ── compact table helpers ─────────────────────────────────────────────
    def tbl_header(headers, col_w, fsize=7.5):
        pdf.set_font("Times", "B", fsize)
        pdf.set_fill_color(210, 210, 215)
        for h, w in zip(headers, col_w):
            pdf.cell(w, 5.5, h, border=1, fill=True, align="C")
        pdf.ln()

    def tbl_row(cells, col_w, fsize=7, fill=False, bold=False):
        pdf.set_fill_color(248, 248, 250) if fill else pdf.set_fill_color(255,255,255)
        pdf.set_font("Times", "B" if bold else "", fsize)
        for i, (txt, w) in enumerate(zip(cells, col_w)):
            al = "L" if i == 0 else "C"
            # Truncate long text to fit
            max_chars = int(w / 1.55)
            if len(str(txt)) > max_chars:
                txt = str(txt)[:max_chars-2] + ".."
            pdf.cell(w, 5, str(txt), border=1, fill=True, align=al)
        pdf.ln()

    # =====================================================================
    # TITLE
    # =====================================================================
    pdf.set_font("Times", "B", 17)
    pdf.multi_cell(CONTENT_W, 9,
        "Foundational Genetic and Protein Language Models:\n"
        "A Taxonomy of Training Data, Architecture,\n"
        "Scaling Laws, and the Data Bottleneck",
        align="C")
    pdf.ln(3)
    pdf.set_font("Times", "B", 11)
    pdf.multi_cell(CONTENT_W, 6, "Evan O'Leary  and  Niall O'Leary", align="C")
    pdf.set_font("Times", "I", 9)
    pdf.multi_cell(CONTENT_W, 5, "Independent researchers  |  evan.oleary99@gmail.com", align="C")
    pdf.ln(1)
    pdf.set_font("Times", "", 8.5)
    pdf.multi_cell(CONTENT_W, 5,
        "bioRxiv preprint  *  September 2026  *  Companion survey to LewyGym (github.com/Tyronita/LewyGym)",
        align="C")
    pdf.ln(4)
    pdf.set_line_width(0.5)
    pdf.line(MARGIN, pdf.get_y(), PW-MARGIN, pdf.get_y())
    pdf.set_line_width(0.2)
    pdf.ln(5)

    # =====================================================================
    # ABSTRACT
    # =====================================================================
    pdf.set_font("Times", "B", 10)
    pdf.cell(0, 6, "Abstract")
    pdf.ln(1)
    pdf.set_font("Times", "", 9)
    pdf.set_fill_color(248, 248, 248)
    pdf.multi_cell(CONTENT_W, 5,
        "We survey 25 foundational biological language models spanning protein sequence "
        "(ESM family, ProtTrans, ProGen/ProGen2, RITA, AMPLIFY, Tranception, EVE, SaProt, "
        "AlphaMissense, ESM-IF), DNA/genomic (DNABERT/2, Nucleotide Transformer v1/v2, "
        "HyenaDNA, Caduceus, Evo, Evo 2), and multimodal (ESM-3) modalities, cataloguing "
        "their training datasets, architectures, parameter counts, perplexity at scale, and "
        "downstream benchmark performance. We find that: (1) protein MLM scaling exponents "
        "(N_opt ~ C^0.77) differ substantially from text LLMs (~C^0.50), meaning existing "
        "large protein models are systematically undertrained; (2) zero-shot fitness prediction "
        "on ProteinGym peaks at ~650M-4B parameters and then declines, with a parameter-free "
        "evolutionary statistics method (RSALOR, rho=0.582) outperforming all neural models "
        "including 40B-parameter Evo 2 (rho=0.360); (3) genomic DNA models have solved the "
        "long-range context problem via subquadratic architectures (StripedHyena, Mamba), "
        "with Evo 2 achieving 1M single-nucleotide context; and (4) the primary bottleneck "
        "is not compute or architecture but data diversity -- the 1.17B truly novel MGnify "
        "dark proteome sequences remain largely untapped, the UniRef diversity ratio declines "
        "yearly, and no RNA foundation model exists. We frame these findings in the context "
        "of disease-specific protein variant prediction, motivated by the LewyGym benchmark "
        "showing that gain-of-function proteins systematically invert conservation-based "
        "scoring signals.",
        border=1, fill=True, align="J")
    pdf.ln(2)
    pdf.set_font("Times", "I", 8.5)
    pdf.multi_cell(CONTENT_W, 5,
        "Keywords: protein language model, genomic language model, scaling laws, "
        "deep mutational scanning, variant effect prediction, data bottleneck")
    pdf.ln(4)
    pdf.set_draw_color(170); pdf.line(MARGIN, pdf.get_y(), PW-MARGIN, pdf.get_y()); pdf.set_draw_color(0)

    # =====================================================================
    # 1. INTRODUCTION
    # =====================================================================
    section("1.", "Introduction")

    para(
        "Biological language models -- pretrained neural networks operating on sequences of "
        "amino acids or nucleotides -- have emerged as the dominant paradigm for zero-shot "
        "prediction of protein fitness, variant pathogenicity, and molecular function [1-4]. "
        "The field has bifurcated into two complementary tracks: protein language models (PLMs) "
        "operating on amino acid vocabularies of 20-441 tokens, and genomic DNA/RNA language "
        "models operating on nucleotide vocabularies of 4-4096 tokens. Both tracks have "
        "rapidly scaled from hundreds of millions to hundreds of billions of parameters between "
        "2021 and 2026."
    )

    para(
        "Despite this rapid growth, no comprehensive survey has examined the full landscape "
        "of training datasets, architectural choices, scaling law behaviour, and fundamental "
        "bottlenecks across both tracks simultaneously. Existing reviews focus on either "
        "protein [5] or genomic [6] models separately and do not systematically characterise "
        "the data-efficiency frontier or identify the point at which additional compute "
        "ceases to improve downstream task performance."
    )

    para(
        "This survey is motivated by an empirical finding from our companion work, LewyGym "
        "[7]: ESM-2 650M achieves Spearman rho = -0.17 on alpha-synuclein (SNCA) variant "
        "fitness prediction, compared to +0.414 on ProteinGym's loss-of-function benchmark. "
        "Understanding why this inversion occurs -- and what training signals would be required "
        "to correct it -- requires understanding the full landscape of available models, "
        "datasets, and their respective limitations."
    )

    # =====================================================================
    # 2. PROTEIN LANGUAGE MODELS
    # =====================================================================
    section("2.", "Protein Language Models")

    subsection("2.1  ESM Family (Meta AI / EvolutionaryScale)")

    para(
        "The ESM series represents the most systematically studied protein LM scaling "
        "trajectory. ESM-1 (2021) established that biological structure and function emerge "
        "from masked language modelling on 250M protein sequences without structural "
        "supervision [1]. ESM-1b introduced Pre-LN stabilisation at 650M parameters. "
        "ESM-1v redirected the architecture toward variant effect prediction by training "
        "on the more diverse UniRef90 (98M sequences) rather than UniRef50, achieving "
        "Spearman rho = 0.510 across 41 DMS datasets with an ensemble of 5 models [2]. "
        "ESM-2 replaced absolute position embeddings with Rotary Position Embeddings (RoPE), "
        "removed dropout entirely, and systematically scaled from 8M to 15B parameters, "
        "establishing the first clean protein-specific scaling law (r = -0.99 between "
        "perplexity and CASP14 TM-score across all six scales) [1]. ESM-3 (2024) extended "
        "the framework to joint multimodal generation over sequence, structure, and function "
        "tokens, training on 3.15 billion proteins and 771 billion tokens [3]. ESM Cambrian "
        "(2024) demonstrated that modern architecture (RoPE + SwiGLU + no biases) plus "
        "metagenomic data allows the 300M-parameter ESM C to match the 650M ESM-2, "
        "training on 6.2 trillion tokens including 2 billion JGI metagenomic clusters."
    )

    subsection("2.2  ProtTrans Family (Rostlab / TU Munich)")

    para(
        "The ProtTrans suite [8] systematically evaluated four NLP architectures (BERT, "
        "ALBERT, XLNet, T5) on protein sequences, providing the first large-scale evidence "
        "that (a) bidirectional MLM outperforms autoregressive permutation LM (ProtXLNet "
        "Q3=73 vs ProtBERT Q3=75-76), and (b) metagenomic data (BFD, 2.1B sequences, "
        "393B tokens) consistently improves over curated databases (UniRef100, 216M "
        "sequences) across all downstream tasks. ProtT5-XL (3B) trained on BFD then "
        "fine-tuned on UniRef50 achieves Q3 secondary structure = 81, the best single-"
        "sequence result in the suite."
    )

    subsection("2.3  Generative Protein Models (ProGen, ProGen2, RITA, ProtGPT2)")

    para(
        "Generative protein models take a GPT-style decoder-only autoregressive approach. "
        "ProGen (Salesforce, 1.2B, 2020) introduced conditional generation via control tags. "
        "RITA (LightOn, 2022) provided the most systematic autoregressive scaling study: "
        "85M to 1.2B parameters on UniRef-100 with RoPE, finding a scaling exponent of "
        "0.74 (loss vs model size) -- steeper than natural language (~0.50) -- and "
        "perplexity 5.48 on UniRef-100 for RITA-XL [9]. ProGen2 (Salesforce, 2022) scaled "
        "to 6.4B parameters on UniRef90 + BFD30 using GPT-J with RoPE, achieving monotonic "
        "perplexity improvement (small 12.9 -> xlarge 9.9) but non-monotonic zero-shot "
        "fitness -- ProGen2-base (764M) marginally outperforms xlarge (6.4B) on ProteinGym "
        "Spearman (0.505 vs 0.476) [10]. ProtGPT2 (738M, 2022) showed that GPT-2 style "
        "training on 44.9M UniRef50 sequences generates structurally plausible proteins "
        "but achieves poor perplexity (18.10 on UniRef-100 vs RITA-XL 5.48)."
    )

    subsection("2.4  Efficiency Frontier (AMPLIFY, xTrimoPGLM)")

    para(
        "AMPLIFY (Mila / Amgen, 2024) demonstrated that modern architectural components "
        "(RMSNorm, SwiGLU, RoPE, FlashAttention) combined with deduplicated training "
        "data (UR100P: 391M sequences) allow AMPLIFY-350M to outperform ESM-2 15B on "
        "ProteinGym benchmarks with 43x fewer parameters and 17x fewer FLOPs [11]. "
        "xTrimoPGLM (Tsinghua / BAAI, 2024) scaled a GLM encoder-decoder to 100B "
        "parameters on ~1 trillion tokens, achieving state-of-the-art across 18 benchmarks."
    )

    # Table: Protein Models
    pdf.ln(2)
    pdf.set_font("Times", "B", 9)
    pdf.cell(0, 5, "Table 1.  Protein language models -- architecture, training data, and key performance metrics.")
    pdf.ln(1)
    # col_w must sum to CONTENT_W = 166
    # Name(36) + Year(10) + Params(22) + Data(32) + Perplexity(18) + ProtGym(16) = 134 ... need 166
    # Name(40) + Year(10) + Params(26) + Data(36) + Perplexity(20) + ProtGym(18) + Arch(16) = 166
    cw = [40, 10, 26, 36, 20, 18, 16]
    tbl_header(["Model", "Yr", "Parameters", "Training Data", "Perplexity", "ProtGym rho", "Arch"], cw)
    rows = [
        ("ESM-1 / ESM-1b",     "2021", "43M-670M",       "UniRef50 250M seqs",       "n/r",        "-",      "BERT"),
        ("ESM-1v",             "2021", "650M x5",         "UniRef90 98M seqs",         "7.29",       "0.510",  "BERT"),
        ("MSA Transformer",    "2021", "100M",            "UniRef50 MSAs",             "n/r",        "0.434",  "Axial"),
        ("ESM-2",              "2022", "8M-15B",          "UniRef50/90 ~1T tok",       "6.37@15B",   "0.414",  "BERT+RoPE"),
        ("ProtBERT / BFD",     "2021", "420M",            "UniRef100 / BFD 393B tok",  "n/r",        "-",      "BERT"),
        ("ProtT5-XL",          "2021", "3B / 11B",        "BFD 393B, UR50 finetune",   "n/r",        "0.51*",  "T5+Enc"),
        ("ProtGPT2",           "2022", "738M",            "UniRef50 44.9M seqs",       "18.10*",     "-",      "GPT-2"),
        ("RITA-XL",            "2022", "1.2B",            "UniRef-100 280M seqs",      "5.48",       "-",      "GPT+RoPE"),
        ("ProGen2-xlarge",     "2022", "6.4B",            "UR90 + BFD30 ~180M seqs",   "9.9",        "0.476",  "GPT-J+RoPE"),
        ("Tranception-L",      "2022", "700M",            "UniRef100 250M seqs",       "n/r",        "0.457*", "GPT+conv"),
        ("EVE",                "2021", "~M / protein",    "Per-protein MSAs",          "n/r (ELBO)", "0.441",  "VAE"),
        ("AlphaMissense",      "2023", "n/d (AF2-scale)", "AF2 data + gnomAD pop freq","n/a (clf)",  "0.474",  "AF2 finetune"),
        ("SaProt-650M",        "2023", "650M",            "40M AF2 structs (3Di tok)", "n/r",        "0.478",  "ESM-2+SA vocab"),
        ("ESM-3 (1.4B open)",  "2024", "1.4B-98B",        "3.15B seqs, 771B tokens",   "0.895 LDDT", "0.466",  "Multi-modal"),
        ("ESM C (6B)",         "2024", "300M-6B",         "6.2T tok incl JGI 2B",      "n/r",        ">ESM-2", "BERT+RoPE"),
        ("AMPLIFY-350M",       "2024", "120M / 350M",     "UR100P 391M seqs",          "n/r",        ">ESM-2 15B","BERT+RMSNorm"),
        ("xTrimoPGLM",         "2024", "100B",            "UR90+ColdFold ~1T tokens",  "10.81",      "SOTA",   "GLM-100B"),
    ]
    for i, row in enumerate(rows):
        tbl_row(row, cw, fsize=7, fill=(i%2==1))
    caption(
        "Table 1. Protein LMs surveyed. ProtGym rho = mean Spearman on ProteinGym substitution benchmark "
        "(zero-shot). n/r = not reported; n/d = not disclosed; n/a = not applicable; * = VESPA/ProtT5 proxy; "
        "Tranception* = with retrieval; EVE is per-protein, not a global model. "
        "Arch: BERT = bidirectional MLM encoder; GPT = autoregressive decoder; T5 = encoder-decoder; "
        "RoPE = Rotary Position Embeddings; SA = structure-aware vocabulary."
    )

    # =====================================================================
    # 3. DNA / GENOMIC LANGUAGE MODELS
    # =====================================================================
    section("3.", "DNA and Genomic Language Models")

    para(
        "DNA language models face a qualitatively different challenge from protein LMs: "
        "the genomic sequence space is less information-dense (4-letter alphabet vs 20), "
        "regulatory signals operate at long range (enhancers 100kb-1Mb from target genes), "
        "and the same sequence encodes multiple overlapping functional elements in both "
        "strands. Early models (DNABERT, 2021) applied BERT to k-mers from the single "
        "human reference genome, demonstrating chromatin accessibility (AUROC 0.85) and "
        "methylation prediction. The dominant recent trend is architectural: subquadratic "
        "alternatives to attention (Hyena, Mamba/SSM) enable single-nucleotide context "
        "of 1M+ base pairs, which transformers cannot achieve at any practical scale."
    )

    subsection("3.1  k-mer to Single-Nucleotide Tokenization")

    para(
        "DNABERT (2021) used k-mer tokenization (k=3-6) with 512-token context (~3kb), "
        "limiting coverage to short regulatory elements. DNABERT-2 (2023) replaced fixed "
        "k-mers with BPE tokenization over 135 species (32.5B nucleotides), achieving 5x "
        "compression and enabling context extension; at 117M parameters it matches the "
        "2.5B Nucleotide Transformer on 28-task GUE benchmark using 21x fewer parameters "
        "and 92x less GPU time. Nucleotide Transformer v1 (InstaDeep/EMBL-EBI, 2023) "
        "scaled to 2.5B parameters with 6-mer tokenization over 850 diverse genomes; "
        "NT-v2 (2023) replaced learned absolute positions with RoPE and SwiGLU, matching "
        "NT-v1-2500M performance at 5x smaller model size."
    )

    subsection("3.2  Subquadratic Architectures: Hyena and Mamba")

    para(
        "HyenaDNA (Hazy Research, 2023) replaced self-attention with Hyena implicit "
        "convolutions (O(L log L)), enabling 1M-bp single-nucleotide context at only 6.6M "
        "parameters. Trained on the single human reference genome, it outperforms models "
        "1,500x larger on most GenomicBenchmarks tasks by exploiting long-range dependencies "
        "inaccessible to k-mer attention models [12]. Caduceus (Cornell, 2024) added "
        "bidirectionality and reverse-complement equivariance to Mamba/SSM blocks, improving "
        "HyenaDNA on double-stranded DNA tasks by encoding both strands symmetrically."
    )

    subsection("3.3  Genomic Foundation Models at Scale (Evo, Evo 2)")

    para(
        "Evo (Arc Institute, 2024, 7B parameters) trained StripedHyena on 300B tokens "
        "of prokaryotic and phage genomes (OpenGenome), enabling zero-shot CRISPR guide "
        "RNA activity and gene essentiality prediction [13]. Evo 2 (2025, up to 40B "
        "parameters) extended to all three domains of life via OpenGenome2 (8.85T "
        "nucleotides, 15,032 eukaryotic + 113,379 prokaryotic genomes), achieving 1M "
        "single-nucleotide context and state-of-the-art noncoding variant effect prediction "
        "(ClinVar noncoding AUROC, ranked 1st). Perplexity 2.597 at 1M context (7B), "
        "vs Transformer baseline 3.09 at identical scale."
    )

    # Table: DNA Models
    pdf.set_font("Times", "B", 9)
    pdf.cell(0, 5, "Table 2.  DNA and genomic language models.")
    pdf.ln(1)
    # Name(36)+Yr(9)+Params(20)+Tokeniz(22)+Training Data(36)+Context(16)+Key(27)=166
    cw2 = [36, 9, 20, 22, 36, 16, 27]
    tbl_header(["Model", "Yr", "Parameters", "Tokenization", "Training Data", "Context", "Architecture"], cw2)
    dna_rows = [
        ("DNABERT",          "2021", "~86-89M",   "k-mer (k=3-6)",    "hg38 (3.2B nt)",          "512 tok / ~3kb",   "BERT, fixed pos"),
        ("DNABERT-2",        "2023", "117M",      "BPE (4096 vocab)",  "135 species 32.5B nt",    "Ext. (ALiBi)",     "MosaicBERT+ALiBi"),
        ("NT v1-2500M-multi","2023", "500M/2.5B", "6-mer (4105 vocab)","850 genomes 174B nt",     "6kb (1000 tok)",   "BERT, learned pos"),
        ("NT v2-500M",       "2023", "50M-2.5B",  "6-mer",            "Human+multi 300B-1T tok",  "12kb (2000 tok)",  "BERT+RoPE+SwiGLU"),
        ("HyenaDNA",         "2023", "0.4M-6.6M", "Single-nucleotide","hg38 only (~3B nt)",       "1M bp",            "Hyena (O(L logL))"),
        ("Caduceus",         "2024", "~7.7M",     "Single-nucleotide","hg38 (~3B nt)",            "131,072 nt",       "BiMamba+RC equiv"),
        ("Evo (Evo 1)",      "2024", "7B",        "Single-nucleotide","OpenGenome 300B tok",      "131,072 nt",       "StripedHyena"),
        ("Evo 2",            "2025", "1B-40B",    "Single-nucleotide","OpenGenome2 8.85T nt",     "1,048,576 nt (1M)","StripedHyena 2"),
    ]
    for i, row in enumerate(dna_rows):
        tbl_row(row, cw2, fsize=7, fill=(i%2==1))
    caption("Table 2. RC equiv = reverse-complement equivariant; BiMamba = bidirectional Mamba/SSM.")

    # =====================================================================
    # 4. ARCHITECTURE CHOICES
    # =====================================================================
    section("4.", "Architecture Choices and Their Consequences")

    subsection("4.1  BERT vs GPT vs T5 for Proteins")

    para(
        "The protein modelling literature has decisively favoured bidirectional MLM encoders "
        "(BERT-style) over autoregressive decoders (GPT-style) for representation learning "
        "and zero-shot fitness prediction. ProtXLNet (autoregressive permutation LM) "
        "underperforms ProtBERT (bidirectional MLM) across all tasks in the ProtTrans "
        "suite [8], and ProGen2-xlarge (6.4B GPT) underperforms AMPLIFY-350M (modern BERT) "
        "on ProteinGym despite being 18x larger. The T5 encoder-decoder hybrid performs well "
        "for per-residue prediction tasks (ProtT5 Q3 = 81) but is rarely used for "
        "generation tasks due to training complexity. For protein generation, GPT-style "
        "models are necessary and have scaled effectively (ProGen2, RITA)."
    )

    subsection("4.2  Position Embeddings: Absolute vs RoPE vs ALiBi")

    para(
        "Rotary Position Embeddings (RoPE) have become the default for all recent protein "
        "and genomic models. ESM-2 introduced RoPE to the protein domain; RITA, ProGen2, "
        "NT-v2, and Evo 2 all use RoPE. ALiBi (additive bias in attention scores) is used "
        "by DNABERT-2 to allow context-length extrapolation beyond training length. Learned "
        "absolute position embeddings (ESM-1b, DNABERT, NT-v1) hard-code maximum context "
        "length and impair extrapolation. The shift to RoPE enabled NT-v2 to double context "
        "from 6kb to 12kb relative to NT-v1 without additional parameters."
    )

    subsection("4.3  Activation Functions and Normalisation")

    para(
        "AMPLIFY's analysis isolates the architecture improvement specifically: "
        "replacing GeLU with SwiGLU and LayerNorm with RMSNorm, combined with removing "
        "biases, yields AMPLIFY-350M outperforming ESM-2 15B at 43x fewer parameters. "
        "The gap is partly attributable to FLOPs efficiency (17x fewer) and partly to "
        "data quality (UR100P vs the 2021 UniRef50 release used by ESM-2). "
        "Disentangling architecture from data quality improvements remains difficult."
    )

    subsection("4.4  Subquadratic Architectures for Long Context")

    para(
        "Transformers require O(L^2) memory and compute for context length L, preventing "
        "practical use beyond ~16k tokens. The Hyena operator (implicit long convolutions, "
        "O(L log L)) enables HyenaDNA's 1M-bp single-nucleotide context at 6.6M parameters. "
        "Mamba/SSM-based models (Caduceus) provide linear-time sequence modelling with "
        "selective state transitions, adding reverse-complement equivariance for genomics. "
        "StripedHyena (Evo 1/2) interleaves Hyena convolutions with sparse MHA layers, "
        "running 3x faster than pure Transformers at 1M context while improving perplexity "
        "(2.597 vs Transformer baseline 3.09 at 7B scale)."
    )

    subsection("4.5  Structure-Aware Vocabulary (SaProt)")

    para(
        "SaProt (2023) achieved the most parameter-efficient improvement on ProteinGym "
        "(rho = 0.478, ranked #1) by a single architectural change: replacing the standard "
        "20-amino-acid vocabulary with 441 structure-aware (SA) tokens pairing each residue "
        "with its Foldseek 3Di structural state. No changes to the ESM-2 transformer "
        "architecture. This demonstrates that vocabulary design is an underexplored "
        "efficiency dimension: the same number of parameters encodes qualitatively richer "
        "information when tokens carry structural context."
    )

    # =====================================================================
    # 5. SCALING LAWS: PERPLEXITY VS PARAMETERS
    # =====================================================================
    section("5.", "Scaling Laws: Perplexity, Parameters, and Data Tokens")

    subsection("5.1  ESM-2 Protein Scaling Law")

    para(
        "ESM-2 provides the cleanest protein-specific scaling law: validation perplexity "
        "decreases from 10.45 (8M parameters) to 6.37 (15B parameters) with Pearson "
        "r = -0.99 between log(perplexity) and downstream CASP14 TM-score across all "
        "six scale points [1]. This near-perfect correlation confirms that perplexity is "
        "a reliable proxy for structural accuracy in protein MLMs -- a result not "
        "guaranteed a priori and not observed in natural language."
    )

    pdf.set_font("Times", "B", 9)
    pdf.cell(0, 5, "Table 3.  ESM-2 perplexity and structure accuracy across scale.")
    pdf.ln(1)
    cw3 = [30, 20, 28, 38, 36, 14]
    tbl_header(["Model", "Parameters", "Perplexity", "Contact P@L/5", "ESMFold CAMEO", "Layers"], cw3)
    esm2_rows = [
        ("ESM-2 8M",   "8M",   "10.45", "15.9",  "-",     "6"),
        ("ESM-2 35M",  "35M",  "~9.8",  "25.7",  "-",     "12"),
        ("ESM-2 150M", "150M", "~9.0",  "33.3",  "-",     "30"),
        ("ESM-2 650M", "650M", "~8.2",  "44.4",  "0.865", "33"),
        ("ESM-2 3B",   "3B",   "~7.4",  "52.0",  "-",     "36"),
        ("ESM-2 15B",  "15B",  "6.37",  "54.5",  "0.871 (TM 72.1)", "48"),
    ]
    for i, row in enumerate(esm2_rows):
        tbl_row(row, cw3, fsize=7.5, fill=(i%2==1))
    caption("Table 3. ESM-2 validation perplexity and downstream metrics. CAMEO = CAMEO structure "
            "benchmark mean TM-score or LDDT depending on source. Contact P@L/5 = long-range precision.")
    pdf.ln(2)

    subsection("5.2  Compute-Optimal Protein Scaling")

    para(
        "The NeurIPS 2024 study by Cheng et al. [14] derived compute-optimal scaling laws "
        "for protein LMs across 300+ models from 3.5M to 10.7B parameters: the optimal "
        "model size scales as N_opt ~ C^0.77 and optimal tokens as D_opt ~ C^0.23 "
        "(MLM objective). The contrast with Chinchilla's text exponents (~0.50/0.50) "
        "is striking: protein MLMs should be far more parameter-heavy relative to "
        "data tokens than text LLMs. A corollary is that ESM-2 3B (trained on ~1T "
        "tokens, ~45 epochs of UniRef50) is severely overtrained -- a compute-optimal "
        "allocation would train a 10.7B model on 260B unique tokens and match or exceed "
        "ESM-2 3B's performance at lower total FLOPs."
    )

    para(
        "A competing analysis by Serrano et al. [15] trained 35M-parameter models on "
        "yearly UniRef100 snapshots (2011-2024) and found N_opt ~ C^0.27, D_opt ~ C^0.71 "
        "-- the opposite recommendation. The disagreement likely reflects dataset "
        "composition: Cheng et al. used UniMeta200B with 52.5% metagenomic sequences "
        "(high diversity), while Serrano et al. used UniRef-only data (increasing "
        "redundancy). This implies the compute-optimal allocation is itself "
        "data-composition-dependent -- a dataset of diverse metagenomes prescribes "
        "larger models, while a dataset of redundant curated sequences prescribes more data."
    )

    subsection("5.3  ProteinGym Scaling Ceiling")

    para(
        "Zero-shot fitness prediction on ProteinGym does not follow the perplexity "
        "scaling law beyond ~650M-4B parameters. ESM-2 3B and 15B do not improve "
        "over 650M on ProteinGym zero-shot Spearman. ESM-3 at 98B achieves 0.466 -- "
        "comparable to ESM-2 650M (0.414) and substantially below the current SOTA "
        "(AIDO Protein-RAG 16B: 0.518). Most strikingly, a parameter-free evolutionary "
        "statistics method, RSALOR (Riesselman-style MSA + structural contacts), "
        "achieves Spearman rho = 0.582 -- outperforming all neural models at any scale, "
        "including 40B-parameter Evo 2 (rho = 0.360) [16]. Of 46 downstream tasks, "
        "only 39% show predictable monotonic scaling behaviour; the remainder are "
        "nonmonotonic, inverse, or trendless."
    )

    # =====================================================================
    # 6. DOES DATA SCALE-OUT WORK?
    # =====================================================================
    section("6.", "Does Data Scale-Out Work?")

    subsection("6.1  UniRef Diversity Ratio Decline")

    para(
        "UniRef100 has grown 33-fold from 11.7M (2011) to 390.8M (2024) sequences, "
        "yet performance gains from training on newer snapshots are non-monotonic. "
        "AMPLIFY's scaling study [11] finds a consistent performance drop between "
        "2018 and 2021 UniRef100 snapshots despite adding ~130M sequences. The "
        "UniRef90/UniRef100 diversity ratio declines each year, indicating that new "
        "sequences are increasingly redundant with existing ones. Redundant training "
        "epochs waste compute and can degrade performance via effective overfitting. "
        "The implication is that naive data accumulation within the UniRef paradigm "
        "has saturated -- diversity, not volume, is the limiting factor."
    )

    subsection("6.2  Metagenomics Breaks the Saturation")

    para(
        "Incorporating metagenomic sequences breaks UniRef saturation. ProtBERT-BFD "
        "(trained on 2.1B BFD sequences including metagenomics) outperforms ProtBERT "
        "(216M UniRef100) on all tasks. ESM C's JGI-augmented training (2B clusters, "
        "32% of 6.2T tokens) enables 300M ESM C to match 650M ESM-2. The NeurIPS 2024 "
        "compute-optimal study used UniMeta200B (52.5% metagenomic), and a 2025 "
        "bioRxiv preprint claims global metagenomics adds ~4x the currently known "
        "protein family space. Yet MGnify alone has >5.7B non-redundant sequences, "
        "of which 1.17B have no similarity to any reference genome or Pfam family -- "
        "the 'dark proteome.' Only a fraction of this has been included in any "
        "published PLM training run."
    )

    subsection("6.3  Dataset Taxonomy")

    pdf.set_font("Times", "B", 9)
    pdf.cell(0, 5, "Table 4.  Training dataset taxonomy across biological sequence modalities.")
    pdf.ln(1)
    # Name(40)+Type(20)+Size(26)+Used_by(48)+Notes(32) = 166
    cw4 = [40, 20, 26, 48, 32]
    tbl_header(["Dataset", "Type", "Size", "Used by (models)", "Key note"], cw4)
    ds_rows = [
        ("UniRef50",         "Protein seq", "53-65M seqs, ~20B tok",  "ESM-2, ESM-1b, ProtGPT2",               "ESM-2 uses as frame, draws from UR90 clusters"),
        ("UniRef90",         "Protein seq", "98M-250M seqs",          "ESM-1v, ProGen2, xTrimoPGLM",           "More diverse than UR50"),
        ("UniRef100",        "Protein seq", "11.7M(2011)-391M(2024)", "ProtBERT, RITA, Tranception, AMPLIFY",   "33x growth; diversity ratio declining"),
        ("BFD",              "Protein seq", "2.1B seqs, 393B tokens", "ProtBERT-BFD, ProtT5-XL, ProGen2(BFD30)","Metagenomic; BFD-trained always beats UniRef"),
        ("MGnify",           "Protein seq", ">5.7B seqs (growing)",   "ESM C (372M clusters)",                  "1.17B truly novel 'dark proteome' untapped"),
        ("JGI",              "Protein seq", "2B clusters at 70% SI",  "ESM C only",                             "Only PLM to use JGI; soil/freshwater/marine"),
        ("UniMeta200B",      "Protein seq", "939M seqs, 194B tokens", "Compute-Optimal NeurIPS 2024",           "52.5% metagenomic; first compute-optimal corpus"),
        ("AFDB (40M)",       "Structure",   "~40M AF2 predictions",   "SaProt (3Di tokens)",                    "3Di tok: structure-aware vocab at no extra inference cost"),
        ("ESMAtlas",         "Structure",   "617M predicted structs",  "ESM-3",                                  "Metagenomic dark proteome with predicted structures"),
        ("hg38",             "DNA",         "3.2B nucleotides",       "DNABERT, HyenaDNA, Caduceus",            "Single genome; sufficient for long-context archi."),
        ("1000 Genomes",     "DNA",         "3,202 human genomes",    "NT v1 (1000g variants)",                 "Captures population SNP diversity"),
        ("NT-multi (850)",   "DNA",         "174B nt, 850 genomes",   "NT v1, NT v2",                           "Multi-species cross-genome conservation"),
        ("DNABERT-2 multi",  "DNA",         "32.5B nt, 135 species",  "DNABERT-2",                              "BPE tokenization; 5x compression vs raw nt"),
        ("OpenGenome",       "DNA",         "300B tokens",            "Evo (Evo 1)",                            "Prokaryote+phage only; excludes eukaryotes"),
        ("OpenGenome2",      "DNA",         "8.85T nucleotides",      "Evo 2",                                  "All 3 domains of life; 30x OpenGenome"),
        ("ProteinGym",       "Annotation",  "217 assays, 2.7M vars",  "Benchmark (all major models)",           "De facto standard; RSALOR 0.582 > all neural models"),
    ]
    for i, row in enumerate(ds_rows):
        tbl_row(row, cw4, fsize=6.8, fill=(i%2==1))
    caption("Table 4. SI = sequence identity. AFDB = AlphaFold Database. UniMeta200B is the only purpose-built compute-optimal corpus; all others were constructed for prior research goals.")

    # =====================================================================
    # 7. THE BOTTLENECK
    # =====================================================================
    section("7.", "The Bottleneck: Where the Ceiling Is")

    para(
        "Synthesising the evidence above, the field faces five compounding bottlenecks. "
        "None is primarily a compute or architecture problem."
    )

    bullets = [
        ("DATA REDUNDANCY IN UNIREF: The dominant protein training corpus (UniRef) adds "
         "increasingly similar sequences each year. Training on newer UniRef100 releases "
         "can degrade model performance due to effective overfitting on near-identical "
         "sequences. Metagenomics (BFD, MGnify, JGI) breaks this ceiling but has not "
         "been fully incorporated into any training corpus. The 1.17B MGnify dark "
         "proteome sequences -- genuinely novel, no Pfam hit -- represent the largest "
         "unexploited reservoir of protein diversity."),
        ("ANNOTATION GAP: Unannotated protein sequences grow exponentially (metagenomics), "
         "while experimentally annotated sequences (SwissProt GO/EC terms, DMS fitness "
         "assays) grow only linearly. All supervised fine-tuning, fitness prediction, and "
         "pathogenicity classification tasks depend on this shrinking annotated fraction. "
         "No current model architecture solves this -- it is a data collection problem."),
        ("PROTEINGYM SATURATION AT ~4B PARAMETERS: Zero-shot fitness prediction peaks at "
         "~650M-4B parameters and declines with further scaling. A parameter-free MSA "
         "method (RSALOR, rho=0.582) outperforms the 40B-parameter Evo 2 (rho=0.360). "
         "This ceiling is consistent with the theoretical limit on pairwise epistasis "
         "encoding and implies that overcoming it requires rethinking the training "
         "objective, not scaling the existing one."),
        ("GAIN-OF-FUNCTION BLIND SPOT: All conservation-based PLMs are systematically "
         "miscalibrated for GOF disease proteins. The LewyGym finding (ESM-2 rho=-0.17 "
         "on SNCA vs +0.414 on LOF proteins) quantifies this for Parkinson's disease. "
         "No existing training dataset provides aggregation-specific DMS data at "
         "scale that would allow models to learn the GOF signal. This is simultaneously "
         "a data gap and a training objective gap."),
        ("RNA AND EUKARYOTIC DARK MATTER: No foundation model analogous to ESM-2 exists "
         "for RNA (despite 27M+ non-redundant sequences in RNAcentral and >4,000 Rfam "
         "families). Eukaryotic metagenomics (protists, micro-algae, fungi) is one "
         "order of magnitude less sequenced than prokaryotic metagenomics. Evo 2 is the "
         "first genomic LM to include eukaryotes at scale, with only months of published "
         "results."),
    ]

    for b in bullets:
        bullet(b, indent=4, size=9.5)
        pdf.ln(1)

    # =====================================================================
    # 8. UNTAPPED DATA SOURCES
    # =====================================================================
    section("8.", "Untapped Training Data")

    para(
        "Table 5 summarises data sources that exist but have not been fully incorporated "
        "into any published PLM training run, ranked by estimated impact."
    )

    pdf.set_font("Times", "B", 9)
    pdf.cell(0, 5, "Table 5.  Untapped training data sources and their potential impact.")
    pdf.ln(1)
    # Source(50)+Size(30)+Why(86) = 166
    cw5 = [46, 28, 92]
    tbl_header(["Source", "Scale", "Why valuable / why unused"], cw5)
    untapped = [
        ("MGnify dark proteome (no Pfam/ref hit)", "1.17B seqs", "Truly novel folds/functions, globally diverse. Only fraction in ESM C (372M clusters). Growing fastest of all databases."),
        ("Global metagenomics expansion", "~4x known protein families", "2025 preprint claims 4x protein family space in metagenomes. Would break UniRef saturation definitively."),
        ("JGI (soil/freshwater/marine microbiomes)", "2B clusters at 70% SI", "Only ESM C uses JGI. Orthogonal diversity to MGnify (different ecosystems, different metabolic niches)."),
        ("Viral proteomes (eukaryote-infecting)", ">330K viral genomes (IMG/VR)", "Excluded by design from Evo 1/2. Viral proteins have distinct evolutionary pressures. No viral PLM exists."),
        ("SNCA/PD aggregation DMS (to be generated)", "~2,660 SNCA variants", "Direct aggregation measurements would enable GOF-calibrated models. Does not exist publicly at scale."),
        ("RNA sequences (RNAcentral, Rfam)", ">27M non-redundant RNAs", "No RNA foundation model exists. Non-coding RNAs are >90% of the transcriptome by count in complex eukaryotes."),
        ("Eukaryotic metagenomics (MetaEuk, MERC)", "Tens of millions of eukaryotic genes", "Eukaryotic microbes (protists, algae, fungi) are 10x undersequenced vs prokaryotes. ~65% of algal proteins uncharacterized."),
        ("Structural annotations via ESMFold at scale", ">5B seqs remaining", "SaProt shows 3Di tokens double contact prediction performance. Only 40M structures used; 5B+ MGnify seqs await."),
    ]
    for i, row in enumerate(untapped):
        tbl_row(row, cw5, fsize=7, fill=(i%2==1))
    caption("Table 5. Evo 1/2 explicitly excludes eukaryote-infecting viruses 'by design.' SNCA aggregation DMS "
            "does not yet exist publicly at the scale needed for model training.")

    # =====================================================================
    # 9. DISCUSSION
    # =====================================================================
    section("9.", "Discussion and Outlook")

    para(
        "The biological language model field has achieved remarkable progress in structural "
        "representation (ESMFold TM-score 0.72 on CAMEO) and genomic modelling (Evo 2 "
        "1M-bp context), but has encountered a systematic ceiling in the task most "
        "directly relevant to human disease: zero-shot variant effect prediction. The "
        "ceiling is mechanistically interpretable: PLMs trained on evolutionary conservation "
        "encode pairwise sequence statistics that correlate with fitness for loss-of-function "
        "proteins but invert for gain-of-function disease proteins. No amount of scaling "
        "within the current training paradigm resolves this."
    )

    para(
        "The path forward bifurcates. For GOF proteins specifically (SNCA/PD, SOD1/ALS, "
        "APP/Alzheimer's), the required training signal is aggregation-specific DMS data -- "
        "a data generation problem, not a model architecture problem. For the broader "
        "fitness prediction ceiling, the evidence points toward rethinking training "
        "objectives to encode higher-order epistasis rather than pairwise correlations. "
        "SaProt demonstrates that vocabulary design (441 SA tokens vs 20 amino acids) "
        "is a tractable efficiency lever. RSALOR's dominance on ProteinGym suggests "
        "explicit structural contact information, not just sequence statistics, is the "
        "missing inductive bias."
    )

    para(
        "The genomic track faces a different frontier: eukaryotic regulatory biology "
        "at chromosome scale. Evo 2 has established 1M-bp context and eukaryotic "
        "pretraining; the challenge is now accumulating sufficient annotated eukaryotic "
        "variant data (regulatory element function, splicing QTLs, enhancer-promoter "
        "links) to fine-tune these models for clinical variant interpretation."
    )

    # =====================================================================
    # 10. REFERENCES
    # =====================================================================
    section("", "References")

    refs = [
        ("1", "Lin, Z. et al. Evolutionary-scale prediction of atomic-level protein structure with a language model. Science 379, 1123-1130 (2023). doi:10.1126/science.ade2574"),
        ("2", "Meier, J. et al. Language models enable zero-shot prediction of the effects of mutations on protein function. NeurIPS 2021. doi:10.1101/2021.07.09.450648"),
        ("3", "Hayes, T. et al. Simulating 500 million years of evolution with a language model. Science 2024 (ESM-3). doi:10.1101/2024.07.01.600583"),
        ("4", "Notin, P. et al. ProteinGym: Large-Scale Benchmarks for Protein Fitness Prediction and Design. NeurIPS 2023. doi:10.1101/2023.12.07.570727"),
        ("5", "Unsal, S. et al. Learning functional properties of proteins with language models. Nature Machine Intelligence 2022."),
        ("6", "Consens, M. et al. To transformers and beyond: large language models for the genome. arXiv 2023."),
        ("7", "O'Leary, E. & O'Leary, N. LewyGym: A Parkinson's Disease Protein Variant Effect Benchmark. bioRxiv 2026."),
        ("8", "Elnaggar, A. et al. ProtTrans: Toward Understanding the Language of Life Through Self-Supervised Learning. IEEE TPAMI 2022. doi:10.1109/TPAMI.2021.3095381"),
        ("9", "Hesslow, D. et al. RITA: a Study on Scaling Up Generative Protein Sequence Models. arXiv:2205.05789 (2022)."),
        ("10","Nijkamp, E. et al. ProGen2: Exploring the Boundaries of Protein Language Models. Cell Systems 2023. doi:10.1016/j.cels.2023.10.002"),
        ("11","Fournier, Q. et al. Protein Language Models are Scalable and Compute-Efficient Sequence Encoders. AMPLIFY. bioRxiv 2024."),
        ("12","Nguyen, E. et al. HyenaDNA: Long-Range Genomic Sequence Modeling at Single Nucleotide Resolution. NeurIPS 2023."),
        ("13","Nguyen, E. et al. Sequence modeling and design from molecular to genome scale with Evo. Science 2024. doi:10.1126/science.ado9336"),
        ("14","Cheng, X. et al. Compute-Optimal Training Strategies for Protein Language Models. NeurIPS 2024."),
        ("15","Serrano, E. et al. Scaling and Data Saturation in Protein Language Models. arXiv:2507.22210 (2025)."),
        ("16","Laine, E. et al. RSALOR: Rapid Structure-Augmented Log-Odds Ratio for variant effect prediction. bioRxiv 2024."),
        ("17","Su, J. et al. SaProt: Protein Language Modeling with Structure-Aware Vocabulary. ICLR 2024."),
        ("18","Cheng, J. et al. AlphaMissense: Accurate proteome-wide missense variant effect prediction. Science 2023. doi:10.1126/science.adg7492"),
        ("19","Fraternali, F. et al. EVE: Evolutionary model of Variant Effect. Nature 2021. doi:10.1038/s41586-021-04043-8"),
    ]

    for num, txt in refs:
        pdf.set_font("Times", "", 8.5)
        pdf.set_x(MARGIN)
        pdf.cell(9, 5, f"[{num}]", align="R")
        pdf.set_x(MARGIN + 10)
        pdf.multi_cell(CONTENT_W - 10, 4.8, txt)
        pdf.ln(0.5)

    out = "/Users/nialloleary/LewyGym/lewygym_survey.pdf"
    pdf.output(out)
    print(f"Saved {pdf.page} pages -> {out}")

if __name__ == "__main__":
    build()
