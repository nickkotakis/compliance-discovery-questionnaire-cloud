"""
AWS Lambda handler for Compliance Discovery API
Wraps the Flask app for Lambda execution
"""
import json
import os
import base64
from compliance_discovery.api_server import app

def handler(event, context):
    """
    Lambda handler function
    
    Args:
        event: API Gateway event
        context: Lambda context
        
    Returns:
        API Gateway response
    """
    # Handle API Gateway proxy integration
    path = event.get('path', '/')
    http_method = event.get('httpMethod', 'GET')
    headers = event.get('headers', {})
    query_params = event.get('queryStringParameters', {}) or {}
    body = event.get('body', '')
    
    # Create WSGI environment
    environ = {
        'REQUEST_METHOD': http_method,
        'PATH_INFO': path,
        'QUERY_STRING': '&'.join([f'{k}={v}' for k, v in query_params.items()]),
        'CONTENT_TYPE': headers.get('content-type', ''),
        'CONTENT_LENGTH': str(len(body)) if body else '0',
        'SERVER_NAME': 'lambda',
        'SERVER_PORT': '443',
        'wsgi.version': (1, 0),
        'wsgi.url_scheme': 'https',
        'wsgi.input': body,
        'wsgi.errors': None,
        'wsgi.multithread': False,
        'wsgi.multiprocess': False,
        'wsgi.run_once': False,
    }
    
    # Add headers to environ
    for key, value in headers.items():
        key = key.upper().replace('-', '_')
        if key not in ('CONTENT_TYPE', 'CONTENT_LENGTH'):
            environ[f'HTTP_{key}'] = value
    
    # Use Flask test client to handle request
    with app.test_client() as client:
        if http_method == 'GET':
            response = client.get(path, query_string=query_params, headers=headers)
        elif http_method == 'POST':
            response = client.post(path, data=body, headers=headers)
        elif http_method == 'PUT':
            response = client.put(path, data=body, headers=headers)
        elif http_method == 'DELETE':
            response = client.delete(path, headers=headers)
        elif http_method == 'OPTIONS':
            response = client.options(path, headers=headers)
        else:
            return {
                'statusCode': 405,
                'body': json.dumps({'error': 'Method not allowed'}),
                'headers': {'Content-Type': 'application/json'}
            }
    
    # Convert Flask response to API Gateway response
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
    
    return {
        'statusCode': response.status_code,
        'body': body,
        'headers': dict(response.headers),
        'isBase64Encoded': is_base64_encoded
    }
