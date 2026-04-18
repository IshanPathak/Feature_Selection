# Feature Selection for Imbalanced Network Intrusion Detection Systems Dataset Using Quantum Annealer

Research codebase for feature selection on an imbalanced network-intrusion style dataset, using a **QUBO / quantum-annealing** style formulation (IBM Quantum backends via Qiskit) alongside classical preprocessing and evaluation.

---

## What belongs on GitHub (required vs optional)

This repository is meant to hold **what is needed to understand and reproduce the method**, not multi‑gigabyte raw captures or local-only PDFs.

| Required on the repo | Purpose |
|----------------------|---------|
| **`README.md`** (this file) | Project title, setup, scope |
| **`requirements.txt`** | Python dependencies |
| **`.env.example`** | Shows `IBM_QUANTUM_TOKEN` only — never commit real tokens |
| **`repo_paths.py`** | Paths for `data/` and `results/`; `FS_PROFILE` for default vs workstation outputs |
| **`notebooks/FS.ipynb`** | **Main** end-to-end notebook (run the first cell first) |
| **`data/features/*.csv`** | Small artifacts: MI, PI, top‑25 features, correlation summaries used to build the QUBO |
| **`results/qubo/*`** | Built QUBO matrix and metadata (non‑`*-Workstation*` names for the default profile) |
| **`results/grid_search/*`** | Grid search state, results CSV, summaries (default profile) |

| Optional / secondary | Purpose |
|---------------------|---------|
| **`notebooks/FS-Workstation.ipynb`** | Same pipeline with `FS_PROFILE=workstation` so outputs use `*-Workstation.*` and do not overwrite lab runs |
| **`results/*-Workstation.*`** | Extra runs from another machine |
| **`docs/GIT_WORKFLOW.md`**, **`docs/README_CSV_Splitter.md`** | Tooling notes |
| **`scripts/restructure_project.py`** | One-time folder layout helper |

| Not in Git (by design — large or private) | |
|------------------------------------------|---|
| **`data/raw/`**, **`data/processed/`** large CSVs | Listed in `.gitignore`; obtain or regenerate locally |
| **`Documents/Refrences/`**, conference PDFs/DOCX/PPTX | Local copies only unless you add [Git LFS](https://git-lfs.github.com/) |
| **`Documents/PCAP/`** | Packet captures — too large for normal Git |

If you want the GitHub **repository description** line, use something like:  
*Feature selection for imbalanced NIDS data using a quantum annealer / QUBO formulation (Qiskit).*

---

## Layout (short)

| Path | Role |
|------|------|
| `data/raw/` | Merged inputs (local only unless you change `.gitignore`) |
| `data/processed/` | Enhanced / augmented / `complex_imbalanced_80k.csv` (local) |
| `data/features/` | Scores and top‑25 tables used for QUBO construction (tracked) |
| `results/qubo/` | QUBO matrix + metadata |
| `results/grid_search/` | Hyperparameter search outputs |
| `results/checkpoints/` | Optional `.pkl` checkpoints |

---

## Setup

```powershell
cd "path\to\Feature Selection"
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

Copy `.env.example` to `.env` (or set env vars) and set **`IBM_QUANTUM_TOKEN`** for IBM Quantum access.

## Run

1. Open the project root in Jupyter / VS Code / Cursor.
2. Open **`notebooks/FS.ipynb`** and run the **first code cell** (bootstrap: `repo_paths`, working directory).
3. Run the rest of the notebook in order.

## Restructure script

To replay folder moves after a fresh clone (if you still use the helper):  
`python scripts/restructure_project.py`

## Git

Daily workflow: **[docs/GIT_WORKFLOW.md](docs/GIT_WORKFLOW.md)**
