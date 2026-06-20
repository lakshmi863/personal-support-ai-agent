# SaaS Product Support Knowledge Base

## 1. Account & Subscription Management

### How to Upgrade or Downgrade Your Plan
- Log in to your account dashboard at app.example.com
- Navigate to **Settings > Billing > Subscription**
- Click **Change Plan** and select your desired tier
- Changes take effect at the start of the next billing cycle
- Downgrading will not delete your data, but may restrict access to premium features

### How to Cancel Your Subscription
- Go to **Settings > Billing > Cancel Subscription**
- Select a cancellation reason and confirm
- Your account remains active until the end of the current billing period
- Data is retained for 30 days after cancellation before permanent deletion
- To reactivate, log in and select **Reactivate Plan**

### Adding or Removing Team Members
- Navigate to **Settings > Team > Members**
- Click **Invite Member**, enter the email address, and assign a role (Admin, Editor, Viewer)
- To remove a member, click the three-dot menu next to their name and select **Remove**
- Seat-based plans will automatically adjust billing on the next invoice

---

## 2. Login & Authentication Issues

### Forgot Password
1. Go to the login page and click **Forgot Password**
2. Enter your registered email address
3. Check your inbox for a reset link (valid for 24 hours)
4. If no email received, check spam/junk folder
5. If still not received, contact support with your account email

### Two-Factor Authentication (2FA)
- Enable 2FA under **Settings > Security > Two-Factor Authentication**
- Supported methods: Authenticator App (Google/Authy), SMS OTP
- If locked out due to lost 2FA device, use backup codes provided during setup
- Backup codes are available under **Settings > Security > View Backup Codes**

### SSO (Single Sign-On) Configuration
- SSO is available on Enterprise plans only
- Supported protocols: SAML 2.0, OAuth 2.0
- To configure, go to **Settings > Security > SSO** and upload your IdP metadata XML
- Contact support if your IdP is not listed in the supported providers

---

## 3. API & Integration Issues

### API Rate Limits
- Free Plan: 100 requests/hour
- Pro Plan: 1,000 requests/hour
- Enterprise Plan: Custom limits (contact sales)
- Rate limit headers returned: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`
- On limit breach, API returns HTTP 429 Too Many Requests

### Webhook Configuration
- Navigate to **Settings > Integrations > Webhooks**
- Click **Add Webhook**, enter your endpoint URL, and select events to subscribe to
- Supported events: `user.created`, `subscription.updated`, `payment.failed`
- Webhook payloads are signed using HMAC-SHA256; verify using your webhook secret
- Retry policy: 3 attempts with exponential backoff on failure

### Common API Error Codes
| Code | Meaning | Resolution |
|------|---------|------------|
| 401 | Unauthorized | Check API key validity |
| 403 | Forbidden | Verify permissions/scopes |
| 404 | Not Found | Confirm endpoint URL |
| 429 | Rate Limit Exceeded | Reduce request frequency |
| 500 | Internal Server Error | Retry after 30 seconds; contact support if persistent |

---

## 4. Data & Storage

### Data Export
- Export your data at any time via **Settings > Data > Export**
- Supported formats: CSV, JSON, XLSX
- Large exports are processed in the background; a download link is emailed upon completion

### Storage Limits by Plan
| Plan | Storage |
|------|---------|
| Free | 5 GB |
| Pro | 50 GB |
| Enterprise | Unlimited |

### Data Backup Policy
- Automated daily backups retained for 30 days
- Point-in-time recovery available on Enterprise plans
- Manual snapshots can be triggered from **Settings > Data > Backups**

---

## 5. Performance & Downtime

### Checking Service Status
- Visit status.example.com for real-time uptime information
- Subscribe to status updates via email or SMS on the status page

### Reporting a Bug
- Go to **Help > Report a Bug** inside the application
- Attach screenshots or screen recordings if possible
- Include your browser version, OS, and steps to reproduce
- Our engineering team responds within 24 hours for Pro/Enterprise plans
