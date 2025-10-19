"""
Custom exceptions for Awario API integration.
"""


class AwarioException(Exception):
    """Base exception for Awario API errors."""
    pass


class AwarioAuthenticationError(AwarioException):
    """Raised when API authentication fails."""
    pass


class AwarioRateLimitError(AwarioException):
    """Raised when API rate limit is exceeded."""
    pass


class AwarioAPIError(AwarioException):
    """Raised when API returns an error response."""
    
    def __init__(self, message: str, status_code: int = None, response_data: dict = None):
        self.message = message
        self.status_code = status_code
        self.response_data = response_data
        super().__init__(self.message)


class AwarioNetworkError(AwarioException):
    """Raised when network request fails."""
    pass


class AwarioValidationError(AwarioException):
    """Raised when request validation fails."""
    pass
