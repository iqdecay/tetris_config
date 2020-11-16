import math
import html

import constants as CN


def url_encoded_to_json(encoded_form):
    """
    Transform url-encoded data (type "application/x-www-form-urlencoded")
    into JSON and lowercase the argument names on the fly
    :param encoded_form: the request arguments
    :return: JSON dictionary
    """
    json_dict = {}
    for key, value in encoded_form.items():
        decoded_key = key.decode(CN.UTF8)
        escaped_key = html.escape(decoded_key)
        if len(value) > 1:
            raise IndexError(
                "The field {} has too many values".format(escaped_key))
        decoded_value = value[0].decode(CN.UTF8)
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
