import pandas as pd
import numpy as np

def detect_anomalies(weekly_df: pd.DataFrame, metric: str, threshold: float = 2.0) -> pd.DataFrame:
    """
    Flag weeks where the metric deviates by more than `threshold` standard deviations
    from the rolling 4-week mean.
    """
    df = weekly_df.copy()
    df['rolling_mean'] = df[metric].rolling(4, min_periods=2).mean()
    df['rolling_std']  = df[metric].rolling(4, min_periods=2).std()
    df['z_score']      = ((df[metric] - df['rolling_mean']) / df['rolling_std'].replace(0, np.nan)).abs()
    df['is_anomaly']   = df['z_score'] > threshold

    def explain(row):
        if not row['is_anomaly'] or pd.isna(row['z_score']):
            return ''
        direction = 'above' if row[metric] > row['rolling_mean'] else 'below'
        pct = abs((row[metric] - row['rolling_mean']) / row['rolling_mean'] * 100)
        return f"{metric.replace('_', ' ').title()} was {pct:.0f}% {direction} your 4-week average"

    df['explanation'] = df.apply(explain, axis=1)
    return df
