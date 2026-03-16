import os, sys, argparse, json
import pandas as pd
from bs4 import BeautifulSoup

RAW_DIR = os.path.join("..", "data", "raw")
CLEAN_DIR = os.path.join("..", "data", "clean")
CSV_DIR = os.path.join("..", "data", "csv")

def get_files(school, player, year):
    files = os.listdir(RAW_DIR)
    if player == ".":
        matches = [f for f in files if f"{school}" in f]
    elif year:
        matches = [f for f in files if f.startswith(f"{school}_{player}_{year}")]
    else:
        matches = [f for f in files if f == f"{school}_{player}_career_raw.json"]
    return [os.path.join(RAW_DIR, f) for f in matches]

def detect_type(data):
    keys = data.keys()
    if "current_stats" in keys or "career_stats" in keys:
        return "year"
    return "career"

def clean(data):
    dtype = detect_type(data)
    if dtype == "career":
        return careerClean(data)
    return yearClean(data)

def get_clean_path(raw_filepath):
    filename = os.path.basename(raw_filepath)
    clean_filename = filename.replace("_raw", "")
    return os.path.join(CLEAN_DIR, clean_filename)

def get_csv_base(clean_filepath):
    # haverford_jocelyn-leal_career.json -> haverford_jocelyn-leal_career
    filename = os.path.basename(clean_filepath).replace(".json", "")
    return os.path.join(CSV_DIR, filename)

def careerClean(data):
    cleaned = {}
    for year in data:
        year_data = data[year]
        cleaned[year] = {k: v for k, v in year_data.items() if k != "season_stats"}
        cleaned[year]["hitting"] = year_data["season_stats"]["hitting_stats"]
        cleaned[year]["fielding"] = year_data["season_stats"]["fielding_stats"]
    return cleaned

def yearClean(data):
    pass

def to_csv(cleaned, clean_filepath, dtype):
    os.makedirs(CSV_DIR, exist_ok=True)
    base = get_csv_base(clean_filepath)

    if dtype == "career":
        hitting_rows = []
        fielding_rows = []
        for year, year_data in cleaned.items():
            meta = {k: v for k, v in year_data.items() if k not in ("hitting", "fielding")}
            hitting_rows.append({"year": year, **meta, **year_data["hitting"]})
            fielding_rows.append({"year": year, **meta, **year_data["fielding"]})
        pd.DataFrame(hitting_rows).to_csv(f"{base}_hitting.csv", index=False)
        pd.DataFrame(fielding_rows).to_csv(f"{base}_fielding.csv", index=False)
    else:
        # year type - single season game by game
        pd.DataFrame(cleaned["hitting"]).to_csv(f"{base}_hitting.csv", index=False)
        pd.DataFrame(cleaned["fielding"]).to_csv(f"{base}_fielding.csv", index=False)

    print(f"Wrote {base}_hitting.csv and {base}_fielding.csv", file=sys.stderr)

# --- entry point ---

if not sys.stdin.isatty():
    raw = sys.stdin.read()
    data = json.loads(raw)
    cleaned = clean(data)
    print(json.dumps(cleaned, indent=2))
else:
    parser = argparse.ArgumentParser()
    parser.add_argument("school")
    parser.add_argument("player", nargs="?", default=".")
    parser.add_argument("-y", "--year", type=int)
    args = parser.parse_args()

    files = get_files(args.school, args.player, args.year)

    if not files:
        print("No files found matching criteria.", file=sys.stderr)
        sys.exit(1)

    for filepath in files:
        with open(filepath) as f:
            data = json.load(f)
        print(f"Cleaning {filepath}...", file=sys.stderr)
        cleaned = clean(data)
        dtype = detect_type(data)
        clean_filepath = get_clean_path(filepath)
        os.makedirs(CLEAN_DIR, exist_ok=True)
        with open(clean_filepath, "w") as f:
            json.dump(cleaned, f, indent=2)
        to_csv(cleaned, clean_filepath, dtype)