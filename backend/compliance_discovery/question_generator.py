"""Discovery question generator for NIST 800-53 controls."""

from typing import List
from compliance_discovery.models.control import Control
from compliance_discovery.models.question import DiscoveryQuestion, QuestionType
from compliance_discovery.control_questions import get_control_questions, has_custom_questions


class DiscoveryQuestionGenerator:
    """Generate discovery questions for compliance assessment."""
    
    def generate_questions(self, control: Control) -> List[DiscoveryQuestion]:
        """Generate discovery questions for a control.
        
        Args:
            control: Control object to generate questions for
            
        Returns:
            List of DiscoveryQuestion objects
        """
        questions = []
        aws_guidance = self._get_aws_service_guidance(control)
        
        # Detect if this is a policy/procedure control (typically -1 controls)
        is_policy_control = control.id.lower().endswith('-1')
        
        # 1. Implementation questions - use custom if available, otherwise generic
        if has_custom_questions(control.id):
            custom_questions = get_control_questions(control.id)
            for idx, q in enumerate(custom_questions):
                questions.append(DiscoveryQuestion(
                    id=f"{control.id}-IMPL-{idx+1}",
                    control_id=control.id,
                    question_text=q['question'],
                    question_type=QuestionType.IMPLEMENTATION,
                    family=control.family,
                    aws_service_guidance=aws_guidance if idx == 0 else None
                ))
        else:
            questions.append(DiscoveryQuestion(
                id=f"{control.id}-IMPLEMENTATION",
                control_id=control.id,
                question_text=f"How is {control.id} implemented in your AWS environment? What AWS services, configurations, or custom solutions are in place?",
                question_type=QuestionType.IMPLEMENTATION,
                family=control.family,
                aws_service_guidance=aws_guidance
            ))
        
        # 2. Evidence question - different for policy vs technical controls
        if is_policy_control:
            questions.append(DiscoveryQuestion(
                id=f"{control.id}-EVIDENCE",
                control_id=control.id,
                question_text=f"Where is the {control.id} policy/procedure document stored? When was it last reviewed and approved? Who is responsible for maintaining it?",
                question_type=QuestionType.EVIDENCE,
                family=control.family
            ))
        else:
            questions.append(DiscoveryQuestion(
                id=f"{control.id}-EVIDENCE",
                control_id=control.id,
                question_text=f"What evidence demonstrates {control.id} compliance in AWS? (AWS Config rules, CloudTrail logs, screenshots, policies, etc.) Where is this evidence stored?",
                question_type=QuestionType.EVIDENCE,
                family=control.family
            ))
        
        # 3. Second line defense question - different for policy vs technical
        if is_policy_control:
            questions.append(DiscoveryQuestion(
                id=f"{control.id}-SECOND-LINE",
                control_id=control.id,
                question_text=f"How does your compliance/risk team ensure the {control.id} policy is followed? Are there periodic reviews or assessments?",
                question_type=QuestionType.SECOND_LINE_DEFENSE,
                family=control.family
            ))
        else:
            questions.append(DiscoveryQuestion(
                id=f"{control.id}-SECOND-LINE",
                control_id=control.id,
                question_text=f"How does your compliance/risk team verify {control.id} in AWS? What oversight mechanisms or automated checks are in place?",
                question_type=QuestionType.SECOND_LINE_DEFENSE,
                family=control.family
            ))
        
        # 4. Third line defense question - different for policy vs technical
        if is_policy_control:
            questions.append(DiscoveryQuestion(
                id=f"{control.id}-THIRD-LINE",
                control_id=control.id,
                question_text=f"Is the {control.id} policy document sufficient for internal audit? Does it clearly define roles, responsibilities, and procedures?",
                question_type=QuestionType.THIRD_LINE_DEFENSE,
                family=control.family
            ))
        else:
            questions.append(DiscoveryQuestion(
                id=f"{control.id}-THIRD-LINE",
                control_id=control.id,
                question_text=f"Is your AWS implementation of {control.id} audit-ready? What documentation or evidence gaps exist for internal audit?",
                question_type=QuestionType.THIRD_LINE_DEFENSE,
                family=control.family
            ))
        
        # 5. Audit readiness question - different for policy vs technical
        if is_policy_control:
            questions.append(DiscoveryQuestion(
                id=f"{control.id}-AUDIT-READY",
                control_id=control.id,
                question_text=f"Can you quickly provide the {control.id} policy document and evidence of its approval/review to auditors? Is version history maintained?",
                question_type=QuestionType.AUDIT_READINESS,
                family=control.family,
                aws_service_guidance=aws_guidance
            ))
        else:
            questions.append(DiscoveryQuestion(
                id=f"{control.id}-AUDIT-READY",
                control_id=control.id,
                question_text=f"Can you quickly generate compliance reports for {control.id} from your AWS environment? Is evidence collection automated?",
                question_type=QuestionType.AUDIT_READINESS,
                family=control.family,
                aws_service_guidance=aws_guidance
            ))
        
        return questions
    
    def _get_aws_service_guidance(self, control: Control) -> str:
        """Get AWS service guidance for audit readiness and monitoring.
        
        Args:
            control: Control object
            
        Returns:
            AWS service guidance string
        """
        # General AWS services for compliance monitoring
        services = [
            "CloudWatch (metrics, logs, alarms)",
            "Security Hub (centralized security findings)",
            "AWS Config (configuration compliance)",
            "Systems Manager (operational data)",
            "AWS Audit Manager (continuous audit readiness)"
        ]
        
        # Add family-specific guidance
        family_guidance = {
            "AC": "Consider IAM Access Analyzer for access control monitoring",
            "AU": "Consider CloudTrail for comprehensive audit logging",
            "CM": "Consider AWS Config for configuration management tracking",
            "IA": "Consider IAM and Cognito for identity and authentication",
            "SC": "Consider VPC Flow Logs and GuardDuty for network security",
            "SI": "Consider Inspector and GuardDuty for system integrity monitoring"
        }
        
        guidance = f"Relevant AWS services: {', '.join(services)}"
        
        if control.family in family_guidance:
            guidance += f". {family_guidance[control.family]}"
        
        return guidance
    
    def generate_family_questions(self, family: str, controls: List[Control]) -> List[DiscoveryQuestion]:
        """Generate questions organized by control family.
        
        Args:
            family: Control family identifier (e.g., 'AC', 'AU')
            controls: Controls in the family
            
        Returns:
            List of DiscoveryQuestion objects for the family
        """
        all_questions = []
        
        for control in controls:
            if control.family == family:
                questions = self.generate_questions(control)
                all_questions.extend(questions)
        
        return all_questions
