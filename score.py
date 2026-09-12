"""LewyGym scoring — masked-marginal ESM-2 over PD variant datasets.

Spearman track:  python score.py --model 650M --assays all
AUROC track:     python score.py --model 650M --track pathogenicity
Smoke test:      python score.py --model 8M --assay SNCA_HUMAN_Newberry_2020
"""
from __future__ import annotations
import argparse, json
from pathlib import Path
import numpy as np
import torch

HF = {
    "8M":   "facebook/esm2_t6_8M_UR50D",
    "35M":  "facebook/esm2_t12_35M_UR50D",
    "650M": "facebook/esm2_t33_650M_UR50D",
}

ROOT    = Path(__file__).parent
DMS_DIR = ROOT / "DMS_LewyGym_substitutions"
PATH_DIR = ROOT / "pathogenicity"
REF_CSV = ROOT / "reference_files" / "DMS_substitutions.csv"


def load_model(model: str, device: str):
    from transformers import AutoTokenizer, EsmForMaskedLM
    tok = AutoTokenizer.from_pretrained(HF[model])
    m = EsmForMaskedLM.from_pretrained(
        HF[model], attn_implementation="sdpa", dtype=torch.float32
    ).eval().to(device)
    return tok, m


@torch.no_grad()
def masked_marginal(tok, m, wt: str, device: str) -> dict[int, torch.Tensor]:
    """One forward pass per position → log-softmax distribution. O(L²) tokens."""
    enc = tok(wt, return_tensors="pt").to(device)
    ids = enc["input_ids"]
    cache = {}
    for i in range(1, ids.shape[1] - 1):
        mi = ids.clone()
        mi[0, i] = tok.mask_token_id
        logits = m(input_ids=mi).logits[0, i].float()
        if device == "cuda":
            torch.cuda.synchronize()
        cache[i] = torch.log_softmax(logits, -1)
    return cache


def score_variant(mutant: str, wt: str, cache: dict, tok) -> float:
    total = 0.0
    for one in mutant.split(":"):
        wt_aa, pos, mt_aa = one[0], int(one[1:-1]), one[-1]
        assert wt[pos - 1] == wt_aa, f"ref mismatch at {pos}: expected {wt_aa}, got {wt[pos-1]}"
        lp = cache[pos]
        total += (lp[tok.convert_tokens_to_ids(mt_aa)]
                - lp[tok.convert_tokens_to_ids(wt_aa)]).item()
    return total


def run_dms(args):
    import pandas as pd
    from scipy.stats import spearmanr

    ref = pd.read_csv(REF_CSV)
    if args.assay != "all":
        ref = ref[ref.DMS_id == args.assay]
        if ref.empty:
            raise SystemExit(f"unknown assay '{args.assay}'. Options: {list(pd.read_csv(REF_CSV).DMS_id)}")

    device = "cuda" if torch.cuda.is_available() else "cpu"
    tok, model = load_model(args.model, device)
    results = {}

    for _, row in ref.iterrows():
        f = DMS_DIR / row.DMS_filename
        if not f.exists():
            print(f"  skip {row.DMS_id} — file not found"); continue
        df = pd.read_csv(f)
        wt = row.target_seq
        print(f"\n{row.DMS_id}  L={row.seq_len}  n={len(df)}")
        cache = masked_marginal(tok, model, wt, device)
        preds, actuals = [], []
        for _, vrow in df.iterrows():
            try:
                s = score_variant(vrow.mutant, wt, cache, tok)
                preds.append(s); actuals.append(vrow.DMS_score)
            except AssertionError as e:
                print(f"    skip {vrow.mutant}: {e}")
        rho = spearmanr(preds, actuals).correlation
        results[row.DMS_id] = {"spearman": rho, "n": len(preds)}
        print(f"  Spearman rho = {rho:+.3f}  (n={len(preds)})")

    print(f"\n{'='*50}")
    print(f"Mean Spearman: {np.mean([v['spearman'] for v in results.values()]):+.3f}")
    Path("results").mkdir(exist_ok=True)
    Path(f"results/dms_{args.model}.json").write_text(json.dumps(results, indent=2))


def run_pathogenicity(args):
    import pandas as pd
    from sklearn.metrics import roc_auc_score

    device = "cuda" if torch.cuda.is_available() else "cpu"
    tok, model = load_model(args.model, device)

    # UniProt sequences for each gene — wildtype
    SEQUENCES = {
        "lrrk2": open(ROOT / "reference_files" / "LRRK2_HUMAN.fasta").read().split("\n", 1)[1].replace("\n", "") if (ROOT / "reference_files" / "LRRK2_HUMAN.fasta").exists() else None,
        "gba":   None,  # add fasta to reference_files/
        "prkn":  None,
        "pink1": None,
        "snca":  "MDVFMKGLSKAKEGVVAAAEKTKQGVAEAAGKTKEGVLYVGSKTKEGVVHGVATVAEKTKEQVTNVGGAVVTGVTAVAQKTVEGAGSIAAATGFVKKDQLGKNEEGAPQEGILEDMPVDPDNEAYEMPSEEGYQDYEPEA",
        "park7": None,
        "vps35": None,
    }

    results = {}
    for csvf in sorted(PATH_DIR.glob("clinvar_*_missense.csv")):
        gene = csvf.stem.replace("clinvar_", "").replace("_missense", "")
        wt = SEQUENCES.get(gene)
        if wt is None:
            print(f"  skip {gene} — no wildtype sequence (add to reference_files/{gene.upper()}_HUMAN.fasta)")
            continue
        df = pd.read_csv(csvf)
        cache = masked_marginal(tok, model, wt, device)
        preds, labels = [], []
        for _, row in df.iterrows():
            try:
                s = score_variant(row.mutant, wt, cache, tok)
                preds.append(-s)   # more negative delta = more damaging
                labels.append(row.label)
            except (AssertionError, KeyError):
                pass
        if len(set(labels)) < 2:
            print(f"  skip {gene} — only one class after filtering"); continue
        auroc = roc_auc_score(labels, preds)
        results[gene] = {"auroc": auroc, "n": len(preds)}
        print(f"  {gene:<8} AUROC={auroc:.3f}  n={len(preds)}")

    print(f"\nMean AUROC: {np.mean([v['auroc'] for v in results.values()]):.3f}")
    Path("results").mkdir(exist_ok=True)
    Path(f"results/pathogenicity_{args.model}.json").write_text(json.dumps(results, indent=2))


def main():
    ap = argparse.ArgumentParser(prog="lewygym score")
    ap.add_argument("--model",  default="8M", choices=list(HF))
    ap.add_argument("--track",  default="dms", choices=["dms", "pathogenicity"])
    ap.add_argument("--assay",  default="all", help="DMS_id or 'all'")
    a = ap.parse_args()
    if a.track == "dms":
        run_dms(a)
    else:
        run_pathogenicity(a)


if __name__ == "__main__":
    main()
