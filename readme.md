# NCAA Softball Analytics

A Python-based data collection and analysis tool for NCAA softball player statistics. Built to scrape game-by-game hitting and fielding data from Sidearm Sports powered college athletics sites, enabling career trajectory analysis and performance research.

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

### Scrape and clean in one step (pipe)
```
python scripts/scrape.py haverford jocelyn-leal --year 2025 | python scripts/clean.py
```

### Scrape multiple years and clean
```
python scripts/scrape.py haverford jocelyn-leal --year 2024 2025 | python scripts/clean.py
```

### Scrape a player's full career and clean
```
python scripts/scrape.py haverford jocelyn-leal | python scripts/clean.py
```

### Save raw JSON to data/raw (for later cleaning)
```
python scripts/scrape.py haverford jocelyn-leal --year 2025 -d
```

### Clean previously saved raw files
```
# Single player, single year
python scripts/clean.py haverford jocelyn-leal -y 2025

# Single player, career
python scripts/clean.py haverford jocelyn-leal

# All saved files for a school
python scripts/clean.py haverford
```

Output CSVs are written to `data/csv/` as `<school>_<player>_<year>_hitting.csv` and `_fielding.csv`.

## Setup

After running:


`git clone https://github.com/destingollamudi/ncaa-softball.git` 

to clone the repo locally on your machine run:

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
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
Date, Opponent, W/L, GS, AB, R, H, RBI, 2B, 3B, HR, BB, IBB, SB, SBA, CS, HBP, SH, SF, GDP, K, home_away

*Derived per game: OPS (OBP + SLG), OBP, SLG, TB*

### Fielding
Date, Opponent, W/L, C, PO, A, E, FLD%, DP, SBA, CSB, PB, CI

## Statistical Analysis

A variety of statistical modeling methods will be applied to uncover
performance trends, predictive patterns, and behavioral archetypes
from game-level data.

**Data available:** A typical four-year D3 softball starter accumulates
roughly 120-160 game-level hitting rows across four seasons, assuming
a ~40-game schedule per year. Season-level aggregates are available
for each completed season but are used for descriptive context only,
not as independent observations. Any in-progress current season is
treated as a snapshot and excluded from cross-season models.

### Supervised Learning
Used when the outcome we are measuring is known. Applied here for
career trajectory analysis and game performance prediction.

**Regression**
- Linear Regression: measures whether improvement across seasons
  represents a genuine upward trend in AVG, OBP, and SLG.
  Interpretable descriptively across four seasons; p-values treated
  with caution given the small number of season-level points.
- Natural Cubic Splines: applied to the within-season game-level
  time series (e.g. rolling AVG across 37 games of 2023) to capture
  curves and bends in her development arc rather than forcing a
  straight line. Not applied at the season level due to insufficient
  data points.
- Multiple Regression: identifies which per-game stats (BB, H, 2B,
  home_away, AB) most strongly drive per-game OPS. Uses all available
  game-level rows; capped at 4-5 predictors to avoid overfitting
  on 80 observations.

**Classification**
- Logistic Regression: predicts whether a given game's OPS will
  fall above or below that season's average. Binary outcome derived
  from H, BB, AB, and extra-base hit columns.
- Linear Discriminant Analysis (LDA): identifies which combination
  of per-game stats best separates above-average and below-average
  performances. Two-class formulation preferred over three-class
  given sample size.

### Unsupervised Learning
Used when we let the data reveal its own structure without
predefined labels.

**Clustering**
- K-Means Clustering: groups individual games by multi-stat
  similarity (H, BB, R, 2B, SB) to discover distinct performance
  archetypes. Tested at k=3 and k=4 on the full 80-game pool.

**Association**
- Rolling window autocorrelation: detects whether OPS or AVG in
  one game genuinely predicts the next, separating real hot streaks
  from random variation. Applied within each season separately;
  wide confidence intervals are expected and are themselves a
  meaningful result.
## Roadmap

- Streamlit web app for player-facing stat dashboards
- Support for additional Sidearm Sports powered schools
- Derived stat calculations (OPS, ISO, OBP, SLG) in clean.py
- Multi-player team-wide analysis
