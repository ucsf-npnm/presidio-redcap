# tests/test_secrets.py
"""Test accessibility of Presidio Secrets."""

from presidio_redcap import secrets


def test_redcap_subjects() -> None:
    """Ensure instantiation of RedcapSubject class."""
    subject = secrets.RedcapSubject(NAME="PRXXX", API_KEYS=["SDSFS", "2GKKS"])
    secrets.RedcapSecrets(API_URL="/dummy", SUBJECTS=[subject])


def test_redcap() -> None:
    """Ensure instantiation of RedcapSecrets class."""
    assert isinstance(secrets.redcap, secrets.RedcapSecrets)
