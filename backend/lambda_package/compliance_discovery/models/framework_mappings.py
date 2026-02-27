"""Data models for framework mappings."""

from dataclasses import dataclass, field
from typing import List


@dataclass
class NISTCSFMapping:
    """Mapping to NIST Cybersecurity Framework.
    
    Attributes:
        function: CSF function (IDENTIFY, PROTECT, DETECT, RESPOND, RECOVER)
        category: CSF category
        subcategory: CSF subcategory
    """
    function: str
    category: str
    subcategory: str


@dataclass
class GLBAMapping:
    """Mapping to Gramm-Leach-Bliley Act requirements.
    
    Attributes:
        requirement_type: Type of requirement (SAFEGUARDS, PRIVACY)
        requirement_id: Requirement identifier
        description: Requirement description
    """
    requirement_type: str
    requirement_id: str
    description: str


@dataclass
class SOXMapping:
    """Mapping to Sarbanes-Oxley Act requirements.
    
    Attributes:
        section: SOX section (302, 404)
        control_type: Type of control (ITGC, APPLICATION)
        description: Control description
    """
    section: str
    control_type: str
    description: str


@dataclass
class FFIECMapping:
    """Mapping to FFIEC requirements.
    
    Attributes:
        domain: FFIEC domain (e.g., "Cyber Risk Management")
        assessment_factor: Assessment factor
        description: Factor description
    """
    domain: str
    assessment_factor: str
    description: str


@dataclass
class ManagedControls:
    """AWS managed control identifiers.
    
    Attributes:
        config_rules: AWS Config rule names
        security_hub_controls: Security Hub control IDs
        control_tower_ids: Control Tower control IDs
    """
    config_rules: List[str] = field(default_factory=list)
    security_hub_controls: List[str] = field(default_factory=list)
    control_tower_ids: List[str] = field(default_factory=list)


@dataclass
class AWSControl:
    """An AWS control from the compass-control-guides MCP server.
    
    Attributes:
        control_id: AWS Control Guide ID (e.g., "AWS-CG-0000138")
        title: Control title
        description: Control description
        services: AWS services involved
        frameworks: Frameworks this control maps to
        managed_controls: Managed control identifiers
        nist_mappings: NIST 800-53 control IDs this maps to
    """
    control_id: str
    title: str
    description: str
    services: List[str]
    frameworks: List[str]
    managed_controls: ManagedControls
    nist_mappings: List[str] = field(default_factory=list)


@dataclass
class AWSControlMapping:
    """Mapping between NIST 800-53 and AWS controls.
    
    Attributes:
        nist_control_id: NIST 800-53 control ID
        aws_controls: AWS controls that implement this NIST control
    """
    nist_control_id: str
    aws_controls: List[AWSControl]


@dataclass
class FrameworkMappings:
    """All framework mappings for a control.
    
    Attributes:
        control_id: NIST 800-53 control ID
        nist_csf: NIST CSF mappings
        glba: GLBA mappings
        sox: SOX mappings
        ffiec: FFIEC mappings
        aws: AWS control mappings
    """
    control_id: str
    nist_csf: List[NISTCSFMapping] = field(default_factory=list)
    glba: List[GLBAMapping] = field(default_factory=list)
    sox: List[SOXMapping] = field(default_factory=list)
    ffiec: List[FFIECMapping] = field(default_factory=list)
    aws: List[AWSControl] = field(default_factory=list)
