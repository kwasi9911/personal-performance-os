import pandas as pd
import numpy as np

def compute_training_load(weekly_df: pd.DataFrame) -> pd.DataFrame:
    """
    Score each week 0-100 based on steps and exercise minutes.
    Weights: 50% steps, 50% exercise minutes.
    """
    df = weekly_df.copy()

    # Normalize each metric to 0-100 using rolling max (last 12 weeks)
    df['steps_norm'] = (df['steps'] / df['steps'].rolling(12, min_periods=1).max() * 100).clip(0, 100)
    df['ex_norm']    = (df['exercise_min'] / df['exercise_min'].rolling(12, min_periods=1).max() * 100).clip(0, 100)

    # Weighted training load score
    df['load_score'] = (0.5 * df['steps_norm'] + 0.5 * df['ex_norm']).round(1)

    # Recovery zone based on score
    def zone(score):
        if score < 30:   return 'Undertraining'
        elif score < 70: return 'Optimal'
        else:            return 'Overtraining'

    df['zone'] = df['load_score'].apply(zone)

    # Zone color for charts
    zone_colors = {'Undertraining': '#F59E0B', 'Optimal': '#10B981', 'Overtraining': '#EF4444'}
    df['zone_color'] = df['zone'].map(zone_colors)

    return df
