import pandas as pd
import json

def load_employee_data(json_path):
    with open(json_path, 'r') as f:
        data = json.load(f)
    return pd.DataFrame(data)

def validate_employee_data(df):
    # Basic validation: check required columns
    required = [
        'employee_id', 'name', 'department', 'role', 'skill_level',
        'current_tasks', 'hours_per_week', 'completion_rate',
        'stress_indicators', 'availability', 'last_updated'
    ]
    for col in required:
        if col not in df.columns:
            raise ValueError(f"Missing column: {col}")
    return True
