import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

def forecast_goal(weekly_df: pd.DataFrame, metric: str, target: float, weeks_ahead: int = 26) -> dict:
    """
    Fit a linear regression on the last 8 weeks of `metric`
    and project when the target will be reached.
    """
    df = weekly_df.dropna(subset=[metric]).copy()
    if len(df) < 4:
        return {'error': 'Not enough data (need at least 4 weeks)'}

    # Use last 8 weeks only
    df = df.tail(8).reset_index(drop=True)
    X = df.index.values.reshape(-1, 1)
    y = df[metric].values

    model = LinearRegression()
    model.fit(X, y)

    r2 = model.score(X, y)

    # Project forward
    future_X = np.arange(len(df), len(df) + weeks_ahead).reshape(-1, 1)
    future_y = model.predict(future_X)

    # Find when target is crossed
    target_week = None
    for i, val in enumerate(future_y):
        if val >= target:
            target_week = i + 1
            break

    return {
        'r2':          round(r2, 3),
        'current':     round(float(y[-1]), 1),
        'target':      target,
        'weeks_to_go': target_week,
        'trend':       round(float(model.coef_[0]), 2),
        'history_x':   list(range(len(df))),
        'history_y':   list(y),
        'future_x':    list(range(len(df), len(df) + weeks_ahead)),
        'future_y':    [round(v, 1) for v in future_y],
    }
