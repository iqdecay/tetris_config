import logging
import sys
import json

from twisted.web.server import Site
from twisted.web.resource import Resource
from twisted.internet import reactor, endpoints

import constants as CN
from decoding_encoding import extraction, encode
from utils import camel_case_to_snake, format_timestamp, url_encoded_to_json

from .api_requests import get_request, post_request

JSON = b"application/json"
URL_ENCODED = b"application/x-www-form-urlencoded"
HEADER = b"<!DOCTYPE html><html><head><meta charset='utf-8'>"
SUCCESS_NO_CONTENT = ("", 204)


class CallbackReceiver(Resource):
    def __init__(self, file_logging=True, console_logging=False,
                 backend_address: str = "localhost",
                 backend_port: str = "4000"):
        super().__init__()
        logging_handlers = []
        if console_logging:
            logging_handlers.append(logging.StreamHandler(sys.stdout))
        if file_logging:
            logging_handlers.append(logging.FileHandler(CN.LOG_FILENAME))
        logging.basicConfig(level=logging.INFO,
                            format="%(asctime)s [%(levelname)s] %(message)s",
                            handlers=logging_handlers, )
        logging.info(f"Initialized the HTTP server on port {CN.HTTP_PORT}")
        self.address = backend_address
        self.port = backend_port
        logging.info(f"API calls will be made to {self.address}:{self.port}")

    def build_api_url(self, api_endpoint: str) -> str:
        """
        Take an endpoint string and build a valid url for an API call out of it
        """
        api_endpoint = api_endpoint.strip("/")
        return f"http://{self.address}:{self.port}/{api_endpoint}/"

    @staticmethod
    def render_not_accepted_method(request):
        """
        Return 405 error when server receives a non-POST request
        """
        request.setResponseCode(405)
        return HEADER + b"<body>Method not accepted for TeTris app</body>"

    @staticmethod
    def format_config_data(config_json: dict) -> dict:
        """
        Take a configuration dictionnary extracted from JSON and turn it into a
        valid sigfox configuration : switch to snake case, remove the name entry,
        perform int or float conversion, and set trame_reçue to 1
        :param config_json: the dictionary in camel case
        :return: the transformed dictionary in snake case
        """
        del config_json["name"]
        config_json["trameReçue"] = 1
        snake_config = dict()
        for camel_key, item in config_json.items():
            snake_key = camel_case_to_snake(camel_key)
            if snake_key in ("seuil_min_ana30v", "seuil_max_ana30v"):
                item_with_type = float(item)
            else:
                item_with_type = int(item)
            snake_config[snake_key] = item_with_type
        return snake_config

    @staticmethod
    def format_device_data(info_json: dict) -> dict:
        """
        Take a dictionary received via an acknowledgement request, transform it
        so it can be processed by the backend and return it
        :param info_json: the JSON received from Sigfox
        :return: dict with the correct content for backend
        """
        device_info = dict()
        # Time is represented as string in backend
        info_json["time"] = format_timestamp(info_json["time"])
        # The backend uses camel case
        device_info["lastAckResponse"] = info_json
        device_info["downlinkTimestamp"] = info_json["time"]
        device_info["lastDownlinkStatus"] = info_json["infoCode"]
        device_info["acknowledged"] = info_json["downlinkAck"]
        return device_info

    def render_GET(self, request):
        logging.warning(f"Received unsupported GET request")
        return self.render_not_accepted_method(request)

    def render_PUT(self, request):
        logging.warning(f"Received unsupported PUT request")
        return self.render_not_accepted_method(request)

    def render_POST(self, request):
        headers = dict(request.requestHeaders.getAllRawHeaders())
        content_type_header = headers[b'Content-Type'][0]
        if content_type_header == JSON:
            logging.info(f"Received POST request with JSON media type")
            content = request.content.read().decode(CN.UTF8)
            try:
                content_as_json = json.loads(content)
            except json.decoder.JSONDecodeError:
                logging.warning("Wrong json data")
                request.setResponseCode(400)
                return "", HEADER + b"<body> Wrong json data </body>"
        elif content_type_header == URL_ENCODED:
            data_encoded = request.args
            content_as_json = url_encoded_to_json(data_encoded)
        else:
            logging.info(f"Received POST request with unsupported media type")
            request.setResponseCode(415)
            return HEADER + b"<body>Unsupported media type</body>"
        # Prepare the response
        resp_string, resp_code = self.generate_POST_response(content_as_json)
        request.setResponseCode(resp_code)
        return resp_string.encode(CN.UTF8)

    def generate_POST_response(self, json_content):
        if "ack" in json_content:
            # The device is asking for configuration
            if json_content["ack"]:
                return self.handle_configuration_request(json_content)
            else:
                return SUCCESS_NO_CONTENT
        # The device is acknowledging the configuration data it received
        elif "downlinkAck" in json_content:
            self.handle_acknowledgement(json_content)
            return SUCCESS_NO_CONTENT
        # The device is sending supervision data or unsupported payload
        else:
            return SUCCESS_NO_CONTENT

    def handle_configuration_request(self, json_content):
        id_device = json_content["device"]
        logging.info(f"Received configuration demand from device {id_device}")
        # Update the info on the device
        device_data = {"time": format_timestamp(json_content["time"])}
        info_url = self.build_api_url(f"info/{id_device}")
        post_request(info_url, device_data)
        # Get the configuration for this device
        config_url = self.build_api_url(f"config/{id_device}/")
        api_data = get_request(config_url)
        if api_data is not None:
            config_data = self.format_config_data(api_data)
            hex_data = encode.build_hex_number(config_data,
                                               extraction.config_encoding_dict)
            response = {
                id_device:
                    {"downlinkData": hex_data}
            }
            response = json.dumps(response, sort_keys=True, indent=2)
            return response, 200
        else:
            return SUCCESS_NO_CONTENT

    def handle_acknowledgement(self, json_content):
        # Update the info on this device in the backend
        id_device = json_content["device"]
        logging.info(f"Received configuration acknowledgement from "
                     f"device {id_device}")
        device_data = self.format_device_data(json_content)
        url = self.build_api_url(f"info/{id_device}")
        post_request(url, device_data)


root = CallbackReceiver(file_logging=True, console_logging=True,
                        backend_port=CN.BACKEND_PORT,
                        backend_address=CN.BACKEND_URL)
root.putChild(b"", root)
factory = Site(root)
endpoint = endpoints.TCP4ServerEndpoint(reactor, CN.HTTP_PORT)
endpoint.listen(factory)
reactor.run()
