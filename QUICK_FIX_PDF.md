# Quick Fix: PDF Export

## TL;DR - Fix PDF Export in 3 Commands

```bash
# 1. Build Lambda package with Docker
cd backend && ./build-lambda-package.sh

# 2. Deploy to AWS
cd ../cdk && ./deploy.sh

# 3. Test
# Open https://d2q7tpn21dr7r0.cloudfront.net and try PDF export
```

## What This Does

- Builds Lambda package using Docker with AWS Lambda Python 3.11 base image
- Compiles reportlab and Pillow for Linux x86_64 (Lambda's environment)
- Deploys updated Lambda function with working PDF export

## Expected Results

**Before Fix:**
```
HTTP 503 - PDF export is temporarily unavailable
```

**After Fix:**
```
HTTP 200 - compliance-questionnaire.pdf downloads successfully
```

## If It Fails

### Docker authentication required?
```bash
# Sign in to Docker Desktop
# Open Docker Desktop app and sign in with your Amazon credentials

# Verify Docker is authenticated
docker ps

# Then retry
cd backend && ./build-lambda-package.sh
```

### Docker not running?
```bash
# Start Docker Desktop
open -a Docker

# Wait for Docker to start, then retry
cd backend && ./build-lambda-package.sh
```

### Build succeeds but PDF still fails?
```bash
# Check Lambda logs
aws logs tail /aws/lambda/ComplianceDiscoveryStack-ApiFunctionCE271BD4-B8iztN4UA52c \
    --since 5m \
    --profile nkotakis+KotakisIsengard-Admin

# Force redeploy
cd cdk && cdk deploy --force
```

### Package too large?
```bash
# Optimize package
cd backend/lambda_package
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -type d -name "tests" -exec rm -rf {} +
find . -type d -name "*.dist-info" -exec rm -rf {} +

# Redeploy
cd ../../cdk && cdk deploy
```

## Full Documentation

See `PDF_EXPORT_FIX_GUIDE.md` for complete details, troubleshooting, and alternative solutions.

---

**Status**: Ready to deploy
**Time to fix**: ~5 minutes (build + deploy)
**Risk**: Low (Excel export still works as fallback)
