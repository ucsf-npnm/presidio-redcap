# pyright: reportUnknownMemberType=false, reportUnknownVariableType=false, reportUnknownArgumentType=false
# src/presidio_redcap/database.py
"""API interface for Presidio RedCap Database."""

from dataclasses import dataclass

import pandas as pd  # type: ignore
from redcap.project import Project as Project

from .rc_keys import RedcapSecrets as RedcapSecrets
from .rc_keys import redcap as redcap


@dataclass
class RedcapDB:
    """Database containing projects related to collection of Presidio subjects.

    Attributes:
        REDCAP_SECRETS: RedcapSecrets
        projects: Redcap projects associated with each subject.
    """

    REDCAP_SECRETS: RedcapSecrets = redcap

    def __post_init__(self):
        self.connect()

    def connect(self) -> None:
        self.projects: dict[str, list[Project]] = dict(
            [
                (
                    subject_id,
                    [
                        Project(self.REDCAP_SECRETS.API_URL, api_key)
                        for api_key in self.REDCAP_SECRETS.get_subject(
                            subject_id
                        ).API_KEYS
                    ],
                )
                for subject_id in self.REDCAP_SECRETS.subject_ids
            ]
        )

    def agg_subject(self, subject_id: str) -> pd.DataFrame:
        """Construct a DataFrame using all RedCap Project records."""

        df_list: list[pd.DataFrame] = []
        for proj in self.projects[subject_id]:
            rec = proj.export_records(export_survey_fields=True)
            df_rec = pd.DataFrame.from_dict(rec)
            df_rec["project_title"] = proj.export_project_info()[
                "project_title"
            ]
            df_rec["subject_id"] = subject_id
            df_list.append(df_rec)
        return pd.concat(df_list).reset_index(drop=True)

    def agg_field_metadata(self, subject_id: str) -> pd.DataFrame:
        """Construct a DataFrame with metadata corresponding to each survey."""

        df_list: list[pd.DataFrame] = []
        for proj in self.projects[subject_id]:
            df_meta = pd.DataFrame(proj.export_metadata())
            df_meta["project_title"] = proj.export_project_info()[
                "project_title"
            ]
            df_meta["subject_id"] = subject_id
            df_list.append(df_meta)
        return pd.concat(df_list).reset_index(drop=True)
