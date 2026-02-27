"""Data models for discovery sessions."""

from dataclasses import dataclass, field
from datetime import datetime, date
from enum import Enum
from typing import List, Dict, Optional

from .question import DiscoveryQuestion


class SessionStatus(Enum):
    """Status of a discovery session."""
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"


@dataclass
class SessionMetadata:
    """Metadata for a discovery session.
    
    Attributes:
        customer_name: Name of the customer being assessed
        analyst_name: Name of the analyst conducting the session
        session_date: Date of the session
        frameworks: List of frameworks to assess
    """
    customer_name: str
    analyst_name: str
    session_date: date
    frameworks: List[str]


@dataclass
class Response:
    """A response to a discovery question.
    
    Attributes:
        question_id: ID of the question being answered
        answer: The answer text
        notes: Optional additional notes
        timestamp: When the response was recorded
    """
    question_id: str
    answer: str
    notes: Optional[str]
    timestamp: datetime


@dataclass
class Evidence:
    """Evidence documentation for a control.
    
    Attributes:
        id: Unique evidence identifier
        control_id: NIST 800-53 control ID
        description: What the evidence is
        location: Where it's stored/found
        notes: Optional additional notes
        timestamp: When evidence was captured
    """
    id: str
    control_id: str
    description: str
    location: str
    notes: Optional[str]
    timestamp: datetime


@dataclass
class SessionProgress:
    """Progress tracking for a discovery session.
    
    Attributes:
        total_questions: Total number of questions
        answered_questions: Number of answered questions
        coverage_by_family: Coverage percentage by control family
        coverage_by_framework: Coverage percentage by framework
        evidence_count_by_control: Count of evidence entries per control
    """
    total_questions: int
    answered_questions: int
    coverage_by_family: Dict[str, float]
    coverage_by_framework: Dict[str, float]
    evidence_count_by_control: Dict[str, int]


@dataclass
class Session:
    """A compliance discovery session.
    
    Attributes:
        id: Unique session identifier
        metadata: Session metadata
        questions: List of discovery questions
        responses: Responses keyed by question_id
        evidence: Evidence entries keyed by control_id
        created_at: When the session was created
        updated_at: When the session was last updated
        status: Current session status
    """
    id: str
    metadata: SessionMetadata
    questions: List[DiscoveryQuestion]
    responses: Dict[str, Response] = field(default_factory=dict)
    evidence: Dict[str, List[Evidence]] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    status: SessionStatus = SessionStatus.ACTIVE
