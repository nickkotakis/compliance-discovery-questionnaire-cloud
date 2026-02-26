#!/bin/bash

# Compliance Discovery Questionnaire - AWS Deployment Helper
# This script helps deploy the application to AWS App Runner and Amplify

set -e

echo "🚀 Compliance Discovery Questionnaire - AWS Deployment Helper"
echo "=============================================================="
echo ""

# Check prerequisites
echo "Checking prerequisites..."

if ! command -v aws &> /dev/null; then
    echo "❌ AWS CLI not found. Please install it first:"
    echo "   https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html"
    exit 1
fi

if ! aws sts get-caller-identity &> /dev/null; then
    echo "❌ AWS CLI not configured. Please run 'aws configure' first."
    exit 1
fi

echo "✅ AWS CLI configured"
echo ""

# Get AWS account info
AWS_ACCOUNT=$(aws sts get-caller-identity --query Account --output text)
AWS_REGION=$(aws configure get region || echo "us-east-1")

echo "AWS Account: $AWS_ACCOUNT"
echo "AWS Region: $AWS_REGION"
echo ""

# Deployment options
echo "Deployment Options:"
echo "1. Deploy Backend (App Runner)"
echo "2. Deploy Frontend (Amplify)"
echo "3. Deploy Both"
echo "4. Update CORS Settings"
echo "5. Check Deployment Status"
echo "6. Exit"
echo ""

read -p "Select option (1-6): " option

case $option in
    1|3)
        echo ""
        echo "📦 Deploying Backend to App Runner..."
        echo ""
        
        read -p "Enter service name [compliance-discovery-api]: " SERVICE_NAME
        SERVICE_NAME=${SERVICE_NAME:-compliance-discovery-api}
        
        echo "Creating App Runner service: $SERVICE_NAME"
        echo "This may take 5-10 minutes..."
        
        # Note: This requires GitHub connection to be set up first
        echo ""
        echo "⚠️  Manual step required:"
        echo "1. Go to https://console.aws.amazon.com/apprunner/"
        echo "2. Click 'Create service'"
        echo "3. Connect to GitHub repository: nickkotakis/compliance-discovery-questionnaire"
        echo "4. Branch: main"
        echo "5. Source directory: /backend"
        echo "6. Use apprunner.yaml for configuration"
        echo ""
        read -p "Press Enter when App Runner service is created..."
        
        read -p "Enter the App Runner service URL: " BACKEND_URL
        echo "Backend URL: $BACKEND_URL"
        echo ""
        
        if [ "$option" == "1" ]; then
            echo "✅ Backend deployment initiated!"
            exit 0
        fi
        ;&
    2)
        echo ""
        echo "🎨 Deploying Frontend to Amplify..."
        echo ""
        
        if [ -z "$BACKEND_URL" ]; then
            read -p "Enter your App Runner backend URL: " BACKEND_URL
        fi
        
        echo "⚠️  Manual step required:"
        echo "1. Go to https://console.aws.amazon.com/amplify/"
        echo "2. Click 'New app' → 'Host web app'"
        echo "3. Connect GitHub repository: nickkotakis/compliance-discovery-questionnaire"
        echo "4. Branch: main"
        echo "5. Set app root to: /frontend"
        echo "6. Add environment variable:"
        echo "   Key: VITE_API_URL"
        echo "   Value: $BACKEND_URL"
        echo ""
        read -p "Press Enter when Amplify app is created..."
        
        read -p "Enter the Amplify app URL: " FRONTEND_URL
        echo "Frontend URL: $FRONTEND_URL"
        echo ""
        echo "✅ Frontend deployment initiated!"
        echo ""
        echo "⚠️  Don't forget to update CORS settings (option 4)"
        ;;
    4)
        echo ""
        echo "🔒 Updating CORS Settings..."
        echo ""
        
        read -p "Enter your frontend URL: " FRONTEND_URL
        
        echo "⚠️  Manual step required:"
        echo "1. Go to https://console.aws.amazon.com/apprunner/"
        echo "2. Select your service"
        echo "3. Go to Configuration → Environment variables"
        echo "4. Update CORS_ORIGINS to: $FRONTEND_URL"
        echo "5. Click 'Deploy'"
        echo ""
        read -p "Press Enter when done..."
        echo "✅ CORS settings updated!"
        ;;
    5)
        echo ""
        echo "📊 Checking Deployment Status..."
        echo ""
        echo "App Runner services:"
        aws apprunner list-services --query 'ServiceSummaryList[*].[ServiceName,Status,ServiceUrl]' --output table
        echo ""
        echo "Amplify apps:"
        aws amplify list-apps --query 'apps[*].[name,defaultDomain]' --output table
        ;;
    6)
        echo "Goodbye!"
        exit 0
        ;;
    *)
        echo "Invalid option"
        exit 1
        ;;
esac

echo ""
echo "🎉 Deployment complete!"
echo ""
echo "Next steps:"
echo "1. Test your application"
echo "2. Set up custom domain (optional)"
echo "3. Configure authentication (optional)"
echo "4. Set up monitoring"
echo ""
echo "For more information, see:"
echo "- QUICKSTART.md"
echo "- DEPLOYMENT_GUIDE.md"
