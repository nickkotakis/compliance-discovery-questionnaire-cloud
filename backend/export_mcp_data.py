#!/usr/bin/env python3
"""
Export AWS control mappings from MCP to a JSON file.

This script should be run within Kiro environment where MCP tools are available.
It queries the compass-control-guides-remote MCP server and saves the results
to aws_controls_mcp_data.json for use by the Flask backend.

Usage:
    python3 export_mcp_data.py
"""

import json
from datetime import datetime

# This will be populated by Kiro when running the script
MCP_DATA_PLACEHOLDER = """
This script needs to be run within Kiro environment.
Kiro will call the MCP tools and populate this data.
"""

def export_mcp_data():
    """Export MCP data for all NIST controls."""
    
    # List of NIST controls to query
    nist_controls = [
        'ac-1', 'ac-2', 'ac-3', 'ac-4', 'ac-6', 'ac-17',
        'au-1', 'au-2', 'au-3', 'au-4', 'au-6', 'au-9', 'au-11', 'au-12',
        'cm-1', 'cm-2', 'cm-3', 'cm-6', 'cm-7', 'cm-8',
        'cp-1', 'cp-6', 'cp-7', 'cp-9', 'cp-10',
        'ia-1', 'ia-2', 'ia-3', 'ia-4', 'ia-5', 'ia-8',
        'ir-1', 'ir-4', 'ir-5', 'ir-6',
        'pe-1', 'pe-2', 'pe-3', 'pe-4', 'pe-5', 'pe-6',
        'sc-1', 'sc-7', 'sc-8', 'sc-12', 'sc-13', 'sc-28',
        'si-1', 'si-2', 'si-3', 'si-4', 'si-7',
        'ra-1', 'ra-5',
    ]
    
    print("=" * 80)
    print("MCP Data Export Script")
    print("=" * 80)
    print(f"\nThis script will query MCP for {len(nist_controls)} NIST controls")
    print("and save the AWS control mappings to aws_controls_mcp_data.json\n")
    print("NOTE: This script must be run within Kiro environment where MCP tools")
    print("are available. The Flask backend cannot access MCP tools directly.\n")
    print("=" * 80)
    
    # Placeholder for MCP data
    # In actual use, Kiro will call MCP tools and populate this
    mcp_data = {
        'metadata': {
            'export_date': datetime.utcnow().isoformat(),
            'total_controls': len(nist_controls),
            'mcp_server': 'compass-control-guides-remote',
            'note': 'This file contains AWS control mappings from MCP server'
        },
        'controls': {}
    }
    
    print("\nTo complete this export, run the following in Kiro:\n")
    print("For each NIST control, call:")
    print("  mcp_compass_control_guides_remote_search_controls")
    print("  with appropriate keywords\n")
    print("Then save the results to this file.\n")
    
    # Save placeholder
    output_file = 'aws_controls_mcp_data.json'
    with open(output_file, 'w') as f:
        json.dump(mcp_data, f, indent=2)
    
    print(f"✓ Created placeholder file: {output_file}")
    print("\nNext steps:")
    print("1. Run this script within Kiro to populate MCP data")
    print("2. Backend will automatically load this file on startup")
    print("3. AWS Implementation Guide will show rich MCP data")

if __name__ == '__main__':
    export_mcp_data()
