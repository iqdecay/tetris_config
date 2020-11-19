from .Extractor import Extractor
import constants as CN

# ------- SUPERVISION DATA ------
# Used to convert the POST data keys to supervision data
supervision_post_keys_to_json = {
    "avgsnr": "avgsnr",
    "data": "data",
    "device": "id_device",
    "duplicate": "duplicate",
    "lat": "lat_station",
    "lng": "long_station",
    "rssi": "rssi",
    "seqnumber": "seqnumber",
    "snr": "snr",
    "station": "station",
    "time": "time",
}

# Given in technical specification
supervision_keys = ['lat', 'long', 'temperature', 'ana_int', 'ana_int2', 'type_send',
                    'seuil_ana_int', 'seuil_ana_int2', 'hygro',
                    'niveau_batt', 'config_switch', 'di0', 'di1', 'di2', 'di3', 'di4',
                    'di5', 'indice_gps', 'de_di0', 'de_di1',
                    'de_di2', 'de_di3', 'de_di4', 'de_di5', 'off_pos', 'config_off_pos']
# Size in bit of each part of the data in the hex payload
supervision_bit_sizes = [20, 21, 7, 9, 11, 2, 1, 1, 5, 2, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1,
                         1, 1, 1, 1, 1]
supervision_special_keys = ["lat", "long", "temperature", "ana_int", "ana_int2", "hygro"]
supervision_signed_keys = ["lat", "long", "ana_int2"]
supervision_boolean_keys = ["seuil_ana_int", "seuil_ana_int2"]
# Used for scaling or int-float conversion
supervision_value_modifier = {
    "lat": 0.0002,
    "long": 0.0002,
    "ana_int": 0.1,
    "ana_int2": 0.1,
    "hygro": 5,
    "temperature": 40,
}

# ------- CONFIGURATION DATA ------
# Given in technical specification

# Key names are not relevant to the user side
config_keys = [
    'seuil_min_ana30v', 'activ_min_ana30v', 'seuil_max_ana30v', 'activ_max_ana30v', 'seuil_min_ana100mv',
    'seuil_max_ana100mv', 'duree_cycle_feux', 'acq_position_base', 'activ_min_ana100mv', 'activ_max_ana100mv',
    'active_tor1', 'active_tor2', 'active_tor3', 'active_tor4', 'active_tor5', 'active_tor6',
    'sens_tor1', 'sens_tor2', 'sens_tor3', 'sens_tor4', 'sens_tor5', 'sens_tor6', 'delai_envoi', 'delai_repet',
    'r_deradage', 'sommeil', 'switch_config', 'trame_reçue'
]
# Size in bit of each part of the data in the hex payload
config_bit_sizes = [7, 1, 7, 1, 8, 8, 5, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1, 5, 1, 1, 1]
config_special_keys = ["seuil_min_ana30v", "seuil_max_ana30v", "duree_cycle_feux", "delai_repet", "delai_envoi"]
config_signed_keys = ["seuil_min_ana100mv", "seuil_max_ana100mv"]
config_boolean_keys = []
config_value_modifiers = {
    "seuil_min_ana30v": 0.25,
    "seuil_max_ana30v": 0.25,
    "duree_cycle_feux": 1,
    "delai_repet": {0: 10, 1: 30},
    "delai_envoi": {0: 10, 1: 20, 2: 30, 3: 60, 4: 120, 5: 240, 6: 360, 7: 720},
}


def build_extraction_dictionary(data_origin, sizes, data_keys, special_keys, signed_keys,
                                boolean_keys, value_modifier):
    """
    Build an extraction dictionary to help extracting information from an
    hexadecimal string and return it
    :param data_origin: str, saying if the data comes from supervision or configuration
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
    assert bit_position == sum(sizes), AssertionError(f"The bit position is {bit_position}, expected {sum(sizes)}")
    return d


supervision_decoding_dict = build_extraction_dictionary(CN.SUPERVISION, supervision_bit_sizes, supervision_keys,
                                                        supervision_special_keys, supervision_signed_keys,
                                                        supervision_boolean_keys,
                                                        supervision_value_modifier)

config_encoding_dict = build_extraction_dictionary(CN.CONFIG, config_bit_sizes, config_keys,
                                                   config_special_keys, config_signed_keys,
                                                   config_boolean_keys, config_value_modifiers)
