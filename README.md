# Feature Selection for Imbalanced Network Intrusion Detection Systems Dataset Using Quantum Annealer

**Repository:** [github.com/IshanPathak/Feature_Selection](https://github.com/IshanPathak/Feature_Selection)

This project builds a **feature-selection pipeline** for tabular intrusion / fault data: classical preprocessing and scoring, a **QUBO** (binary quadratic) problem built from those scores, optimization on **IBM Quantum** hardware via **Qiskit**, and optional **grid search** over hyperparameters. The main code is **`notebooks/FS.ipynb`**.

---

## Step-by-step: how to run (first time)

| Step | Action |
|------|--------|
| 1 | **Clone** this repository to your machine. |
| 2 | Open a terminal in the **project root** (the folder that contains `README.md` and `repo_paths.py`). |
| 3 | **Create a virtual environment** and install dependencies: |
|   | `python -m venv .venv` |
|   | Windows: `.\.venv\Scripts\activate` |
|   | `pip install -r requirements.txt` |
| 4 | **IBM Quantum API token** — required for quantum cells. Get a token at [IBM Quantum](https://quantum.ibm.com/account). Set it **only** in the environment (never commit it): |
|   | PowerShell: `$env:IBM_QUANTUM_TOKEN = "your_token"` |
|   | Or copy `.env.example` to `.env` and load it with your tooling (`.env` is gitignored). |
| 5 | **Large data files** — If you do not already have them, run the **early cells** of `FS.ipynb` to build them, or copy your CSVs into the paths below. Files under `data/raw/` and large `data/processed/` files are **not** stored in Git (see [.gitignore](.gitignore)). |
| 6 | Start **Jupyter**, **VS Code**, or **Cursor** and open **`notebooks/FS.ipynb`**. |
| 7 | Select a Python **kernel** that uses the `.venv` you created. |
| 8 | Run the **first code cell** (bootstrap). It sets the working directory to the project root, loads **`repo_paths` as `rp`**, and sets **`FS_PROFILE`** (default profile in `FS.ipynb`). **Always run this cell before any other code cell.** |
| 9 | Run **all following cells in order** from top to bottom. Skipping a stage will fail later cells unless the files that stage produces already exist on disk. |

**Second machine / avoid overwriting results:** use **`notebooks/FS-Workstation.ipynb`** instead. Its bootstrap sets `FS_PROFILE=workstation` so outputs use filenames like `*-Workstation.csv` and do not overwrite the default run.

**More detail:** [docs/USAGE_AND_PROCESS.md](docs/USAGE_AND_PROCESS.md)

---

## What the code does (pipeline in plain language)

1. **Merge and clean** separate fault and label tables into one dataset.  
2. **Engineer features** (rolling stats, derivatives, etc.) → enhanced table.  
3. **Optionally augment** (noise, shifts, blends) and **sample** to a fixed-size **imbalanced** dataset used for training (`complex_imbalanced_80k.csv` locally).  
4. **Score features** with **mutual information** and **permutation importance** (e.g. Random Forest).  
5. **Intersect** scores, keep **top‑k** names, compute **correlation** on that subset.  
6. **Build a symmetric QUBO matrix** from relevance, redundancy, and cardinality terms + save **metadata** JSON.  
7. **Quantum optimization** on IBM backends to select a feature subset encoded in the QUBO.  
8. **Grid search** (optional): sweep hyperparameters (e.g. `k`, λ, μ, γ), rebuild QUBO per setting, evaluate with a classifier, log accuracy/F1 and timings.

---

## What each file / folder is

| Path | What it is |
|------|------------|
| **`repo_paths.py`** | Single source of truth for folder paths (`data/`, `results/`) and profile-specific filenames. Imports after bootstrap; uses `FS_PROFILE`. |
| **`notebooks/FS.ipynb`** | **Main** notebook: full pipeline, default output names. |
| **`notebooks/FS-Workstation.ipynb`** | Same logic; writes `*-Workstation.*` artifacts. |
| **`requirements.txt`** | Python packages (`pandas`, `numpy`, `scikit-learn`, `qiskit`, `qiskit-ibm-runtime`, …). |
| **`.env.example`** | Shows **`IBM_QUANTUM_TOKEN`** name only — no real secret. |
| **`scripts/restructure_project.py`** | One-time helper to move files into `data/` / `results/` layout (usually not needed on a normal clone). |
| **`docs/USAGE_AND_PROCESS.md`** | Longer usage and troubleshooting. |
| **`docs/GIT_WORKFLOW.md`** | Git commands (commit, push, new remote). |
| **`docs/README_CSV_Splitter.md`** | Optional tool to split huge CSVs by size/rows. |

**Defaults:** If you do not set anything, `FS_PROFILE` behaves as **`default`** (no `-Workstation` suffix on QUBO/grid files). There is **no** default IBM token — you must set **`IBM_QUANTUM_TOKEN`** yourself or quantum cells will fail.

---

## What each CSV (and related) file means

### Local-only large data (usually **not** in Git — regenerate or supply yourself)

| File (under `data/raw/` or `data/processed/`) | Meaning |
|-----------------------------------------------|---------|
| **`fault_data.csv`** | Raw fault-side measurements (features without labels or before merge). |
| **`labeled_fault_data.csv`** | Labels aligned to fault records for merging. |
| **`merged_fault_data.csv`** | Combined fault + label table after merge. |
| **`labeled_fault_data_enhanced.csv`** | Merged data after **feature engineering** (extra columns such as rolling stats). |
| **`augmented_fault_data.csv`** | Large table after **augmentation** (real + synthetic variants). |
| **`complex_imbalanced_80k.csv`** | **Main analysis table** used for MI, PI, correlations, and downstream ML — balanced/sampled to ~80k rows, still **imbalanced** labels. |
| **`selected_80k_samples.csv`** | Optional alternate 80k sample (if your notebook uses it); may be unused depending on your run. |

### Tracked small artifacts — `data/features/` (in repo when committed)

| File | Meaning |
|------|---------|
| **`mutual_info_scores.csv`** | One row per feature: **`Feature`**, **`MI_Score`** (dependence with the label). |
| **`pi_scores_simple_rf.csv`** | **Permutation importance** (e.g. Random Forest): feature name, **`PI_Mean`**, **`PI_Std`**, etc. |
| **`permutation_importance_scores.csv`** | Alternate/legacy PI export if generated; main PI file used by the QUBO build is usually **`pi_scores_simple_rf.csv`**. |
| **`nonzero_features_both.csv`** | Features that are nonzero in **both** MI and PI views, with scores for intersection logic. |
| **`top_25_features.csv`** | Full rows for the **top 25** features chosen for the next stage. |
| **`top_25_feature_names.csv`** | **Only** the 25 feature names (used to subset columns for correlation). |
| **`top25_correlation_matrix.csv`** | **25×25** Pearson (or project default) correlation among the top features; rows/columns are feature names. |
| **`top25_correlation_pairs.csv`** | Pairwise correlation list (long format) for inspection. |

### Results — `results/qubo/`

| File | Meaning |
|------|---------|
| **`qubo_matrix_symmetric.csv`** | **Symmetric QUBO matrix** used by the quantum code (default profile). Index/columns = feature names or indices per notebook convention. |
| **`qubo_metadata.json`** | Small JSON: hyperparameters used to build the matrix, feature list, notes. |
| **`qubo_matrix_symmetric-Workstation.csv`** | Same role when **`FS_PROFILE=workstation`**. |
| **`qubo_metadata-Workstation.json`** | Metadata for workstation profile. |
| **`qubo_parameter_search_results_intermediate.csv`** | **Intermediate** sweep during parameter search (if that cell was run); not required for a minimal end-to-end run. |

### Results — `results/grid_search/`

| File | Meaning |
|------|---------|
| **`grid_search_results.csv`** | One row per **(k, λ, μ, γ)** run: params, **accuracy**, **F1**, **selected_features**, backend, timestamps, quantum/ML/total time. |
| **`grid_search_state.json`** | **Resumable state** for the grid search (what finished, current pointer). |
| **`grid_search_summary.txt`** | Human-readable **summary** of the grid search. |
| **`*-Workstation.*`** | Same roles for the workstation profile. |

### Results — `results/checkpoints/` (optional)

| File | Meaning |
|------|---------|
| **`checkpoint.pkl`** | Optional checkpoint for long quantum optimization loops. |
| **`quantum_feature_results.pkl`** | Saved **final quantum feature-selection** outputs (Python pickle). |
| **`gridsearch_state.pkl`** | Legacy/alternate grid state format if present. |

---

## Git

Daily workflow: [docs/GIT_WORKFLOW.md](docs/GIT_WORKFLOW.md)

**Suggested GitHub “About” description:**  
*Feature selection for imbalanced NIDS data using a QUBO formulation and IBM Quantum (Qiskit).*
