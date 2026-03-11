"""Custom second line (risk management) and third line (audit) defense questions.

Second Line (Risk Management):
- Challenges and reviews first-line operations
- Monitors risk and control effectiveness
- Validates that controls operate as designed
- Provides independent oversight of control owners

Third Line (Internal Audit):
- Independent assurance over first and second line
- Tests control design and operating effectiveness
- Evaluates evidence sufficiency for external audit
- Identifies gaps in documentation and audit trails
"""

from typing import Optional, Dict, List

# ---------------------------------------------------------------------------
# NIST 800-53 — Second Line (Risk Management) Questions by Family
# ---------------------------------------------------------------------------
NIST_SECOND_LINE: Dict[str, Dict[str, str]] = {
    # Access Control
    "AC": {
        "policy": (
            "How does your risk management function review the access control policy "
            "for adequacy? Do they challenge whether the policy addresses current threats, "
            "cloud-specific risks, and least-privilege principles across your AWS environment?"
        ),
        "technical": (
            "How does your risk management team independently validate that access controls "
            "are operating effectively? Do they review IAM access analyzer findings, "
            "monitor for privilege escalation patterns, or challenge whether role-based "
            "access models remain appropriate as the environment changes?"
        ),
    },
    # Awareness and Training
    "AT": {
        "policy": (
            "How does your risk management function assess whether security awareness "
            "and training programs address the actual risks your organization faces? "
            "Do they review training completion rates, phishing simulation results, "
            "and whether training content reflects current cloud security threats?"
        ),
        "technical": (
            "How does your risk management team evaluate the effectiveness of security "
            "training beyond completion metrics? Do they correlate training gaps with "
            "security incidents, review whether role-based training covers AWS-specific "
            "responsibilities, or challenge the frequency of refresher training?"
        ),
    },
    # Audit and Accountability
    "AU": {
        "policy": (
            "How does your risk management function review the audit and accountability "
            "policy to confirm it addresses log retention requirements, monitoring scope, "
            "and incident correlation needs across your AWS accounts and regions?"
        ),
        "technical": (
            "How does your risk management team independently verify that audit logging "
            "is functioning as intended? Do they validate CloudTrail coverage across all "
            "accounts and regions, review log integrity controls, challenge whether "
            "alerting thresholds catch real threats, or test that log correlation "
            "actually detects suspicious activity patterns?"
        ),
    },
    # Security Assessment and Authorization
    "CA": {
        "policy": (
            "How does your risk management function review the security assessment "
            "and authorization policy? Do they challenge whether assessment frequency, "
            "scope, and methodology are sufficient to identify control weaknesses "
            "before they become audit findings?"
        ),
        "technical": (
            "How does your risk management team oversee the security assessment process? "
            "Do they review assessment results for completeness, challenge remediation "
            "timelines for identified weaknesses, validate that Plan of Action and "
            "Milestones (POA&Ms) are tracked to closure, or verify that continuous "
            "monitoring tools like Security Hub provide adequate coverage?"
        ),
    },
    # Configuration Management
    "CM": {
        "policy": (
            "How does your risk management function review configuration management "
            "policies to confirm they address baseline configurations, change control "
            "processes, and drift detection for your AWS infrastructure?"
        ),
        "technical": (
            "How does your risk management team validate that configuration baselines "
            "are maintained? Do they review AWS Config compliance dashboards, challenge "
            "whether approved configuration changes follow the change management process, "
            "monitor for unauthorized configuration drift, or verify that hardening "
            "standards are applied consistently across accounts?"
        ),
    },
    # Contingency Planning
    "CP": {
        "policy": (
            "How does your risk management function review contingency planning policies "
            "to confirm they address recovery time objectives, backup requirements, "
            "and failover procedures for AWS-hosted workloads?"
        ),
        "technical": (
            "How does your risk management team validate that contingency plans actually "
            "work? Do they review disaster recovery test results, challenge whether "
            "backup restoration has been tested recently, verify that failover "
            "procedures for multi-region or multi-AZ architectures are documented "
            "and rehearsed, or assess whether RTO/RPO targets are realistic?"
        ),
    },
    # Identification and Authentication
    "IA": {
        "policy": (
            "How does your risk management function review identification and "
            "authentication policies to confirm they address MFA requirements, "
            "password complexity, service account management, and federation "
            "standards for AWS access?"
        ),
        "technical": (
            "How does your risk management team verify that authentication controls "
            "are operating effectively? Do they review MFA adoption rates across "
            "IAM users and roles, challenge whether service accounts use temporary "
            "credentials, monitor for authentication anomalies, or validate that "
            "federation and SSO configurations follow organizational standards?"
        ),
    },
    # Incident Response
    "IR": {
        "policy": (
            "How does your risk management function review the incident response "
            "policy to confirm it addresses cloud-specific incident scenarios, "
            "escalation paths, communication protocols, and coordination with "
            "AWS support during security events?"
        ),
        "technical": (
            "How does your risk management team evaluate incident response readiness? "
            "Do they review post-incident reports for lessons learned, challenge "
            "whether detection-to-response times meet targets, validate that "
            "GuardDuty and Security Hub findings are triaged promptly, or assess "
            "whether tabletop exercises cover realistic AWS breach scenarios?"
        ),
    },
    # Maintenance
    "MA": {
        "policy": (
            "How does your risk management function review maintenance policies "
            "to confirm they address patching cadences, maintenance windows, "
            "and change approval processes for AWS-hosted systems?"
        ),
        "technical": (
            "How does your risk management team verify that maintenance activities "
            "are performed on schedule? Do they review patching compliance rates, "
            "challenge whether critical vulnerabilities are remediated within SLA, "
            "or validate that maintenance activities are logged and authorized?"
        ),
    },
    # Media Protection
    "MP": {
        "policy": (
            "How does your risk management function review media protection policies "
            "to confirm they address data classification, encryption requirements, "
            "and secure disposal procedures for data stored in AWS?"
        ),
        "technical": (
            "How does your risk management team verify that media protection controls "
            "are effective? Do they review S3 bucket encryption status, challenge "
            "whether EBS volume encryption is enforced, validate that data lifecycle "
            "policies properly dispose of sensitive data, or monitor for unencrypted "
            "data stores?"
        ),
    },
    # Physical and Environmental Protection
    "PE": {
        "policy": (
            "How does your risk management function confirm that physical and "
            "environmental protection responsibilities are clearly delineated between "
            "AWS (data center) and your organization (on-premises, endpoints)? "
            "Do they review AWS SOC reports and compliance artifacts for this coverage?"
        ),
        "technical": (
            "How does your risk management team validate physical security coverage? "
            "For AWS-managed infrastructure, do they review AWS Artifact reports? "
            "For customer-managed components (offices, endpoints), do they challenge "
            "whether physical access controls and environmental protections are "
            "tested and documented?"
        ),
    },
    # Planning
    "PL": {
        "policy": (
            "How does your risk management function review security planning documents "
            "to confirm they reflect the current AWS architecture, threat landscape, "
            "and organizational risk appetite? Do they challenge whether plans are "
            "updated when significant changes occur?"
        ),
        "technical": (
            "How does your risk management team validate that security plans are "
            "actionable and current? Do they review whether planned controls are "
            "actually implemented, challenge gaps between documented architecture "
            "and actual AWS deployment, or verify that security plans address "
            "all in-scope systems and data flows?"
        ),
    },
    # Program Management
    "PM": {
        "policy": (
            "How does your risk management function review the information security "
            "program to confirm it has adequate resources, executive sponsorship, "
            "and measurable objectives? Do they challenge whether program metrics "
            "reflect actual security posture?"
        ),
        "technical": (
            "How does your risk management team evaluate program effectiveness? "
            "Do they review security KPIs and trend data, challenge whether the "
            "program addresses emerging cloud risks, validate that risk register "
            "entries are current and prioritized, or assess whether the program "
            "drives measurable improvement over time?"
        ),
    },
    # Personnel Security
    "PS": {
        "policy": (
            "How does your risk management function review personnel security policies "
            "to confirm they address background screening, access provisioning/deprovisioning, "
            "transfer procedures, and termination processes for staff with AWS access?"
        ),
        "technical": (
            "How does your risk management team verify that personnel security controls "
            "operate effectively? Do they review timeliness of access revocation upon "
            "termination, challenge whether transfer processes update AWS permissions "
            "appropriately, or validate that background check requirements are met "
            "before granting access to sensitive environments?"
        ),
    },
    # PII Processing and Transparency
    "PT": {
        "policy": (
            "How does your risk management function review PII processing and "
            "transparency policies to confirm they address data subject rights, "
            "consent management, and privacy impact assessments for AWS-hosted "
            "applications that process personal data?"
        ),
        "technical": (
            "How does your risk management team validate PII protection controls? "
            "Do they review data flow mappings for personal data in AWS, challenge "
            "whether encryption and access controls are sufficient for PII, or "
            "verify that data retention and deletion procedures work as documented?"
        ),
    },
    # Risk Assessment
    "RA": {
        "policy": (
            "How does your risk management function review the risk assessment "
            "methodology to confirm it addresses cloud-specific threat vectors, "
            "shared responsibility model implications, and emerging risks to "
            "your AWS environment?"
        ),
        "technical": (
            "How does your risk management team validate that risk assessments "
            "are thorough and current? Do they review vulnerability scan results "
            "from Inspector or third-party tools, challenge whether risk ratings "
            "reflect actual exploitability, or verify that risk treatment decisions "
            "are documented and tracked to closure?"
        ),
    },
    # System and Services Acquisition
    "SA": {
        "policy": (
            "How does your risk management function review system and services "
            "acquisition policies to confirm they address secure development "
            "practices, third-party risk assessment, and supply chain security "
            "for AWS-deployed applications?"
        ),
        "technical": (
            "How does your risk management team oversee the acquisition and "
            "development lifecycle? Do they review secure coding practices, "
            "challenge whether third-party dependencies are vetted for "
            "vulnerabilities, validate that development environments are "
            "isolated from production, or verify that security requirements "
            "are included in procurement and development processes?"
        ),
    },
    # System and Communications Protection
    "SC": {
        "policy": (
            "How does your risk management function review system and communications "
            "protection policies to confirm they address encryption standards, "
            "network segmentation requirements, and boundary protection for "
            "your AWS architecture?"
        ),
        "technical": (
            "How does your risk management team validate network and communications "
            "security? Do they review VPC configurations and security group rules, "
            "challenge whether encryption in transit and at rest meets standards, "
            "monitor for unauthorized network flows using VPC Flow Logs, or verify "
            "that boundary protections like WAF and Shield are configured correctly?"
        ),
    },
    # System and Information Integrity
    "SI": {
        "policy": (
            "How does your risk management function review system and information "
            "integrity policies to confirm they address vulnerability management, "
            "malware protection, and integrity monitoring for AWS workloads?"
        ),
        "technical": (
            "How does your risk management team validate system integrity controls? "
            "Do they review vulnerability remediation timelines, challenge whether "
            "GuardDuty and Inspector findings are addressed within SLA, verify that "
            "integrity monitoring detects unauthorized changes, or assess whether "
            "patch management covers all AWS-hosted systems?"
        ),
    },
    # Supply Chain Risk Management
    "SR": {
        "policy": (
            "How does your risk management function review supply chain risk "
            "management policies to confirm they address third-party risk "
            "assessment, vendor security requirements, and software supply "
            "chain integrity for AWS-deployed applications?"
        ),
        "technical": (
            "How does your risk management team validate supply chain controls? "
            "Do they review third-party vendor security assessments, challenge "
            "whether software bill of materials (SBOM) practices are in place, "
            "verify that container images and dependencies are scanned for "
            "vulnerabilities, or assess whether vendor access to AWS environments "
            "is appropriately restricted and monitored?"
        ),
    },
}


