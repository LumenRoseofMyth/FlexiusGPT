import requests
import os

url = "http://127.0.0.1:8000/module"
headers = {
    "X-API-KEY": os.environ.get("FLEXIUSGPT_API_KEY"),
    "Content-Type": "application/json"
}
data = {
    "module_id": "04_safety_overrides",
    "action": "enforce_safety_protocols",
    "user_log": {
        "hrv_score": 20,
        "sleep_hours": 4,
        "reported_illness": False
    }
}

response = requests.post(url, json=data, headers=headers)
print("Status:", response.status_code)
print("Response:", response.text)
