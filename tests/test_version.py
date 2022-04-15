# tests/test_version.py
"""Test the version number."""

import presidio_redcap


def test_has_version():
    """Ensure a version number is set for the package."""
    assert presidio_redcap.__version__ is not None
