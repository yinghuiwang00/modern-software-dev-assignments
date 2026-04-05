"""Custom exceptions for the application."""

from __future__ import annotations

from typing import Any


class BaseApplicationError(Exception):
    """Base exception for all application errors."""

    def __init__(
        self, message: str, status_code: int = 500, details: dict[str, Any] | None = None
    ):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.details = details or {}

    def to_dict(self) -> dict[str, Any]:
        """Convert exception to dictionary for API response."""
        error_dict = {
            "error": self.__class__.__name__,
            "message": self.message,
            "status_code": self.status_code,
        }
        if self.details:
            error_dict["details"] = self.details
        return error_dict


class DatabaseError(BaseApplicationError):
    """Exception raised when a database operation fails."""

    def __init__(
        self, message: str = "Database operation failed", details: dict[str, Any] | None = None
    ):
        super().__init__(message, status_code=500, details=details)


class ValidationError(BaseApplicationError):
    """Exception raised when input validation fails."""

    def __init__(
        self, message: str = "Validation failed", details: dict[str, Any] | None = None
    ):
        super().__init__(message, status_code=422, details=details)


class NotFoundError(BaseApplicationError):
    """Exception raised when a requested resource is not found."""

    def __init__(self, resource_type: str, resource_id: Any):
        message = f"{resource_type} with id {resource_id} not found"
        details = {"resource_type": resource_type, "resource_id": str(resource_id)}
        super().__init__(message, status_code=404, details=details)


class ServiceError(BaseApplicationError):
    """Exception raised when a service operation fails."""

    def __init__(
        self, message: str = "Service operation failed", details: dict[str, Any] | None = None
    ):
        super().__init__(message, status_code=500, details=details)


class ConfigurationError(BaseApplicationError):
    """Exception raised when configuration is invalid or missing."""

    def __init__(
        self, message: str = "Invalid configuration", details: dict[str, Any] | None = None
    ):
        super().__init__(message, status_code=500, details=details)
