"""
Create data/ + results/ layout, move artifacts out of Codes/, patch notebooks.
Run from project root:

    python scripts/restructure_project.py
"""
from __future__ import annotations

import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CODES = ROOT / "Codes"
NOTEBOOKS = ROOT / "notebooks"
DOCS = ROOT / "docs"

MOVES: list[tuple[str, str]] = [
    ("Codes/fault_data.csv", "data/raw/fault_data.csv"),
    ("Codes/labeled_fault_data.csv", "data/raw/labeled_fault_data.csv"),
    ("Codes/merged_fault_data.csv", "data/raw/merged_fault_data.csv"),
    ("Codes/labeled_fault_data_enhanced.csv", "data/processed/labeled_fault_data_enhanced.csv"),
    ("Codes/augmented_fault_data.csv", "data/processed/augmented_fault_data.csv"),
    ("Codes/complex_imbalanced_80k.csv", "data/processed/complex_imbalanced_80k.csv"),
    ("Codes/selected_80k_samples.csv", "data/processed/selected_80k_samples.csv"),
    ("Codes/mutual_info_scores.csv", "data/features/mutual_info_scores.csv"),
    ("Codes/pi_scores_simple_rf.csv", "data/features/pi_scores_simple_rf.csv"),
    ("Codes/permutation_importance_scores.csv", "data/features/permutation_importance_scores.csv"),
    ("Codes/nonzero_features_both.csv", "data/features/nonzero_features_both.csv"),
    ("Codes/top_25_features.csv", "data/features/top_25_features.csv"),
    ("Codes/top_25_feature_names.csv", "data/features/top_25_feature_names.csv"),
    ("Codes/top25_correlation_matrix.csv", "data/features/top25_correlation_matrix.csv"),
    ("Codes/top25_correlation_pairs.csv", "data/features/top25_correlation_pairs.csv"),
    ("Codes/qubo_matrix_symmetric.csv", "results/qubo/qubo_matrix_symmetric.csv"),
    ("Codes/qubo_metadata.json", "results/qubo/qubo_metadata.json"),
    ("Codes/qubo_matrix_symmetric-Workstation.csv", "results/qubo/qubo_matrix_symmetric-Workstation.csv"),
    ("Codes/qubo_metadata-Workstation.json", "results/qubo/qubo_metadata-Workstation.json"),
    ("Codes/qubo_parameter_search_results_intermediate.csv", "results/qubo/qubo_parameter_search_results_intermediate.csv"),
    ("Codes/grid_search_results.csv", "results/grid_search/grid_search_results.csv"),
    ("Codes/grid_search_state.json", "results/grid_search/grid_search_state.json"),
    ("Codes/grid_search_results-Workstation.csv", "results/grid_search/grid_search_results-Workstation.csv"),
    ("Codes/grid_search_state-Workstation.json", "results/grid_search/grid_search_state-Workstation.json"),
    ("Codes/grid_search_summary.txt", "results/grid_search/grid_search_summary.txt"),
    ("Codes/grid_search_summary-Workstation.txt", "results/grid_search/grid_search_summary-Workstation.txt"),
    ("Codes/best_results_analysis.md", "results/grid_search/best_results_analysis.md"),
    ("Codes/quantum_feature_results.pkl", "results/checkpoints/quantum_feature_results.pkl"),
    ("Codes/gridsearch_state.pkl", "results/checkpoints/gridsearch_state.pkl"),
    ("Codes/README_CSV_Splitter.md", "docs/README_CSV_Splitter.md"),
]

BOOTSTRAP_DEFAULT = """# RUN THIS CELL FIRST — project root + path profile (default / lab machine)
import importlib
import os
import sys
from pathlib import Path

_root = Path.cwd().resolve()
if _root.name == "notebooks":
    _root = _root.parent
if not (_root / "repo_paths.py").exists():
    _root = _root.parent
sys.path.insert(0, str(_root))
os.chdir(_root)

os.environ["FS_PROFILE"] = "default"

import repo_paths as rp
importlib.reload(rp)
print("ROOT:", rp.ROOT)
print("FS_PROFILE:", os.environ.get("FS_PROFILE"))
print("QUBO file:", rp.QUBO_MATRIX)
"""

BOOTSTRAP_WORKSTATION = BOOTSTRAP_DEFAULT.replace(
    'os.environ["FS_PROFILE"] = "default"',
    'os.environ["FS_PROFILE"] = "workstation"',
)


def _bootstrap_source_lines(text: str) -> list[str]:
    return [line + "\n" for line in text.splitlines()]


