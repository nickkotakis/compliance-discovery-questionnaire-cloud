"""Example usage of the Compliance Discovery Questionnaire Tool.

This script demonstrates how to use the ExportGenerator to create
blank questionnaire templates in various formats.
"""

from datetime import datetime
from compliance_discovery.export_generator import ExportGenerator
from compliance_discovery.models import (
    Control,
    DiscoveryQuestion,
    QuestionType,
    FrameworkMappings,
    NISTCSFMapping,
    GLBAMapping,
    SOXMapping,
    FFIECMapping,
    AWSControl,
    ManagedControls,
)


def create_sample_data():
    """Create sample data for demonstration purposes."""
    
    # Sample controls
    controls = [
        Control(
            id="AC-1",
            title="Policy and Procedures",
            description="Develop, document, and disseminate access control policy and procedures.",
            family="AC",
            in_moderate_baseline=True,
        ),
        Control(
            id="AC-2",
            title="Account Management",
            description="Manage information system accounts, including establishing, activating, modifying, reviewing, disabling, and removing accounts.",
            family="AC",
            in_moderate_baseline=True,
        ),
        Control(
            id="AU-1",
            title="Policy and Procedures",
            description="Develop, document, and disseminate audit and accountability policy and procedures.",
            family="AU",
            in_moderate_baseline=True,
        ),
    ]
    
    # Sample questions
    questions = {
        "AC-1": [
            DiscoveryQuestion(
                id="Q-AC-1-1",
                control_id="AC-1",
                question_text="Describe your organization's current access control policy. How is it documented and communicated to relevant personnel?",
                question_type=QuestionType.CURRENT_STATE,
                family="AC",
            ),
            DiscoveryQuestion(
                id="Q-AC-1-2",
                control_id="AC-1",
                question_text="Is the access control policy currently implemented across all systems? If not, which systems are covered?",
                question_type=QuestionType.IMPLEMENTATION,
                family="AC",
            ),
            DiscoveryQuestion(
                id="Q-AC-1-3",
                control_id="AC-1",
                question_text="What evidence exists to demonstrate compliance with the access control policy?",
                question_type=QuestionType.EVIDENCE,
                family="AC",
            ),
        ],
        "AC-2": [
            DiscoveryQuestion(
                id="Q-AC-2-1",
                control_id="AC-2",
                question_text="Describe your current account management processes. How are accounts created, modified, and removed?",
                question_type=QuestionType.CURRENT_STATE,
                family="AC",
            ),
            DiscoveryQuestion(
                id="Q-AC-2-2",
                control_id="AC-2",
                question_text="How mature is your account management process? Is it ad-hoc, defined, managed, or optimized?",
                question_type=QuestionType.MATURITY,
                family="AC",
            ),
            DiscoveryQuestion(
                id="Q-AC-2-3",
                control_id="AC-2",
                question_text="Consider AWS IAM for centralized account management. How could AWS services help automate and improve your account management processes?",
                question_type=QuestionType.AWS_IMPLEMENTATION,
                family="AC",
                aws_service_guidance="AWS IAM, AWS Organizations, AWS SSO",
            ),
        ],
        "AU-1": [
            DiscoveryQuestion(
                id="Q-AU-1-1",
                control_id="AU-1",
                question_text="Describe your organization's audit and accountability policy. How comprehensive is it?",
                question_type=QuestionType.CURRENT_STATE,
                family="AU",
            ),
            DiscoveryQuestion(
                id="Q-AU-1-2",
                control_id="AU-1",
                question_text="Is automated audit logging and reporting in place? How readily accessible is audit evidence?",
                question_type=QuestionType.AUDIT_READINESS,
                family="AU",
                aws_service_guidance="CloudWatch Logs, CloudTrail, Security Hub, AWS Audit Manager",
            ),
        ],
    }
    
    # Sample framework mappings
    mappings = {
        "AC-1": FrameworkMappings(
            control_id="AC-1",
            nist_csf=[
                NISTCSFMapping(
                    function="IDENTIFY",
                    category="ID.GV",
                    subcategory="ID.GV-1",
                ),
            ],
            glba=[
                GLBAMapping(
                    requirement_type="SAFEGUARDS",
                    requirement_id="GLBA-Safeguards-Access-Control",
                    description="Access control policy and procedures",
                ),
            ],
            sox=[
                SOXMapping(
                    section="404",
                    control_type="ITGC",
                    description="IT general controls for access management",
                ),
            ],
            ffiec=[
                FFIECMapping(
                    domain="Cyber Risk Management",
                    assessment_factor="Access Control",
                    description="Access control policies and procedures",
                ),
            ],
        ),
        "AC-2": FrameworkMappings(
            control_id="AC-2",
            nist_csf=[
                NISTCSFMapping(
                    function="PROTECT",
                    category="PR.AC",
                    subcategory="PR.AC-1",
                ),
            ],
            glba=[
                GLBAMapping(
                    requirement_type="SAFEGUARDS",
                    requirement_id="GLBA-Safeguards-Account-Management",
                    description="Account management procedures",
                ),
            ],
            aws=[
                AWSControl(
                    control_id="AWS-CG-0000138",
                    title="IAM Account Management",
                    description="Implement IAM account management controls",
                    services=["IAM", "Organizations"],
                    frameworks=["NIST-800-53"],
                    managed_controls=ManagedControls(
                        config_rules=["IAM_USER_UNUSED_CREDENTIALS_CHECK"],
                        security_hub_controls=["IAM.1", "IAM.2"],
                        control_tower_ids=["CT.IAM.PR.1"],
                    ),
                    nist_mappings=["AC-2"],
                ),
            ],
        ),
        "AU-1": FrameworkMappings(
            control_id="AU-1",
            nist_csf=[
                NISTCSFMapping(
                    function="DETECT",
                    category="DE.AE",
                    subcategory="DE.AE-1",
                ),
            ],
            sox=[
                SOXMapping(
                    section="404",
                    control_type="ITGC",
                    description="Audit logging and monitoring",
                ),
            ],
        ),
    }
    
    return controls, questions, mappings


