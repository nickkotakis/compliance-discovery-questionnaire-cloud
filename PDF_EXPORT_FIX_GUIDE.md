# PDF Export Fix - Complete Implementation Guide

## Problem Summary

The PDF export functionality was failing with the error:
```
ImportError: cannot import name '_imaging' from 'PIL'
```

**Root Cause**: The `reportlab` library depends on `Pillow` (PIL), which contains compiled C extensions. These extensions are platform-specific:
- Development environment: macOS ARM64 (Apple Silicon)
- AWS Lambda environment: Linux x86_64

When we packaged dependencies on macOS, the compiled `.so` files were built for macOS and don't work on Lambda's Linux environment.

## Solution: Docker-Based Lambda Package Build

We've implemented a Docker-based build process that compiles all dependencies in an environment identical to AWS Lambda.

### Files Created

1. **`backend/Dockerfile.lambda`** - Docker configuration using AWS Lambda Python 3.11 base image
2. **`backend/requirements.txt`** - Complete list of Python dependencies
3. **`backend/build-lambda-package.sh`** - Automated build script

### How It Works

1. **Docker Base Image**: Uses `public.ecr.aws/lambda/python:3.11` - the exact same environment Lambda uses
2. **System Dependencies**: Installs all required system libraries for Pillow (JPEG, PNG, TIFF support, etc.)
3. **Python Dependencies**: Installs all Python packages with native compilation
4. **Package Assembly**: Copies application code and creates deployment package

## Step-by-Step Deployment

### Prerequisites

- Docker installed and running
- AWS CLI configured with Isengard credentials
- CDK installed (`npm install -g aws-cdk`)

### Step 1: Build Lambda Package

```bash
cd backend
./build-lambda-package.sh
```

This will:
- Build a Docker image with all dependencies
- Compile reportlab and Pillow for Linux x86_64
- Create `lambda_package/` directory with everything needed
- Verify the package contents

**Expected output:**
```
Building Lambda deployment package with Docker...
Cleaning up old lambda_package directory...
Building Docker image...
Extracting built package from Docker container...
Verifying package contents...
✓ lambda_handler.py found
✓ compliance_discovery module found
✓ reportlab library found
✓ Pillow (PIL) library found

Package size: 45M

Lambda package built successfully!
```

### Step 2: Deploy to AWS

```bash
cd ../cdk
./deploy.sh
```

Or manually:
```bash
cd ../cdk

# Ensure AWS credentials are set
export AWS_PROFILE=nkotakis+KotakisIsengard-Admin

# Deploy
cdk deploy
```

### Step 3: Test PDF Export

1. Open the application: https://d2q7tpn21dr7r0.cloudfront.net
2. Complete a questionnaire session
3. Click "Export" → "PDF"
4. Verify the PDF downloads successfully

## Verification

### Check Lambda Package Contents

```bash
# List key files
ls -lh backend/lambda_package/ | grep -E "(reportlab|PIL|lambda_handler)"

# Check reportlab
ls backend/lambda_package/reportlab/

# Check Pillow
ls backend/lambda_package/PIL/
```

### Test Locally with Docker

```bash
cd backend

# Build the image
docker build -f Dockerfile.lambda -t compliance-lambda-test .

# Run a test container
docker run --rm -it compliance-lambda-test python3 -c "
from reportlab.lib.pagesizes import letter
from PIL import Image
print('✓ reportlab imported successfully')
print('✓ Pillow imported successfully')
"
```

### Check Lambda Logs

```bash
# Get recent logs
aws logs tail /aws/lambda/ComplianceDiscoveryStack-ApiFunctionCE271BD4-B8iztN4UA52c \
    --follow \
    --profile nkotakis+KotakisIsengard-Admin
```

## Troubleshooting

### Issue: Docker build fails

**Solution**: Ensure Docker is running and you have internet connectivity
```bash
docker ps  # Should show Docker is running
```

### Issue: Package size too large

Lambda has a 250MB unzipped limit. Our package should be ~45MB.

**Check size:**
```bash
du -sh backend/lambda_package/
```

**If too large**, remove unnecessary files:
```bash
cd backend/lambda_package
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -type d -name "*.dist-info" -exec rm -rf {} +
find . -type d -name "tests" -exec rm -rf {} +
```