# ---------------------------------------------------------------------------
# NIST 800-53 — Third Line (Internal Audit) Questions by Family
# ---------------------------------------------------------------------------
NIST_THIRD_LINE: Dict[str, Dict[str, str]] = {
    "AC": {
        "policy": (
            "Has internal audit independently tested whether the access control policy "
            "is enforced in practice? Did they sample user access reviews, verify that "
            "policy exceptions are documented and approved, and assess whether the policy "
            "keeps pace with changes to the AWS environment?"
        ),
        "technical": (
            "Has internal audit independently tested access control effectiveness? "
            "Did they sample IAM roles and policies for least-privilege adherence, "
            "test whether access reviews are performed on schedule, verify that "
            "terminated user access is revoked promptly, and assess whether "
            "evidence of access control operation is sufficient for external audit?"
        ),
    },
    "AT": {
        "policy": (
            "Has internal audit assessed whether the security training program meets "
            "regulatory and organizational requirements? Did they verify training "
            "records are maintained, test whether role-based training assignments "
            "are accurate, and evaluate whether training content is current?"
        ),
        "technical": (
            "Has internal audit tested training effectiveness beyond completion rates? "
            "Did they interview staff to assess knowledge retention, verify that "
            "personnel with AWS administrative access received cloud-specific training, "
            "and evaluate whether training gaps correlate with security incidents?"
        ),
    },
    "AU": {
        "policy": (
            "Has internal audit independently verified that the audit and accountability "
            "policy is enforced? Did they test whether log retention meets stated "
            "requirements, verify that audit log review procedures are followed, "
            "and assess whether the policy addresses all in-scope AWS services?"
        ),
        "technical": (
            "Has internal audit independently tested audit logging controls? Did they "
            "verify CloudTrail is enabled in all accounts and regions, test log "
            "integrity validation, confirm that log review and alerting processes "
            "detect simulated suspicious activity, and assess whether audit evidence "
            "is tamper-resistant and retrievable for the required retention period?"
        ),
    },
    "CA": {
        "policy": (
            "Has internal audit reviewed the security assessment and authorization "
            "process for independence and rigor? Did they verify that assessments "
            "cover all in-scope systems, that findings are tracked to remediation, "
            "and that authorization decisions are based on current risk information?"
        ),
        "technical": (
            "Has internal audit independently tested the security assessment process? "
            "Did they verify that assessment scope covers all AWS accounts and services, "
            "test whether POA&M items are remediated within target dates, and evaluate "
            "whether continuous monitoring provides adequate ongoing assurance between "
            "formal assessments?"
        ),
    },
    "CM": {
        "policy": (
            "Has internal audit verified that configuration management policies are "
            "enforced? Did they test whether baseline configurations are documented "
            "and current, verify that change management procedures are followed, "
            "and assess whether the policy addresses infrastructure-as-code practices?"
        ),
        "technical": (
            "Has internal audit independently tested configuration management controls? "
            "Did they sample AWS Config rule compliance results, verify that "
            "unauthorized configuration changes are detected and remediated, test "
            "whether change records match actual infrastructure changes, and assess "
            "whether configuration evidence is sufficient for external audit?"
        ),
    },
    "CP": {
        "policy": (
            "Has internal audit verified that contingency planning policies are "
            "actionable and tested? Did they review DR test results, verify that "
            "backup and recovery procedures are documented for AWS workloads, "
            "and assess whether the policy addresses realistic failure scenarios?"
        ),
        "technical": (
            "Has internal audit independently tested contingency plan effectiveness? "
            "Did they verify that backup restoration has been tested within the "
            "required timeframe, test whether failover procedures achieve stated "
            "RTO/RPO targets, and assess whether DR test evidence demonstrates "
            "actual recovery capability rather than just procedural compliance?"
        ),
    },
    "IA": {
        "policy": (
            "Has internal audit verified that identification and authentication "
            "policies are enforced? Did they test whether MFA requirements are "
            "met across all user populations, verify that password/credential "
            "standards are applied, and assess whether the policy addresses "
            "programmatic and service account authentication?"
        ),
        "technical": (
            "Has internal audit independently tested authentication controls? "
            "Did they verify MFA is enforced for all console and CLI access, "
            "test whether service accounts use temporary credentials, sample "
            "federation configurations for proper attribute mapping, and assess "
            "whether authentication evidence trails are sufficient for external audit?"
        ),
    },
    "IR": {
        "policy": (
            "Has internal audit verified that the incident response policy is "
            "actionable and tested? Did they review incident response test results, "
            "verify that roles and escalation paths are current, and assess whether "
            "the policy addresses cloud-specific incident scenarios?"
        ),
        "technical": (
            "Has internal audit independently tested incident response capabilities? "
            "Did they review a sample of closed incidents for proper handling, verify "
            "that detection-to-containment times meet targets, test whether incident "
            "evidence is preserved and retrievable, and assess whether post-incident "
            "reviews drive measurable improvements?"
        ),
    },
    "MA": {
        "policy": (
            "Has internal audit verified that maintenance policies are enforced? "
            "Did they test whether patching cadences are met, verify that maintenance "
            "windows are approved and documented, and assess whether the policy "
            "addresses both OS-level and application-level maintenance?"
        ),
        "technical": (
            "Has internal audit independently tested maintenance controls? Did they "
            "verify patching compliance rates against stated SLAs, test whether "
            "emergency patches are applied within required timeframes, and assess "
            "whether maintenance records provide sufficient evidence of timely "
            "remediation for external audit?"
        ),
    },
    "MP": {
        "policy": (
            "Has internal audit verified that media protection policies are enforced? "
            "Did they test whether data classification drives encryption decisions, "
            "verify that disposal procedures are followed, and assess whether the "
            "policy addresses cloud storage lifecycle management?"
        ),
        "technical": (
            "Has internal audit independently tested media protection controls? "
            "Did they verify that S3 buckets and EBS volumes are encrypted per policy, "
            "test whether data lifecycle rules properly expire or archive data, and "
            "assess whether evidence of encryption enforcement is sufficient for "
            "external audit?"
        ),
    },
    "PE": {
        "policy": (
            "Has internal audit verified that physical and environmental protection "
            "responsibilities are clearly documented? Did they confirm that AWS "
            "Artifact reports are reviewed for physical security coverage, and that "
            "customer-managed physical controls are independently assessed?"
        ),
        "technical": (
            "Has internal audit independently verified physical security coverage? "
            "Did they review current AWS SOC reports for physical control assurance, "
            "test whether customer-managed facility controls are operating effectively, "
            "and assess whether the shared responsibility delineation is clearly "
            "documented and evidenced?"
        ),
    },
    "PL": {
        "policy": (
            "Has internal audit verified that security plans are current and approved? "
            "Did they test whether plans reflect the actual AWS architecture, verify "
            "that plans are updated when significant changes occur, and assess whether "
            "plans address all in-scope systems?"
        ),
        "technical": (
            "Has internal audit independently tested whether security plans are "
            "implemented as documented? Did they compare planned controls against "
            "actual AWS configurations, verify that architecture diagrams match "
            "deployed infrastructure, and assess whether planning documentation "
            "is sufficient for external audit?"
        ),
    },
    "PM": {
        "policy": (
            "Has internal audit assessed the information security program for "
            "adequacy and effectiveness? Did they verify that program objectives "
            "are measurable, that executive reporting is accurate, and that the "
            "program addresses the organization's risk profile?"
        ),
        "technical": (
            "Has internal audit independently evaluated program management "
            "effectiveness? Did they verify that security metrics are accurate "
            "and meaningful, test whether risk register entries are current, "
            "and assess whether the program drives measurable security improvement "
            "across the AWS environment?"
        ),
    },
    "PS": {
        "policy": (
            "Has internal audit verified that personnel security policies are "
            "enforced? Did they test whether background checks are performed "
            "before access is granted, verify that termination procedures include "
            "timely access revocation, and assess whether transfer processes "
            "update access appropriately?"
        ),
        "technical": (
            "Has internal audit independently tested personnel security controls? "
            "Did they sample terminated employees to verify AWS access was revoked "
            "within required timeframes, test whether transfer processes properly "
            "adjust IAM permissions, and assess whether personnel security evidence "
            "trails are sufficient for external audit?"
        ),
    },
    "PT": {
        "policy": (
            "Has internal audit verified that PII processing and transparency "
            "policies are enforced? Did they test whether privacy impact assessments "
            "are performed for new systems, verify that data subject rights processes "
            "work as documented, and assess policy alignment with applicable regulations?"
        ),
        "technical": (
            "Has internal audit independently tested PII protection controls? "
            "Did they verify that personal data flows are mapped and accurate, "
            "test whether data subject access requests are fulfilled within "
            "required timeframes, and assess whether PII protection evidence "
            "is sufficient for regulatory and external audit?"
        ),
    },
    "RA": {
        "policy": (
            "Has internal audit verified that the risk assessment methodology is "
            "sound and consistently applied? Did they test whether risk assessments "
            "are performed at required intervals, verify that findings drive "
            "remediation actions, and assess whether the methodology addresses "
            "cloud-specific risks?"
        ),
        "technical": (
            "Has internal audit independently tested risk assessment processes? "
            "Did they verify that vulnerability scans cover all in-scope AWS "
            "resources, test whether risk ratings are consistent and defensible, "
            "and assess whether risk treatment plans are tracked to closure with "
            "sufficient evidence for external audit?"
        ),
    },
    "SA": {
        "policy": (
            "Has internal audit verified that system and services acquisition "
            "policies are enforced? Did they test whether security requirements "
            "are included in procurement, verify that development practices follow "
            "secure coding standards, and assess whether third-party risk "
            "assessments are performed?"
        ),
        "technical": (
            "Has internal audit independently tested acquisition and development "
            "controls? Did they review secure development lifecycle evidence, "
            "verify that third-party components are assessed for vulnerabilities, "
            "test whether development and production environments are properly "
            "separated, and assess whether acquisition evidence is sufficient "
            "for external audit?"
        ),
    },
    "SC": {
        "policy": (
            "Has internal audit verified that system and communications protection "
            "policies are enforced? Did they test whether encryption standards are "
            "applied consistently, verify that network segmentation requirements "
            "are met, and assess whether the policy addresses all data-in-transit "
            "and data-at-rest scenarios?"
        ),
        "technical": (
            "Has internal audit independently tested communications protection "
            "controls? Did they verify that TLS/encryption is enforced for all "
            "data in transit, test whether VPC segmentation and security groups "
            "enforce least-privilege network access, and assess whether network "
            "security evidence is sufficient for external audit?"
        ),
    },
    "SI": {
        "policy": (
            "Has internal audit verified that system and information integrity "
            "policies are enforced? Did they test whether vulnerability management "
            "SLAs are met, verify that integrity monitoring is in place, and assess "
            "whether the policy addresses all in-scope AWS services?"
        ),
        "technical": (
            "Has internal audit independently tested system integrity controls? "
            "Did they verify that vulnerability remediation meets stated SLAs, "
            "test whether integrity monitoring detects unauthorized changes, "
            "sample GuardDuty and Inspector findings for timely resolution, and "
            "assess whether integrity evidence is sufficient for external audit?"
        ),
    },
    "SR": {
        "policy": (
            "Has internal audit verified that supply chain risk management policies "
            "are enforced? Did they test whether vendor assessments are performed, "
            "verify that software supply chain controls are in place, and assess "
            "whether the policy addresses third-party access to AWS environments?"
        ),
        "technical": (
            "Has internal audit independently tested supply chain controls? "
            "Did they verify that vendor security assessments are current, test "
            "whether software dependencies are scanned for vulnerabilities, "
            "and assess whether supply chain risk evidence is sufficient for "
            "external audit?"
        ),
    },
}


