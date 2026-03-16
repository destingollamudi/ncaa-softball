import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data" / "csv"

def load_hitting_data() -> pd.DataFrame:
    files = [
        f for f in DATA_DIR.glob("*hitting*.csv")
        if "career" not in f.name
    ]

    frames = []
    for f in files:
        df = pd.read_csv(f)
        season = int(f.stem.split("_")[-2])
        df["season"] = season
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

    return combined

