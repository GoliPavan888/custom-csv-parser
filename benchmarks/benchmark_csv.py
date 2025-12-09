import csv
import os
import random
import string
import timeit
import sys

# Make src importable
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from src.custom_csv import CustomCsvReader, CustomCsvWriter

DATA_FILE = "benchmarks/benchmark_data.csv"
ROWS = 10_000
COLS = 5


def random_field():
    base = "".join(random.choices(string.ascii_letters, k=8))
    # occasionally add commas, quotes, or newlines
    extras = [",", '"', "\n", ""]
    return base + random.choice(extras)


def generate_data():
    rows = [[random_field() for _ in range(COLS)] for _ in range(ROWS)]
    return rows


def setup_file_builtin():
    rows = generate_data()
    with open(DATA_FILE, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerows(rows)


def write_builtin():
    rows = generate_data()
    with open(DATA_FILE, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerows(rows)


def write_custom():
    rows = generate_data()
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        w = CustomCsvWriter(f)
        w.writerows(rows)


def read_builtin():
    with open(DATA_FILE, newline="", encoding="utf-8") as f:
        r = csv.reader(f)
        for _ in r:
            pass


def read_custom():
    with open(DATA_FILE, encoding="utf-8") as f:
        r = CustomCsvReader(f)
        for _ in r:
            pass


def run_bench():
    # create initial file for read tests
    setup_file_builtin()

    repeats = 5
    number = 1  # each timing runs once, repeated "repeats" times

    def avg(stmt):
        return min(
            timeit.repeat(
                stmt,
                globals=globals(),
                repeat=repeats,
                number=number,
            )
        )

    print(f"Rows: {ROWS}, Cols: {COLS}")
    print("Timing values are best-of ", repeats)

    builtin_write = avg("write_builtin()")
    custom_write = avg("write_custom()")
    builtin_read = avg("read_builtin()")
    custom_read = avg("read_custom()")

    print("\nWrite timings (seconds)")
    print(f"builtin csv.writer : {builtin_write:.4f}")
    print(f"CustomCsvWriter    : {custom_write:.4f}")

    print("\nRead timings (seconds)")
    print(f"builtin csv.reader : {builtin_read:.4f}")
    print(f"CustomCsvReader    : {custom_read:.4f}")


if __name__ == "__main__":
    run_bench()
