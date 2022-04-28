# src/presidio_redcap/database.py
"""API interface for Presidio RedCap Database."""


# Import #
# Standard Libraries #
from dataclasses import dataclass
from typing import List, Union

# Third-Party Packages #
import numpy as np
import pandas as pd
import redcap as rc

# Local Packages #
from .secrets import RedcapSubject
from .surveydefs import SurveyCollection


@dataclass
class RedcapDB:
    """Database containing projects related to a single Presidio subject.

    Attributes:
        API_URL: URL for accessing the RedCap database.
        API_SUBJECT: RedcapSubject containing the secrets pertaining to the subject.
    """

    API_URL: str
    API_SUBJECT: RedcapSubject

    def connect(self) -> List[Union[rc.Project, None]]:
        """Establish interface to RedCap via API."""
        self.projects = [
            rc.Project(self.API_URL, api_key) for api_key in self.API_SUBJECT.API_KEYS
        ]
        return self.projects

    @property
    def full_dataframe(self) -> pd.DataFrame:
        """Construct a DataFrame using all RedCap Project records."""
        df = pd.concat(
            [pd.DataFrame.from_dict(proj.export_records()) for proj in self.projects]
        ).reset_index(drop=True)
        return df

    @property
    def survey_times(self) -> pd.DataFrame:
        """Retrieve fields with date or time information."""
        date_time_fields = [
            field
            for field in self.full_dataframe.columns
            if (("date" in field.lower()) or ("time" in field.lower()))
        ]
        time_frame = (
            self.full_dataframe[date_time_fields]
            .apply(lambda x: pd.to_datetime(x, errors="coerce"))
            .T.max(axis=0)
        )
        time_frame.name = "Timestamp"
        return time_frame

    def get_survey_as_dataframe(
        self,
        survey: SurveyCollection,
        index_by_survey_times: bool = True,
        empty_to_nan: bool = True,
        cast_as_float: bool = True,
    ) -> pd.DataFrame:
        """Extract DataFrames for corresponding to a SurveyCollection object."""
        # Map the current fields onto the fields defined by SurveyCollection
        all_fields = self.full_dataframe.columns
        field_mapper = dict(
            (field, survey.find_equivalent(field)[0])
            for field in all_fields
            if len(survey.find_equivalent(field)) > 0
        )

        # Select and rename fields based on SurveyCollection
        survey_dataframe = self.full_dataframe[field_mapper.keys()].rename(
            columns=field_mapper
        )

        # Use NaNs instead of blanks to placehold missing data
        if empty_to_nan:
            empty_str = survey_dataframe == ""
            survey_dataframe[empty_str] = np.nan

        # Define whether survey values should be considered numerical and
        # cast as floats
        if cast_as_float:
            survey_dataframe = survey_dataframe.astype(float)

        # Aggregate renamed fields that share root field from SurveyCollection
        survey_dataframe = pd.concat(
            [
                pd.DataFrame(
                    np.nanmax(
                        survey_dataframe[col].values.reshape(len(survey_dataframe), -1),
                        axis=1,
                    ),
                    columns=[col],
                )
                for col in survey_dataframe.columns.unique()
            ],
            axis=1,
        )

        # Re-index the rows using Timestamp information
        if index_by_survey_times:
            survey_dataframe.index = self.survey_times

        # Organize the fields based on major name of SurveyCollection
        cols_multiidx = pd.MultiIndex.from_tuples(
            [(survey.name, field) for field in survey_dataframe.columns],
            names=["Survey_Type", "field"],
        )
        survey_dataframe.columns = cols_multiidx

        return survey_dataframe
