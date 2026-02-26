"""Unit tests for template export functionality."""

import pytest
from datetime import datetime
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
    BlankQuestionnaireTemplate,
    TemplateMetadata,
)
from compliance_discovery.export_generator import ExportGenerator
from compliance_discovery.exceptions import TemplateNotReadyError, TemplateGenerationError


class TestTemplateReadiness:
    """Tests for template readiness checks."""
    
    def test_is_ready_with_all_data_loaded(self):
        """Test readiness check returns True when all data is loaded."""
        generator = ExportGenerator()
        
        # Set up test data
        controls = [
            Control(
                id="AC-1",
                title="Policy and Procedures",
                description="Test description",
                family="AC",
                in_moderate_baseline=True,
            )
        ]
        
        questions = {
            "AC-1": [
                DiscoveryQuestion(
                    id="Q-AC-1-1",
                    control_id="AC-1",
                    question_text="Test question?",
                    question_type=QuestionType.IMPLEMENTATION,
                    family="AC",
                )
            ]
        }
        
        mappings = {
            "AC-1": FrameworkMappings(
                control_id="AC-1",
                nist_csf=[
                    NISTCSFMapping(
                        function="IDENTIFY",
                        category="ID.GV",
                        subcategory="ID.GV-1",
                    )
                ],
            )
        }
        
        generator.set_controls(controls)
        generator.set_questions(questions)
        generator.set_framework_mappings(mappings)
        
        assert generator.is_ready_for_template_export() is True
    
    def test_is_ready_with_missing_controls(self):
        """Test readiness check raises error when controls not loaded."""
        generator = ExportGenerator()
        
        questions = {"AC-1": []}
        mappings = {"AC-1": FrameworkMappings(control_id="AC-1")}
        
        generator.set_questions(questions)
        generator.set_framework_mappings(mappings)
        
        with pytest.raises(TemplateNotReadyError) as exc_info:
            generator.is_ready_for_template_export()
        
        assert "controls not fully loaded" in str(exc_info.value).lower()
    
    def test_is_ready_with_missing_questions(self):
        """Test readiness check raises error when questions not generated."""
        generator = ExportGenerator()
        
        controls = [Control(id="AC-1", title="Test", description="Test", family="AC")]
        mappings = {"AC-1": FrameworkMappings(control_id="AC-1")}
        
        generator.set_controls(controls)
        generator.set_framework_mappings(mappings)
        
        with pytest.raises(TemplateNotReadyError) as exc_info:
            generator.is_ready_for_template_export()
        
        assert "questions not generated" in str(exc_info.value).lower()
    
    def test_is_ready_with_missing_mappings(self):
        """Test readiness check raises error when mappings not available."""
        generator = ExportGenerator()
        
        controls = [Control(id="AC-1", title="Test", description="Test", family="AC")]
        questions = {"AC-1": []}
        
        generator.set_controls(controls)
        generator.set_questions(questions)
        
        with pytest.raises(TemplateNotReadyError) as exc_info:
            generator.is_ready_for_template_export()
        
        assert "framework mappings not available" in str(exc_info.value).lower()


