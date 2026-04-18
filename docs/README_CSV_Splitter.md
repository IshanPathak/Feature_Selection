# CSV File Splitter

A Python tool to split large CSV files into smaller chunks based on file size or row count.

## Features

- Split CSV files by size (MB) or row count
- Automatic file naming with sequential numbering
- Option to include/exclude headers in split files
- Memory-efficient processing using pandas chunks
- Interactive mode and command-line interface
- Progress tracking and file size reporting

## Installation

Make sure you have pandas installed:
```bash
pip install pandas
```

## Usage

### Method 1: Interactive Mode (Recommended for beginners)

Simply run the script without arguments:
```bash
python csv_splitter.py
```

The script will prompt you for:
1. Input CSV file path
2. Output directory
3. Split method (size or rows)
4. Size limit or row count

### Method 2: Command Line Interface

#### Split by Size
```bash
python csv_splitter.py input_file.csv output_directory --size 100
```
This splits the file into chunks of maximum 100MB each.

#### Split by Rows
```bash
python csv_splitter.py input_file.csv output_directory --rows 50000
```
This splits the file into chunks of maximum 50,000 rows each.

#### Exclude Headers
```bash
python csv_splitter.py input_file.csv output_directory --size 100 --no-header
```

### Method 3: Using the Example Script

Run the example script to automatically split all large CSV files in your workspace:
```bash
python example_split_large_files.py
```

## Examples

### Example 1: Split a 3.5GB file into 100MB chunks

```python
from csv_splitter import split_csv_by_size

# Split augmented_fault_data.csv into 100MB chunks
split_csv_by_size(
    input_file="augmented_fault_data.csv",
    output_dir="split_augmented_data",
    max_size_mb=100
)
```

### Example 2: Split by row count

```python
from csv_splitter import split_csv_by_rows

# Split into files with 50,000 rows each
split_csv_by_rows(
    input_file="large_dataset.csv",
    output_dir="split_by_rows",
    max_rows=50000
)
```

## Output

The splitter creates files with the naming pattern:
- `filename_part_001.csv`
- `filename_part_002.csv`
- `filename_part_003.csv`
- etc.

Each file will contain:
- Header row (unless `--no-header` is specified)
- Data rows up to the specified limit
- File size and row count information during processing

## Large Files in Your Workspace

Based on your workspace, here are the large CSV files that can be split:

| File | Size | Recommended Split |
|------|------|-------------------|
| `augmented_fault_data.csv` | 3.5GB | 100MB chunks |
| `selected_80k_samples.csv` | 84MB | 50MB chunks |
| `labeled_fault_data_enhanced.csv` | 73MB | 50MB chunks |
| `merged_fault_data.csv` | 65MB | 50MB chunks |
| `fault_data.csv` | 62MB | 50MB chunks |
| `labeled_fault_data.csv` | 65MB | 50MB chunks |
| `complex_imbalanced_80k.csv` | 68MB | 50MB chunks |

## Tips

1. **Memory Usage**: The tool processes files in chunks, so it's memory-efficient even for very large files.

2. **File Size Estimation**: The tool estimates row counts based on sample data, so actual file sizes may vary slightly.

3. **Headers**: By default, each split file includes the header row. Use `--no-header` if you don't want headers.

4. **Output Directory**: The tool automatically creates the output directory if it doesn't exist.

5. **Progress Tracking**: The tool shows progress and file information during splitting.

## Error Handling

- File not found errors are handled gracefully
- Invalid size/row inputs are caught and reported
- Memory errors for extremely large files are handled with chunked processing

## Requirements

- Python 3.6+
- pandas
- pathlib (built-in)
- argparse (built-in) 