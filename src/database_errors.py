"""
Define database module errors
"""


class InvalidInitializer(Exception):
    """
    Error to raise when the argument that initializes some object is invalid
    """
    def __init__(self):
        self.message = "Invalid initialization value"


class InvalidSize(Exception):
    """
    Error to raise when some object has more entries than it should
    """
    pass
