#!/usr/bin/env python3
"""
Improve evidence questions for NIST 800-53 controls.
Generates specific, AWS-focused evidence questions based on AWS controls data.
"""

import json
from pathlib import Path
from typing import List, Dict

def load_aws_controls_data() -> Dict:
    """Load AWS controls data from JSON file."""
    data_file = Path(__file__).parent / 'compliance_discovery' / 'aws_controls_mcp_data.json'
    with open(data_file, 'r') as f:
        return json.load(f)

def generate_evidence_question(control_id: str, aws_controls: List[Dict]) -> str:
    """Generate specific evidence question from AWS controls data."""
    
    if not aws_controls:
        # Fallback for controls without AWS data
        return None
    
    # Collect evidence types
    config_rules = []
    security_hub = []
    control_tower = []
    services = set()
    
    for control in aws_controls:
        config_rules.extend(control.get('config_rules', []))
        security_hub.extend(control.get('security_hub_controls', []))
        control_tower.extend(control.get('control_tower_ids', []))
        services.update(control.get('services', []))
    
    # Build evidence items list
    evidence_items = []
    
    # Add Config rules (limit to 3 most relevant)
    if config_rules:
        rules_str = ', '.join(config_rules[:3])
        if len(config_rules) > 3:
            rules_str += f" (and {len(config_rules) - 3} more)"
        evidence_items.append(f"AWS Config compliance reports for {rules_str}")
    
    # Add Security Hub controls (limit to 3)
    if security_hub:
        controls_str = ', '.join(security_hub[:3])
        if len(security_hub) > 3:
            controls_str += f" (and {len(security_hub) - 3} more)"
        evidence_items.append(f"Security Hub findings for {controls_str}")
    
    # Add Control Tower controls (limit to 2)
    if control_tower:
        ct_str = ', '.join(control_tower[:2])
        if len(control_tower) > 2:
            ct_str += f" (and {len(control_tower) - 2} more)"
        evidence_items.append(f"Control Tower compliance status for {ct_str}")
    
    # Add service-specific evidence
    if services:
        services_str = ', '.join(sorted(services)[:3])
        if len(services) > 3:
            services_str += f" (and {len(services) - 3} more services)"
        evidence_items.append(f"Configuration screenshots from {services_str}")
    
    # Always add CloudTrail
    evidence_items.append("CloudTrail logs of relevant API calls")
    
    # Build question
    question = f"What evidence demonstrates {control_id.upper()} compliance in AWS? Provide: "
    question += "; ".join(evidence_items)
    question += ". Where are these artifacts stored?"
    
    return question


def generate_all_evidence_questions() -> Dict[str, str]:
    """Generate evidence questions for all controls with AWS data."""
    
    aws_data = load_aws_controls_data()
    evidence_questions = {}
    
    print("Generating evidence questions for controls with AWS data...\n")
    
    for control_id, aws_controls in aws_data['controls'].items():
        question = generate_evidence_question(control_id, aws_controls)
        if question:
            evidence_questions[control_id] = question
            print(f"✓ {control_id.upper()}: Generated ({len(aws_controls)} AWS controls)")
        else:
            print(f"⚠ {control_id.upper()}: Skipped (no AWS data)")
    
    return evidence_questions


def generate_python_code(evidence_questions: Dict[str, str]) -> str:
    """Generate Python code to add to control_questions.py."""
    
    code_lines = []
    code_lines.append("# Evidence questions for controls with AWS implementation data")
    code_lines.append("# Add these to the respective control entries in CONTROL_QUESTIONS")
    code_lines.append("")
    
    for control_id, question in sorted(evidence_questions.items()):
        code_lines.append(f"# {control_id.upper()}")
        code_lines.append("{")
        code_lines.append("    'type': 'evidence',")
        code_lines.append(f"    'question': '{question}',")
        code_lines.append("},")
        code_lines.append("")
    
    return "\n".join(code_lines)


def save_evidence_questions(evidence_questions: Dict[str, str]):
    """Save evidence questions to a JSON file for reference."""
    
    output_file = Path(__file__).parent / 'evidence_questions_generated.json'
    
    with open(output_file, 'w') as f:
        json.dump(evidence_questions, f, indent=2)
    
    print(f"\n✓ Saved evidence questions to: {output_file}")


def save_python_code(code: str):
    """Save Python code to a file for easy copying."""
    
    output_file = Path(__file__).parent / 'evidence_questions_code.py'
    
    with open(output_file, 'w') as f:
        f.write(code)
    
    print(f"✓ Saved Python code to: {output_file}")


def print_sample_questions(evidence_questions: Dict[str, str], count: int = 5):
    """Print sample evidence questions for review."""
    
    print(f"\n{'='*80}")
    print(f"SAMPLE EVIDENCE QUESTIONS (first {count})")
    print(f"{'='*80}\n")
    
    for control_id in sorted(evidence_questions.keys())[:count]:
        print(f"{control_id.upper()}:")
        print(f"  {evidence_questions[control_id]}")
        print()


def main():
    """Main execution function."""
    
    print("="*80)
    print("EVIDENCE QUESTIONS IMPROVEMENT SCRIPT")
    print("="*80)
    print()
    
    # Generate evidence questions
    evidence_questions = generate_all_evidence_questions()
    
    # Print summary
    print(f"\n{'='*80}")
    print("SUMMARY")
    print(f"{'='*80}")
    print(f"Total evidence questions generated: {len(evidence_questions)}")
    print()
    
    # Print samples
    print_sample_questions(evidence_questions)
    
    # Generate Python code
    python_code = generate_python_code(evidence_questions)
    
    # Save outputs
    save_evidence_questions(evidence_questions)
    save_python_code(python_code)
    
    print(f"\n{'='*80}")
    print("NEXT STEPS")
    print(f"{'='*80}")
    print("1. Review evidence_questions_generated.json")
    print("2. Review evidence_questions_code.py")
    print("3. Manually add evidence questions to control_questions.py")
    print("4. Update question_generator.py to check for custom evidence questions")
    print("5. Test with sample questionnaire")
    print()
    print("See EVIDENCE_QUESTIONS_TASK.md for detailed instructions.")
    print()


if __name__ == '__main__':
    main()
