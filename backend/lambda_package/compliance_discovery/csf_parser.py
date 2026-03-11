"""Parser for NIST Cybersecurity Framework (CSF) 2.0."""

import json
import os
from typing import List, Dict, Any, Optional
from compliance_discovery.models.control import Control, Parameter, ControlEnhancement


class NISTCSFParser:
    """Parser for NIST CSF 2.0 data."""

    def __init__(self):
        """Initialize parser and load CSF data."""
        self.csf_data = self._load_csf_data()

    def _load_csf_data(self) -> dict:
        """Load CSF data from the bundled JSON file."""
        data_file = os.path.join(os.path.dirname(__file__), 'csf_data.json')
        with open(data_file, 'r') as f:
            return json.load(f)

    def get_all_subcategories(self) -> List[Control]:
        """Parse CSF data and return all subcategories as Control objects.

        Maps CSF structure to the existing Control model:
        - Control.id = subcategory ID (e.g., "GV.OC-01")
        - Control.title = subcategory text
        - Control.description = subcategory text (same as title for CSF)
        - Control.family = function code (e.g., "GV")
        - Control.in_moderate_baseline = True (all CSF subcategories are included)
        - Control.enhancements = [] (CSF doesn't have enhancements)
        - Control.parameters = [] (CSF doesn't have parameters)

        Returns:
            List of Control objects representing CSF subcategories
        """
        controls = []
        functions = self.csf_data.get('functions', {})

        for func_code, func_data in functions.items():
            categories = func_data.get('categories', {})
            for cat_code, cat_data in categories.items():
                subcategories = cat_data.get('subcategories', {})
                for sub_id, sub_text in subcategories.items():
                    controls.append(Control(
                        id=sub_id,
                        title=sub_text,
                        description=sub_text,
                        family=func_code,
                        parameters=[],
                        enhancements=[],
                        in_moderate_baseline=True
                    ))

        return controls

    def get_functions(self) -> Dict[str, Dict[str, str]]:
        """Get all CSF functions with their names and descriptions.

        Returns:
            Dict mapping function code to name and description
        """
        result = {}
        for func_code, func_data in self.csf_data.get('functions', {}).items():
            result[func_code] = {
                'name': func_data['name'],
                'description': func_data['description']
            }
        return result

    def get_categories(self, function_code: Optional[str] = None) -> Dict[str, Dict[str, str]]:
        """Get CSF categories, optionally filtered by function.

        Args:
            function_code: Optional function code to filter by (e.g., "GV")

        Returns:
            Dict mapping category code to name and description
        """
        result = {}
        functions = self.csf_data.get('functions', {})

        for func_code, func_data in functions.items():
            if function_code and func_code != function_code.upper():
                continue
            categories = func_data.get('categories', {})
            for cat_code, cat_data in categories.items():
                result[cat_code] = {
                    'name': cat_data['name'],
                    'description': cat_data['description'],
                    'function': func_code
                }
        return result

    def get_function_name(self, function_code: str) -> str:
        """Get the display name for a CSF function code."""
        func_data = self.csf_data.get('functions', {}).get(function_code.upper(), {})
        return func_data.get('name', function_code.upper())

    def get_category_name(self, category_code: str) -> str:
        """Get the display name for a CSF category code."""
        for func_data in self.csf_data.get('functions', {}).values():
            cat_data = func_data.get('categories', {}).get(category_code, {})
            if cat_data:
                return cat_data.get('name', category_code)
        return category_code
