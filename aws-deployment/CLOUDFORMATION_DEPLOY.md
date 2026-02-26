# CloudFormation Deployment Guide

Deploy the entire Compliance Discovery Questionnaire stack with a single CloudFormation template.

## Prerequisites (5 minutes)

### 1. Create GitHub Connection for App Runner

App Runner needs permission to access your private GitHub repository.

**Using AWS Console:**
1. Go to [App Runner Console](https://console.aws.amazon.com/apprunner/)
2. Click "Create service" (we'll cancel this, just need the connection)
3. Under "Source", click "Add new" next to "GitHub connection"
4. Follow the GitHub authorization flow
5. **Copy the Connection ARN** (looks like: `arn:aws:apprunner:us-east-1:123456789012:connection/MyConnection/abc123`)
6. Cancel the service creation (we'll use CloudFormation instead)

**Save this ARN** - you'll need it for the CloudFormation deployment.

### 2. Create GitHub Personal Access Token for Amplify

Amplify needs a token to access your repository.

1. Go to [GitHub Settings > Developer settings > Personal access tokens > Tokens (classic)](https://github.com/settings/tokens)
2. Click "Generate new token (classic)"
3. Name: `AWS Amplify - Compliance Discovery`
4. Expiration: Choose your preference (90 days recommended)
5. Scopes: Select `repo` (full control of private repositories)
6. Click "Generate token"
7. **Copy the token** (you won't see it again!)

### 3. Store GitHub Token in AWS Secrets Manager

```bash
aws secretsmanager create-secret \
  --name github/personal-access-token \
  --description "GitHub PAT for Amplify deployments" \
  --secret-string '{"token":"ghp_your_token_here"}'
```

Replace `ghp_your_token_here` with your actual token.

## Deploy with CloudFormation (5 minutes)

### Option 1: AWS Console

1. Go to [CloudFormation Console](https://console.aws.amazon.com/cloudformation/)
2. Click "Create stack" → "With new resources"
3. **Template**:
   - Choose "Upload a template file"
   - Upload `cloudformation-template.yaml`
4. **Stack name**: `compliance-discovery-questionnaire`
5. **Parameters**:
   - GitHubRepository: `https://github.com/nickkotakis/compliance-discovery-questionnaire`
   - GitHubBranch: `main`
   - GitHubConnectionArn: `<paste your connection ARN from step 1>`
   - AppRunnerInstanceCpu: `1 vCPU` (default)
   - AppRunnerInstanceMemory: `2 GB` (default)
6. Click "Next" → "Next"
7. Check "I acknowledge that AWS CloudFormation might create IAM resources"
8. Click "Submit"
9. Wait 5-10 minutes for deployment to complete

### Option 2: AWS CLI

```bash
aws cloudformation create-stack \
  --stack-name compliance-discovery-questionnaire \
  --template-body file://cloudformation-template.yaml \
  --parameters \
    ParameterKey=GitHubRepository,ParameterValue=https://github.com/nickkotakis/compliance-discovery-questionnaire \
    ParameterKey=GitHubBranch,ParameterValue=main \
    ParameterKey=GitHubConnectionArn,ParameterValue=arn:aws:apprunner:us-east-1:123456789012:connection/MyConnection/abc123 \
  --capabilities CAPABILITY_IAM \
  --region us-east-1

# Monitor deployment
aws cloudformation wait stack-create-complete \
  --stack-name compliance-discovery-questionnaire \
  --region us-east-1

# Get outputs
aws cloudformation describe-stacks \
  --stack-name compliance-discovery-questionnaire \
  --query 'Stacks[0].Outputs' \
  --region us-east-1
```

## Post-Deployment (2 minutes)

### 1. Get Your URLs

```bash
# Get all outputs
aws cloudformation describe-stacks \
  --stack-name compliance-discovery-questionnaire \
  --query 'Stacks[0].Outputs[*].[OutputKey,OutputValue]' \
  --output table
```

Or in the CloudFormation console, go to your stack → "Outputs" tab.

You'll see:
- **FrontendUrl**: Your application URL (e.g., `https://main.d123abc.amplifyapp.com`)
- **BackendServiceUrl**: Your API URL (e.g., `https://abc123.us-east-1.awsapprunner.com`)

### 2. Update CORS Settings

Update the backend to only allow your frontend domain:

```bash
# Get the frontend URL from outputs
FRONTEND_URL=$(aws cloudformation describe-stacks \
  --stack-name compliance-discovery-questionnaire \
  --query 'Stacks[0].Outputs[?OutputKey==`FrontendUrl`].OutputValue' \
  --output text)

# Get the App Runner service ARN
SERVICE_ARN=$(aws cloudformation describe-stacks \
  --stack-name compliance-discovery-questionnaire \
  --query 'Stacks[0].Outputs[?OutputKey==`BackendServiceArn`].OutputValue' \
  --output text)

# Update CORS (requires manual update in console for now)
echo "Update CORS_ORIGINS to: $FRONTEND_URL"
```

**Manual step**: Go to App Runner console → Select your service → Configuration → Environment variables → Update `CORS_ORIGINS` to your frontend URL → Deploy

### 3. Test Your Application

```bash
# Get frontend URL
aws cloudformation describe-stacks \
  --stack-name compliance-discovery-questionnaire \
  --query 'Stacks[0].Outputs[?OutputKey==`FrontendUrl`].OutputValue' \
  --output text

# Test backend health
BACKEND_URL=$(aws cloudformation describe-stacks \
  --stack-name compliance-discovery-questionnaire \
  --query 'Stacks[0].Outputs[?OutputKey==`BackendServiceUrl`].OutputValue' \
  --output text)

curl $BACKEND_URL/api/health
```

## What Gets Deployed

```
┌─────────────────────────────────────────────────────────┐
│                  CloudFormation Stack                    │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────────────────────────────────────────┐      │
│  │         AWS Amplify (Frontend)               │      │
│  │  - React + TypeScript app                    │      │
│  │  - Auto-deploy from GitHub                   │      │
│  │  - Custom domain support                     │      │
│  │  - HTTPS enabled                             │      │
│  └──────────────────────────────────────────────┘      │
│                        │                                 │
│                        │ HTTPS                           │
│                        ▼                                 │
│  ┌──────────────────────────────────────────────┐      │
│  │      AWS App Runner (Backend)                │      │
│  │  - Python Flask API                          │      │
│  │  - Auto-scaling                              │      │
│  │  - Auto-deploy from GitHub                   │      │
│  │  - Health checks                             │      │
│  │  - CloudWatch logs                           │      │
│  └──────────────────────────────────────────────┘      │
│                                                          │
│  ┌──────────────────────────────────────────────┐      │
│  │              IAM Roles                       │      │
│  │  - App Runner instance role                  │      │
│  │  - App Runner access role                    │      │
│  │  - Amplify service role                      │      │
│  └──────────────────────────────────────────────┘      │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

## Stack Outputs

| Output | Description |
|--------|-------------|
| BackendServiceUrl | API endpoint URL |
| BackendServiceArn | App Runner service ARN |
| FrontendAppId | Amplify app ID |
| FrontendUrl | Application URL |
| FrontendDefaultDomain | Amplify domain |
| NextSteps | Post-deployment instructions |

## Update the Stack

To update your deployment (e.g., change instance size):

```bash
aws cloudformation update-stack \
  --stack-name compliance-discovery-questionnaire \
  --template-body file://cloudformation-template.yaml \
  --parameters \
    ParameterKey=GitHubRepository,UsePreviousValue=true \
    ParameterKey=GitHubBranch,UsePreviousValue=true \
    ParameterKey=GitHubConnectionArn,UsePreviousValue=true \
    ParameterKey=AppRunnerInstanceCpu,ParameterValue="2 vCPU" \
    ParameterKey=AppRunnerInstanceMemory,ParameterValue="4 GB" \
  --capabilities CAPABILITY_IAM
```

## Delete the Stack

To remove all resources:

```bash
aws cloudformation delete-stack \
  --stack-name compliance-discovery-questionnaire

# Wait for deletion
aws cloudformation wait stack-delete-complete \
  --stack-name compliance-discovery-questionnaire
```

**Note**: This will delete:
- App Runner service (and all data in ephemeral storage)
- Amplify app
- IAM roles
- CloudWatch logs (after retention period)

## Troubleshooting

### Stack creation fails at App Runner

**Error**: "Connection ARN is invalid"
- Verify you created the GitHub connection in App Runner console
- Ensure the ARN format is correct: `arn:aws:apprunner:region:account:connection/name/id`

### Stack creation fails at Amplify

**Error**: "Access token is invalid"
- Verify the GitHub token is stored in Secrets Manager
- Ensure the secret name is exactly: `github/personal-access-token`
- Verify the token has `repo` scope

### Frontend can't connect to backend

- Check CORS settings in App Runner
- Verify `VITE_API_URL` environment variable in Amplify
- Check App Runner service is running

### App Runner service won't start

- Check CloudWatch logs: App Runner console → Service → Logs
- Verify `requirements.txt` is present in `/backend`
- Check environment variables are set correctly

## Cost Estimate

| Service | Configuration | Monthly Cost |
|---------|--------------|--------------|
| App Runner | 1 vCPU, 2GB RAM | $25-50 |
| Amplify | Static hosting | $0-5 |
| CloudWatch Logs | Standard retention | $1-5 |
| **Total** | | **$26-60** |

## Next Steps

1. ✅ Set up custom domain (optional)
2. ✅ Configure authentication (optional)
3. ✅ Set up CloudWatch alarms
4. ✅ Enable AWS WAF (optional)
5. ✅ Configure backup strategy

## Support

- **CloudFormation Issues**: Check AWS CloudFormation console → Events tab
- **App Runner Issues**: Check CloudWatch logs
- **Amplify Issues**: Check Amplify console → Build logs
- **General**: See [QUICKSTART.md](QUICKSTART.md#troubleshooting)