class TestTemplateDataPreparation:
    """Tests for template data preparation."""
    
    def test_aws_hints_formatting_with_multiple_mappings(self):
        """Test AWS hints formatting with multiple AWS mappings."""
        generator = ExportGenerator()
        
        # Set up AWS control with multiple managed controls
        aws_control = AWSControl(
            control_id="AWS-CG-0000138",
            title="Test Control",
            description="Test",
            services=["S3"],
            frameworks=["NIST-800-53"],
            managed_controls=ManagedControls(
                config_rules=["S3_BUCKET_VERSIONING_ENABLED"],
                security_hub_controls=["S3.5"],
                control_tower_ids=["CT.S3.PR.1"],
            ),
        )
        
        mappings = {
            "AC-1": FrameworkMappings(
                control_id="AC-1",
                aws=[aws_control],
            )
        }
        
        generator.set_framework_mappings(mappings)
        
        hints = generator._format_aws_hints("AC-1")
        
        assert len(hints) == 1
        assert "Config: S3_BUCKET_VERSIONING_ENABLED" in hints[0]
        assert "Security Hub: S3.5" in hints[0]
        assert "Control Tower: CT.S3.PR.1" in hints[0]
    
    def test_aws_hints_formatting_with_no_mappings(self):
        """Test AWS hints formatting with no AWS mappings."""
        generator = ExportGenerator()
        
        mappings = {
            "AC-1": FrameworkMappings(control_id="AC-1")
        }
        
        generator.set_framework_mappings(mappings)
        
        hints = generator._format_aws_hints("AC-1")
        
        assert hints == []
    
    def test_template_metadata_completeness(self):
        """Test template metadata contains all required fields."""
        generator = ExportGenerator()
        
        controls = [Control(id="AC-1", title="Test", description="Test", family="AC")]
        questions = {"AC-1": []}
        mappings = {"AC-1": FrameworkMappings(control_id="AC-1")}
        
        generator.set_controls(controls)
        generator.set_questions(questions)
        generator.set_framework_mappings(mappings)
        generator.set_mcp_available(True)
        
        metadata = generator._build_template_metadata()
        
        assert metadata.template_version == "1.0.0"
        assert metadata.baseline_version == "NIST 800-53 Rev 5 Moderate Baseline"
        assert isinstance(metadata.export_date, datetime)
        assert metadata.total_control_count == 1
        assert "NIST CSF" in metadata.frameworks_included
        assert "GLBA" in metadata.frameworks_included
        assert "SOX" in metadata.frameworks_included
        assert "FFIEC" in metadata.frameworks_included
        assert "AWS" in metadata.frameworks_included
        assert len(metadata.instructions) > 0
    
    def test_instructions_generation(self):
        """Test instructions generation."""
        generator = ExportGenerator()
        
        instructions = generator._generate_instructions()
        
        assert "How to Complete This Questionnaire" in instructions
        assert "NIST 800-53" in instructions
        assert "Moderate Baseline" in instructions
        assert "Evidence" in instructions
        assert "Framework Mappings" in instructions
        assert "AWS Control Hints" in instructions


class TestTemplateVersionManagement:
    """Tests for template version management."""
    
    def test_get_template_version(self):
        """Test get_template_version returns semantic version."""
        generator = ExportGenerator()
        
        version = generator.get_template_version()
        
        assert version == "1.0.0"
        # Verify semantic versioning format
        parts = version.split(".")
        assert len(parts) == 3
        assert all(part.isdigit() for part in parts)


class TestTemplateMetadataValidation:
    """Tests for template metadata validation."""
    
    def test_valid_semantic_version(self):
        """Test TemplateMetadata accepts valid semantic version."""
        metadata = TemplateMetadata(
            template_version="1.0.0",
            baseline_version="NIST 800-53 Rev 5 Moderate Baseline",
            export_date=datetime.now(),
            total_control_count=325,
            frameworks_included=["NIST CSF", "GLBA", "SOX", "FFIEC"],
            instructions="Test instructions",
        )
        
        assert metadata.template_version == "1.0.0"
    
    def test_invalid_semantic_version(self):
        """Test TemplateMetadata rejects invalid semantic version."""
        with pytest.raises(ValueError) as exc_info:
            TemplateMetadata(
                template_version="1.0",  # Invalid: missing patch version
                baseline_version="NIST 800-53 Rev 5 Moderate Baseline",
                export_date=datetime.now(),
                total_control_count=325,
                frameworks_included=["NIST CSF"],
                instructions="Test",
            )
        
        assert "Invalid semantic version format" in str(exc_info.value)
    
    def test_non_numeric_version(self):
        """Test TemplateMetadata rejects non-numeric version."""
        with pytest.raises(ValueError):
            TemplateMetadata(
                template_version="v1.0.0",  # Invalid: contains 'v' prefix
                baseline_version="NIST 800-53 Rev 5 Moderate Baseline",
                export_date=datetime.now(),
                total_control_count=325,
                frameworks_included=["NIST CSF"],
                instructions="Test",
            )


class TestExcelExport:
    """Tests for Excel template export."""
    
    def test_excel_export_with_all_data_loaded(self):
        """Test Excel export generates valid workbook."""
        generator = ExportGenerator()
        
        # Set up minimal test data
        controls = [
            Control(
                id="AC-1",
                title="Policy and Procedures",
                description="Test description",
                family="AC",
                in_moderate_baseline=True,
            )
        ]
        
        questions = {
            "AC-1": [
                DiscoveryQuestion(
                    id="Q-AC-1-1",
                    control_id="AC-1",
                    question_text="Test question?",
                    question_type=QuestionType.IMPLEMENTATION,
                    family="AC",
                )
            ]
        }
        
        mappings = {
            "AC-1": FrameworkMappings(
                control_id="AC-1",
                nist_csf=[
                    NISTCSFMapping(
                        function="IDENTIFY",
                        category="ID.GV",
                        subcategory="ID.GV-1",
                    )
                ],
            )
        }
        
        generator.set_controls(controls)
        generator.set_questions(questions)
        generator.set_framework_mappings(mappings)
        generator.set_mcp_available(False)
        
        template = generator.prepare_blank_template()
        excel_bytes = generator.export_blank_template_excel(template)
        
        assert isinstance(excel_bytes, bytes)
        assert len(excel_bytes) > 0
        
        # Verify it's a valid Excel file (starts with PK for ZIP format)
        assert excel_bytes[:2] == b'PK'


