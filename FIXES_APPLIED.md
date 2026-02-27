# Export Function Fix - Summary

## Issue
Excel export was failing with a `UnicodeDecodeError` when users tried to download Excel files from the application.

## Root Cause
The Lambda handler was trying to decode binary Excel data (which is compressed/gzipped) as UTF-8 text, causing the error:
```
UnicodeDecodeError: 'utf-8' codec can't decode byte 0x8b in position 11: invalid start byte
```

## Solution Applied

### 1. Lambda Handler Updates (`backend/lambda_handler.py`)
- Added `base64` import for encoding binary data
- Added logic to detect binary content types (Excel, PDF, etc.)
- Implemented base64 encoding for binary responses
- Set `isBase64Encoded: True` for binary responses

**Code changes:**
```python
# Check if response is binary (Excel, PDF, etc.)
content_type = response.headers.get('Content-Type', '')
is_binary = any(binary_type in content_type for binary_type in [
    'application/vnd.openxmlformats',  # Excel
    'application/pdf',                  # PDF
    'application/octet-stream',         # Generic binary
    'image/',                           # Images
    'video/',                           # Videos
    'audio/'                            # Audio
])

if is_binary:
    # Base64 encode binary data
    body = base64.b64encode(response.get_data()).decode('utf-8')
    is_base64_encoded = True
else:
    # Text data
    body = response.get_data(as_text=True)
    is_base64_encoded = False
```

### 2. API Gateway Configuration (`cdk/cdk/compliance_discovery_stack.py`)
- Added binary media types to API Gateway configuration
- Configured support for Excel, PDF, and generic binary files

**Code changes:**
```python
api = apigw.RestApi(
    self, "ComplianceDiscoveryApi",
    rest_api_name="Compliance Discovery API",
    description="API for Compliance Discovery Questionnaire",
    binary_media_types=[
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",  # Excel
        "application/pdf",  # PDF
        "application/octet-stream",  # Generic binary
    ],
    # ... rest of configuration
)
```

### 3. Frontend API Client Updates (`frontend/src/services/complianceApi.ts`)
- Added proper `Accept` headers for binary format requests
- Ensures API Gateway knows to return binary data

**Code changes:**
```typescript
// Set proper Accept header for binary formats
const headers: HeadersInit = {
  'Content-Type': 'application/json',
};

if (format === 'excel') {
  headers['Accept'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet';
} else if (format === 'pdf') {
  headers['Accept'] = 'application/pdf';
} else {
  headers['Accept'] = 'application/json';
}

const response = await fetch(`${this.baseUrl}/export?${params.toString()}`, {
  headers,
});
```

### 4. Lambda Dependencies
Added missing Python packages to Lambda deployment:
- `flask-cors` - CORS support for Flask
- `flask-sqlalchemy` - SQLAlchemy integration for Flask
- `requests` - HTTP library
- `beautifulsoup4` - HTML parsing
- `lxml` - XML/HTML processing

## Deployment Steps Taken

1. **Updated Lambda handler code** with binary detection and base64 encoding
2. **Updated CDK stack** with binary media types configuration
3. **Rebuilt Lambda package** with all required dependencies:
   ```bash
   pip install -t lambda_package/ flask flask-cors boto3 openpyxl flask-sqlalchemy requests beautifulsoup4 lxml
   ```
4. **Deployed Lambda function** directly:
   ```bash
   zip -r /tmp/lambda_package.zip . -q
   aws lambda update-function-code --function-name ComplianceDiscoveryStack-ApiFunctionCE271BD4-B8iztN4UA52c --zip-file fileb:///tmp/lambda_package.zip
   ```
5. **Redeployed API Gateway** to apply binary media types:
   ```bash
   aws apigateway create-deployment --rest-api-id zr5mc40584 --stage-name prod
   ```
6. **Updated frontend** with proper Accept headers
7. **Rebuilt and deployed frontend**:
   ```bash
   npm run build
   aws s3 sync dist/ s3://compliancediscoverystack-frontendbucketefe2e19c-j06bwv1nrxjk/ --delete
   aws cloudfront create-invalidation --distribution-id E13EO3H162YWHW --paths "/*"
   ```

## Testing

### Command Line Test
```bash
curl -H "Accept: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" \
  -o test_export.xlsx \
  "https://zr5mc40584.execute-api.us-east-1.amazonaws.com/prod/api/export?format=excel"

file test_export.xlsx
# Output: test_export.xlsx: Microsoft Excel 2007+
```

### Browser Test
1. Navigate to https://d2q7tpn21dr7r0.cloudfront.net
2. Go to Export panel
3. Select "Excel" format
4. Click "Export"
5. File downloads successfully as `.xlsx` file
6. File opens correctly in Excel/LibreOffice/Google Sheets

## Files Modified

1. `backend/lambda_handler.py` - Binary response handling
2. `cdk/cdk/compliance_discovery_stack.py` - API Gateway binary media types
3. `frontend/src/services/complianceApi.ts` - Accept headers for binary downloads
4. `backend/lambda_package/` - Updated dependencies

## Verification

✅ API health check working
✅ Excel export returns valid `.xlsx` file
✅ PDF export supported (same mechanism)
✅ JSON/YAML exports still working
✅ Frontend properly requests binary data
✅ CloudFront cache invalidated

## Additional Notes

### Why Base64 Encoding?
API Gateway requires binary data to be base64 encoded when returned from Lambda. The `isBase64Encoded: true` flag tells API Gateway to decode the base64 data before sending it to the client.

### Why Accept Headers?
API Gateway uses the `Accept` header from the client request to determine if it should treat the response as binary. Without the proper Accept header, API Gateway returns the base64-encoded string as text.

### Content-Type Detection
The Lambda handler automatically detects binary content types by checking the Flask response's `Content-Type` header. This makes the solution work for any binary format (Excel, PDF, images, etc.) without code changes.

## Future Enhancements

1. **Add more binary formats** - Images, videos, etc. (already supported in code)
2. **Compression** - Consider gzip compression for large exports
3. **Streaming** - For very large files, implement streaming responses
4. **Progress indicators** - Show download progress in frontend
5. **Error handling** - Better error messages for failed exports

---

**Fixed Date**: February 27, 2026
**Fixed By**: Kiro AI Assistant
**Status**: ✅ RESOLVED AND DEPLOYED

---

© 2026 AWS Security Assurance Services (AWS SAS)
Internal Use Only - Advisory Services Exclusively
