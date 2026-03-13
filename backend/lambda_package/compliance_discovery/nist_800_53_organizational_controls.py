"""Organizational (non-AWS) control requirements for NIST 800-53 Rev 5.

Each control requires both technical AWS controls AND organizational controls
(policies, procedures, training, governance). This module defines the
non-technical requirements that complement the AWS Implementation Guide.

Categories:
- POLICY: Written policies, standards, and procedures
- PROCESS: Defined processes and workflows
- GOVERNANCE: Leadership oversight, roles, and accountability
- TRAINING: Awareness, education, and competency programs
- DOCUMENTATION: Records, evidence, and audit artifacts
- THIRD_PARTY: Vendor management and external relationships
"""

from typing import Dict, List

NIST_800_53_ORG_REQUIREMENTS: Dict[str, List[Dict[str, str]]] = {

    # =========================================================================
    # AC — Access Control
    # =========================================================================
    "AC-1": [
        {"category": "POLICY", "title": "Access control policy",
         "description": "Maintain a documented access control policy defining authorized users, approval processes, and conditions for access revocation. Review at least annually."},
        {"category": "GOVERNANCE", "title": "Policy ownership",
         "description": "Assign an owner responsible for maintaining and updating the access control policy. Ensure leadership approves the policy."},
    ],
    "AC-2": [
        {"category": "PROCESS", "title": "Account lifecycle management",
         "description": "Define formal processes for requesting, approving, provisioning, reviewing, and revoking user accounts — including timelines for each step."},
        {"category": "PROCESS", "title": "Periodic access reviews",
         "description": "Conduct access reviews at least quarterly for privileged accounts and annually for standard accounts. Document review findings and remediation actions."},
    ],
    "AC-3": [
        {"category": "DOCUMENTATION", "title": "Access control matrix",
         "description": "Maintain a role-based access control matrix documenting which roles can access which resources and what actions they can perform."},
    ],
    "AC-4": [
        {"category": "DOCUMENTATION", "title": "Data flow diagrams",
         "description": "Maintain data flow diagrams showing approved information flow paths between security domains, systems, and external entities."},
        {"category": "POLICY", "title": "Information flow policy",
         "description": "Define approved channels for data transmission and prohibit unauthorized channels (personal email, unapproved cloud storage)."},
    ],
    "AC-5": [
        {"category": "DOCUMENTATION", "title": "Separation of duties matrix",
         "description": "Document which duties are incompatible and must be performed by different individuals. Review when roles change."},
    ],
    "AC-6": [
        {"category": "POLICY", "title": "Least privilege policy",
         "description": "Require least privilege as organizational policy. Define requirements for periodic permission reviews and removal of unnecessary access."},
        {"category": "PROCESS", "title": "Privileged account management",
         "description": "Define procedures for managing privileged accounts — approval, monitoring, periodic review, and emergency access (break-glass)."},
    ],
    "AC-7": [
        {"category": "POLICY", "title": "Account lockout policy",
         "description": "Document lockout thresholds, lockout duration, and unlock procedures."},
    ],
    "AC-8": [
        {"category": "POLICY", "title": "System use notification",
         "description": "Define required banner content including authorized use, monitoring consent, and legal warnings. Apply to all login screens."},
    ],
    "AC-11": [
        {"category": "POLICY", "title": "Session lock policy",
         "description": "Define inactivity timeout periods and require pattern-hiding displays that conceal sensitive content."},
    ],
    "AC-12": [
        {"category": "POLICY", "title": "Session termination policy",
         "description": "Define conditions for automatic session termination (inactivity, end of day, token expiration)."},
    ],
    "AC-14": [
        {"category": "DOCUMENTATION", "title": "Permitted unauthenticated actions",
         "description": "Document any actions permitted without authentication and justify why each is necessary."},
    ],
    "AC-17": [
        {"category": "POLICY", "title": "Remote access policy",
         "description": "Document approved remote access methods, MFA requirements, encryption standards, and monitoring procedures."},
        {"category": "PROCESS", "title": "Remote access authorization",
         "description": "Define the approval process for granting remote access and conditions for revocation."},
    ],
    "AC-18": [
        {"category": "POLICY", "title": "Wireless access policy",
         "description": "Define wireless security standards, authorization requirements, and separation of CUI-accessible wireless from guest networks."},
    ],
    "AC-19": [
        {"category": "POLICY", "title": "Mobile device policy",
         "description": "Define permitted devices, required security configurations (encryption, screen lock, remote wipe), and MDM enrollment requirements."},
    ],
    "AC-20": [
        {"category": "POLICY", "title": "External system connections",
         "description": "Require security agreements before connecting to external systems. Define security requirements external systems must meet."},
        {"category": "PROCESS", "title": "External connection review",
         "description": "Periodically review all external connections to verify they are still needed and agreements are current."},
    ],
    "AC-21": [
        {"category": "POLICY", "title": "Information sharing policy",
         "description": "Define what information can be shared, with whom, through what channels, and what approvals are required."},
    ],
    "AC-22": [
        {"category": "POLICY", "title": "Public content controls",
         "description": "Prohibit posting sensitive information on public systems. Define a review and approval process before publishing."},
    ],

    # =========================================================================
    # AT — Awareness and Training
    # =========================================================================
    "AT-1": [
        {"category": "POLICY", "title": "Training policy",
         "description": "Define training requirements including topics, frequency, target audiences, and completion tracking. Review annually."},
        {"category": "GOVERNANCE", "title": "Training program ownership",
         "description": "Assign responsibility for maintaining the training program and ensuring content stays current with evolving threats."},
    ],
    "AT-2": [
        {"category": "TRAINING", "title": "Security awareness program",
         "description": "Deliver security awareness training to all personnel covering phishing, social engineering, password security, and data handling. Refresh annually."},
        {"category": "DOCUMENTATION", "title": "Training completion records",
         "description": "Track completion by individual with dates and scores. Follow up on non-completions."},
    ],
    "AT-3": [
        {"category": "TRAINING", "title": "Role-based security training",
         "description": "Provide specialized training for personnel in security roles — system admins, developers, incident responders — covering their specific duties."},
    ],
    "AT-4": [
        {"category": "DOCUMENTATION", "title": "Training records management",
         "description": "Maintain training records for the required retention period. Track individual completion, scores, and certification status."},
    ],

    # =========================================================================
    # AU — Audit and Accountability
    # =========================================================================
    "AU-1": [
        {"category": "POLICY", "title": "Audit and accountability policy",
         "description": "Define which events must be logged, retention periods, log protection requirements, and review procedures."},
    ],
    "AU-2": [
        {"category": "DOCUMENTATION", "title": "Auditable events list",
         "description": "Maintain a documented list of events that must be captured (logins, privilege use, config changes, data access, failures). Review when systems change."},
    ],
    "AU-3": [
        {"category": "POLICY", "title": "Audit record content requirements",
         "description": "Define minimum content for audit records: who, what, when, where, and outcome."},
    ],
    "AU-4": [
        {"category": "PROCESS", "title": "Log storage management",
         "description": "Monitor log storage capacity and define procedures for archiving or expanding storage before capacity is exhausted."},
    ],
    "AU-5": [
        {"category": "PROCESS", "title": "Logging failure response",
         "description": "Define escalation procedures when audit logging fails — who is notified, what actions are taken, and how quickly logging must be restored."},
    ],
    "AU-6": [
        {"category": "PROCESS", "title": "Log review process",
         "description": "Define who reviews logs, how often, what they look for, and how findings are escalated. Document review activities."},
    ],
    "AU-7": [
        {"category": "PROCESS", "title": "Audit reporting capability",
         "description": "Ensure the ability to generate on-demand audit reports for investigations, compliance reviews, and management reporting."},
    ],
    "AU-8": [
        {"category": "POLICY", "title": "Time synchronization policy",
         "description": "Require all systems to synchronize to an authoritative time source. Define acceptable drift tolerances."},
    ],
    "AU-9": [
        {"category": "POLICY", "title": "Audit log protection",
         "description": "Define who can access, modify, or delete audit logs. Require immutable storage and separate access controls for log infrastructure."},
        {"category": "GOVERNANCE", "title": "Log access separation",
         "description": "Ensure the team managing audit logs is separate from the teams whose activities are being logged."},
    ],
    "AU-11": [
        {"category": "POLICY", "title": "Audit record retention",
         "description": "Define retention periods by log type that meet regulatory requirements. Ensure logs are accessible for the full retention period."},
    ],
    "AU-12": [
        {"category": "PROCESS", "title": "Audit generation management",
         "description": "Ensure new systems and services get logging configured as part of the deployment process. Verify logging coverage periodically."},
    ],

    # =========================================================================
    # CA — Security Assessment and Authorization
    # =========================================================================
    "CA-1": [
        {"category": "POLICY", "title": "Assessment and authorization policy",
         "description": "Define procedures for conducting assessments, managing POA&Ms, and granting authorization to operate."},
    ],
    "CA-2": [
        {"category": "PROCESS", "title": "Security assessment process",
         "description": "Define assessment methodology, frequency, scope, and assessor qualifications. Document assessment plans and results."},
    ],
    "CA-3": [
        {"category": "DOCUMENTATION", "title": "System interconnection agreements",
         "description": "Maintain interconnection security agreements (ISAs) or MOUs for all system connections with external organizations."},
    ],
    "CA-5": [
        {"category": "DOCUMENTATION", "title": "Plan of Action and Milestones",
         "description": "Maintain a POA&M tracking all security deficiencies with owners, target dates, milestones, and status. Review regularly."},
        {"category": "GOVERNANCE", "title": "POA&M oversight",
         "description": "Assign management oversight for POA&M items. Establish escalation for overdue items."},
    ],
    "CA-6": [
        {"category": "GOVERNANCE", "title": "Authorization to Operate",
         "description": "Obtain formal authorization from the authorizing official before operating the system. Document authorization boundary and conditions."},
    ],
    "CA-7": [
        {"category": "PROCESS", "title": "Continuous monitoring strategy",
         "description": "Define what is monitored, how often, by whom, and how findings are reported and acted upon."},
    ],
    "CA-9": [
        {"category": "DOCUMENTATION", "title": "Internal system connections",
         "description": "Document all internal system connections with security requirements and approval records."},
    ],

    # =========================================================================
    # CM — Configuration Management
    # =========================================================================
    "CM-1": [
        {"category": "POLICY", "title": "Configuration management policy",
         "description": "Define procedures for baseline management, change control, and configuration monitoring."},
    ],
    "CM-2": [
        {"category": "DOCUMENTATION", "title": "Baseline configuration documentation",
         "description": "Document baseline configurations for all system types. Update when significant changes occur."},
    ],
    "CM-3": [
        {"category": "PROCESS", "title": "Change management process",
         "description": "Define formal change management with request, review, approval, implementation, and verification steps."},
        {"category": "DOCUMENTATION", "title": "Change log",
         "description": "Maintain a log of all changes including who requested, who approved, what changed, and when."},
    ],
    "CM-4": [
        {"category": "PROCESS", "title": "Security impact analysis",
         "description": "Require security impact analysis before implementing changes. Document the analysis and mitigations."},
    ],
    "CM-5": [
        {"category": "POLICY", "title": "Change access restrictions",
         "description": "Define who is authorized to make changes to production systems and require approval workflows."},
    ],
    "CM-6": [
        {"category": "POLICY", "title": "Security configuration standards",
         "description": "Adopt configuration standards (CIS Benchmarks, STIGs) for all system types. Document deviations with justification."},
    ],
    "CM-7": [
        {"category": "DOCUMENTATION", "title": "Approved services and ports",
         "description": "Maintain a list of approved services, ports, and protocols. Require justification for exceptions."},
    ],
    "CM-8": [
        {"category": "PROCESS", "title": "System inventory management",
         "description": "Define how the inventory is maintained, reconciled, and updated when assets are added or decommissioned."},
    ],
    "CM-9": [
        {"category": "DOCUMENTATION", "title": "Configuration management plan",
         "description": "Document roles, responsibilities, and processes for managing system configurations throughout the lifecycle."},
    ],
    "CM-10": [
        {"category": "POLICY", "title": "Software usage restrictions",
         "description": "Define software licensing compliance requirements and track license usage."},
    ],
    "CM-11": [
        {"category": "POLICY", "title": "User-installed software policy",
         "description": "Define what software users can install, what requires approval, and what is prohibited."},
    ],
    "CM-12": [
        {"category": "DOCUMENTATION", "title": "Information location tracking",
         "description": "Maintain an inventory of where sensitive data resides across all systems and storage services."},
    ],

    # =========================================================================
    # CP — Contingency Planning
    # =========================================================================
    "CP-1": [
        {"category": "POLICY", "title": "Contingency planning policy",
         "description": "Define procedures for backup, recovery, and business continuity. Address cloud-specific recovery scenarios."},
    ],
    "CP-2": [
        {"category": "DOCUMENTATION", "title": "Contingency plan",
         "description": "Maintain a contingency plan with recovery procedures, RTOs/RPOs, contact lists, and escalation procedures. Review annually."},
    ],
    "CP-3": [
        {"category": "TRAINING", "title": "Contingency training",
         "description": "Train personnel with recovery responsibilities on their roles. Include cloud-specific recovery procedures."},
    ],
    "CP-4": [
        {"category": "PROCESS", "title": "Contingency plan testing",
         "description": "Test the contingency plan at least annually. Document results, lessons learned, and plan updates."},
    ],
    "CP-6": [
        {"category": "DOCUMENTATION", "title": "Alternate storage site",
         "description": "Document the alternate storage location, geographic separation, and security controls at the alternate site."},
    ],
    "CP-7": [
        {"category": "DOCUMENTATION", "title": "Alternate processing site",
         "description": "Document the DR site architecture, failover procedures, and RTO/RPO validation results."},
    ],
    "CP-8": [
        {"category": "DOCUMENTATION", "title": "Telecommunications redundancy",
         "description": "Document redundant network connectivity and failover procedures."},
    ],
    "CP-9": [
        {"category": "PROCESS", "title": "Backup procedures",
         "description": "Define backup schedules, retention periods, encryption requirements, and restoration testing frequency."},
    ],
    "CP-10": [
        {"category": "PROCESS", "title": "Recovery procedures",
         "description": "Document step-by-step recovery procedures and post-recovery verification checklists."},
    ],

    # =========================================================================
    # IA — Identification and Authentication
    # =========================================================================
    "IA-1": [
        {"category": "POLICY", "title": "Identification and authentication policy",
         "description": "Define authentication methods, MFA requirements, credential management, and password standards."},
    ],
    "IA-2": [
        {"category": "POLICY", "title": "MFA requirements",
         "description": "Require MFA for all privileged and network access. Specify approved MFA types."},
    ],
    "IA-3": [
        {"category": "POLICY", "title": "Device authentication policy",
         "description": "Define how devices are identified and authenticated before network access."},
    ],
    "IA-4": [
        {"category": "PROCESS", "title": "Identifier lifecycle management",
         "description": "Define procedures for creating, assigning, deactivating, and preventing reuse of identifiers."},
    ],
    "IA-5": [
        {"category": "POLICY", "title": "Password and credential policy",
         "description": "Define password complexity, history, expiration, and secure storage requirements. Address service account credentials."},
    ],
    "IA-6": [
        {"category": "POLICY", "title": "Authentication feedback policy",
         "description": "Require password masking and generic error messages that don't reveal which credential was incorrect."},
    ],
    "IA-7": [
        {"category": "DOCUMENTATION", "title": "Cryptographic module inventory",
         "description": "Maintain an inventory of cryptographic modules used for authentication with their FIPS validation status."},
    ],
    "IA-8": [
        {"category": "POLICY", "title": "External user authentication",
         "description": "Define authentication requirements for non-organizational users (contractors, partners, customers)."},
    ],
    "IA-11": [
        {"category": "POLICY", "title": "Re-authentication policy",
         "description": "Define when users must re-authenticate — sensitive actions, inactivity, security domain changes."},
    ],
    "IA-12": [
        {"category": "PROCESS", "title": "Identity proofing procedures",
         "description": "Define how identities are verified before issuing credentials — government ID, in-person verification, enhanced checks for privileged access."},
    ],

    # =========================================================================
    # IR — Incident Response
    # =========================================================================
    "IR-1": [
        {"category": "POLICY", "title": "Incident response policy",
         "description": "Define IR procedures covering detection, analysis, containment, eradication, and recovery. Address cloud-specific incidents."},
        {"category": "GOVERNANCE", "title": "IR team designation",
         "description": "Formally designate an IR team with defined roles, authority levels, and on-call responsibilities."},
    ],
    "IR-2": [
        {"category": "TRAINING", "title": "IR training program",
         "description": "Train IR team members on their responsibilities including cloud-specific scenarios. Refresh when the plan changes."},
    ],
    "IR-3": [
        {"category": "PROCESS", "title": "IR testing program",
         "description": "Test IR capabilities at least annually through tabletop exercises or simulations. Document results and plan updates."},
    ],
    "IR-4": [
        {"category": "PROCESS", "title": "Incident handling procedures",
         "description": "Define step-by-step runbooks for common incident types. Include escalation criteria and communication templates."},
    ],
    "IR-5": [
        {"category": "PROCESS", "title": "Incident tracking",
         "description": "Define how incidents are tracked from detection through resolution. Maintain metrics (MTTD, MTTR)."},
    ],
    "IR-6": [
        {"category": "PROCESS", "title": "Incident reporting procedures",
         "description": "Define reporting timelines, recipients (management, regulators, law enforcement), and templates."},
    ],
    "IR-7": [
        {"category": "DOCUMENTATION", "title": "IR assistance resources",
         "description": "Document available assistance resources — AWS Support tier, third-party IR retainers, legal counsel contacts."},
    ],
    "IR-8": [
        {"category": "PROCESS", "title": "IR plan maintenance",
         "description": "Review and update the IR plan after incidents, exercises, and organizational changes. Distribute updates to all IR personnel."},
    ],

    # =========================================================================
    # MA — Maintenance
    # =========================================================================
    "MA-1": [
        {"category": "POLICY", "title": "Maintenance policy",
         "description": "Define maintenance procedures, schedules, tool controls, and personnel requirements."},
    ],
    "MA-2": [
        {"category": "PROCESS", "title": "Maintenance scheduling",
         "description": "Define maintenance schedules, communication procedures, and documentation requirements for all maintenance activities."},
    ],
    "MA-3": [
        {"category": "POLICY", "title": "Maintenance tools policy",
         "description": "Define approved maintenance tools, integrity verification requirements, and usage restrictions."},
    ],
    "MA-4": [
        {"category": "POLICY", "title": "Remote maintenance policy",
         "description": "Require MFA and encryption for remote maintenance. Mandate session termination when complete."},
    ],
    "MA-5": [
        {"category": "PROCESS", "title": "Maintenance personnel authorization",
         "description": "Define authorization requirements and supervision procedures for maintenance personnel."},
    ],
    "MA-6": [
        {"category": "PROCESS", "title": "Timely maintenance",
         "description": "Define timelines for obtaining replacement parts and completing maintenance to minimize system downtime."},
    ],

    # =========================================================================
    # MP — Media Protection
    # =========================================================================
    "MP-1": [
        {"category": "POLICY", "title": "Media protection policy",
         "description": "Define requirements for media handling, storage, transport, sanitization, and disposal."},
    ],
    "MP-2": [
        {"category": "PROCESS", "title": "Media access authorization",
         "description": "Define who can access media containing sensitive data and maintain access logs."},
    ],
    "MP-3": [
        {"category": "POLICY", "title": "Media marking requirements",
         "description": "Define marking requirements for media containing sensitive data — banners, labels, metadata tags."},
    ],
    "MP-4": [
        {"category": "POLICY", "title": "Media storage requirements",
         "description": "Define physical and logical storage requirements for media containing sensitive data."},
    ],
    "MP-5": [
        {"category": "PROCESS", "title": "Media transport accountability",
         "description": "Define chain-of-custody procedures for media transported outside controlled areas."},
    ],
    "MP-6": [
        {"category": "PROCESS", "title": "Media sanitization procedures",
         "description": "Define sanitization methods per NIST SP 800-88 for each media type. Maintain sanitization records."},
    ],
    "MP-7": [
        {"category": "POLICY", "title": "Removable media restrictions",
         "description": "Define restrictions on removable media use, approved devices, and exception procedures."},
    ],
    "MP-8": [
        {"category": "POLICY", "title": "Media downgrading policy",
         "description": "Define procedures for downgrading media from higher to lower classification levels."},
    ],

    # =========================================================================
    # PE — Physical and Environmental Protection
    # =========================================================================
    "PE-1": [
        {"category": "POLICY", "title": "Physical security policy",
         "description": "Acknowledge AWS shared responsibility for data center security. Define physical security for on-premises and remote work."},
    ],
    "PE-4": [
        {"category": "DOCUMENTATION", "title": "Transmission line protection",
         "description": "Document physical protection for network cabling and Direct Connect connections."},
    ],
    "PE-17": [
        {"category": "POLICY", "title": "Remote work security policy",
         "description": "Define security requirements for remote access — VPN, MFA, endpoint security, private workspace."},
        {"category": "DOCUMENTATION", "title": "Telework agreements",
         "description": "Require signed telework agreements acknowledging security responsibilities."},
    ],

    # =========================================================================
    # PL — Planning
    # =========================================================================
    "PL-1": [
        {"category": "POLICY", "title": "Security planning policy",
         "description": "Define procedures for developing and maintaining system security plans."},
    ],
    "PL-2": [
        {"category": "DOCUMENTATION", "title": "System Security Plan",
         "description": "Maintain an SSP covering system boundaries, environment, security controls, and connections. Update when changes occur."},
    ],
    "PL-4": [
        {"category": "DOCUMENTATION", "title": "Rules of behavior",
         "description": "Require signed acknowledgment of acceptable use rules from all users before granting access."},
    ],
    "PL-8": [
        {"category": "DOCUMENTATION", "title": "Security architecture",
         "description": "Document the security architecture showing defense-in-depth, multi-account strategy, and network segmentation."},
    ],
    "PL-10": [
        {"category": "DOCUMENTATION", "title": "Baseline selection rationale",
         "description": "Document which control baseline was selected and the rationale for the choice."},
    ],
    "PL-11": [
        {"category": "DOCUMENTATION", "title": "Baseline tailoring rationale",
         "description": "Document rationale for each control scoped out, compensated, or supplemented from the baseline."},
    ],

    # =========================================================================
    # PM — Program Management
    # =========================================================================
    "PM-1": [
        {"category": "GOVERNANCE", "title": "Security program plan",
         "description": "Maintain an information security program plan with governance structure, metrics, and KPIs."},
    ],
    "PM-2": [
        {"category": "GOVERNANCE", "title": "Senior security officer",
         "description": "Designate a senior official (CISO) responsible for the information security program."},
    ],
    "PM-3": [
        {"category": "GOVERNANCE", "title": "Security resources",
         "description": "Ensure adequate budget, staffing, and tooling for the security program. Include in capital planning."},
    ],
    "PM-4": [
        {"category": "PROCESS", "title": "POA&M process",
         "description": "Define the organization-wide process for creating, tracking, and closing POA&M items."},
    ],
    "PM-5": [
        {"category": "DOCUMENTATION", "title": "System inventory",
         "description": "Maintain an inventory of all organizational systems including boundaries, owners, and authorization status."},
    ],
    "PM-6": [
        {"category": "PROCESS", "title": "Security metrics",
         "description": "Define and collect security metrics to measure program effectiveness and report to leadership."},
    ],
    "PM-7": [
        {"category": "DOCUMENTATION", "title": "Enterprise architecture",
         "description": "Integrate security into the enterprise architecture. Document security considerations in architecture decisions."},
    ],
    "PM-8": [
        {"category": "DOCUMENTATION", "title": "Critical infrastructure plan",
         "description": "Document how the organization protects critical infrastructure components."},
    ],
    "PM-9": [
        {"category": "PROCESS", "title": "Risk management strategy",
         "description": "Define the organizational risk management strategy including risk tolerance, assessment methodology, and response procedures."},
    ],
    "PM-10": [
        {"category": "GOVERNANCE", "title": "Authorization process",
         "description": "Define the process for authorizing systems to operate, including roles, criteria, and ongoing monitoring."},
    ],
    "PM-11": [
        {"category": "PROCESS", "title": "Mission/business process definition",
         "description": "Define mission and business processes and identify the security requirements for each."},
    ],
    "PM-12": [
        {"category": "PROCESS", "title": "Insider threat program",
         "description": "Establish an insider threat program with detection, reporting, and response procedures."},
    ],
    "PM-13": [
        {"category": "PROCESS", "title": "Security workforce",
         "description": "Define security workforce requirements, training, and professional development programs."},
    ],
    "PM-14": [
        {"category": "PROCESS", "title": "Testing and evaluation",
         "description": "Define the organization-wide approach to security testing, evaluation, and continuous improvement."},
    ],
    "PM-15": [
        {"category": "PROCESS", "title": "Security groups and associations",
         "description": "Participate in security groups, forums, and information sharing organizations to stay current on threats."},
    ],
    "PM-16": [
        {"category": "PROCESS", "title": "Threat awareness program",
         "description": "Establish a threat awareness program that monitors threat intelligence and communicates relevant threats to stakeholders."},
    ],

    # =========================================================================
    # PS — Personnel Security
    # =========================================================================
    "PS-1": [
        {"category": "POLICY", "title": "Personnel security policy",
         "description": "Define screening requirements, access conditions, and procedures for terminations and transfers."},
    ],
    "PS-2": [
        {"category": "PROCESS", "title": "Position risk designation",
         "description": "Assign risk designations to positions based on access to sensitive data and systems. Screen accordingly."},
    ],
    "PS-3": [
        {"category": "PROCESS", "title": "Personnel screening",
         "description": "Conduct background checks before granting access. Define re-screening frequency for high-risk positions."},
    ],
    "PS-4": [
        {"category": "PROCESS", "title": "Personnel termination",
         "description": "Define offboarding procedures — access revocation timelines, equipment return, exit interviews, knowledge transfer."},
    ],
    "PS-5": [
        {"category": "PROCESS", "title": "Personnel transfer",
         "description": "Review and adjust access when personnel transfer to new roles. Remove access no longer needed."},
    ],
    "PS-6": [
        {"category": "DOCUMENTATION", "title": "Access agreements",
         "description": "Require signed access agreements (NDAs, acceptable use) before granting access to sensitive systems."},
    ],
    "PS-7": [
        {"category": "POLICY", "title": "Third-party personnel security",
         "description": "Define security requirements for contractors and third-party personnel with system access."},
    ],
    "PS-8": [
        {"category": "PROCESS", "title": "Personnel sanctions",
         "description": "Define sanctions for personnel who violate security policies. Document and enforce consistently."},
    ],
    "PS-9": [
        {"category": "PROCESS", "title": "Position descriptions",
         "description": "Include security responsibilities in position descriptions for roles with access to sensitive systems."},
    ],

    # =========================================================================
    # PT — PII Processing and Transparency
    # =========================================================================
    "PT-1": [
        {"category": "POLICY", "title": "PII processing policy",
         "description": "Define how PII is collected, processed, stored, and shared. Address consent, purpose limitation, and data minimization."},
    ],
    "PT-2": [
        {"category": "GOVERNANCE", "title": "Authority to process PII",
         "description": "Document the legal authority for processing PII and ensure processing is limited to authorized purposes."},
    ],
    "PT-3": [
        {"category": "POLICY", "title": "PII processing purposes",
         "description": "Document and limit PII processing to specific, documented purposes. Obtain consent where required."},
    ],
    "PT-4": [
        {"category": "PROCESS", "title": "Consent management",
         "description": "Implement consent collection, tracking, and withdrawal mechanisms for PII processing."},
    ],
    "PT-5": [
        {"category": "DOCUMENTATION", "title": "Privacy notices",
         "description": "Provide clear privacy notices explaining what PII is collected, how it's used, and individual rights."},
    ],
    "PT-6": [
        {"category": "DOCUMENTATION", "title": "System of records notices",
         "description": "Maintain system of records notices (SORNs) for systems processing PII as required by applicable regulations."},
    ],
    "PT-7": [
        {"category": "PROCESS", "title": "PII data quality",
         "description": "Implement processes to ensure PII accuracy, completeness, and timeliness. Allow individuals to correct their data."},
    ],
    "PT-8": [
        {"category": "DOCUMENTATION", "title": "Computer matching agreements",
         "description": "Document agreements for computer matching programs involving PII as required by applicable regulations."},
    ],

    # =========================================================================
    # RA — Risk Assessment
    # =========================================================================
    "RA-1": [
        {"category": "POLICY", "title": "Risk assessment policy",
         "description": "Define risk assessment methodology, frequency, scope, and roles."},
    ],
    "RA-2": [
        {"category": "DOCUMENTATION", "title": "Security categorization",
         "description": "Document system and data categorization with impact levels. Apply categorization to resource tagging."},
    ],
    "RA-3": [
        {"category": "DOCUMENTATION", "title": "Risk register",
         "description": "Maintain a risk register with identified risks, likelihood, impact, ratings, and response decisions. Update at least annually."},
    ],
    "RA-5": [
        {"category": "PROCESS", "title": "Vulnerability management program",
         "description": "Define scanning frequency, scope, tools, and remediation timelines by severity."},
    ],
    "RA-7": [
        {"category": "PROCESS", "title": "Risk response process",
         "description": "Define criteria and approval authority for risk response decisions (accept, mitigate, transfer, avoid)."},
    ],
    "RA-9": [
        {"category": "DOCUMENTATION", "title": "Criticality analysis",
         "description": "Identify mission-critical systems and document business impact if they are compromised or unavailable."},
    ],

    # =========================================================================
    # SA — System and Services Acquisition
    # =========================================================================
    "SA-1": [
        {"category": "POLICY", "title": "Acquisition policy",
         "description": "Define security requirements for system and service acquisitions. Include vendor assessment procedures."},
    ],
    "SA-2": [
        {"category": "GOVERNANCE", "title": "Security resource allocation",
         "description": "Include security resources in capital planning and investment decisions."},
    ],
    "SA-3": [
        {"category": "PROCESS", "title": "Secure development lifecycle",
         "description": "Integrate security into the SDLC — threat modeling, secure coding, security testing, code review."},
    ],
    "SA-4": [
        {"category": "PROCESS", "title": "Acquisition security requirements",
         "description": "Include security requirements in contracts. Evaluate vendor security posture before procurement."},
    ],
    "SA-5": [
        {"category": "DOCUMENTATION", "title": "System documentation",
         "description": "Maintain administrator and user documentation for all systems. Include security configuration guidance."},
    ],
    "SA-8": [
        {"category": "POLICY", "title": "Security engineering principles",
         "description": "Apply security engineering principles (defense-in-depth, least privilege, fail-secure) in system design."},
    ],
    "SA-9": [
        {"category": "THIRD_PARTY", "title": "External service provider management",
         "description": "Maintain an inventory of external providers. Require SOC 2 or equivalent reports. Review security posture periodically."},
    ],
    "SA-10": [
        {"category": "PROCESS", "title": "Developer configuration management",
         "description": "Require configuration management for development environments — version control, branch protection, environment separation."},
    ],
    "SA-11": [
        {"category": "PROCESS", "title": "Developer security testing",
         "description": "Require security testing in the development pipeline — SAST, DAST, dependency scanning, penetration testing."},
    ],
    "SA-15": [
        {"category": "PROCESS", "title": "Development process standards",
         "description": "Define development process standards including secure coding guidelines, code review requirements, and testing criteria."},
    ],
    "SA-16": [
        {"category": "TRAINING", "title": "Developer security training",
         "description": "Provide security training for developers covering secure coding, common vulnerabilities, and secure configuration."},
    ],
    "SA-17": [
        {"category": "DOCUMENTATION", "title": "Security architecture documentation",
         "description": "Document security architecture and design decisions. Include threat models and Well-Architected reviews."},
    ],
    "SA-22": [
        {"category": "PROCESS", "title": "Unsupported system components",
         "description": "Track end-of-life dates for all components. Define procedures for replacing or mitigating unsupported components."},
    ],

    # =========================================================================
    # SC — System and Communications Protection
    # =========================================================================
    "SC-1": [
        {"category": "POLICY", "title": "System and communications protection policy",
         "description": "Define boundary protection, encryption standards, and network security requirements."},
    ],
    "SC-7": [
        {"category": "DOCUMENTATION", "title": "Boundary protection architecture",
         "description": "Document network boundaries, security zones, and traffic flow rules. Update when architecture changes."},
    ],
    "SC-8": [
        {"category": "POLICY", "title": "Transmission confidentiality policy",
         "description": "Require TLS 1.2+ for all data in transit. Define minimum cipher suites and certificate management."},
    ],
    "SC-12": [
        {"category": "PROCESS", "title": "Key management procedures",
         "description": "Define key lifecycle procedures — generation, distribution, storage, rotation, revocation, destruction."},
    ],
    "SC-13": [
        {"category": "POLICY", "title": "FIPS cryptography requirement",
         "description": "Require FIPS 140-2 validated modules. Maintain a cryptographic module inventory with validation status."},
    ],
    "SC-28": [
        {"category": "POLICY", "title": "Encryption at rest policy",
         "description": "Require encryption at rest for all sensitive data storage. Define minimum encryption standards and key management."},
    ],

    # =========================================================================
    # SI — System and Information Integrity
    # =========================================================================
    "SI-1": [
        {"category": "POLICY", "title": "System integrity policy",
         "description": "Define flaw remediation, malware protection, and security monitoring requirements."},
    ],
    "SI-2": [
        {"category": "PROCESS", "title": "Flaw remediation process",
         "description": "Define patch management timelines by severity, testing requirements, and tracking procedures."},
    ],
    "SI-3": [
        {"category": "POLICY", "title": "Malware protection policy",
         "description": "Require antivirus/anti-malware on all endpoints. Define update frequency, scan schedules, and response procedures."},
    ],
    "SI-4": [
        {"category": "PROCESS", "title": "System monitoring program",
         "description": "Define what is monitored, alerting thresholds, and escalation procedures for detected anomalies."},
        {"category": "GOVERNANCE", "title": "Monitoring oversight",
         "description": "Assign responsibility for monitoring operations and periodic review of monitoring effectiveness."},
    ],
    "SI-5": [
        {"category": "PROCESS", "title": "Security advisory monitoring",
         "description": "Define which alert sources to monitor, who reviews them, and the process for evaluating and responding."},
    ],
    "SI-6": [
        {"category": "PROCESS", "title": "Security function verification",
         "description": "Periodically verify that security functions (encryption, logging, access controls) are operating correctly."},
    ],
    "SI-7": [
        {"category": "PROCESS", "title": "Integrity monitoring",
         "description": "Implement file integrity monitoring and configuration drift detection for critical systems."},
    ],
    "SI-8": [
        {"category": "POLICY", "title": "Spam and email security",
         "description": "Define email security requirements including SPF, DKIM, DMARC, and spam filtering."},
    ],
    "SI-10": [
        {"category": "POLICY", "title": "Input validation standards",
         "description": "Require input validation in all applications to prevent injection attacks."},
    ],
    "SI-11": [
        {"category": "POLICY", "title": "Error handling standards",
         "description": "Require generic error messages to users while logging detailed errors internally."},
    ],
    "SI-12": [
        {"category": "POLICY", "title": "Data retention and disposal",
         "description": "Define retention periods by data type and secure deletion procedures when retention expires."},
    ],
    "SI-16": [
        {"category": "POLICY", "title": "Memory protection requirements",
         "description": "Require memory protection mechanisms (ASLR, DEP/NX) on all systems processing sensitive data."},
    ],

    # =========================================================================
    # SR — Supply Chain Risk Management
    # =========================================================================
    "SR-1": [
        {"category": "POLICY", "title": "Supply chain risk management policy",
         "description": "Define procedures for assessing and monitoring supplier security. Address cloud marketplace and open-source risks."},
    ],
    "SR-2": [
        {"category": "DOCUMENTATION", "title": "Supply chain risk management plan",
         "description": "Document the supply chain risk management strategy, supplier criticality assessments, and monitoring procedures."},
    ],
    "SR-3": [
        {"category": "PROCESS", "title": "Supply chain controls",
         "description": "Define security controls required from suppliers. Include in contracts and verify compliance."},
    ],
    "SR-5": [
        {"category": "PROCESS", "title": "Component authenticity verification",
         "description": "Verify authenticity of software and hardware components before deployment. Check signatures and provenance."},
    ],
    "SR-6": [
        {"category": "THIRD_PARTY", "title": "Supplier assessments",
         "description": "Conduct security assessments of suppliers. Require SOC 2 or equivalent reports. Reassess periodically."},
    ],
}


NIST_800_53_CATEGORY_METADATA: Dict[str, Dict[str, str]] = {
    "POLICY": {"label": "Policy", "icon": "file", "color": "#0972d3"},
    "PROCESS": {"label": "Process", "icon": "settings", "color": "#037f0c"},
    "GOVERNANCE": {"label": "Governance", "icon": "user-profile", "color": "#5f6b7a"},
    "TRAINING": {"label": "Training", "icon": "contact", "color": "#8b5cf6"},
    "DOCUMENTATION": {"label": "Documentation", "icon": "edit", "color": "#d97706"},
    "THIRD_PARTY": {"label": "Third Party", "icon": "external", "color": "#dc2626"},
}


def get_nist_organizational_requirements(control_id: str) -> List[Dict[str, str]]:
    """Get organizational requirements for a NIST 800-53 control."""
    return NIST_800_53_ORG_REQUIREMENTS.get(control_id.upper(), [])


def get_nist_category_metadata() -> Dict[str, Dict[str, str]]:
    """Get category metadata for display."""
    return NIST_800_53_CATEGORY_METADATA
