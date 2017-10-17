class BaseError(Exception):
    """Base exception class in server module"""
    pass


class ParseError(BaseError):
    """Exception raised for errors in the message format

    Attributes:
        message -- explanation of the error
    """
    def __init__(self, message):
        super().__init__(message)
        self.message = message
