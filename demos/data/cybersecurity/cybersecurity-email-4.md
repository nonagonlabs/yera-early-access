From: jessica.park@cyberdefense.io
To: jack@nonagonlabs.com
Date: January 2, 2026 2:14 PM
Subject: APT activity - financial sector targeting

Jack-

Seeing coordinated scanning activity against fintech companies last 48hrs. Looks like APT but attribution still unclear.

**C2 Infrastructure:**
45.142.212.88
103.89.91.203
176.123.8.156

**Domains:**
api-gateway-cdn[.]net
payment-processor-test[.]com
fintech-validation[.]org

**Observed Malware:**
SHA256: d8e2f5a9c3b7f1e4d6a8c2f9b5e1d7a4c3f8b6e2a5d9c1f7b4e8d3a6c2f5b9e1
SHA256: 2a5c8f1e4d7b9a3c6f2e5d8a1c4f7b3e6d9a2c5f8b1e4d7a3c6f9b2e5d8a1c4f

**TTPs:**
T1190 - Exploit Public-Facing Application
T1133 - External Remote Services  
T1078 - Valid Accounts
T1071.001 - Web Protocols
T1027 - Obfuscated Files or Information
T1057 - Process Discovery
T1083 - File and Directory Discovery
T1005 - Data from Local System

**Artifacts:**
- Web shells at: /api/v2/auth/callback.php
- Persistence via cron: /etc/cron.d/system-update
- Drops: /tmp/.system/cache/update

More analysis ongoing - will update.

Jess

--
Jessica Park
Threat Hunter
CyberDefense.io