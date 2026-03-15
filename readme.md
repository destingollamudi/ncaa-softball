# NCAA Softball Analytics

A Python-based data collection and analysis tool for NCAA DIII softball player statistics. Built to scrape game-by-game hitting and fielding data from Sidearm Sports powered college athletics sites, enabling career trajectory analysis and performance research.

## Project Structure

```
ncaa-softball/
    data/
        raw/          # Raw JSON responses from the stats API
        clean/        # Processed DataFrames ready for analysis
    scripts/
        scrape.py     # Data collection script
        clean.py      # Data processing and stat calculation script
        schools.py    # School name to base URL mappings
    README.md
```

## Usage

### Scrape a specific player and year
```
python scripts/scrape.py haverford jocelyn-leal --year 2025
```

### Scrape a player's full career
```
python scripts/scrape.py haverford jocelyn-leal
```

### Scrape and save raw JSON to data/raw
```
python scripts/scrape.py haverford jocelyn-leal --year 2025 -d
```

## Setup

```
python3 -m venv venv
source venv/bin/activate
pip install requests beautifulsoup4 pandas
```

## Adding a New School

Open `scripts/schools.py` and add a new entry to the `SCHOOLS` dictionary with the school's short name as the key and its base athletics URL as the value.

## Adding a New Player

No configuration needed. Pass any player slug from their roster page URL directly as the second argument. The script automatically discovers their season IDs from the roster page.

## Data Sources

All statistics are sourced from publicly accessible college athletics pages powered by Sidearm Sports. Data is used for personal educational and analytical purposes only and is not intended for commercial use. All stats remain the property of their respective institutions and athletes.

## Current Schools

- Haverford College

## Stats Collected

### Hitting
Date, Opponent, W/L, AB, R, H, RBI, 2B, 3B, HR, BB, IBB, SB, SBA, CS, HBP, SH, SF, GDP, K, AVG

### Fielding
Date, Opponent, W/L, C, PO, A, E, FLD%, DP, SBA, CSB, PB, CI

## Roadmap

- Streamlit web app for player-facing stat dashboards
- Support for additional Sidearm Sports powered schools
- Derived stat calculations (OPS, ISO, OBP, SLG) in clean.py
- Multi-player team-wide analysis