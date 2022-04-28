# src/presidio_redcap/surveydefs.py
"""Definitions for relevant Survey scales."""


# Import #
# Standard Libraries #
from dataclasses import dataclass
import re
from typing import List

# Third-Party Packages #

# Local Packages #


@dataclass(frozen=True)
class SurveyItem:
    """Define a Survey item and synonym field names.

    Attributes:
        item: Define name of the survey item.
        synonyms: Regex pattern defining synonyms considered equivalent to the item.
    """

    item: str
    synonyms: re.Pattern

    def is_equivalent(self, reference: str) -> bool:
        """Determine if the reference string is equivalent to the survey item."""
        return self.synonyms.search(reference) is not None


@dataclass(frozen=True)
class SurveyCollection:
    """Define a collection of SurveyItem objects.

    Attributes:
        name: Name of the collection of survey items.
        fields: SurveyItem objects that are naturally grouped under the collection.
    """

    name: str
    fields: List[SurveyItem]

    def find_equivalent(self, reference: str) -> List[str]:
        """Find survey item corresponding to reference string."""
        return [sitem.item for sitem in self.fields if sitem.is_equivalent(reference)]


Survey_Timestamp = SurveyCollection(
    "Timestamp", [SurveyItem("Timestamp", re.compile(r"(date)|(time)"))]
)

Survey_VAS = SurveyCollection(
    "Visual_Analogue_Scale",
    [
        SurveyItem("VAS_Anxiety", re.compile(r"vas_anxiety")),
        SurveyItem("VAS_Depression", re.compile(r"vas_depression")),
        SurveyItem("VAS_Energy", re.compile(r"vas_energy")),
    ],
)

Survey_HAMD6 = SurveyCollection(
    "HAMD6",
    [
        SurveyItem("HAMD6_Q1_DepressedMood", re.compile(r"hamd.*_q1")),
        SurveyItem("HAMD6_Q2_Guilt", re.compile(r"hamd.*_q2")),
        SurveyItem("HAMD6_Q3_WorkInterest", re.compile(r"hamd.*_q3")),
        SurveyItem("HAMD6_Q4_Psychomotor", re.compile(r"hamd.*_q4")),
        SurveyItem("HAMD6_Q5_PsychicAnxiety", re.compile(r"hamd.*_q5")),
        SurveyItem("HAMD6_Q6_SomaticSymptoms", re.compile(r"hamd.*_q6")),
    ],
)

Survey_MADRSS = SurveyCollection(
    "MADRS-S",
    [
        SurveyItem("MADRS-S_Q1_Mood", re.compile("q1")),
        SurveyItem("MADRS-S_Q2_Unease", re.compile("q2")),
        SurveyItem("MADRS-S_Q3_Sleep", re.compile("q3")),
        SurveyItem("MADRS-S_Q4_Appetite", re.compile("q4")),
        SurveyItem("MADRS-S_Q5_Concentration", re.compile("q5")),
        SurveyItem("MADRS-S_Q6_Initiative", re.compile("q6")),
        SurveyItem("MADRS-S_Q7_EmotionalInvolvement", re.compile("q7")),
        SurveyItem("MADRS-S_Q8_Pessimism", re.compile("q8")),
        SurveyItem("MADRS-S_Q9_ZestForLife", re.compile("q9")),
    ],
)
