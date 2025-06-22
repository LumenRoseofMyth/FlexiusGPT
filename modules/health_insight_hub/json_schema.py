def get_empty_day_log(date_str):
    return {
        "date": date_str,
        "steps": 0,
        "resting_hr": None,
        "calories_burned": None,
        "calories_intake": None,
        "weight": None,
        "sleep": {
            "duration_hours": None,
            "deep": None,
            "light": None,
            "rem": None
        },
        "bp": {
            "systolic": None,
            "diastolic": None
        },
        "notes": ""
    }
