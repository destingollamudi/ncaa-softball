import argparse
import os
import sys
import json 
from bs4 import BeautifulSoup

RAW_DIR = os.path.join("..", "data", "raw")

def get_files(school, player, year):
    files = os.listdir(RAW_DIR)
    if player == ".":
        # all players for that school
        matches = [f for f in files if f"_{school}" in f]
    elif year:
        matches = [f for f in files if f.startswith(f"{player}_{school}_{year}")]
    else:
        matches = [f for f in files if f.startswith(f"{player}_{school}")]
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

def careerClean(data):
    pass

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
        clean(data)