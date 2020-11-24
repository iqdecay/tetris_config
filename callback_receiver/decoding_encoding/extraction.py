from .Extractor import Extractor
import constants as CN

# ------- CONFIGURATION DATA ------
# Given in technical specification

# Key names are not relevant to the user side
config_keys = [
    'seuil_min_ana30v', 'activ_min_ana30v', 'seuil_max_ana30v',
    'activ_max_ana30v', 'seuil_min_ana100mv', 'seuil_max_ana100mv',
    'duree_cycle_feux', 'acq_position_base', 'activ_min_ana100mv',
    'activ_max_ana100mv', 'active_tor1', 'active_tor2', 'active_tor3',
    'active_tor4', 'active_tor5', 'active_tor6', 'sens_tor1', 'sens_tor2',
    'sens_tor3', 'sens_tor4', 'sens_tor5', 'sens_tor6', 'delai_envoi',
    'delai_repet', 'r_deradage', 'sommeil', 'switch_config', 'trame_reçue'
]
# Size in bit of each part of the data in the hex payload
bit_sizes = [7, 1, 7, 1, 8, 8, 5, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
             3, 1, 5, 1, 1, 1]
# Keys that need more work than simple int conversion
special_keys = ["seuil_min_ana30v", "seuil_max_ana30v", "duree_cycle_feux",
                "delai_repet"]
# Signed int keys
signed_keys = ["seuil_min_ana100mv", "seuil_max_ana100mv"]
# Not used here
boolean_keys = []
# Used for special keys
value_modifiers = {
    "seuil_min_ana30v": 0.25,
    "seuil_max_ana30v": 0.25,
    "duree_cycle_feux": 1,
    "delai_repet": {0: 10, 1: 30},
}


def build_extraction_dictionary(sizes: List[int], data_keys: List[str],
                                special_keys: List[str], signed_keys: List[str],
                                boolean_keys: List[str], value_modifier: dict):
    """
    Build an extraction dictionary to help extracting information from an
    hexadecimal string and return it
    :param sizes: size in bit of the different pieces of data
    :param data_keys: name of the different pieces of data
    :param special_keys: key of data that needs special treatment
    (scaling or int to float conversion)
    :param signed_keys: key of signed data
    :param boolean_keys: key of boolean data
    :param value_modifier: value modifiers for special_data
    :return: the extraction dictionary
    """
    d = dict()
    bit_position = 0
    for key, size in zip(data_keys, sizes):
        extractor = Extractor(bit_position, size, data_origin)
        bit_position += size
        if key in special_keys:
            extractor.is_special = True
            if key in value_modifier:
                extractor.value_modifier = value_modifier[key]
        if key in signed_keys:
            extractor.is_signed = True
        if key in boolean_keys:
            extractor.is_boolean = True
        d[key] = extractor
    # Must be 96 ( 24 hex characters)
    err_str = f"The bit position is {bit_position}, expected {sum(sizes)}"
    assert bit_position == sum(sizes), AssertionError(err_str)
    return d


config_encoding_dict = build_extraction_dictionary(bit_sizes,
                                                   config_keys,
                                                   special_keys,
                                                   signed_keys,
                                                   boolean_keys,
                                                   value_modifiers)
