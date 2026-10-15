"""
locketlam - Unofficial Python API SDK for Locket Camera.
Author: LAMDev x DaLyMMO.com
"""

from .client import LocketClient
from .device import DeviceProfile
from .session import SessionManager
from .modules.moments import NoteType
from .modules.chat import ReactionEmoji
from .exceptions import (
    LocketError,
    AuthenticationError,
    LocketAPIError,
    StorageUploadError
)

__version__ = "1.0.1"
__all__ = [
    "LocketClient",
    "DeviceProfile",
    "SessionManager",
    "NoteType",
    "ReactionEmoji",
    "LocketError",
    "AuthenticationError",
    "LocketAPIError",
    "StorageUploadError"
]
