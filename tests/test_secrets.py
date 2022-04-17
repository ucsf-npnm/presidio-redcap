# tests/test_secrets.py
"""Test accessibility of Presidio Secrets."""


def test_redcap_subjects(mock_env) -> None:
    """Ensure instantiation of RedcapSubject class."""
    from presidio_redcap import secrets

    subject = secrets.RedcapSubject(NAME="PRXXX", API_KEYS=["SDSFS", "2GKKS"])
    secrets.RedcapSecrets(API_URL="/dummy", SUBJECTS=[subject])


def test_redcap_loader(mock_env) -> None:
    """Ensure JSON can be parsed into RedcapSecrets class."""
    from presidio_redcap import secrets

    assert isinstance(secrets.redcap, secrets.RedcapSecrets)
