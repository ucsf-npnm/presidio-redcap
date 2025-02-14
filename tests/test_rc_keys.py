# tests/test_rc_keys.py
"""Test accessibility of Presidio Secrets."""


def test_redcap_subjects(mock_env) -> None:
    """Ensure instantiation of RedcapSubject class."""
    from presidio_redcap import rc_keys

    subject = rc_keys.RedcapSubject(NAME="PRXXX", API_KEYS=["SDSFS", "2GKKS"])
    rc_keys.RedcapSecrets(API_URL="/dummy", SUBJECTS=[subject])


def test_redcap_loader(mock_env) -> None:
    """Ensure JSON can be parsed into RedcapSecrets class."""
    from presidio_redcap import rc_keys

    assert isinstance(rc_keys.redcap, rc_keys.RedcapSecrets)


def test_redcap_get_subject(mock_env) -> None:
    """Ensure RedcapSubject can be retrieved."""
    from presidio_redcap import rc_keys

    #redcap = rc_keys.get_redcap("./assets/presidio_redcap.json")
    rc_subject = rc_keys.redcap.get_subject("S2")
    print("\n {}".format(rc_keys.redcap.subject_ids))
    print("\n {}".format(rc_subject))
    assert isinstance(rc_subject, rc_keys.RedcapSubject)
