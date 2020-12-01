import string
import random
import os

import requests


http_port = int(os.getenv("HTTP_PORT", 8080))
def test_device_asks_config(n=3):
    api_url = f"http://localhost:{http_port}/"
    data = {
        "ack": "true",
    }
    basetime = 1262630000
    alphanum = string.ascii_uppercase + string.digits

    for i in range(n):
        timestamp = basetime + random.randint(0, 1000)
        timestamp = 1262630191
        device_id = "".join(random.choices(alphanum, k=6))
        data["device"] = device_id
        data["time"] = timestamp
        print(requests.post(api_url, json=data))
test_device_asks_config()
