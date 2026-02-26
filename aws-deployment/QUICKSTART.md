# 🚀 AWS Deployment Quickstart (15 minutes)

Deploy the Compliance Discovery Questionnaire to AWS using App Runner (backend) and Amplify (frontend).

## Prerequisites

- AWS Account with appropriate permissions
- AWS CLI configured (`aws configure`)
- GitHub account with this repository
- 15 minutes

## Step 1: Deploy Backend (5 minutes)

### Option A: Using AWS Console

1. Go to [AWS App Runner Console](https://console.aws.amazon.com/apprunner/)
2. Click "Create service"
3. **Source**:
   - Repository type: Source code repository
   - Connect to GitHub (first time only)
   - Repository: `nickkotakis/compliance-discovery-questionnaire`
   - Branch: `main`
   - Source directory: `/backend`
4. **Build settings**:
   - Configuration file: Use `apprunner.yaml`
5. **Service settings**:
   - Service name: `compliance-discovery-api`
   - Port: `5001`
   - Environment variables:
     - `DATABASE_PATH`: `/app/data/sessions.db`
     - `CORS_ORIGINS`: `*` (update after frontend deployment)
6. Click "Create & deploy"
7. **Copy the service URL** (e.g., `https://abc123.us-east-1.awsapprunner.com`)

### Option B: Using AWS CLI

```bash
# From repository root
cd backend

# Create App Runner service
aws apprunner create-service \
  --service-name compliance-discovery-api \
  --source-configuration '{
    "CodeRepository": {
      "RepositoryUrl": "https://github.com/nickkotakis/compliance-discovery-questionnaire",
      "SourceCodeVersion": {"Type": "BRANCH", "Value": "main"},
      "CodeConfiguration": {
        "ConfigurationSource": "API",
        "CodeConfigurationValues": {
          "Runtime": "PYTHON_3",
          "BuildCommand": "pip install -r requirements.txt",
          "StartCommand": "python -m compliance_discovery.api_server",
          "Port": "5001",
          "RuntimeEnvironmentVariables": {
            "DATABASE_PATH": "/app/data/sessions.db",
            "CORS_ORIGINS": "*"
          }
        }
      }
    }
  }' \
  --instance-configuration '{
    "Cpu": "1 vCPU",
    "Memory": "2 GB"
  }'

# Get service URL
aws apprunner describe-service \
  --service-arn <service-arn-from-above> \
  --query 'Service.ServiceUrl' \
  --output text
```

## Step 2: Deploy Frontend (5 minutes)

### Using AWS Console

1. Go to [AWS Amplify Console](https://console.aws.amazon.com/amplify/)
2. Click "New app" → "Host web app"
3. **Connect repository**:
   - GitHub
   - Repository: `nickkotakis/compliance-discovery-questionnaire`
   - Branch: `main`
4. **Build settings**:
   - Amplify will auto-detect `amplify.yml`
   - Monorepo: Set app root to `/frontend`
5. **Environment variables**:
   - Key: `VITE_API_URL`
   - Value: `<your-app-runner-url>` (from Step 1, without `/api`)
6. Click "Save and deploy"
7. Wait 3-5 minutes for deployment
8. **Copy the Amplify URL** (e.g., `https://main.d123abc.amplifyapp.com`)

## Step 3: Update CORS (2 minutes)

Update the backend to only allow your frontend domain:

1. Go back to App Runner console
2. Select your service
3. Go to "Configuration" → "Environment variables"
4. Update `CORS_ORIGINS` to your Amplify URL:
   ```
   https://main.d123abc.amplifyapp.com
   ```
5. Click "Deploy" to apply changes

## Step 4: Test (3 minutes)

1. Open your Amplify URL in a browser
2. You should see the Compliance Discovery Questionnaire
3. Try creating a session and answering questions
4. Test the export functionality

## 🎉 Done!

Your application is now live on AWS!

- **Frontend**: `https://main.d123abc.amplifyapp.com`
- **Backend**: `https://abc123.us-east-1.awsapprunner.com`

## Next Steps

- [Set up custom domain](DEPLOYMENT_GUIDE.md#custom-domain)
- [Configure authentication](DEPLOYMENT_GUIDE.md#authentication)
- [Set up monitoring](DEPLOYMENT_GUIDE.md#monitoring)
- [Review security best practices](DEPLOYMENT_GUIDE.md#security)

## Troubleshooting

### Backend not starting
- Check App Runner logs in CloudWatch
- Verify `requirements.txt` is present
- Check environment variables are set correctly

### Frontend can't connect to backend
- Verify `VITE_API_URL` is set correctly (without `/api` suffix)
- Check CORS settings in backend
- Verify App Runner service is running

### Database not persisting
- App Runner uses ephemeral storage by default
- For production, consider using RDS or DynamoDB
- See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md#database-options)

## Cost Estimate

- **App Runner**: ~$25-50/month (1 vCPU, 2GB RAM)
- **Amplify**: ~$0-5/month (depends on traffic)
- **Total**: ~$25-55/month

## Support

For detailed documentation, see [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
