#!/usr/bin/env python3
import os
import csv

# 1) adjust these paths if needed
INPUT_DIR  = "Data"
YEARS      = [str(y) for y in range(2015, 2025)]

# 2) ensure each year subfolder exists under Data/
for yr in YEARS:
    outdir = os.path.join(INPUT_DIR, yr)
    os.makedirs(outdir, exist_ok=True)

# 3) process each station file
for station_file in ("72429793812.csv", "99495199999.csv"):
    in_path = os.path.join(INPUT_DIR, station_file)
    if not os.path.exists(in_path):
        print(f"⚠️  Skipping missing file {in_path}")
        continue

    with open(in_path, newline='', encoding='utf-8') as inf:
        reader = csv.reader(inf)
        header = next(reader)

        # prepare one writer per year, on‐demand
        writers = {}

        # find the index of the DATE column once
        try:
            date_idx = header.index("DATE")
        except ValueError:
            raise RuntimeError("Could not find a 'DATE' column in the header")

        # iterate over every row
        for row in reader:
            date = row[date_idx]
            year = date.split("-")[0]
            if year not in YEARS:
                # skip rows outside 2015–2024
                continue

            # open writer for this year if needed
            if year not in writers:
                out_path = os.path.join(INPUT_DIR, year, station_file)
                outf = open(out_path, "w", newline='', encoding='utf-8')
                writer = csv.writer(outf)
                writer.writerow(header)         # write header
                writers[year] = (outf, writer)

            # write the row
            writers[year][1].writerow(row)

        # close all year‐files for this station
        for outf, _ in writers.values():
            outf.close()

    print(f"✔️  Finished splitting {station_file}")

print("🎉 All done!")
