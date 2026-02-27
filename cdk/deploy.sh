#!/usr/bin/env bash
set -e

echo "🚀 Compliance Discovery Questionnaire - CDK Deployment"
echo "========================================================"
echo ""

# Check if authenticated
if ! aws sts get-caller-identity &> /dev/null; then
    echo "❌ Not authenticated with AWS"
    echo "Run: export AWS_PROFILE='nkotakis+KotakisIsengard-Admin'"
    exit 1
fi

echo "✅ AWS Authentication verified"
AWS_ACCOUNT=$(aws sts get-caller-identity --query Account --output text)
AWS_REGION=$(aws configure get region || echo "us-east-1")
echo "Account: $AWS_ACCOUNT"
echo "Region: $AWS_REGION"
echo ""

# Step 1: Install CDK dependencies
echo "📦 Installing CDK dependencies..."
source .venv/bin/activate
pip install -q --upgrade pip
pip install -q -r requirements.txt
echo "✅ Dependencies installed"
echo ""

# Step 2: Build frontend
echo "🎨 Building frontend..."
cd ../frontend
npm install --silent
npm run build
echo "✅ Frontend built"
echo ""

# Step 3: Bootstrap CDK (if needed)
echo "🔧 Checking CDK bootstrap..."
cd ../cdk
if ! aws cloudformation describe-stacks --stack-name CDKToolkit &> /dev/null; then
    echo "Bootstrapping CDK..."
    cdk bootstrap
else
    echo "✅ CDK already bootstrapped"
fi
echo ""

# Step 4: Deploy stack
echo "☁️  Deploying CDK stack..."
cdk deploy --require-approval never
echo "✅ Stack deployed"
echo ""

# Step 5: Get outputs
echo "📋 Deployment Outputs:"
aws cloudformation describe-stacks \
  --stack-name ComplianceDiscoveryStack \
  --query 'Stacks[0].Outputs[*].[OutputKey,OutputValue]' \
  --output table
echo ""

# Step 6: Upload frontend
echo "📤 Uploading frontend to S3..."
BUCKET_NAME=$(aws cloudformation describe-stacks \
  --stack-name ComplianceDiscoveryStack \
  --query 'Stacks[0].Outputs[?OutputKey==`FrontendBucketName`].OutputValue' \
  --output text)

aws s3 sync ../frontend/dist/ s3://$BUCKET_NAME/ --delete --quiet
echo "✅ Frontend uploaded"
echo ""

# Step 7: Invalidate CloudFront
echo "🔄 Invalidating CloudFront cache..."
DISTRIBUTION_ID=$(aws cloudfront list-distributions \
  --query "DistributionList.Items[?Origins.Items[0].DomainName=='$BUCKET_NAME.s3.amazonaws.com'].Id" \
  --output text)

if [ -n "$DISTRIBUTION_ID" ]; then
    aws cloudfront create-invalidation \
      --distribution-id $DISTRIBUTION_ID \
      --paths "/*" \
      --query 'Invalidation.Id' \
      --output text
    echo "✅ Cache invalidated"
else
    echo "⚠️  Could not find CloudFront distribution"
fi
echo ""

# Step 8: Get URLs
API_URL=$(aws cloudformation describe-stacks \
  --stack-name ComplianceDiscoveryStack \
  --query 'Stacks[0].Outputs[?OutputKey==`ApiUrl`].OutputValue' \
  --output text)

FRONTEND_URL=$(aws cloudformation describe-stacks \
  --stack-name ComplianceDiscoveryStack \
  --query 'Stacks[0].Outputs[?OutputKey==`FrontendUrl`].OutputValue' \
  --output text)

echo "🎉 Deployment Complete!"
echo ""
echo "📍 Your Application URLs:"
echo "   Frontend: $FRONTEND_URL"
echo "   API:      $API_URL"
echo ""
echo "⚠️  Note: CloudFront distribution may take 15-20 minutes to fully deploy"
echo ""
echo "Next steps:"
echo "1. Test API: curl $API_URL/api/health"
echo "2. Open frontend: open $FRONTEND_URL"
echo "3. Update CORS if needed (see DEPLOYMENT_GUIDE.md)"
