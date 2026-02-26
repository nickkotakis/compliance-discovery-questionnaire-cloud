# AWS Deployment Documentation

This directory contains all documentation and scripts for deploying the Compliance Discovery Questionnaire to AWS.

## Quick Links

- **[QUICKSTART.md](QUICKSTART.md)** - Deploy in 15 minutes
- **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)** - Comprehensive deployment guide
- **[PRE_DEPLOYMENT_CHECKLIST.md](PRE_DEPLOYMENT_CHECKLIST.md)** - Pre-flight checklist
- **[deploy.sh](deploy.sh)** - Interactive deployment helper script

## Architecture

```
┌─────────────────┐
│   AWS Amplify   │  Frontend (React + TypeScript)
│   (Frontend)    │  - Static hosting
└────────┬────────┘  - CI/CD from GitHub
         │
         │ HTTPS
         │
┌────────▼────────┐
│  AWS App Runner │  Backend (Python Flask)
│   (Backend)     │  - Auto-scaling
└─────────────────┘  - Managed containers
```

## Services Used

1. **AWS App Runner** - Backend API hosting
   - Automatic scaling
   - Managed container runtime
   - Built-in load balancing
   - Cost: ~$25-50/month

2. **AWS Amplify** - Frontend hosting
   - Static site hosting
   - CI/CD from GitHub
   - Custom domain support
   - Cost: ~$0-5/month

## Deployment Options

### Option 1: Quick Deploy (Recommended)
Follow [QUICKSTART.md](QUICKSTART.md) for a 15-minute deployment using AWS Console.

### Option 2: CLI Deployment
Use the [deploy.sh](deploy.sh) script for an interactive CLI-based deployment.

### Option 3: Manual Deployment
Follow [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed step-by-step instructions.

## Repository Structure

```
compliance-discovery-questionnaire/
├── backend/
│   ├── compliance_discovery/    # Python application code
│   ├── Dockerfile              # Container configuration
│   ├── apprunner.yaml          # App Runner service config
│   ├── .dockerignore           # Docker build exclusions
│   └── requirements.txt        # Python dependencies
├── frontend/
│   ├── src/                    # React application code
│   ├── amplify.yml             # Amplify build config
│   ├── .env.example            # Environment variables template
│   └── package.json            # Node dependencies
└── aws-deployment/
    ├── QUICKSTART.md           # Quick deployment guide
    ├── DEPLOYMENT_GUIDE.md     # Comprehensive guide
    ├── PRE_DEPLOYMENT_CHECKLIST.md
    └── deploy.sh               # Deployment helper script
```

## Prerequisites

- AWS Account with appropriate permissions
- AWS CLI configured
- GitHub account
- Basic knowledge of AWS services

## Cost Estimate

| Service | Configuration | Monthly Cost |
|---------|--------------|--------------|
| App Runner | 1 vCPU, 2GB RAM | $25-50 |
| Amplify | Static hosting | $0-5 |
| **Total** | | **$25-55** |

*Costs may vary based on usage and region*

## Support

For issues or questions:
1. Check [QUICKSTART.md](QUICKSTART.md#troubleshooting)
2. Review [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
3. Open an issue on GitHub

## Next Steps

1. Review [PRE_DEPLOYMENT_CHECKLIST.md](PRE_DEPLOYMENT_CHECKLIST.md)
2. Follow [QUICKSTART.md](QUICKSTART.md)
3. Configure custom domain (optional)
4. Set up monitoring and alerts
