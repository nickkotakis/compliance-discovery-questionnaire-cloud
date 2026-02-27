# Compliance Discovery Questionnaire - AWS CDK Deployment Guide

## Architecture Overview

This deployment creates a serverless, production-ready infrastructure:

- **Backend**: AWS Lambda + API Gateway (auto-scaling, pay-per-use)
- **Frontend**: S3 + CloudFront (global CDN, HTTPS)
- **Database**: DynamoDB (serverless, managed)
- **Infrastructure**: AWS CDK (Python)

## Prerequisites

1. AWS Account with Admin access (Isengard account: KotakisIsengard)
2. AWS CLI configured with Isengard credentials
3. Node.js and npm installed
4. Python 3.11+ installed
5. AWS CDK CLI installed globally

## Step 1: Authenticate with Isengard

```bash
# Add profile
isengardcli add-profile "nkotakis+KotakisIsengard@amazon.com" --role "Admin"

# Set AWS profile
export AWS_PROFILE="nkotakis+KotakisIsengard-Admin"

# Verify authentication
aws sts get-caller-identity
```

## Step 2: Install CDK Dependencies

```bash
cd cdk

# Activate virtual environment
source .venv/bin/activate

# Upgrade pip
python -m pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

## Step 3: Bootstrap CDK (First Time Only)

```bash
# Bootstrap your AWS account for CDK
cdk bootstrap aws://620360465022/us-east-1
```

## Step 4: Build Frontend

```bash
cd ../frontend

# Install dependencies
npm install

# Build for production
npm run build

# Verify dist/ folder was created
ls -la dist/
```

## Step 5: Prepare Backend

```bash
cd ../backend

# Install Python dependencies
pip install -r requirements.txt -t .

# Verify compliance_discovery module exists
ls -la compliance_discovery/
```

## Step 6: Deploy Infrastructure

```bash
cd ../cdk

# Synthesize CloudFormation template (preview)
cdk synth

# Deploy to AWS
cdk deploy

# Confirm deployment when prompted
```

## Step 7: Deploy Frontend to S3

After CDK deployment completes, you'll get outputs including the S3 bucket name.

```bash
# Get bucket name from CDK output
BUCKET_NAME=$(aws cloudformation describe-stacks \
  --stack-name ComplianceDiscoveryStack \
  --query 'Stacks[0].Outputs[?OutputKey==`FrontendBucketName`].OutputValue' \
  --output text)

# Upload frontend files
aws s3 sync ../frontend/dist/ s3://$BUCKET_NAME/ --delete

# Invalidate CloudFront cache
DISTRIBUTION_ID=$(aws cloudfront list-distributions \
  --query "DistributionList.Items[?Origins.Items[0].DomainName=='$BUCKET_NAME.s3.amazonaws.com'].Id" \
  --output text)

aws cloudfront create-invalidation \
  --distribution-id $DISTRIBUTION_ID \
  --paths "/*"
```

## Step 8: Update Frontend Environment

Update the frontend to use the deployed API:

```bash
# Get API URL
API_URL=$(aws cloudformation describe-stacks \
  --stack-name ComplianceDiscoveryStack \
  --query 'Stacks[0].Outputs[?OutputKey==`ApiUrl`].OutputValue' \
  --output text)

echo "API URL: $API_URL"

# Update frontend/.env.production
echo "VITE_API_URL=$API_URL" > ../frontend/.env.production

# Rebuild and redeploy frontend
cd ../frontend
npm run build
aws s3 sync dist/ s3://$BUCKET_NAME/ --delete
```

## Step 9: Update CORS Settings

```bash
# Get CloudFront URL
FRONTEND_URL=$(aws cloudformation describe-stacks \
  --stack-name ComplianceDiscoveryStack \
  --query 'Stacks[0].Outputs[?OutputKey==`FrontendUrl`].OutputValue' \
  --output text)

echo "Frontend URL: $FRONTEND_URL"

# Update Lambda environment variable
FUNCTION_NAME=$(aws lambda list-functions \
  --query "Functions[?starts_with(FunctionName, 'ComplianceDiscoveryStack-ApiFunction')].FunctionName" \
  --output text)

aws lambda update-function-configuration \
  --function-name $FUNCTION_NAME \
  --environment "Variables={CORS_ORIGINS=$FRONTEND_URL,SESSIONS_TABLE=ComplianceDiscoveryStack-SessionsTable}"
```

## Step 10: Test Deployment

```bash
# Test API health endpoint
curl $API_URL/api/health

# Open frontend in browser
open $FRONTEND_URL
```

## Useful Commands

```bash
# View all stack outputs
aws cloudformation describe-stacks \
  --stack-name ComplianceDiscoveryStack \
  --query 'Stacks[0].Outputs[*].[OutputKey,OutputValue]' \
  --output table

# View CloudWatch logs
aws logs tail /aws/lambda/ComplianceDiscoveryStack-ApiFunction --follow

# Update stack (after code changes)
cdk deploy

# Destroy stack (cleanup)
cdk destroy
```

## Cost Estimate

Monthly costs (assuming moderate usage):

- **Lambda**: $0-5 (1M requests free tier)
- **API Gateway**: $3.50 per million requests
- **DynamoDB**: $0-5 (25GB free tier)
- **S3**: $0.50 (first 50GB)
- **CloudFront**: $1-10 (1TB free tier first year)

**Total**: ~$5-25/month

## Troubleshooting

### CDK Bootstrap Fails
```bash
# Ensure you're authenticated
aws sts get-caller-identity

# Try with explicit account/region
cdk bootstrap aws://620360465022/us-east-1 --profile nkotakis+KotakisIsengard-Admin
```

### Lambda Deployment Fails
```bash
# Check backend dependencies are installed
cd backend
pip install -r requirements.txt -t .

# Verify module structure
ls -la compliance_discovery/
```

### Frontend Not Loading
```bash
# Check S3 sync completed
aws s3 ls s3://$BUCKET_NAME/

# Check CloudFront distribution status
aws cloudfront list-distributions --query "DistributionList.Items[*].[Id,Status]"

# Wait for distribution to deploy (can take 15-20 minutes)
```

### CORS Errors
```bash
# Verify Lambda environment variables
aws lambda get-function-configuration --function-name $FUNCTION_NAME

# Update CORS_ORIGINS to match frontend URL exactly
```

## Next Steps

1. **Custom Domain**: Add Route53 domain and ACM certificate
2. **Authentication**: Add Cognito user pools
3. **Monitoring**: Set up CloudWatch dashboards and alarms
4. **CI/CD**: Add GitHub Actions or CodePipeline
5. **Backup**: Enable DynamoDB point-in-time recovery

## Support

For issues or questions, contact AWS SAS team.
