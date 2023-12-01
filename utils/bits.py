def test_bit(int_type, offset):
    """
    testBit() returns a nonzero result, 2**offset, if the bit at 'offset' is one.
    """
    mask = 1 << offset
    return int_type & mask


def set_bit(int_type, offset):
    """
    setBit() returns an integer with the bit at 'offset' set to 1.
    """
    mask = 1 << offset
    return int_type | mask


def clear_bit(int_type, offset):
    """
    clearBit() returns an integer with the bit at 'offset' cleared.
    """
    mask = ~(1 << offset)
    return int_type & mask


def toggle_bit(int_type, offset):
    """
    toggleBit() returns an integer with the bit at 'offset' inverted, 0 -> 1 and 1 -> 0.
    """
    mask = 1 << offset
    return int_type ^ mask
