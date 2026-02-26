# ⚡ CloudFormation Quick Start (10 minutes)

The fastest way to deploy your Compliance Discovery Questionnaire to AWS.

## TL;DR

```bash
# 1. Create GitHub connection in App Runner console (one-time, 2 min)
# 2. Create GitHub PAT and store in Secrets Manager (one-time, 2 min)
# 3. Deploy stack (5 min)

aws cloudformation create-stack \
  --stack-name compliance-discovery \
  --template-body file://cloudformation-template.yaml \
  --parameters \
    ParameterKey=GitHubConnectionArn,ParameterValue=YOUR_CONNECTION_ARN \
  --capabilities CAPABILITY_IAM

# 4. Get your URLs
aws cloudformation describe-stacks \
  --stack-name compliance-discovery \
  --query 'Stacks[0].Outputs[*].[OutputKey,OutputValue]' \
  --output table
```

## Step-by-Step

### 1. Create GitHub Connection (2 minutes, one-time)

```bash
# Open App Runner console
open https://console.aws.amazon.com/apprunner/

# Click "Create service" → "Source" → "Add new" GitHub connection
# Authorize GitHub → Copy the Connection ARN
# Cancel service creation (we'll use CloudFormation)
```

Save the ARN: `arn:aws:apprunner:us-east-1:123456789012:connection/MyConnection/abc123`

### 2. Store GitHub Token (2 minutes, one-time)

```bash
# Create GitHub Personal Access Token
open https://github.com/settings/tokens

# Generate token with 'repo' scope → Copy token

# Store in Secrets Manager
aws secretsmanager create-secret \
  --name github/personal-access-token \
  --secret-string '{"token":"ghp_YOUR_TOKEN_HERE"}'
```

### 3. Deploy Stack (5 minutes)

```bash
# Navigate to deployment directory
cd aws-deployment

# Deploy
aws cloudformation create-stack \
  --stack-name compliance-discovery \
  --template-body file://cloudformation-template.yaml \
  --parameters \
    ParameterKey=GitHubConnectionArn,ParameterValue=arn:aws:apprunner:us-east-1:123456789012:connection/MyConnection/abc123 \
  --capabilities CAPABILITY_IAM \
  --region us-east-1

# Wait for completion (5-10 minutes)
aws cloudformation wait stack-create-complete \
  --stack-name compliance-discovery
```

### 4. Get Your URLs (30 seconds)

```bash
# Get all outputs
aws cloudformation describe-stacks \
  --stack-name compliance-discovery \
  --query 'Stacks[0].Outputs[*].[OutputKey,OutputValue]' \
  --output table

# Or just the frontend URL
aws cloudformation describe-stacks \
  --stack-name compliance-discovery \
  --query 'Stacks[0].Outputs[?OutputKey==`FrontendUrl`].OutputValue' \
  --output text
```

### 5. Update CORS (1 minute)

```bash
# Get frontend URL
FRONTEND_URL=$(aws cloudformation describe-stacks \
  --stack-name compliance-discovery \
  --query 'Stacks[0].Outputs[?OutputKey==`FrontendUrl`].OutputValue' \
  --output text)

echo "Update CORS_ORIGINS in App Runner to: $FRONTEND_URL"

# Go to App Runner console → Service → Configuration → Environment variables
# Update CORS_ORIGINS → Deploy
```

## Done! 🎉

Your application is live:
- **Frontend**: Check CloudFormation outputs for `FrontendUrl`
- **Backend**: Check CloudFormation outputs for `BackendServiceUrl`

## What You Get

- ✅ Auto-scaling backend (App Runner)
- ✅ Static frontend hosting (Amplify)
- ✅ Auto-deploy from GitHub (both services)
- ✅ HTTPS enabled
- ✅ Health checks configured
- ✅ CloudWatch logging
- ✅ IAM roles configured
- ✅ Cost: ~$25-55/month

## Common Commands

```bash
# Check stack status
aws cloudformation describe-stacks \
  --stack-name compliance-discovery \
  --query 'Stacks[0].StackStatus'

# View events
aws cloudformation describe-stack-events \
  --stack-name compliance-discovery \
  --max-items 10

# Update stack (e.g., change instance size)
aws cloudformation update-stack \
  --stack-name compliance-discovery \
  --template-body file://cloudformation-template.yaml \
  --parameters \
    ParameterKey=GitHubConnectionArn,UsePreviousValue=true \
    ParameterKey=AppRunnerInstanceCpu,ParameterValue="2 vCPU" \
  --capabilities CAPABILITY_IAM

# Delete stack
aws cloudformation delete-stack \
  --stack-name compliance-discovery
```

## Troubleshooting

**Stack fails at App Runner:**
- Verify GitHub connection ARN is correct
- Check you have access to the private repository

**Stack fails at Amplify:**
- Verify GitHub token is in Secrets Manager
- Check token has 'repo' scope
- Ensure secret name is exactly: `github/personal-access-token`

**Frontend can't connect to backend:**
- Update CORS_ORIGINS in App Runner (step 5)
- Check both services are running

## Full Documentation

For detailed information, see [CLOUDFORMATION_DEPLOY.md](CLOUDFORMATION_DEPLOY.md)
