#!/usr/bin/env python3
import os
import aws_cdk as cdk
from cdk.cdk_stack import ComplianceDiscoveryStack

app = cdk.App()

ComplianceDiscoveryStack(
    app, 
    "ComplianceDiscoveryStack",
    env=cdk.Environment(
        account=os.getenv('CDK_DEFAULT_ACCOUNT'),
        region=os.getenv('CDK_DEFAULT_REGION', 'us-east-1')
    ),
    description="Compliance Discovery Questionnaire - Full Stack Deployment"
)

app.synth()
