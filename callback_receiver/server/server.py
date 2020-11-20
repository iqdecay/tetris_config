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

    def format_config_data(self, id_device: str):
        # The server wants a configuration message :
        if self.config_dict[id_device]:
            config_data = self.config_dict[id_device]
        else:
            config_data = encode.generate_random_config_data()
        hex_data = encode.build_hex_number(config_data,
                                           extraction.config_encoding_dict)
        return hex_data

    def render_GET(self, request):
        logging.warning(f"Received GET request")
        # TODO : return the data it requested
        if self.get_from_react:
            device_dict_json = json.dumps(self.device_dict,
                                          cls=BeaconDeviceJSONEncoder,
                                          sort_keys=True, indent=2)
            print(device_dict_json)
            return None
        else:
            return self.render_not_accepted_method(request)

    def render_PUT(self, request):
        logging.warning(f"Received PUT request")
        return self.render_not_accepted_method(request)

    def render_POST(self, request):
        print("Render post poto")
        headers = dict(request.requestHeaders.getAllRawHeaders())
        content_type_header = headers[b'Content-Type'][0]
        if content_type_header == JSON:
            logging.info(f"Received POST request with JSON media type")
            content = request.content.read().decode(CN.UTF8)
            try:
                content_as_json = json.loads(content)
            except json.decoder.JSONDecodeError:
                logging.warning("Empty json data")
                request.setResponseCode(400)
                return "", HEADER + b"<body> Empty json data </body>"
        else:
            logging.info(f"Received POST request with unsupported media type")
            request.setResponseCode(415)
            return HEADER + b"<body>Unsupported media type</body>"
        # Prepare the response
        resp_string, resp_code = self.generate_POST_response(content_as_json)
        request.setResponseCode(resp_code)
        if resp_code == 200:
            origin = request.requestHeaders[b"origin"]
        return resp_string.encode(CN.UTF8)

    def generate_POST_response(self, json_content):
        # The device is asking for configuration data
        if self.POST_req_from_react:
            device_id = json_content[id]
            # Name was updated
            if "name" in json_content:
                self.device_dict[id].name = json_content["name"]
            return "", 200
        if "ack" in json_content:
            # Get the device id for answering back to it if needed
            id_device = json_content["device"]
            if id_device not in self.device_dict:
                logging.info(f"New beacon with id {id_device} detected")
                self.device_dict[id_device] = BeaconDevice(id_device)
                self.save_device_dict()
            if json_content["ack"] == "true":
                logging.info(f"Received configuration demand from "
                             f"device {id_device}")
                hex_data = self.format_config_data()
                response = {
                    id_device:
                        {"downlinkData": hex_data}
                }
                response = json.dumps(response, sort_keys=True, indent=2)
                # Set to true once device acknowledgement is received
                self.device_dict[id_device].acknowledged = False
                self.save_device_dict()
                return response, 200
            return "", 204
        # The device is sending supervision data
        elif "data" in json_content:
            try:
                response = decode.extract_format_supervision_data(json_content)
                return response, 200
            except Exception as e:
                logging.warning(e)
                return "<body> Incorrect json data </body>", 403
        # The device is acknowledging the configuration data it received
        elif "downlinkAck" in json_content:
            id_device = json_content["device"]
            logging.info(f"Received configuration acknowledgement from "
                         f"device {id_device}")
            current_device = self.device_dict[id_device]
            current_device.last_ack_response = json_content
            current_device.last_downlink_timestamp = json_content["time"]
            current_device.last_downlink_status = json_content["infoCode"]
            current_device.acknowledged = json_content["downlinkAck"]
            self.device_dict[id_device] = current_device
            return "", 204
        else:
            return "", 204

    def save_device_dict(self):
        filename = CN.DEVICE_LIST_FILENAME
        try:
            with open(filename, "w") as file:
                logging.info("Serializing device dict to memory")
                # Use custom JSON serializer
                json.dump(self.device_dict, file, cls=BeaconDeviceJSONEncoder,
                          sort_keys=True, indent=2)
        except Exception as e:
            raise e

    def save_config_dict(self):
        filename = CN.CONFIG_LIST_FILENAME
        try:
            with open(filename, "w") as file:
                logging.info("Serializing config dict to memory")
                json.dump(self.device_dict, file,
                          sort_keys=True, indent=2)
        except Exception as e:
            raise e


root = CallbackReceiver(file_logging=True, console_logging=True)
root.putChild(b"", root)
factory = Site(root)
endpoint = endpoints.TCP4ServerEndpoint(reactor, CN.HTTP_PORT)
endpoint.listen(factory)
reactor.run()