### Issue: PDF export still fails after deployment

**Check Lambda logs:**
```bash
aws logs tail /aws/lambda/ComplianceDiscoveryStack-ApiFunctionCE271BD4-B8iztN4UA52c \
    --since 5m \
    --profile nkotakis+KotakisIsengard-Admin
```

**Common issues:**
1. Old package still deployed - redeploy with `cdk deploy --force`
2. Lambda timeout - increase timeout in `cdk/cdk/compliance_discovery_stack.py`
3. Memory limit - increase memory_size in CDK stack

### Issue: ImportError for other libraries

**Solution**: Add missing library to `backend/requirements.txt` and rebuild:
```bash
cd backend
echo "missing-library==1.0.0" >> requirements.txt
./build-lambda-package.sh
cd ../cdk
cdk deploy
```

## Alternative Solutions (If Docker Doesn't Work)

### Option 1: Use AWS Lambda Layers

Create a Lambda Layer with pre-compiled dependencies:

```bash
# Build layer
cd backend
mkdir -p layer/python
pip install -r requirements.txt -t layer/python/

# Create layer zip
cd layer
zip -r ../lambda-layer.zip .

# Upload to Lambda Layer
aws lambda publish-layer-version \
    --layer-name compliance-discovery-deps \
    --zip-file fileb://../lambda-layer.zip \
    --compatible-runtimes python3.11 \
    --profile nkotakis+KotakisIsengard-Admin
```

Then update CDK stack to use the layer.

### Option 2: Use Pure Python PDF Library

Replace reportlab with a pure Python alternative:

```python
# Install fpdf2 (pure Python)
pip install fpdf2

# Update api_server.py to use fpdf2 instead of reportlab
```

### Option 3: Use External PDF Service

Use a service like WeasyPrint or Puppeteer:

```python
# Generate HTML
html_content = render_template('questionnaire.html', data=template_data)

# Convert to PDF using external service
pdf_bytes = convert_html_to_pdf(html_content)
```

## Package Size Optimization

If the package is too large, optimize it:

```bash
cd backend/lambda_package

# Remove test files
find . -type d -name "tests" -exec rm -rf {} +
find . -type d -name "test" -exec rm -rf {} +

# Remove documentation
find . -type d -name "docs" -exec rm -rf {} +
find . -type f -name "*.md" -delete

# Remove cache
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -type f -name "*.pyc" -delete
find . -type f -name "*.pyo" -delete

# Remove dist-info
find . -type d -name "*.dist-info" -exec rm -rf {} +

# Remove unnecessary Pillow components
rm -rf PIL/Tests/
```

## Deployment Information

**Current Deployment:**
- **Account**: KotakisIsengard (620360465022)
- **Region**: us-east-1
- **Profile**: nkotakis+KotakisIsengard-Admin
- **Lambda Function**: ComplianceDiscoveryStack-ApiFunctionCE271BD4-B8iztN4UA52c
- **API URL**: https://zr5mc40584.execute-api.us-east-1.amazonaws.com/prod/
- **Frontend URL**: https://d2q7tpn21dr7r0.cloudfront.net

## Next Steps

1. **Build the package**: `cd backend && ./build-lambda-package.sh`
2. **Deploy to AWS**: `cd ../cdk && ./deploy.sh`
3. **Test PDF export**: Open app and try exporting a questionnaire as PDF
4. **Monitor logs**: Check CloudWatch logs for any errors
5. **Verify success**: Download and open the PDF file

## Success Criteria

✓ Docker build completes without errors
✓ Lambda package contains reportlab and PIL directories
✓ Package size is under 250MB
✓ CDK deployment succeeds
✓ PDF export returns HTTP 200 with valid PDF file
✓ PDF opens correctly in PDF reader
✓ PDF contains all questionnaire content with proper formatting

## AWS SAS Compliance Note

This implementation follows AWS SAS best practices for serverless deployments:
- Infrastructure as Code (CDK)
- Automated build process
- Proper error handling
- Comprehensive logging
- Security best practices (no hardcoded credentials)

---

**AWS Security Assurance Services (AWS SAS) - Internal Use Only**

This guide provides technical implementation guidance exclusively. For compliance or regulatory questions, consult qualified legal counsel.
