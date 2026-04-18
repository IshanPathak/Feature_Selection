# Feature selection (quantum-assisted pipeline)

## Layout

| Path | Purpose |
|------|---------|
| `notebooks/FS.ipynb` | Full pipeline. Uses **default** profile: writes `results/qubo/qubo_matrix_symmetric.csv`, `results/grid_search/grid_search_results.csv`, etc. |
| `notebooks/FS-Workstation.ipynb` | Same workflow as `FS.ipynb`, but the first cell sets `FS_PROFILE=workstation` so outputs use the **`*-Workstation.*`** filenames and do not overwrite lab runs. |
| `repo_paths.py` | Single place for `data/` and `results/` paths; honors `FS_PROFILE`. |
| `data/raw/` | Merged inputs: `fault_data.csv`, `labeled_fault_data.csv`, `merged_fault_data.csv`. |
| `data/processed/` | Enhanced, augmented, and the main `complex_imbalanced_80k.csv` training table. |
| `data/features/` | Mutual information, permutation importance, top-25 lists, correlation matrices. |
| `results/qubo/` | QUBO matrix CSV + JSON metadata (profile-specific names). |
| `results/grid_search/` | Grid search CSV/JSON/text summaries + `best_results_analysis.md`. |
| `results/checkpoints/` | `checkpoint.pkl`, `quantum_feature_results.pkl`, legacy `gridsearch_state.pkl`. |
| `docs/` | Extra notes (e.g. CSV splitter README). |
| `Documents/` | Papers, PCAPs, references (unchanged). |
| `Codes/` | Stub `README.txt` only after restructure; safe to ignore. |

## Running notebooks

1. Open the project folder in Jupyter/VS Code so the kernel can resolve paths.
2. Run the **first code cell** in the notebook (bootstrap). It sets the working directory to the project root and loads `repo_paths`.
3. Set `IBM_QUANTUM_TOKEN` in the environment (see `.env.example`); do not commit tokens.

## Restructure script

To recreate moves on another clone (after copying raw files into `Codes/`), run:

`python scripts/restructure_project.py`

## Git

Step-by-step instructions (init, first commit, GitHub, daily workflow): **[docs/GIT_WORKFLOW.md](docs/GIT_WORKFLOW.md)**
