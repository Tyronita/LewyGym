"""Build PDGym reference files matching ProteinGym's reference CSV structure."""
import csv
from pathlib import Path

# SNCA wildtype sequence (UniProt P37840, canonical isoform, L=140)
SNCA_WT = "MDVFMKGLSKAKEGVVAAAEKTKQGVAEAAGKTKEGVLYVGSKTKEGVVHGVATVAEKTKEQVTNVGGAVVTGVTAVAQKTVEGAGSIAAATGFVKKDQLGKNEEGAPQEGILEDMPVDPDNEAYEMPSEEGYQDYEPEA"

DMS_ASSAYS = [
    {
        "DMS_id": "SNCA_HUMAN_Newberry_2020",
        "UniProt_ID": "P37840",
        "gene_name": "SNCA",
        "protein_name": "Alpha-synuclein",
        "organism": "Homo sapiens",
        "target_seq": SNCA_WT,
        "seq_len": 140,
        "DMS_filename": "SNCA_HUMAN_Newberry_2020.csv",
        "number_mutants": 2728,
        "DMS_phenotype": "Yeast expression level (GFP fusion) — membrane-bound toxicity readout",
        "DMS_mutant_type": "substitution",
        "DMS_score_type": "fitness",
        "source": "MaveDB urn:mavedb:00000045-k-1",
        "publication": "Newberry et al., Nature Chemical Biology 2020 (doi:10.1038/s41589-020-0480-6)",
        "PD_relevance": "SNCA encodes alpha-synuclein; aggregation causes PD. GOF toxicity mechanism.",
    },
    {
        "DMS_id": "SNCA_HUMAN_Noh_2026_1pct",
        "UniProt_ID": "P37840",
        "gene_name": "SNCA",
        "protein_name": "Alpha-synuclein",
        "organism": "Homo sapiens",
        "target_seq": SNCA_WT,
        "seq_len": 140,
        "DMS_filename": "SNCA_HUMAN_Noh_2026_1pct.csv",
        "number_mutants": 2725,
        "DMS_phenotype": "Yeast fitness at 1% galactose induction (high concentration)",
        "DMS_mutant_type": "substitution",
        "DMS_score_type": "fitness",
        "source": "MaveDB urn:mavedb:00001249-a-1",
        "publication": "Noh et al., Protein Science 2026 (doi:10.1002/pro.70456)",
        "PD_relevance": "Concentration-dependent folding landscape; SNCA duplication/triplication causes familial PD.",
    },
    {
        "DMS_id": "SNCA_HUMAN_Noh_2026_01pct",
        "UniProt_ID": "P37840",
        "gene_name": "SNCA",
        "protein_name": "Alpha-synuclein",
        "organism": "Homo sapiens",
        "target_seq": SNCA_WT,
        "seq_len": 140,
        "DMS_filename": "SNCA_HUMAN_Noh_2026_01pct.csv",
        "number_mutants": 2733,
        "DMS_phenotype": "Yeast fitness at 0.1% galactose induction",
        "DMS_mutant_type": "substitution",
        "DMS_score_type": "fitness",
        "source": "MaveDB urn:mavedb:00001249-a-2",
        "publication": "Noh et al., Protein Science 2026 (doi:10.1002/pro.70456)",
        "PD_relevance": "Concentration-dependent folding landscape.",
    },
    {
        "DMS_id": "SNCA_HUMAN_Noh_2026_001pct",
        "UniProt_ID": "P37840",
        "gene_name": "SNCA",
        "protein_name": "Alpha-synuclein",
        "organism": "Homo sapiens",
        "target_seq": SNCA_WT,
        "seq_len": 140,
        "DMS_filename": "SNCA_HUMAN_Noh_2026_001pct.csv",
        "number_mutants": 2731,
        "DMS_phenotype": "Yeast fitness at 0.01% galactose induction",
        "DMS_mutant_type": "substitution",
        "DMS_score_type": "fitness",
        "source": "MaveDB urn:mavedb:00001249-a-3",
        "publication": "Noh et al., Protein Science 2026 (doi:10.1002/pro.70456)",
        "PD_relevance": "Concentration-dependent folding landscape.",
    },
    {
        "DMS_id": "SNCA_HUMAN_Noh_2026_0001pct",
        "UniProt_ID": "P37840",
        "gene_name": "SNCA",
        "protein_name": "Alpha-synuclein",
        "organism": "Homo sapiens",
        "target_seq": SNCA_WT,
        "seq_len": 140,
        "DMS_filename": "SNCA_HUMAN_Noh_2026_0001pct.csv",
        "number_mutants": 2643,
        "DMS_phenotype": "Yeast fitness at 0.001% galactose induction (low concentration)",
        "DMS_mutant_type": "substitution",
        "DMS_score_type": "fitness",
        "source": "MaveDB urn:mavedb:00001249-a-4",
        "publication": "Noh et al., Protein Science 2026 (doi:10.1002/pro.70456)",
        "PD_relevance": "Concentration-dependent folding landscape.",
    },
]

FIELDS = ["DMS_id","UniProt_ID","gene_name","protein_name","organism","seq_len",
          "number_mutants","DMS_phenotype","DMS_mutant_type","DMS_score_type",
          "source","publication","PD_relevance","DMS_filename","target_seq"]

Path("reference_files").mkdir(exist_ok=True)
with open("reference_files/DMS_substitutions.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=FIELDS)
    w.writeheader()
    w.writerows(DMS_ASSAYS)

print(f"reference_files/DMS_substitutions.csv: {len(DMS_ASSAYS)} assays")
for a in DMS_ASSAYS:
    print(f"  {a['DMS_id']}: {a['number_mutants']} variants")
