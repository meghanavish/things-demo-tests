import pytest
import time
import requests

# Replace this with your actual device access token from ThingsBoard
DEVICE_TOKEN = "NrV6iMibDrYxCz7OJT4d"
DEVICE_ID="bdd640d0-477b-11f0-905b-715188ad2cd8"
BASE_URL = f"https://demo.thingsboard.io/api/v1/{DEVICE_TOKEN}/telemetry"
jwt_token="eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJnZWV2aXNod2FuYXRoMDAxQGdtYWlsLmNvbSIsInVzZXJJZCI6ImFlNDM5NmUwLTQ3N2ItMTFmMC05MDViLTcxNTE4OGFkMmNkOCIsInNjb3BlcyI6WyJURU5BTlRfQURNSU4iXSwic2Vzc2lvbklkIjoiMmVmYzgyYWEtZjJjNy00YzEzLWIyNDctOGY1OGU2OTUzNTUwIiwiZXhwIjoxNzUxNTI1NzU4LCJpc3MiOiJ0aGluZ3Nib2FyZC5pbyIsImlhdCI6MTc0OTcyNTc1OCwiZmlyc3ROYW1lIjoibWVnaGFuYSIsImxhc3ROYW1lIjoibiIsImVuYWJsZWQiOnRydWUsInByaXZhY3lQb2xpY3lBY2NlcHRlZCI6dHJ1ZSwiaXNQdWJsaWMiOmZhbHNlLCJ0ZW5hbnRJZCI6ImFlMWNmYzEwLTQ3N2ItMTFmMC05MDViLTcxNTE4OGFkMmNkOCIsImN1c3RvbWVySWQiOiIxMzgxNDAwMC0xZGQyLTExYjItODA4MC04MDgwODA4MDgwODAifQ.ONYPwoyCIQMwk8zaY0-dNfzWd8UGsWWGf8j250GgxmkwUX5C7z9havcYhnBac3oJOxEBkfHfcun1fYUyHaf31A"
HEADERS = headers = {
    "Content-Type": "application/json",
    "X-Authorization": f"Bearer {jwt_token}"}
AUTHORIZATION_HEADER={"X-Authorization": f"Bearer {jwt_token}"}

def test_delete_anomaly_prediction_before_test():
    print("TEST 1: Delete existing anomaly or predictions if any")
    url = (f"https://demo.thingsboard.io/api/plugins/telemetry/DEVICE/{DEVICE_ID}/timeseries/delete?keys=anomaly,prediction"f"?keys=anomaly,prediction&deleteAllDataForKeys=true")
    response = requests.delete(url, headers=AUTHORIZATION_HEADER)
    print(response.content)
    assert response.status_code==200


def test_missing_telemetry_response():
    print("TEST 2 - Check for Anamoly or Predictions")
    url = f"https://demo.thingsboard.io/api/plugins/telemetry/DEVICE/{DEVICE_ID}/values/timeseries"
    read_resp = requests.get(url,headers=AUTHORIZATION_HEADER)
    print(read_resp.content)
    assert read_resp.status_code == 200

    telemetry = read_resp.json()
    assert "anomaly" not in telemetry or not telemetry["anomaly"], "Anomaly should not exist"
    assert "prediction" not in telemetry or not telemetry["prediction"], "Prediction should not exist"



@pytest.mark.parametrize("payload", [
    {"anomaly": False, "prediction": 26.4},
    {"anomaly": True, "prediction": 89.2},
])


def test_send_and_validate_model_telemetry(payload):
    print("TEST 1 - Update the device with Anomaly and predictions and validate")
    resp = requests.post(BASE_URL, headers=HEADERS, json=payload)
    print(resp.content)
    assert resp.status_code == 200, "Failed to send telemetry"

    fetch_url = f"https://demo.thingsboard.io/api/plugins/telemetry/DEVICE/{DEVICE_ID}/values/timeseries"
    read_resp = requests.get(fetch_url,headers=AUTHORIZATION_HEADER)
    print(read_resp.content)
    assert read_resp.status_code == 200, "Failed to read telemetry"

    telemetry = read_resp.json()
    for key in payload:
        assert key in telemetry, f"{key} not found in telemetry"




def test_invalid_telemetry_data():
    print("TEST 3 - Test invalid data")
    payload = {"anomaly": "maybe", "prediction": "NaN"}
    resp = requests.post(BASE_URL, headers=HEADERS, json=payload)
    print(resp.content)
    assert resp.status_code == 200, "Telemetry post should not fail, but should be handled gracefully"