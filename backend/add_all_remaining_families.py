#!/usr/bin/env python3
"""
Add AWS-specific questions for all remaining control families:
CA, SA, PS, MA, MP, PM, PT, SR
"""

# New questions to add to CONTROL_QUESTIONS dictionary
NEW_CONTROL_QUESTIONS = """
    
    # Assessment, Authorization, and Monitoring (CA)
    'ca-1': [
        {
            'type': 'policy_existence',
            'question': 'Do you have documented policies for security assessment, authorization, and continuous monitoring in AWS? Does it define assessment frequency, authorization requirements, and monitoring scope?',
        },
        {
            'type': 'aws_assessment_tools',
            'question': 'Does your policy specify which AWS assessment tools to use (Security Hub, Config, Inspector, Trusted Advisor, Audit Manager)? Are assessment procedures documented?',
        },
        {
            'type': 'authorization_process',
            'question': 'What is your AWS system authorization process (initial ATO, continuous ATO, reauthorization frequency)? Who is the authorizing official for AWS workloads?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates CA-1 compliance? Provide: Assessment and authorization policy document with approval signatures, policy review records, assessment procedure documentation. Where are these artifacts stored?',
        },
    ],
    'ca-2': [
        {
            'type': 'assessment_frequency',
            'question': 'How often are security control assessments conducted in AWS (annually, continuously, after major changes)? Are you using AWS Audit Manager for continuous assessment?',
        },
        {
            'type': 'assessment_scope',
            'question': 'What is assessed (IAM policies, network configurations, encryption settings, logging, monitoring, incident response capabilities)? Do assessments cover all AWS accounts and regions?',
        },
        {
            'type': 'assessment_tools',
            'question': 'What tools support control assessments (Security Hub security standards, Config conformance packs, Inspector assessments, manual reviews)? Are findings tracked in a centralized system?',
        },
        {
            'type': 'independent_assessors',
            'question': 'Are assessments conducted by independent assessors (third-party auditors, internal audit team separate from operations)? How is assessor independence verified?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates CA-2 compliance? Provide: Assessment reports, Security Hub compliance summaries, Config conformance pack results, assessment schedules, assessor qualifications. Where are these artifacts stored?',
        },
    ],
    'ca-3': [
        {
            'type': 'connection_authorization',
            'question': 'What is your process for authorizing connections between AWS and external systems (VPN, Direct Connect, VPC peering, Transit Gateway, third-party SaaS)? Who approves these connections?',
        },
        {
            'type': 'security_requirements',
            'question': 'What security requirements must external connections meet (encryption in transit, authentication, logging, data classification restrictions)? How are requirements enforced?',
        },
        {
            'type': 'connection_monitoring',
            'question': 'How are external connections monitored (VPC Flow Logs, CloudWatch metrics, GuardDuty findings, third-party network monitoring)? Are unauthorized connections detected and blocked?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates CA-3 compliance? Provide: Connection authorization documentation, security requirements for external connections, VPC Flow Logs, network diagrams, connection monitoring reports. Where are these artifacts stored?',
        },
    ],
    'ca-5': [
        {
            'type': 'poam_process',
            'question': 'Do you maintain a Plan of Action and Milestones (POA&M) for AWS security findings? What tool tracks remediation (JIRA, ServiceNow, AWS Security Hub, spreadsheet)?',
        },
        {
            'type': 'finding_sources',
            'question': 'What sources feed into your POA&M (Security Hub findings, Config non-compliance, Inspector vulnerabilities, penetration test results, audit findings)? How are findings prioritized?',
        },
        {
            'type': 'remediation_tracking',
            'question': 'What are your remediation SLAs by severity (critical: 7 days, high: 30 days, medium: 90 days)? How often is POA&M status reviewed with management?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates CA-5 compliance? Provide: Current POA&M with all open findings, remediation status reports, management review meeting notes, closed finding documentation. Where are these artifacts stored?',
        },
    ],
    'ca-6': [
        {
            'type': 'authorization_process',
            'question': 'What is your AWS system authorization process? Do you have an Authority to Operate (ATO) for your AWS environment? When does it expire, and what triggers reauthorization?',
        },
        {
            'type': 'authorization_package',
            'question': 'What is included in your authorization package (system security plan, risk assessment, control assessment results, POA&M, authorization decision letter)? Is it updated regularly?',
        },
        {
            'type': 'authorizing_official',
            'question': 'Who is the Authorizing Official for AWS systems? Do they have appropriate authority level and independence from system operations?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates CA-6 compliance? Provide: Current authorization decision letter, system security plan, authorization package documentation, reauthorization schedule. Where are these artifacts stored?',
        },
    ],
    'ca-7': [
        {
            'type': 'monitoring_strategy',
            'question': 'What is your continuous monitoring strategy for AWS (Security Hub, Config, GuardDuty, CloudWatch, CloudTrail)? Are all AWS accounts and regions monitored?',
        },
        {
            'type': 'monitoring_scope',
            'question': 'What is monitored (configuration changes, security findings, compliance status, vulnerabilities, threats, user activity, network traffic)? How frequently are findings reviewed?',
        },
        {
            'type': 'automated_response',
            'question': 'Do you have automated responses to monitoring findings (Lambda remediation, Systems Manager automation, Security Hub custom actions, EventBridge rules)? What findings trigger automatic remediation?',
        },
        {
            'type': 'reporting',
            'question': 'How often are monitoring results reported to management (daily dashboards, weekly summaries, monthly reports)? Who receives these reports, and what actions result?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates CA-7 compliance? Provide: Security Hub dashboards, Config compliance timelines, GuardDuty findings reports, monitoring strategy document, management review records. Where are these artifacts stored?',
        },
    ],
    'ca-9': [
        {
            'type': 'internal_connections',
            'question': 'What internal connections exist in your AWS environment (VPC peering, Transit Gateway, PrivateLink, cross-account access)? Are they documented and authorized?',
        },
        {
            'type': 'connection_security',
            'question': 'How are internal connections secured (security groups, NACLs, IAM policies, resource policies, SCPs)? Are least privilege principles applied?',
        },
        {
            'type': 'connection_monitoring',
            'question': 'How are internal connections monitored (VPC Flow Logs, CloudTrail, Config rules for unauthorized connections)? Are connection changes alerted?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates CA-9 compliance? Provide: Network architecture diagrams, connection authorization records, VPC Flow Logs, security group configurations, monitoring alerts. Where are these artifacts stored?',
        },
    ],
    
    # System and Services Acquisition (SA)
    'sa-1': [
        {
            'type': 'policy_existence',
            'question': 'Do you have documented policies for acquiring and developing systems in AWS? Does it cover security requirements, vendor assessment, and secure development practices?',
        },
        {
            'type': 'aws_service_selection',
            'question': 'Does your policy define criteria for selecting AWS services (compliance certifications, data residency, encryption capabilities, audit logging)? Who approves new AWS service usage?',
        },
        {
            'type': 'third_party_services',
            'question': 'What is your process for evaluating third-party services that integrate with AWS (security assessment, contract review, data protection requirements)? Are approved services documented?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates SA-1 compliance? Provide: System acquisition policy document with approval signatures, AWS service approval process, approved services list, policy review records. Where are these artifacts stored?',
        },
    ],
    'sa-2': [
        {
            'type': 'resource_allocation',
            'question': 'How do you allocate resources for AWS security (budget for security tools, staff for security operations, time for security reviews)? Is security funding adequate?',
        },
        {
            'type': 'security_budget',
            'question': 'What security tools and services are funded (Security Hub, GuardDuty, Inspector, Macie, third-party tools)? Are security costs tracked separately from infrastructure costs?',
        },
        {
            'type': 'staffing',
            'question': 'Do you have dedicated AWS security staff or is it shared responsibility? What is the ratio of security staff to AWS accounts/workloads?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates SA-2 compliance? Provide: Security budget documentation, security tool subscriptions, staffing plans, resource allocation decisions. Where are these artifacts stored?',
        },
    ],
    'sa-3': [
        {
            'type': 'sdlc_process',
            'question': 'What is your secure development lifecycle for AWS applications? Does it include threat modeling, secure coding, security testing, and deployment reviews?',
        },
        {
            'type': 'security_gates',
            'question': 'What security gates exist in your SDLC (design review, code review, SAST/DAST scanning, penetration testing, security approval before production)? Can deployments be blocked for security issues?',
        },
        {
            'type': 'infrastructure_as_code',
            'question': 'Do you use Infrastructure as Code for AWS deployments (CloudFormation, Terraform, CDK)? Are IaC templates scanned for security issues (Checkov, cfn-nag, Terraform Sentinel)?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates SA-3 compliance? Provide: SDLC documentation, security gate requirements, IaC scanning reports, code review records, security approval documentation. Where are these artifacts stored?',
        },
    ],
    'sa-4': [
        {
            'type': 'acquisition_requirements',
            'question': 'What security requirements are included in AWS service and third-party acquisitions (encryption, logging, compliance certifications, data residency, incident response)?',
        },
        {
            'type': 'vendor_assessment',
            'question': 'How do you assess third-party vendors that integrate with AWS (security questionnaires, SOC 2 reports, penetration test results, compliance certifications)? Who approves vendors?',
        },
        {
            'type': 'contract_requirements',
            'question': 'What security clauses are in vendor contracts (data protection, breach notification, audit rights, data deletion, subprocessor restrictions)? Are contracts reviewed by legal and security?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates SA-4 compliance? Provide: Security requirements documentation, vendor assessment reports, approved vendor list, contract security clauses, vendor compliance certificates. Where are these artifacts stored?',
        },
    ],
    'sa-5': [
        {
            'type': 'system_documentation',
            'question': 'What documentation exists for AWS systems (architecture diagrams, data flow diagrams, security controls, configuration standards, runbooks)? Is it kept current?',
        },
        {
            'type': 'documentation_location',
            'question': 'Where is AWS system documentation stored (wiki, SharePoint, Git repository, AWS Systems Manager documents)? Who has access, and how is it version controlled?',
        },
        {
            'type': 'documentation_updates',
            'question': 'How often is documentation reviewed and updated (after changes, quarterly, annually)? Who is responsible for maintaining documentation accuracy?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates SA-5 compliance? Provide: System architecture diagrams, security control documentation, configuration standards, documentation update logs, documentation access controls. Where are these artifacts stored?',
        },
    ],
    'sa-8': [
        {
            'type': 'security_principles',
            'question': 'What security engineering principles guide AWS architecture (defense in depth, least privilege, separation of duties, fail secure, complete mediation)? Are they documented?',
        },
        {
            'type': 'well_architected',
            'question': 'Do you follow the AWS Well-Architected Framework security pillar? Have you conducted Well-Architected Reviews? How are findings addressed?',
        },
        {
            'type': 'security_by_design',
            'question': 'How is security incorporated into design decisions (threat modeling, security architecture review, security requirements in design documents)? Who reviews designs for security?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates SA-8 compliance? Provide: Security engineering principles documentation, Well-Architected Review reports, threat models, security architecture review records. Where are these artifacts stored?',
        },
    ],
    'sa-9': [
        {
            'type': 'external_services',
            'question': 'What external services integrate with your AWS environment (SaaS applications, third-party APIs, managed services, data processors)? Are they inventoried and approved?',
        },
        {
            'type': 'service_security',
            'question': 'How do you ensure external services meet security requirements (SOC 2 Type II, ISO 27001, security assessments, contract terms)? Are services reassessed periodically?',
        },
        {
            'type': 'data_protection',
            'question': 'How is data protected when shared with external services (encryption in transit, data minimization, access controls, data residency requirements)? Are data flows documented?',
        },
        {
            'type': 'monitoring',
            'question': 'How are external service connections monitored (API logging, CloudTrail for AWS service integrations, anomaly detection)? Are unauthorized connections detected?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates SA-9 compliance? Provide: External services inventory, service security assessments, data flow diagrams, service contracts, monitoring logs. Where are these artifacts stored?',
        },
    ],
    'sa-10': [
        {
            'type': 'configuration_management',
            'question': 'How do you manage AWS infrastructure configurations (Git for IaC, AWS Config for drift detection, version control for CloudFormation/Terraform)? Are changes tracked and auditable?',
        },
        {
            'type': 'change_control',
            'question': 'What is your change control process for AWS infrastructure (pull requests, peer review, automated testing, approval workflow)? Can unauthorized changes be prevented?',
        },
        {
            'type': 'baseline_configurations',
            'question': 'Do you have baseline configurations for AWS resources (EC2 AMIs, security group templates, IAM policy templates)? How are baselines enforced and deviations detected?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates SA-10 compliance? Provide: IaC repository with change history, Config drift detection reports, baseline configuration documentation, change approval records. Where are these artifacts stored?',
        },
    ],
    'sa-11': [
        {
            'type': 'security_testing',
            'question': 'What security testing is performed before AWS deployments (SAST, DAST, dependency scanning, IaC security scanning, penetration testing)? Are tests automated in CI/CD?',
        },
        {
            'type': 'testing_frequency',
            'question': 'How often is security testing conducted (every commit, every release, quarterly, annually)? Are critical findings blocking deployments?',
        },
        {
            'type': 'testing_tools',
            'question': 'What tools support security testing (SonarQube, Snyk, Checkmarx, OWASP ZAP, AWS Inspector, third-party scanners)? Are findings tracked and remediated?',
        },
        {
            'type': 'penetration_testing',
            'question': 'How often are penetration tests conducted on AWS environments (annually, after major changes)? Are AWS penetration testing guidelines followed? Who conducts tests?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates SA-11 compliance? Provide: Security testing reports, SAST/DAST scan results, penetration test reports, testing schedule, remediation tracking. Where are these artifacts stored?',
        },
    ],
    'sa-15': [
        {
            'type': 'development_standards',
            'question': 'What secure development standards apply to AWS applications (OWASP Top 10, AWS security best practices, coding standards, security libraries)? Are developers trained on these standards?',
        },
        {
            'type': 'development_tools',
            'question': 'What development tools enforce security (IDE security plugins, pre-commit hooks, automated code review, security linters)? Are insecure practices prevented?',
        },
        {
            'type': 'code_review',
            'question': 'Are security-focused code reviews required (peer review, security team review for sensitive changes)? What security issues are reviewers trained to identify?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates SA-15 compliance? Provide: Secure development standards documentation, code review records, security training completion, development tool configurations. Where are these artifacts stored?',
        },
    ],
    'sa-22': [
        {
            'type': 'unsupported_components',
            'question': 'How do you identify unsupported components in AWS (EOL operating systems, deprecated AWS services, unmaintained libraries)? Are they inventoried?',
        },
        {
            'type': 'replacement_plan',
            'question': 'What is your plan for replacing unsupported components (migration timeline, alternative solutions, risk acceptance for delays)? Who approves continued use of unsupported components?',
        },
        {
            'type': 'monitoring',
            'question': 'How are unsupported components monitored for vulnerabilities (Inspector scanning, manual tracking, vendor notifications)? Are compensating controls in place?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates SA-22 compliance? Provide: Unsupported components inventory, replacement plans, risk acceptance documentation, vulnerability monitoring reports. Where are these artifacts stored?',
        },
    ],
    
    # Personnel Security (PS)
    'ps-1': [
        {
            'type': 'policy_existence',
            'question': 'Do you have documented personnel security policies covering position risk designation, screening, termination, and access agreements? When was it last reviewed?',
        },
        {
            'type': 'aws_access_controls',
            'question': 'Does your policy address AWS-specific personnel security (IAM user lifecycle, privileged access management, access reviews, separation of duties)?',
        },
        {
            'type': 'policy_enforcement',
            'question': 'How is your personnel security policy enforced (HR processes, IAM automation, access review workflows, termination checklists)? Are violations tracked?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates PS-1 compliance? Provide: Personnel security policy document with approval signatures, policy review records, enforcement procedure documentation. Where are these artifacts stored?',
        },
    ],
    'ps-2': [
        {
            'type': 'position_designation',
            'question': 'Have you designated risk levels for positions with AWS access (high risk for admins, moderate for developers, low for read-only users)? Is this documented?',
        },
        {
            'type': 'screening_requirements',
            'question': 'What screening requirements apply to each risk level (background checks, reference checks, education verification)? Are requirements based on position sensitivity?',
        },
        {
            'type': 'reassessment',
            'question': 'How often are position risk designations reassessed (when duties change, annually, when access level changes)? Who approves risk designations?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates PS-2 compliance? Provide: Position risk designation documentation, screening requirements by risk level, reassessment records. Where are these artifacts stored?',
        },
    ],
    'ps-3': [
        {
            'type': 'screening_process',
            'question': 'What screening is conducted before granting AWS access (background checks, employment verification, reference checks, education verification)? Who conducts screening?',
        },
        {
            'type': 'screening_criteria',
            'question': 'What are the screening criteria for AWS privileged access (criminal background check, credit check for financial systems, citizenship requirements)? Are criteria risk-based?',
        },
        {
            'type': 'rescreening',
            'question': 'How often is rescreening conducted (every 5 years, when position changes, when access level increases)? Are rescreening requirements documented?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates PS-3 compliance? Provide: Screening procedure documentation, background check records (redacted), screening completion records, rescreening schedule. Where are these artifacts stored?',
        },
    ],
    'ps-4': [
        {
            'type': 'termination_process',
            'question': 'What is your process for terminating AWS access when employees leave (immediate IAM user disablement, access key deletion, MFA device removal, session revocation)? How quickly is it executed?',
        },
        {
            'type': 'termination_checklist',
            'question': 'Do you have a termination checklist for AWS access (disable IAM user, remove from groups, delete access keys, remove MFA, review CloudTrail for final actions)? Who verifies completion?',
        },
        {
            'type': 'knowledge_transfer',
            'question': 'How is AWS knowledge transferred when personnel leave (documentation handoff, access to runbooks, credential rotation, system ownership transfer)? Is this tracked?',
        },
        {
            'type': 'post_termination_review',
            'question': 'Are terminated user activities reviewed post-termination (CloudTrail logs, resource changes, data access)? How long are logs retained for this purpose?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates PS-4 compliance? Provide: Termination checklist, IAM user termination records, CloudTrail logs of termination actions, knowledge transfer documentation. Where are these artifacts stored?',
        },
    ],
    'ps-5': [
        {
            'type': 'transfer_process',
            'question': 'What is your process when personnel transfer to new roles (access review, privilege adjustment, new role training, knowledge transfer)? How quickly is access adjusted?',
        },
        {
            'type': 'access_adjustment',
            'question': 'How are AWS permissions adjusted during transfers (remove old role permissions, add new role permissions, review for least privilege)? Is this automated or manual?',
        },
        {
            'type': 'transfer_review',
            'question': 'Who reviews and approves access changes during transfers (new manager, security team, HR)? Are approvals documented?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates PS-5 compliance? Provide: Transfer procedure documentation, access change records, approval documentation, IAM policy change logs. Where are these artifacts stored?',
        },
    ],
    'ps-6': [
        {
            'type': 'access_agreements',
            'question': 'Do personnel sign access agreements before receiving AWS access (acceptable use policy, confidentiality agreement, security responsibilities)? Are agreements reviewed annually?',
        },
        {
            'type': 'agreement_content',
            'question': 'What do access agreements cover (data protection, password security, MFA requirements, prohibited activities, incident reporting, acceptable use)?',
        },
        {
            'type': 'nda_requirements',
            'question': 'Are NDAs required for personnel with access to sensitive AWS data? Are third-party contractors required to sign additional agreements?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates PS-6 compliance? Provide: Access agreement templates, signed agreements (redacted), annual review records, contractor agreements. Where are these artifacts stored?',
        },
    ],
    'ps-7': [
        {
            'type': 'third_party_requirements',
            'question': 'What security requirements apply to third-party personnel with AWS access (background checks, security training, access agreements, supervision requirements)?',
        },
        {
            'type': 'contractor_management',
            'question': 'How are contractors and third-party personnel managed in AWS (separate IAM accounts, time-limited access, activity monitoring, access reviews)? Are they clearly identified?',
        },
        {
            'type': 'third_party_termination',
            'question': 'How is third-party access terminated when contracts end (automated expiration, manual review, access key deletion)? Who verifies termination?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates PS-7 compliance? Provide: Third-party security requirements, contractor IAM accounts list, access termination records, monitoring reports. Where are these artifacts stored?',
        },
    ],
    'ps-8': [
        {
            'type': 'sanctions_policy',
            'question': 'Do you have a personnel sanctions policy for security violations (policy violations, unauthorized access, data breaches, negligence)? What are the consequences?',
        },
        {
            'type': 'violation_tracking',
            'question': 'How are security violations tracked and investigated (incident tickets, HR cases, CloudTrail analysis)? Who investigates violations?',
        },
        {
            'type': 'sanctions_process',
            'question': 'What is the sanctions process (warning, suspension, termination, legal action)? Are sanctions proportional to violation severity? Who approves sanctions?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates PS-8 compliance? Provide: Personnel sanctions policy, violation tracking records (redacted), sanctions decisions (redacted), policy communication records. Where are these artifacts stored?',
        },
    ],
    'ps-9': [
        {
            'type': 'position_descriptions',
            'question': 'Do position descriptions for AWS roles include security responsibilities (least privilege, MFA usage, incident reporting, security training, acceptable use)?',
        },
        {
            'type': 'security_roles',
            'question': 'Are security roles and responsibilities clearly defined (security team, system administrators, developers, auditors)? Do job descriptions reflect actual AWS access levels?',
        },
        {
            'type': 'role_review',
            'question': 'How often are position descriptions reviewed and updated (annually, when duties change, when new AWS services are adopted)? Who approves updates?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates PS-9 compliance? Provide: Position descriptions with security responsibilities, role definition documentation, review and update records. Where are these artifacts stored?',
        },
    ],
    
    # Maintenance (MA)
    'ma-1': [
        {
            'type': 'policy_existence',
            'question': 'Do you have documented maintenance policies for AWS systems (patching, updates, maintenance windows, emergency maintenance)? When was it last reviewed?',
        },
        {
            'type': 'aws_maintenance',
            'question': 'Does your policy address AWS-specific maintenance (Systems Manager Patch Manager, automated patching, AMI updates, Lambda runtime updates, RDS maintenance windows)?',
        },
        {
            'type': 'maintenance_windows',
            'question': 'Are maintenance windows defined for AWS resources? How are maintenance activities scheduled and communicated? Are emergency patches expedited?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates MA-1 compliance? Provide: Maintenance policy document with approval signatures, maintenance schedule, policy review records. Where are these artifacts stored?',
        },
    ],
    'ma-2': [
        {
            'type': 'maintenance_control',
            'question': 'How is AWS maintenance controlled (change management, approval workflows, maintenance windows, rollback procedures)? Who approves maintenance activities?',
        },
        {
            'type': 'maintenance_logging',
            'question': 'Are maintenance activities logged (CloudTrail for API calls, Systems Manager maintenance windows, change tickets)? How long are maintenance logs retained?',
        },
        {
            'type': 'maintenance_review',
            'question': 'Are maintenance activities reviewed post-completion (success verification, rollback if needed, lessons learned)? Who conducts reviews?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates MA-2 compliance? Provide: Maintenance approval records, CloudTrail logs of maintenance activities, maintenance window reports, post-maintenance reviews. Where are these artifacts stored?',
        },
    ],
    'ma-3': [
        {
            'type': 'maintenance_tools',
            'question': 'What tools are used for AWS maintenance (Systems Manager, third-party patch management, automation scripts)? Are tools approved and secured?',
        },
        {
            'type': 'tool_security',
            'question': 'How are maintenance tools secured (IAM roles with least privilege, MFA for access, audit logging, tool integrity verification)? Are tools regularly updated?',
        },
        {
            'type': 'tool_inspection',
            'question': 'Are maintenance tools inspected for security issues (vulnerability scanning, code review for custom scripts, vendor security assessments)? How often?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates MA-3 compliance? Provide: Approved maintenance tools list, tool security configurations, tool inspection reports, IAM policies for maintenance tools. Where are these artifacts stored?',
        },
    ],
    'ma-4': [
        {
            'type': 'nonlocal_maintenance',
            'question': 'How is remote maintenance of AWS resources controlled (VPN requirements, MFA, session recording, approval workflows)? Are remote sessions monitored?',
        },
        {
            'type': 'remote_access_tools',
            'question': 'What tools enable remote AWS maintenance (Systems Manager Session Manager, AWS Client VPN, third-party remote access)? Are sessions encrypted and logged?',
        },
        {
            'type': 'third_party_maintenance',
            'question': 'If third parties perform remote maintenance, how is access controlled (time-limited IAM roles, supervised sessions, activity logging)? Are third-party actions reviewed?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates MA-4 compliance? Provide: Remote maintenance procedure documentation, Session Manager logs, VPN access logs, third-party maintenance records. Where are these artifacts stored?',
        },
    ],
    'ma-5': [
        {
            'type': 'maintenance_personnel',
            'question': 'Who is authorized to perform AWS maintenance (system administrators, DevOps team, third-party vendors)? Is authorization documented and reviewed?',
        },
        {
            'type': 'personnel_supervision',
            'question': 'Are maintenance personnel supervised during sensitive activities (production changes, security configuration updates, data access)? Who provides supervision?',
        },
        {
            'type': 'personnel_screening',
            'question': 'What screening is required for maintenance personnel (background checks, security training, access agreements)? Are requirements risk-based?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates MA-5 compliance? Provide: Authorized maintenance personnel list, supervision records, personnel screening documentation, IAM access records. Where are these artifacts stored?',
        },
    ],
    'ma-6': [
        {
            'type': 'timely_maintenance',
            'question': 'How quickly are security patches applied to AWS resources (critical: 7 days, high: 30 days, medium: 90 days)? Are SLAs documented and tracked?',
        },
        {
            'type': 'patch_management',
            'question': 'What is your AWS patch management process (Systems Manager Patch Manager, automated patching, patch testing, rollback procedures)? Are all resource types covered?',
        },
        {
            'type': 'maintenance_tracking',
            'question': 'How is maintenance compliance tracked (Systems Manager compliance reports, Config rules, third-party tools)? Are overdue patches escalated?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates MA-6 compliance? Provide: Patch management SLAs, Systems Manager compliance reports, patch deployment records, overdue patch reports. Where are these artifacts stored?',
        },
    ],
    
    # Media Protection (MP)
    'mp-1': [
        {
            'type': 'policy_existence',
            'question': 'Do you have documented media protection policies for AWS (data classification, encryption requirements, data disposal, backup protection)? When was it last reviewed?',
        },
        {
            'type': 'aws_data_protection',
            'question': 'Does your policy address AWS-specific media protection (S3 encryption, EBS encryption, RDS encryption, backup encryption, data lifecycle management)?',
        },
        {
            'type': 'data_classification',
            'question': 'Do you have a data classification scheme (public, internal, confidential, restricted)? Are AWS resources tagged with data classification? How is classification enforced?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates MP-1 compliance? Provide: Media protection policy document with approval signatures, data classification scheme, policy review records. Where are these artifacts stored?',
        },
    ],
    'mp-2': [
        {
            'type': 'media_access',
            'question': 'How is access to AWS data storage controlled (S3 bucket policies, EBS volume encryption, IAM policies, resource policies)? Is least privilege enforced?',
        },
        {
            'type': 'access_logging',
            'question': 'Are data access activities logged (S3 access logging, CloudTrail data events, VPC Flow Logs for EBS)? How long are access logs retained?',
        },
        {
            'type': 'unauthorized_access',
            'question': 'How is unauthorized data access detected and prevented (GuardDuty, Macie, Config rules for public access, automated remediation)? Are alerts configured?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates MP-2 compliance? Provide: S3 bucket policies, IAM access policies, access logging configurations, GuardDuty findings, unauthorized access alerts. Where are these artifacts stored?',
        },
    ],
    'mp-3': [
        {
            'type': 'media_marking',
            'question': 'How is AWS data marked with classification (resource tags, S3 object tags, metadata)? Are classification tags required and enforced?',
        },
        {
            'type': 'marking_automation',
            'question': 'Is data classification marking automated (Lambda functions, Config rules, tag policies)? How are untagged resources detected?',
        },
        {
            'type': 'marking_validation',
            'question': 'How is classification marking validated (Config rules, automated scanning, periodic reviews)? Are incorrectly marked resources corrected?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates MP-3 compliance? Provide: Tagging standards documentation, resource tag reports, untagged resource reports, tag enforcement policies. Where are these artifacts stored?',
        },
    ],
    'mp-4': [
        {
            'type': 'media_storage',
            'question': 'How is AWS data stored securely (encryption at rest, access controls, network isolation, backup encryption)? Are storage security requirements documented?',
        },
        {
            'type': 'encryption_requirements',
            'question': 'What encryption is required for AWS storage (S3 default encryption, EBS encryption, RDS encryption, KMS key management)? Are encryption requirements enforced?',
        },
        {
            'type': 'storage_monitoring',
            'question': 'How is storage security monitored (Config rules for encryption, Macie for sensitive data, Security Hub findings)? Are unencrypted resources detected?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates MP-4 compliance? Provide: Storage encryption configurations, Config compliance reports, KMS key policies, storage security monitoring reports. Where are these artifacts stored?',
        },
    ],
    'mp-5': [
        {
            'type': 'media_transport',
            'question': 'How is data protected during transport to/from AWS (TLS/SSL, VPN, Direct Connect with MACsec, AWS Transfer Family with encryption)? Are transport security requirements documented?',
        },
        {
            'type': 'transport_encryption',
            'question': 'Is encryption in transit enforced (S3 bucket policies requiring SSL, ALB/NLB with TLS, API Gateway with TLS)? Are weak protocols blocked?',
        },
        {
            'type': 'transport_monitoring',
            'question': 'How is data transport monitored (VPC Flow Logs, CloudTrail, GuardDuty for unusual data transfers)? Are unencrypted transfers detected?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates MP-5 compliance? Provide: Transport encryption configurations, S3 bucket policies requiring SSL, VPC Flow Logs, transport security monitoring reports. Where are these artifacts stored?',
        },
    ],
    'mp-6': [
        {
            'type': 'media_sanitization',
            'question': 'What is your process for sanitizing AWS data before disposal (S3 object deletion with versioning disabled, EBS volume deletion, RDS snapshot deletion, KMS key deletion)?',
        },
        {
            'type': 'sanitization_verification',
            'question': 'How do you verify data sanitization (CloudTrail logs of deletion, Config rules for deleted resources, automated verification)? Are deletion activities logged?',
        },
        {
            'type': 'aws_responsibility',
            'question': 'Do you acknowledge AWS responsibility for physical media sanitization in their data centers? Have you reviewed AWS data destruction procedures in AWS Artifact?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates MP-6 compliance? Provide: Data sanitization procedures, CloudTrail logs of deletion activities, sanitization verification records, AWS Artifact data destruction documentation. Where are these artifacts stored?',
        },
    ],
    'mp-7': [
        {
            'type': 'media_use',
            'question': 'Are there restrictions on AWS data usage (data classification-based access, purpose limitations, geographic restrictions)? How are restrictions enforced?',
        },
        {
            'type': 'usage_monitoring',
            'question': 'How is data usage monitored (CloudTrail data events, S3 access logging, Macie for sensitive data access, GuardDuty for anomalous access)? Are violations detected?',
        },
        {
            'type': 'usage_restrictions',
            'question': 'What technical controls enforce usage restrictions (IAM policies, S3 bucket policies, SCPs, VPC endpoints, PrivateLink)? Are controls tested?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates MP-7 compliance? Provide: Data usage restriction policies, IAM policies enforcing restrictions, usage monitoring reports, violation alerts. Where are these artifacts stored?',
        },
    ],
    'mp-8': [
        {
            'type': 'media_downgrading',
            'question': 'What is your process for downgrading AWS data classification (review and approval, metadata updates, access control changes)? Who approves downgrading?',
        },
        {
            'type': 'downgrading_verification',
            'question': 'How is data downgrading verified (tag updates, policy changes, access reviews)? Are downgrading activities logged and auditable?',
        },
        {
            'type': 'downgrading_restrictions',
            'question': 'What restrictions exist on data downgrading (approval requirements, prohibited downgrades, retention requirements)? Are restrictions enforced?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates MP-8 compliance? Provide: Data downgrading procedures, approval records, tag change logs, access control updates. Where are these artifacts stored?',
        },
    ],
    
    # Program Management (PM)
    'pm-1': [
        {
            'type': 'security_program',
            'question': 'Do you have a documented information security program for AWS? Does it include governance, risk management, compliance, and continuous improvement?',
        },
        {
            'type': 'program_leadership',
            'question': 'Who leads the AWS security program (CISO, security director, cloud security lead)? Do they have appropriate authority and resources?',
        },
        {
            'type': 'program_review',
            'question': 'How often is the security program reviewed and updated (annually, after major changes, continuous improvement)? Are metrics tracked?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates PM-1 compliance? Provide: Security program documentation, program charter, leadership appointments, program review records. Where are these artifacts stored?',
        },
    ],
    'pm-2': [
        {
            'type': 'senior_leadership',
            'question': 'How is senior leadership involved in AWS security (security briefings, risk acceptance decisions, budget approval, policy approval)? How often do they review security?',
        },
        {
            'type': 'security_reporting',
            'question': 'What security metrics are reported to leadership (Security Hub findings, compliance status, incident trends, risk posture)? How frequently?',
        },
        {
            'type': 'leadership_decisions',
            'question': 'What security decisions require leadership approval (risk acceptance, major security investments, policy exceptions, incident response escalation)?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates PM-2 compliance? Provide: Leadership security briefing materials, meeting minutes, security metrics reports, leadership decision records. Where are these artifacts stored?',
        },
    ],
    'pm-3': [
        {
            'type': 'security_resources',
            'question': 'What resources are allocated to AWS security (security tools budget, security staff, training budget, incident response resources)? Are resources adequate?',
        },
        {
            'type': 'resource_planning',
            'question': 'How are security resource needs identified and planned (risk assessments, security roadmap, capacity planning)? Who approves resource allocation?',
        },
        {
            'type': 'resource_tracking',
            'question': 'How are security resources tracked (budget tracking, staff utilization, tool usage)? Are resources used effectively?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates PM-3 compliance? Provide: Security budget documentation, staffing plans, resource allocation decisions, resource utilization reports. Where are these artifacts stored?',
        },
    ],
    'pm-4': [
        {
            'type': 'action_plans',
            'question': 'Do you have action plans for AWS security improvements (POA&M, security roadmap, remediation plans)? Are plans tracked and updated?',
        },
        {
            'type': 'plan_tracking',
            'question': 'How are action plans tracked (project management tools, POA&M tracking, Security Hub custom actions)? Are milestones monitored?',
        },
        {
            'type': 'plan_reporting',
            'question': 'How often are action plan status updates provided to management (weekly, monthly, quarterly)? Are delays escalated?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates PM-4 compliance? Provide: Security action plans, POA&M status reports, milestone tracking, management status updates. Where are these artifacts stored?',
        },
    ],
    'pm-5': [
        {
            'type': 'system_inventory',
            'question': 'Do you maintain an inventory of AWS systems and services (accounts, regions, services used, data classification)? How is inventory maintained?',
        },
        {
            'type': 'inventory_automation',
            'question': 'Is inventory automated (AWS Config, Systems Manager Inventory, third-party CMDB, tagging)? How often is inventory updated?',
        },
        {
            'type': 'inventory_accuracy',
            'question': 'How is inventory accuracy verified (automated discovery, periodic reviews, reconciliation)? Are discrepancies investigated?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates PM-5 compliance? Provide: AWS system inventory, Config resource inventory, inventory update procedures, accuracy verification records. Where are these artifacts stored?',
        },
    ],
    'pm-6': [
        {
            'type': 'security_measures',
            'question': 'What security measures are implemented in AWS (encryption, access controls, monitoring, logging, incident response, vulnerability management)? Are measures documented?',
        },
        {
            'type': 'measure_effectiveness',
            'question': 'How is security measure effectiveness assessed (metrics, testing, audits, penetration tests)? Are ineffective measures improved or replaced?',
        },
        {
            'type': 'measure_review',
            'question': 'How often are security measures reviewed (annually, after incidents, continuous improvement)? Who conducts reviews?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates PM-6 compliance? Provide: Security measures documentation, effectiveness assessment reports, measure review records, improvement plans. Where are these artifacts stored?',
        },
    ],
    'pm-7': [
        {
            'type': 'insider_threat',
            'question': 'Do you have an insider threat program for AWS (user behavior monitoring, privileged access monitoring, data exfiltration detection)? What tools support this?',
        },
        {
            'type': 'threat_detection',
            'question': 'How are insider threats detected (GuardDuty, CloudTrail anomaly detection, Macie for data access, third-party UEBA)? Are alerts investigated?',
        },
        {
            'type': 'threat_response',
            'question': 'What is your response to suspected insider threats (investigation procedures, access suspension, forensics, legal involvement)? Who leads investigations?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates PM-7 compliance? Provide: Insider threat program documentation, detection tool configurations, investigation procedures, incident records (redacted). Where are these artifacts stored?',
        },
    ],
    'pm-8': [
        {
            'type': 'critical_infrastructure',
            'question': 'Have you identified critical AWS infrastructure (production accounts, critical services, data stores, authentication systems)? Is criticality documented?',
        },
        {
            'type': 'protection_measures',
            'question': 'What additional protections exist for critical infrastructure (enhanced monitoring, stricter access controls, redundancy, backup)? Are protections tested?',
        },
        {
            'type': 'criticality_review',
            'question': 'How often is infrastructure criticality reassessed (annually, after architecture changes, after incidents)? Who approves criticality designations?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates PM-8 compliance? Provide: Critical infrastructure inventory, protection measures documentation, criticality assessment records. Where are these artifacts stored?',
        },
    ],
    'pm-9': [
        {
            'type': 'risk_strategy',
            'question': 'What is your AWS risk management strategy (risk identification, assessment, mitigation, acceptance, monitoring)? Is it documented and approved?',
        },
        {
            'type': 'risk_assessment',
            'question': 'How often are AWS risks assessed (continuously, quarterly, annually, after major changes)? What methodology is used?',
        },
        {
            'type': 'risk_acceptance',
            'question': 'What is your risk acceptance process (risk register, acceptance criteria, approval authority, time limits)? Are accepted risks reviewed periodically?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates PM-9 compliance? Provide: Risk management strategy document, risk assessment reports, risk register, risk acceptance documentation. Where are these artifacts stored?',
        },
    ],
    'pm-10': [
        {
            'type': 'security_authorization',
            'question': 'What is your AWS security authorization strategy (continuous ATO, traditional ATO, risk-based authorization)? Is it documented?',
        },
        {
            'type': 'authorization_scope',
            'question': 'What is the scope of authorization (per account, per workload, entire AWS environment)? How are authorization boundaries defined?',
        },
        {
            'type': 'reauthorization',
            'question': 'How often is reauthorization required (every 3 years, after major changes, continuous authorization)? What triggers reauthorization?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates PM-10 compliance? Provide: Authorization strategy document, authorization boundaries, authorization decision letters, reauthorization schedule. Where are these artifacts stored?',
        },
    ],
    'pm-11': [
        {
            'type': 'mission_functions',
            'question': 'Have you identified mission-critical functions supported by AWS (customer-facing applications, financial systems, operational systems)? Is criticality documented?',
        },
        {
            'type': 'function_protection',
            'question': 'What protections exist for mission-critical functions (high availability, disaster recovery, enhanced monitoring, incident response priority)? Are protections tested?',
        },
        {
            'type': 'function_review',
            'question': 'How often are mission-critical functions reassessed (annually, after business changes, after incidents)? Who approves criticality designations?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates PM-11 compliance? Provide: Mission-critical functions inventory, protection measures documentation, criticality assessment records. Where are these artifacts stored?',
        },
    ],
    'pm-12': [
        {
            'type': 'insider_threat_program',
            'question': 'Do you have a comprehensive insider threat program for AWS (detection, prevention, response, deterrence)? Is it documented and resourced?',
        },
        {
            'type': 'program_components',
            'question': 'What components does your insider threat program include (user monitoring, privileged access management, data loss prevention, security awareness, incident response)?',
        },
        {
            'type': 'program_effectiveness',
            'question': 'How is insider threat program effectiveness measured (incidents detected, response time, false positive rate, user awareness)? Are metrics reviewed?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates PM-12 compliance? Provide: Insider threat program documentation, program metrics, detection tool configurations, incident response records (redacted). Where are these artifacts stored?',
        },
    ],
    'pm-13': [
        {
            'type': 'security_workforce',
            'question': 'Do you have adequate AWS security workforce (security engineers, architects, analysts, incident responders)? Are roles clearly defined?',
        },
        {
            'type': 'workforce_development',
            'question': 'How is the security workforce developed (AWS certifications, security training, conferences, hands-on labs)? Is training budget adequate?',
        },
        {
            'type': 'workforce_retention',
            'question': 'What is your strategy for retaining security talent (competitive compensation, career development, challenging work, work-life balance)? What is turnover rate?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates PM-13 compliance? Provide: Security workforce plan, role definitions, training records, certification records, retention metrics. Where are these artifacts stored?',
        },
    ],
    'pm-14': [
        {
            'type': 'testing_program',
            'question': 'Do you have a security testing program for AWS (vulnerability scanning, penetration testing, red team exercises, security assessments)? How often is testing conducted?',
        },
        {
            'type': 'testing_scope',
            'question': 'What is tested (applications, infrastructure, IAM policies, network configurations, incident response procedures)? Are all critical systems tested?',
        },
        {
            'type': 'testing_remediation',
            'question': 'How are testing findings remediated (POA&M tracking, SLA-based remediation, verification testing)? Are findings tracked to closure?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates PM-14 compliance? Provide: Security testing program documentation, testing schedule, test reports, remediation tracking, retest results. Where are these artifacts stored?',
        },
    ],
    'pm-15': [
        {
            'type': 'contacts',
            'question': 'Have you designated security contacts for AWS (security team email, incident response hotline, AWS account alternate contacts)? Are contacts documented and current?',
        },
        {
            'type': 'contact_availability',
            'question': 'Are security contacts available 24/7 for critical incidents? Is there an escalation path for after-hours incidents?',
        },
        {
            'type': 'contact_communication',
            'question': 'How are security contacts communicated (employee handbook, intranet, security awareness training, AWS account settings)? Are contacts tested periodically?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates PM-15 compliance? Provide: Security contacts documentation, AWS account contact settings, contact communication records, contact test results. Where are these artifacts stored?',
        },
    ],
    'pm-16': [
        {
            'type': 'threat_awareness',
            'question': 'How do you stay aware of AWS security threats (AWS Security Bulletins, GuardDuty findings, threat intelligence feeds, security communities)? Who monitors threats?',
        },
        {
            'type': 'threat_sharing',
            'question': 'Do you share threat information (industry ISACs, AWS security forums, peer organizations)? Do you receive threat intelligence from external sources?',
        },
        {
            'type': 'threat_response',
            'question': 'How are new threats addressed (security advisories, emergency patches, configuration changes, monitoring updates)? What is the response timeline?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates PM-16 compliance? Provide: Threat intelligence sources documentation, threat monitoring reports, threat response records, information sharing agreements. Where are these artifacts stored?',
        },
    ],
    
    # PII Processing and Transparency (PT)
    'pt-1': [
        {
            'type': 'policy_existence',
            'question': 'Do you have documented policies for PII processing in AWS (collection, use, retention, disclosure, disposal)? Does it comply with privacy regulations (GDPR, CCPA)?',
        },
        {
            'type': 'aws_pii_protection',
            'question': 'Does your policy address AWS-specific PII protection (encryption, access controls, data residency, Macie for PII discovery, data lifecycle management)?',
        },
        {
            'type': 'privacy_compliance',
            'question': 'What privacy regulations apply to your AWS PII (GDPR, CCPA, HIPAA, FERPA)? How do you ensure compliance? Are Data Processing Agreements in place with AWS?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates PT-1 compliance? Provide: PII processing policy document with approval signatures, privacy compliance documentation, AWS DPA, policy review records. Where are these artifacts stored?',
        },
    ],
    'pt-2': [
        {
            'type': 'authority_to_collect',
            'question': 'What is your legal authority to collect PII in AWS (consent, contract, legitimate interest, legal obligation)? Is authority documented for each PII type?',
        },
        {
            'type': 'collection_limitation',
            'question': 'Do you limit PII collection to what is necessary (data minimization)? How is necessity determined? Are collection practices reviewed?',
        },
        {
            'type': 'consent_management',
            'question': 'If using consent, how is it obtained and managed (consent forms, consent management platform, audit trail)? Can consent be withdrawn?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates PT-2 compliance? Provide: Legal authority documentation, data minimization assessments, consent records, collection limitation policies. Where are these artifacts stored?',
        },
    ],
    'pt-3': [
        {
            'type': 'pii_inventory',
            'question': 'Do you maintain an inventory of PII in AWS (data types, locations, purposes, retention periods)? How is inventory maintained?',
        },
        {
            'type': 'pii_discovery',
            'question': 'How do you discover PII in AWS (Macie for S3, database scanning, application inventory, data flow mapping)? Is discovery automated?',
        },
        {
            'type': 'inventory_accuracy',
            'question': 'How is PII inventory accuracy verified (periodic reviews, automated discovery, data classification validation)? Are discrepancies investigated?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates PT-3 compliance? Provide: PII inventory, Macie discovery reports, data flow diagrams, inventory update procedures. Where are these artifacts stored?',
        },
    ],
    'pt-4': [
        {
            'type': 'consent_management',
            'question': 'How do you manage consent for PII processing in AWS (consent capture, consent storage, consent withdrawal, consent audit trail)? Is consent granular?',
        },
        {
            'type': 'consent_verification',
            'question': 'How do you verify consent before processing PII (consent checks in applications, consent database, automated verification)? Are consent violations prevented?',
        },
        {
            'type': 'consent_withdrawal',
            'question': 'How can individuals withdraw consent? What happens to their PII after withdrawal (deletion, anonymization, processing cessation)? Is withdrawal honored promptly?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates PT-4 compliance? Provide: Consent management procedures, consent records, withdrawal requests and responses, consent verification logs. Where are these artifacts stored?',
        },
    ],
    'pt-5': [
        {
            'type': 'privacy_notice',
            'question': 'Do you provide privacy notices for PII collection in AWS (what PII, why collected, how used, who has access, retention period, rights)? Are notices clear and accessible?',
        },
        {
            'type': 'notice_timing',
            'question': 'When are privacy notices provided (at collection, before processing, in privacy policy)? Are notices provided in multiple languages if needed?',
        },
        {
            'type': 'notice_updates',
            'question': 'How are privacy notices updated when practices change? Are individuals notified of material changes? How is notification documented?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates PT-5 compliance? Provide: Privacy notices, notice delivery records, notice update history, user acknowledgment records. Where are these artifacts stored?',
        },
    ],
    'pt-6': [
        {
            'type': 'data_subject_rights',
            'question': 'How do individuals exercise privacy rights for AWS PII (access, correction, deletion, portability, objection)? Is there a request process?',
        },
        {
            'type': 'request_handling',
            'question': 'What is your process for handling privacy rights requests (request verification, data retrieval, response timeline, appeal process)? Are requests tracked?',
        },
        {
            'type': 'response_timeline',
            'question': 'What are your response timelines for privacy rights requests (30 days for GDPR, 45 days for CCPA)? Are timelines met? Are delays communicated?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates PT-6 compliance? Provide: Privacy rights request procedures, request tracking records, response documentation, timeline compliance reports. Where are these artifacts stored?',
        },
    ],
    'pt-7': [
        {
            'type': 'pii_redress',
            'question': 'How can individuals seek redress for PII issues (complaints, disputes, corrections)? Is there a complaint process? Who handles complaints?',
        },
        {
            'type': 'complaint_handling',
            'question': 'What is your complaint handling process (complaint receipt, investigation, resolution, response, appeal)? Are complaints tracked and analyzed?',
        },
        {
            'type': 'redress_timeline',
            'question': 'What are your timelines for complaint resolution? Are individuals kept informed of progress? Is there an escalation path?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates PT-7 compliance? Provide: Complaint handling procedures, complaint records (redacted), resolution documentation, timeline compliance reports. Where are these artifacts stored?',
        },
    ],
    'pt-8': [
        {
            'type': 'computer_matching',
            'question': 'Do you perform computer matching of PII in AWS (data matching, record linkage, data analytics)? Is matching authorized and documented?',
        },
        {
            'type': 'matching_agreements',
            'question': 'If performing computer matching, do you have matching agreements (purpose, data sources, matching criteria, retention, oversight)? Are agreements reviewed?',
        },
        {
            'type': 'matching_safeguards',
            'question': 'What safeguards protect PII during matching (access controls, encryption, audit logging, data minimization, accuracy verification)?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates PT-8 compliance? Provide: Computer matching agreements, matching procedures, safeguard documentation, matching audit logs. Where are these artifacts stored?',
        },
    ],
    
    # Supply Chain Risk Management (SR)
    'sr-1': [
        {
            'type': 'policy_existence',
            'question': 'Do you have documented supply chain risk management policies for AWS (vendor assessment, third-party risk, software supply chain, service provider oversight)? When was it last reviewed?',
        },
        {
            'type': 'aws_supply_chain',
            'question': 'Does your policy address AWS-specific supply chain risks (third-party integrations, marketplace solutions, open source dependencies, container images, Lambda layers)?',
        },
        {
            'type': 'risk_assessment',
            'question': 'How do you assess supply chain risks (vendor security assessments, dependency scanning, third-party audits, continuous monitoring)? How often?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates SR-1 compliance? Provide: Supply chain risk management policy document with approval signatures, risk assessment procedures, policy review records. Where are these artifacts stored?',
        },
    ],
    'sr-2': [
        {
            'type': 'supplier_reviews',
            'question': 'How often do you review AWS service providers and third-party vendors (annually, after security incidents, continuous monitoring)? What is reviewed?',
        },
        {
            'type': 'review_criteria',
            'question': 'What criteria are used in supplier reviews (security posture, compliance certifications, incident history, financial stability, contract compliance)?',
        },
        {
            'type': 'review_actions',
            'question': 'What actions result from supplier reviews (continued use, enhanced monitoring, contract renegotiation, supplier termination)? Who approves actions?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates SR-2 compliance? Provide: Supplier review schedule, review reports, review criteria documentation, action records. Where are these artifacts stored?',
        },
    ],
    'sr-3': [
        {
            'type': 'supply_chain_controls',
            'question': 'What supply chain security controls are required for AWS vendors (security assessments, SOC 2 reports, penetration testing, incident response capabilities)?',
        },
        {
            'type': 'control_verification',
            'question': 'How do you verify vendor security controls (audit reports, security questionnaires, on-site assessments, continuous monitoring)? How often?',
        },
        {
            'type': 'control_deficiencies',
            'question': 'How are vendor control deficiencies addressed (remediation plans, compensating controls, contract enforcement, vendor termination)? Are deficiencies tracked?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates SR-3 compliance? Provide: Vendor security requirements, SOC 2 reports, security assessment results, deficiency remediation records. Where are these artifacts stored?',
        },
    ],
    'sr-4': [
        {
            'type': 'provenance',
            'question': 'How do you verify the provenance of AWS components (container images from trusted registries, signed AMIs, verified Lambda layers, authenticated packages)?',
        },
        {
            'type': 'integrity_verification',
            'question': 'How do you verify component integrity (checksum verification, digital signatures, ECR image scanning, artifact signing)? Is verification automated?',
        },
        {
            'type': 'unauthorized_components',
            'question': 'How are unauthorized or unverified components detected and prevented (admission controllers, Config rules, automated scanning)? Are violations blocked?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates SR-4 compliance? Provide: Provenance verification procedures, integrity verification logs, ECR scanning reports, unauthorized component alerts. Where are these artifacts stored?',
        },
    ],
    'sr-5': [
        {
            'type': 'acquisition_strategies',
            'question': 'What strategies reduce supply chain risk in AWS acquisitions (multiple vendors, trusted sources, security requirements in contracts, vendor diversity)?',
        },
        {
            'type': 'vendor_diversity',
            'question': 'Do you avoid single points of failure in your AWS supply chain (multiple cloud providers, multiple SaaS vendors, alternative solutions)? Is diversity documented?',
        },
        {
            'type': 'risk_mitigation',
            'question': 'What mitigations address supply chain risks (vendor monitoring, contract terms, insurance, incident response plans, alternative vendors)?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates SR-5 compliance? Provide: Acquisition strategy documentation, vendor diversity analysis, risk mitigation plans, contract security terms. Where are these artifacts stored?',
        },
    ],
    'sr-6': [
        {
            'type': 'tamper_resistance',
            'question': 'How do you protect AWS components from tampering (code signing, artifact repositories with access controls, immutable infrastructure, integrity monitoring)?',
        },
        {
            'type': 'tamper_detection',
            'question': 'How is tampering detected (file integrity monitoring, CloudTrail for unauthorized changes, Config for drift detection, GuardDuty for malicious activity)?',
        },
        {
            'type': 'tamper_response',
            'question': 'What is your response to detected tampering (incident response, forensics, component replacement, root cause analysis)? Are incidents tracked?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates SR-6 compliance? Provide: Tamper protection mechanisms, integrity monitoring configurations, tamper detection alerts, incident response records. Where are these artifacts stored?',
        },
    ],
    'sr-7': [
        {
            'type': 'supply_chain_operations',
            'question': 'What operational security practices protect your AWS supply chain (secure development, secure deployment, access controls, monitoring, incident response)?',
        },
        {
            'type': 'operations_monitoring',
            'question': 'How are supply chain operations monitored (dependency updates, vendor security advisories, vulnerability disclosures, threat intelligence)? Who monitors?',
        },
        {
            'type': 'operations_response',
            'question': 'How do you respond to supply chain security events (vulnerability patches, vendor breaches, compromised dependencies)? What is the response timeline?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates SR-7 compliance? Provide: Supply chain operations procedures, monitoring reports, security advisory tracking, incident response records. Where are these artifacts stored?',
        },
    ],
    'sr-8': [
        {
            'type': 'notification_agreements',
            'question': 'Do you have agreements with AWS vendors for security notification (breach notification, vulnerability disclosure, security advisories, incident reporting)?',
        },
        {
            'type': 'notification_timeline',
            'question': 'What are the notification timelines in vendor agreements (immediate for breaches, 24 hours for critical vulnerabilities, weekly for advisories)? Are timelines enforced?',
        },
        {
            'type': 'notification_response',
            'question': 'How do you respond to vendor security notifications (impact assessment, remediation, communication, incident response)? Are responses tracked?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates SR-8 compliance? Provide: Vendor notification agreements, notification records, response documentation, timeline compliance reports. Where are these artifacts stored?',
        },
    ],
    'sr-9': [
        {
            'type': 'tamper_evident',
            'question': 'How do you make AWS supply chain tampering evident (audit logging, integrity monitoring, version control, change tracking, digital signatures)?',
        },
        {
            'type': 'evidence_preservation',
            'question': 'How is tampering evidence preserved (log retention, immutable logs, forensic copies, chain of custody)? How long is evidence retained?',
        },
        {
            'type': 'evidence_review',
            'question': 'How often is tampering evidence reviewed (continuous monitoring, periodic audits, after incidents)? Who reviews evidence?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates SR-9 compliance? Provide: Tamper-evident mechanisms, audit log configurations, evidence preservation procedures, review records. Where are these artifacts stored?',
        },
    ],
    'sr-10': [
        {
            'type': 'component_inspection',
            'question': 'How do you inspect AWS components for tampering (vulnerability scanning, malware scanning, code review, integrity verification, provenance checks)?',
        },
        {
            'type': 'inspection_frequency',
            'question': 'How often are components inspected (before deployment, continuously, after updates, randomly)? Is inspection automated?',
        },
        {
            'type': 'inspection_findings',
            'question': 'How are inspection findings handled (component rejection, remediation, investigation, vendor notification)? Are findings tracked?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates SR-10 compliance? Provide: Component inspection procedures, inspection reports, finding remediation records, automated scanning configurations. Where are these artifacts stored?',
        },
    ],
    'sr-11': [
        {
            'type': 'component_authenticity',
            'question': 'How do you verify AWS component authenticity (digital signatures, trusted sources, certificate validation, vendor verification)?',
        },
        {
            'type': 'authenticity_enforcement',
            'question': 'Is component authenticity verification enforced (automated checks, deployment gates, admission controllers)? Can unauthenticated components be deployed?',
        },
        {
            'type': 'authenticity_failures',
            'question': 'How are authenticity verification failures handled (deployment blocking, alerts, investigation, vendor contact)? Are failures tracked?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates SR-11 compliance? Provide: Authenticity verification procedures, verification logs, deployment gate configurations, failure records. Where are these artifacts stored?',
        },
    ],
    'sr-12': [
        {
            'type': 'component_disposal',
            'question': 'How do you dispose of AWS supply chain components (decommissioning procedures, data sanitization, license termination, vendor notification)?',
        },
        {
            'type': 'disposal_verification',
            'question': 'How is component disposal verified (deletion confirmation, data sanitization verification, license cancellation confirmation)? Is disposal documented?',
        },
        {
            'type': 'disposal_data_protection',
            'question': 'How is data protected during component disposal (encryption, sanitization, secure deletion, vendor data deletion requests)? Are data protection requirements met?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates SR-12 compliance? Provide: Component disposal procedures, disposal verification records, data sanitization logs, vendor termination confirmations. Where are these artifacts stored?',
        },
    ],
}
"""

if __name__ == "__main__":
    print("This file contains AWS-specific questions for control families:")
    print("CA, SA, PS, MA, MP, PM, PT, SR")
    print("\nTo integrate these questions into control_questions.py:")
    print("1. Open control_questions.py")
    print("2. Find the line with 'ra-5': [ (the last control before the closing brace)")
    print("3. Add the NEW_CONTROL_QUESTIONS content before the closing brace of CONTROL_QUESTIONS")
    print("4. Save and test")
