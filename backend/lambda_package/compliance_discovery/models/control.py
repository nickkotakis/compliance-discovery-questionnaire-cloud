"""Data models for NIST 800-53 controls."""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Parameter:
    """A parameter within a control.
    
    Attributes:
        id: Parameter identifier
        label: Human-readable label
        description: Parameter description
        constraints: Optional list of constraints or allowed values
    """
    id: str
    label: str
    description: str
    constraints: Optional[List[str]] = None


@dataclass
class ControlEnhancement:
    """An enhancement to a base control.
    
    Attributes:
        id: Enhancement identifier (e.g., "AC-1(1)")
        title: Enhancement title
        description: Enhancement description
        parent_control_id: ID of the parent control
        in_moderate_baseline: Whether this enhancement is in the Moderate Baseline
    """
    id: str
    title: str
    description: str
    parent_control_id: str
    in_moderate_baseline: bool


@dataclass
class Control:
    """A NIST 800-53 security control.
    
    Attributes:
        id: Control identifier (e.g., "AC-1")
        title: Control title
        description: Control description
        family: Control family identifier (e.g., "AC" for Access Control)
        parameters: List of parameters within the control
        enhancements: List of control enhancements
        in_moderate_baseline: Whether this control is in the Moderate Baseline
    """
    id: str
    title: str
    description: str
    family: str
    parameters: List[Parameter] = field(default_factory=list)
    enhancements: List[ControlEnhancement] = field(default_factory=list)
    in_moderate_baseline: bool = False
