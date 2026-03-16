import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from pathlib import Path
import data_loader as d

OUTPUT_DIR = Path(__file__).parent / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

def linear_regression_season_trend(df):
    season_df = df.groupby("season")[["H","AB","BB","HBP","SF","TB"]].sum()
    season_df["SLG"] = (season_df["TB"] / season_df["AB"]).round(3)
    season_df["OBP"] = ((season_df["H"] + season_df["BB"] + season_df["HBP"]) / (season_df["AB"] + season_df["BB"] + season_df["HBP"] + season_df["SF"])).round(3)
    season_df["OPS"] = (season_df["OBP"] + season_df["SLG"]).round(3)
    season_df = season_df.reset_index()

    X = sm.add_constant(season_df["season"])
    y = season_df["OPS"]
    model = sm.OLS(y, X).fit()
    print(model.summary())

    plt.scatter(season_df["season"], y)
    plt.plot(season_df["season"], model.fittedvalues)
    plt.xlabel("Season")
    plt.ylabel("OPS")
    plt.title("OPS Trend by Season")
    plt.savefig(OUTPUT_DIR / "ops_season_trend.png")
    plt.close()
    print("Plot saved to /outputs")

    return model

def multiple_regression_game_trends(df):
    df["home_flag"] = (df["home_away"] == "home").astype(int)
    X = sm.add_constant(df["AB", "BB", "2B", "home_flag"])
    y = df["OPS"]
    model = sm.OLS(y, X).fit()
    print(model)

    plt.scatter(df["AB", "BB", "2B", "home_flag"], y)
    plt.plot(df["AB", "BB", "2B", "home_flag"], model.fittedvalues)
    plt.xlabel("Factors")
    plt.ylabel("OPS")
    plt.savefig(OUTPUT_DIR / "ops_mlr_trend.png")
    plt.close()
    print("Plot saved to /outputs")
    
 
if __name__ == "__main__":
    df = d.load_hitting_data()
    multiple_regression_game_trends(df.copy())