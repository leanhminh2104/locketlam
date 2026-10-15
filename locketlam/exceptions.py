class LocketError(Exception):
    """Base exception for all errors in the locketlam library."""
    pass

class AuthenticationError(LocketError):
    """Raised when authentication fails (invalid credentials, expired token, or blocked request)."""
    pass

class LocketAPIError(LocketError):
    """Raised when the Locket Camera backend returns an API error."""
    def __init__(self, message: str, status_code: int = None, response_data: dict = None):
        super().__init__(message)
        self.status_code = status_code
        self.response_data = response_data

class StorageUploadError(LocketError):
    """Raised when binary uploads to Google Firebase Storage fail."""
    pass
