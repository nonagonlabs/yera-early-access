From: chen.liu@infosec-watch.com
To: jack@nonagonlabs.com  
Date: January 2, 2026 4:38 PM
Subject: Web app exploitation - CVE-2024-XXXX active exploitation

Jack,

Active exploitation of unpatched web apps - seeing mass scanning + exploitation attempts.

CVE: CVE-2024-45789 (SQL injection in popular CMS plugin)

**Attacker IPs (last 24h):**
159.203.45.187
167.99.218.72
134.209.156.41
188.166.91.203

**User-Agents:**
Mozilla/5.0 (compatible; Scanner/1.0)
python-requests/2.28.1
sqlmap/1.7.2

**Web shells deployed:**
/wp-content/plugins/cache/api.php
/admin/includes/class.upload.php  
/assets/js/jquery.min.php
/uploads/images/shell.php

**Sample payloads (URL encoded):**
' OR '1'='1
'; DROP TABLE users--
' UNION SELECT NULL,NULL,username,password FROM admin_users--

**Shell hashes:**
SHA256: 6e8d2f5a9c3b7f1e4d6a8c2f9b5e1d7a4c3f8b6e2a5d9c1f7b4e8d3a6c2f5b9e1
SHA256: a4c7f3e6b9d2a5c8f1e4b7d9a3c6f2e5b8d1a4c7f3e6b9d2a5c8f1e4b7d9a3c6

**Post-exploitation activity:**
T1190 - Exploit Public-Facing Application
T1505.003 - Web Shell
T1136.001 - Create Account: Local Account
T1078.003 - Valid Accounts: Local Accounts
T1018 - Remote System Discovery
T1082 - System Information Discovery

**Created accounts:**
admin2
webmaster
support

Check your web apps ASAP - patch available from vendor as of yesterday.

Chen

---
Chen Liu | Threat Intelligence
InfoSec-Watch.com | chen.liu@infosec-watch.com