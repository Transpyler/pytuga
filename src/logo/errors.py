class InvalidResponseError(Exception):
    """
    Raised when client receives an invalid response.
    """


class InvalidMessageError(Exception):
    """
    Raised when server encounter invalid messages.
    """