def patch_notebook(path: Path, profile: str) -> None:
    with path.open(encoding="utf-8") as f:
        nb = json.load(f)

    boot = BOOTSTRAP_DEFAULT if profile == "default" else BOOTSTRAP_WORKSTATION
    nb["cells"].insert(
        0,
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": _bootstrap_source_lines(boot),
        },
    )

    replacements: list[tuple[str, str]] = [
        (
            'fault_data_path = r"C:\\Users\\ishan\\OneDrive\\Desktop\\Feature Selection\\fault_data.csv"',
            'fault_data_path = str(rp.DATA_RAW / "fault_data.csv")',
        ),
        (
            'label_data_path = r"C:\\Users\\ishan\\OneDrive\\Desktop\\Feature Selection\\labeled_fault_data.csv"',
            'label_data_path = str(rp.DATA_RAW / "labeled_fault_data.csv")',
        ),
        (
            'output_path = r"C:\\Users\\ishan\\OneDrive\\Desktop\\Feature Selection\\merged_fault_data.csv"',
            'output_path = str(rp.DATA_RAW / "merged_fault_data.csv")',
        ),
        (
            'file_path = r"C:\\Users\\ishan\\OneDrive\\Desktop\\Feature Selection\\merged_fault_data.csv"',
            'file_path = str(rp.DATA_RAW / "merged_fault_data.csv")',
        ),
        (
            'df = pd.read_csv(r"C:\\Users\\ishan\\OneDrive\\Desktop\\Feature Selection\\labeled_fault_data_enhanced.csv")',
            'df = pd.read_csv(str(rp.DATA_PROCESSED / "labeled_fault_data_enhanced.csv"))',
        ),
        (
            'file_path = r"C:\\Users\\ishan\\OneDrive\\Desktop\\Feature Selection\\labeled_fault_data_enhanced.csv"',
            'file_path = str(rp.DATA_PROCESSED / "labeled_fault_data_enhanced.csv")',
        ),
        (
            'save_path = r"C:\\Users\\ishan\\OneDrive\\Desktop\\Feature Selection\\augmented_fault_data.csv"',
            'save_path = str(rp.DATA_PROCESSED / "augmented_fault_data.csv")',
        ),
        (
            "file_path = r'C:\\Users\\ishan\\OneDrive\\Desktop\\Feature Selection\\augmented_fault_data.csv'",
            'file_path = str(rp.DATA_PROCESSED / "augmented_fault_data.csv")',
        ),
        (
            'final_complex_imbalanced.to_csv("complex_imbalanced_80k.csv", index=False)',
            "final_complex_imbalanced.to_csv(str(rp.COMPLEX_80K), index=False)",
        ),
        ('df = pd.read_csv("complex_imbalanced_80k.csv")', "df = pd.read_csv(str(rp.COMPLEX_80K))"),
        ("file_path = 'complex_imbalanced_80k.csv'", "file_path = str(rp.COMPLEX_80K)"),
        ('file_path = "complex_imbalanced_80k.csv"', "file_path = str(rp.COMPLEX_80K)"),
        ('    df = pd.read_csv("complex_imbalanced_80k.csv")', '    df = pd.read_csv(str(rp.COMPLEX_80K))'),
        (
            "    mi_results.to_csv('mutual_info_scores.csv', index=False)",
            "    mi_results.to_csv(str(rp.MI_SCORES), index=False)",
        ),
        (
            '            filename = f\'pi_scores_{model_name.lower().replace(" ", "_")}.csv\'',
            '            filename = str(rp.DATA_FEATURES / f\'pi_scores_{model_name.lower().replace(" ", "_")}.csv\')',
        ),
        ("        pi_df = pd.read_csv('pi_scores_simple_rf.csv')", "        pi_df = pd.read_csv(str(rp.PI_SCORES_RF))"),
        ("        mi_df = pd.read_csv('mutual_info_scores.csv')", "        mi_df = pd.read_csv(str(rp.MI_SCORES))"),
        ("    combined.to_csv('nonzero_features_both.csv', index=False)", "    combined.to_csv(str(rp.NONZERO_BOTH), index=False)"),
        ("        df = pd.read_csv('nonzero_features_both.csv')", "        df = pd.read_csv(str(rp.NONZERO_BOTH))"),
        ("    top_25.to_csv('top_25_features.csv', index=False)", "    top_25.to_csv(str(rp.TOP25_FEATURES), index=False)"),
        ("    feature_names_df.to_csv('top_25_feature_names.csv', index=False)", "    feature_names_df.to_csv(str(rp.TOP25_NAMES), index=False)"),
        ("        top25_df = pd.read_csv('top_25_feature_names.csv')", "        top25_df = pd.read_csv(str(rp.TOP25_NAMES))"),
        ('        df = pd.read_csv("complex_imbalanced_80k.csv")', '        df = pd.read_csv(str(rp.COMPLEX_80K))'),
        ("    correlation_matrix.to_csv('top25_correlation_matrix.csv')", "    correlation_matrix.to_csv(str(rp.TOP25_CORR_MAT))"),
        ("    correlation_summary.to_csv('top25_correlation_pairs.csv', index=False)", "    correlation_summary.to_csv(str(rp.TOP25_CORR_PAIRS), index=False)"),
        ('        MI_df = pd.read_csv("mutual_info_scores.csv", index_col=0)', '        MI_df = pd.read_csv(str(rp.MI_SCORES), index_col=0)'),
        ('        PI_df = pd.read_csv("pi_scores_simple_rf.csv", index_col=0)', '        PI_df = pd.read_csv(str(rp.PI_SCORES_RF), index_col=0)'),
        ('        R_df = pd.read_csv("top25_correlation_matrix.csv", index_col=0)', '        R_df = pd.read_csv(str(rp.TOP25_CORR_MAT), index_col=0)'),
        ('    qubo_df.to_csv("qubo_matrix_symmetric.csv")', "    qubo_df.to_csv(str(rp.QUBO_MATRIX))"),
        ("    with open('qubo_metadata.json', 'w') as f:", "    with open(rp.QUBO_META, 'w') as f:"),
        ("        with open('quantum_feature_results.pkl', 'wb') as f:", "        with open(rp.QUANTUM_RESULTS_PKL, 'wb') as f:"),
        (
            '    def __init__(self, qubo_matrix_file="qubo_matrix_symmetric.csv", checkpoint_file="checkpoint.pkl"):',
            "    def __init__(self, qubo_matrix_file=str(rp.QUBO_MATRIX), checkpoint_file=str(rp.CHECKPOINT_PKL)):",
        ),
        ('                 qubo_matrix_file="qubo_matrix_symmetric.csv",', "                 qubo_matrix_file=str(rp.QUBO_MATRIX),"),
        ('                 checkpoint_file="checkpoint.pkl",', "                 checkpoint_file=str(rp.CHECKPOINT_PKL),"),
        ('                 results_file="grid_search_results.csv",', "                 results_file=str(rp.GRID_RESULTS),"),
        ('                 state_file="grid_search_state.json"):', "                 state_file=str(rp.GRID_STATE)):"),
        ('                 state_file="grid_search_state.json",', "                 state_file=str(rp.GRID_STATE),"),
        ('                 results_file="grid_search_results.csv"):', "                 results_file=str(rp.GRID_RESULTS)):"),
        ("        with open('qubo_metadata.json', 'w') as f:", "        with open(rp.QUBO_META, 'w') as f:"),
        ("df = pd.read_csv('complex_imbalanced_80k.csv')", "df = pd.read_csv(str(rp.COMPLEX_80K))"),
        ("CSV_FILE = 'complex_imbalanced_80k.csv'", "CSV_FILE = str(rp.COMPLEX_80K)"),
        ('        selector.load_data("complex_imbalanced_80k.csv", "Fault_Label")', '        selector.load_data(str(rp.COMPLEX_80K), "Fault_Label")'),
        (
            '    def export_summary(self, filename="grid_search_summary.txt"):',
            "    def export_summary(self, filename=str(rp.GRID_SUMMARY)):",
        ),
    ]

    def apply_line(line: str) -> str:
        for old, new in replacements:
            if old in line:
                line = line.replace(old, new)
        return line

    for cell in nb["cells"]:
        if cell.get("cell_type") != "code":
            continue
        src = cell.get("source")
        if isinstance(src, str):
            cell["source"] = apply_line(src)
        else:
            cell["source"] = [apply_line(line) for line in src]

    with path.open("w", encoding="utf-8") as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)
        f.write("\n")


