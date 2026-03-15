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
Date, Opponent, W/L, AB, R, H, RBI, 2B, 3B, HR, BB, IBB, SB, SBA, CS, HBP, SH, SF, GDP, K, AVG

### Fielding
Date, Opponent, W/L, C, PO, A, E, FLD%, DP, SBA, CSB, PB, CI

## Statistical Analysis

A variety of statistical modeling methods will be applied to uncover 
performance trends, predictive patterns, and behavioral archetypes 
from game-level data.

### Supervised Learning
Used when the outcome we are measuring is known. Applied here for 
career trajectory analysis and game performance prediction.

**Regression**
- Linear Regression: measures whether improvement across seasons 
  represents a genuine upward trend
- Natural Cubic Splines: captures curves and bends in her development 
  arc rather than forcing a straight line
- Multiple Regression: identifies which stats most strongly drive 
  per game OPS

**Classification**
- Logistic Regression: predicts whether next game performance will 
  be above or below season average
- Linear Discriminant Analysis (LDA): identifies which combination 
  of stats best separates strong, average, and poor game performances

### Unsupervised Learning
Used when we let the data reveal its own structure without 
predefined labels.

**Clustering**
- K-Means Clustering: groups games by multi-stat similarity to 
  discover distinct performance archetypes

**Association**
- Rolling window autocorrelation: detects whether performance in 
  one game genuinely predicts the next, separating real hot streaks 
  from random variation

## Roadmap

- Streamlit web app for player-facing stat dashboards
- Support for additional Sidearm Sports powered schools
- Derived stat calculations (OPS, ISO, OBP, SLG) in clean.py
- Multi-player team-wide analysis