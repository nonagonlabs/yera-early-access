**From:** Sarah Chen <sarah.chen@threatsentry.io>  
**To:** Jack Morrison <jack@nonagonlabs.com>  
**CC:** Security Team  
**Date:** January 2, 2026, 3:47 PM  
**Subject:** Heads up - new ransomware gang hitting healthcare/fintech hard

Hey Jack,

Hope you had a good holiday! Quick heads up on something we've been tracking that I thought you should know about ASAP.

We've seen a new ransomware operation (calling themselves "ShadowVault") that's been absolutely hammering healthcare and financial services companies since mid-November. They're pretty sophisticated and seem to have their shit together unfortunately. We've confirmed about 150+ victims so far across US, UK, Canada, and Australia.

## What we're seeing

The initial access is usually through compromised VPN credentials - looks like they're buying them from initial access brokers. Once they're in, they're moving fast:

- Dump credentials with standard tools (Mimikatz, nothing fancy)
- Lateral movement via RDP and SMB
- Deploy Cobalt Strike beacons for C2
- Exfiltrate data to their servers before encrypting
- Hit the encrypt button usually within 48-72 hours of initial access

The encryption is solid (ChaCha20 with RSA-2048 for key protection), and they're doing the whole double extortion thing - threatening to publish stolen data if ransom isn't paid. Ransom demands we've seen range from $500K to $3M depending on company size.

## Technical stuff you should check for

Here are some IOCs we've pulled from recent incidents:

**Known C2 infrastructure:**
- 45.87.154.23
- 198.211.117.89
- 104.168.195.47
- suspicious-update[.]xyz
- cloud-backup-service[.]net

**Malware hashes:**
- SHA256: a4b2c8d9e1f3a7b5c2d8e4f1a9b7c3d5e2f8a4b9c7d3e1f5a8b4c2d9e7f3a1b5c8
- SHA256: f3e7d9a2c5b8f1d4e7a3c9b5f2e8d1a6c4b9f7e2d5a8c3f1b6e9d4a7c2f5b8e1

**File artifacts:**
- C:\ProgramData\SystemCache\svcupdate.exe
- C:\Windows\Temp\msu.tmp (drops main payload)
- Ransom note: README_TO_DECRYPT.txt

**Registry persistence:**
- HKCU\Software\Microsoft\Windows\CurrentVersion\Run\WindowsDefenderUpdate

They also create a mutex: Global\SV_2024_MTX

## MITRE stuff (if you care)

For your threat modeling:
- T1078 (Valid Accounts) - compromised VPN creds
- T1021.001 (RDP) - lateral movement
- T1003.001 (LSASS dump) - credential theft
- T1219 (Remote Access Software) - Cobalt Strike
- T1567.002 (Exfiltration to Cloud) - stealing data before encrypt
- T1486 (Data Encrypted for Impact) - the main event
- T1491.001 (Defacement: Internal) - ransom notes everywhere

## What happened at MedCorp Systems (UK)

One case that really sucked - mid-sized healthcare provider in Manchester got hit on Dec 18th. Attackers got in through a contractor's VPN account (no MFA, ugh). They spent 3 days mapping the network, grabbed about 2TB of patient records, then encrypted everything including their backup systems.

The attackers knew exactly what they were doing - they disabled their EDR before deploying the ransomware across 400+ machines simultaneously using scheduled tasks. Company ended up paying $1.2M to get the decryption keys because they couldn't operate without the systems. Really brutal.

**IOCs from that incident specifically:**
- Initial access: 45.87.154.23:443
- Cobalt Strike beacon: 198.211.117.89:8080
- Exfil server: cloud-backup-service[.]net
- Dropped tool: ntdsutil.exe (credential dumping)

## Another one - TechFinance Solutions (Canada)

Fintech company in Toronto got hit Dec 28th. Similar playbook but they used a different entry point - exploited an unpatched Fortinet VPN (CVE-2023-27997). Once inside:

1. Deployed web shell at /remote/login?lang=../../../../../../../bin/sh
2. Created local admin account "support_admin"
3. Used PsExec to spread laterally
4. Grabbed trading algorithms and customer financial data (~500GB)
5. Encrypted file servers and databases

They didn't pay and the attackers dumped 50GB of their data on a leak site as "proof" they weren't bluffing. Company's currently dealing with regulatory fallout and potential lawsuits.

**More IOCs:**
- Web shell path: /remote/login?lang=../../../../../../../bin/sh
- Malicious account: support_admin
- Additional C2: 104.168.195.47:443
- Mutex variant: Global\SV_2024_FIN_MTX

## What you should do

Not trying to be alarmist but this group is active RIGHT NOW. Here's what I'd recommend:

**This week:**
1. Make sure all VPN access has MFA - seriously, this is their #1 entry point
2. Patch that Fortinet vuln if you have their VPNs (CVE-2023-27997)
3. Check your logs for any connections to those IPs above
4. Make sure your backups are offline/immutable and actually test them
5. Verify your EDR can't be disabled without proper auth

**Longer term:**
- Segment your network so lateral movement isn't trivial
- Monitor for Cobalt Strike beacons (lots of good YARA rules out there)
- Consider implementing application whitelisting on critical systems
- Review who has RDP access and whether they really need it

## Resources

I'm attaching our full threat brief if you want more details. We've also got some YARA rules and Sigma detection rules that might help - let me know if you want them.

Also, there's a good write-up on this group from the folks at CyberReason if you google "ShadowVault ransomware analysis" - they found some interesting TTPs we haven't seen yet.

Happy to jump on a call if you want to walk through any of this or need help checking your environment. We've got some scripts that can scan for these IOCs if that's useful.

Stay safe out there,
Sarah

---

**Sarah Chen**  
Senior Threat Intelligence Analyst  
ThreatSentry | Cyber Threat Intelligence  
sarah.chen@threatsentry.io | +1 (415) 555-0147

*P.S. - Saw your post about Yera on X, looks really interesting! Would love to chat about use cases in threat intel sometime.*