#!/bin/bash
# AWS Setup Script - Ensures credentials are configured

set -e

echo "🔐 Setting up AWS credentials..."

# Assume role using isengardcli
eval $(isengardcli assume fahtu+dev --region us-east-1)

# Verify credentials are working
if aws sts get-caller-identity &>/dev/null; then
    echo "✅ AWS credentials configured successfully"
    aws sts get-caller-identity --query 'Account' --output text | xargs -I {} echo "📋 Account: {}"
    echo "🌍 Region: us-east-1"
else
    echo "❌ Failed to configure AWS credentials"
    exit 1
fi