# ---------------------------------------------------------------------------
# NIST CSF 2.0 — Second Line (Risk Management) Questions by Function
# ---------------------------------------------------------------------------
CSF_SECOND_LINE: Dict[str, str] = {
    "GV": (
        "How does your risk management function review and challenge the governance "
        "structures supporting this outcome? Do they assess whether policies, roles, "
        "and oversight mechanisms are adequate for the organization's risk profile, "
        "and whether governance decisions are informed by current threat intelligence "
        "and business context?"
    ),
    "ID": (
        "How does your risk management function validate that asset identification, "
        "risk assessment, and business environment understanding are thorough and current? "
        "Do they challenge whether asset inventories reflect the actual AWS environment, "
        "whether risk assessments address emerging threats, and whether improvement "
        "opportunities are prioritized based on risk?"
    ),
    "PR": (
        "How does your risk management function verify that protective controls are "
        "operating as intended? Do they review access management effectiveness, "
        "challenge whether security awareness programs address real risks, validate "
        "that data protection and platform security controls are configured correctly, "
        "and assess whether resilience measures are tested?"
    ),
    "DE": (
        "How does your risk management function evaluate detection capabilities? "
        "Do they challenge whether continuous monitoring covers all critical assets, "
        "review detection rule effectiveness and false positive rates, validate that "
        "adverse event analysis processes identify real threats, and assess whether "
        "detection timelines meet organizational risk tolerance?"
    ),
    "RS": (
        "How does your risk management function oversee incident response readiness? "
        "Do they review response plan adequacy, challenge whether communication "
        "protocols work during incidents, validate that analysis capabilities can "
        "determine root cause, and assess whether containment and mitigation "
        "actions are effective and timely?"
    ),
    "RC": (
        "How does your risk management function evaluate recovery capabilities? "
        "Do they challenge whether recovery plans are realistic and tested, review "
        "whether recovery communication reaches all stakeholders, and validate that "
        "lessons learned from recovery exercises drive measurable improvements?"
    ),
}

