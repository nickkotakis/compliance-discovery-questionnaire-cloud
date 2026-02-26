#!/usr/bin/env python3
"""
Populate AWS implementation guide data for additional high-priority controls.
Uses the compass-control-guides MCP server to fetch AWS control mappings.
"""

import json
import sys
from pathlib import Path

# Add the backend directory to the path
sys.path.insert(0, str(Path(__file__).parent))

from compliance_discovery.mcp_integration import search_aws_controls_for_nist

# High-priority controls to populate
CONTROLS_TO_POPULATE = {
    'ac-6': ['least privilege', 'IAM permissions', 'access analyzer'],
    'ac-17': ['remote access', 'VPN', 'bastion', 'session manager'],
    'au-3': ['audit content', 'CloudTrail', 'log details'],
    'au-6': ['audit review', 'log analysis', 'monitoring'],
    'au-9': ['audit protection', 'log security', 'log encryption'],
    'cm-3': ['change control', 'change management', 'approval'],
    'cm-7': ['least functionality', 'disable services', 'minimize'],
    'cm-8': ['inventory', 'asset management', 'resource tracking'],
    'cp-2': ['contingency plan', 'disaster recovery plan', 'DR'],
    'cp-4': ['contingency testing', 'DR testing', 'failover test'],
    'ia-5': ['authenticator', 'credential management', 'password', 'key rotation'],
    'ir-8': ['incident response plan', 'IR plan', 'security incident'],
    'sc-8': ['encryption in transit', 'TLS', 'transmission encryption'],
    'sc-12': ['key management', 'KMS', 'cryptographic keys'],
    'sc-13': ['cryptographic protection', 'encryption standards', 'FIPS'],
    'si-3': ['malware protection', 'antivirus', 'malicious code'],
    'si-4': ['system monitoring', 'intrusion detection', 'GuardDuty'],
}


def main():
    """Populate AWS controls for additional high-priority NIST controls."""
    
    # Load existing data
    data_file = Path(__file__).parent / 'compliance_discovery' / 'aws_controls_mcp_data.json'
    
    if data_file.exists():
        with open(data_file, 'r') as f:
            existing_data = json.load(f)
        print(f"Loaded existing data with {len(existing_data)} controls")
    else:
        existing_data = {}
        print("No existing data found, starting fresh")
    
    # Populate each control
    new_controls = 0
    updated_controls = 0
    
    for nist_control, keywords in CONTROLS_TO_POPULATE.items():
        print(f"\n{'='*60}")
        print(f"Processing {nist_control.upper()}")
        print(f"Keywords: {', '.join(keywords)}")
        print(f"{'='*60}")
        
        # Search for AWS controls
        aws_controls = search_aws_controls_for_nist(nist_control, keywords)
        
        if aws_controls:
            if nist_control in existing_data:
                print(f"  ✓ Updated {nist_control.upper()} with {len(aws_controls)} AWS controls")
                updated_controls += 1
            else:
                print(f"  ✓ Added {nist_control.upper()} with {len(aws_controls)} AWS controls")
                new_controls += 1
            
            existing_data[nist_control] = aws_controls
            
            # Show summary
            services = set()
            for control in aws_controls:
                services.update(control.get('services', []))
            print(f"    AWS Services: {', '.join(sorted(services))}")
        else:
            print(f"  ⚠ No AWS controls found for {nist_control.upper()}")
    
    # Save updated data
    with open(data_file, 'w') as f:
        json.dump(existing_data, f, indent=2)
    
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    print(f"New controls added: {new_controls}")
    print(f"Existing controls updated: {updated_controls}")
    print(f"Total controls in file: {len(existing_data)}")
    print(f"\nData saved to: {data_file}")


if __name__ == '__main__':
    main()
