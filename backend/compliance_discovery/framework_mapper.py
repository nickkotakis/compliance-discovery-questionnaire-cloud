"""Simple framework mapping for NIST 800-53 controls.

This provides basic framework relevance indicators for common compliance frameworks.
Mappings are high-level and indicate which frameworks typically care about each control family.
"""

from typing import List, Dict

# Framework relevance by control family
# This is a simplified mapping - specific control mappings would require detailed analysis
FRAMEWORK_RELEVANCE = {
    # Access Control
    'ac': {
        'frameworks': ['PCI-DSS', 'HIPAA', 'SOX', 'FFIEC', 'GLBA', 'FedRAMP'],
        'notes': 'Access control is fundamental to most compliance frameworks'
    },
    # Awareness and Training
    'at': {
        'frameworks': ['PCI-DSS', 'HIPAA', 'SOX', 'FFIEC', 'GLBA'],
        'notes': 'Security awareness training required by most frameworks'
    },
    # Audit and Accountability
    'au': {
        'frameworks': ['PCI-DSS', 'HIPAA', 'SOX', 'FFIEC', 'GLBA', 'FedRAMP'],
        'notes': 'Audit logging critical for compliance and forensics'
    },
    # Assessment, Authorization, and Monitoring
    'ca': {
        'frameworks': ['PCI-DSS', 'HIPAA', 'SOX', 'FFIEC', 'FedRAMP'],
        'notes': 'Continuous monitoring and assessment required'
    },
    # Configuration Management
    'cm': {
        'frameworks': ['PCI-DSS', 'HIPAA', 'SOX', 'FFIEC', 'FedRAMP'],
        'notes': 'Configuration management and change control'
    },
    # Contingency Planning
    'cp': {
        'frameworks': ['PCI-DSS', 'HIPAA', 'SOX', 'FFIEC', 'GLBA'],
        'notes': 'Business continuity and disaster recovery'
    },
    # Identification and Authentication
    'ia': {
        'frameworks': ['PCI-DSS', 'HIPAA', 'SOX', 'FFIEC', 'GLBA', 'FedRAMP'],
        'notes': 'Identity management and authentication'
    },
    # Incident Response
    'ir': {
        'frameworks': ['PCI-DSS', 'HIPAA', 'SOX', 'FFIEC', 'GLBA'],
        'notes': 'Incident response and breach notification'
    },
    # Maintenance
    'ma': {
        'frameworks': ['PCI-DSS', 'HIPAA', 'FFIEC', 'FedRAMP'],
        'notes': 'System maintenance and patching'
    },
    # Media Protection
    'mp': {
        'frameworks': ['PCI-DSS', 'HIPAA', 'GLBA', 'FedRAMP'],
        'notes': 'Data protection and media sanitization'
    },
    # Physical and Environmental Protection
    'pe': {
        'frameworks': ['PCI-DSS', 'HIPAA', 'SOX', 'FFIEC'],
        'notes': 'Physical security (often AWS responsibility)'
    },
    # Planning
    'pl': {
        'frameworks': ['PCI-DSS', 'HIPAA', 'SOX', 'FFIEC', 'FedRAMP'],
        'notes': 'Security planning and architecture'
    },
    # Program Management
    'pm': {
        'frameworks': ['PCI-DSS', 'HIPAA', 'SOX', 'FFIEC', 'GLBA'],
        'notes': 'Security program management and governance'
    },
    # Personnel Security
    'ps': {
        'frameworks': ['PCI-DSS', 'HIPAA', 'SOX', 'FFIEC', 'GLBA'],
        'notes': 'Background checks and personnel security'
    },
    # PII Processing and Transparency
    'pt': {
        'frameworks': ['HIPAA', 'GLBA', 'GDPR', 'CCPA'],
        'notes': 'Privacy and PII protection requirements'
    },
    # Risk Assessment
    'ra': {
        'frameworks': ['PCI-DSS', 'HIPAA', 'SOX', 'FFIEC', 'GLBA', 'FedRAMP'],
        'notes': 'Risk assessment and vulnerability management'
    },
    # System and Services Acquisition
    'sa': {
        'frameworks': ['PCI-DSS', 'HIPAA', 'SOX', 'FFIEC'],
        'notes': 'Vendor management and secure development'
    },
    # System and Communications Protection
    'sc': {
        'frameworks': ['PCI-DSS', 'HIPAA', 'SOX', 'FFIEC', 'GLBA', 'FedRAMP'],
        'notes': 'Encryption and network security'
    },
    # System and Information Integrity
    'si': {
        'frameworks': ['PCI-DSS', 'HIPAA', 'SOX', 'FFIEC', 'FedRAMP'],
        'notes': 'Malware protection and system integrity'
    },
    # Supply Chain Risk Management
    'sr': {
        'frameworks': ['PCI-DSS', 'FFIEC', 'FedRAMP'],
        'notes': 'Supply chain security and vendor risk'
    },
}

