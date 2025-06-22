import pandas as pd
import json
from datetime import datetime
from .json_schema import get_empty_day_log

def parse_csv_to_json(csv_path, output_path):
    df = pd.read_csv(csv_path)
    date_str = datetime.today().strftime("%Y-%m-%d")
    log = get_empty_day_log(date_str)

    if 'steps' in df.columns:
        log["steps"] = int(df['steps'].sum())
    if 'resting_hr' in df.columns:
        log["resting_hr"] = round(df['resting_hr'].mean(), 1)
    if 'calories_burned' in df.columns:
        log["calories_burned"] = int(df['calories_burned'].sum())
    if 'weight' in df.columns:
        log["weight"] = round(df['weight'].mean(), 1)

    with open(output_path, 'w') as f:
        json.dump(log, f, indent=2)

    return output_path
