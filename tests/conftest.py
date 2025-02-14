# tests/conftest.py
"""Declare fixtures for mock environment."""

import os

import pytest


@pytest.fixture
def mock_env(monkeypatch):
    """Set mock environment variables for testing configs."""
    monkeypatch.setenv(
        "PRESIDIO_REDCAP", os.path.abspath("./assets/presidio_redcap.json")
    )
