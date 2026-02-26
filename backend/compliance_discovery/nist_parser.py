"""Parser for NIST 800-53 Rev 5 OSCAL catalog and Moderate Baseline profile."""

import requests
from typing import List, Dict, Any, Optional
from compliance_discovery.models.control import Control, Parameter, ControlEnhancement
from compliance_discovery.exceptions import (
    ProfileRetrievalError,
    CatalogRetrievalError,
    InvalidFormatError,
    ParseError,
    ControlNotFoundError
)


class NIST80053Parser:
    """Parser for NIST 800-53 Rev 5 OSCAL format."""
    
    # Default URLs for NIST OSCAL content
    DEFAULT_PROFILE_URL = "https://raw.githubusercontent.com/usnistgov/oscal-content/main/nist.gov/SP800-53/rev5/json/NIST_SP-800-53_rev5_MODERATE-baseline_profile.json"
    DEFAULT_CATALOG_URL = "https://raw.githubusercontent.com/usnistgov/oscal-content/main/nist.gov/SP800-53/rev5/json/NIST_SP-800-53_rev5_catalog.json"
    
    def __init__(self, timeout: int = 30, max_retries: int = 3):
        """Initialize parser with configuration.
        
        Args:
            timeout: Request timeout in seconds
            max_retries: Maximum number of retry attempts
        """
        self.timeout = timeout
        self.max_retries = max_retries
    
    def retrieve_profile(self, url: str) -> dict:
        """Retrieve OSCAL Moderate Baseline profile from NIST repository.
        
        Args:
            url: GitHub URL to OSCAL Moderate Baseline profile JSON
            
        Returns:
            Raw OSCAL profile as dictionary
            
        Raises:
            ProfileRetrievalError: If profile cannot be retrieved
            InvalidFormatError: If profile is not valid NIST 800-53 Rev 5 Moderate Baseline
        """
        for attempt in range(self.max_retries):
            try:
                response = requests.get(url, timeout=self.timeout)
                response.raise_for_status()
                profile_data = response.json()
                
                # Validate profile format
                self._validate_profile_format(profile_data)
                
                return profile_data
                
            except requests.Timeout:
                if attempt == self.max_retries - 1:
                    raise ProfileRetrievalError(f"Connection timeout after {self.max_retries} attempts")
            except requests.ConnectionError as e:
                if attempt == self.max_retries - 1:
                    raise ProfileRetrievalError(f"Connection failed: {str(e)}")
            except requests.HTTPError as e:
                raise ProfileRetrievalError(f"HTTP error {e.response.status_code}: {e.response.reason}")
            except ValueError as e:
                raise ProfileRetrievalError(f"Invalid JSON response: {str(e)}")
        
        raise ProfileRetrievalError("Failed to retrieve profile after all retries")
    
    def _validate_profile_format(self, profile_data: dict) -> None:
        """Validate that profile data is NIST 800-53 Rev 5 Moderate Baseline.
        
        Args:
            profile_data: Raw OSCAL profile dictionary
            
        Raises:
            InvalidFormatError: If profile format is invalid
        """
        if "profile" not in profile_data:
            raise InvalidFormatError("Missing required field: profile")
        
        profile = profile_data["profile"]
        
        # Check for required metadata
        if "metadata" not in profile:
            raise InvalidFormatError("Missing required field: metadata")
        
        metadata = profile["metadata"]
        title = metadata.get("title", "").lower()
        
        # Validate this is NIST 800-53 Rev 5 Moderate Baseline
        if "nist" not in title or "800-53" not in title or "moderate" not in title:
            raise InvalidFormatError("Expected NIST 800-53 Rev 5 Moderate Baseline profile")
    
    def parse_profile(self, oscal_profile: dict) -> List[str]:
        """Parse OSCAL profile to extract list of included control IDs.
        
        Args:
            oscal_profile: Raw OSCAL profile dictionary
            
        Returns:
            List of control IDs included in the Moderate Baseline
            
        Raises:
            ParseError: If profile structure is invalid
        """
        try:
            profile = oscal_profile["profile"]
            imports = profile.get("imports", [])
            
            control_ids = set()
            
            for import_item in imports:
                include_controls = import_item.get("include-controls", [])
                
                for include in include_controls:
                    # Get with-ids (specific control IDs)
                    with_ids = include.get("with-ids", [])
                    control_ids.update(with_ids)
            
            if not control_ids:
                raise ParseError("No controls specified in baseline profile")
            
            return sorted(list(control_ids))
            
        except KeyError as e:
            raise ParseError(f"Missing required profile field: {str(e)}")
        except Exception as e:
            raise ParseError(f"Error parsing profile structure: {str(e)}")
    
    def retrieve_catalog(self, url: str) -> dict:
        """Retrieve full OSCAL catalog from NIST repository.
        
        Args:
            url: GitHub URL to OSCAL catalog JSON
            
        Returns:
            Raw OSCAL catalog as dictionary
            
        Raises:
            CatalogRetrievalError: If catalog cannot be retrieved
        """
        for attempt in range(self.max_retries):
            try:
                response = requests.get(url, timeout=self.timeout)
                response.raise_for_status()
                catalog_data = response.json()
                
                # Validate catalog format
                self._validate_catalog_format(catalog_data)
                
                return catalog_data
                
            except requests.Timeout:
                if attempt == self.max_retries - 1:
                    raise CatalogRetrievalError(f"Connection timeout after {self.max_retries} attempts")
            except requests.ConnectionError as e:
                if attempt == self.max_retries - 1:
                    raise CatalogRetrievalError(f"Connection failed: {str(e)}")
            except requests.HTTPError as e:
                raise CatalogRetrievalError(f"HTTP error {e.response.status_code}: {e.response.reason}")
            except ValueError as e:
                raise CatalogRetrievalError(f"Invalid JSON response: {str(e)}")
        
        raise CatalogRetrievalError("Failed to retrieve catalog after all retries")
    
    def _validate_catalog_format(self, catalog_data: dict) -> None:
        """Validate that catalog data is NIST 800-53 Rev 5.
        
        Args:
            catalog_data: Raw OSCAL catalog dictionary
            
        Raises:
            InvalidFormatError: If catalog format is invalid
        """
        if "catalog" not in catalog_data:
            raise InvalidFormatError("Missing required field: catalog")
        
        catalog = catalog_data["catalog"]
        
        if "metadata" not in catalog:
            raise InvalidFormatError("Missing required field: metadata")
        
        metadata = catalog["metadata"]
        title = metadata.get("title", "").lower()
        
        if "nist" not in title or "800-53" not in title:
            raise InvalidFormatError("Expected NIST 800-53 Rev 5 catalog")

    
    @staticmethod
    def _normalize_control_id(control_id: str) -> str:
        """Normalize control ID format for comparison.
        
        Converts both formats to the same style:
        - ac-11.1 -> AC-11(1)
        - ac-11(1) -> AC-11(1)
        - AC-11 -> AC-11
        
        Args:
            control_id: Control ID in any format
            
        Returns:
            Normalized control ID
        """
        # Convert to uppercase
        normalized = control_id.upper()
        
        # Convert dot notation to parentheses: ac-11.1 -> AC-11(1)
        if '.' in normalized and '(' not in normalized:
            parts = normalized.split('.')
            if len(parts) == 2:
                normalized = f"{parts[0]}({parts[1]})"
        
        return normalized
    
    def parse_baseline_controls(self, oscal_catalog: dict, baseline_control_ids: List[str]) -> List[Control]:
        """Parse OSCAL catalog to extract only Moderate Baseline controls.
        
        Args:
            oscal_catalog: Raw OSCAL catalog dictionary
            baseline_control_ids: List of control IDs from Moderate Baseline profile
            
        Returns:
            List of parsed Control objects for baseline controls only
            
        Raises:
            ParseError: If catalog structure is invalid
        """
        try:
            catalog = oscal_catalog["catalog"]
            groups = catalog.get("groups", [])
            
            # Normalize baseline control IDs
            normalized_baseline_ids = set(self._normalize_control_id(cid) for cid in baseline_control_ids)
            
            # Build a map of all controls and enhancements in the catalog
            all_controls = {}
            
            for group in groups:
                family = group.get("id", "UNKNOWN")
                controls = group.get("controls", [])
                
                for control_data in controls:
                    control = self._parse_control(control_data, family, normalized_baseline_ids)
                    normalized_id = self._normalize_control_id(control.id)
                    all_controls[normalized_id] = control
                    
                    # Also add enhancements to the map
                    for enhancement in control.enhancements:
                        normalized_enh_id = self._normalize_control_id(enhancement.id)
                        all_controls[normalized_enh_id] = control
            
            # Filter to only baseline controls (base controls, not enhancements)
            baseline_controls = []
            seen_control_ids = set()
            
            for control_id in normalized_baseline_ids:
                if control_id in all_controls:
                    control = all_controls[control_id]
                    # Only add each base control once
                    normalized_control_id = self._normalize_control_id(control.id)
                    if normalized_control_id not in seen_control_ids:
                        baseline_controls.append(control)
                        seen_control_ids.add(normalized_control_id)
            
            return baseline_controls
            
        except KeyError as e:
            raise ParseError(f"Missing required catalog field: {str(e)}")
        except Exception as e:
            raise ParseError(f"Error parsing catalog structure: {str(e)}")
    
    def _parse_control(self, control_data: dict, family: str, baseline_control_ids: set) -> Control:
        """Parse a single control from OSCAL format.
        
        Args:
            control_data: Raw control data from OSCAL
            family: Control family identifier
            baseline_control_ids: Set of normalized baseline control IDs (uppercase)
            
        Returns:
            Parsed Control object
        """
        control_id = control_data.get("id", "")
        title = control_data.get("title", "")
        
        # Extract description from parts
        description = self._extract_description(control_data)
        
        # Parse parameters
        parameters = self._parse_parameters(control_data)
        
        # Parse enhancements
        enhancements = self._parse_enhancements(control_data, control_id, baseline_control_ids)
        
        # Check if this control is in the baseline (case-insensitive)
        in_baseline = control_id.upper() in baseline_control_ids
        
        return Control(
            id=control_id,
            title=title,
            description=description,
            family=family,
            parameters=parameters,
            enhancements=enhancements,
            in_moderate_baseline=in_baseline
        )
    
    def _extract_description(self, control_data: dict) -> str:
        """Extract control description from parts and clean up parameter placeholders.
        
        Args:
            control_data: Raw control data
            
        Returns:
            Control description text with cleaned parameter references
        """
        parts = control_data.get("parts", [])
        description_parts = []
        
        for part in parts:
            if part.get("name") == "statement":
                prose = part.get("prose", "")
                if prose:
                    # Clean up parameter placeholders
                    cleaned_prose = self._clean_parameter_references(prose)
                    description_parts.append(cleaned_prose)
                
                # Check for nested parts
                nested_parts = part.get("parts", [])
                for nested in nested_parts:
                    nested_prose = nested.get("prose", "")
                    if nested_prose:
                        cleaned_nested = self._clean_parameter_references(nested_prose)
                        description_parts.append(cleaned_nested)
        
        return " ".join(description_parts) if description_parts else control_data.get("title", "")
    
    @staticmethod
    def _clean_parameter_references(text: str) -> str:
        """Clean up OSCAL parameter references to be more human-readable.
        
        Removes parameter placeholders entirely since they're shown separately
        in the parameters section.
        
        Args:
            text: Raw text with OSCAL parameter syntax
            
        Returns:
            Cleaned text
        """
        import re
        
        # Remove {{ insert: param, ... }} entirely
        text = re.sub(r'\{\{\s*insert:\s*param,\s*[^}]+\}\}', '', text)
        
        # Remove {{ ... }} entirely
        text = re.sub(r'\{\{[^}]+\}\}', '', text)
        
        # Clean up extra spaces and punctuation
        text = re.sub(r'\s+', ' ', text)  # Multiple spaces to single
        text = re.sub(r'\s+([.,;:])', r'\1', text)  # Space before punctuation
        text = re.sub(r'([.,;:])\s*([.,;:])', r'\1', text)  # Double punctuation
        text = text.strip()
        
        return text
    
    def _parse_parameters(self, control_data: dict) -> List[Parameter]:
        """Parse parameters from control data.
        
        Args:
            control_data: Raw control data
            
        Returns:
            List of Parameter objects
        """
        params = control_data.get("params", [])
        parameters = []
        
        for param in params:
            param_id = param.get("id", "")
            label = param.get("label", "")
            
            # Extract description from select or guidelines
            description = ""
            if "select" in param:
                select = param["select"]
                description = select.get("how-many", "")
            elif "guidelines" in param:
                guidelines = param["guidelines"]
                if isinstance(guidelines, list) and guidelines:
                    description = guidelines[0].get("prose", "")
            
            # Extract constraints
            constraints = []
            if "select" in param:
                select = param["select"]
                choices = select.get("choice", [])
                constraints = choices if isinstance(choices, list) else [choices]
            
            parameters.append(Parameter(
                id=param_id,
                label=label,
                description=description,
                constraints=constraints if constraints else None
            ))
        
        return parameters
    
    def _parse_enhancements(self, control_data: dict, parent_id: str, baseline_control_ids: set) -> List[ControlEnhancement]:
        """Parse control enhancements.
        
        Args:
            control_data: Raw control data
            parent_id: Parent control ID
            baseline_control_ids: Set of normalized baseline control IDs (uppercase)
            
        Returns:
            List of ControlEnhancement objects
        """
        controls = control_data.get("controls", [])
        enhancements = []
        
        for enhancement_data in controls:
            enhancement_id = enhancement_data.get("id", "")
            title = enhancement_data.get("title", "")
            description = self._extract_description(enhancement_data)
            
            # Check if this enhancement is in the baseline (case-insensitive)
            in_baseline = enhancement_id.upper() in baseline_control_ids
            
            enhancements.append(ControlEnhancement(
                id=enhancement_id,
                title=title,
                description=description,
                parent_control_id=parent_id,
                in_moderate_baseline=in_baseline
            ))
        
        return enhancements
    
    def get_moderate_baseline_controls(
        self,
        profile_url: Optional[str] = None,
        catalog_url: Optional[str] = None
    ) -> List[Control]:
        """Convenience method to retrieve and parse Moderate Baseline controls.
        
        This method orchestrates the full workflow:
        1. Retrieve Moderate Baseline profile
        2. Parse profile to get control IDs
        3. Retrieve full catalog
        4. Parse and filter catalog to get only baseline controls
        
        Args:
            profile_url: GitHub URL to OSCAL Moderate Baseline profile JSON (optional)
            catalog_url: GitHub URL to OSCAL catalog JSON (optional)
            
        Returns:
            List of parsed Control objects for Moderate Baseline
            
        Raises:
            ProfileRetrievalError: If profile cannot be retrieved
            CatalogRetrievalError: If catalog cannot be retrieved
            ParseError: If parsing fails
        """
        # Use default URLs if not provided
        profile_url = profile_url or self.DEFAULT_PROFILE_URL
        catalog_url = catalog_url or self.DEFAULT_CATALOG_URL
        
        # Step 1: Retrieve and parse profile
        profile_data = self.retrieve_profile(profile_url)
        baseline_control_ids = self.parse_profile(profile_data)
        
        # Step 2: Retrieve and parse catalog
        catalog_data = self.retrieve_catalog(catalog_url)
        baseline_controls = self.parse_baseline_controls(catalog_data, baseline_control_ids)
        
        return baseline_controls
