"""Parser for CMMC Level 2 (v2.0) practices."""

import json
import os
from typing import List, Dict, Optional
from compliance_discovery.models.control import Control


class CMMCParser:
    """Parser for CMMC Level 2 data."""

    def __init__(self):
        """Initialize parser and load CMMC data."""
        self.cmmc_data = self._load_cmmc_data()

    def _load_cmmc_data(self) -> dict:
        """Load CMMC data from the bundled JSON file."""
        data_file = os.path.join(os.path.dirname(__file__), 'cmmc_data.json')
        with open(data_file, 'r') as f:
            return json.load(f)

    def get_all_practices(self) -> List[Control]:
        """Parse CMMC data and return all practices as Control objects.

        Maps CMMC structure to the existing Control model:
        - Control.id = practice ID (e.g., "AC.L2-3.1.1")
        - Control.title = practice text
        - Control.description = practice text
        - Control.family = domain code (e.g., "AC")
        - Control.in_moderate_baseline = True (all Level 2 practices)
        - Control.enhancements = []
        - Control.parameters = []

        Returns:
            List of Control objects representing CMMC practices
        """
        controls = []
        domains = self.cmmc_data.get('domains', {})

        for domain_code, domain_data in domains.items():
            practices = domain_data.get('practices', {})
            for practice_id, practice_text in practices.items():
                controls.append(Control(
                    id=practice_id,
                    title=practice_text,
                    description=practice_text,
                    family=domain_code,
                    parameters=[],
                    enhancements=[],
                    in_moderate_baseline=True
                ))

        return controls

    def get_domains(self) -> Dict[str, Dict[str, str]]:
        """Get all CMMC domains with their names and descriptions.

        Returns:
            Dict mapping domain code to name and description
        """
        result = {}
        for domain_code, domain_data in self.cmmc_data.get('domains', {}).items():
            result[domain_code] = {
                'name': domain_data['name'],
                'description': domain_data['description']
            }
        return result

    def get_domain_name(self, domain_code: str) -> str:
        """Get the display name for a CMMC domain code."""
        domain_data = self.cmmc_data.get('domains', {}).get(domain_code.upper(), {})
        return domain_data.get('name', domain_code.upper())
