import requests
import pytest
import urllib
import os

BASE_URL = "https://demo.thingsboard.io"
jwt_token=os.getenv("JWT_TOKEN")
DEVICE_NAME = "DHT22 Demo Device"
headers = {"X-Authorization": f"Bearer {jwt_token}"}


@pytest.fixture(scope="session")
def device_id():
    DEVICE=urllib.parse.quote(DEVICE_NAME)
    print(DEVICE)
    resp_devices = requests.get(f"https://demo.thingsboard.io/api/tenant/devices?deviceName={DEVICE}", headers=headers)
    if not resp_devices:
        print("Device not found")
        pytest.fail(f"Device '{DEVICE_NAME}' not found")
    else:
        assert resp_devices.status_code==200
        devices = resp_devices.json().get("id", [])
        return devices["id"]
    

def test_api_telemetry(device_id):
    print("Validate if the device has model influence telemetry data")
    resp_dev=requests.get(f"https://demo.thingsboard.io/api/plugins/telemetry/DEVICE/{device_id}/values/timeseries?keys=temperature,anomaly,confidence",headers=headers)
    print(resp_dev.content)
    assert resp_dev.status_code==200

    if not resp_dev:
        pytest.fail("No response data received")
    else:
        resp_data=resp_dev.json()

        assert "anomaly" in resp_data, "Missing Anamoly data the device is not model influenced"
        assert "confidence" in resp_data, "Missing Confidence data the device is not model-influence"



