import logging
logging.basicConfig(filename="errors.log", level=logging.ERROR)

class MonasteryError(Exception):
    """Base class for exceptions in the Monastery module."""
    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message)
        self.status_code = status_code
        self.message = message
        logging.error(f"{status_code} - {message}")

class DbConnectionError(Exception):
    """Base class for exceptions for mysql database"""
    def __init__(self, message: str, status_code: int = 500):
        super().__init__(message)
        self.status_code = status_code
        self.message = message

class MonasteryNotFoundError(MonasteryError):
    """Raised when a monastery is not found in the database."""
    def __init__(self, message="Monastery not found"):
        super().__init__(message, status_code=404)

class MonasterySaveError(MonasteryError):
    """Raised when there is an error saving a monastery to the database."""
    def __init__(self, message="Monastery save error"):
        super().__init__(message, status_code=400)
        
class MonasteryUpdateError(MonasteryError):
    """Raised when there is an error updating a monastery in the database."""
    def __init__(self, message="Monastery update error"):
        super().__init__(message, status_code=400)

class MonasteryDeleteError(MonasteryError):
    """Raised when there is an error deleting a monastery from the database."""
    def __init__(self, message="Monastery delete error"):
        super().__init__(message, status_code=400)
