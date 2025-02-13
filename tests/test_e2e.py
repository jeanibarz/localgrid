import os
import time
import requests

MAIN_APP_URL = os.environ.get('MAIN_APP_URL', 'http://main-app:8000')

def test_integration():
    # Wait for the main app to be ready
    for _ in range(10):
        try:
            r = requests.get(f"{MAIN_APP_URL}/run")
            if r.status_code == 200:
                break
        except Exception:
            pass
        time.sleep(2)
    else:
        assert False, "Main app not reachable"

    response = requests.get(f"{MAIN_APP_URL}/run")
    data = response.json()
    assert data.get('postgres') == 'test name'
    assert data.get('redis') == 'bar'
    assert data.get('grpc') == 'Hello, World'
    assert data.get('s3') == 'Hello S3'