def main() -> None:
    for sub in (
        "data/raw",
        "data/processed",
        "data/features",
        "results/qubo",
        "results/grid_search",
        "results/checkpoints",
        "notebooks",
        "docs",
        "scripts",
    ):
        (ROOT / sub).mkdir(parents=True, exist_ok=True)

    for rel_src, rel_dst in MOVES:
        src, dst = ROOT / rel_src, ROOT / rel_dst
        if not src.exists():
            print("skip (missing):", rel_src)
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        print("move:", rel_src, "->", rel_dst)
        shutil.move(str(src), str(dst))

    for name in ("FS.ipynb", "FS-Workstation.ipynb"):
        src_nb = CODES / name
        if not src_nb.exists():
            print("skip notebook:", src_nb)
            continue
        dst_nb = NOTEBOOKS / name
        print("move notebook:", src_nb.name, "-> notebooks/")
        shutil.move(str(src_nb), str(dst_nb))
        profile = "default" if name == "FS.ipynb" else "workstation"
        patch_notebook(dst_nb, profile)

    stub = CODES / "README.txt"
    stub.write_text(
        "Project layout was reorganized.\n\n"
        "Notebooks: ../notebooks/FS.ipynb (default profile) and "
        "../notebooks/FS-Workstation.ipynb (FS_PROFILE=workstation).\n"
        "Data: ../data/ — Results: ../results/ — Paths: ../repo_paths.py\n",
        encoding="utf-8",
    )
    print("done.")


if __name__ == "__main__":
    main()
