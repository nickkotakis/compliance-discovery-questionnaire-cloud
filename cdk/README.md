# Compliance Discovery Questionnaire - AWS CDK Deployment

## Quick Start (5 minutes)

```bash
# 1. Authenticate
export AWS_PROFILE="nkotakis+KotakisIsengard-Admin"

# 2. Deploy everything
./deploy.sh
```

That's it! The script will:
- Install dependencies
- Build frontend
- Bootstrap CDK (if needed)
- Deploy infrastructure
- Upload frontend to S3
- Invalidate CloudFront cache
- Show you the URLs

## What Gets Deployed

- **Lambda Function**: Python 3.11 backend API
- **API Gateway**: REST API with CORS enabled
- **DynamoDB**: Sessions table (pay-per-request)
- **S3 Bucket**: Frontend hosting
- **CloudFront**: Global CDN with HTTPS
- **IAM Roles**: Least-privilege access

## Architecture

```
┌─────────────┐
│   Users     │
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│   CloudFront    │ ◄── HTTPS, Global CDN
└────────┬────────┘
         │
         ├──► S3 Bucket (Frontend)
         │
         └──► API Gateway
                  │
                  ▼
              Lambda Function
                  │
                  ▼
              DynamoDB
```

## Manual Deployment

If you prefer step-by-step:

```bash
# 1. Install dependencies
source .venv/bin/activate
pip install -r requirements.txt

# 2. Build frontend
cd ../frontend && npm install && npm run build

# 3. Bootstrap CDK (first time only)
cd ../cdk
cdk bootstrap

# 4. Deploy
cdk deploy

# 5. Upload frontend
BUCKET=$(aws cloudformation describe-stacks \
  --stack-name ComplianceDiscoveryStack \
  --query 'Stacks[0].Outputs[?OutputKey==`FrontendBucketName`].OutputValue' \
  --output text)
aws s3 sync ../frontend/dist/ s3://$BUCKET/
```

## Useful Commands

```bash
# View stack outputs
cdk deploy --outputs-file outputs.json

# View CloudFormation template
cdk synth

# Compare deployed vs local
cdk diff

# Destroy everything
cdk destroy

# View logs
aws logs tail /aws/lambda/ComplianceDiscoveryStack-ApiFunction --follow
```

## Cost

~$5-25/month for moderate usage (mostly free tier eligible)

## Documentation

- [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) - Detailed step-by-step guide
- [AWS CDK Docs](https://docs.aws.amazon.com/cdk/)

## Troubleshooting

**"Unable to locate credentials"**
```bash
export AWS_PROFILE="nkotakis+KotakisIsengard-Admin"
aws sts get-caller-identity
```

**"Stack already exists"**
```bash
cdk deploy --force
```

**Frontend not loading**
- Wait 15-20 minutes for CloudFront distribution
- Check S3 bucket has files: `aws s3 ls s3://$BUCKET/`

## Support

Contact AWS SAS team for assistance.
