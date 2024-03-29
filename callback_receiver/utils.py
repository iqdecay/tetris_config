import html
import math
import re
import time


def camel_case_to_snake(camel_string: str) -> str:
    """
    Take a camel case string and return it as snake case
    """
    pattern = re.compile(r'(?<!^)(?=[A-Z])')
    snake_string = pattern.sub('_', camel_string).lower()
    return snake_string


def format_timestamp(timestamp: str) -> str:
    """
    Format a string timestamp to almost ISO8601  and return it as string
    """
    return time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(int(timestamp)))


def url_encoded_to_json(encoded_form):
    """
    Transform url-encoded data (type "application/x-www-form-urlencoded")
    into JSON and lowercase the argument names on the fly
    :param encoded_form: the request arguments
    :return: JSON dictionary
    """
    json_dict = {}
    for key, value in encoded_form.items():
        decoded_key = key.decode("utf-8")
        escaped_key = html.escape(decoded_key)
        if len(value) > 1:
            raise IndexError(
                "The field {} has too many values".format(escaped_key))
        decoded_value = value[0].decode("utf-8")
        escaped_value = html.escape(decoded_value)
        json_dict[escaped_key] = escaped_value
    return json_dict


def change_endianness(hex_string):
    hex_string = hex_string.replace("0x", "")
    try:
        ba = bytearray.fromhex(hex_string)
    except ValueError as v:
        print(f"This is the hex string {hex_string}")
        raise v
    ba.reverse()
    other_endianness = "".join(format(x, "02x") for x in ba)
    return other_endianness


def generate_mask(n):
    # Generate a mask with n bits set
    two_power_n = 1 << n
    mask = two_power_n - 1
    return mask
