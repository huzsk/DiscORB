"""
Custom exceptions for DiscORBDiscORB.

Keep it small — one base class + a few specific ones.
"""


class DiscORBError(Exception):
    """Base error for all DiscORB errors."""


class NetworkError(DiscORBError):
    """An API / HTTP call failed."""


class SteamNotFoundError(DiscORBError):
    """Steam installation could not be located."""


class DatabaseLoadError(DiscORBError):
    """Failed to load the games database from any source."""
