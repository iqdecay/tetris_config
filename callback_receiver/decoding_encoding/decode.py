from utils import change_endianness, generate_mask


def decode_signed_integer(num: int, size: int) -> int:
    """
    Take signed integer in two's complement form and return it in default form
    :param num: signed integer in two's complement representation
    :param size: number of bits it is encoded on
    :return: signed integer
    """
    if (num & (1 << (size - 1))) != 0:
        num = num - (1 << size)
    return num


def int_to_special_value(bin_value: int, key: str, modifier):
    """
    :param bin_value: integer value extracted from hex
    :param key: data key
    :param modifier: float, int or dict of int, helps reconstitute accurate data
    :return: the correct value
    """
    if key in ["delai_repet", "delai_envoi"]:
        return modifier[bin_value]
    elif key == "duree_cycle_feux":
        return bin_value + modifier
    elif key in ["seuil_min_ana30v", "seuil_max_ana30v"]:
        return bin_value * modifier
    else:
        raise TypeError("The key is unexpected")


def from_hex_to_data(hex_string: str, extractor_dict: dict) -> dict:
    """
    Take a little-endian string, extract its data in a dictionary and return it
    :param extractor_dict:
    :param hex_string: 24 char hexadecimal string, little-endian
    :return: dictionary containing the decoded data
    """
    big_endian = change_endianness(hex_string)
    hex_number = int(big_endian, 16)
    data = {}
    for key, extractor in extractor_dict.items():
        size = extractor.size
        bin_number_long = hex_number >> extractor.rshift
        mask = generate_mask(extractor.size)
        bin_number = mask & bin_number_long
        if extractor.is_signed:
            actual_bin_value = decode_signed_integer(bin_number, size)
        else:
            actual_bin_value = bin_number
        if extractor.is_special:
            correct_value = int_to_special_value(actual_bin_value, key, extractor.value_modifier)
        elif extractor.is_boolean:
            correct_value = (actual_bin_value == 1)
        else:
            correct_value = actual_bin_value
        data[key] = correct_value
    return data
