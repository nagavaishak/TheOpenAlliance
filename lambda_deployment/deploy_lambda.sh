#!/bin/bash
set -e

echo "📦 Creating Lambda deployment package..."

# Install dependencies to package directory
pip install -r requirements.txt -t package/

# Copy application code
cp -r agents package/
cp -r tools package/
cp -r sample_configs package/
cp lambda_handler.py package/

# Create ZIP
cd package
zip -r ../autoran-lambda.zip . -x "*.pyc" "*__pycache__*"
cd ..

echo "✅ Deployment package created: autoran-lambda.zip"
echo "📦 Size: $(du -h autoran-lambda.zip | cut -f1)"

# Upload to S3
BUCKET_NAME="autoran-lambda-deploy-$(date +%s)"
echo "🪣 Creating S3 bucket: $BUCKET_NAME"
aws s3 mb s3://$BUCKET_NAME --region us-east-1

echo "⬆️ Uploading to S3..."
aws s3 cp autoran-lambda.zip s3://$BUCKET_NAME/

echo "✅ Uploaded to: s3://$BUCKET_NAME/autoran-lambda.zip"
echo ""
echo "Next steps:"
echo "1. Create Lambda function using this S3 object"
echo "2. Use bucket: $BUCKET_NAME"
