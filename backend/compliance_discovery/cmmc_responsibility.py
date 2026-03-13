"""CMMC Level 2 shared responsibility model mapping.

Maps each CMMC practice to the appropriate AWS shared responsibility category:
- 'customer': Customer is fully responsible (policies, training, procedures, physical)
- 'shared': Both AWS and customer share responsibility (AWS provides services,
            customer must configure and use them properly)
- 'aws': AWS is primarily responsible (physical data center security)

Rationale:
- AT (Awareness/Training): Always customer — AWS doesn't train your staff
- PE (Physical Protection): Mostly AWS for cloud, customer for on-premises
- PS (Personnel Security): Always customer — AWS doesn't screen your employees
- MA (Maintenance): Mostly customer for patching/config, AWS for infrastructure
- MP (Media Protection): Mixed — AWS handles cloud media, customer handles endpoints
- IR (Incident Response): Mostly customer — you must have your own IR capability
- RA (Risk Assessment): Customer — you must assess your own risks
- CA (Security Assessment): Customer — you must assess your own controls
"""

from typing import Optional


# Maps CMMC practice IDs to responsibility: 'customer', 'shared', or 'aws'
CMMC_RESPONSIBILITY: dict[str, str] = {

    # =========================================================================
    # AC — Access Control
    # =========================================================================
    # Most AC controls are shared — AWS provides IAM, VPC, etc. but customer
    # must configure them properly
    "AC.L2-3.1.1": "shared",    # Authorized access — IAM, Identity Center
    "AC.L2-3.1.2": "shared",    # Transaction/function types — IAM policies
    "AC.L2-3.1.3": "shared",    # CUI flow control — VPC, security groups
    "AC.L2-3.1.4": "shared",    # Separation of duties — IAM roles
    "AC.L2-3.1.5": "shared",    # Least privilege — IAM policies, SCPs
    "AC.L2-3.1.6": "shared",    # Non-privileged accounts — IAM roles
    "AC.L2-3.1.7": "shared",    # Prevent privileged function execution — IAM, CloudTrail
    "AC.L2-3.1.8": "shared",    # Unsuccessful logon attempts — IdP + CloudWatch
    "AC.L2-3.1.9": "customer",  # Privacy/security notices — customer must configure banners
    "AC.L2-3.1.10": "customer", # Session lock — customer configures on endpoints/WorkSpaces
    "AC.L2-3.1.11": "shared",   # Session termination — ALB/app timeouts, IAM session duration
    "AC.L2-3.1.12": "shared",   # Remote access monitoring — Session Manager, VPN, CloudTrail
    "AC.L2-3.1.13": "shared",   # Remote access encryption — VPN, TLS, Direct Connect
    "AC.L2-3.1.14": "shared",   # Managed access control points — Client VPN, bastion hosts
    "AC.L2-3.1.15": "customer", # Remote privileged command authorization — customer process
    "AC.L2-3.1.16": "customer", # Wireless access authorization — customer network controls
    "AC.L2-3.1.17": "customer", # Wireless authentication/encryption — customer network
    "AC.L2-3.1.18": "customer", # Mobile device control — customer MDM
    "AC.L2-3.1.19": "customer", # Mobile device encryption — customer endpoint management
    "AC.L2-3.1.20": "shared",   # External system connections — VPC peering, Transit Gateway
    "AC.L2-3.1.21": "customer", # Portable storage restrictions — customer endpoint policy
    "AC.L2-3.1.22": "shared",   # Public information control — S3 Block Public Access, Macie

    # =========================================================================
    # AT — Awareness and Training (ALL CUSTOMER)
    # =========================================================================
    "AT.L2-3.2.1": "customer",  # Security awareness — customer trains their staff
    "AT.L2-3.2.2": "customer",  # Role-based training — customer trains their staff
    "AT.L2-3.2.3": "customer",  # Insider threat training — customer trains their staff

    # =========================================================================
    # AU — Audit and Accountability
    # =========================================================================
    "AU.L2-3.3.1": "shared",    # Audit logs — CloudTrail, CloudWatch, but customer configures
    "AU.L2-3.3.2": "shared",    # Individual accountability — IAM, CloudTrail attribution
    "AU.L2-3.3.3": "customer",  # Review/update logged events — customer decides what to log
    "AU.L2-3.3.4": "shared",    # Audit logging failure alerts — CloudWatch alarms, SCPs
    "AU.L2-3.3.5": "shared",    # Log correlation — Detective, CloudWatch Insights, SIEM
    "AU.L2-3.3.6": "shared",    # Audit reduction/reporting — Athena, CloudWatch Insights
    "AU.L2-3.3.7": "shared",    # Time synchronization — Amazon Time Sync Service
    "AU.L2-3.3.8": "shared",    # Protect audit info — S3 Object Lock, separate logging account
    "AU.L2-3.3.9": "shared",    # Limit audit management — IAM policies, SCPs

    # =========================================================================
    # CM — Configuration Management
    # =========================================================================
    "CM.L2-3.4.1": "shared",    # Baseline configs/inventory — AWS Config, Systems Manager
    "CM.L2-3.4.2": "shared",    # Security config settings — Security Hub, Config rules
    "CM.L2-3.4.3": "shared",    # Change tracking — CloudTrail, CloudFormation, Config
    "CM.L2-3.4.4": "customer",  # Security impact analysis — customer process before changes
    "CM.L2-3.4.5": "shared",    # Change access restrictions — IAM roles, SCPs
    "CM.L2-3.4.6": "shared",    # Least functionality — SCPs, security groups
    "CM.L2-3.4.7": "shared",    # Restrict nonessential services — security groups, SCPs
    "CM.L2-3.4.8": "shared",    # Software authorization — Systems Manager, AppLocker
    "CM.L2-3.4.9": "customer",  # User-installed software — customer endpoint management

    # =========================================================================
    # IA — Identification and Authentication
    # =========================================================================
    "IA.L2-3.5.1": "shared",    # User/device identification — IAM, Identity Center
    "IA.L2-3.5.2": "shared",    # Authentication — IAM, Identity Center, federation
    "IA.L2-3.5.3": "shared",    # MFA — IAM MFA, Identity Center MFA
    "IA.L2-3.5.4": "shared",    # Replay-resistant auth — TOTP, SAML, OIDC
    "IA.L2-3.5.5": "customer",  # Identifier reuse prevention — customer IdP policy
    "IA.L2-3.5.6": "shared",    # Disable inactive identifiers — IAM credential report
    "IA.L2-3.5.7": "customer",  # Password complexity — customer IdP configuration
    "IA.L2-3.5.8": "customer",  # Password reuse prevention — customer IdP configuration
    "IA.L2-3.5.9": "customer",  # Temporary passwords — customer IdP configuration
    "IA.L2-3.5.10": "shared",   # Cryptographic password protection — KMS, Secrets Manager
    "IA.L2-3.5.11": "customer", # Authentication feedback obscuring — customer app config

    # =========================================================================
    # IR — Incident Response (MOSTLY CUSTOMER)
    # =========================================================================
    "IR.L2-3.6.1": "customer",  # IR capability — customer must build their own IR program
    "IR.L2-3.6.2": "customer",  # Incident tracking/reporting — customer process
    "IR.L2-3.6.3": "customer",  # IR testing — customer conducts exercises

    # =========================================================================
    # MA — Maintenance (MOSTLY CUSTOMER)
    # =========================================================================
    "MA.L2-3.7.1": "shared",    # System maintenance — Systems Manager Patch Manager
    "MA.L2-3.7.2": "customer",  # Maintenance tool controls — customer manages tools
    "MA.L2-3.7.3": "customer",  # Off-site maintenance sanitization — customer process
    "MA.L2-3.7.4": "customer",  # Diagnostic media scanning — customer process
    "MA.L2-3.7.5": "shared",    # Remote maintenance MFA — Session Manager, VPN + MFA
    "MA.L2-3.7.6": "customer",  # Maintenance personnel supervision — customer process

    # =========================================================================
    # MP — Media Protection (MOSTLY CUSTOMER)
    # =========================================================================
    "MP.L2-3.8.1": "customer",  # Physical media protection — customer physical security
    "MP.L2-3.8.2": "shared",    # Media access control — S3 policies, IAM for digital; customer for physical
    "MP.L2-3.8.3": "shared",    # Media sanitization — AWS handles cloud media; customer handles endpoints
    "MP.L2-3.8.4": "customer",  # CUI markings — customer marking process
    "MP.L2-3.8.5": "customer",  # Media transport accountability — customer chain of custody
    "MP.L2-3.8.6": "shared",    # Transport encryption — KMS, S3 encryption for digital media
    "MP.L2-3.8.7": "customer",  # Removable media control — customer endpoint policy
    "MP.L2-3.8.8": "customer",  # Unidentified storage prohibition — customer policy
    "MP.L2-3.8.9": "shared",    # Backup CUI protection — AWS Backup with KMS encryption

    # =========================================================================
    # PE — Physical Protection (MOSTLY AWS for cloud, CUSTOMER for on-prem)
    # =========================================================================
    "PE.L2-3.10.1": "aws",      # Physical access control — AWS data center security
    "PE.L2-3.10.2": "aws",      # Physical facility monitoring — AWS data center security
    "PE.L2-3.10.3": "aws",      # Visitor escort/monitoring — AWS data center security
    "PE.L2-3.10.4": "aws",      # Physical access audit logs — AWS data center security
    "PE.L2-3.10.5": "aws",      # Physical access device management — AWS data center security
    "PE.L2-3.10.6": "customer", # Alternate work site safeguards — customer telework policy

    # =========================================================================
    # PS — Personnel Security (ALL CUSTOMER)
    # =========================================================================
    "PS.L2-3.9.1": "customer",  # Personnel screening — customer HR process
    "PS.L2-3.9.2": "customer",  # Personnel actions (termination/transfer) — customer HR process

    # =========================================================================
    # RA — Risk Assessment (MOSTLY CUSTOMER)
    # =========================================================================
    "RA.L2-3.11.1": "customer", # Risk assessment — customer risk management process
    "RA.L2-3.11.2": "shared",   # Vulnerability scanning — Inspector, but customer runs scans
    "RA.L2-3.11.3": "customer", # Vulnerability remediation — customer remediation process

    # =========================================================================
    # CA — Security Assessment (MOSTLY CUSTOMER)
    # =========================================================================
    "CA.L2-3.12.1": "shared",   # Security control assessment — Audit Manager, Security Hub
    "CA.L2-3.12.2": "customer", # POA&M — customer manages their own POA&M
    "CA.L2-3.12.3": "shared",   # Continuous monitoring — Config, Security Hub, GuardDuty
    "CA.L2-3.12.4": "customer", # System security plan — customer documents their SSP

    # =========================================================================
    # SC — System and Communications Protection
    # =========================================================================
    "SC.L2-3.13.1": "shared",   # Boundary protection — VPC, Network Firewall, WAF
    "SC.L2-3.13.2": "shared",   # Security architecture — Well-Architected, defense-in-depth
    "SC.L2-3.13.3": "shared",   # User/management separation — VPC subnets, bastion hosts
    "SC.L2-3.13.4": "shared",   # Shared resource protection — Nitro, EC2 isolation
    "SC.L2-3.13.5": "shared",   # Public component separation — public/private subnets
    "SC.L2-3.13.6": "shared",   # Default deny — security groups, NACLs
    "SC.L2-3.13.7": "customer", # Split tunneling prevention — customer VPN configuration
    "SC.L2-3.13.8": "shared",   # Encryption in transit — TLS, VPN, Direct Connect
    "SC.L2-3.13.9": "shared",   # Session termination — ALB timeouts, app config
    "SC.L2-3.13.10": "shared",  # Key management — KMS
    "SC.L2-3.13.11": "shared",  # FIPS cryptography — KMS FIPS endpoints
    "SC.L2-3.13.12": "customer",# Collaborative computing devices — customer device policy
    "SC.L2-3.13.13": "customer",# Mobile code — customer browser/app policy
    "SC.L2-3.13.14": "customer",# VoIP — customer communications platform
    "SC.L2-3.13.15": "shared",  # Session authenticity — TLS, certificate validation
    "SC.L2-3.13.16": "shared",  # CUI at rest encryption — KMS, S3/EBS/RDS encryption

    # =========================================================================
    # SI — System and Information Integrity
    # =========================================================================
    "SI.L2-3.14.1": "shared",   # Flaw remediation — Systems Manager Patch Manager
    "SI.L2-3.14.2": "shared",   # Malware protection — GuardDuty Malware Protection
    "SI.L2-3.14.3": "customer", # Security alerts/advisories — customer monitors advisories
    "SI.L2-3.14.4": "shared",   # Malware protection updates — GuardDuty auto-updates
    "SI.L2-3.14.5": "shared",   # Malware scanning — Inspector, GuardDuty
    "SI.L2-3.14.6": "shared",   # System monitoring — GuardDuty, VPC Flow Logs, CloudTrail
    "SI.L2-3.14.7": "shared",   # Unauthorized use detection — GuardDuty anomaly detection
}


def get_cmmc_responsibility(practice_id: str) -> str:
    """Get the shared responsibility classification for a CMMC practice.

    Args:
        practice_id: CMMC practice ID (e.g., 'AC.L2-3.1.1')

    Returns:
        'customer', 'shared', or 'aws'
    """
    return CMMC_RESPONSIBILITY.get(practice_id.upper(), 'customer')
