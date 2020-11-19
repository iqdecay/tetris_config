import logging
import sys
import pickle
import json
import os

from twisted.web.server import Site
from twisted.web.resource import Resource
from twisted.internet import reactor, endpoints

import constants as CN
from decoding_encoding import decode, extraction, encode
from .BeaconDevice import BeaconDevice, BeaconDeviceJSONEncoder
from utils import url_encoded_to_json

JSON = b"application/json"
URL_ENCODED = b"application/x-www-form-urlencoded"
HEADER = b"<!DOCTYPE html><html><head><meta charset='utf-8'>"


class CallbackReceiver(Resource):
    def __init__(self, file_logging=True, console_logging=False):
        super().__init__()
        logging_handlers = []
        if console_logging:
            logging_handlers.append(logging.StreamHandler(sys.stdout))
        if file_logging:
            logging_handlers.append(logging.FileHandler(CN.LOG_FILENAME))
        logging.basicConfig(level=logging.INFO,
                            format="%(asctime)s [%(levelname)s] %(message)s", handlers=logging_handlers, )
        logging.info(f"Initialized the HTTP server on port {CN.HTTP_PORT}")
        self.device_list = self.load_device_list_from_memory()

    ## TODO : load the device list from the mongodb database
    @staticmethod
    def load_device_list_from_memory():
        filename = CN.DEVICE_LIST_FILENAME
        if os.path.exists(filename):
            try:
                with open(filename, 'rb') as file:
                    # Protocol version used is automatically detected, no need to specify it
                    device_list = json.load(file)
                    return device_list
            except EOFError:
                logging.warning(f"Empty device list found in {filename} in {os.getcwd()}")
                return dict()
            except Exception as e:
                logging.error(e)
                raise e
        else:
            logging.warning(f"No file found for device list, {filename} will be created in {os.getcwd()} if needed")
            return {}

    @staticmethod
    def render_not_accepted_method(request):
        """
        Return 405 error when server receives a non-POST request
        """
        request.setResponseCode(405)
        return HEADER + b"<body>Method not accepted for TeTris app</body>"

    @staticmethod
    def format_config_data():
        # The server wants a configuration message :
        random_data = encode.generate_random_config_data()
        hex_data = encode.build_hex_number(random_data, extraction.config_encoding_dict)
        return hex_data

    @staticmethod
    def extract_and_format_supervision_data(post_json_content):
        # lowercase the keys to avoid confusion
        post_json_content = {key.lower(): value for (key, value) in post_json_content.items()}
        formatted_json = {}
        # Normalize key names
        for (key, value) in post_json_content.items():
            if key not in ("data", "true_data"):
                if key in extraction.supervision_post_keys_to_json:
                    corresponding_key = extraction.supervision_post_keys_to_json[key]
                    formatted_json[corresponding_key] = value
                else:
                    formatted_json[key] = value
        hex_data = post_json_content["data"]
        decoded_data = decode.from_hex_to_data(hex_data, extraction.supervision_decoding_dict)
        for (key, value) in decoded_data.items():
            formatted_json[key] = value
        json_string = json.dumps(formatted_json, sort_keys=True, indent=2)
        return json_string

    @staticmethod
    def request_to_json(request):
        headers = dict(request.requestHeaders.getAllRawHeaders())
        content_type_header = headers[b'Content-Type'][0]
        if content_type_header == JSON:
            logging.info(f"Received POST request with JSON media type")
            content = request.content.read().decode(CN.UTF8)
            try:
                json_content = json.loads(content)
            except json.decoder.JSONDecodeError:
                logging.warning("Empty json data")
                request.setResponseCode(400)
                return HEADER + b"<body> Empty json data </body>"
        elif content_type_header == URL_ENCODED:
            logging.info(f"Received POST request with url-encoded media type")
            data_encoded = request.args
            json_content = url_encoded_to_json(data_encoded)
        else:
            logging.info(f"Received POST request with unsupported media type")
            request.setResponseCode(415)
            return HEADER + b"<body>Unsupported media type</body>"
        return json_content

    def render_GET(self, request):
        logging.warning(f"Received GET request with content {request.content.read()}")
        self.save_device_list()
        return self.render_not_accepted_method(request)

    def render_PUT(self, request):
        logging.warning(f"Received PUT request")
        return self.render_not_accepted_method(request)

    def render_POST(self, request):
        content_as_json = self.request_to_json(request)
        # Prepare the response
        response_string, response_code = self.generate_POST_response(content_as_json)
        request.setResponseCode(response_code)
        if response_code == 200:
            request.responseHeaders.addRawHeader(b"content-type",
                                                 b"application/json")
        return response_string.encode(CN.UTF8)

    def generate_POST_response(self, json_content):
        # The device is asking for configuration data
        if "ack" in json_content:
            # Get the device id for answering back to it if needed
            id_device = json_content["device"]
            if id_device not in self.device_list:
                logging.info(f"New beacon with id {id_device} detected")
                self.device_list[id_device] = BeaconDevice(id_device)
                self.save_device_list()
            if json_content["ack"] == "true":
                logging.info(f"Received configuration demand from device {id_device}")
                hex_data = self.format_config_data()
                response = {
                    id_device:
                        {"downlinkData": hex_data}
                }
                response = json.dumps(response, sort_keys=True, indent=2)
                # Will be set to true once we receive acknowledgement from the device
                self.device_list[id_device].acknowledged = False
                self.save_device_list()
                return response, 200
            return "", 204
        # The device is sending supervision data
        elif "data" in json_content:
            try:
                response = self.extract_and_format_supervison_data(json_content)
                return response, 200
            except Exception as e:
                logging.warning(e)
                return "<body> Incorrect json data </body>", 403
        # The device is acknowledging the configuration data it received
        elif "downlinkAck" in json_content:
            id_device = json_content["device"]
            logging.info(f"Received configuration acknowledgement from device {id_device}")
            self.device_list[id_device].last_ack_response = json_content
            self.device_list[id_device].last_downlink_timestamp = json_content["time"]
            self.device_list[id_device].last_downlink_status = json_content["infoCode"]
            self.device_list[id_device].acknowledged = True
            self.save_device_list()
            return "", 204
        else:
            return "", 204

    ## TODO : write the device list to the mongodb database
    def save_device_list(self):
        filename = CN.DEVICE_LIST_FILENAME
        try:
            with open(filename, "w") as file:
                logging.info("Serializing device list to memory")
                # Use custom JSON serializer
                json.dump(self.device_list, file, cls=BeaconDeviceJSONEncoder, sort_keys=True, indent=2)
        except Exception as e:
            logging.error(e)


root = CallbackReceiver(file_logging=True, console_logging=True)
root.putChild(b"", root)
factory = Site(root)
endpoint = endpoints.TCP4ServerEndpoint(reactor, CN.HTTP_PORT)
endpoint.listen(factory)
reactor.run()
