#!/usr/bin/env bash
# Build Lambda deployment package using Docker
# This ensures all dependencies (especially reportlab and Pillow) are compiled for Lambda's Linux environment

set -euo pipefail

echo "Building Lambda deployment package with Docker..."

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Clean up old package
echo "Cleaning up old lambda_package directory..."
rm -rf lambda_package
mkdir -p lambda_package

# Build Docker image
echo "Building Docker image..."
docker build -f Dockerfile.lambda -t compliance-lambda-builder .

# Create container and copy built package
echo "Extracting built package from Docker container..."
CONTAINER_ID=$(docker create compliance-lambda-builder)
docker cp "$CONTAINER_ID:/asset/." lambda_package/
docker rm "$CONTAINER_ID"

# Verify the package
echo ""
echo "Verifying package contents..."
if [ -f "lambda_package/lambda_handler.py" ]; then
    echo "✓ lambda_handler.py found"
else
    echo "✗ lambda_handler.py NOT found"
    exit 1
fi

if [ -d "lambda_package/compliance_discovery" ]; then
    echo "✓ compliance_discovery module found"
else
    echo "✗ compliance_discovery module NOT found"
    exit 1
fi

if [ -d "lambda_package/reportlab" ]; then
    echo "✓ reportlab library found"
else
    echo "✗ reportlab library NOT found"
    exit 1
fi

if [ -d "lambda_package/PIL" ]; then
    echo "✓ Pillow (PIL) library found"
else
    echo "✗ Pillow (PIL) library NOT found"
    exit 1
fi

# Check package size
PACKAGE_SIZE=$(du -sh lambda_package | cut -f1)
echo ""
echo "Package size: $PACKAGE_SIZE"
echo ""
echo "Lambda package built successfully!"
echo "Package location: $SCRIPT_DIR/lambda_package/"
echo ""
echo "Next steps:"
echo "1. Deploy with CDK: cd ../cdk && ./deploy.sh"
echo "2. Or manually: cd ../cdk && cdk deploy"
