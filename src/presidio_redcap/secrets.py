# src/presidio_redcap/secrets.py
"""Verify and validate user-specific secrets for Presidio."""


# Import #
# Standard Libraries #
from dataclasses import dataclass
import json
import os
from typing import List

# Third-Party Packages #
import dacite

# Local Packages #


@dataclass(frozen=True)
class RedcapSubject:
    """Holds pertinent secrets for individual subjects in the Presidio Redcap.

    Attributes:
        NAME: RedCap subject name identifier.
        API_KEYS: API keys used to interface with RedCap projects for subject.
    """

    NAME: str
    API_KEYS: List[str]


@dataclass(frozen=True)
class RedcapSecrets:
    """Holds pertinent secrets for a collection of subjects in the Presidio Redcap.

    Attributes:
        API_URL: Location of the API to access RedCap data for Presidio.
        SUBJECTS: Collection of RedcapSubject pointing to pertinent api keys.
    """

    API_URL: str
    SUBJECTS: List[RedcapSubject]

    @property
    def subject_ids(self) -> List:
        """List of subject names held by the object."""
        return [rc_subject.NAME for rc_subject in self.SUBJECTS]

    def get_subject(self, subject_id: str) -> RedcapSubject:
        """Retrieve RedcapSubject API keys for a desired subject."""
        return self.SUBJECTS[self.subject_ids.index(subject_id)]


ENV_SECRETS = str(os.environ.get("PRESIDIO_SECRETS"))
redcap = dacite.from_dict(
    data_class=RedcapSecrets, data=json.load(open(ENV_SECRETS, "rb"))["REDCAP"]
)
