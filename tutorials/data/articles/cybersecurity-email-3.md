From: alex.kumar@threatintel.co
To: jack@nonagonlabs.com
Date: January 2, 2026 6:47 AM
Subject: FYI - IOCs from overnight analysis

Jack,

Quick share from overnight shift - we tracked some new infrastructure tied to a ransomware campaign. Don't have the full picture yet but here's what we've got so far.

## Indicators

**IPs:**
203.0.113.47
198.51.100.89
192.0.2.154

**Domains:**
maintenance-portal[.]tech
secure-backup[.]cloud

**Hashes:**
SHA256: 4e7d9f2a5b8c1f3e6d9a2c5f8b1e4d7a3c6f9b2e5d8a1c4f7b3e6d9a2c5f8b1e4
SHA256: 9a3f6d2e8b5c1f4e7d9a3c6f8b2e5d1a4c7f9b3e6d2a5c8f1b4e7d9a3c6f2e5d

**File paths seen:**
C:\Windows\System32\drivers\svchost.dll
C:\ProgramData\cache\winupdate.exe

**Registry:**
HKLM\Software\Microsoft\Windows\CurrentVersion\RunOnce\Update

## MITRE

T1566.001 - Spearphishing Attachment
T1204.002 - User Execution: Malicious File  
T1059.001 - PowerShell
T1003.001 - LSASS Memory
T1021.001 - Remote Desktop Protocol
T1486 - Data Encrypted for Impact
T1490 - Inhibit System Recovery

Still pulling together the full report but wanted to get these out to you now. Will send more details later today.

Alex

---
Alex Kumar | Night Shift Analyst
ThreatIntel.co