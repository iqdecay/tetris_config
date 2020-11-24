from random import choice, randint

from utils import change_endianness, generate_mask
import constants as CN


def binary_choice():
    """Randomly choose an integer between 0 and 1 and return it"""
    return choice([0, 1])


def generate_round_float(min_bound: int, max_bound: int,
                         precision: float) -> float:
    """
    Return a random float in [min_bound, max_bound] rounded down to precision
    """
    rand_int = randint(min_bound / precision, max_bound / precision)
    rand_float = rand_int * precision
    return round(rand_float, 5)


def generate_random_config_data() -> dict:
    """
    Return random supervision data based on technical specification
    """
    data = {
        'seuil_min_ana30v': generate_round_float(0, 30, .25),
        'activ_min_ana30v': binary_choice(),
        'seuil_max_ana30v': generate_round_float(0, 30, .25),
        'activ_max_ana30v': binary_choice(),
        'seuil_min_ana100mv': generate_round_float(-100, 100, 1),
        'seuil_max_ana100mv': generate_round_float(-100, 100, 1),
        'duree_cycle_feux': generate_round_float(1, 32, 1),
        'acq_position_base': binary_choice(),
        'activ_min_ana100mv': binary_choice(),
        'activ_max_ana100mv': binary_choice(),
        'active_tor1': binary_choice(),
        'active_tor2': binary_choice(),
        'active_tor3': binary_choice(),
        'active_tor4': binary_choice(),
        'active_tor5': binary_choice(),
        'active_tor6': binary_choice(),
        'sens_tor1': binary_choice(),
        'sens_tor2': binary_choice(),
        'sens_tor3': binary_choice(),
        'sens_tor4': binary_choice(),
        'sens_tor5': binary_choice(),
        'sens_tor6': binary_choice(),
        'delai_envoi': generate_round_float(0, 7, 1),
        'delai_repet': choice([10, 30]),
        'r_deradage': generate_round_float(0, 31, 1),
        'sommeil': 0,
        'switch_config': binary_choice(),
        'trame_reçue': 1,
    }
    return data


def encode_signed_integer(num: int, size: int) -> int:
    """
    Encode signed integer *num* in two's complement representation
    over *size* bits and return it
    """
    mask = generate_mask(size)
    twoc_rep = num & mask
    return twoc_rep


def encode_unsigned_integer(num: int, size: int) -> int:
    """
    Encode signed integer *num* over *size* bits and return it
    """
    assert num >= 0
    return num


def special_value_to_int(value: float, key: str, modifier: float) -> int:
    """
    Return float *value* as its code integer using *modifier*, and depending on the data origin
    """
    if key == "delai_repet":
        # Don't use the [] syntax to avoid possible key errors
        for key, modifier_value in modifier.items():
            if value == modifier_value:
                return key
    elif key == "duree_cycle_feux":
        return value - modifier
    elif key in ["seuil_min_ana30v", "seuil_max_ana30v"]:
        return int(round(value / modifier))
    else:
        raise TypeError(f"The key is unexpected : got {key}")


def build_hex_number(data: dict, extractors_dictionary: dict) -> int:
    """
    Build big endian hexadecimal number representing *data*, convert it
    to little endian and return it
    :param data: supervision or configuration data from Sigfox
    :return "hexa" int in little endian (actually just an int for python)
    """
    underlying_int = 0
    for key, info in data.items():
        extractor = extractors_dictionary[key]
        data_origin = extractor.data_origin
        if extractor.is_special:
            value_as_int = special_value_to_int(info, key, extractor.value_modifier)
        else:
            value_as_int = info
        if extractor.is_signed:
            value_as_num = encode_signed_integer(value_as_int, extractor.size)
        else:
            value_as_num = value_as_int
        data_as_int = value_as_num << extractor.rshift
        underlying_int += data_as_int
    big_endian = hex(underlying_int)
    if len(big_endian) % 2 != 0:
        big_endian = big_endian.replace("0x", "0x0")
    little_endian = change_endianness(big_endian)
    return little_endian