# ---------------------------------------------------------------------------
# NIST CSF 2.0 — Third Line (Internal Audit) Questions by Function
# ---------------------------------------------------------------------------
CSF_THIRD_LINE: Dict[str, str] = {
    "GV": (
        "Has internal audit independently assessed the effectiveness of cybersecurity "
        "governance? Did they test whether governance policies are enforced in practice, "
        "verify that oversight roles have adequate authority and resources, evaluate "
        "whether risk management decisions are documented and defensible, and assess "
        "whether governance evidence is sufficient for external audit or regulatory review?"
    ),
    "ID": (
        "Has internal audit independently tested identification and risk assessment "
        "processes? Did they verify that asset inventories are accurate and current, "
        "test whether risk assessments are performed at required intervals with "
        "consistent methodology, and assess whether identification evidence "
        "demonstrates the organization understands its risk posture?"
    ),
    "PR": (
        "Has internal audit independently tested protective controls? Did they sample "
        "access controls for least-privilege adherence, verify that training records "
        "are maintained, test whether data protection controls operate as designed, "
        "validate platform security configurations against baselines, and assess "
        "whether protection evidence is sufficient for external audit?"
    ),
    "DE": (
        "Has internal audit independently tested detection capabilities? Did they "
        "verify that monitoring covers all in-scope assets, test whether detection "
        "rules identify simulated threats, review adverse event analysis for "
        "thoroughness, and assess whether detection evidence demonstrates timely "
        "identification of security events?"
    ),
    "RS": (
        "Has internal audit independently tested incident response capabilities? "
        "Did they review a sample of incidents for proper handling and documentation, "
        "test whether response timelines meet stated targets, verify that forensic "
        "evidence is preserved, and assess whether response evidence is sufficient "
        "for external audit and regulatory reporting?"
    ),
    "RC": (
        "Has internal audit independently tested recovery capabilities? Did they "
        "verify that recovery plans have been tested within required timeframes, "
        "test whether recovery procedures achieve stated objectives, and assess "
        "whether recovery evidence demonstrates actual capability rather than "
        "just procedural documentation?"
    ),
}


