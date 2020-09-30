class ValidationError(Exception):
    """
    Base exception for input mapper.
    """
    def __init__(self, mapper=None):
        self.mapper = mapper


class InvalidAttributeValueException(ValidationError):
    """
    Raised when validation in mapper fails for some attribute.
    """

    def __init__(self, attribute, value, mapper):
        self.attribute = attribute
        self.value = value
        super().__init__(mapper)


class MissingUserInput(ValidationError):
    """
    Raised when some key in user's input is missing.
    """

    def __init__(self, attribute, mapper):
        self.attribute = attribute
        super().__init__(mapper)


class MissingValidators(ValidationError):
    """
    Raised when some key from input is missing in 'validators' dict in mapper.
    """

    def __init__(self, attribute, value, mapper):
        self.attribute = attribute
        self.value = value
        self.mapper = mapper
        super().__init__(mapper)
