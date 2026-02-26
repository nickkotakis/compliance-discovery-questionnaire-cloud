# 🎯 START HERE - Compliance Discovery Questionnaire

Welcome! This guide will get you up and running quickly.

## What is this?

A web application for conducting NIST 800-53 compliance assessments with AWS implementation guidance. It helps you:
- Generate compliance questionnaires
- Map controls to AWS services
- Export professional reports (Excel, PDF, JSON, YAML)
- Track assessment progress

## Quick Links

- **Deploy to AWS** (15 min): [aws-deployment/QUICKSTART.md](aws-deployment/QUICKSTART.md)
- **Run Locally**: See below
- **Full Documentation**: [aws-deployment/DEPLOYMENT_GUIDE.md](aws-deployment/DEPLOYMENT_GUIDE.md)

## Run Locally (5 minutes)

### Prerequisites
- Python 3.11+
- Node.js 18+
- npm or yarn

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
python -m compliance_discovery.api_server
```

Backend runs on http://localhost:5001

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend runs on http://localhost:5173

## Deploy to AWS (15 minutes)

See [aws-deployment/QUICKSTART.md](aws-deployment/QUICKSTART.md) for step-by-step instructions.

**Services used:**
- AWS App Runner (backend)
- AWS Amplify (frontend)
- Estimated cost: $25-55/month

## Project Structure

```
├── backend/                 # Python Flask API
│   ├── compliance_discovery/
│   ├── Dockerfile          # Container configuration
│   ├── apprunner.yaml      # App Runner configuration
│   └── requirements.txt
├── frontend/               # React TypeScript UI
│   ├── src/
│   ├── amplify.yml        # Amplify configuration
│   └── package.json
└── aws-deployment/        # Deployment documentation
    ├── QUICKSTART.md      # 15-minute deployment guide
    └── DEPLOYMENT_GUIDE.md # Comprehensive guide
```

## Features

- **177 NIST 800-53 Controls** (Moderate Baseline)
- **134 Discovery Questions** across all control families
- **53 AWS Implementation Guides** for Shared responsibility controls
- **Professional Exports**: Excel, PDF (fillable), JSON, YAML
- **Session Management**: Save and resume assessments
- **AWS Responsibility Mapping**: Automatic classification (AWS/Customer/Shared)

## Need Help?

1. **Deployment Issues**: See [aws-deployment/QUICKSTART.md](aws-deployment/QUICKSTART.md#troubleshooting)
2. **Local Development**: See [README.md](README.md)
3. **AWS Configuration**: See [aws-deployment/DEPLOYMENT_GUIDE.md](aws-deployment/DEPLOYMENT_GUIDE.md)

## Next Steps

1. ✅ Run locally to test
2. ✅ Deploy to AWS
3. ✅ Configure custom domain (optional)
4. ✅ Set up authentication (optional)
5. ✅ Start your first assessment!

---

**Repository**: https://github.com/nickkotakis/compliance-discovery-questionnaire
