"""Framework relevance mapping for NIST CSF 2.0 subcategories.

Maps CSF functions and subcategories to relevant compliance frameworks,
following the same pattern as framework_mapper.py for NIST 800-53.
"""

from typing import Dict, List, Any

# Framework relevance by CSF function
CSF_FRAMEWORK_RELEVANCE = {
    'gv': {
        'frameworks': ['PCI-DSS', 'HIPAA', 'SOX', 'ISO 27001', 'FFIEC', 'GLBA'],
        'notes': 'Governance controls map to policy and oversight requirements across frameworks'
    },
    'id': {
        'frameworks': ['PCI-DSS', 'HIPAA', 'SOX', 'ISO 27001', 'FFIEC', 'GLBA', 'FedRAMP'],
        'notes': 'Asset management and risk assessment are foundational to most frameworks'
    },
    'pr': {
        'frameworks': ['PCI-DSS', 'HIPAA', 'SOX', 'ISO 27001', 'FFIEC', 'GLBA', 'FedRAMP'],
        'notes': 'Protective safeguards align with technical control requirements across frameworks'
    },
    'de': {
        'frameworks': ['PCI-DSS', 'HIPAA', 'SOX', 'ISO 27001', 'FFIEC', 'FedRAMP'],
        'notes': 'Detection and monitoring requirements are present in most security frameworks'
    },
    'rs': {
        'frameworks': ['PCI-DSS', 'HIPAA', 'SOX', 'ISO 27001', 'FFIEC', 'GLBA'],
        'notes': 'Incident response and breach notification required by most frameworks'
    },
    'rc': {
        'frameworks': ['PCI-DSS', 'HIPAA', 'SOX', 'ISO 27001', 'FFIEC'],
        'notes': 'Recovery and continuity planning required for operational resilience'
    },
}

# Specific subcategory-to-framework mappings for key subcategories
CSF_SPECIFIC_MAPPINGS = {
    'pr.aa-01': {
        'pci_dss': ['8.1', '8.2', '8.3'],
        'hipaa': ['164.308(a)(3)', '164.308(a)(4)', '164.312(d)'],
        'sox': ['ITGC - Access Control'],
        'iso_27001': ['A.9.2'],
    },
    'pr.aa-03': {
        'pci_dss': ['8.3'],
        'hipaa': ['164.312(d)'],
        'sox': ['ITGC - Authentication'],
        'iso_27001': ['A.9.4.2'],
    },
    'pr.aa-05': {
        'pci_dss': ['7.1', '7.2'],
        'hipaa': ['164.308(a)(4)', '164.312(a)(1)'],
        'sox': ['ITGC - Least Privilege'],
        'iso_27001': ['A.9.1', 'A.9.4'],
    },
    'pr.ds-01': {
        'pci_dss': ['3.4', '3.5'],
        'hipaa': ['164.312(a)(2)(iv)', '164.312(e)(2)(ii)'],
        'sox': ['ITGC - Data Protection'],
        'iso_27001': ['A.10.1'],
    },
    'pr.ds-02': {
        'pci_dss': ['4.1', '4.2'],
        'hipaa': ['164.312(e)(1)', '164.312(e)(2)(i)'],
        'sox': ['ITGC - Encryption in Transit'],
        'iso_27001': ['A.13.1', 'A.10.1'],
    },
    'pr.ds-11': {
        'pci_dss': ['9.5', '12.10'],
        'hipaa': ['164.308(a)(7)(ii)(A)', '164.310(d)(2)(iv)'],
        'sox': ['ITGC - Backup'],
        'iso_27001': ['A.12.3'],
    },
    'pr.ps-01': {
        'pci_dss': ['2.2'],
        'hipaa': ['164.312(a)(2)(ii)'],
        'sox': ['ITGC - Configuration Management'],
        'iso_27001': ['A.12.1', 'A.14.2'],
    },
    'pr.ps-02': {
        'pci_dss': ['6.2'],
        'hipaa': ['164.308(a)(5)(ii)(B)'],
        'sox': ['ITGC - Patch Management'],
        'iso_27001': ['A.12.6'],
    },
    'pr.ps-04': {
        'pci_dss': ['10.1', '10.2', '10.3'],
        'hipaa': ['164.312(b)'],
        'sox': ['ITGC - Audit Logging'],
        'iso_27001': ['A.12.4'],
    },
    'pr.ir-01': {
        'pci_dss': ['1.1', '1.2', '1.3'],
        'hipaa': ['164.312(e)(1)'],
        'sox': ['ITGC - Network Security'],
        'iso_27001': ['A.13.1'],
    },
    'de.cm-01': {
        'pci_dss': ['10.6', '11.4'],
        'hipaa': ['164.308(a)(1)(ii)(D)'],
        'sox': ['ITGC - Monitoring'],
        'iso_27001': ['A.12.4'],
    },
    'de.cm-09': {
        'pci_dss': ['5.1', '5.2', '11.4'],
        'hipaa': ['164.308(a)(5)(ii)(B)'],
        'sox': ['ITGC - Malware Detection'],
        'iso_27001': ['A.12.2'],
    },
    'de.ae-02': {
        'pci_dss': ['10.6'],
        'hipaa': ['164.308(a)(1)(ii)(D)'],
        'sox': ['ITGC - Log Review'],
        'iso_27001': ['A.16.1'],
    },
    'rs.ma-01': {
        'pci_dss': ['12.10'],
        'hipaa': ['164.308(a)(6)'],
        'sox': ['ITGC - Incident Response'],
        'iso_27001': ['A.16.1'],
    },
    'id.ra-01': {
        'pci_dss': ['6.1', '11.2'],
        'hipaa': ['164.308(a)(1)(ii)(A)'],
        'sox': ['ITGC - Vulnerability Management'],
        'iso_27001': ['A.12.6'],
    },
    'id.ra-05': {
        'pci_dss': ['12.2'],
        'hipaa': ['164.308(a)(1)(ii)(A)', '164.308(a)(1)(ii)(B)'],
        'sox': ['ITGC - Risk Assessment'],
        'iso_27001': ['A.8.2', 'A.8.3'],
    },
    'rc.rp-02': {
        'pci_dss': ['12.10.4'],
        'hipaa': ['164.308(a)(7)(ii)(B)', '164.308(a)(7)(ii)(D)'],
        'sox': ['ITGC - Disaster Recovery'],
        'iso_27001': ['A.17.1'],
    },
}


def get_csf_framework_relevance(subcategory_id: str) -> Dict[str, Any]:
    """Get framework relevance for a CSF subcategory.

    Args:
        subcategory_id: CSF subcategory ID (e.g., "GV.OC-01" or "PR.DS-01")

    Returns:
        Dictionary with framework relevance information
    """
    normalized = subcategory_id.lower()
    # Extract function code: "gv.oc-01" -> "gv"
    function_code = normalized.split('.')[0] if '.' in normalized else normalized

    function_info = CSF_FRAMEWORK_RELEVANCE.get(function_code, {
        'frameworks': [],
        'notes': 'Framework relevance not mapped'
    })

    specific_mappings = CSF_SPECIFIC_MAPPINGS.get(normalized, {})

    return {
        'control_id': subcategory_id,
        'family': function_code,
        'relevant_frameworks': function_info['frameworks'],
        'notes': function_info['notes'],
        'specific_mappings': specific_mappings,
        'has_specific_mappings': len(specific_mappings) > 0
    }
