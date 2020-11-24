import os
UTF8 = "utf-8"
HTTP_PORT = int(os.getenv("HTTP_PORT", 8080))
GO_PORT = str(os.getenv("GO_PORT", 4000))
LOG_FILENAME = "callback_receiver.log"
SUPERVISION = "supervision_data"
CONFIG = "configuration_data"
