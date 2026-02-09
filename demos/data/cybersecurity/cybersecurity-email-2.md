From: mike.torres@cybersecops.net
To: jack@nonagonlabs.com
Date: Jan 2 2026 11:23pm
Subject: RE: RE: saw this new ransomware you should know about

hey jack

sorry for the late email but wanted to get this to you tonight since we just finished analyzing samples from 3 different incidents today and the pattern is pretty clear now. this group (we're calling them DarkNexus but they dont have a public name yet) is going after mid-market companies in manufacturing and logistics primarily.

saw about 80 confirmed hits since october, mostly in US (like 45 or so) rest spread across EU and some in asia. theyre not super sophisticated but theyre fast and they know what theyre doing.

ENTRY POINTS - mix of everything really
- spearphishing with macro docs (saw invoices, shipping documents, that kind of thing)
- compromised RMM tools from MSPs (this is the scary one, once theyre in an MSP they hit multiple clients)
- some exploitation of exposed remote desktop - looks like they scan for it then bruteforce or use leaked creds

once theyre in its pretty standard playbook: disable AV, dump creds, move laterally, find backups and kill them, then encrypt. usual time from entry to encryption is 36-48hrs based on what we've reconstructed from logs.

The ransomware itself uses AES256+RSA4096 so no breaking that. They're asking anywhere from 200k to 2mil depending on revenue/size. doing the double extortion thing with a leak site on tor.

IOCs we've collected so far:

IPs:
167.172.45.219
188.166.83.147  
142.93.201.88
104.131.62.155
these are all C2 servers we've seen actively used in last 2 weeks

domains:
update-manager[.]site
cloud-storage-sync[.]online  
system-update-api[.]net
(all registered late nov/early dec, all using namecheap)

File hashes:
SHA256: 7f8e3d9a2b5c1f4e6d8a3c7b9f2e5d1a4c8b6f3e9d2a5c7f1b4e8d6a3c9f2e5d1
SHA256: b3e8f1d4a7c2e9f5d1a8c4b7e3f9d2a6c5b8f1e4d7a3c9f2e5b8d1a4c7f3e9b2
SHA256: c9f2e5d8a1b4c7f3e6d9a2c5f8b1e4d7a3c6f9b2e5d8a1c4f7b3e6d9a2c5f8b1

Usual dropper location: C:\Users\Public\Documents\sysmon.exe (yes really, they name it sysmon)
also seen: C:\ProgramData\Windows\csrss.exe
scheduled task name: "WindowsUpdateCheck" or "SystemHealthMonitor"

registry keys for persistence:
HKLM\Software\Microsoft\Windows\CurrentVersion\Run\SecurityUpdate
HKCU\Software\Microsoft\Windows\CurrentVersion\Run\MSUpdate

Mutex: Global\{8F3E9D2A-5C1B-4F7E-9D3A-2C8B5F1E4D7A}

MITRE mappings (as best as we can tell):
T1566.001 - phishing attachments
T1059.003 - windows command shell / powershell
T1486 - data encrypted for impact
T1490 - inhibit system recovery (vssadmin delete shadows, wbadmin delete catalog, bcdedit set recoveryenabled no)
T1070.001 - clear windows event logs
T1003.001 - LSASS memory dumps for creds
T1021.001 - RDP for lateral movement
T1047 - WMI for execution
T1053.005 - scheduled tasks
T1562.001 - disable/modify security tools

CASE 1: midwest manufacturing company (name redacted but you can probably guess)
hit on Dec 15th, initial access via MSP compromise - attackers had access to their RMM console (Datto RMM i think). deployed ransomware to ~300 endpoints simultaneously.

they encrypted production systems AND backups (backups werent properly segregated). company shut down for 4 days, ended up paying $850k.

technical details from their incident:
- initial beacon: 167.172.45.219:443
- used mimikatz (standard version, no custom build)
- lateral movement via psexec and wmi
- data exfil before encrypt: ~800GB to 188.166.83.147:8443
- ransomware deployed via scheduled tasks all set to trigger at 2am
- ransom note filename: HOW_TO_DECRYPT.txt
- encrypted file extension: .dnx

Additional IOCs from this one:
- PowerShell script: C:\Windows\Temp\update.ps1 (does the actual encryption prep)
- Tool used: advanced_port_scanner.exe (for network recon)
- Created local admin account: "helpdsk" (yeah with typo)

CASE 2: logistics company in EU (netherlands i think?)
hit Dec 22nd, different entry - they got in via exposed RDP on a server (port 3389 open to internet, weak password).

Timeline we reconstructed:
Day 1 (Dec 22): initial access via RDP bruteforce, created backdoor account "admin2"
Day 2: reconnaissance, deployed cobalt strike beacon to 142.93.201.88:8080
Day 3: credential dumping, lateral movement to domain controller
Day 4: deployed ransomware, encrypted ~180 systems

They didnt pay, gang posted 120GB of shipping manifests and customer data on their leak site 5 days later. company is dealing with GDPR fines now on top of recovery costs.

IOCs:
- backdoor account: admin2 / Admin2@2024! (we found the password in cleared logs)
- cobalt strike config: 142.93.201.88:8080, /jquery/api.js URI
- batch file used for deployment: deploy.bat in C:\Windows\Temp\
- ransomware connects to: system-update-api[.]net for key exchange

Also found they used a tool called "ShareFinder.ps1" for finding network shares and "Invoke-TheHash" for pass-the-hash attacks.

CASE 3: got details on this one today actually - another manufacturing company in georgia USA
happened Jan 1st (yes new years day, these guys dont take breaks). entry via macro document sent to accounting department - "Invoice_Dec2025.xlsm"

victim opened it, enabled macros, boom. dropped first stage payload which downloaded second stage from cloud-storage-sync[.]online/files/update.exe

they moved FAST on this one - from initial infection to encryption was only 28 hours. our theory is they have automated tools now because that's faster than previous incidents.

encrypted 240 machines including ESXi hosts (yeah they got into the virtualization layer). ransom demand was $1.1M. status: ongoing, company hasnt decided whether to pay yet.

IOCs from this one:
- initial doc hash: SHA256: 3a7f9e2d5c8b1f4e6a9d3c7b2f5e8d1a4c9b6f3e2d5a8c1f4b7e9d6a3c2f5b8e1
- C2 for first stage: 104.131.62.155:443
- downloaded payload URL: hxxps://cloud-storage-sync[.]online/files/update.exe
- payload hash: SHA256: 7f8e3d9a2b5c1f4e6d8a3c7b9f2e5d1a4c8b6f3e9d2a5c7f1b4e8d6a3c9f2e5d1
- ESXi encryption: they used a linux variant, different hash
- lateral movement: mix of RDP and SMB with stolen domain admin creds

Also worth noting - they installed anydesk for remote access as backup: installer at C:\Users\Public\AnyDesk.exe, custom anydesk ID in logs was 987654321 (probably not useful but documenting it)

RECOMMENDATIONS (you probably already do this but just in case):

immediate stuff:
- block those IPs at firewall
- scan for those hashes
- check for any accounts named helpdsk, admin2, or other suspicious admin accounts created recently
- look for scheduled tasks with those names i mentioned
- check for anydesk or other remote access tools you didnt install

short term:
- disable macros by default if you havent (GPO policy)
- MFA on EVERYTHING especially RDP and VPN
- segment your network, put backups on isolated network
- make sure EDR cant be disabled without special auth
- review all your MSP/vendor access

longer term:
- proper backup strategy (3-2-1 rule, test restores)
- network segmentation especially for OT/production systems
- application whitelisting on critical systems
- regular vuln scanning
- incident response plan and TEST IT

I can send you some YARA rules we wrote for detection if you want them. also have some sigma rules for the scheduled task creation patterns and the specific powershell commands they use.

Let me know if you need anything else or want to discuss. I know this email is a mess but wanted to get the info to you quick.

-mike

--
Mike Torres
Incident Response Lead
CyberSecOps  
m.torres@cybersecops.net

ps - if you see any of this in your environment CALL ME immediately dont wait, this group moves fast once they decide to hit the encrypt button. cell is 415-555-0891