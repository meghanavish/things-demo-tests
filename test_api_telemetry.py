import requests
import pytest
import urllib
import os

BASE_URL = "https://demo.thingsboard.io"
#jwt_token="eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJnZWV2aXNod2FuYXRoMDAxQGdtYWlsLmNvbSIsInVzZXJJZCI6ImFlNDM5NmUwLTQ3N2ItMTFmMC05MDViLTcxNTE4OGFkMmNkOCIsInNjb3BlcyI6WyJURU5BTlRfQURNSU4iXSwic2Vzc2lvbklkIjoiZDY4MjU3NDktMDgwNi00YmQ5LTllYmEtMjI0MjdlZjljZGZhIiwiZXhwIjoxNzUxNTk1NzI3LCJpc3MiOiJ0aGluZ3Nib2FyZC5pbyIsImlhdCI6MTc0OTc5NTcyNywiZmlyc3ROYW1lIjoibWVnaGFuYSIsImxhc3ROYW1lIjoibiIsImVuYWJsZWQiOnRydWUsInByaXZhY3lQb2xpY3lBY2NlcHRlZCI6dHJ1ZSwiaXNQdWJsaWMiOmZhbHNlLCJ0ZW5hbnRJZCI6ImFlMWNmYzEwLTQ3N2ItMTFmMC05MDViLTcxNTE4OGFkMmNkOCIsImN1c3RvbWVySWQiOiIxMzgxNDAwMC0xZGQyLTExYjItODA4MC04MDgwODA4MDgwODAifQ.abTp-2O3e361BGfWU9NY9Oss72iI-Gt9c2s8kpPvppyUCXKd8IZKwuD9qKZKDPBSUOBAg4CWT2cKUI8Ukn7_BA"
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



