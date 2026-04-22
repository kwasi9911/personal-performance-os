import xml.etree.ElementTree as ET
import pandas as pd

def load_health_data(xml_path: str) -> dict:
    """Parse Apple Health export.xml into DataFrames."""
    tree = ET.parse(xml_path)
    root = tree.getroot()

    records = []
    for record in root.findall('Record'):
        records.append({
            'type':       record.get('type', ''),
            'value':      record.get('value', ''),
            'unit':       record.get('unit', ''),
            'startDate':  record.get('startDate', ''),
            'endDate':    record.get('endDate', ''),
        })

    df = pd.DataFrame(records)
    df['startDate'] = pd.to_datetime(df['startDate'], errors='coerce')
    df['endDate']   = pd.to_datetime(df['endDate'],   errors='coerce')
    df['value']     = pd.to_numeric(df['value'], errors='coerce')
    df = df.dropna(subset=['startDate'])
    df['date'] = df['startDate'].dt.date

    # Filter to key metrics
    steps = df[df['type'].str.contains('StepCount')]
    heart = df[df['type'].str.contains('HeartRate')]
    active = df[df['type'].str.contains('ActiveEnergyBurned')]
    exercise = df[df['type'].str.contains('ExerciseTime')]
    distance = df[df['type'].str.contains('DistanceWalkingRunning')]

    return {
        'steps':    steps,
        'heart':    heart,
        'active':   active,
        'exercise': exercise,
        'distance': distance,
        'raw':      df
    }

def weekly_summary(data: dict) -> pd.DataFrame:
    """Aggregate all metrics into a weekly summary DataFrame."""
    steps_wk = (
        data['steps'].groupby('date')['value'].sum()
        .reset_index().rename(columns={'value': 'steps'})
    )
    steps_wk['date'] = pd.to_datetime(steps_wk['date'])
    steps_wk['week'] = steps_wk['date'].dt.to_period('W')
    weekly = steps_wk.groupby('week')['steps'].sum().reset_index()

    exercise_wk = (
        data['exercise'].groupby('date')['value'].sum()
        .reset_index().rename(columns={'value': 'exercise_min'})
    )
    exercise_wk['date'] = pd.to_datetime(exercise_wk['date'])
    exercise_wk['week'] = exercise_wk['date'].dt.to_period('W')
    ex_weekly = exercise_wk.groupby('week')['exercise_min'].sum().reset_index()

    weekly = weekly.merge(ex_weekly, on='week', how='left').fillna(0)
    weekly['week_str'] = weekly['week'].astype(str)
    return weekly
