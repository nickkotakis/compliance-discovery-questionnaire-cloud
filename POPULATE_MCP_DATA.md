# Populating MCP Data for All Controls

## Current Status
- ✅ AC-2: 10 AWS controls loaded
- ⏳ Need to add: ~50+ more NIST controls

## Approach

Since we have 177 NIST controls in the Moderate Baseline, and querying MCP for each one individually would be time-consuming, I recommend a hybrid approach:

### Option 1: Batch Query by Control Family (Recommended)
Query MCP by AWS service keywords and map results back to NIST controls:

**Access Control (AC)**: IAM, Organizations, SSO
**Audit & Accountability (AU)**: CloudTrail, CloudWatch Logs, Config
**Configuration Management (CM)**: Config, Systems Manager, CloudFormation
**Contingency Planning (CP)**: Backup, S3, RDS snapshots
**Identification & Authentication (IA)**: IAM, Cognito, MFA
**Incident Response (IR)**: GuardDuty, Security Hub, Detective
**Physical & Environmental (PE)**: AWS responsibility (Artifact links)
**System & Communications Protection (SC)**: Security Groups, WAF, KMS, TLS
**System & Information Integrity (SI)**: Inspector, GuardDuty, Patch Manager
**Risk Assessment (RA)**: Inspector, Security Hub, GuardDuty

### Option 2: Focus on Top 20 Most Common Controls
Based on typical compliance assessments, these are the most frequently assessed:

1. ✅ AC-2 (Account Management) - DONE
2. AU-2 (Audit Events)
3. AU-3 (Audit Record Content)
4. AU-6 (Audit Review)
5. AU-9 (Audit Protection)
6. AU-12 (Audit Generation)
7. CM-2 (Baseline Configuration)
8. CM-6 (Configuration Settings)
9. CM-7 (Least Functionality)
10. CM-8 (System Inventory)
11. CP-9 (Backup)
12. IA-2 (Identification & Authentication)
13. IA-5 (Authenticator Management)
14. SC-7 (Boundary Protection)
15. SC-8 (Transmission Confidentiality)
16. SC-12 (Cryptographic Key Management)
17. SC-13 (Cryptographic Protection)
18. SC-28 (Protection of Information at Rest)
19. SI-2 (Flaw Remediation)
20. SI-4 (System Monitoring)

### Option 3: Use MCP Aggregated Metadata
The MCP search results include `aggregated_metadata` that shows all Config rules, Security Hub controls, and Control Tower IDs for a search. We can use this to quickly populate data.

## Recommended Implementation

Let me create a semi-automated approach:

1. **Query MCP for each control family** (10 queries total)
2. **Extract aggregated metadata** from each query
3. **Map results to NIST controls** based on keywords
4. **Generate comprehensive JSON file**

This will give us coverage for ~80% of controls with AWS implementations.

## What I'll Do Next

I'll query MCP for the top control families and generate a comprehensive `aws_controls_mcp_data.json` file with data for:
- All AC controls (Access Control)
- All AU controls (Audit & Accountability)
- All CM controls (Configuration Management)
- All CP controls (Contingency Planning)
- All IA controls (Identification & Authentication)
- All IR controls (Incident Response)
- All SC controls (System & Communications Protection)
- All SI controls (System & Information Integrity)
- All RA controls (Risk Assessment)

This should cover the majority of controls that have AWS implementations.

Would you like me to proceed with this approach?