class TestCSVExport:
    """Tests for CSV template export."""
    
    def test_csv_export_generates_all_files(self):
        """Test CSV export generates all required files."""
        generator = ExportGenerator()
        
        controls = [Control(id="AC-1", title="Test", description="Test", family="AC")]
        questions = {
            "AC-1": [
                DiscoveryQuestion(
                    id="Q-AC-1-1",
                    control_id="AC-1",
                    question_text="Test?",
                    question_type=QuestionType.IMPLEMENTATION,
                    family="AC",
                )
            ]
        }
        mappings = {"AC-1": FrameworkMappings(control_id="AC-1")}
        
        generator.set_controls(controls)
        generator.set_questions(questions)
        generator.set_framework_mappings(mappings)
        
        template = generator.prepare_blank_template()
        csv_files = generator.export_blank_template_csv(template)
        
        assert "controls.csv" in csv_files
        assert "questions.csv" in csv_files
        assert "mappings.csv" in csv_files
        assert "aws_hints.csv" in csv_files
        assert "metadata.csv" in csv_files
        assert "evidence.csv" in csv_files
    
    def test_csv_file_headers_are_correct(self):
        """Test CSV files have correct headers."""
        generator = ExportGenerator()
        
        controls = [Control(id="AC-1", title="Test", description="Test", family="AC")]
        questions = {"AC-1": []}
        mappings = {"AC-1": FrameworkMappings(control_id="AC-1")}
        
        generator.set_controls(controls)
        generator.set_questions(questions)
        generator.set_framework_mappings(mappings)
        
        template = generator.prepare_blank_template()
        csv_files = generator.export_blank_template_csv(template)
        
        # Check controls.csv header
        controls_lines = csv_files["controls.csv"].split("\n")
        assert "control_id,title,description,family" in controls_lines[0]
        
        # Check questions.csv header
        questions_lines = csv_files["questions.csv"].split("\n")
        assert "question_id,control_id,question_text,question_type,response" in questions_lines[0]
        
        # Check metadata.csv header
        metadata_lines = csv_files["metadata.csv"].split("\n")
        assert "key,value" in metadata_lines[0]


class TestJSONYAMLExport:
    """Tests for JSON and YAML template export."""
    
    def test_json_export_generates_valid_json(self):
        """Test JSON export generates valid parseable JSON."""
        import json
        
        generator = ExportGenerator()
        
        controls = [Control(id="AC-1", title="Test", description="Test", family="AC")]
        questions = {"AC-1": []}
        mappings = {"AC-1": FrameworkMappings(control_id="AC-1")}
        
        generator.set_controls(controls)
        generator.set_questions(questions)
        generator.set_framework_mappings(mappings)
        
        template = generator.prepare_blank_template()
        json_str = generator.export_blank_template_json(template)
        
        # Should be valid JSON
        data = json.loads(json_str)
        
        assert "metadata" in data
        assert "controls" in data
        assert "questions" in data
        assert "framework_mappings" in data
        assert "aws_hints" in data
        assert "evidence" in data
    
    def test_yaml_export_generates_valid_yaml(self):
        """Test YAML export generates valid YAML syntax."""
        import yaml
        
        generator = ExportGenerator()
        
        controls = [Control(id="AC-1", title="Test", description="Test", family="AC")]
        questions = {"AC-1": []}
        mappings = {"AC-1": FrameworkMappings(control_id="AC-1")}
        
        generator.set_controls(controls)
        generator.set_questions(questions)
        generator.set_framework_mappings(mappings)
        
        template = generator.prepare_blank_template()
        yaml_str = generator.export_blank_template_yaml(template)
        
        # Should be valid YAML
        data = yaml.safe_load(yaml_str)
        
        assert "metadata" in data
        assert "controls" in data
        assert "questions" in data
        assert "framework_mappings" in data
        assert "aws_hints" in data
        assert "evidence" in data
