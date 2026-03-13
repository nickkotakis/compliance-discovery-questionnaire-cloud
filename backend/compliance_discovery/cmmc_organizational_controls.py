"""Organizational (non-AWS) control requirements for CMMC Level 2 practices.

Each CMMC practice requires both technical AWS controls AND organizational
controls (policies, procedures, training, governance). This module defines
the non-technical requirements that complement the AWS Implementation Guide.

Categories of organizational controls:
- POLICY: Written policies, standards, and procedures
- PROCESS: Defined processes and workflows
- GOVERNANCE: Leadership oversight, roles, and accountability
- TRAINING: Awareness, education, and competency programs
- DOCUMENTATION: Records, evidence, and audit artifacts
- THIRD_PARTY: Vendor management and external relationships
"""

from typing import Dict, List, Optional


CMMC_ORGANIZATIONAL_REQUIREMENTS: Dict[str, List[Dict[str, str]]] = {

    # =========================================================================
    # AC — Access Control
    # =========================================================================

    "AC.L2-3.1.1": [
        {"category": "POLICY", "title": "Access control policy",
         "description": "Maintain a documented access control policy defining who is authorized to access CUI systems, the approval process for granting access, and conditions for access revocation."},
        {"category": "PROCESS", "title": "Account provisioning and deprovisioning",
         "description": "Define a formal process for requesting, approving, provisioning, and revoking user access — including timelines for removing access when employees leave or change roles."},
    ],
    "AC.L2-3.1.2": [
        {"category": "DOCUMENTATION", "title": "Role-based access matrix",
         "description": "Document which roles exist, what functions each role can perform, and maintain a mapping of users to roles. Review and update at least annually."},
    ],
    "AC.L2-3.1.3": [
        {"category": "DOCUMENTATION", "title": "CUI data flow diagrams",
         "description": "Maintain data flow diagrams showing how CUI moves between systems, users, and external partners. Update when system architecture changes."},
        {"category": "POLICY", "title": "Information flow policy",
         "description": "Define approved paths for CUI transmission and prohibit unauthorized channels (personal email, unapproved cloud storage, etc.)."},
    ],
    "AC.L2-3.1.4": [
        {"category": "DOCUMENTATION", "title": "Separation of duties matrix",
         "description": "Document which duties are incompatible and must be performed by different individuals. Include examples relevant to your CUI environment."},
    ],
    "AC.L2-3.1.5": [
        {"category": "POLICY", "title": "Least privilege policy",
         "description": "Document the principle of least privilege as organizational policy, including requirements for periodic access reviews and removal of unnecessary permissions."},
        {"category": "PROCESS", "title": "Privileged account management",
         "description": "Define procedures for managing privileged accounts — who can have them, how they're approved, how often they're reviewed, and how privileged actions are monitored."},
    ],
    "AC.L2-3.1.6": [
        {"category": "POLICY", "title": "Non-privileged account usage",
         "description": "Require administrators to use non-privileged accounts for routine tasks and only elevate to privileged accounts when performing security functions."},
    ],
    "AC.L2-3.1.7": [
        {"category": "PROCESS", "title": "Privileged function monitoring",
         "description": "Define a process for reviewing audit logs of privileged function execution and investigating unauthorized attempts."},
    ],
    "AC.L2-3.1.8": [
        {"category": "POLICY", "title": "Account lockout policy",
         "description": "Document account lockout thresholds, lockout duration, and the process for unlocking accounts after lockout."},
    ],
    "AC.L2-3.1.9": [
        {"category": "POLICY", "title": "System use notification",
         "description": "Define the required content for system use notification banners, including authorized use, monitoring consent, and legal warnings."},
    ],
    "AC.L2-3.1.10": [
        {"category": "POLICY", "title": "Session lock policy",
         "description": "Define inactivity timeout periods for session lock and require pattern-hiding displays that conceal CUI content."},
    ],
    "AC.L2-3.1.11": [
        {"category": "POLICY", "title": "Session termination policy",
         "description": "Define conditions under which user sessions are automatically terminated (inactivity timeout, end of business day, token expiration)."},
    ],
    "AC.L2-3.1.12": [
        {"category": "POLICY", "title": "Remote access policy",
         "description": "Document approved remote access methods, authentication requirements (MFA), encryption standards, and monitoring procedures for remote sessions."},
        {"category": "PROCESS", "title": "Remote access authorization",
         "description": "Define the process for authorizing remote access, including who can approve it and under what conditions it can be granted or revoked."},
    ],
    "AC.L2-3.1.13": [
        {"category": "POLICY", "title": "Encryption for remote access",
         "description": "Require cryptographic protection for all remote access sessions and specify minimum encryption standards (e.g., TLS 1.2+, IPsec)."},
    ],
    "AC.L2-3.1.14": [
        {"category": "POLICY", "title": "Managed access control points",
         "description": "Require all remote access to route through managed access control points (VPN, jump box) rather than direct connections to individual systems."},
    ],
    "AC.L2-3.1.15": [
        {"category": "PROCESS", "title": "Remote privileged command authorization",
         "description": "Define an authorization process for remote execution of privileged commands, including who can approve and how approvals are documented."},
    ],
    "AC.L2-3.1.16": [
        {"category": "POLICY", "title": "Wireless access authorization",
         "description": "Require authorization before wireless access points or wireless-enabled devices can connect to networks handling CUI."},
        {"category": "PROCESS", "title": "Rogue AP detection",
         "description": "Establish a process for periodically scanning for and responding to unauthorized wireless access points."},
    ],
    "AC.L2-3.1.17": [
        {"category": "POLICY", "title": "Wireless security standards",
         "description": "Define minimum wireless security standards (WPA2-Enterprise or WPA3) and require separation of CUI-accessible wireless from guest networks."},
    ],
    "AC.L2-3.1.18": [
        {"category": "POLICY", "title": "Mobile device policy",
         "description": "Define which mobile devices are permitted to access CUI, required security configurations (encryption, screen lock, remote wipe), and MDM enrollment requirements."},
    ],
    "AC.L2-3.1.19": [
        {"category": "POLICY", "title": "Mobile device encryption",
         "description": "Require full-disk encryption on all mobile devices and laptops that store or access CUI. Define procedures for lost or stolen devices."},
    ],
    "AC.L2-3.1.20": [
        {"category": "POLICY", "title": "External system connections",
         "description": "Require security agreements (ISAs/MOUs) before connecting to external systems. Define security requirements that external systems must meet."},
        {"category": "PROCESS", "title": "External connection review",
         "description": "Periodically review all external system connections to verify they are still needed and security agreements are current."},
    ],
    "AC.L2-3.1.21": [
        {"category": "POLICY", "title": "Portable storage restrictions",
         "description": "Restrict or prohibit the use of portable storage devices (USB drives, external hard drives) on systems that access CUI."},
    ],
    "AC.L2-3.1.22": [
        {"category": "POLICY", "title": "Public information controls",
         "description": "Prohibit posting CUI on publicly accessible systems. Define a review and approval process before any content is made publicly available."},
        {"category": "PROCESS", "title": "Public content review",
         "description": "Establish a review process to verify no CUI is included before publishing content to public-facing systems."},
    ],

    # =========================================================================
    # AT — Awareness and Training
    # =========================================================================

    "AT.L2-3.2.1": [
        {"category": "POLICY", "title": "Security awareness training policy",
         "description": "Define training requirements including topics, frequency (at least annually), target audiences, and completion tracking."},
        {"category": "TRAINING", "title": "CUI-specific awareness content",
         "description": "Include CUI handling rules, marking requirements, authorized distribution channels, and reporting procedures in awareness training."},
        {"category": "DOCUMENTATION", "title": "Training completion records",
         "description": "Maintain records of training completion by individual, including dates, scores, and follow-up for non-completions."},
    ],
    "AT.L2-3.2.2": [
        {"category": "TRAINING", "title": "Role-based security training",
         "description": "Provide specialized training for personnel in security-related roles (system admins, security analysts, incident responders) covering their specific duties."},
        {"category": "DOCUMENTATION", "title": "Role-based training records",
         "description": "Track completion of role-specific training and ensure personnel are trained before assuming security responsibilities."},
    ],
    "AT.L2-3.2.3": [
        {"category": "TRAINING", "title": "Insider threat awareness",
         "description": "Train all personnel to recognize potential insider threat indicators and provide clear reporting procedures with non-retaliation protections."},
        {"category": "PROCESS", "title": "Insider threat reporting",
         "description": "Establish a confidential reporting channel for insider threat concerns and define how reports are investigated."},
    ],

    # =========================================================================
    # AU — Audit and Accountability
    # =========================================================================

    "AU.L2-3.3.1": [
        {"category": "POLICY", "title": "Audit logging policy",
         "description": "Define which events must be logged, minimum retention periods, and log protection requirements. Address both system and application-level logging."},
        {"category": "DOCUMENTATION", "title": "Auditable events list",
         "description": "Maintain a documented list of events that must be captured in audit logs (logins, privilege use, config changes, data access, failures)."},
    ],
    "AU.L2-3.3.2": [
        {"category": "POLICY", "title": "Individual accountability policy",
         "description": "Prohibit shared or generic accounts. Require every action to be traceable to a specific individual through unique identifiers."},
    ],
    "AU.L2-3.3.3": [
        {"category": "PROCESS", "title": "Audit event review process",
         "description": "Establish a periodic review process to evaluate whether the right events are being logged and update logging configuration when new systems are deployed."},
    ],
    "AU.L2-3.3.4": [
        {"category": "PROCESS", "title": "Logging failure response",
         "description": "Define escalation procedures when audit logging fails — who is notified, what actions are taken, and how quickly logging must be restored."},
    ],
    "AU.L2-3.3.5": [
        {"category": "PROCESS", "title": "Log correlation and analysis",
         "description": "Define procedures for correlating logs from multiple sources to detect suspicious patterns and support incident investigation."},
    ],
    "AU.L2-3.3.6": [
        {"category": "PROCESS", "title": "Audit reporting capability",
         "description": "Ensure the ability to generate on-demand audit reports for investigations, compliance reviews, and management reporting."},
    ],
    "AU.L2-3.3.7": [
        {"category": "POLICY", "title": "Time synchronization policy",
         "description": "Require all systems to synchronize to an authoritative time source and define acceptable time drift tolerances."},
    ],
    "AU.L2-3.3.8": [
        {"category": "POLICY", "title": "Audit log protection",
         "description": "Define who can access, modify, or delete audit logs. Require log integrity protection (immutable storage, separate access controls)."},
        {"category": "GOVERNANCE", "title": "Log access separation",
         "description": "Ensure the team managing audit logs is separate from the teams whose activities are being logged."},
    ],
    "AU.L2-3.3.9": [
        {"category": "POLICY", "title": "Audit management restrictions",
         "description": "Restrict the ability to configure, modify, or disable audit logging to a small set of authorized administrators."},
    ],

    # =========================================================================
    # CM — Configuration Management
    # =========================================================================

    "CM.L2-3.4.1": [
        {"category": "DOCUMENTATION", "title": "Baseline configuration documentation",
         "description": "Document baseline configurations for all system types (servers, workstations, network devices, cloud resources) and maintain a current hardware/software inventory."},
        {"category": "PROCESS", "title": "Inventory management process",
         "description": "Define how the system inventory is maintained, reconciled, and updated when assets are added, modified, or decommissioned."},
    ],
    "CM.L2-3.4.2": [
        {"category": "POLICY", "title": "Security configuration standards",
         "description": "Adopt and document security configuration standards (CIS Benchmarks, STIGs, or custom hardening guides) for all system types in the CUI environment."},
    ],
    "CM.L2-3.4.3": [
        {"category": "PROCESS", "title": "Change management process",
         "description": "Define a formal change management process with request, review, approval, implementation, and verification steps. Require documentation of all changes to CUI systems."},
        {"category": "DOCUMENTATION", "title": "Change log",
         "description": "Maintain a log of all changes to CUI systems including who requested, who approved, what changed, and when."},
    ],
    "CM.L2-3.4.4": [
        {"category": "PROCESS", "title": "Security impact analysis",
         "description": "Require a security impact analysis before implementing changes to CUI systems. Document the analysis and any mitigations applied."},
    ],
    "CM.L2-3.4.5": [
        {"category": "POLICY", "title": "Change access restrictions",
         "description": "Define who is authorized to make changes to CUI systems and require both physical and logical access controls for change implementation."},
    ],
    "CM.L2-3.4.6": [
        {"category": "POLICY", "title": "Least functionality policy",
         "description": "Require systems to be configured with only essential capabilities. Document approved services, functions, and ports for each system type."},
    ],
    "CM.L2-3.4.7": [
        {"category": "DOCUMENTATION", "title": "Approved ports and services",
         "description": "Maintain a documented list of approved ports, protocols, and services for each system type. Require justification for any exceptions."},
    ],
    "CM.L2-3.4.8": [
        {"category": "POLICY", "title": "Software authorization policy",
         "description": "Define whether you use application whitelisting (allow only approved) or blacklisting (block known-bad). Maintain the approved or prohibited software list."},
    ],
    "CM.L2-3.4.9": [
        {"category": "POLICY", "title": "User-installed software policy",
         "description": "Define restrictions on user-installed software on CUI systems. Specify what is permitted, what requires approval, and what is prohibited."},
    ],

    # =========================================================================
    # IA — Identification and Authentication
    # =========================================================================

    "IA.L2-3.5.1": [
        {"category": "POLICY", "title": "Identifier management policy",
         "description": "Require unique identifiers for all users, processes, and devices. Prohibit shared or generic accounts in the CUI environment."},
    ],
    "IA.L2-3.5.2": [
        {"category": "POLICY", "title": "Authentication policy",
         "description": "Define approved authentication methods and minimum requirements for each access type (local, network, remote, privileged)."},
    ],
    "IA.L2-3.5.3": [
        {"category": "POLICY", "title": "MFA policy",
         "description": "Require multifactor authentication for all privileged accounts and for network access to non-privileged accounts. Specify approved MFA types."},
    ],
    "IA.L2-3.5.4": [
        {"category": "POLICY", "title": "Replay-resistant authentication",
         "description": "Require authentication mechanisms that are resistant to replay attacks (TOTP, challenge-response, token-based) for network access."},
    ],
    "IA.L2-3.5.5": [
        {"category": "POLICY", "title": "Identifier reuse prevention",
         "description": "Define a waiting period before deactivated identifiers can be reassigned to prevent confusion in audit trails."},
    ],
    "IA.L2-3.5.6": [
        {"category": "POLICY", "title": "Inactive account policy",
         "description": "Define the inactivity period after which accounts are automatically disabled (e.g., 90 days). Include a process for reactivation."},
    ],
    "IA.L2-3.5.7": [
        {"category": "POLICY", "title": "Password complexity policy",
         "description": "Define minimum password requirements: length (15+ characters for DoD), complexity, character change requirements, and prohibited patterns."},
    ],
    "IA.L2-3.5.8": [
        {"category": "POLICY", "title": "Password history policy",
         "description": "Define the number of previous passwords tracked to prevent reuse (typically 24 generations for DoD environments)."},
    ],
    "IA.L2-3.5.9": [
        {"category": "PROCESS", "title": "Temporary password procedures",
         "description": "Define how temporary passwords are generated, securely delivered, and require immediate change upon first login."},
    ],
    "IA.L2-3.5.10": [
        {"category": "POLICY", "title": "Credential protection policy",
         "description": "Require cryptographic protection for stored passwords (one-way hashing) and transmitted passwords (TLS encryption). Prohibit plaintext storage."},
    ],
    "IA.L2-3.5.11": [
        {"category": "POLICY", "title": "Authentication feedback policy",
         "description": "Require password masking on all login screens and prohibit error messages that reveal whether the username or password was incorrect."},
    ],

    # =========================================================================
    # IR — Incident Response
    # =========================================================================

    "IR.L2-3.6.1": [
        {"category": "POLICY", "title": "Incident response policy",
         "description": "Maintain a documented incident response policy covering preparation, detection, analysis, containment, eradication, and recovery — with specific procedures for CUI-related incidents."},
        {"category": "DOCUMENTATION", "title": "Incident response plan",
         "description": "Maintain a detailed IR plan with roles, responsibilities, contact lists, escalation procedures, and step-by-step runbooks for common incident types."},
        {"category": "GOVERNANCE", "title": "IR team designation",
         "description": "Formally designate an incident response team with defined roles, authority levels, and on-call responsibilities."},
    ],
    "IR.L2-3.6.2": [
        {"category": "PROCESS", "title": "Incident tracking and documentation",
         "description": "Define a process for tracking incidents from detection through resolution — including a ticketing system or incident log with required fields (date, description, severity, actions taken, resolution)."},
        {"category": "PROCESS", "title": "Incident reporting procedures",
         "description": "Define who must be notified of incidents (internal management, DIBCAC, DoD, law enforcement) and within what timelines. Include reporting templates and contact information."},
        {"category": "DOCUMENTATION", "title": "Incident report templates",
         "description": "Maintain standardized incident report templates that capture all required information for internal tracking and external reporting obligations."},
    ],
    "IR.L2-3.6.3": [
        {"category": "PROCESS", "title": "IR testing program",
         "description": "Establish a schedule for testing incident response capabilities through tabletop exercises, simulations, or live drills — at least annually."},
        {"category": "DOCUMENTATION", "title": "Exercise after-action reports",
         "description": "Document lessons learned from each IR test or exercise and track improvements made to the IR plan based on findings."},
    ],

    # =========================================================================
    # MA — Maintenance
    # =========================================================================

    "MA.L2-3.7.1": [
        {"category": "PROCESS", "title": "Maintenance scheduling",
         "description": "Define a maintenance schedule for CUI systems including patching cadence, update windows, and communication procedures for planned maintenance."},
        {"category": "DOCUMENTATION", "title": "Maintenance records",
         "description": "Maintain records of all maintenance activities performed on CUI systems, including who performed them, what was done, and when."},
    ],
    "MA.L2-3.7.2": [
        {"category": "POLICY", "title": "Maintenance tools policy",
         "description": "Define approved maintenance tools and techniques. Require integrity verification of tools before use on CUI systems."},
    ],
    "MA.L2-3.7.3": [
        {"category": "PROCESS", "title": "Off-site maintenance sanitization",
         "description": "Define procedures for sanitizing equipment of CUI before it leaves the facility for maintenance. Document sanitization actions taken."},
    ],
    "MA.L2-3.7.4": [
        {"category": "PROCESS", "title": "Diagnostic media scanning",
         "description": "Require malware scanning of all diagnostic and test media before use on CUI systems. Document scan results."},
    ],
    "MA.L2-3.7.5": [
        {"category": "POLICY", "title": "Remote maintenance policy",
         "description": "Require MFA for remote maintenance sessions and mandate session termination when maintenance is complete. Log all remote maintenance activity."},
    ],
    "MA.L2-3.7.6": [
        {"category": "PROCESS", "title": "Maintenance personnel supervision",
         "description": "Define escort and supervision procedures for maintenance personnel who lack CUI access authorization. Document supervision activities."},
    ],

    # =========================================================================
    # MP — Media Protection
    # =========================================================================

    "MP.L2-3.8.1": [
        {"category": "POLICY", "title": "Media protection policy",
         "description": "Define requirements for physically securing media containing CUI — locked storage, controlled access areas, and inventory tracking."},
    ],
    "MP.L2-3.8.2": [
        {"category": "PROCESS", "title": "Media access authorization",
         "description": "Define who is authorized to access media containing CUI and maintain access logs for media storage locations."},
    ],
    "MP.L2-3.8.3": [
        {"category": "PROCESS", "title": "Media sanitization procedures",
         "description": "Define sanitization methods per NIST SP 800-88 for each media type (cryptographic erase for SSDs, degaussing for magnetic media, physical destruction). Maintain sanitization records."},
    ],
    "MP.L2-3.8.4": [
        {"category": "POLICY", "title": "CUI marking requirements",
         "description": "Define CUI marking requirements for all media types — banners on documents, labels on storage devices, and metadata tags on digital files."},
    ],
    "MP.L2-3.8.5": [
        {"category": "PROCESS", "title": "Media transport accountability",
         "description": "Define chain-of-custody procedures for CUI media transported outside controlled areas, including tracking forms and approved transport methods."},
    ],
    "MP.L2-3.8.6": [
        {"category": "POLICY", "title": "Transport encryption requirements",
         "description": "Require encryption (AES-256, FIPS 140-2 validated) for CUI on digital media during transport, or document alternative physical safeguards used."},
    ],
    "MP.L2-3.8.7": [
        {"category": "POLICY", "title": "Removable media policy",
         "description": "Define restrictions on removable media use on CUI systems — which devices are approved, who can authorize exceptions, and how usage is monitored."},
    ],
    "MP.L2-3.8.8": [
        {"category": "POLICY", "title": "Unidentified storage device prohibition",
         "description": "Prohibit use of portable storage devices with no identifiable owner. Include this in security awareness training."},
    ],
    "MP.L2-3.8.9": [
        {"category": "POLICY", "title": "Backup CUI protection",
         "description": "Require encryption and access controls for backup copies of CUI. Define who can access backups and under what circumstances."},
    ],

    # =========================================================================
    # PE — Physical Protection
    # =========================================================================

    "PE.L2-3.10.1": [
        {"category": "POLICY", "title": "Physical access control policy",
         "description": "Define who is authorized for physical access to CUI areas, the approval process, and access control mechanisms (badges, biometrics, keys)."},
        {"category": "DOCUMENTATION", "title": "Authorized access list",
         "description": "Maintain a current list of individuals authorized for physical access to each CUI area. Review and update at least quarterly."},
    ],
    "PE.L2-3.10.2": [
        {"category": "PROCESS", "title": "Physical monitoring procedures",
         "description": "Define monitoring requirements for CUI facilities — security cameras, intrusion detection, guard patrols — and procedures for reviewing monitoring data."},
    ],
    "PE.L2-3.10.3": [
        {"category": "PROCESS", "title": "Visitor management procedures",
         "description": "Define visitor sign-in requirements, badge issuance, escort procedures, and activity monitoring for all visitors to CUI areas."},
        {"category": "DOCUMENTATION", "title": "Visitor logs",
         "description": "Maintain visitor logs with name, organization, date/time, escort, and purpose of visit. Retain for the required period."},
    ],
    "PE.L2-3.10.4": [
        {"category": "DOCUMENTATION", "title": "Physical access audit logs",
         "description": "Maintain audit logs of physical access to CUI areas (badge reader logs, sign-in sheets). Define retention periods and review frequency."},
    ],
    "PE.L2-3.10.5": [
        {"category": "PROCESS", "title": "Physical access device management",
         "description": "Define procedures for issuing, tracking, and revoking physical access devices (keys, badges, cards). Conduct periodic inventory reconciliation."},
    ],
    "PE.L2-3.10.6": [
        {"category": "POLICY", "title": "Alternate work site policy",
         "description": "Define security requirements for accessing CUI from alternate work sites (home offices) — encrypted devices, VPN, private workspace, screen privacy."},
        {"category": "DOCUMENTATION", "title": "Telework agreements",
         "description": "Require signed telework agreements acknowledging security responsibilities for CUI access from alternate locations."},
    ],

    # =========================================================================
    # PS — Personnel Security
    # =========================================================================

    "PS.L2-3.9.1": [
        {"category": "PROCESS", "title": "Personnel screening process",
         "description": "Define background screening requirements before granting access to CUI systems — criminal checks, employment verification, reference checks. Define re-screening frequency."},
        {"category": "DOCUMENTATION", "title": "Screening records",
         "description": "Maintain records of completed background screenings for all personnel with CUI access."},
    ],
    "PS.L2-3.9.2": [
        {"category": "PROCESS", "title": "Termination and transfer procedures",
         "description": "Define offboarding procedures including access revocation timelines, equipment return, badge collection, exit interviews, and knowledge transfer for CUI-related responsibilities."},
        {"category": "DOCUMENTATION", "title": "Offboarding checklist",
         "description": "Maintain a standardized offboarding checklist covering all access revocation steps — system accounts, physical access, badges, keys, equipment, and CUI material return."},
    ],

    # =========================================================================
    # RA — Risk Assessment
    # =========================================================================

    "RA.L2-3.11.1": [
        {"category": "PROCESS", "title": "Risk assessment process",
         "description": "Define a formal risk assessment process including methodology, frequency (at least annually), scope, and roles. Cover threats to CUI confidentiality, integrity, and availability."},
        {"category": "DOCUMENTATION", "title": "Risk register",
         "description": "Maintain a risk register documenting identified risks, likelihood, impact, risk ratings, and risk response decisions."},
        {"category": "GOVERNANCE", "title": "Risk assessment oversight",
         "description": "Assign responsibility for conducting and reviewing risk assessments. Ensure results are reported to management for risk acceptance decisions."},
    ],
    "RA.L2-3.11.2": [
        {"category": "PROCESS", "title": "Vulnerability scanning program",
         "description": "Define vulnerability scanning frequency, scope, tools, and remediation timelines by severity. Include both scheduled and event-triggered scans."},
    ],
    "RA.L2-3.11.3": [
        {"category": "PROCESS", "title": "Vulnerability remediation process",
         "description": "Define remediation timelines by severity (e.g., critical: 48 hours, high: 30 days, medium: 90 days). Track remediation progress and escalate overdue items."},
        {"category": "DOCUMENTATION", "title": "Remediation tracking",
         "description": "Maintain records of vulnerability findings, remediation actions, and closure dates. Document risk acceptance for vulnerabilities not remediated within timelines."},
    ],

    # =========================================================================
    # CA — Security Assessment
    # =========================================================================

    "CA.L2-3.12.1": [
        {"category": "PROCESS", "title": "Security control assessment",
         "description": "Define a process for periodically assessing whether security controls are effective — including assessment methodology, frequency, and assessor qualifications."},
    ],
    "CA.L2-3.12.2": [
        {"category": "DOCUMENTATION", "title": "Plan of Action and Milestones (POA&M)",
         "description": "Maintain a POA&M tracking all identified security deficiencies with owners, target dates, milestones, and status. Review regularly and report to management."},
        {"category": "GOVERNANCE", "title": "POA&M oversight",
         "description": "Assign management oversight for POA&M items. Establish escalation procedures for overdue items and a process for closing completed items with evidence."},
    ],
    "CA.L2-3.12.3": [
        {"category": "PROCESS", "title": "Continuous monitoring strategy",
         "description": "Define a continuous monitoring strategy specifying what is monitored, how often, by whom, and how findings are reported and acted upon."},
    ],
    "CA.L2-3.12.4": [
        {"category": "DOCUMENTATION", "title": "System Security Plan (SSP)",
         "description": "Maintain a System Security Plan describing system boundaries, environment, security control implementation, and connections to other systems. Update when significant changes occur."},
        {"category": "PROCESS", "title": "SSP maintenance",
         "description": "Define a process for reviewing and updating the SSP at least annually and whenever significant system changes occur."},
    ],

    # =========================================================================
    # SC — System and Communications Protection
    # =========================================================================

    "SC.L2-3.13.1": [
        {"category": "DOCUMENTATION", "title": "Network architecture documentation",
         "description": "Maintain network architecture diagrams showing external and internal boundaries, security zones, and traffic flow paths. Update when architecture changes."},
    ],
    "SC.L2-3.13.2": [
        {"category": "POLICY", "title": "Security architecture standards",
         "description": "Define security architecture principles (defense-in-depth, least privilege, fail-secure) and require their application in system design."},
    ],
    "SC.L2-3.13.3": [
        {"category": "POLICY", "title": "User/management separation",
         "description": "Require separation of user-facing functionality from system management interfaces. Document which interfaces are management-only and restrict access accordingly."},
    ],
    "SC.L2-3.13.4": [
        {"category": "POLICY", "title": "Shared resource protection",
         "description": "Define requirements for preventing information leakage through shared system resources (memory, temp files, connection pools). Address in secure development standards."},
    ],
    "SC.L2-3.13.5": [
        {"category": "DOCUMENTATION", "title": "DMZ architecture documentation",
         "description": "Document the separation between publicly accessible components and internal networks, including the security controls at each boundary."},
    ],
    "SC.L2-3.13.6": [
        {"category": "POLICY", "title": "Default-deny network policy",
         "description": "Require deny-by-default network configurations. All allowed traffic must be explicitly documented and justified."},
    ],
    "SC.L2-3.13.7": [
        {"category": "POLICY", "title": "Split tunneling prevention",
         "description": "Prohibit split tunneling on VPN connections to prevent CUI traffic from bypassing security controls."},
    ],
    "SC.L2-3.13.8": [
        {"category": "POLICY", "title": "Encryption in transit policy",
         "description": "Require encryption (TLS 1.2+) for all CUI in transit. Define minimum cipher suites and certificate management requirements."},
    ],
    "SC.L2-3.13.9": [
        {"category": "POLICY", "title": "Session termination policy",
         "description": "Define session timeout values for different connection types and require automatic termination of inactive sessions."},
    ],
    "SC.L2-3.13.10": [
        {"category": "PROCESS", "title": "Cryptographic key management",
         "description": "Define key management procedures covering key generation, distribution, storage, rotation, revocation, and destruction. Assign key custodian responsibilities."},
    ],
    "SC.L2-3.13.11": [
        {"category": "POLICY", "title": "FIPS cryptography requirement",
         "description": "Require FIPS 140-2 validated cryptographic modules for protecting CUI confidentiality. Maintain an inventory of cryptographic modules and their validation status."},
    ],
    "SC.L2-3.13.12": [
        {"category": "POLICY", "title": "Collaborative computing device policy",
         "description": "Define policies for devices with remote activation capability (cameras, microphones). Require visible indicators when devices are active and prohibit unauthorized remote activation."},
    ],
    "SC.L2-3.13.13": [
        {"category": "POLICY", "title": "Mobile code policy",
         "description": "Define which mobile code technologies are allowed, restricted, or prohibited on CUI systems. Require code signing for approved mobile code."},
    ],
    "SC.L2-3.13.14": [
        {"category": "POLICY", "title": "VoIP security policy",
         "description": "Define security requirements for VoIP communications involving CUI — encryption, network segmentation, and approved platforms."},
    ],
    "SC.L2-3.13.15": [
        {"category": "POLICY", "title": "Session authenticity policy",
         "description": "Require session authenticity protection (TLS certificate validation, mutual TLS for service-to-service) to prevent man-in-the-middle attacks."},
    ],
    "SC.L2-3.13.16": [
        {"category": "POLICY", "title": "Encryption at rest policy",
         "description": "Require encryption at rest for all CUI storage. Define minimum encryption standards and key management requirements."},
    ],

    # =========================================================================
    # SI — System and Information Integrity
    # =========================================================================

    "SI.L2-3.14.1": [
        {"category": "PROCESS", "title": "Flaw remediation process",
         "description": "Define a process for identifying, reporting, and correcting system flaws including patch management timelines by severity and testing requirements before deployment."},
    ],
    "SI.L2-3.14.2": [
        {"category": "POLICY", "title": "Malware protection policy",
         "description": "Require antivirus/anti-malware on all CUI endpoints and servers. Define update frequency, scan schedules, and response procedures for detections."},
    ],
    "SI.L2-3.14.3": [
        {"category": "PROCESS", "title": "Security advisory monitoring",
         "description": "Define which security alert sources to monitor (CISA, US-CERT, vendor advisories), who reviews them, and the process for evaluating applicability and taking action."},
    ],
    "SI.L2-3.14.4": [
        {"category": "PROCESS", "title": "Malware protection updates",
         "description": "Define requirements for keeping malware protection current — automatic signature updates, engine updates, and verification that updates are applied across all systems."},
    ],
    "SI.L2-3.14.5": [
        {"category": "POLICY", "title": "Malware scanning policy",
         "description": "Require both periodic full-system scans and real-time scanning of files from external sources. Define scan frequency and response procedures for detections."},
    ],
    "SI.L2-3.14.6": [
        {"category": "PROCESS", "title": "System monitoring program",
         "description": "Define what is monitored (inbound/outbound traffic, API calls, user behavior), alerting thresholds, and escalation procedures for detected anomalies."},
        {"category": "GOVERNANCE", "title": "Monitoring oversight",
         "description": "Assign responsibility for monitoring operations, alert triage, and periodic review of monitoring effectiveness."},
    ],
    "SI.L2-3.14.7": [
        {"category": "PROCESS", "title": "Unauthorized use detection",
         "description": "Define baseline normal behavior for CUI systems and establish procedures for detecting and investigating deviations that may indicate unauthorized use."},
    ],
}


# Category metadata for display
CMMC_CATEGORY_METADATA: Dict[str, Dict[str, str]] = {
    "POLICY": {"label": "Policy", "icon": "file", "color": "#0972d3"},
    "PROCESS": {"label": "Process", "icon": "settings", "color": "#037f0c"},
    "GOVERNANCE": {"label": "Governance", "icon": "user-profile", "color": "#5f6b7a"},
    "TRAINING": {"label": "Training", "icon": "contact", "color": "#8b5cf6"},
    "DOCUMENTATION": {"label": "Documentation", "icon": "edit", "color": "#d97706"},
    "THIRD_PARTY": {"label": "Third Party", "icon": "external", "color": "#dc2626"},
}


def get_cmmc_organizational_requirements(practice_id: str) -> List[Dict[str, str]]:
    """Get organizational requirements for a CMMC practice.

    Args:
        practice_id: CMMC practice ID (e.g., 'IR.L2-3.6.2')

    Returns:
        List of requirement dicts with category, title, description
    """
    return CMMC_ORGANIZATIONAL_REQUIREMENTS.get(practice_id.upper(), [])


def get_cmmc_category_metadata() -> Dict[str, Dict[str, str]]:
    """Get category metadata for display."""
    return CMMC_CATEGORY_METADATA
