# Custom CSV Reader and Writer in Python

This project implements a custom CSV (Comma-Separated Values) reader and writer from scratch in Python, without using the built-in `csv` module for the core parsing logic.[web:5][web:6] The goal is to understand low-level CSV parsing (quotes, commas, escaped quotes, embedded newlines) and to benchmark the custom implementation against Python’s standard library.

## Project Structure

- `src/custom_csv.py` – implementation of `CustomCsvReader` and `CustomCsvWriter`.
- `src/__init__.py` – makes `src` a package.
- `tests/compare_with_builtin.py` – correctness tests that compare the custom reader with `csv.reader`.
- `benchmarks/benchmark_csv.py` – benchmark script for read/write performance.
- `README.md` – project overview, usage, and benchmark analysis.
- `requirements.txt` – Python dependencies (for this project, only optional dev tools).

## Setup

1. Clone the repository:

git clone https://github.com/GoliPavan888/custom-csv-parser.git
cd custom-csv-parser


2. Create and activate a virtual environment (recommended):

python -m venv .venv

Windows
.venv\Scripts\activate

macOS / Linux
source .venv/bin/activate


3. Install dependencies:

pip install -r requirements.txt


The core implementation only uses the Python standard library, so the project runs on any recent Python 3 version without extra runtime packages.[web:84][web:78]

## Usage

### Writing CSV with `CustomCsvWriter`

from src.custom_csv import CustomCsvWriter

rows = [
["a", "b,c"],
['he said "hi"', "x"],
["line1\nline2", "y"],
]

with open("example.csv", "w", encoding="utf-8") as f:
writer = CustomCsvWriter(f)
writer.writerows(rows)


`CustomCsvWriter` will:[web:5][web:6]

- Escape any existing double quotes in fields by doubling them.
- Automatically wrap fields containing commas, quotes, or newlines in double quotes.
- Write rows one per line, joining fields with commas.

### Reading CSV with `CustomCsvReader`

with open("example.csv", encoding="utf-8") as f:
reader = CustomCsvReader(f)
for row in reader:
print(row)


`CustomCsvReader`:[web:5][web:6]

- Treats commas as delimiters, except inside quoted fields.
- Handles escaped quotes represented as two consecutive double quotes.
- Supports newlines inside quoted fields.
- Streams rows one at a time, without loading the entire file into memory.

## Correctness Tests

The script `tests/compare_with_builtin.py` writes a small dataset using Python’s built-in `csv.writer` and reads it back using `CustomCsvReader`.[web:5][web:6] It then checks that all rows match exactly.

Run the test from the project root:

python tests/compare_with_builtin.py


You should see the builtin rows, custom rows, and a message confirming that they are equal (`Equal? : True`).

## Benchmarking

`benchmarks/benchmark_csv.py` measures the read and write performance of the custom implementation versus the standard library.[web:11][web:17] The script:

- Generates a synthetic dataset of 10,000 rows and 5 columns.
- Populates fields with random strings, occasionally including commas, double quotes, and newlines to exercise edge cases.
- Benchmarks four functions using `timeit.repeat`:
  - Writing with `csv.writer`
  - Writing with `CustomCsvWriter`
  - Reading with `csv.reader`
  - Reading with `CustomCsvReader`

Run the benchmark:

python benchmarks/benchmark_csv.py

### Benchmark Results

On a sample run (10,000 rows × 5 columns, best of 5 repetitions), the timings were:

| Operation              | Implementation     | Time (seconds) |
|------------------------|--------------------|----------------|
| Write CSV              | `csv.writer`       | 0.1025         |
| Write CSV              | `CustomCsvWriter`  | 0.1254         |
| Read CSV               | `csv.reader`       | 0.0086         |
| Read CSV               | `CustomCsvReader`  | 0.0634         |

These results show that the built-in `csv` module is faster for both reading and writing, especially for reading, which is expected because the standard library is implemented in optimized C while this project uses pure Python.[web:5][web:11] The goal of this assignment is not to surpass the standard library but to build a correct, robust parser and to understand the performance trade-offs.

## Design Overview

`CustomCsvReader` uses a small state machine that tracks whether the parser is currently inside a quoted field.[web:48][web:79]

- Outside quotes, commas end the current field and newlines end the current row.
- Inside quotes, commas and newlines are treated as data.
- A double quote inside a quoted field is treated as an escaped quote when it is followed by another double quote.

`CustomCsvWriter` decides whether a field needs quoting based on the presence of commas, quotes, or newline characters, then escapes any embedded quotes before surrounding the field with quotes.[web:5][web:79]

Both classes are written with streaming in mind so that large CSV files can be processed row by row.

## How to Run Everything

From the project root:

Basic manual test (optional)
python try_custom_csv.py

Correctness test against builtin csv
python tests/compare_with_builtin.py

Benchmark performance
python benchmarks/benchmark_csv.py



This repository is intended as a learning project to deepen understanding of file I/O, string handling, stateful parsing, and performance benchmarking in Python.

