"""Data models for blank questionnaire templates."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict
import re

from .control import Control
from .question import DiscoveryQuestion
from .framework_mappings import FrameworkMappings


@dataclass
class TemplateMetadata:
    """Metadata for a blank questionnaire template.
    
    Attributes:
        template_version: Semantic version string (e.g., "1.0.0")
        baseline_version: NIST baseline identifier (e.g., "NIST 800-53 Rev 5 Moderate Baseline")
        export_date: When the template was exported
        total_control_count: Number of controls in the template
        frameworks_included: List of framework names included in mappings
        instructions: How to complete the template
    """
    template_version: str
    baseline_version: str
    export_date: datetime
    total_control_count: int
    frameworks_included: List[str]
    instructions: str
    
    def __post_init__(self):
        """Validate semantic versioning format."""
        if not self._is_valid_semver(self.template_version):
            raise ValueError(
                f"Invalid semantic version format: {self.template_version}. "
                "Expected format: MAJOR.MINOR.PATCH (e.g., '1.0.0')"
            )
    
    @staticmethod
    def _is_valid_semver(version: str) -> bool:
        """Check if version string follows semantic versioning format.
        
        Args:
            version: Version string to validate
            
        Returns:
            True if valid semantic version, False otherwise
        """
        pattern = r'^\d+\.\d+\.\d+$'
        return bool(re.match(pattern, version))


@dataclass
class BlankQuestionnaireTemplate:
    """A blank questionnaire template for offline completion.
    
    Contains all Moderate Baseline controls, discovery questions, framework mappings,
    and AWS hints with empty response fields ready for user input.
    
    Attributes:
        controls: All Moderate Baseline controls
        questions: Discovery questions organized by control_id
        framework_mappings: Framework mappings organized by control_id
        aws_hints: Simple AWS hint strings organized by control_id
        metadata: Template metadata including version and instructions
    """
    controls: List[Control]
    questions: Dict[str, List[DiscoveryQuestion]]
    framework_mappings: Dict[str, FrameworkMappings]
    aws_hints: Dict[str, List[str]]
    metadata: TemplateMetadata
