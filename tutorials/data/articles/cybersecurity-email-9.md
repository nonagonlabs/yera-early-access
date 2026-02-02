From: emma.rodriguez@phishwatch.io
To: jack@nonagonlabs.com
Date: January 1, 2026 7:21 PM
Subject: phishing campaign - executive impersonation

jack -

BEC campaign going around targeting finance/accounting teams. impersonating executives requesting wire transfers.

**Phishing infrastructure:**

Sender domains:
nonagon-labs[.]co (note the hyphen - not your real domain)
nonagonlabs[.]net
secure-nonagon[.]com

Sending IPs:
45.79.143.26
198.199.88.154
104.236.47.89

**Landing pages:**
hxxps://login-verify[.]digital/auth
hxxps://account-secure[.]online/verify
hxxps://office365-auth[.]site/login

**Credential harvester hashes:**
SHA256: 9e2d5f8a1c4b7f3e6d9a2c5f8b1e4d7a3c6f9b2e5d8a1c4f7b3e6d9a2c5f8b1e
SHA256: c5f8b2e9d1a4c7f3e6b9d2a5c8f1e4b7d9a3c6f2e5b8d1a4c7f3e6b9d2a5c8f1

**Email characteristics:**
- Subject lines: "Urgent: Wire Transfer Required", "RE: Payment Authorization Needed"
- Spoofed display names matching your executives
- Urgency language: "need this today", "time sensitive", "confidential"
- Request to use "new payment portal" or "verify account details"

techniques observed:
T1566.002 - Phishing: Spearphishing Link
T1598.003 - Phishing for Information: Spearphishing Link
T1539 - Steal Web Session Cookie
T1056.003 - Input Capture: Web Portal Capture
T1114.002 - Email Collection: Remote Email Collection

also deploying infostealer if user downloads "invoice.pdf.exe":
C:\Users\<user>\Downloads\invoice.pdf.exe
C:\Users\<user>\AppData\Local\Temp\setup_installer.exe

SHA256: 7a3c9f2e5b8d1a4c7f3e6b9d2a5c8f1e4b7d9a3c6f2e5b8d1a4c7f3e6b9d2a5c

warn your finance team

emma

Emma Rodriguez  
PhishWatch.io