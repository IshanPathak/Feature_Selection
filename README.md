# Feature Selection for Imbalanced Network Intrusion Detection Systems Dataset Using Quantum Annealer

Research codebase for feature selection on an **imbalanced** network-intrusion-style dataset: classical preprocessing and scoring, then a **QUBO** formulation optimized with **IBM Quantum** (Qiskit) to select features, with optional hyperparameter **grid search**.

---

## Full guide (process · run · code)

**Read this first for step-by-step process, how to run the notebook, and how to reuse paths/code:**

### [docs/USAGE_AND_PROCESS.md](docs/USAGE_AND_PROCESS.md)

---

## Quick start

1. **Clone** this repository.
2. **Python environment** (from repo root):

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **IBM Quantum token** — set `IBM_QUANTUM_TOKEN` (see `.env.example`). Never commit secrets.
4. **Large data** — place or generate `data/raw/` and `data/processed/` files locally (they are gitignored). See the usage doc for filenames.
5. Open **`notebooks/FS.ipynb`**, run the **first cell** (bootstrap), then run **cells in order**.

---

## What’s in this repository

| Item | Role |
|------|------|
| [docs/USAGE_AND_PROCESS.md](docs/USAGE_AND_PROCESS.md) | **Process, run instructions, how to use `repo_paths` and profiles** |
| [repo_paths.py](repo_paths.py) | Central paths for `data/` and `results/`; `FS_PROFILE` switches default vs workstation outputs |
| [notebooks/FS.ipynb](notebooks/FS.ipynb) | **Main** pipeline (profile: default) |
| [notebooks/FS-Workstation.ipynb](notebooks/FS-Workstation.ipynb) | Same pipeline; `FS_PROFILE=workstation` → `*-Workstation.*` files |
| [requirements.txt](requirements.txt) | Python dependencies |
| [`.env.example`](.env.example) | Example env var for IBM token only |
| `data/features/`, `results/` | Small/medium artifacts (when committed); large CSVs stay local — see [.gitignore](.gitignore) |

**Git how-to:** [docs/GIT_WORKFLOW.md](docs/GIT_WORKFLOW.md)

---

## Connect this folder to GitHub (after a clean slate)

If you removed the old remote or repo, from the project folder:

```powershell
cd "C:\Users\ishan\OneDrive\Desktop\GRA\Feature Selection"
git init
git add .
git commit -m "Initial commit: quantum feature selection pipeline and docs"
git branch -M main
git remote add origin https://github.com/YOUR_USER/YOUR_REPO.git
git push -u origin main
```

If the repo already exists and only `origin` is missing:

```powershell
git remote add origin https://github.com/YOUR_USER/YOUR_REPO.git
git push -u origin main
```

---

## Suggested GitHub “About” description

*Feature selection for imbalanced NIDS data using a QUBO / quantum annealer formulation (Qiskit, IBM Quantum).*
