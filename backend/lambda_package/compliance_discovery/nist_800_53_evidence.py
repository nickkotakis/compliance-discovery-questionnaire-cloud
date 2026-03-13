"""Control-specific evidence questions for NIST 800-53 Rev 5.

Each control maps to a specific evidence question that explains what artifacts
an assessor would expect to see, with concrete examples of acceptable evidence
and hints about where to find them in AWS.

These override the generic family-level evidence templates and the auto-generated
evidence questions in control_questions.py.
"""

from typing import Optional

NIST_800_53_EVIDENCE: dict[str, str] = {

    # =========================================================================
    # AC — Access Control
    # =========================================================================

    "AC-1": "Provide your access control policy and procedures document showing: (1) who approved it and when it was last reviewed, (2) how it addresses AWS IAM, federation, and least privilege, (3) version history showing it's updated at least annually. Assessors want to see a living document, not a shelf document.",

    "AC-2": "Provide: (1) IAM credential report showing all users, MFA status, and last login dates, (2) evidence of your account provisioning and deprovisioning process — show a recent new hire getting access and a terminated employee being removed, (3) IAM Access Analyzer report showing unused permissions identified and remediated, (4) periodic access review records with dates and reviewer names.",

    "AC-3": "Provide: (1) IAM policies for your key roles showing least-privilege scoping (no wildcard actions on wildcard resources), (2) SCP policies from AWS Organizations showing account-level guardrails, (3) S3 bucket policies or resource policies demonstrating access restrictions on sensitive data, (4) evidence of a denied access attempt in CloudTrail showing enforcement works.",

    "AC-4": "Provide: (1) VPC architecture diagram showing network segmentation and data flow paths, (2) security group and NACL configurations showing traffic restrictions between segments, (3) VPC Flow Log analysis showing only approved traffic patterns, (4) AWS Network Firewall or WAF rules controlling information flow at boundaries.",

    "AC-5": "Provide: (1) separation of duties matrix showing which roles are incompatible, (2) IAM role definitions showing different people hold different roles (e.g., deployer vs. approver), (3) evidence from your CI/CD pipeline showing code requires a different person to approve than the author, (4) SCP or permission boundary preventing a single role from having both read and write access to sensitive resources.",

    "AC-6": "Provide: (1) IAM Access Analyzer findings showing you've identified and removed unused permissions, (2) IAM policies for privileged roles showing they're scoped to specific resources and actions, (3) evidence that root account access keys are deleted and root usage triggers alerts, (4) CloudTrail logs showing privileged actions are attributed to specific individuals.",

    "AC-7": "Provide: (1) identity provider configuration showing account lockout thresholds (e.g., lock after 5 failed attempts for 30 minutes), (2) GuardDuty findings or CloudWatch alarms configured to detect brute-force login attempts, (3) evidence of a test showing lockout actually triggers after the defined number of failures.",

    "AC-8": "Provide: (1) screenshots of system use notification banners on all login screens — AWS console (via custom SAML landing page), VPN portal, bastion hosts, and WorkSpaces, (2) banner text content showing it includes authorized use, monitoring consent, and legal warnings, (3) policy requiring banners on all systems.",

    "AC-11": "Provide: (1) Group Policy or MDM configuration showing screen lock timeout (e.g., 15 minutes), (2) WorkSpaces or remote desktop timeout settings, (3) evidence that locked screens conceal all content — a screenshot of the lock screen itself.",

    "AC-12": "Provide: (1) application session timeout configurations (web apps, SSH, RDP), (2) IAM role maximum session duration settings, (3) load balancer idle timeout configurations, (4) evidence of a session being automatically terminated after the defined inactivity period.",

    "AC-14": "Provide: (1) documented list of actions permitted without authentication (e.g., public website, health check endpoints), (2) evidence these unauthenticated endpoints don't expose sensitive data, (3) architecture diagram showing which components are public vs. authenticated.",

    "AC-17": "Provide: (1) VPN or Systems Manager Session Manager configuration showing encrypted remote access, (2) CloudTrail or Session Manager logs showing remote session activity with user attribution, (3) MFA enforcement evidence for remote access, (4) security group rules showing remote access ports are restricted to VPN/bastion only.",

    "AC-18": "Provide: (1) wireless access point inventory and configuration showing WPA2-Enterprise or WPA3, (2) wireless network segmentation evidence (separate SSIDs for corporate vs. guest), (3) 802.1X authentication configuration, (4) rogue access point scan results.",

    "AC-19": "Provide: (1) MDM enrollment report showing managed devices with encryption and screen lock enforced, (2) mobile device policy document, (3) evidence of remote wipe capability, (4) list of approved mobile device types and OS versions.",

    "AC-20": "Provide: (1) inventory of external system connections with security agreements (ISAs/MOUs), (2) VPC peering or Transit Gateway configurations showing controlled external connections, (3) security group rules restricting traffic to approved external endpoints, (4) periodic review records of external system connections.",

    "AC-21": "Provide: (1) information sharing policy defining what can be shared and with whom, (2) S3 cross-account access configurations with scoped IAM roles, (3) pre-signed URL configurations with expiration settings, (4) data sharing agreement templates used with partners.",

    "AC-22": "Provide: (1) S3 Block Public Access configuration at the account level, (2) AWS Config rules S3_BUCKET_PUBLIC_READ_PROHIBITED and S3_BUCKET_PUBLIC_WRITE_PROHIBITED showing compliance, (3) Amazon Macie scan results for publicly accessible sensitive data, (4) content review process documentation for public-facing systems.",

    # =========================================================================
    # AT — Awareness and Training
    # =========================================================================

    "AT-1": "Provide: (1) security awareness and training policy with approval signatures and review date, (2) training curriculum covering AWS-specific topics (IAM, phishing, data handling), (3) annual training schedule, (4) evidence the policy is reviewed and updated at least annually.",

    "AT-2": "Provide: (1) training completion records showing percentage of staff trained (target: 100%), (2) training content covering phishing, social engineering, password security, and CUI handling, (3) phishing simulation results and trend data, (4) follow-up records for employees who failed simulations.",

    "AT-3": "Provide: (1) role-based training curriculum for privileged users (AWS admins, security analysts), (2) completion records showing cloud administrators received AWS security training (IAM, CloudTrail, GuardDuty), (3) AWS certification records if applicable, (4) hands-on lab completion records.",

    "AT-4": "Provide: (1) training records database or LMS showing individual completion dates and scores, (2) evidence records are retained for the required period, (3) reports showing training compliance by department or role.",

    # =========================================================================
    # AU — Audit and Accountability
    # =========================================================================

    "AU-1": "Provide: (1) audit and accountability policy with approval signatures, (2) procedures defining what events to log, retention periods, and log protection requirements, (3) evidence the policy addresses CloudTrail, CloudWatch, VPC Flow Logs, and application logging, (4) annual review records.",

    "AU-2": "Provide: (1) list of auditable events your organization has defined (logins, privilege use, config changes, data access), (2) CloudTrail configuration showing management and data events are captured, (3) evidence of periodic review of which events are logged — meeting minutes or change records showing the event list was updated.",

    "AU-3": "Provide: (1) sample CloudTrail log entries showing they contain: who (userIdentity), what (eventName), when (eventTime), where (sourceIPAddress, awsRegion), and outcome (errorCode or responseElements), (2) application log samples showing similar detail, (3) evidence that log format meets your audit requirements.",

    "AU-4": "Provide: (1) S3 bucket storage metrics for CloudTrail log buckets showing adequate capacity, (2) S3 lifecycle policies transitioning older logs to Glacier, (3) CloudWatch Logs retention period configurations, (4) monitoring or alerts for storage capacity thresholds.",

    "AU-5": "Provide: (1) CloudWatch alarm or EventBridge rule configured to detect CloudTrail being stopped or modified, (2) SCP preventing CloudTrail deletion (show the policy JSON), (3) evidence of a test or actual alert firing when logging was disrupted, (4) escalation procedures for logging failures.",

    "AU-6": "Provide: (1) log review schedule and records showing who reviews logs and how often, (2) CloudWatch Logs Insights or Athena queries used for routine log analysis, (3) Security Hub finding triage records showing how findings are investigated, (4) sample investigation report from a recent security event showing logs were correlated.",

    "AU-7": "Provide: (1) demonstration of on-demand report generation — run an Athena query on CloudTrail or a CloudWatch Logs Insights query and show the results, (2) SIEM dashboard screenshots showing audit data visualization, (3) sample reports generated for a recent audit or investigation.",

    "AU-8": "Provide: (1) NTP configuration on servers showing synchronization to an authoritative source (Amazon Time Sync Service for EC2), (2) evidence that on-premises systems sync to the same time source, (3) monitoring configuration that alerts on time drift, (4) sample log entries from different systems showing consistent timestamps.",

    "AU-9": "Provide: (1) S3 bucket configuration for CloudTrail logs showing Object Lock or versioning enabled, (2) IAM policies showing only the security team can access log buckets, (3) separate logging account in AWS Organizations that application teams cannot access, (4) evidence that log integrity validation is enabled on CloudTrail.",

    "AU-11": "Provide: (1) log retention policy document specifying retention periods by log type, (2) S3 lifecycle policy configurations showing retention enforcement, (3) CloudWatch Logs retention period settings, (4) evidence that logs from the required retention period are actually accessible — pull a log entry from 12 months ago.",

    "AU-12": "Provide: (1) CloudTrail configuration showing multi-region trail with management events and data events enabled, (2) list of additional log sources enabled (VPC Flow Logs, S3 access logs, RDS audit logs, application logs), (3) evidence that new services deployed get logging configured as part of the deployment process.",

    # =========================================================================
    # CA — Security Assessment and Authorization
    # =========================================================================

    "CA-1": "Provide: (1) security assessment and authorization policy with approval signatures, (2) procedures for conducting assessments, managing POA&Ms, and granting ATOs, (3) evidence the policy is reviewed annually and updated when significant changes occur.",

    "CA-2": "Provide: (1) most recent security assessment report with findings and recommendations, (2) assessment plan showing scope, methodology, and assessor qualifications, (3) Security Hub compliance scores or AWS Audit Manager assessment results used as assessment inputs.",

    "CA-3": "Provide: (1) inventory of system interconnections with other organizations or systems, (2) interconnection security agreements (ISAs) or memoranda of understanding (MOUs), (3) VPC peering, Transit Gateway, or Direct Connect configurations showing controlled interconnections, (4) periodic review records of interconnection agreements.",

    "CA-5": "Provide: (1) Plan of Action and Milestones (POA&M) document with all open items, (2) each POA&M entry should show: finding description, owner, target date, status, and milestones, (3) evidence of regular POA&M reviews (meeting minutes or status updates), (4) closed POA&M items with completion evidence.",

    "CA-6": "Provide: (1) Authorization to Operate (ATO) letter or equivalent approval document, (2) authorizing official's name and signature, (3) authorization boundary documentation, (4) conditions of authorization and any risk acceptance statements.",

    "CA-7": "Provide: (1) continuous monitoring strategy document, (2) AWS Config rules running continuously with compliance dashboards, (3) Security Hub enabled with automated finding aggregation, (4) GuardDuty and Inspector providing ongoing threat and vulnerability monitoring, (5) monthly or quarterly security metrics reports showing trends.",

    "CA-8": "Provide: (1) most recent penetration test report (following AWS pen test policy), (2) scope of testing including AWS resources tested, (3) remediation tracking for findings, (4) evidence of periodic testing schedule (at least annually).",

    "CA-9": "Provide: (1) inventory of internal system connections, (2) architecture diagrams showing VPC-to-VPC, account-to-account, and service-to-service connections, (3) security group and IAM role configurations governing internal connections, (4) approval records for new internal connections.",

    # =========================================================================
    # CM — Configuration Management
    # =========================================================================

    "CM-1": "Provide: (1) configuration management policy with approval signatures, (2) procedures for baseline management, change control, and configuration monitoring, (3) evidence the policy addresses AWS resource configuration management using Config, CloudFormation, or CDK.",

    "CM-2": "Provide: (1) documented baseline configurations for your system types (EC2 AMIs, container images, network configurations), (2) AWS Config resource inventory showing tracked resources, (3) CloudFormation or CDK templates representing your infrastructure baseline, (4) evidence baselines are updated when significant changes occur.",

    "CM-3": "Provide: (1) change management process documentation with approval workflows, (2) recent change request records showing the full lifecycle (request, review, approve, implement, verify), (3) CloudTrail logs showing who made configuration changes and when, (4) CloudFormation change sets or git commit history showing infrastructure changes are version-controlled.",

    "CM-4": "Provide: (1) security impact analysis procedures, (2) recent change requests showing a security review was performed before approval, (3) evidence of testing changes in a non-production environment before deploying to production.",

    "CM-5": "Provide: (1) IAM roles showing who has permission to modify production systems, (2) evidence that production changes require approval from someone other than the requester, (3) SCP or IAM policies preventing unauthorized users from modifying production resources, (4) CloudTrail logs showing change activity attributed to authorized personnel.",

    "CM-6": "Provide: (1) security configuration standards you follow (CIS Benchmarks, AWS FSBP, STIGs), (2) Security Hub compliance report showing CIS or FSBP standard results, (3) AWS Config rule compliance reports for configuration checks, (4) evidence of automated remediation for common misconfigurations.",

    "CM-7": "Provide: (1) list of approved AWS services and ports/protocols, (2) SCPs restricting unapproved services or regions, (3) security group configurations showing only required ports are open, (4) evidence of disabled or removed unnecessary services on EC2 instances.",

    "CM-8": "Provide: (1) AWS Config resource inventory showing all tracked resources, (2) Systems Manager Inventory reports for EC2 instances, (3) evidence the inventory is reconciled periodically — compare Config inventory to what's actually running, (4) tagging compliance reports showing resources are properly labeled.",

    "CM-9": "Provide: (1) configuration management plan document, (2) roles and responsibilities for configuration management, (3) evidence the plan covers AWS resource lifecycle from provisioning through decommissioning.",

    "CM-10": "Provide: (1) software licensing policy, (2) AWS License Manager configuration and compliance reports, (3) inventory of commercial software running on EC2 with license tracking.",

    "CM-11": "Provide: (1) user-installed software policy, (2) endpoint management configuration restricting software installation, (3) Systems Manager Inventory reports showing installed software on managed instances, (4) evidence of monitoring for unauthorized software installations.",

    "CM-12": "Provide: (1) data inventory showing where sensitive data resides in AWS (which S3 buckets, RDS instances, DynamoDB tables), (2) Amazon Macie sensitive data discovery reports, (3) data flow diagrams showing how data moves between services, (4) evidence the inventory is updated when new data stores are created.",

    # =========================================================================
    # CP — Contingency Planning
    # =========================================================================

    "CP-1": "Provide: (1) contingency planning policy with approval signatures, (2) procedures for backup, recovery, and business continuity, (3) evidence the policy addresses AWS-specific recovery (AWS Backup, cross-Region replication, CloudFormation redeployment).",

    "CP-2": "Provide: (1) contingency plan document with recovery procedures for your AWS workloads, (2) RTOs and RPOs for critical systems, (3) contact lists and escalation procedures, (4) evidence the plan is reviewed and updated at least annually.",

    "CP-3": "Provide: (1) contingency training records for personnel with recovery responsibilities, (2) training materials covering AWS Backup restoration, DR region failover, and CloudFormation redeployment, (3) evidence training is refreshed when the contingency plan changes.",

    "CP-4": "Provide: (1) contingency plan test records with dates, participants, and scenarios, (2) test results showing whether RTOs and RPOs were met, (3) after-action reports with improvement recommendations, (4) evidence of AWS-specific testing (backup restoration, failover to DR region).",

    "CP-6": "Provide: (1) alternate storage site documentation (separate AWS Region, separate account, or off-site), (2) S3 Cross-Region Replication configuration, (3) AWS Backup cross-Region copy rules, (4) evidence the alternate site is geographically separated from the primary.",

    "CP-7": "Provide: (1) alternate processing site documentation (DR Region architecture), (2) evidence of warm standby, pilot light, or multi-Region deployment, (3) failover test records showing the alternate site can actually take over, (4) RTO/RPO validation results.",

    "CP-8": "Provide: (1) network connectivity architecture showing redundancy (dual Direct Connect, VPN backup), (2) evidence of diverse network paths to AWS, (3) failover test records for network connectivity.",

    "CP-9": "Provide: (1) AWS Backup policy configurations showing backup schedules and retention, (2) backup completion reports showing successful backups, (3) backup restoration test records with dates and results, (4) Backup Vault Lock configuration if applicable, (5) KMS key configuration for backup encryption.",

    "CP-10": "Provide: (1) system recovery procedures document, (2) evidence of a recent recovery test — restoring from AWS Backup, redeploying from CloudFormation/CDK, or failing over to DR, (3) post-recovery verification checklist showing the restored system was validated before returning to production.",

    # =========================================================================
    # IA — Identification and Authentication
    # =========================================================================

    "IA-1": "Provide: (1) identification and authentication policy with approval signatures, (2) procedures covering user identification, authentication methods, MFA requirements, and credential management, (3) evidence the policy addresses AWS IAM, federation, and service authentication.",

    "IA-2": "Provide: (1) IAM Identity Center or federation configuration showing how users authenticate, (2) IAM credential report showing MFA is enabled for all console users, (3) evidence that privileged users use hardware MFA tokens or FIDO2 keys, (4) root account MFA configuration evidence.",

    "IA-3": "Provide: (1) device authentication policy, (2) certificate-based or 802.1X authentication configuration for network devices, (3) IoT device authentication configuration if applicable, (4) evidence that unauthenticated devices cannot access the network.",

    "IA-4": "Provide: (1) identifier management procedures covering creation, assignment, and deactivation, (2) IAM credential report showing no shared or generic accounts, (3) evidence of identifier reuse prevention — policy or IdP configuration showing deactivated usernames cannot be immediately reassigned.",

    "IA-5": "Provide: (1) password policy configuration in your identity provider showing complexity requirements (length, character types), (2) IAM account password policy settings, (3) evidence of password history enforcement (e.g., last 24 passwords), (4) Secrets Manager or Parameter Store usage for application credentials instead of hardcoded secrets.",

    "IA-6": "Provide: (1) screenshots of login screens showing password masking (dots/asterisks), (2) evidence that error messages don't reveal whether the username or password was incorrect, (3) application configuration showing authentication feedback is obscured.",

    "IA-7": "Provide: (1) inventory of cryptographic modules used for authentication, (2) FIPS 140-2 validation certificates for modules protecting authentication data, (3) AWS FIPS endpoint configuration for API calls, (4) KMS key configuration showing FIPS-validated HSM backing.",

    "IA-8": "Provide: (1) external user authentication policy, (2) cross-account IAM role configurations with external ID conditions for partner access, (3) Amazon Cognito configuration for customer-facing authentication, (4) SAML/OIDC federation configuration for external identity providers.",

    "IA-11": "Provide: (1) re-authentication policy defining when users must re-authenticate, (2) application configurations enforcing re-authentication for sensitive actions, (3) session timeout configurations that force re-authentication after inactivity.",

    "IA-12": "Provide: (1) identity proofing procedures document, (2) evidence of identity verification performed during onboarding (government ID check, in-person verification), (3) enhanced verification records for privileged access recipients.",

    # =========================================================================
    # IR — Incident Response
    # =========================================================================

    "IR-1": "Provide: (1) incident response policy with approval signatures, (2) procedures covering detection, analysis, containment, eradication, and recovery, (3) evidence the policy addresses AWS-specific incidents (compromised credentials, S3 exposure, unauthorized EC2), (4) annual review records.",

    "IR-2": "Provide: (1) incident response training curriculum, (2) training completion records for IR team members, (3) evidence training covers AWS-specific scenarios (GuardDuty triage, CloudTrail forensics, credential compromise response), (4) training refresh records after plan updates.",

    "IR-3": "Provide: (1) incident response test schedule, (2) tabletop exercise or simulation records with dates, participants, and scenarios, (3) after-action reports with lessons learned, (4) plan updates made based on exercise findings.",

    "IR-4": "Provide: (1) incident handling procedures with step-by-step runbooks, (2) recent incident records showing the full lifecycle (detect, analyze, contain, eradicate, recover), (3) GuardDuty and Security Hub integration evidence showing automated detection feeds into your IR process, (4) post-incident review reports.",

    "IR-5": "Provide: (1) incident tracking system or log showing all security incidents, (2) incident metrics (number of incidents, mean time to detect, mean time to resolve), (3) Security Hub workflow status records showing incident triage, (4) trend analysis showing incident patterns over time.",

    "IR-6": "Provide: (1) incident reporting procedures with defined timelines and recipients, (2) evidence of recent incident reports sent to management, (3) regulatory notification procedures and evidence of compliance (e.g., 72-hour GDPR notification), (4) contact lists for external reporting (law enforcement, regulators, CISA).",

    "IR-7": "Provide: (1) incident response assistance resources documentation, (2) AWS Support plan details (Enterprise/Business tier), (3) third-party IR retainer agreements, (4) contact information for assistance resources accessible during emergencies.",

    "IR-8": "Provide: (1) incident response plan document with version history, (2) plan distribution records showing relevant personnel have current copies, (3) plan update records triggered by incidents, exercises, or organizational changes.",

    # =========================================================================
    # MA — Maintenance
    # =========================================================================

    "MA-1": "Provide: (1) maintenance policy with approval signatures, (2) procedures for scheduled and unscheduled maintenance, (3) evidence the policy addresses AWS patching (Systems Manager Patch Manager) and maintenance windows.",

    "MA-2": "Provide: (1) maintenance schedule and records, (2) Systems Manager Patch Manager compliance reports, (3) maintenance window configurations, (4) evidence that maintenance activities are logged and reviewed.",

    "MA-3": "Provide: (1) approved maintenance tools inventory, (2) tool integrity verification procedures, (3) evidence that maintenance tools are inspected before use on production systems.",

    "MA-4": "Provide: (1) remote maintenance policy requiring MFA and encryption, (2) Systems Manager Session Manager configuration and logs, (3) VPN or secure remote access configuration for maintenance, (4) session termination evidence after maintenance completion.",

    "MA-5": "Provide: (1) maintenance personnel authorization records, (2) escort and supervision logs for unauthorized maintenance personnel, (3) background check records for maintenance staff with system access.",

    # =========================================================================
    # MP — Media Protection
    # =========================================================================

    "MP-1": "Provide: (1) media protection policy with approval signatures, (2) procedures for media handling, storage, transport, and sanitization, (3) evidence the policy addresses both physical media and AWS digital storage (S3, EBS, backups).",

    "MP-2": "Provide: (1) media access authorization records, (2) S3 bucket policies and IAM roles restricting access to sensitive data, (3) physical media storage access logs, (4) evidence of periodic access reviews for media storage.",

    "MP-6": "Provide: (1) media sanitization procedures referencing NIST SP 800-88, (2) sanitization records with method, date, and personnel, (3) destruction certificates for physically destroyed media, (4) AWS SOC reports documenting AWS media sanitization for cloud resources.",

    "MP-7": "Provide: (1) removable media policy, (2) USB device control configuration (Group Policy, endpoint protection), (3) enforcement logs showing blocked unauthorized devices, (4) approved removable media inventory if exceptions exist.",

    # =========================================================================
    # PE — Physical and Environmental Protection
    # =========================================================================

    "PE-1": "Provide: (1) physical security policy acknowledging AWS shared responsibility (AWS secures data centers, you secure access to AWS services), (2) AWS Artifact SOC reports documenting AWS physical security, (3) on-premises physical security procedures if applicable.",

    "PE-4": "Provide: (1) for Direct Connect or hybrid connections — physical protection evidence for transmission lines (locked cabinets, conduits), (2) AWS Artifact SOC reports for AWS-side physical security, (3) on-premises network cable security evidence.",

    "PE-17": "Provide: (1) remote work security policy, (2) VPN or secure access configuration for remote workers, (3) endpoint security requirements (encryption, antivirus, patching), (4) signed telework agreements.",

    # =========================================================================
    # PL — Planning
    # =========================================================================

    "PL-1": "Provide: (1) security planning policy with approval signatures, (2) procedures for developing and maintaining system security plans, (3) annual review records.",

    "PL-2": "Provide: (1) System Security Plan (SSP) document covering system boundaries, environment description, and security control implementation, (2) AWS architecture diagrams within the SSP, (3) SSP version history showing periodic updates, (4) evidence the SSP is reviewed when significant changes occur.",

    "PL-4": "Provide: (1) rules of behavior document, (2) signed acknowledgment records from all users, (3) evidence rules cover acceptable use of AWS resources and data handling requirements.",

    "PL-8": "Provide: (1) security architecture document showing defense-in-depth approach, (2) AWS multi-account strategy documentation, (3) VPC design and network segmentation diagrams, (4) identity and encryption architecture documentation.",

    "PL-10": "Provide: (1) baseline selection documentation showing which NIST 800-53 baseline was chosen and why, (2) tailoring rationale for any controls added or removed from the baseline.",

    "PL-11": "Provide: (1) baseline tailoring documentation, (2) rationale for each control that was scoped out, compensated, or supplemented, (3) risk acceptance documentation for any tailoring decisions.",

    # =========================================================================
    # PM — Program Management
    # =========================================================================

    "PM-1": "Provide: (1) information security program plan, (2) program governance structure showing CISO/security team reporting, (3) program metrics and KPIs, (4) annual program review records.",

    # =========================================================================
    # RA — Risk Assessment
    # =========================================================================

    "RA-1": "Provide: (1) risk assessment policy with approval signatures, (2) risk assessment methodology documentation (NIST SP 800-30, FAIR, or custom), (3) procedures for conducting and documenting risk assessments.",

    "RA-2": "Provide: (1) system categorization documentation (FIPS 199 impact levels), (2) data classification scheme and evidence it's applied to AWS resources via tags, (3) AWS Config rules for REQUIRED_TAGS showing classification tags are enforced.",

    "RA-3": "Provide: (1) most recent risk assessment report, (2) risk register with identified risks, likelihood, impact, and risk ratings, (3) Security Hub findings and Inspector vulnerability data used as risk inputs, (4) evidence of periodic risk assessment updates (at least annually).",

    "RA-5": "Provide: (1) Amazon Inspector scan configuration and recent vulnerability reports, (2) vulnerability remediation tracking records with timelines by severity, (3) network vulnerability scan results, (4) web application scan results (OWASP Top 10), (5) evidence of scanning frequency (continuous for Inspector, periodic for network/app scans).",

    "RA-7": "Provide: (1) risk response procedures document, (2) risk register entries showing response decisions (accept, mitigate, transfer, avoid) with rationale, (3) Security Hub finding workflow status showing triage decisions, (4) risk acceptance records with approver signatures.",

    "RA-9": "Provide: (1) criticality analysis document identifying mission-critical systems, (2) business impact analysis for AWS workloads, (3) evidence that criticality drives security control selection and resource allocation.",

    # =========================================================================
    # SA — System and Services Acquisition
    # =========================================================================

    "SA-1": "Provide: (1) system and services acquisition policy, (2) procedures for security requirements in acquisitions, (3) evidence security is evaluated during vendor selection and contract negotiation.",

    "SA-2": "Provide: (1) security resource allocation documentation, (2) budget for security tools and personnel, (3) evidence security resources are included in system development lifecycle planning.",

    "SA-3": "Provide: (1) system development lifecycle (SDLC) documentation showing security integration, (2) evidence of security gates in the development process, (3) secure coding standards and code review requirements.",

    "SA-4": "Provide: (1) security requirements in acquisition contracts, (2) vendor security assessment records, (3) evidence that AWS Marketplace purchases and third-party tools undergo security review before deployment.",

    "SA-8": "Provide: (1) security engineering principles documentation, (2) evidence of threat modeling during system design, (3) AWS Well-Architected Framework security pillar review results.",

    "SA-9": "Provide: (1) external service provider inventory, (2) security requirements in service agreements, (3) SOC 2 or ISO 27001 reports from critical providers, (4) AWS Artifact compliance reports for AWS services.",

    "SA-10": "Provide: (1) configuration management for development environments, (2) evidence of separate dev/test/prod environments in AWS (separate accounts or VPCs), (3) code repository access controls and branch protection rules.",

    "SA-11": "Provide: (1) security testing procedures for developed software, (2) SAST/DAST scan results from CI/CD pipeline, (3) dependency vulnerability scan results, (4) penetration test results for custom applications.",

    "SA-16": "Provide: (1) developer-provided training materials for custom systems, (2) secure configuration guides for deployed applications, (3) training completion records for operations staff.",

    "SA-17": "Provide: (1) security architecture and design documentation, (2) threat model documents for AWS workloads, (3) evidence of security architecture review during design phase, (4) Well-Architected Framework review results.",

    # =========================================================================
    # SC — System and Communications Protection
    # =========================================================================

    "SC-1": "Provide: (1) system and communications protection policy with approval signatures, (2) procedures for boundary protection, encryption, and network security, (3) evidence the policy addresses AWS VPC design, encryption standards, and TLS requirements.",

    "SC-5": "Provide: (1) DDoS protection configuration — AWS Shield Standard (automatic) or Shield Advanced, (2) CloudFront or ALB configurations providing DDoS absorption, (3) WAF rate-limiting rules, (4) incident response procedures for DDoS events.",

    "SC-7": "Provide: (1) VPC architecture diagrams showing boundary protection at external and internal boundaries, (2) security group and NACL configurations, (3) AWS Network Firewall or WAF rule sets, (4) VPC Flow Log analysis showing traffic patterns, (5) evidence of default-deny rules at network boundaries.",

    "SC-8": "Provide: (1) TLS configuration evidence showing TLS 1.2+ enforced on all communications, (2) ACM certificate inventory, (3) ALB/CloudFront HTTPS-only listener configurations, (4) S3 bucket policies requiring aws:SecureTransport, (5) Site-to-Site VPN or Direct Connect encryption configuration.",

    "SC-12": "Provide: (1) KMS key inventory with rotation configuration, (2) key management procedures covering creation, rotation, and destruction, (3) IAM policies restricting key management to authorized personnel, (4) CloudTrail logs showing KMS key usage and management events.",

    "SC-13": "Provide: (1) FIPS 140-2 validation evidence for cryptographic modules, (2) AWS FIPS endpoint configuration, (3) KMS key configuration showing FIPS-validated HSM backing, (4) on-premises FIPS module certificates.",

    "SC-28": "Provide: (1) encryption-at-rest configuration for all storage services — S3 (SSE-KMS), EBS (encrypted volumes), RDS (storage encryption), DynamoDB (encryption), (2) AWS Config rules verifying encryption (ENCRYPTED_VOLUMES, RDS_STORAGE_ENCRYPTED, S3_BUCKET_SERVER_SIDE_ENCRYPTION_ENABLED), (3) KMS key policies showing access controls.",

    # =========================================================================
    # SI — System and Information Integrity
    # =========================================================================

    "SI-1": "Provide: (1) system and information integrity policy with approval signatures, (2) procedures for flaw remediation, malware protection, and security monitoring, (3) evidence the policy addresses AWS patching, GuardDuty, Inspector, and Security Hub.",

    "SI-2": "Provide: (1) Systems Manager Patch Manager compliance reports showing patch status, (2) patch management timelines by severity (critical within 48 hours, high within 30 days), (3) Inspector vulnerability findings and remediation tracking, (4) evidence of testing patches before production deployment.",

    "SI-3": "Provide: (1) antivirus/anti-malware deployment evidence on all endpoints and servers, (2) GuardDuty Malware Protection configuration for EC2/EBS, (3) malware signature update configuration showing automatic updates, (4) malware detection and response records from recent events.",

    "SI-4": "Provide: (1) GuardDuty configuration showing all protection types enabled, (2) VPC Flow Log monitoring configuration, (3) CloudTrail analysis for suspicious API activity, (4) SIEM or Security Hub alerting configuration, (5) sample alert and investigation records from recent monitoring events.",

    "SI-5": "Provide: (1) subscribed security alert sources (CISA, US-CERT, AWS Security Bulletins, vendor advisories), (2) alert review and triage records, (3) evidence of actions taken in response to recent advisories, (4) AWS Health and GuardDuty notification routing configuration.",

    "SI-6": "Provide: (1) security function verification procedures, (2) test records showing encryption, logging, and access controls were verified to be working, (3) automated verification evidence (Config rules checking security function status).",

    "SI-7": "Provide: (1) file integrity monitoring configuration on critical systems, (2) CloudFormation drift detection results, (3) AWS Config change tracking for critical resources, (4) code signing configuration (AWS Signer for Lambda), (5) evidence of unauthorized change detection and response.",

    "SI-8": "Provide: (1) email security configuration (SPF, DKIM, DMARC records), (2) spam filtering configuration for email services, (3) Amazon SES or WorkMail security settings if applicable.",

    "SI-10": "Provide: (1) input validation standards for applications, (2) AWS WAF configuration with OWASP managed rule group, (3) application security testing results showing input validation coverage, (4) code review records showing input validation checks.",

    "SI-11": "Provide: (1) error handling standards for applications, (2) evidence that error messages don't expose internal details (stack traces, database queries), (3) application configuration showing detailed errors go to logs while users see generic messages.",

    "SI-12": "Provide: (1) data retention and disposal policy, (2) S3 lifecycle policy configurations, (3) DynamoDB TTL settings, (4) RDS snapshot retention configurations, (5) evidence of secure data deletion when retention periods expire.",

    "SI-16": "Provide: (1) memory protection configuration on operating systems (ASLR, DEP/NX enabled), (2) EC2 instance type documentation showing Nitro-based instances, (3) AWS Nitro Enclave configuration if used for sensitive processing.",

    # =========================================================================
    # SR — Supply Chain Risk Management
    # =========================================================================

    "SR-1": "Provide: (1) supply chain risk management policy, (2) procedures for assessing and monitoring supplier security, (3) evidence the policy addresses AWS Marketplace, third-party AMIs, and open-source dependencies.",

    "SR-2": "Provide: (1) supply chain risk management plan, (2) supplier criticality assessment records, (3) evidence of supply chain risk integration into enterprise risk management.",

    "SR-3": "Provide: (1) supply chain controls documentation, (2) vendor security assessment records, (3) contract clauses requiring security controls from suppliers.",

    "SR-5": "Provide: (1) component authenticity verification procedures, (2) AMI source validation records, (3) container image signature verification configuration, (4) software composition analysis (SCA) results for open-source dependencies.",

    "SR-6": "Provide: (1) supplier assessment records, (2) SOC 2 or ISO 27001 reports from critical suppliers, (3) security questionnaire responses, (4) periodic reassessment schedule and records.",

    "SR-10": "Provide: (1) component inspection procedures, (2) evidence of security scanning for third-party components before deployment, (3) ECR image scan results for container images, (4) dependency vulnerability scan results from CI/CD pipeline.",

    "SR-11": "Provide: (1) component authenticity procedures, (2) software provenance tracking (SBOM), (3) code signing verification configuration, (4) approved component sources list.",

    "SR-12": "Provide: (1) component disposal procedures, (2) media sanitization records for decommissioned hardware, (3) AWS resource cleanup evidence (terminated instances, deleted volumes), (4) vendor data deletion confirmation records.",
}


def get_nist_evidence_question(control_id: str) -> Optional[str]:
    """Get a control-specific evidence question for a NIST 800-53 control.

    Args:
        control_id: Control ID (e.g., 'AC-2', 'AU-8')

    Returns:
        Evidence question string if exists, None otherwise
    """
    return NIST_800_53_EVIDENCE.get(control_id.upper())


def has_nist_evidence_question(control_id: str) -> bool:
    """Check if a control-specific evidence question exists."""
    return control_id.upper() in NIST_800_53_EVIDENCE
