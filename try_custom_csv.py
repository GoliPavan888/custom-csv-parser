from src.custom_csv import CustomCsvReader, CustomCsvWriter

with open("test.csv", "w", encoding="utf-8") as f:
    w = CustomCsvWriter(f)
    w.writerow(["a", "b,c", 'he said "hi"', "line1\nline2"])

with open("test.csv", encoding="utf-8") as f:
    r = CustomCsvReader(f)
    for row in r:
        print(row)
