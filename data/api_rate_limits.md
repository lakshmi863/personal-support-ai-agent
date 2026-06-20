# API Rate Limiting Policy
To ensure stability, Adsparkx limits requests based on subscription tier:
- Free Tier: 50 requests per minute (RPM).
- Pro Tier: 500 requests per minute (RPM).
- Enterprise: Custom limits (Default 2000 RPM).
If you exceed these limits, you will receive a '429 Too Many Requests' error. 
Please implement exponential backoff in your code logic.