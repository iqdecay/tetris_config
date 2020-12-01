import string
import random
import constants as CN
from server.api_requests import post_request


def device_asks_config(n=3):
    api_url = f"http://localhost:{CN.HTTP_PORT}/"
    data = {
        "ack": "true",
    }
    basetime = 1262630000
    alphanum = string.ascii_uppercase + string.digits

    for i in range(n):
        timestamp = str(basetime + random.randint(0, 1000))
        device_id = "".join(random.choices(alphanum, k=6))
        data["device"] = device_id
        data["time"] = timestamp
        post_request(api_url, data)
device_asks_config()
