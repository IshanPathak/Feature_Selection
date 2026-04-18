# Usage, process, and how to run

This document explains **what the pipeline does**, **in what order**, **how to run it**, and **how to reuse the code** in your own scripts.

---

## 1. What this project does

You start from **tabular fault / intrusion-style features** and a **label** (e.g. `Fault_Label`). The workflow:

1. **Classical prep** — merge raw tables, engineer features, optionally augment, then build a fixed-size **imbalanced** dataset (`complex_imbalanced_80k.csv` locally under `data/processed/`).
2. **Classical scoring** — mutual information, permutation importance, correlation among top features → small CSVs under `data/features/`.
3. **QUBO construction** — combine relevance, redundancy, and cardinality into a **QUBO matrix** (`results/qubo/`).
4. **Quantum-assisted selection** — optimize on IBM Quantum hardware (Qiskit Runtime) to pick a subset of features; optional **grid search** over hyperparameters (`results/grid_search/`).

The main implementation lives in **`notebooks/FS.ipynb`**. **`notebooks/FS-Workstation.ipynb`** is the same idea but writes `*-Workstation.*` files so a second machine does not overwrite your main results.

---

## 2. End-to-end process (notebook order)

Run cells **from top to bottom** after the bootstrap cell. Typical stages (names may vary slightly in the notebook):

| Stage | What happens | Main outputs (paths) |
|--------|----------------|----------------------|
| Merge labels | Combine fault + label CSVs | `data/raw/merged_fault_data.csv` (local) |
| Enhancement | Feature engineering on merged data | `data/processed/labeled_fault_data_enhanced.csv` (local) |
| Augmentation | Noise/shift/blend → large augmented set | `data/processed/augmented_fault_data.csv` (local, large) |
| Balanced 80k | Stratified / complex sampling | `data/processed/complex_imbalanced_80k.csv` (local) |
| Mutual information | MI vs label | `data/features/mutual_info_scores.csv` |
| Permutation importance | PI (e.g. Random Forest) | `data/features/pi_scores_simple_rf.csv` |
| Intersection / top-25 | Combine MI & PI, pick top features | `data/features/nonzero_features_both.csv`, `top_25_*.csv` |
| Correlation | Top-25 correlation matrix | `data/features/top25_correlation_*.csv` |
| Build QUBO | Assemble symmetric QUBO from MI, PI, R | `results/qubo/qubo_matrix_symmetric.csv`, `qubo_metadata.json` |
| Quantum feature selection | VQE/QAOA-style loop on IBM backend | checkpoints / `quantum_feature_results.pkl` |
| Grid search | Sweep k, λ, μ, γ; train evaluator | `results/grid_search/grid_search_results.csv`, `grid_search_state.json` |

**Important:** Large CSVs are **gitignored**. After cloning the repo you must **place your own copies** under `data/raw/` and `data/processed/` (or rerun the early notebook cells to regenerate them).

---

## 3. Prerequisites

- **Python 3.10+** recommended (match what you used for development).
- **Install dependencies** (from project root):

  ```powershell
  python -m venv .venv
  .\.venv\Scripts\activate
  pip install -r requirements.txt
  ```

- **IBM Quantum** — create an API token at [IBM Quantum](https://quantum.ibm.com/account). **Never commit the token.**

  **PowerShell (current session):**

  ```powershell
  $env:IBM_QUANTUM_TOKEN = "paste_token_here"
  ```

  Or copy `.env.example` to `.env` and load with your tooling (do not commit `.env`).

- **Disk space** — augmented and processed CSVs can be **many GB**; keep them outside Git or on a large drive.

---

## 4. How to run (step by step)

1. **Clone** the repository (or copy the project folder).
2. **Create venv** and `pip install -r requirements.txt` (see above).
3. **Set `IBM_QUANTUM_TOKEN`** before any quantum cells.
4. Open **`notebooks/FS.ipynb`** in Jupyter, VS Code, or Cursor.
5. **Run the first code cell** (bootstrap). It:
   - Finds the **project root** (folder that contains `repo_paths.py`),
   - Sets `os.chdir` to that root,
   - Sets `FS_PROFILE` (`default` in `FS.ipynb`; `workstation` in `FS-Workstation.ipynb`),
   - Imports **`repo_paths`** as `rp` so all paths resolve to `data/` and `results/`.
6. **Run subsequent cells in order.** Skipping stages that build files will break later cells unless those files already exist locally.

**Kernel:** Use a kernel that points to the venv where you installed `requirements.txt`.

---

## 5. How to use the code (reuse patterns)

### 5.1 Paths — always go through `repo_paths`

After the bootstrap cell, use **`rp`** instead of hardcoded paths:

```python
import repo_paths as rp

# Main training table (local file; must exist on disk)
df = pd.read_csv(rp.COMPLEX_80K)

# Feature artifacts
mi = pd.read_csv(rp.MI_SCORES, index_col=0)

# QUBO + grid outputs (profile-dependent names)
print(rp.QUBO_MATRIX)      # default: .../qubo_matrix_symmetric.csv
print(rp.GRID_RESULTS)     # default: .../grid_search_results.csv
```

**Profiles:**

- **`FS_PROFILE` unset or `default`** — unsuffixed filenames.
- **`FS_PROFILE=workstation`** — filenames end with `-Workstation` before the extension.

Set **before** `import repo_paths` (the bootstrap cell does this for you):

```python
import os
os.environ["FS_PROFILE"] = "workstation"
import importlib
import repo_paths as rp
importlib.reload(rp)
```

### 5.2 Adding your own script

From the project root:

```python
import sys
from pathlib import Path
root = Path(__file__).resolve().parent  # if script in project root
sys.path.insert(0, str(root))
import repo_paths as rp

df = pd.read_csv(rp.DATA_FEATURES / "mutual_info_scores.csv", index_col=0)
```

Keep scripts under `scripts/` or project root and run them with `python script.py` from the repo root so imports stay simple.

### 5.3 Restructure helper

If you ever need to replay the folder layout from an old flat `Codes/` dump:

```powershell
python scripts/restructure_project.py
```

(Usually not needed for a normal clone.)

---

## 6. Two notebooks — when to use which

| Notebook | Use when |
|----------|----------|
| **`FS.ipynb`** | Normal runs; writes standard `results/qubo/` and `results/grid_search/` names. |
| **`FS-Workstation.ipynb`** | Second PC or long runs where you must **not** overwrite the main QUBO/grid files — uses `*-Workstation.*` outputs. |

---

## 7. Troubleshooting

| Problem | What to check |
|---------|----------------|
| `FileNotFoundError` for `complex_imbalanced_80k.csv` | File must exist under `data/processed/`; run earlier notebook stages or copy data in. |
| `IBM_QUANTUM_TOKEN` / auth errors | Token set in env; not expired; account has access to chosen backends. |
| Wrong output filenames | `FS_PROFILE`: default vs `workstation` and `importlib.reload(rp)` after changing it. |
| Paths point to wrong folder | Always run the **bootstrap cell first** so `os.chdir` is the project root. |

---

## 8. Related docs

- **[README.md](../README.md)** — overview and repo layout.
- **[GIT_WORKFLOW.md](GIT_WORKFLOW.md)** — Git init, commit, push.
- **[README_CSV_Splitter.md](README_CSV_Splitter.md)** — splitting huge CSVs (if you use that tool).
