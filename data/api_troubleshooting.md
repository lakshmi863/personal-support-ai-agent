# API Troubleshooting Guide
If you receive a '401 Unauthorized' error, ensure your Bearer token is valid.
Check the header format: 'Authorization: Bearer YOUR_TOKEN'.
The '500 Internal Server Error' usually implies a malformed JSON body in the request. 
Check for missing trailing commas or invalid data types in the integration portal.


## Bearer Token Authentication
The Authorization header must follow this exact format:
Authorization: Bearer YOUR_ACCESS_TOKEN

## Header Requirements
- Content-Type: application/json
- Authorization: Bearer <your_token>
- Accept: application/json

## Common Errors
- 401 Unauthorized: Token is missing, expired, or malformed.
- 403 Forbidden: Token is valid but lacks required permissions.
- 500 Internal Server Error: Usually caused by malformed JSON body.

## How to Get a Token
1. Log in to the developer portal.
2. Navigate to Settings > API Keys.
3. Click Generate New Token.
4. Copy the token and include it in every API request header.

## Token Expiry
Tokens expire after 24 hours. Regenerate from the portal when expired.