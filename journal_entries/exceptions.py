"""Separate file for custom exceptions.
This helps to know if the problem is based on an expected exception,
or it is coming from a different source, like a dependency.
"""


class JournalEntryInvalid(Exception):
    """Raised when the Journal Entry is invalid"""
    pass
