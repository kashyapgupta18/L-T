"""Domain exceptions for L&T Hazira Platform."""

class PlatformException(Exception):
    """Base exception for the platform."""
    pass

class DataValidationError(PlatformException):
    """Raised when data records violate schema constraints or physical limits."""
    pass

class DatabaseConnectionError(PlatformException):
    """Raised when SQLite connection fails or database cannot be opened."""
    pass

class ModelInferenceError(PlatformException):
    """Raised when feature engineering or model inference fails."""
    pass

class ETLPipelineError(PlatformException):
    """Raised when an ETL pipeline stage fails."""
    pass
