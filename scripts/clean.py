import argparse
import os
import sys
import json 
from bs4 import BeautifulSoup

RAW_DIR = os.path.join("..", "data", "raw")
CLEAN_DIR = os.path.join("..", "data", "clean")

def get_files(school, player, year):
    files = os.listdir(RAW_DIR)
    if player == ".":
        # all players for that school
        matches = [f for f in files if f"_{school}" in f]
    elif year:
        matches = [f for f in files if f.startswith(f"{player}_{school}_{year}")]
    else:
        matches = [f for f in files if f in (f"{player}_{school}_raw.json", f"{player}_{school}.json")]
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

# --- entry point ---

if not sys.stdin.isatty():
    raw = sys.stdin.read()
    print(f"Read {len(raw)} characters from stdin.", file=sys.stderr)
    data = json.loads(raw)
    clean(data)
else:
    parser = argparse.ArgumentParser()
    parser.add_argument("school", help="School to clean data from, or '.' for all schools")
    parser.add_argument("player", nargs="?", default=".", help="firstname-lastname, or '.' for all players (default: .)")
    parser.add_argument("-y", "--year", type=int, help="specific year to clean")
    args = parser.parse_args()

    files = get_files(args.school, args.player, args.year)

    if not files:
        print(f"No files found matching criteria.", file=sys.stderr)
        sys.exit(1)

    for filepath in files:
        with open(filepath) as f:
            data = json.load(f)
        print(f"Cleaning {filepath}...", file=sys.stderr)
        cleaned = clean(data)
        clean_filepath = get_clean_path(filepath)
        print(f"Dumping {clean_filepath}...", file=sys.stderr)
        with open(clean_filepath, "w") as f:
            json.dump(cleaned, f, indent=2)