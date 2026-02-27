"""Data models for discovery questions."""

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class QuestionType(Enum):
    """Types of discovery questions."""
    CURRENT_STATE = "current_state"
    IMPLEMENTATION = "implementation"
    MATURITY = "maturity"
    EVIDENCE = "evidence"
    GAP_ANALYSIS = "gap_analysis"
    REMEDIATION = "remediation"
    AWS_IMPLEMENTATION = "aws_implementation"
    PARAMETER = "parameter"
    SECOND_LINE_DEFENSE = "second_line_defense"
    THIRD_LINE_DEFENSE = "third_line_defense"
    AUDIT_READINESS = "audit_readiness"
    CONTINUOUS_MONITORING = "continuous_monitoring"


@dataclass
class DiscoveryQuestion:
    """A discovery question for assessing control implementation.
    
    Attributes:
        id: Unique question identifier
        control_id: ID of the control this question assesses
        question_text: The question text
        question_type: Type of question
        family: Control family identifier
        aws_service_guidance: Optional AWS service recommendations for audit readiness
    """
    id: str
    control_id: str
    question_text: str
    question_type: QuestionType
    family: str
    aws_service_guidance: Optional[str] = None
