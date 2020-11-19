class Extractor:
    """
    Holds information to help extract supervision data from an hexadecimal
    string
    """

    def __init__(self, rshift, n_bits, data_origin):
        # position of the first relevant bit in the string
        self.rshift = rshift
        self.size = n_bits  # lenght in bit
        # needs special treatment (int to float or scaling)
        self.is_special = False
        self.is_signed = False
        self.is_boolean = False
        self.value_modifier = None  # contains a value if is_special is True
        self.data_origin = data_origin  # tells if data is from configuration or supervision

    def __repr__(self):
        return f"{self.rshift}, {self.size}"