# ---------------------------------------------------------------------------
# Lookup Functions
# ---------------------------------------------------------------------------

def get_nist_second_line_question(control_id: str) -> Optional[str]:
    """Get a family-specific second line defense question for a NIST 800-53 control.
    
    Returns a question tailored to the control family that prompts the customer
    to describe how their risk management function reviews and challenges
    first-line operations for this control area.
    """
    family = control_id.upper().split('-')[0] if '-' in control_id else control_id.upper()
    is_policy = control_id.lower().endswith('-1')
    
    family_qs = NIST_SECOND_LINE.get(family)
    if not family_qs:
        return None
    
    return family_qs.get('policy' if is_policy else 'technical')


def get_nist_third_line_question(control_id: str) -> Optional[str]:
    """Get a family-specific third line defense question for a NIST 800-53 control.
    
    Returns a question tailored to the control family that prompts the customer
    to describe how internal audit independently tests and evaluates controls
    in this area.
    """
    family = control_id.upper().split('-')[0] if '-' in control_id else control_id.upper()
    is_policy = control_id.lower().endswith('-1')
    
    family_qs = NIST_THIRD_LINE.get(family)
    if not family_qs:
        return None
    
    return family_qs.get('policy' if is_policy else 'technical')


def get_csf_second_line_question(subcategory_id: str) -> Optional[str]:
    """Get a function-specific second line defense question for a CSF subcategory.
    
    Returns a question tailored to the CSF function (GV, ID, PR, DE, RS, RC)
    that prompts the customer to describe how their risk management function
    reviews and challenges first-line operations for this outcome area.
    """
    # Extract function code: "GV.OC-01" -> "GV", "DE.AE-02" -> "DE"
    func_code = subcategory_id.upper().split('.')[0] if '.' in subcategory_id else None
    if not func_code:
        return None
    
    return CSF_SECOND_LINE.get(func_code)


def get_csf_third_line_question(subcategory_id: str) -> Optional[str]:
    """Get a function-specific third line defense question for a CSF subcategory.
    
    Returns a question tailored to the CSF function (GV, ID, PR, DE, RS, RC)
    that prompts the customer to describe how internal audit independently
    tests and evaluates controls supporting this outcome.
    """
    func_code = subcategory_id.upper().split('.')[0] if '.' in subcategory_id else None
    if not func_code:
        return None
    
    return CSF_THIRD_LINE.get(func_code)
