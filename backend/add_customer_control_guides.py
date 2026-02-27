#!/usr/bin/env python3
"""Add AWS implementation guides for customer responsibility controls.

This script uses the compass-control-guides MCP server to fetch detailed
implementation guides for NIST 800-53 controls that are customer responsibility.
"""

import sys
import json
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from compliance_discovery.nist_parser import NIST80053Parser
from compliance_discovery.aws_control_mapping import get_aws_responsibility


def load_existing_mcp_data():
    """Load existing MCP data."""
    mcp_file = Path(__file__).parent / 'compliance_discovery' / 'aws_controls_mcp_data.json'
    if mcp_file.exists():
        with open(mcp_file, 'r') as f:
            data = json.load(f)
            return data.get('controls', {})
    return {}


def save_mcp_data(controls_data):
    """Save MCP data to JSON file."""
    mcp_file = Path(__file__).parent / 'compliance_discovery' / 'aws_controls_mcp_data.json'
    
    output = {
        'metadata': {
            'source': 'compass-control-guides MCP server',
            'description': 'AWS implementation guides for NIST 800-53 controls',
            'total_controls': len(controls_data)
        },
        'controls': controls_data
    }
    
    with open(mcp_file, 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"\nSaved {len(controls_data)} controls to {mcp_file}")


def main():
    """Main function to add customer control guides."""
    print("Loading NIST 800-53 controls...")
    parser = NIST80053Parser()
    controls = parser.get_moderate_baseline_controls()
    
    # Load existing data
    mcp_data = load_existing_mcp_data()
    print(f"Loaded {len(mcp_data)} existing control guides")
    
    # Find customer controls without guides
    customer_controls_needed = []
    for control in controls:
        control_id = control.id.lower()
        resp = get_aws_responsibility(control_id)
        
        if resp == 'customer' and control_id not in mcp_data:
            customer_controls_needed.append(control)
    
    print(f"\nFound {len(customer_controls_needed)} customer controls without implementation guides")
    
    if not customer_controls_needed:
        print("All customer controls already have implementation guides!")
        return
    
    print("\nCustomer controls needing guides:")
    for control in customer_controls_needed[:10]:
        print(f"  {control.id}: {control.title[:60]}...")
    if len(customer_controls_needed) > 10:
        print(f"  ... and {len(customer_controls_needed) - 10} more")
    
    print("\n" + "="*80)
    print("MANUAL STEP REQUIRED:")
    print("="*80)
    print("\nTo add implementation guides for these controls, you need to:")
    print("1. Use the compass-control-guides MCP server")
    print("2. Search for each control ID")
    print("3. Get the control details")
    print("4. Add them to the aws_controls_mcp_data.json file")
    print("\nOr run this script with MCP integration enabled.")
    print("="*80)
    
    # Print the list of control IDs for easy copying
    print("\nControl IDs to search:")
    control_ids = [c.id.upper() for c in customer_controls_needed]
    print(", ".join(control_ids[:20]))
    if len(control_ids) > 20:
        print(f"... and {len(control_ids) - 20} more")


if __name__ == '__main__':
    main()
