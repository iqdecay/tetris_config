import json


class BeaconDevice:
    def __init__(self, id):
        self.id = id
        # User-defined via the web interface
        self.name = ""
        self.acknowledged = False
        # JSON string representing the last ACK response received
        self.last_ack_response = ""
        # Status code for the downlink message transmission
        self.last_downlink_status = ""
        self.last_downlink_timestamp = ""

    def __repr__(self):
        return f"Device with id {self.id} named {self.name}, ack = {self.acknowledged}, time = " \
               f"{self.last_downlink_timestamp} downlink_status = {self.last_downlink_status} " \
               f"{self.last_ack_response}"


class BeaconDeviceJSONEncoder(json.JSONEncoder):
    def default(self, o: BeaconDevice) -> dict:
        return o.__dict__
