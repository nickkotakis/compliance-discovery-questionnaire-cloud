#!/usr/bin/env python3
"""
Add evidence questions to control_questions.py for remaining controls.
"""

import json
from pathlib import Path

# Evidence questions to add (from evidence_questions_generated.json)
EVIDENCE_QUESTIONS = {
    'au-1': "What evidence demonstrates AU-1 compliance in AWS? Provide: AWS Config compliance reports for CLOUDTRAIL_SECURITY_TRAIL_ENABLED, CW_LOGGROUP_RETENTION_PERIOD_CHECK; Security Hub findings for CloudTrail.3, CloudWatch.16; Control Tower compliance status for CONFIG.CLOUDTRAIL.DT.6, CONFIG.LOGS.DT.2; Configuration screenshots from AWS CloudTrail, AWS Organizations, Amazon CloudWatch Logs (and 1 more services); CloudTrail logs of relevant API calls. Where are these artifacts stored?",
    'cm-1': "What evidence demonstrates CM-1 compliance in AWS? Provide: AWS Config compliance reports for CLOUDFORMATION_STACK_NOTIFICATION_CHECK; Security Hub findings for CloudFormation.1; Control Tower compliance status for AWS-GR_CONFIG_ENABLED, CONFIG.CLOUDFORMATION.DT.1; Configuration screenshots from AWS CloudFormation, AWS Config; CloudTrail logs of relevant API calls. Where are these artifacts stored?",
    'cp-1': "What evidence demonstrates CP-1 compliance in AWS? Provide: AWS Config compliance reports for BACKUP_RECOVERY_POINT_ENCRYPTED, BACKUP_RECOVERY_POINT_MINIMUM_RETENTION_CHECK; Security Hub findings for Backup.1; Control Tower compliance status for BACKUP_RECOVERY_POINT_MINIMUM_RETENTION_CHECK; Configuration screenshots from AWS Backup, Amazon DynamoDB, Amazon RDS (and 1 more services); CloudTrail logs of relevant API calls. Where are these artifacts stored?",
    'ia-1': "What evidence demonstrates IA-1 compliance in AWS? Provide: AWS Config compliance reports for IAM_PASSWORD_POLICY; Security Hub findings for IAM.7, IAM.8, IAM.9 (and 2 more); Control Tower compliance status for SH.IAM.7, SH.IAM.8; Configuration screenshots from AWS IAM Identity Center, AWS Identity and Access Management; CloudTrail logs of relevant API calls. Where are these artifacts stored?",
    'ir-1': "What evidence demonstrates IR-1 compliance in AWS? Provide: AWS Config compliance reports for SECURITYHUB_ENABLED; Control Tower compliance status for CONFIG.SECURITYHUB.DT.1; Configuration screenshots from AWS Security Hub, Amazon EventBridge; CloudTrail logs of relevant API calls. Where are these artifacts stored?",
    'ra-1': "What evidence demonstrates RA-1 compliance in AWS? Provide: AWS Config compliance reports for SECURITYHUB_ENABLED; Control Tower compliance status for CONFIG.SECURITYHUB.DT.1; Configuration screenshots from AWS Security Hub, AWS Trusted Advisor; CloudTrail logs of relevant API calls. Where are these artifacts stored?",
    'sc-1': "What evidence demonstrates SC-1 compliance in AWS? Provide: AWS Config compliance reports for DYNAMODB_TABLE_ENCRYPTED_KMS, S3_DEFAULT_ENCRYPTION_KMS, RDS_STORAGE_ENCRYPTED; Security Hub findings for DynamoDB.1, S3.4, RDS.3; Control Tower compliance status for CONFIG.DYNAMODB.DT.4, SH.RDS.3; Configuration screenshots from AWS Config, AWS Key Management Service, AWS Organizations; CloudTrail logs of relevant API calls. Where are these artifacts stored?",
    'si-1': "What evidence demonstrates SI-1 compliance in AWS? Provide: AWS Config compliance reports for GUARDDUTY_ENABLED_CENTRALIZED, INSPECTOR_ENABLED; Security Hub findings for GuardDuty.1; Control Tower compliance status for CONFIG.GUARDDUTY.DT.1, SH.GuardDuty.1; Configuration screenshots from AWS Security Hub, Amazon GuardDuty, Amazon Inspector; CloudTrail logs of relevant API calls. Where are these artifacts stored?",
    'sc-20': "What evidence demonstrates SC-20 compliance in AWS? Provide: AWS Config compliance reports for ROUTE53_HOSTED_ZONE_TAGGED; Control Tower compliance status for CONFIG.ROUTE53.DT.2; Configuration screenshots from Amazon Route 53; CloudTrail logs of relevant API calls. Where are these artifacts stored?",
    'sc-21': "What evidence demonstrates SC-21 compliance in AWS? Provide: AWS Config compliance reports for GUARDDUTY_ENABLED_CENTRALIZED; Security Hub findings for GuardDuty.1; Control Tower compliance status for SH.GuardDuty.1; Configuration screenshots from Amazon GuardDuty, Amazon Route 53; CloudTrail logs of relevant API calls. Where are these artifacts stored?",
}

def main():
    print("="*80)
    print("EVIDENCE QUESTIONS TO ADD")
    print("="*80)
    print()
    
    for control_id, question in sorted(EVIDENCE_QUESTIONS.items()):
        print(f"{control_id.upper()}:")
        print(f"  {question[:100]}...")
        print()
    
    print(f"Total: {len(EVIDENCE_QUESTIONS)} evidence questions")
    print()
    print("Add these manually to control_questions.py using strReplace")
    print("Format:")
    print("    {")
    print("        'type': 'evidence',")
    print("        'question': '<question>',")
    print("    },")

if __name__ == '__main__':
    main()
