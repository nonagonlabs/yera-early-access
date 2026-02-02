From: marcus.wong@securityops.net
To: jack@nonagonlabs.com
Date: January 1, 2026 11:52 PM  
Subject: re: info stealer hitting SaaS companies

hey just got off incident call - info stealer campaign targeting saas/cloud companies. sharing what we have:

IPs we're tracking:
- 185.220.101.38
- 194.36.191.227
- 91.219.237.44
- 162.247.74.199

C2 callback domains:
stats-collector[.]xyz
analytics-cdn[.]live  
metrics-api[.]space

samples:
SHA256: 5c9f3e7a2d8b1f6e4a9c3d7f2e5b8a1d6c4f9e3b7a2d5c8f1e4b9d6a3c7f2e5b
SHA256: 8f2e5d1a4c7b9e3f6d2a5c8f1b4e7d9a3c6f2e5b8d1a4c7f3e6b9d2a5c8f1e4d
SHA256: 1d6a3c9f2e5b8a4d7c1f9e6b3a5d8c2f7e4b9d1a6c3f8e2b5d9a7c4f1e3b6d8a

MITRE:
T1566.002 - Spearphishing Link
T1204.001 - Malicious Link
T1112 - Modify Registry  
T1555.003 - Credentials from Web Browsers
T1552.001 - Credentials In Files
T1113 - Screen Capture
T1115 - Clipboard Data
T1041 - Exfiltration Over C2 Channel

files dropped:
C:\Users\<user>\AppData\Roaming\Microsoft\Credentials\cred_store.db
C:\Users\<user>\AppData\Local\Temp\chrome_data.tmp

targeting browser credential stores (Chrome, Firefox, Edge) + discord tokens + crypto wallets

more soon

-M

Marcus Wong | SOC Lead
marcus.wong@securityops.net