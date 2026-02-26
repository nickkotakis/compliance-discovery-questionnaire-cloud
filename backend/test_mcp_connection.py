#!/usr/bin/env python3
"""Test MCP connection and control mapping."""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from compliance_discovery.mcp_integration import MCPClient, create_aws_hints

def test_mcp_connection():
    """Test MCP connection and control mapping."""
    print("=" * 80)
    print("Testing MCP Connection to compass-control-guides-remote")
    print("=" * 80)
    
    # Initialize client
    client = MCPClient()
    
    # Test connection
    print("\n1. Testing connection...")
    if client.connect():
        print("✓ Connected successfully!")
    else:
        print("✗ Connection failed")
        return
    
    # Test mapping for AC-2
    print("\n2. Testing mapping for AC-2 (Account Management)...")
    aws_controls = client.map_compliance_requirements("AC-2")
    
    if aws_controls:
        print(f"✓ Found {len(aws_controls)} AWS controls for AC-2")
        hints = create_aws_hints(aws_controls)
        print("\nAWS Hints:")
        for hint in hints[:5]:  # Show first 5
            print(hint)
    else:
        print("✗ No AWS controls found for AC-2")
    
    # Test mapping for PE-4
    print("\n3. Testing mapping for PE-4 (Access Control for Transmission)...")
    aws_controls = client.map_compliance_requirements("PE-4")
    
    if aws_controls:
        print(f"✓ Found {len(aws_controls)} AWS controls for PE-4")
        hints = create_aws_hints(aws_controls)
        print("\nAWS Hints:")
        for hint in hints[:5]:
            print(hint)
    else:
        print("✗ No AWS controls found for PE-4")
    
    # Test mapping for AU-2
    print("\n4. Testing mapping for AU-2 (Audit Events)...")
    aws_controls = client.map_compliance_requirements("AU-2")
    
    if aws_controls:
        print(f"✓ Found {len(aws_controls)} AWS controls for AU-2")
        hints = create_aws_hints(aws_controls)
        print("\nAWS Hints:")
        for hint in hints[:5]:
            print(hint)
    else:
        print("✗ No AWS controls found for AU-2")
    
    print("\n" + "=" * 80)
    print("Test complete!")
    print("=" * 80)

if __name__ == "__main__":
    test_mcp_connection()
