"""Organizational (non-AWS) control requirements for NIST CSF 2.0 subcategories.

Each CSF subcategory requires both technical AWS controls AND organizational
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


# Each requirement has a category, title, and description
CSF_ORGANIZATIONAL_REQUIREMENTS: Dict[str, List[Dict[str, str]]] = {

    # =========================================================================
    # GV - GOVERN
    # =========================================================================

    # GV.OC - Organizational Context
    "GV.OC-01": [
        {"category": "DOCUMENTATION", "title": "Mission-to-risk mapping",
         "description": "Document how the organizational mission and business objectives inform cybersecurity risk management priorities."},
        {"category": "GOVERNANCE", "title": "Executive risk alignment",
         "description": "Obtain leadership sign-off on how cybersecurity investments map to business priorities."},
        {"category": "PROCESS", "title": "Annual strategy review",
         "description": "Establish a recurring review cycle to reassess the alignment between mission objectives and cybersecurity strategy."},
    ],
    "GV.OC-02": [
        {"category": "DOCUMENTATION", "title": "Stakeholder register",
         "description": "Maintain a register of internal and external stakeholders with their cybersecurity expectations and communication preferences."},
        {"category": "PROCESS", "title": "Stakeholder engagement process",
         "description": "Define how stakeholder needs are gathered, prioritized, and incorporated into risk management decisions."},
        {"category": "GOVERNANCE", "title": "Board/executive reporting",
         "description": "Establish regular reporting cadence to communicate cybersecurity risk posture to leadership and key stakeholders."},
    ],
    "GV.OC-03": [
        {"category": "DOCUMENTATION", "title": "Regulatory obligations inventory",
         "description": "Maintain a current inventory of all legal, regulatory, and contractual cybersecurity requirements (e.g., PCI DSS, HIPAA, GDPR, SOC 2)."},
        {"category": "PROCESS", "title": "Regulatory change monitoring",
         "description": "Establish a process to monitor for changes in applicable laws, regulations, and contractual obligations."},
        {"category": "GOVERNANCE", "title": "Legal/compliance coordination",
         "description": "Assign responsibility for tracking regulatory obligations and coordinating with legal counsel on interpretation."},
    ],
    "GV.OC-04": [
        {"category": "DOCUMENTATION", "title": "Critical services catalog",
         "description": "Document the services, capabilities, and objectives that external stakeholders depend on, including SLAs and availability targets."},
        {"category": "PROCESS", "title": "External communication procedures",
         "description": "Define procedures for communicating security posture, incidents, and service status to external stakeholders."},
    ],
    "GV.OC-05": [
        {"category": "DOCUMENTATION", "title": "Dependency inventory",
         "description": "Maintain an inventory of external services, suppliers, and dependencies critical to organizational operations."},
        {"category": "PROCESS", "title": "Dependency health monitoring",
         "description": "Establish processes to monitor the availability and security posture of critical external dependencies."},
    ],

    # GV.RM - Risk Management Strategy
    "GV.RM-01": [
        {"category": "GOVERNANCE", "title": "Risk management charter",
         "description": "Establish documented risk management objectives agreed upon by senior leadership and aligned with enterprise risk management."},
        {"category": "DOCUMENTATION", "title": "Risk management framework document",
         "description": "Maintain a formal risk management framework document that defines objectives, scope, and methodology."},
    ],
    "GV.RM-02": [
        {"category": "POLICY", "title": "Risk appetite statement",
         "description": "Define and document organizational risk appetite and risk tolerance statements for different data classifications and business functions."},
        {"category": "GOVERNANCE", "title": "Risk tolerance communication",
         "description": "Communicate risk appetite and tolerance statements to all relevant decision-makers and ensure they inform architecture and investment decisions."},
    ],
    "GV.RM-03": [
        {"category": "PROCESS", "title": "ERM integration",
         "description": "Integrate cybersecurity risk management activities into the enterprise risk management (ERM) program."},
        {"category": "GOVERNANCE", "title": "Cross-functional risk coordination",
         "description": "Establish coordination between cybersecurity, finance, legal, and business units for risk discussions."},
    ],
    "GV.RM-04": [
        {"category": "POLICY", "title": "Risk response strategy",
         "description": "Document approved risk response options (accept, mitigate, transfer, avoid) and criteria for selecting each."},
        {"category": "GOVERNANCE", "title": "Risk response authority",
         "description": "Define who has authority to approve risk acceptance, transfer, or mitigation decisions at each level."},
    ],
    "GV.RM-05": [
        {"category": "PROCESS", "title": "Risk communication channels",
         "description": "Establish formal communication channels for cybersecurity risks across the organization, including supply chain risks."},
        {"category": "GOVERNANCE", "title": "Cross-organizational risk reporting",
         "description": "Define reporting lines and escalation paths for cybersecurity risk information."},
    ],
    "GV.RM-06": [
        {"category": "PROCESS", "title": "Risk scoring methodology",
         "description": "Establish a standardized method for calculating, documenting, categorizing, and prioritizing cybersecurity risks."},
        {"category": "DOCUMENTATION", "title": "Risk register",
         "description": "Maintain a risk register using the standardized methodology with consistent scoring across the organization."},
    ],
    "GV.RM-07": [
        {"category": "PROCESS", "title": "Opportunity assessment",
         "description": "Include positive risks (opportunities) in cybersecurity risk discussions and investment planning."},
    ],

    # GV.RR - Roles, Responsibilities, and Authorities
    "GV.RR-01": [
        {"category": "GOVERNANCE", "title": "Leadership accountability",
         "description": "Assign explicit cybersecurity risk accountability to organizational leadership with documented responsibilities."},
        {"category": "GOVERNANCE", "title": "Risk-aware culture",
         "description": "Foster a culture of risk awareness, ethical behavior, and continuous improvement through leadership actions and messaging."},
    ],
    "GV.RR-02": [
        {"category": "DOCUMENTATION", "title": "RACI matrix",
         "description": "Document cybersecurity roles, responsibilities, and authorities in a RACI matrix or equivalent, communicated to all personnel."},
        {"category": "PROCESS", "title": "Role enforcement",
         "description": "Establish mechanisms to enforce assigned cybersecurity responsibilities (e.g., performance reviews, job descriptions)."},
    ],
    "GV.RR-03": [
        {"category": "GOVERNANCE", "title": "Resource allocation",
         "description": "Allocate adequate budget, staffing, and tools commensurate with the cybersecurity risk strategy and organizational needs."},
        {"category": "PROCESS", "title": "Resource adequacy review",
         "description": "Periodically assess whether cybersecurity resources are sufficient to meet risk management objectives."},
    ],
    "GV.RR-04": [
        {"category": "POLICY", "title": "HR security policies",
         "description": "Include cybersecurity responsibilities in HR practices: onboarding, role changes, offboarding, and performance management."},
        {"category": "PROCESS", "title": "Personnel lifecycle management",
         "description": "Define processes for granting, modifying, and revoking access as personnel join, move within, or leave the organization."},
    ],

    # GV.PO - Policy
    "GV.PO-01": [
        {"category": "POLICY", "title": "Cybersecurity policy document",
         "description": "Establish a formal cybersecurity risk management policy based on organizational context, strategy, and priorities. The policy must be approved by leadership."},
        {"category": "PROCESS", "title": "Policy communication",
         "description": "Distribute the policy to all relevant personnel and obtain acknowledgment. Use training sessions, intranet postings, or email distribution."},
        {"category": "PROCESS", "title": "Policy enforcement",
         "description": "Implement administrative and technical controls to enforce the policy, including disciplinary procedures for non-compliance."},
        {"category": "DOCUMENTATION", "title": "Policy approval records",
         "description": "Maintain records of policy approval by leadership, version history, and distribution/acknowledgment logs."},
    ],
    "GV.PO-02": [
        {"category": "PROCESS", "title": "Policy review cycle",
         "description": "Establish a defined review cycle (e.g., annual) and trigger-based review process for policy updates when threats, technology, or requirements change."},
        {"category": "DOCUMENTATION", "title": "Policy change log",
         "description": "Maintain a version-controlled change log documenting all policy revisions, reviewers, and approval dates."},
    ],

    # GV.SC - Supply Chain Risk Management
    "GV.SC-01": [
        {"category": "POLICY", "title": "Supply chain risk management program",
         "description": "Establish a documented supply chain risk management program with strategy, objectives, and policies agreed to by stakeholders."},
        {"category": "GOVERNANCE", "title": "SCRM program ownership",
         "description": "Assign ownership and accountability for the supply chain risk management program."},
    ],
    "GV.SC-02": [
        {"category": "DOCUMENTATION", "title": "Third-party roles and responsibilities",
         "description": "Document cybersecurity roles and responsibilities for suppliers, customers, and partners in contracts and agreements."},
        {"category": "PROCESS", "title": "Third-party coordination",
         "description": "Establish processes for coordinating cybersecurity responsibilities with external parties."},
    ],
    "GV.SC-03": [
        {"category": "PROCESS", "title": "SCRM integration",
         "description": "Integrate supply chain risk management into enterprise risk management and improvement processes."},
    ],
    "GV.SC-04": [
        {"category": "DOCUMENTATION", "title": "Supplier criticality assessment",
         "description": "Maintain a prioritized inventory of suppliers ranked by criticality to organizational operations."},
    ],
    "GV.SC-05": [
        {"category": "POLICY", "title": "Supplier security requirements",
         "description": "Establish cybersecurity requirements for suppliers in contracts, SLAs, and agreements."},
        {"category": "DOCUMENTATION", "title": "Contract security clauses",
         "description": "Include specific cybersecurity clauses in supplier contracts covering incident notification, data protection, and audit rights."},
    ],
    "GV.SC-06": [
        {"category": "PROCESS", "title": "Supplier due diligence",
         "description": "Perform cybersecurity due diligence before engaging suppliers and periodically thereafter."},
    ],
    "GV.SC-07": [
        {"category": "PROCESS", "title": "Supply chain risk assessment",
         "description": "Assess and manage risks associated with the supply chain, including risks from supplier changes or disruptions."},
    ],
    "GV.SC-08": [
        {"category": "PROCESS", "title": "Supplier incident procedures",
         "description": "Establish procedures for managing cybersecurity incidents involving suppliers, including notification and response coordination."},
    ],
    "GV.SC-09": [
        {"category": "PROCESS", "title": "Supply chain monitoring",
         "description": "Monitor supply chain security practices and performance against established requirements."},
    ],
    "GV.SC-10": [
        {"category": "PROCESS", "title": "Post-contract supplier management",
         "description": "Establish procedures for managing cybersecurity risks when supplier relationships end, including data return and access revocation."},
    ],

    # =========================================================================
    # ID - IDENTIFY
    # =========================================================================

    # ID.AM - Asset Management
    "ID.AM-01": [
        {"category": "DOCUMENTATION", "title": "Hardware asset inventory",
         "description": "Maintain a current inventory of all hardware assets managed by the organization."},
        {"category": "PROCESS", "title": "Asset discovery process",
         "description": "Establish automated and manual processes for discovering and cataloging hardware assets."},
    ],
    "ID.AM-02": [
        {"category": "DOCUMENTATION", "title": "Software asset inventory",
         "description": "Maintain a current inventory of all software platforms and applications."},
        {"category": "PROCESS", "title": "Software lifecycle management",
         "description": "Define processes for software approval, deployment, patching, and decommissioning."},
    ],
    "ID.AM-03": [
        {"category": "DOCUMENTATION", "title": "Network topology documentation",
         "description": "Document network communication flows, data flows, and system interconnections."},
    ],
    "ID.AM-04": [
        {"category": "DOCUMENTATION", "title": "External service catalog",
         "description": "Inventory external information systems and services used by the organization."},
    ],
    "ID.AM-05": [
        {"category": "POLICY", "title": "Asset classification policy",
         "description": "Classify assets based on criticality and business value to prioritize protection efforts."},
        {"category": "PROCESS", "title": "Asset prioritization process",
         "description": "Establish criteria and process for prioritizing assets based on risk and business impact."},
    ],
    "ID.AM-07": [
        {"category": "DOCUMENTATION", "title": "Data inventory and classification",
         "description": "Maintain an inventory of data with classification labels (public, internal, confidential, restricted)."},
        {"category": "POLICY", "title": "Data classification policy",
         "description": "Define data classification levels, handling requirements, and labeling standards."},
    ],
    "ID.AM-08": [
        {"category": "DOCUMENTATION", "title": "System-of-record documentation",
         "description": "Document systems that serve as authoritative sources for asset and configuration data."},
    ],

    # ID.IM - Improvement
    "ID.IM-01": [
        {"category": "PROCESS", "title": "Lessons learned process",
         "description": "Establish a process to identify improvements from security incidents, tests, and exercises."},
    ],
    "ID.IM-02": [
        {"category": "PROCESS", "title": "Continuous improvement program",
         "description": "Implement a continuous improvement program for cybersecurity based on assessments, metrics, and lessons learned."},
    ],
    "ID.IM-03": [
        {"category": "PROCESS", "title": "Security testing program",
         "description": "Establish a program for regular security testing including penetration tests, vulnerability scans, and tabletop exercises."},
    ],
    "ID.IM-04": [
        {"category": "PROCESS", "title": "Incident-driven improvements",
         "description": "Define how findings from incidents and response activities feed back into security program improvements."},
    ],

    # ID.RA - Risk Assessment
    "ID.RA-01": [
        {"category": "DOCUMENTATION", "title": "Vulnerability inventory",
         "description": "Maintain a documented inventory of known vulnerabilities across organizational assets."},
        {"category": "PROCESS", "title": "Vulnerability identification process",
         "description": "Establish processes for identifying and documenting vulnerabilities through scanning, threat intelligence, and vendor advisories."},
    ],
    "ID.RA-02": [
        {"category": "PROCESS", "title": "Threat intelligence program",
         "description": "Receive and analyze cyber threat intelligence from information sharing forums and sources."},
    ],
    "ID.RA-03": [
        {"category": "PROCESS", "title": "Threat modeling",
         "description": "Identify and document internal and external threats to the organization through threat modeling exercises."},
    ],
    "ID.RA-04": [
        {"category": "PROCESS", "title": "Business impact analysis",
         "description": "Assess and document potential business impacts and likelihoods of identified threats exploiting vulnerabilities."},
    ],
    "ID.RA-05": [
        {"category": "PROCESS", "title": "Risk prioritization",
         "description": "Prioritize identified risks using a consistent methodology that considers likelihood, impact, and organizational context."},
    ],
    "ID.RA-06": [
        {"category": "DOCUMENTATION", "title": "Risk response documentation",
         "description": "Document chosen risk responses (accept, mitigate, transfer, avoid) with rationale and approval."},
    ],
    "ID.RA-07": [
        {"category": "PROCESS", "title": "Risk change management",
         "description": "Manage changes to risks over time, including reassessment when the threat landscape or business context changes."},
    ],
    "ID.RA-08": [
        {"category": "PROCESS", "title": "Risk assessment integration",
         "description": "Integrate risk assessment results into decision-making processes for acquisitions and technology changes."},
    ],
    "ID.RA-09": [
        {"category": "PROCESS", "title": "Risk assessment of critical assets",
         "description": "Conduct risk assessments focused on critical assets, including hardware, software, and data."},
    ],
    "ID.RA-10": [
        {"category": "PROCESS", "title": "Supplier risk assessment",
         "description": "Assess cybersecurity risks associated with critical suppliers and supply chain dependencies."},
    ],

    # =========================================================================
    # PR - PROTECT
    # =========================================================================

    # PR.AA - Identity Management, Authentication, and Access Control
    "PR.AA-01": [
        {"category": "POLICY", "title": "Identity management policy",
         "description": "Establish a policy governing identity lifecycle management including provisioning, review, and deprovisioning."},
        {"category": "PROCESS", "title": "Identity lifecycle process",
         "description": "Define processes for creating, modifying, disabling, and removing identities across all systems."},
    ],
    "PR.AA-02": [
        {"category": "POLICY", "title": "Authentication policy",
         "description": "Define authentication requirements including MFA, password complexity, and session management standards."},
    ],
    "PR.AA-03": [
        {"category": "PROCESS", "title": "Access provisioning process",
         "description": "Establish a formal access request, approval, and provisioning workflow with documented approvals."},
        {"category": "PROCESS", "title": "Periodic access reviews",
         "description": "Conduct regular access reviews (e.g., quarterly) to validate that access rights remain appropriate."},
    ],
    "PR.AA-04": [
        {"category": "POLICY", "title": "Least privilege policy",
         "description": "Establish a policy requiring least privilege access and separation of duties for all systems."},
    ],
    "PR.AA-05": [
        {"category": "POLICY", "title": "Network access control policy",
         "description": "Define policies for network segmentation, access control, and authorized network connections."},
    ],
    "PR.AA-06": [
        {"category": "POLICY", "title": "Privileged access policy",
         "description": "Establish specific policies for managing, monitoring, and auditing privileged accounts and access."},
        {"category": "PROCESS", "title": "Privileged access management",
         "description": "Implement processes for just-in-time privileged access, session recording, and regular privileged account reviews."},
    ],

    # PR.AT - Awareness and Training
    "PR.AT-01": [
        {"category": "TRAINING", "title": "Security awareness program",
         "description": "Establish a security awareness and training program for all personnel, including role-based training for privileged users."},
        {"category": "DOCUMENTATION", "title": "Training records",
         "description": "Maintain records of training completion, including dates, attendees, and content covered."},
    ],
    "PR.AT-02": [
        {"category": "TRAINING", "title": "Privileged user training",
         "description": "Provide specialized training for users with privileged roles covering their specific security responsibilities."},
    ],

    # PR.DS - Data Security
    "PR.DS-01": [
        {"category": "POLICY", "title": "Data-at-rest protection policy",
         "description": "Define requirements for protecting data at rest, including encryption standards and key management procedures."},
    ],
    "PR.DS-02": [
        {"category": "POLICY", "title": "Data-in-transit protection policy",
         "description": "Define requirements for protecting data in transit, including TLS standards and certificate management."},
    ],
    "PR.DS-10": [
        {"category": "POLICY", "title": "Data disposal policy",
         "description": "Define requirements for secure data disposal and media sanitization when data is no longer needed."},
        {"category": "PROCESS", "title": "Data disposal procedures",
         "description": "Establish procedures for verifying data destruction and maintaining disposal records."},
    ],
    "PR.DS-11": [
        {"category": "POLICY", "title": "Backup policy",
         "description": "Define backup requirements including frequency, retention, encryption, and testing schedules."},
        {"category": "PROCESS", "title": "Backup testing process",
         "description": "Establish a schedule for testing backup restoration to verify data recoverability."},
    ],

    # PR.IR - Technology Infrastructure Resilience
    "PR.IR-01": [
        {"category": "POLICY", "title": "Infrastructure resilience policy",
         "description": "Define requirements for infrastructure redundancy, failover, and resilience aligned with business continuity objectives."},
    ],
    "PR.IR-02": [
        {"category": "POLICY", "title": "Configuration management policy",
         "description": "Establish standards for secure baseline configurations and change management processes."},
        {"category": "PROCESS", "title": "Configuration change control",
         "description": "Define a change control process for infrastructure modifications including review, approval, and rollback procedures."},
    ],
    "PR.IR-03": [
        {"category": "PROCESS", "title": "Capacity planning",
         "description": "Establish capacity planning processes to maintain availability and performance under expected and peak conditions."},
    ],
    "PR.IR-04": [
        {"category": "POLICY", "title": "Recovery planning policy",
         "description": "Define recovery time objectives (RTO) and recovery point objectives (RPO) for critical systems."},
        {"category": "DOCUMENTATION", "title": "Disaster recovery plan",
         "description": "Maintain documented disaster recovery and business continuity plans with defined roles and procedures."},
    ],

    # PR.PS - Platform Security
    "PR.PS-01": [
        {"category": "PROCESS", "title": "Configuration management process",
         "description": "Establish processes for maintaining secure configurations across all platforms and systems."},
    ],
    "PR.PS-02": [
        {"category": "POLICY", "title": "Software management policy",
         "description": "Define policies for software installation, updates, and removal including approved software lists."},
    ],
    "PR.PS-03": [
        {"category": "PROCESS", "title": "Hardware lifecycle management",
         "description": "Establish processes for hardware provisioning, maintenance, and secure decommissioning."},
    ],
    "PR.PS-04": [
        {"category": "PROCESS", "title": "Log management process",
         "description": "Define log generation, collection, retention, and review requirements for security-relevant events."},
        {"category": "POLICY", "title": "Logging policy",
         "description": "Establish a policy defining what events must be logged, retention periods, and access controls for log data."},
    ],
    "PR.PS-05": [
        {"category": "PROCESS", "title": "Secure development lifecycle",
         "description": "Integrate security into the software development lifecycle including code review, testing, and deployment practices."},
    ],
    "PR.PS-06": [
        {"category": "PROCESS", "title": "Secure deployment process",
         "description": "Establish secure deployment practices including integrity verification and rollback capabilities."},
    ],

    # =========================================================================
    # DE - DETECT
    # =========================================================================

    # DE.AE - Adverse Event Analysis
    "DE.AE-02": [
        {"category": "PROCESS", "title": "Event analysis process",
         "description": "Establish processes for analyzing detected adverse events to understand attack targets and methods."},
    ],
    "DE.AE-03": [
        {"category": "PROCESS", "title": "Event correlation process",
         "description": "Define processes for correlating events from multiple sources to identify potential security incidents."},
    ],
    "DE.AE-04": [
        {"category": "PROCESS", "title": "Impact estimation process",
         "description": "Establish procedures for estimating the impact and scope of adverse events."},
    ],
    "DE.AE-06": [
        {"category": "PROCESS", "title": "Incident declaration criteria",
         "description": "Define criteria and thresholds for declaring a security incident based on event analysis."},
        {"category": "DOCUMENTATION", "title": "Incident classification scheme",
         "description": "Maintain a documented incident classification and severity scheme."},
    ],
    "DE.AE-07": [
        {"category": "PROCESS", "title": "Threat intelligence integration",
         "description": "Integrate cyber threat intelligence into event analysis to improve detection accuracy."},
    ],
    "DE.AE-08": [
        {"category": "PROCESS", "title": "False positive management",
         "description": "Establish processes for identifying, documenting, and reducing false positive detections."},
    ],

    # DE.CM - Continuous Monitoring
    "DE.CM-01": [
        {"category": "POLICY", "title": "Continuous monitoring policy",
         "description": "Establish a policy defining continuous monitoring requirements, scope, and responsibilities."},
        {"category": "PROCESS", "title": "Monitoring operations",
         "description": "Define operational procedures for monitoring networks and systems for cybersecurity events."},
    ],
    "DE.CM-02": [
        {"category": "PROCESS", "title": "Physical environment monitoring",
         "description": "Establish monitoring for the physical environment of critical IT infrastructure."},
    ],
    "DE.CM-03": [
        {"category": "PROCESS", "title": "Personnel activity monitoring",
         "description": "Define processes for monitoring personnel activity to detect potential cybersecurity events."},
        {"category": "POLICY", "title": "Acceptable use policy",
         "description": "Establish acceptable use policies that define monitored activities and user expectations."},
    ],
    "DE.CM-06": [
        {"category": "PROCESS", "title": "External service monitoring",
         "description": "Monitor external service provider activities for cybersecurity events."},
    ],
    "DE.CM-09": [
        {"category": "PROCESS", "title": "Endpoint monitoring",
         "description": "Establish endpoint detection and monitoring processes across computing devices."},
    ],

    # =========================================================================
    # RS - RESPOND
    # =========================================================================

    # RS.AN - Incident Analysis
    "RS.AN-03": [
        {"category": "PROCESS", "title": "Forensic analysis process",
         "description": "Establish forensic analysis procedures for investigating security incidents, including evidence preservation."},
    ],
    "RS.AN-06": [
        {"category": "PROCESS", "title": "Incident investigation process",
         "description": "Define procedures for investigating incidents to determine root cause and scope of impact."},
    ],
    "RS.AN-07": [
        {"category": "PROCESS", "title": "Artifact collection process",
         "description": "Establish procedures for collecting and preserving incident artifacts and forensic evidence."},
    ],
    "RS.AN-08": [
        {"category": "PROCESS", "title": "Incident severity assessment",
         "description": "Define criteria for assessing incident severity and escalation thresholds."},
    ],

    # RS.CO - Incident Response Reporting and Communication
    "RS.CO-02": [
        {"category": "PROCESS", "title": "Internal incident reporting",
         "description": "Establish internal incident reporting procedures including escalation paths and notification timelines."},
        {"category": "DOCUMENTATION", "title": "Incident communication templates",
         "description": "Maintain pre-approved communication templates for different incident severity levels."},
    ],
    "RS.CO-03": [
        {"category": "PROCESS", "title": "External incident reporting",
         "description": "Define procedures for reporting incidents to external stakeholders, regulators, and law enforcement as required."},
        {"category": "DOCUMENTATION", "title": "Regulatory notification requirements",
         "description": "Document regulatory notification requirements and timelines for each applicable jurisdiction."},
    ],

    # RS.MA - Incident Management
    "RS.MA-01": [
        {"category": "POLICY", "title": "Incident response policy",
         "description": "Establish a formal incident response policy defining roles, responsibilities, and procedures."},
        {"category": "DOCUMENTATION", "title": "Incident response plan",
         "description": "Maintain a documented incident response plan with playbooks for common incident types."},
    ],
    "RS.MA-02": [
        {"category": "PROCESS", "title": "Incident triage process",
         "description": "Define triage procedures for categorizing and prioritizing incidents based on severity and impact."},
    ],
    "RS.MA-03": [
        {"category": "PROCESS", "title": "Incident tracking process",
         "description": "Establish processes for tracking incidents from detection through resolution and closure."},
    ],
    "RS.MA-04": [
        {"category": "PROCESS", "title": "Incident escalation process",
         "description": "Define escalation procedures including criteria, timelines, and escalation contacts."},
    ],
    "RS.MA-05": [
        {"category": "PROCESS", "title": "Post-incident review",
         "description": "Conduct post-incident reviews (lessons learned) to identify improvements and update response procedures."},
    ],

    # RS.MI - Incident Mitigation
    "RS.MI-01": [
        {"category": "PROCESS", "title": "Containment procedures",
         "description": "Define containment strategies and procedures for limiting the impact of security incidents."},
    ],
    "RS.MI-02": [
        {"category": "PROCESS", "title": "Eradication and recovery procedures",
         "description": "Establish procedures for eradicating threats and recovering affected systems to normal operations."},
    ],

    # =========================================================================
    # RC - RECOVER
    # =========================================================================

    # RC.CO - Recovery Communication
    "RC.CO-03": [
        {"category": "PROCESS", "title": "Recovery status communication",
         "description": "Establish procedures for communicating recovery status to internal and external stakeholders."},
    ],
    "RC.CO-04": [
        {"category": "PROCESS", "title": "Public communication procedures",
         "description": "Define procedures for public communications during and after recovery, including media coordination."},
    ],

    # RC.RP - Recovery Planning
    "RC.RP-01": [
        {"category": "DOCUMENTATION", "title": "Recovery plan",
         "description": "Maintain a documented recovery plan that is executed during or after a cybersecurity incident."},
        {"category": "PROCESS", "title": "Recovery plan activation",
         "description": "Define criteria and procedures for activating the recovery plan."},
    ],
    "RC.RP-02": [
        {"category": "PROCESS", "title": "Recovery prioritization",
         "description": "Establish priorities for restoring systems and services based on business criticality and impact."},
    ],
    "RC.RP-03": [
        {"category": "PROCESS", "title": "Recovery verification",
         "description": "Define procedures for verifying the integrity of restored systems and data before returning to normal operations."},
    ],
    "RC.RP-04": [
        {"category": "PROCESS", "title": "Recovery plan testing",
         "description": "Establish a schedule for testing recovery plans through exercises, drills, or simulations."},
    ],
    "RC.RP-05": [
        {"category": "PROCESS", "title": "Recovery plan updates",
         "description": "Update recovery plans based on lessons learned from incidents, tests, and changes to the environment."},
    ],
    "RC.RP-06": [
        {"category": "DOCUMENTATION", "title": "Recovery documentation",
         "description": "Document recovery actions taken, timelines, and outcomes for post-incident review and audit purposes."},
    ],
}


# Category display metadata
CATEGORY_LABELS: Dict[str, Dict[str, str]] = {
    "POLICY": {"label": "Policy", "icon": "file-open", "color": "#0073BB"},
    "PROCESS": {"label": "Process", "icon": "settings", "color": "#037F0C"},
    "GOVERNANCE": {"label": "Governance", "icon": "user-profile", "color": "#6B40B8"},
    "TRAINING": {"label": "Training", "icon": "contact", "color": "#D45B07"},
    "DOCUMENTATION": {"label": "Documentation", "icon": "edit", "color": "#00838F"},
    "THIRD_PARTY": {"label": "Third-party", "icon": "share", "color": "#687078"},
}


def get_organizational_requirements(subcategory_id: str) -> List[Dict[str, str]]:
    """Get organizational requirements for a CSF subcategory.

    Args:
        subcategory_id: CSF subcategory ID (e.g., "GV.PO-01")

    Returns:
        List of requirement dicts with category, title, and description.
        Returns empty list if no requirements are defined.
    """
    return CSF_ORGANIZATIONAL_REQUIREMENTS.get(subcategory_id.upper(), [])


def get_category_metadata() -> Dict[str, Dict[str, str]]:
    """Get display metadata for organizational requirement categories."""
    return CATEGORY_LABELS