# Specific control mappings for high-priority controls
SPECIFIC_CONTROL_MAPPINGS = {
    'ac-2': {
        'pci_dss': ['8.1', '8.2'],
        'hipaa': ['164.308(a)(3)', '164.308(a)(4)'],
        'sox': ['ITGC - Access Control'],
        'ffiec': ['Access Rights Management'],
        'glba': ['Safeguards Rule - Access Controls']
    },
    'ac-3': {
        'pci_dss': ['7.1', '7.2'],
        'hipaa': ['164.308(a)(4)'],
        'sox': ['ITGC - Access Control'],
        'ffiec': ['Access Rights Management']
    },
    'au-2': {
        'pci_dss': ['10.1', '10.2', '10.3'],
        'hipaa': ['164.312(b)'],
        'sox': ['ITGC - Audit Logging'],
        'ffiec': ['Audit and Accountability']
    },
    'au-6': {
        'pci_dss': ['10.6'],
        'hipaa': ['164.308(a)(1)(ii)(D)'],
        'sox': ['ITGC - Log Review'],
        'ffiec': ['Audit and Accountability']
    },
    'ia-2': {
        'pci_dss': ['8.3'],
        'hipaa': ['164.312(d)'],
        'sox': ['ITGC - Authentication'],
        'ffiec': ['Authentication']
    },
    'ia-5': {
        'pci_dss': ['8.2', '8.3'],
        'hipaa': ['164.308(a)(5)(ii)(D)'],
        'sox': ['ITGC - Password Management'],
        'ffiec': ['Authentication']
    },
    'sc-7': {
        'pci_dss': ['1.1', '1.2', '1.3'],
        'hipaa': ['164.312(e)(1)'],
        'sox': ['ITGC - Network Security'],
        'ffiec': ['Network Security']
    },
    'sc-8': {
        'pci_dss': ['4.1', '4.2'],
        'hipaa': ['164.312(e)(1)', '164.312(e)(2)(i)'],
        'sox': ['ITGC - Encryption'],
        'ffiec': ['Encryption']
    },
    'sc-13': {
        'pci_dss': ['3.4', '3.5', '3.6'],
        'hipaa': ['164.312(a)(2)(iv)', '164.312(e)(2)(ii)'],
        'sox': ['ITGC - Cryptography'],
        'ffiec': ['Encryption']
    },
    'sc-28': {
        'pci_dss': ['3.4'],
        'hipaa': ['164.312(a)(2)(iv)'],
        'sox': ['ITGC - Data Protection'],
        'ffiec': ['Encryption']
    },
    'si-2': {
        'pci_dss': ['6.2'],
        'hipaa': ['164.308(a)(5)(ii)(B)'],
        'sox': ['ITGC - Patch Management'],
        'ffiec': ['Patch Management']
    },
    'si-4': {
        'pci_dss': ['10.6', '11.4'],
        'hipaa': ['164.308(a)(1)(ii)(D)'],
        'sox': ['ITGC - Monitoring'],
        'ffiec': ['Threat Detection']
    },
    'cp-9': {
        'pci_dss': ['9.5', '12.10'],
        'hipaa': ['164.308(a)(7)(ii)(A)'],
        'sox': ['ITGC - Backup'],
        'ffiec': ['Business Continuity']
    },
    'ir-4': {
        'pci_dss': ['12.10'],
        'hipaa': ['164.308(a)(6)'],
        'sox': ['ITGC - Incident Response'],
        'ffiec': ['Incident Response']
    },
}


def get_framework_relevance(control_id: str) -> Dict[str, any]:
    """Get framework relevance for a control.
    
    Args:
        control_id: NIST control ID (e.g., "AC-2" or "ac-2")
        
    Returns:
        Dictionary with framework information
    """
    normalized_id = control_id.lower()
    family = normalized_id.split('-')[0]
    
    # Get family-level relevance
    family_info = FRAMEWORK_RELEVANCE.get(family, {
        'frameworks': [],
        'notes': 'Framework relevance not mapped'
    })
    
    # Get specific control mappings if available
    specific_mappings = SPECIFIC_CONTROL_MAPPINGS.get(normalized_id, {})
    
    return {
        'control_id': control_id,
        'family': family,
        'relevant_frameworks': family_info['frameworks'],
        'notes': family_info['notes'],
        'specific_mappings': specific_mappings,
        'has_specific_mappings': len(specific_mappings) > 0
    }


def get_all_frameworks() -> List[str]:
    """Get list of all frameworks referenced in mappings.
    
    Returns:
        Sorted list of framework names
    """
    frameworks = set()
    for info in FRAMEWORK_RELEVANCE.values():
        frameworks.update(info['frameworks'])
    return sorted(frameworks)
