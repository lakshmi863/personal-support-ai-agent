# Cloud Services Support Knowledge Base

## 1. Account & Access Management

### Creating a Cloud Account
1. Visit cloud.example.com and click **Sign Up**
2. Enter your organization email and set a strong password
3. Verify your email address via the confirmation link
4. Complete your organization profile and billing information
5. Select a plan (Free Tier, Standard, Enterprise)

### IAM (Identity and Access Management)
- Create users and groups under **Console > IAM > Users**
- Assign roles using least-privilege principles
- Predefined roles: Viewer, Editor, Admin, Billing Admin
- Custom roles can be created with granular permission sets
- Service accounts are used for application-to-cloud authentication

### Multi-Factor Authentication (MFA)
- MFA is mandatory for all admin-level accounts
- Supported: TOTP apps (Google Authenticator, Authy), hardware security keys (YubiKey)
- Enable under **Account Settings > Security > MFA**
- Recovery codes are generated on setup — store them securely offline

---

## 2. Compute Services

### Virtual Machine (VM) Not Starting
1. Check VM status in **Console > Compute > Instances**
2. Review activity logs for error codes
3. Verify that vCPU and memory quotas have not been exceeded
4. Check if the boot disk has sufficient space (minimum 10% free)
5. If in STOPPED state, click **Start**; if in ERROR state, escalate to cloud support

### VM Performance Degradation
- Check CPU/memory utilization in **Monitoring > Metrics**
- Enable autoscaling if traffic spikes are the cause
- Upgrade machine type for persistent high utilization (stop VM first, resize, restart)
- Check for noisy-neighbor effects by reviewing hypervisor metrics
- Review running processes inside the VM via SSH

### SSH Access Issues
- **Permission denied**: Verify the correct SSH key is associated with the VM
- **Connection timeout**: Check firewall rules — port 22 must be open for your IP
- **Host key changed warning**: Remove old entry from `~/.ssh/known_hosts`
- For emergency access without SSH key: use the in-browser console in the cloud dashboard

---

## 3. Storage Services

### Object Storage (Blob/S3-Compatible)

**Bucket Creation**
- Navigate to **Storage > Buckets > Create Bucket**
- Select region closest to your users for lowest latency
- Set access control: Private, Public Read, or Custom ACL

**Upload/Download Issues**
- Max single file upload: 5 TB (use multipart upload for files > 100 MB)
- If upload fails midway, resume using multipart upload API
- For slow downloads, enable CDN on the bucket for geo-distributed caching

**Bucket Permissions**
- Bucket-level policies use JSON IAM syntax
- Pre-signed URLs allow temporary public access without changing bucket policy
- Enable versioning to protect against accidental deletion

### Block Storage (Persistent Disks)
- Attach/detach disks from **Console > Storage > Disks**
- Resize disks online (increase only; decrease requires backup and re-create)
- Snapshots can be scheduled automatically under **Storage > Snapshots > Schedule**

---

## 4. Networking

### Firewall Rule Configuration
- Navigate to **Networking > Firewall > Add Rule**
- Specify: direction (ingress/egress), protocol, port range, source/destination IP
- Common ports: 22 (SSH), 80 (HTTP), 443 (HTTPS), 3306 (MySQL), 5432 (PostgreSQL)
- Rules are evaluated in priority order (lower number = higher priority)

### Load Balancer Setup
1. Create a backend service and add VM instances or instance groups
2. Configure health checks (HTTP/HTTPS/TCP)
3. Create a frontend with a static IP and target the backend service
4. SSL certificates can be managed (Google-managed or custom) under **Load Balancer > Certificates**

### DNS Management
- Add/edit DNS records under **Networking > DNS > Zones**
- Supported record types: A, AAAA, CNAME, MX, TXT, NS
- TTL changes propagate within 5 minutes within the cloud DNS; global propagation up to 48 hours

---

## 5. Billing & Cost Management

### Understanding Your Bill
- Detailed invoice available under **Billing > Invoices**
- Costs broken down by: compute, storage, network egress, managed services
- Export billing data to BigQuery/Storage for custom analysis

### Cost Optimization Tips
- Use committed use discounts (1-year or 3-year) for predictable workloads
- Enable idle VM detection alerts under **Billing > Recommendations**
- Set budget alerts at 50%, 90%, and 100% of monthly budget
- Delete unused snapshots, disks, and static IPs — these incur charges even when idle

### Unexpected Charges
- Review **Billing > Cost Breakdown** filtered by service and date range
- Check for accidentally left-on resources (VMs, NAT gateways, premium network tiers)
- If charges appear fraudulent, immediately revoke all API keys and contact billing support
- Billing disputes must be raised within 60 days of the invoice date
