import os
UTF8 = "utf-8"
HTTP_PORT = int(os.getenv("HTTP_PORT", 8080))
BACKEND_PORT = str(os.getenv("BACKEND_PORT", 4000))
BACKEND_URL = str(os.getenv("BACKEND_URL", "localhost"))

LOG_FILENAME = "callback_receiver.log"
