#!/usr/bin/env python3
"""
Add AWS-specific questions for missing SC (System and Communications Protection) controls
Missing: SC-2, SC-4, SC-5, SC-10, SC-15, SC-17, SC-18, SC-22, SC-23, SC-39
"""

MISSING_SC_QUESTIONS = """
    'sc-2': [
        {
            'type': 'separation_implementation',
            'question': 'How do you separate system and user functionality in AWS (separate VPCs for management vs application, separate AWS accounts, IAM role separation, resource tagging)?',
        },
        {
            'type': 'management_separation',
            'question': 'Are management functions separated from user functions (separate management VPC, Systems Manager for admin access, bastion hosts in separate subnets, PrivateLink for service access)?',
        },
        {
            'type': 'separation_enforcement',
            'question': 'How is separation enforced (security groups, NACLs, SCPs, IAM policies, VPC endpoints)? Can users access management functions?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates SC-2 compliance? Provide: VPC architecture diagrams, security group configurations, IAM policy separation, account structure documentation. Where are these artifacts stored?',
        },
    ],
    'sc-4': [
        {
            'type': 'shared_resources',
            'question': 'What AWS resources are shared between workloads or tenants (shared VPCs, shared services, multi-tenant applications, shared databases)? Are they documented?',
        },
        {
            'type': 'information_protection',
            'question': 'How is information protected in shared resources (encryption, access controls, data isolation, separate schemas/tables, tenant ID filtering)?',
        },
        {
            'type': 'residual_information',
            'question': 'How do you prevent information leakage in shared resources (memory clearing, secure deletion, EBS volume encryption, RDS encryption, Lambda execution environment isolation)?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates SC-4 compliance? Provide: Shared resource inventory, data isolation mechanisms, encryption configurations, tenant separation documentation. Where are these artifacts stored?',
        },
    ],
    'sc-5': [
        {
            'type': 'ddos_protection',
            'question': 'What DDoS protection is in place for AWS resources (AWS Shield Standard/Advanced, CloudFront, Route 53, WAF rate limiting, Auto Scaling)?',
        },
        {
            'type': 'resource_limits',
            'question': 'How do you prevent resource exhaustion (service quotas, API rate limiting, Lambda concurrency limits, RDS connection limits, Auto Scaling policies)?',
        },
        {
            'type': 'ddos_response',
            'question': 'What is your DDoS response plan (Shield Response Team engagement, traffic analysis, mitigation strategies, communication plan)? Have you tested it?',
        },
        {
            'type': 'monitoring',
            'question': 'How do you monitor for DoS attacks (CloudWatch metrics, Shield Advanced detection, WAF blocked requests, GuardDuty findings, anomaly detection)?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates SC-5 compliance? Provide: Shield configurations, WAF rules, Auto Scaling policies, DDoS response plan, monitoring dashboards. Where are these artifacts stored?',
        },
    ],
    'sc-10': [
        {
            'type': 'session_termination',
            'question': 'How are inactive AWS sessions terminated (IAM session duration limits, SSO session timeout, console session timeout, API token expiration)?',
        },
        {
            'type': 'timeout_configuration',
            'question': 'What are your session timeout settings (console: 12 hours max, API tokens: 1 hour, SSO: configurable, database connections: timeout settings)?',
        },
        {
            'type': 'forced_disconnect',
            'question': 'Can sessions be forcibly disconnected (IAM session revocation, SSO session termination, Systems Manager session termination, emergency access revocation)?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates SC-10 compliance? Provide: IAM session duration policies, SSO timeout configurations, session termination logs, timeout enforcement documentation. Where are these artifacts stored?',
        },
    ],
    'sc-15': [
        {
            'type': 'collaborative_devices',
            'question': 'What collaborative computing devices/applications integrate with AWS (video conferencing, screen sharing, collaboration tools, remote access tools)? Are they approved?',
        },
        {
            'type': 'device_security',
            'question': 'How are collaborative devices secured when accessing AWS (endpoint security, MFA, VPN requirements, device compliance checks, approved applications list)?',
        },
        {
            'type': 'usage_restrictions',
            'question': 'What restrictions exist on collaborative device usage (no recording of sensitive data, no screen sharing of AWS console, approved tools only, data classification restrictions)?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates SC-15 compliance? Provide: Approved collaborative tools list, usage policy, endpoint security requirements, compliance monitoring reports. Where are these artifacts stored?',
        },
    ],
    'sc-17': [
        {
            'type': 'pki_certificates',
            'question': 'What PKI certificates are used in AWS (ACM certificates for load balancers, API Gateway custom domains, CloudFront distributions, IoT device certificates)?',
        },
        {
            'type': 'certificate_management',
            'question': 'How are certificates managed (AWS Certificate Manager for public certs, ACM Private CA for internal certs, automated renewal, expiration monitoring)?',
        },
        {
            'type': 'certificate_validation',
            'question': 'How are certificates validated (certificate transparency logs, OCSP/CRL checking, certificate pinning, automated validation)?',
        },
        {
            'type': 'certificate_revocation',
            'question': 'What is your certificate revocation process (ACM certificate deletion, Private CA revocation, CRL distribution, emergency revocation procedures)?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates SC-17 compliance? Provide: ACM certificate inventory, Private CA configuration, certificate renewal logs, revocation procedures. Where are these artifacts stored?',
        },
    ],
    'sc-18': [
        {
            'type': 'mobile_code',
            'question': 'What mobile code is used in AWS (JavaScript in web apps, Lambda functions, container images, browser extensions, mobile apps)?',
        },
        {
            'type': 'code_security',
            'question': 'How is mobile code secured (code signing, integrity verification, sandboxing, Lambda execution role restrictions, container image scanning)?',
        },
        {
            'type': 'code_approval',
            'question': 'What is your mobile code approval process (code review, security scanning, testing, deployment approval)? Are unapproved code deployments prevented?',
        },
        {
            'type': 'code_monitoring',
            'question': 'How is mobile code monitored (Lambda function monitoring, CloudWatch Logs, GuardDuty for malicious activity, runtime security)?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates SC-18 compliance? Provide: Mobile code inventory, code signing configurations, approval records, security scanning reports. Where are these artifacts stored?',
        },
    ],
    'sc-22': [
        {
            'type': 'dns_architecture',
            'question': 'What is your DNS architecture in AWS (Route 53 hosted zones, private hosted zones, DNS resolution in VPCs, hybrid DNS with on-premises)?',
        },
        {
            'type': 'dns_security',
            'question': 'How is DNS secured (DNSSEC for Route 53, DNS query logging, GuardDuty DNS protection, private hosted zones for internal resources)?',
        },
        {
            'type': 'dns_redundancy',
            'question': 'How is DNS availability ensured (Route 53 multi-region, health checks, failover routing, backup DNS servers)?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates SC-22 compliance? Provide: Route 53 hosted zone configurations, DNSSEC settings, DNS query logs, architecture diagrams. Where are these artifacts stored?',
        },
    ],
    'sc-23': [
        {
            'type': 'session_authenticity',
            'question': 'How do you ensure AWS session authenticity (TLS for all connections, certificate validation, MFA for console access, signed API requests)?',
        },
        {
            'type': 'session_protection',
            'question': 'How are sessions protected from hijacking (session tokens with short expiration, IP address binding, user agent validation, CloudTrail monitoring for anomalies)?',
        },
        {
            'type': 'session_monitoring',
            'question': 'How are suspicious sessions detected (GuardDuty for unusual API calls, CloudTrail analysis, impossible travel detection, concurrent session alerts)?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates SC-23 compliance? Provide: TLS configurations, session token policies, GuardDuty findings, session monitoring alerts. Where are these artifacts stored?',
        },
    ],
    'sc-39': [
        {
            'type': 'process_isolation',
            'question': 'How are processes isolated in AWS (separate AWS accounts, VPC isolation, container isolation, Lambda execution environment isolation, EC2 instance isolation)?',
        },
        {
            'type': 'isolation_enforcement',
            'question': 'How is process isolation enforced (security groups, NACLs, IAM policies, SCPs, container runtime security, hypervisor isolation)?',
        },
        {
            'type': 'isolation_monitoring',
            'question': 'How is isolation monitored (GuardDuty for unusual behavior, VPC Flow Logs, CloudTrail for cross-account access, runtime security monitoring)?',
        },
        {
            'type': 'evidence',
            'question': 'What evidence demonstrates SC-39 compliance? Provide: Account isolation architecture, VPC configurations, container security policies, isolation monitoring reports. Where are these artifacts stored?',
        },
    ],
"""

if __name__ == "__main__":
    print("Missing SC controls with AWS-specific questions:")
    print("SC-2, SC-4, SC-5, SC-10, SC-15, SC-17, SC-18, SC-22, SC-23, SC-39")
    print("\nTotal: 10 controls")
