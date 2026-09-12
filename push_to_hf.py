"""Push LewyGym datasets to HuggingFace Hub."""
from pathlib import Path
from huggingface_hub import HfApi, create_repo
import pandas as pd

REPO_ID = "Tyronita/LewyGym"
ROOT = Path(__file__).parent

api = HfApi()

# Create repo
try:
    create_repo(REPO_ID, repo_type="dataset", exist_ok=True, private=False)
    print(f"repo ready: {REPO_ID}")
except Exception as e:
    print(f"repo create: {e}")

# Upload dataset card
api.upload_file(
    path_or_fileobj=str(ROOT / "hf_dataset_card.md"),
    path_in_repo="README.md",
    repo_id=REPO_ID, repo_type="dataset"
)

# Upload DMS substitution CSVs
dms_dir = ROOT / "DMS_PDGym_substitutions"
# handle both old and new name
if not dms_dir.exists():
    dms_dir = ROOT / "DMS_LewyGym_substitutions"
if not dms_dir.exists():
    # find it
    dms_dir = next(ROOT.glob("DMS_*substitutions"), None)

if dms_dir:
    for f in sorted(dms_dir.glob("*.csv")):
        api.upload_file(
            path_or_fileobj=str(f),
            path_in_repo=f"substitutions/{f.name}",
            repo_id=REPO_ID, repo_type="dataset"
        )
        print(f"  uploaded substitutions/{f.name}")

# Upload pathogenicity CSVs
for f in sorted((ROOT / "pathogenicity").glob("*.csv")):
    api.upload_file(
        path_or_fileobj=str(f),
        path_in_repo=f"pathogenicity/{f.name}",
        repo_id=REPO_ID, repo_type="dataset"
    )
    print(f"  uploaded pathogenicity/{f.name}")

# Upload reference files
for f in sorted((ROOT / "reference_files").glob("*.csv")):
    api.upload_file(
        path_or_fileobj=str(f),
        path_in_repo=f"reference_files/{f.name}",
        repo_id=REPO_ID, repo_type="dataset"
    )
    print(f"  uploaded reference_files/{f.name}")

print(f"\nDone. View at: https://huggingface.co/datasets/{REPO_ID}")
