#!/usr/bin/env python3
"""Test evidence questions generation for AU-2"""

from compliance_discovery.models.control import Control
from compliance_discovery.question_generator import DiscoveryQuestionGenerator

# Create AU-2 control
control = Control(
    id='AU-2',
    title='Audit Events',
    description='Determine which events must be audited',
    family='AU'
)

# Generate questions
generator = DiscoveryQuestionGenerator()
questions = generator.generate_questions(control)

print("="*80)
print(f"QUESTIONS FOR {control.id}")
print("="*80)
print()

for i, q in enumerate(questions, 1):
    print(f"{i}. [{q.question_type.value}] {q.id}")
    print(f"   {q.question_text[:100]}...")
    print()

print(f"Total questions: {len(questions)}")
print()
print("Implementation questions:", sum(1 for q in questions if q.question_type.value == 'implementation'))
print("Evidence questions:", sum(1 for q in questions if q.question_type.value == 'evidence'))
print("Second line defense questions:", sum(1 for q in questions if q.question_type.value == 'second_line_defense'))
print("Third line defense questions:", sum(1 for q in questions if q.question_type.value == 'third_line_defense'))
print("Audit readiness questions:", sum(1 for q in questions if q.question_type.value == 'audit_readiness'))
