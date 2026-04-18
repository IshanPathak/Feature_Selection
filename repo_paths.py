"""
Central paths for the quantum feature-selection project.

Set environment variable FS_PROFILE before importing (default / lab machine):
  - default: writes qubo_matrix_symmetric.csv, grid_search_results.csv, etc.
  - workstation: writes *-Workstation.csv/json so runs do not overwrite lab results.

Example (first cell in notebook):
    import os
    os.environ["FS_PROFILE"] = "workstation"
"""
from __future__ import annotations

import os
from pathlib import Path

ROOT: Path = Path(__file__).resolve().parent

_profile = os.environ.get("FS_PROFILE", "default").strip().lower()
SUFFIX = "-Workstation" if _profile == "workstation" else ""

DATA_RAW = ROOT / "data" / "raw"
DATA_PROCESSED = ROOT / "data" / "processed"
DATA_FEATURES = ROOT / "data" / "features"
RESULTS_QUBO = ROOT / "results" / "qubo"
RESULTS_GRID = ROOT / "results" / "grid_search"
RESULTS_CHECKPOINTS = ROOT / "results" / "checkpoints"

COMPLEX_80K = DATA_PROCESSED / "complex_imbalanced_80k.csv"

MI_SCORES = DATA_FEATURES / "mutual_info_scores.csv"
PI_SCORES_RF = DATA_FEATURES / "pi_scores_simple_rf.csv"
NONZERO_BOTH = DATA_FEATURES / "nonzero_features_both.csv"
TOP25_FEATURES = DATA_FEATURES / "top_25_features.csv"
TOP25_NAMES = DATA_FEATURES / "top_25_feature_names.csv"
TOP25_CORR_MAT = DATA_FEATURES / "top25_correlation_matrix.csv"
TOP25_CORR_PAIRS = DATA_FEATURES / "top25_correlation_pairs.csv"

QUBO_MATRIX = RESULTS_QUBO / f"qubo_matrix_symmetric{SUFFIX}.csv"
QUBO_META = RESULTS_QUBO / f"qubo_metadata{SUFFIX}.json"
GRID_RESULTS = RESULTS_GRID / f"grid_search_results{SUFFIX}.csv"
GRID_STATE = RESULTS_GRID / f"grid_search_state{SUFFIX}.json"
GRID_SUMMARY = RESULTS_GRID / f"grid_search_summary{SUFFIX}.txt"

CHECKPOINT_PKL = RESULTS_CHECKPOINTS / "checkpoint.pkl"
QUANTUM_RESULTS_PKL = RESULTS_CHECKPOINTS / "quantum_feature_results.pkl"

for _dir in (
    DATA_RAW,
    DATA_PROCESSED,
    DATA_FEATURES,
    RESULTS_QUBO,
    RESULTS_GRID,
    RESULTS_CHECKPOINTS,
):
    _dir.mkdir(parents=True, exist_ok=True)
