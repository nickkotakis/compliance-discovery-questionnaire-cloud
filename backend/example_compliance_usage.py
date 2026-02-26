#!/usr/bin/env python3
"""
Example usage of the Compliance Discovery Questionnaire components.

This script demonstrates how to:
1. Parse NIST 800-53 Moderate Baseline controls
2. Generate discovery questions
3. Work with the MCP integration (placeholder)
"""

from compliance_discovery.nist_parser import NIST80053Parser
from compliance_discovery.question_generator import DiscoveryQuestionGenerator
from compliance_discovery.mcp_integration import MCPClient


def main():
    print("=" * 80)
    print("Compliance Discovery Questionnaire - Example Usage")
    print("=" * 80)
    print()
    
    # Step 1: Parse NIST 800-53 Moderate Baseline
    print("Step 1: Parsing NIST 800-53 Moderate Baseline...")
    print("-" * 80)
    
    parser = NIST80053Parser()
    
    try:
        # This will download and parse the OSCAL data from NIST GitHub
        # It may take 10-30 seconds on first run
        controls = parser.get_moderate_baseline_controls()
        
        print(f"✓ Successfully loaded {len(controls)} controls")
        print()
        
        # Show first 3 controls as examples
        print("Example controls:")
        for control in controls[:3]:
            print(f"  • {control.id}: {control.title}")
            print(f"    Family: {control.family}")
            print(f"    Parameters: {len(control.parameters)}")
            print(f"    Enhancements: {len(control.enhancements)}")
            print()
        
    except Exception as e:
        print(f"✗ Error loading controls: {str(e)}")
        print("  Make sure you have internet connectivity to reach NIST GitHub")
        return
    
    # Step 2: Generate discovery questions
    print()
    print("Step 2: Generating discovery questions...")
    print("-" * 80)
    
    generator = DiscoveryQuestionGenerator()
    
    # Generate questions for the first control
    first_control = controls[0]
    questions = generator.generate_questions(first_control)
    
    print(f"✓ Generated {len(questions)} questions for {first_control.id}")
    print()
    print(f"Example questions for {first_control.id} ({first_control.title}):")
    print()
    
    # Show first 3 questions
    for i, question in enumerate(questions[:3], 1):
        print(f"{i}. [{question.question_type.value.upper()}]")
        print(f"   {question.question_text}")
        if question.aws_service_guidance:
            print(f"   AWS Guidance: {question.aws_service_guidance}")
        print()
    
    # Step 3: Count questions by type
    print()
    print("Step 3: Question type distribution...")
    print("-" * 80)
    
    question_types = {}
    for question in questions:
        qtype = question.question_type.value
        question_types[qtype] = question_types.get(qtype, 0) + 1
    
    print(f"Question types for {first_control.id}:")
    for qtype, count in sorted(question_types.items()):
        print(f"  • {qtype}: {count}")
    print()
    
    # Step 4: MCP Integration (placeholder)
    print()
    print("Step 4: MCP Integration (placeholder)...")
    print("-" * 80)
    
    mcp_client = MCPClient()
    
    try:
        mcp_client.connect()
        print("✓ MCP client connected (placeholder)")
        print("  Note: Full MCP integration requires implementing the actual protocol")
        print("  See compliance_discovery/mcp_integration.py for details")
    except Exception as e:
        print(f"✗ MCP connection failed: {str(e)}")
    
    print()
    
    # Step 5: Summary statistics
    print()
    print("Step 5: Summary statistics...")
    print("-" * 80)
    
    # Count controls by family
    families = {}
    for control in controls:
        families[control.family] = families.get(control.family, 0) + 1
    
    print(f"Total controls: {len(controls)}")
    print(f"Control families: {len(families)}")
    print()
    print("Controls by family:")
    for family, count in sorted(families.items()):
        print(f"  • {family}: {count} controls")
    
    print()
    
    # Estimate total questions
    total_questions = len(controls) * len(questions)  # Approximate
    print(f"Estimated total questions: ~{total_questions:,}")
    print()
    
    print("=" * 80)
    print("Example completed successfully!")
    print()
    print("Next steps:")
    print("  1. Start the API server: python compliance_discovery/api_server.py")
    print("  2. Start the frontend: npm run dev")
    print("  3. Navigate to: http://localhost:5173/compliance")
    print("=" * 80)


if __name__ == "__main__":
    main()