def main():
    """Main function to demonstrate template export."""
    
    print("Compliance Discovery Questionnaire Tool - Example Usage")
    print("=" * 60)
    print()
    
    # Create sample data
    print("Creating sample data...")
    controls, questions, mappings = create_sample_data()
    print(f"  - {len(controls)} controls")
    print(f"  - {sum(len(q) for q in questions.values())} questions")
    print(f"  - {len(mappings)} framework mappings")
    print()
    
    # Initialize export generator
    print("Initializing export generator...")
    generator = ExportGenerator()
    generator.set_controls(controls)
    generator.set_questions(questions)
    generator.set_framework_mappings(mappings)
    generator.set_mcp_available(True)  # Simulate MCP availability
    print("  ✓ Export generator ready")
    print()
    
    # Check readiness
    print("Checking template export readiness...")
    try:
        generator.is_ready_for_template_export()
        print("  ✓ All data loaded and ready for export")
    except Exception as e:
        print(f"  ✗ Not ready: {e}")
        return
    print()
    
    # Prepare template
    print("Preparing blank questionnaire template...")
    template = generator.prepare_blank_template()
    print(f"  ✓ Template prepared")
    print(f"    - Version: {template.metadata.template_version}")
    print(f"    - Controls: {template.metadata.total_control_count}")
    print(f"    - Frameworks: {', '.join(template.metadata.frameworks_included)}")
    print()
    
    # Export to Excel
    print("Exporting to Excel...")
    try:
        excel_bytes = generator.export_blank_template_excel(template)
        with open("questionnaire_example.xlsx", "wb") as f:
            f.write(excel_bytes)
        print(f"  ✓ Excel template saved: questionnaire_example.xlsx ({len(excel_bytes)} bytes)")
    except Exception as e:
        print(f"  ✗ Excel export failed: {e}")
    print()
    
    # Export to CSV
    print("Exporting to CSV...")
    try:
        csv_files = generator.export_blank_template_csv(template)
        for filename, content in csv_files.items():
            with open(f"example_{filename}", "w") as f:
                f.write(content)
        print(f"  ✓ CSV templates saved: {len(csv_files)} files")
        for filename in csv_files.keys():
            print(f"    - example_{filename}")
    except Exception as e:
        print(f"  ✗ CSV export failed: {e}")
    print()
    
    # Export to PDF
    print("Exporting to PDF...")
    try:
        pdf_bytes = generator.export_blank_template_pdf(template)
        with open("questionnaire_example.pdf", "wb") as f:
            f.write(pdf_bytes)
        print(f"  ✓ PDF template saved: questionnaire_example.pdf ({len(pdf_bytes)} bytes)")
    except Exception as e:
        print(f"  ✗ PDF export failed: {e}")
    print()
    
    # Export to JSON
    print("Exporting to JSON...")
    try:
        json_str = generator.export_blank_template_json(template)
        with open("questionnaire_example.json", "w") as f:
            f.write(json_str)
        print(f"  ✓ JSON template saved: questionnaire_example.json ({len(json_str)} bytes)")
    except Exception as e:
        print(f"  ✗ JSON export failed: {e}")
    print()
    
    # Export to YAML
    print("Exporting to YAML...")
    try:
        yaml_str = generator.export_blank_template_yaml(template)
        with open("questionnaire_example.yaml", "w") as f:
            f.write(yaml_str)
        print(f"  ✓ YAML template saved: questionnaire_example.yaml ({len(yaml_str)} bytes)")
    except Exception as e:
        print(f"  ✗ YAML export failed: {e}")
    print()
    
    print("=" * 60)
    print("Example completed successfully!")
    print()
    print("Generated files:")
    print("  - questionnaire_example.xlsx")
    print("  - example_controls.csv")
    print("  - example_questions.csv")
    print("  - example_mappings.csv")
    print("  - example_aws_hints.csv")
    print("  - example_metadata.csv")
    print("  - example_evidence.csv")
    print("  - questionnaire_example.pdf")
    print("  - questionnaire_example.json")
    print("  - questionnaire_example.yaml")


if __name__ == "__main__":
    main()
