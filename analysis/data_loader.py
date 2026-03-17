import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data" / "csv"

def load_hitting_data(player: str = None) -> pd.DataFrame:
    files = [
        f for f in DATA_DIR.glob("*hitting*.csv")
        if "career" not in f.name
        and (player is None or player in f.name)
    ]

    frames = []
    for f in files:
        df = pd.read_csv(f)
        season = int(f.stem.split("_")[-2])
        df["season"] = season
        df["school"] = f.stem.split("_")[0].title()
        df["player"] = "-".join(f.stem.split("_")[1:3]).replace("-", " ").title()
        frames.append(df)

    combined = pd.concat(frames, ignore_index=True)
    combined = combined[combined["AB"].notna() & (combined["AB"] > 0)]

    combined["TB"] = (
        combined["H"] +
        combined["2B"] +
        (2 * combined["3B"]) +
        (3 * combined["HR"])
    )
    combined["SLG"] = combined["TB"] / combined["AB"]
    combined["OBP"] = (
        (combined["H"] + combined["BB"] + combined["HBP"]) /
        (combined["AB"] + combined["BB"] + combined["HBP"] + combined["SF"])
    )
    combined["OPS"] = combined["OBP"] + combined["SLG"]
    combined = combined.sort_values(["season", "Date"])
    combined["game_number"] = combined.groupby("season").cumcount() + 1
    combined = combined.sort_values(["season", "game_number"])
    combined["career_game_number"] = range(1, len(combined) + 1)
    season_mean = combined.groupby("season")["OPS"].transform("mean")
    combined["above_avg"] = (combined["OPS"] > season_mean).astype(int)
    combined["3_game_rolling_OPS"] = (
        combined.groupby("season")["OPS"]
        .transform(lambda x: x.shift(1).rolling(3).mean())
    )
    combined["home_flag"] = (combined["home_away"] == "home").astype(int)
    combined["rolling_bb"] = (

    combined.groupby("season")["BB"]
    .transform(lambda x: x.shift(1).rolling(3).mean())
    )   
    combined["rolling_2b"] = (
        combined.groupby("season")["2B"]
        .transform(lambda x: x.shift(1).rolling(3).mean())
    )

    return combined

