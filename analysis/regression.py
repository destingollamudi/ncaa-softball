import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from pathlib import Path
import data_loader as d
import patsy

def get_output_dir(df: pd.DataFrame) -> Path:
    player = df["player"].iloc[0]
    school = df["school"].iloc[0]
    output_dir = Path(__file__).parent / "outputs" / school.lower() / player.lower().replace(" ", "-")
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir

def linear_regression_season_trend(df: pd.DataFrame):
    output_dir = get_output_dir(df)
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
    plt.savefig(output_dir / "ops_season_trend.png")
    plt.close()
    print("Plot saved to /outputs")

    return model

def multiple_regression_game_trends(df: pd.DataFrame):
    output_dir = get_output_dir(df)
    X = sm.add_constant(df[["BB", "2B"]])
    y = df["OPS"]
    model = sm.OLS(y, X).fit()
    print(model.summary())
    # coefficient plot
    coefs = model.params.drop("const")
    errors = (model.conf_int().drop("const")[1] - model.conf_int().drop("const")[0]) / 2

    plt.figure(figsize=(8, 5))
    plt.barh(coefs.index, coefs.values, xerr=errors, color="steelblue", capsize=5)
    plt.axvline(x=0, color="red", linestyle="--", linewidth=1)
    plt.xlabel("Coefficient (effect on OPS)")
    plt.title("Multiple Regression: Predictors of Per-Game OPS")
    plt.tight_layout()
    plt.savefig(output_dir / "ops_mlr_coefficients.png")
    plt.close()
    print("Plot saved to outputs/ops_mlr_coefficients.png")

    return model

def spline_season_arc(df: pd.DataFrame, season: int):
    output_dir = get_output_dir(df)
    df = df[df["season"] == season]
    X = df["game_number"]
    y = df["OPS"]
    spline_basis = patsy.cr(X, df=4)
    model = sm.OLS(y, spline_basis).fit()

    x_smooth = np.linspace(X.min(), X.max(), 300)
    spline_smooth = patsy.cr(x_smooth, df=4)
    y_smooth = model.predict(spline_smooth)

    plt.figure(figsize=(10, 5))
    plt.scatter(X, y, alpha=0.5, label="Actual OPS")
    plt.plot(x_smooth, y_smooth, color="red", linewidth=2, label="Spline fit")
    plt.xlabel("Game Number")
    plt.ylabel("OPS")
    plt.title(f"{season} Season OPS Arc")
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_dir / f"spline_{season}.png")
    plt.close()
    print(f"Plot saved to outputs/spline_{season}.png")

def spline_overlay(df: pd.DataFrame):
    output_dir = get_output_dir(df)
    plt.figure(figsize=(12, 6))
    
    for season in [2023, 2024, 2025, 2026]:
        season_data = df[df["season"] == season]
        X = season_data["game_number"]
        y = season_data["OPS"]
        spline_basis = patsy.cr(X, df=4)
        model = sm.OLS(y, spline_basis).fit()
        x_smooth = np.linspace(X.min(), X.max(), 300)
        spline_smooth = patsy.cr(x_smooth, df=4)
        y_smooth = model.predict(spline_smooth)
        plt.plot(x_smooth, y_smooth, label=str(season), linewidth=2)
    
    plt.xlabel("Game Number")
    plt.ylabel("OPS")
    plt.title("Season OPS Arc Overlay")
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_dir / "spline_overlay.png")
    plt.close()
    print("Plot saved to /outputs")

def spline_all(df: pd.DataFrame):
    output_dir = get_output_dir(df)
    X = df["career_game_number"]
    y = df["OPS"]
    spline_basis = patsy.cr(X, df=4)
    model = sm.OLS(y, spline_basis).fit()

    x_smooth = np.linspace(X.min(), X.max(), 300)
    spline_smooth = patsy.cr(x_smooth, df=4)
    y_smooth = model.predict(spline_smooth)

    plt.figure(figsize=(10, 5))
    plt.scatter(X, y, alpha=0.5, label="Actual OPS")
    plt.plot(x_smooth, y_smooth, color="red", linewidth=2, label="Spline fit")
    plt.xlabel("Career Game Number")
    plt.ylabel("OPS")
    plt.title(f"Career OPS Arc")
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_dir / f"spline_career.png")
    plt.close()
    print(f"Plot saved to /outputs")
 
if __name__ == "__main__":
    df = d.load_hitting_data(player="jayme-prandine")
    multiple_regression_game_trends(df)
    for season in [2023, 2024, 2025, 2026]:
        spline_season_arc(df.copy(), season)
    spline_overlay(df.copy())
    spline_all(df.copy())