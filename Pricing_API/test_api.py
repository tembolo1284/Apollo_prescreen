import requests
import math
import json
from datetime import datetime, timedelta
"""
# Can also call the API using the below curl command.
curl -X POST http://127.0.0.1:8000/calculate_bond \
-H 'Content-Type: application/json' \
-d '{
    "bond_type": "Corporate",
    "face_value": 1000.0,
    "coupon_rate": 0.05,
    "maturity": 10.0,
    "yield_to_maturity": null,
    "issue_date": "2022-07-20T22:43:59.567602",
    "maturity_date": "2032-07-17T22:43:59.567602"
}'

"""
url = "http://127.0.0.1:8000/calculate_bond"
params = {
    "bond_type": "Corporate",
    "face_value": 1000.0,
    "coupon_rate": 0.05,
    "maturity": 10.0,
    "yield_to_maturity": None,
    "issue_date": (datetime.now() - timedelta(days=365)).isoformat(),  # Set issue date as 1 year ago
    "maturity_date": (datetime.now() + timedelta(days=365*9)).isoformat()  # Set maturity date as 9 years from now
}
headers = {'Content-Type': 'application/json'}
print(params)
response = requests.post(url, data=json.dumps(params), headers=headers)
response_data = response.json()

# Check for NaN values
if math.isnan(response_data["NPV"]) or math.isnan(response_data["YTM"]) or \
        math.isnan(response_data["Spread"]):
    print("Error: NaN value detected in calculation.")
else:
    print("-------response_data-------")
    print(response_data)
