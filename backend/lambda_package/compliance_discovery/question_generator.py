"""Discovery question generator for NIST 800-53 controls."""

from typing import List, Dict, Any, Optional
from compliance_discovery.models.control import Control
from compliance_discovery.models.question import DiscoveryQuestion, QuestionType
from compliance_discovery.control_questions import get_control_questions, has_custom_questions
from compliance_discovery.csf_custom_questions import get_csf_custom_questions, has_csf_custom_questions, get_csf_evidence_question, has_csf_evidence_question
from compliance_discovery.cmmc_custom_questions import get_cmmc_custom_questions, has_cmmc_custom_questions, get_cmmc_evidence_question, has_cmmc_evidence_question
from compliance_discovery.evidence_questions import get_family_evidence_question, has_family_evidence_question
from compliance_discovery.nist_800_53_evidence import get_nist_evidence_question, has_nist_evidence_question
from compliance_discovery.defense_line_questions import (
    get_nist_second_line_question, get_nist_third_line_question,
    get_csf_second_line_question, get_csf_third_line_question,
)


class DiscoveryQuestionGenerator:
    """Generate discovery questions for compliance assessment."""
    
    def __init__(self):
        """Initialize the question generator."""
        self.aws_controls_cache: Dict[str, List[Dict[str, Any]]] = {}
    
    def set_aws_controls_data(self, aws_controls_data: Dict[str, List[Dict[str, Any]]]):
        """Set AWS controls data for generating AWS-specific questions.
        
        Args:
            aws_controls_data: Dictionary mapping control IDs to AWS control data
        """
        self.aws_controls_cache = aws_controls_data
    
    def generate_questions(self, control: Control, aws_controls: Optional[List[Dict[str, Any]]] = None) -> List[DiscoveryQuestion]:
        """Generate discovery questions for a control.
        
        Args:
            control: Control object to generate questions for
            aws_controls: Optional AWS control data for this control
            
        Returns:
            List of DiscoveryQuestion objects
        """
        questions = []
        
        # Use provided AWS controls or look up from cache
        if aws_controls is None:
            aws_controls = self.aws_controls_cache.get(control.id.lower(), [])
        
        aws_guidance = self._get_aws_service_guidance(control, aws_controls)
        
        # Detect if this is a policy/procedure control (typically -1 controls)
        is_policy_control = control.id.lower().endswith('-1')
        
        # 1. Implementation questions - use custom if available, otherwise generate AWS-specific
        if has_custom_questions(control.id):
            custom_questions = get_control_questions(control.id)
            # Separate implementation questions from evidence questions
            impl_questions = [q for q in custom_questions if q.get('type') != 'evidence']
            evidence_questions = [q for q in custom_questions if q.get('type') == 'evidence']
            
            # Add implementation questions
            for idx, q in enumerate(impl_questions):
                questions.append(DiscoveryQuestion(
                    id=f"{control.id}-IMPL-{idx+1}",
                    control_id=control.id,
                    question_text=q['question'],
                    question_type=QuestionType.IMPLEMENTATION,
                    family=control.family,
                    aws_service_guidance=aws_guidance if idx == 0 else None
                ))
            
            # Add evidence question — priority: control-specific > custom > family-level > auto-generated
            if has_nist_evidence_question(control.id):
                evidence_text = get_nist_evidence_question(control.id)
                questions.append(DiscoveryQuestion(
                    id=f"{control.id}-EVIDENCE",
                    control_id=control.id,
                    question_text=f"What evidence demonstrates {control.id} compliance? {evidence_text}",
                    question_type=QuestionType.EVIDENCE,
                    family=control.family
                ))
            elif evidence_questions:
                ev_text = evidence_questions[0]['question']
                # If the custom evidence is a generic template, prefer family-level
                is_generic = ('Configuration screenshots from' in ev_text
                              or 'CloudTrail logs of relevant API calls. Where are these artifacts stored?' in ev_text)
                if is_generic and has_family_evidence_question(control.id):
                    family_evidence = get_family_evidence_question(control.id, control.title)
                    questions.append(DiscoveryQuestion(
                        id=f"{control.id}-EVIDENCE",
                        control_id=control.id,
                        question_text=family_evidence,
                        question_type=QuestionType.EVIDENCE,
                        family=control.family
                    ))
                elif is_generic and has_nist_evidence_question(control.id):
                    evidence_text = get_nist_evidence_question(control.id)
                    questions.append(DiscoveryQuestion(
                        id=f"{control.id}-EVIDENCE",
                        control_id=control.id,
                        question_text=f"What evidence demonstrates {control.id} compliance? {evidence_text}",
                        question_type=QuestionType.EVIDENCE,
                        family=control.family
                    ))
                else:
                    questions.append(DiscoveryQuestion(
                        id=f"{control.id}-EVIDENCE",
                        control_id=control.id,
                        question_text=ev_text,
                        question_type=QuestionType.EVIDENCE,
                        family=control.family
                    ))
            elif has_family_evidence_question(control.id):
                family_evidence = get_family_evidence_question(control.id, control.title)
                questions.append(DiscoveryQuestion(
                    id=f"{control.id}-EVIDENCE",
                    control_id=control.id,
                    question_text=family_evidence,
                    question_type=QuestionType.EVIDENCE,
                    family=control.family
                ))
            else:
                # Fall back to AWS-specific evidence question
                if is_policy_control:
                    questions.append(DiscoveryQuestion(
                        id=f"{control.id}-EVIDENCE",
                        control_id=control.id,
                        question_text=f"Where is the {control.id} policy/procedure document stored? When was it last reviewed and approved? Who is responsible for maintaining it?",
                        question_type=QuestionType.EVIDENCE,
                        family=control.family
                    ))
                else:
                    evidence_question = self._generate_aws_evidence_question(control, aws_controls)
                    questions.append(DiscoveryQuestion(
                        id=f"{control.id}-EVIDENCE",
                        control_id=control.id,
                        question_text=evidence_question,
                        question_type=QuestionType.EVIDENCE,
                        family=control.family
                    ))
        else:
            # Generate AWS-specific implementation question
            impl_question = self._generate_aws_implementation_question(control, aws_controls)
            questions.append(DiscoveryQuestion(
                id=f"{control.id}-IMPLEMENTATION",
                control_id=control.id,
                question_text=impl_question,
                question_type=QuestionType.IMPLEMENTATION,
                family=control.family,
                aws_service_guidance=aws_guidance
            ))
            
            # Generate AWS-specific evidence question
            if has_nist_evidence_question(control.id):
                evidence_text = get_nist_evidence_question(control.id)
                questions.append(DiscoveryQuestion(
                    id=f"{control.id}-EVIDENCE",
                    control_id=control.id,
                    question_text=f"What evidence demonstrates {control.id} compliance? {evidence_text}",
                    question_type=QuestionType.EVIDENCE,
                    family=control.family
                ))
            elif has_family_evidence_question(control.id):
                family_evidence = get_family_evidence_question(control.id, control.title)
                questions.append(DiscoveryQuestion(
                    id=f"{control.id}-EVIDENCE",
                    control_id=control.id,
                    question_text=family_evidence,
                    question_type=QuestionType.EVIDENCE,
                    family=control.family
                ))
            elif is_policy_control:
                questions.append(DiscoveryQuestion(
                    id=f"{control.id}-EVIDENCE",
                    control_id=control.id,
                    question_text=f"Where is the {control.id} policy/procedure document stored? When was it last reviewed and approved? Who is responsible for maintaining it?",
                    question_type=QuestionType.EVIDENCE,
                    family=control.family
                ))
            else:
                evidence_question = self._generate_aws_evidence_question(control, aws_controls)
                questions.append(DiscoveryQuestion(
                    id=f"{control.id}-EVIDENCE",
                    control_id=control.id,
                    question_text=evidence_question,
                    question_type=QuestionType.EVIDENCE,
                    family=control.family
                ))
        
        # 3. Second line defense question — family-specific risk management oversight
        second_line_q = get_nist_second_line_question(control.id)
        if second_line_q:
            questions.append(DiscoveryQuestion(
                id=f"{control.id}-SECOND-LINE",
                control_id=control.id,
                question_text=second_line_q,
                question_type=QuestionType.SECOND_LINE_DEFENSE,
                family=control.family
            ))
        else:
            # Fallback for families not yet covered
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
        
        # 4. Third line defense question — family-specific internal audit assurance
        third_line_q = get_nist_third_line_question(control.id)
        if third_line_q:
            questions.append(DiscoveryQuestion(
                id=f"{control.id}-THIRD-LINE",
                control_id=control.id,
                question_text=third_line_q,
                question_type=QuestionType.THIRD_LINE_DEFENSE,
                family=control.family
            ))
        else:
            # Fallback for families not yet covered
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
        
        # 5. Audit readiness question
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
    
    def _generate_aws_implementation_question(self, control: Control, aws_controls: List[Dict[str, Any]]) -> str:
        """Generate AWS-specific implementation question.
        
        Args:
            control: Control object
            aws_controls: AWS control data
            
        Returns:
            AWS-specific implementation question
        """
        if not aws_controls:
            return f"How is {control.id} implemented in your AWS environment? What AWS services, configurations, or custom solutions are in place?"
        
        # Extract unique services, config rules, and security hub controls
        services = set()
        config_rules = set()
        security_hub = set()
        control_tower = set()
        
        for ac in aws_controls:
            services.update(ac.get('services', []))
            config_rules.update(ac.get('config_rules', []))
            security_hub.update(ac.get('security_hub_controls', []))
            control_tower.update(ac.get('control_tower_ids', []))
        
        # Build specific question based on available AWS controls
        question_parts = [f"How is {control.id} implemented in your AWS environment?"]
        
        if services:
            service_list = ', '.join(sorted(services)[:3])
            if len(services) > 3:
                service_list += f", and {len(services) - 3} more"
            question_parts.append(f"Are you using {service_list}?")
        
        if config_rules:
            rule_list = ', '.join(sorted(config_rules)[:2])
            if len(config_rules) > 2:
                rule_list += f", and {len(config_rules) - 2} more"
            question_parts.append(f"Have you enabled AWS Config rules like {rule_list}?")
        
        if security_hub:
            hub_list = ', '.join(sorted(security_hub)[:2])
            if len(security_hub) > 2:
                hub_list += f", and {len(security_hub) - 2} more"
            question_parts.append(f"Are you monitoring Security Hub controls {hub_list}?")
        
        if control_tower and not config_rules and not security_hub:
            # Only mention Control Tower if we haven't mentioned Config or Security Hub
            tower_list = ', '.join(sorted(control_tower)[:2])
            if len(control_tower) > 2:
                tower_list += f", and {len(control_tower) - 2} more"
            question_parts.append(f"Are Control Tower guardrails {tower_list} enabled?")
        
        return ' '.join(question_parts)
    
    def _generate_aws_evidence_question(self, control: Control, aws_controls: List[Dict[str, Any]]) -> str:
        """Generate AWS-specific evidence question.
        
        Args:
            control: Control object
            aws_controls: AWS control data
            
        Returns:
            AWS-specific evidence question
        """
        if not aws_controls:
            return f"What evidence demonstrates {control.id} compliance in AWS? (AWS Config rules, CloudTrail logs, screenshots, policies, etc.) Where is this evidence stored?"
        
        # Extract evidence sources
        config_rules = set()
        security_hub = set()
        
        for ac in aws_controls:
            config_rules.update(ac.get('config_rules', []))
            security_hub.update(ac.get('security_hub_controls', []))
        
        # Build specific evidence question
        evidence_sources = []
        
        if config_rules:
            rule_list = ', '.join(sorted(config_rules)[:2])
            if len(config_rules) > 2:
                rule_list += f", and {len(config_rules) - 2} more"
            evidence_sources.append(f"AWS Config compliance reports for {rule_list}")
        
        if security_hub:
            hub_list = ', '.join(sorted(security_hub)[:2])
            if len(security_hub) > 2:
                hub_list += f", and {len(security_hub) - 2} more"
            evidence_sources.append(f"Security Hub findings for {hub_list}")
        
        if evidence_sources:
            evidence_list = '; '.join(evidence_sources)
            return f"What evidence demonstrates {control.id} compliance? Provide: {evidence_list}; Configuration screenshots from relevant AWS services; CloudTrail logs of relevant API calls. Where are these artifacts stored?"
        else:
            return f"What evidence demonstrates {control.id} compliance in AWS? (AWS Config rules, CloudTrail logs, screenshots, policies, etc.) Where is this evidence stored?"
    
    def _get_aws_service_guidance(self, control: Control, aws_controls: List[Dict[str, Any]]) -> str:
        """Get AWS service guidance for audit readiness and monitoring.
        
        Args:
            control: Control object
            aws_controls: AWS control data
            
        Returns:
            AWS service guidance string
        """
        if aws_controls:
            # Extract services from AWS controls data
            services = set()
            for ac in aws_controls:
                services.update(ac.get('services', []))
            
            if services:
                service_list = ', '.join(sorted(services)[:5])
                if len(services) > 5:
                    service_list += f", and {len(services) - 5} more"
                return f"Relevant AWS services for {control.id}: {service_list}"
        
        # Fallback to general AWS services for compliance monitoring
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

    def generate_csf_questions(self, control: Control, aws_controls: Optional[List[Dict[str, Any]]] = None) -> List[DiscoveryQuestion]:
        """Generate discovery questions for a NIST CSF 2.0 subcategory.

        Uses custom implementation questions when available, falling back to
        AWS-specific generated questions. Evidence, second-line, and audit-readiness
        questions are always generated.

        Args:
            control: Control object representing a CSF subcategory
            aws_controls: Optional AWS control data mapped to this subcategory

        Returns:
            List of DiscoveryQuestion objects
        """
        questions = []

        if aws_controls is None:
            aws_controls = []

        aws_guidance = self._get_aws_service_guidance(control, aws_controls) if aws_controls else None

        # 1. Implementation questions — use custom if available
        if has_csf_custom_questions(control.id):
            custom_qs = get_csf_custom_questions(control.id)
            for idx, q in enumerate(custom_qs):
                questions.append(DiscoveryQuestion(
                    id=f"{control.id}-IMPL-{idx+1}",
                    control_id=control.id,
                    question_text=q['question'],
                    question_type=QuestionType.IMPLEMENTATION,
                    family=control.family,
                    aws_service_guidance=aws_guidance if idx == 0 else None
                ))
        else:
            # Fallback: generate AWS-specific implementation question
            if aws_controls:
                services = set()
                config_rules = set()
                security_hub = set()
                for ac in aws_controls:
                    services.update(ac.get('services', []))
                    config_rules.update(ac.get('config_rules', []))
                    security_hub.update(ac.get('security_hub_controls', []))

                parts = [f"How is {control.id} ({control.title}) implemented in your AWS environment?"]
                if services:
                    svc_list = ', '.join(sorted(services)[:3])
                    parts.append(f"Are you using {svc_list}?")
                if config_rules:
                    rule_list = ', '.join(sorted(config_rules)[:2])
                    parts.append(f"Have you enabled AWS Config rules like {rule_list}?")
                if security_hub:
                    hub_list = ', '.join(sorted(security_hub)[:2])
                    parts.append(f"Are you monitoring Security Hub controls {hub_list}?")
                impl_text = ' '.join(parts)
            else:
                impl_text = f"What is the current implementation status of {control.id} ({control.title})? What processes, tools, or AWS services support this outcome?"

            questions.append(DiscoveryQuestion(
                id=f"{control.id}-IMPL-1",
                control_id=control.id,
                question_text=impl_text,
                question_type=QuestionType.IMPLEMENTATION,
                family=control.family,
                aws_service_guidance=aws_guidance
            ))

        # 2. Evidence question — use custom if available, otherwise AWS-specific
        if has_csf_evidence_question(control.id):
            evidence_text = get_csf_evidence_question(control.id)
        elif aws_controls:
            services = set()
            for ac in aws_controls:
                services.update(ac.get('services', []))
            if services:
                service_list = ', '.join(sorted(services)[:4])
                evidence_text = f"What evidence demonstrates achievement of {control.id}? Are you using AWS services such as {service_list} to support this outcome?"
            else:
                evidence_text = f"What evidence demonstrates achievement of {control.id}? What AWS services, configurations, or processes support this outcome?"
        else:
            evidence_text = f"What evidence demonstrates achievement of {control.id}? What processes, tools, or documentation support this outcome?"

        questions.append(DiscoveryQuestion(
            id=f"{control.id}-EVIDENCE",
            control_id=control.id,
            question_text=evidence_text,
            question_type=QuestionType.EVIDENCE,
            family=control.family
        ))

        # 3. Second line defense — function-specific risk management oversight
        second_line_q = get_csf_second_line_question(control.id)
        if second_line_q:
            questions.append(DiscoveryQuestion(
                id=f"{control.id}-SECOND-LINE",
                control_id=control.id,
                question_text=second_line_q,
                question_type=QuestionType.SECOND_LINE_DEFENSE,
                family=control.family
            ))
        else:
            questions.append(DiscoveryQuestion(
                id=f"{control.id}-SECOND-LINE",
                control_id=control.id,
                question_text=f"How does your risk management function review and challenge the controls supporting {control.id}? What independent oversight mechanisms validate that this outcome is being achieved?",
                question_type=QuestionType.SECOND_LINE_DEFENSE,
                family=control.family
            ))

        # 4. Third line defense — function-specific internal audit assurance
        third_line_q = get_csf_third_line_question(control.id)
        if third_line_q:
            questions.append(DiscoveryQuestion(
                id=f"{control.id}-THIRD-LINE",
                control_id=control.id,
                question_text=third_line_q,
                question_type=QuestionType.THIRD_LINE_DEFENSE,
                family=control.family
            ))
        else:
            questions.append(DiscoveryQuestion(
                id=f"{control.id}-THIRD-LINE",
                control_id=control.id,
                question_text=f"Has internal audit independently tested the controls supporting {control.id}? What evidence exists to demonstrate this outcome is achieved and audit-ready?",
                question_type=QuestionType.THIRD_LINE_DEFENSE,
                family=control.family
            ))

        # 5. Gap and improvement
        questions.append(DiscoveryQuestion(
            id=f"{control.id}-GAPS",
            control_id=control.id,
            question_text=f"What gaps or improvement opportunities exist for {control.id}? Are there planned initiatives to enhance this capability?",
            question_type=QuestionType.AUDIT_READINESS,
            family=control.family,
            aws_service_guidance=aws_guidance
        ))

        return questions

    def generate_cmmc_questions(self, control: Control, aws_controls: Optional[List[Dict[str, Any]]] = None) -> List[DiscoveryQuestion]:
        """Generate discovery questions for a CMMC Level 2 practice.

        Uses custom implementation questions when available, falling back to
        AWS-specific generated questions. Evidence questions use custom versions
        when available. Second-line, third-line, and audit-readiness questions
        are always generated.

        Args:
            control: Control object representing a CMMC practice
            aws_controls: Optional AWS control data mapped to this practice

        Returns:
            List of DiscoveryQuestion objects
        """
        questions = []

        if aws_controls is None:
            aws_controls = []

        aws_guidance = self._get_aws_service_guidance(control, aws_controls) if aws_controls else None

        # 1. Implementation questions — use custom if available
        if has_cmmc_custom_questions(control.id):
            custom_qs = get_cmmc_custom_questions(control.id)
            for idx, q in enumerate(custom_qs):
                questions.append(DiscoveryQuestion(
                    id=f"{control.id}-IMPL-{idx+1}",
                    control_id=control.id,
                    question_text=q['question'],
                    question_type=QuestionType.IMPLEMENTATION,
                    family=control.family,
                    aws_service_guidance=aws_guidance if idx == 0 else None
                ))
        else:
            # Fallback: generate AWS-specific implementation question
            if aws_controls:
                services = set()
                config_rules = set()
                security_hub = set()
                for ac in aws_controls:
                    services.update(ac.get('services', []))
                    config_rules.update(ac.get('config_rules', []))
                    security_hub.update(ac.get('security_hub_controls', []))

                parts = [f"How is {control.id} ({control.title}) implemented in your AWS environment?"]
                if services:
                    svc_list = ', '.join(sorted(services)[:3])
                    parts.append(f"Are you using {svc_list}?")
                if config_rules:
                    rule_list = ', '.join(sorted(config_rules)[:2])
                    parts.append(f"Have you enabled AWS Config rules like {rule_list}?")
                if security_hub:
                    hub_list = ', '.join(sorted(security_hub)[:2])
                    parts.append(f"Are you monitoring Security Hub controls {hub_list}?")
                impl_text = ' '.join(parts)
            else:
                impl_text = f"What is the current implementation status of {control.id} ({control.title})? What processes, tools, or controls support this CMMC practice?"

            questions.append(DiscoveryQuestion(
                id=f"{control.id}-IMPL-1",
                control_id=control.id,
                question_text=impl_text,
                question_type=QuestionType.IMPLEMENTATION,
                family=control.family,
                aws_service_guidance=aws_guidance
            ))

        # 2. Evidence question — use custom if available, otherwise AWS-specific
        if has_cmmc_evidence_question(control.id):
            evidence_text = get_cmmc_evidence_question(control.id)
        elif aws_controls:
            services = set()
            for ac in aws_controls:
                services.update(ac.get('services', []))
            if services:
                service_list = ', '.join(sorted(services)[:4])
                evidence_text = f"What evidence demonstrates implementation of {control.id}? Are you using AWS services such as {service_list} to support this practice?"
            else:
                evidence_text = f"What evidence demonstrates implementation of {control.id}? What AWS services, configurations, or processes support this practice?"
        else:
            evidence_text = f"What evidence demonstrates implementation of {control.id}? What documentation, logs, or artifacts can be provided to an assessor?"

        questions.append(DiscoveryQuestion(
            id=f"{control.id}-EVIDENCE",
            control_id=control.id,
            question_text=evidence_text,
            question_type=QuestionType.EVIDENCE,
            family=control.family
        ))

        # 3. Second line defense — risk management oversight
        questions.append(DiscoveryQuestion(
            id=f"{control.id}-SECOND-LINE",
            control_id=control.id,
            question_text=f"How does your risk management function review and validate the controls supporting {control.id}? What independent oversight mechanisms exist to confirm this practice is operating effectively?",
            question_type=QuestionType.SECOND_LINE_DEFENSE,
            family=control.family
        ))

        # 4. Third line defense — internal audit assurance
        questions.append(DiscoveryQuestion(
            id=f"{control.id}-THIRD-LINE",
            control_id=control.id,
            question_text=f"Has internal audit independently tested the controls supporting {control.id}? What evidence exists to demonstrate this practice meets CMMC Level 2 assessment objectives?",
            question_type=QuestionType.THIRD_LINE_DEFENSE,
            family=control.family
        ))

        # 5. Gap and improvement
        questions.append(DiscoveryQuestion(
            id=f"{control.id}-GAPS",
            control_id=control.id,
            question_text=f"What gaps or improvement opportunities exist for {control.id}? Are there planned initiatives to achieve or maintain CMMC Level 2 compliance for this practice?",
            question_type=QuestionType.AUDIT_READINESS,
            family=control.family,
            aws_service_guidance=aws_guidance
        ))

        return questions


