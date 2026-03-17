import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import data_loader as d
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

OUTPUT_DIR = Path(__file__).parent / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

def log_reg_game_prediction(df: pd.DataFrame):
    df = df[["game_number", "home_flag", "3_game_rolling_OPS", "rolling_bb", "rolling_2b", "above_avg"]].dropna()
    X = df[["game_number", "home_flag", "3_game_rolling_OPS", "rolling_bb", "rolling_2b"]]
    y = df["above_avg"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LogisticRegression().fit(X_train, y_train)
    y_pred = model.predict(X_test)
    print(classification_report(y_test, y_pred))




if __name__ == "__main__":
    df = d.load_hitting_data(player="")
    log_reg_game_prediction(df)