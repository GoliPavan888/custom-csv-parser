import csv
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from src.custom_csv import CustomCsvReader, CustomCsvWriter

TEST_FILE = "tests/sample.csv"

rows = [
    ["a", "b"],
    ["1", "2,3"],
    ['he said "hi"', "x"],
    ["line1\nline2", "y"],
]

# Write using builtin csv.writer
with open(TEST_FILE, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerows(rows)

# Read using your CustomCsvReader
with open(TEST_FILE, encoding="utf-8") as f:
    custom_rows = list(CustomCsvReader(f))

print("Builtin rows:", rows)
print("Custom rows :", custom_rows)
print("Equal?      :", rows == custom_rows)
