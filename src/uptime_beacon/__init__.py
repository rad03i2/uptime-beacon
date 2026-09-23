"""Uptime Beacon public API."""
from .core import CheckResult, check_many, check_url, validate_url

__all__ = ["CheckResult", "check_many", "check_url", "validate_url"]
__version__ = "1.0.0"
