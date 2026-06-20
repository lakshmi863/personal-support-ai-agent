# IT Helpdesk Knowledge Base

## 1. Hardware Issues

### Computer Not Turning On
1. Check that the power cable is securely connected
2. Verify the power outlet is working (test with another device)
3. For laptops: hold the power button for 10 seconds, then press again
4. Remove external devices (USB drives, monitors) and try again
5. If the power LED doesn't light up at all, escalate to Level 2 hardware support

### Monitor Display Issues
- **No signal**: Check HDMI/DisplayPort/VGA cable connections at both ends
- **Flickering screen**: Update graphics drivers via Device Manager
- **Blurry display**: Right-click Desktop > Display Settings > Adjust Resolution to recommended
- **Dual monitor not detected**: Right-click Desktop > Display Settings > Detect

### Keyboard/Mouse Not Working
1. Unplug and reconnect the USB device
2. Try a different USB port
3. For wireless: replace batteries or re-pair the device
4. Check Device Manager for driver errors (yellow exclamation mark)
5. Test the device on another computer to isolate the issue

---

## 2. Software & OS Issues

### Windows Update Failures
- Error 0x80070002: Run Windows Update Troubleshooter from Settings > Update & Security
- Error 0x800705b4: Temporarily disable antivirus and retry
- Stuck at 0%: Restart Windows Update service via services.msc
- If updates keep failing, use the Windows Update Assistant tool from Microsoft's website

### Application Crashes
1. Check Event Viewer (eventvwr.msc) for error logs under Windows Logs > Application
2. Repair the application via Control Panel > Programs > Repair
3. Uninstall and reinstall the application
4. Ensure .NET Framework and Visual C++ Redistributables are up to date
5. Check for application-specific patch notes or known issues on the vendor's site

### Slow Computer Performance
- Check CPU/RAM usage in Task Manager (Ctrl+Shift+Esc)
- Disable startup programs: Task Manager > Startup tab
- Run Disk Cleanup: search "Disk Cleanup" in Start menu
- Check for malware using Windows Defender full scan
- Consider upgrading RAM if consistently above 85% usage

---

## 3. Network & Connectivity

### No Internet Connection
1. Restart router and modem (unplug for 30 seconds)
2. Run Windows Network Troubleshooter: Settings > Network > Troubleshoot
3. Release and renew IP: open CMD as Admin, type `ipconfig /release` then `ipconfig /renew`
4. Flush DNS: type `ipconfig /flushdns` in CMD
5. Check if other devices on the same network are affected

### VPN Connection Issues
- **Cannot connect**: Verify VPN credentials and server address
- **Connected but no access**: Check split tunneling settings; ensure VPN routes internal traffic
- **Slow VPN**: Switch to a closer server endpoint; check bandwidth on local network
- **Certificate errors**: Re-import the VPN certificate from IT portal
- Always use the company-approved VPN client (GlobalProtect / Cisco AnyConnect)

### Shared Drive / Network Folder Access
- Map network drive: File Explorer > This PC > Map Network Drive > Enter UNC path (\\server\share)
- If access denied: contact IT to verify your Active Directory group permissions
- Disconnected drives: right-click the drive > Disconnect, then re-map
- For remote access to shared drives, ensure VPN is connected first

---

## 4. Email & Communication Tools

### Outlook Not Receiving Emails
1. Check internet connectivity
2. Verify account settings: File > Account Settings > Repair
3. Check if emails are going to Junk/Clutter folder
4. Disable add-ins: File > Options > Add-ins > Manage COM Add-ins
5. Recreate the Outlook profile if issue persists: Control Panel > Mail > Show Profiles

### Microsoft Teams Issues
- **Cannot join meetings**: Update Teams to latest version; clear cache (%appdata%\Microsoft\Teams)
- **Audio/video not working**: Check default devices in Settings > Devices
- **Cannot send messages**: Check network firewall — Teams requires port 443 (TCP)
- **Status stuck on Away**: Go to profile picture > Set Status > Available

---

## 5. Security & Access

### Password Reset (Active Directory)
- Self-service: visit resetpassword.company.com and verify identity via registered mobile/email
- IT-assisted reset: raise a ticket with employee ID; IT will reset after identity verification
- New password requirements: minimum 12 characters, uppercase, lowercase, number, special character
- Password expiry: every 90 days; reminder sent 14 days before expiry

### Locked Account
- Accounts are locked after 5 consecutive failed login attempts
- Auto-unlock after 30 minutes, or contact IT for immediate unlock
- Provide employee ID and manager's email for verification

### Software Installation Requests
- Submit a request via the IT Service Portal: portal.company.com
- Approval from line manager required for non-standard software
- Standard software (Office, Chrome, Zoom) auto-deployed within 2 hours
- Non-standard software reviewed within 2 business days
