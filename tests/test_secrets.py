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


def test_redcap_get_subject(mock_env) -> None:
    """Ensure RedcapSubject can be retrieved."""
    from presidio_redcap import secrets

    rc_subject = secrets.redcap.get_subject('S2')
    print('\n {}'.format(secrets.redcap.subject_ids))
    print('\n {}'.format(rc_subject))
    assert isinstance(rc_subject, secrets.RedcapSubject)
