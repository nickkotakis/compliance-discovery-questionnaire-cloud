#!/usr/bin/env python3
"""Merge customer control guides from JSON files into MCP data."""

import json
from pathlib import Path

def load_json_file(filename):
    """Load JSON file."""
    filepath = Path(__file__).parent / filename
    with open(filepath, 'r') as f:
        return json.load(f)

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
            'source': 'AWS best practices and service documentation',
            'description': 'AWS implementation guides for NIST 800-53 controls',
            'total_controls': len(controls_data)
        },
        'controls': controls_data
    }
    
    with open(mcp_file, 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"Saved {len(controls_data)} controls to {mcp_file}")

def main():
    """Main function."""
    print("Loading existing MCP data...")
    mcp_data = load_existing_mcp_data()
    print(f"Loaded {len(mcp_data)} existing controls")
    
    # Load all customer guide parts
    parts = [
        'customer_guides_part1.json',
        'customer_guides_part2.json', 
        'customer_guides_part3.json',
        'customer_guides_final.json',
        'customer_guides_remaining.json',
        'customer_guides_ca2.json'
    ]
    
    added_count = 0
    for part_file in parts:
        print(f"\nProcessing {part_file}...")
        guides = load_json_file(part_file)
        
        for control_id, guide_data in guides.items():
            if control_id not in mcp_data:
                # Format the guide data to match MCP structure
                mcp_data[control_id] = [{
                    'control_id': f'AWS-CG-{control_id.upper()}',
                    'title': guide_data['title'],
                    'description': guide_data['description'],
                    'services': guide_data['services'],
                    'config_rules': guide_data.get('config_rules', []),
                    'security_hub_controls': guide_data.get('security_hub_controls', []),
                    'control_tower_ids': guide_data.get('control_tower_ids', []),
                    'frameworks': guide_data.get('frameworks', ['NIST-800-53']),
                    'implementation_guidance': guide_data['implementation']
                }]
                added_count += 1
                print(f"  Added: {control_id.upper()} - {guide_data['title']}")
            else:
                print(f"  Skipped: {control_id.upper()} (already exists)")
    
    # Save updated data
    save_mcp_data(mcp_data)
    print(f"\n✓ Successfully added {added_count} new customer control guides")
    print(f"✓ Total controls in MCP data: {len(mcp_data)}")

if __name__ == '__main__':
    main()
