#!/usr/bin/env python3
"""
Integrate generated evidence questions into control_questions.py
"""

import json
from pathlib import Path

def load_evidence_questions():
    """Load generated evidence questions."""
    with open('evidence_questions_generated.json', 'r') as f:
        return json.load(f)

def read_control_questions():
    """Read the current control_questions.py file."""
    file_path = Path('compliance_discovery/control_questions.py')
    with open(file_path, 'r') as f:
        return f.read()

def integrate_evidence_questions(content: str, evidence_questions: dict) -> str:
    """Integrate evidence questions into control_questions.py content."""
    
    lines = content.split('\n')
    new_lines = []
    i = 0
    
    while i < len(lines):
        line = lines[i]
        new_lines.append(line)
        
        # Check if this line defines a control (e.g., 'ac-2': [)
        for control_id in evidence_questions.keys():
            if f"'{control_id}':" in line and '[' in line:
                # Found a control that needs evidence question
                # Find the closing bracket for this control
                indent_level = len(line) - len(line.lstrip())
                j = i + 1
                
                # Skip to find the last question dict in this control
                last_question_end = i
                while j < len(lines):
                    if lines[j].strip().startswith('},'):
                        last_question_end = j
                    # Check if we've reached the end of this control's list
                    if lines[j].strip() == '],' and len(lines[j]) - len(lines[j].lstrip()) == indent_level:
                        # Insert evidence question before the closing ],
                        evidence_q = evidence_questions[control_id]
                        new_lines.append('        {')
                        new_lines.append("            'type': 'evidence',")
                        new_lines.append(f"            'question': '{evidence_q}',")
                        new_lines.append('        },')
                        break
                    j += 1
                break
        
        i += 1
    
    return '\n'.join(new_lines)

def main():
    print("="*80)
    print("INTEGRATING EVIDENCE QUESTIONS INTO control_questions.py")
    print("="*80)
    print()
    
    # Load evidence questions
    evidence_questions = load_evidence_questions()
    print(f"Loaded {len(evidence_questions)} evidence questions")
    
    # Read current file
    content = read_control_questions()
    print("Read control_questions.py")
    
    # Integrate
    new_content = integrate_evidence_questions(content, evidence_questions)
    
    # Write backup
    backup_path = Path('compliance_discovery/control_questions.py.backup')
    with open(backup_path, 'w') as f:
        f.write(content)
    print(f"Created backup: {backup_path}")
    
    # Write new file
    output_path = Path('compliance_discovery/control_questions.py')
    with open(output_path, 'w') as f:
        f.write(new_content)
    print(f"Updated: {output_path}")
    
    print()
    print("✓ Integration complete!")
    print()
    print("NEXT STEPS:")
    print("1. Review the changes in control_questions.py")
    print("2. Update question_generator.py to check for custom evidence questions")
    print("3. Test with a sample questionnaire")

if __name__ == '__main__':
    main()
