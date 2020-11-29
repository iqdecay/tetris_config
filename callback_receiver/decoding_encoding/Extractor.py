class Extractor:
    """
    Holds information to help extract data from an hexadecimal string
    """

    def __init__(self, rshift, n_bits):
        # position of the first relevant bit in the string, is used for right-shifting the bits
        self.rshift = rshift
        self.size = n_bits  # length in bit
        # needs special treatment (int to float or scaling)
        self.is_special = False
        self.is_signed = False
        self.is_boolean = False
        self.value_modifier = None  # contains a value if is_special is True

    def __repr__(self):
        return f"{self.rshift}, {self.size}"
