"""
Unit tests for compliance discovery questionnaire integration.

These tests verify that the core components work correctly.
"""

import pytest
from compliance_discovery.nist_parser import NIST80053Parser
from compliance_discovery.question_generator import DiscoveryQuestionGenerator
from compliance_discovery.mcp_integration import MCPClient, create_aws_hints, AWSControl, ManagedControls
from compliance_discovery.models.control import Control, Parameter, ControlEnhancement
from compliance_discovery.models.question import QuestionType


class TestNISTParser:
    """Tests for NIST 800-53 parser."""
    
    def test_parser_initialization(self):
        """Test parser can be initialized."""
        parser = NIST80053Parser()
        assert parser is not None
        assert parser.timeout == 30
        assert parser.max_retries == 3
    
    def test_parser_has_default_urls(self):
        """Test parser has default NIST URLs."""
        parser = NIST80053Parser()
        assert "nist.gov" in parser.DEFAULT_PROFILE_URL
        assert "MODERATE-baseline" in parser.DEFAULT_PROFILE_URL
        assert "catalog" in parser.DEFAULT_CATALOG_URL


class TestQuestionGenerator:
    """Tests for discovery question generator."""
    
    def test_generator_initialization(self):
        """Test generator can be initialized."""
        generator = DiscoveryQuestionGenerator()
        assert generator is not None
    
    def test_generate_questions_for_control(self):
        """Test question generation for a control."""
        generator = DiscoveryQuestionGenerator()
        
        # Create a test control
        control = Control(
            id="AC-1",
            title="Policy and Procedures",
            description="Test description",
            family="AC",
            parameters=[],
            enhancements=[],
            in_moderate_baseline=True
        )
        
        questions = generator.generate_questions(control)
        
        # Should generate at least 8 questions (9 without parameters)
        assert len(questions) >= 8
        
        # Check question types are present
        question_types = {q.question_type for q in questions}
        assert QuestionType.CURRENT_STATE in question_types
        assert QuestionType.IMPLEMENTATION in question_types
        assert QuestionType.MATURITY in question_types
        assert QuestionType.EVIDENCE in question_types
        assert QuestionType.AUDIT_READINESS in question_types
        assert QuestionType.CONTINUOUS_MONITORING in question_types
    
    def test_generate_questions_with_parameters(self):
        """Test question generation includes parameter questions."""
        generator = DiscoveryQuestionGenerator()
        
        # Create a control with parameters
        control = Control(
            id="AC-2",
            title="Account Management",
            description="Test description",
            family="AC",
            parameters=[
                Parameter(
                    id="ac-2_prm_1",
                    label="Prerequisites",
                    description="Test parameter",
                    constraints=None
                )
            ],
            enhancements=[],
            in_moderate_baseline=True
        )
        
        questions = generator.generate_questions(control)
        
        # Should have parameter question
        param_questions = [q for q in questions if q.question_type == QuestionType.PARAMETER]
        assert len(param_questions) == 1
        assert "ac-2_prm_1" in param_questions[0].id
    
    def test_aws_service_guidance_included(self):
        """Test AWS service guidance is included in audit readiness questions."""
        generator = DiscoveryQuestionGenerator()
        
        control = Control(
            id="AU-1",
            title="Audit Policy",
            description="Test description",
            family="AU",
            parameters=[],
            enhancements=[],
            in_moderate_baseline=True
        )
        
        questions = generator.generate_questions(control)
        
        # Find audit readiness question
        audit_questions = [q for q in questions if q.question_type == QuestionType.AUDIT_READINESS]
        assert len(audit_questions) > 0
        
        # Should have AWS guidance
        assert audit_questions[0].aws_service_guidance is not None
        assert "CloudWatch" in audit_questions[0].aws_service_guidance


class TestMCPIntegration:
    """Tests for MCP integration."""
    
    def test_mcp_client_initialization(self):
        """Test MCP client can be initialized."""
        client = MCPClient()
        assert client is not None
        assert not client.connected
    
    def test_mcp_client_connect(self):
        """Test MCP client connection (placeholder)."""
        client = MCPClient()
        result = client.connect()
        assert result is True
        assert client.connected
    
    def test_create_aws_hints(self):
        """Test AWS hints generation."""
        # Create test AWS controls
        controls = [
            AWSControl(
                control_id="AWS-CG-0001",
                title="S3 Bucket Versioning",
                description="Test description",
                services=["S3"],
                frameworks=["NIST-SP-800-53-r5"],
                managed_controls=ManagedControls(
                    config_rules=["S3_BUCKET_VERSIONING_ENABLED"],
                    security_hub_controls=["S3.5"],
                    control_tower_ids=["CT.S3.PR.1"]
                ),
                nist_mappings=["AC-1"]
            )
        ]
        
        hints = create_aws_hints(controls)
        
        assert len(hints) > 0
        assert "S3 Bucket Versioning" in hints[0]
        assert "Config: S3_BUCKET_VERSIONING_ENABLED" in hints[0]
        assert "Security Hub: S3.5" in hints[0]
        assert "Control Tower: CT.S3.PR.1" in hints[0]


class TestDataModels:
    """Tests for data models."""
    
    def test_control_creation(self):
        """Test Control model can be created."""
        control = Control(
            id="AC-1",
            title="Policy and Procedures",
            description="Test description",
            family="AC",
            parameters=[],
            enhancements=[],
            in_moderate_baseline=True
        )
        
        assert control.id == "AC-1"
        assert control.title == "Policy and Procedures"
        assert control.family == "AC"
        assert control.in_moderate_baseline is True
    
    def test_control_with_enhancements(self):
        """Test Control with enhancements."""
        enhancement = ControlEnhancement(
            id="AC-1(1)",
            title="Test Enhancement",
            description="Test description",
            parent_control_id="AC-1",
            in_moderate_baseline=True
        )
        
        control = Control(
            id="AC-1",
            title="Policy and Procedures",
            description="Test description",
            family="AC",
            parameters=[],
            enhancements=[enhancement],
            in_moderate_baseline=True
        )
        
        assert len(control.enhancements) == 1
        assert control.enhancements[0].id == "AC-1(1)"
        assert control.enhancements[0].parent_control_id == "AC-1"


class TestQuestionTypes:
    """Tests for question type enum."""
    
    def test_all_question_types_exist(self):
        """Test all required question types are defined."""
        required_types = [
            "CURRENT_STATE",
            "IMPLEMENTATION",
            "MATURITY",
            "EVIDENCE",
            "PARAMETER",
            "SECOND_LINE_DEFENSE",
            "THIRD_LINE_DEFENSE",
            "AUDIT_READINESS",
            "CONTINUOUS_MONITORING"
        ]
        
        for type_name in required_types:
            assert hasattr(QuestionType, type_name)
    
    def test_question_type_values(self):
        """Test question type enum values."""
        assert QuestionType.CURRENT_STATE.value == "current_state"
        assert QuestionType.IMPLEMENTATION.value == "implementation"
        assert QuestionType.MATURITY.value == "maturity"
        assert QuestionType.EVIDENCE.value == "evidence"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
