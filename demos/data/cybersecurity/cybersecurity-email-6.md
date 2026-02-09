From: raj.patel@threatalert.com
To: jack@nonagonlabs.com
Date: January 2, 2026 9:03 AM
Subject: Cryptominer spreading via npm packages

Quick alert - cryptominer in supply chain attack via compromised npm packages.

**Malicious packages (now removed):**
- node-crypto-helper v2.4.1
- express-jwt-validator v1.8.3

**Mining pool connections:**
pool.minexmr[.]com:4444
xmr-eu1.nanopool[.]org:14444

**Hashes:**
SHA256: f7d3a9e2c5b8f1d4e7a3c9b6f2e8d1a5c4b9f7e2d6a8c3f1b5e9d4a7c2f6b8e1
SHA256: 3b8f1e6d9a2c5f8b1e4d7a3c6f9b2e5d8a1c4f7b3e6d9a2c5f8b1e4d7a3c6f9b

**MITRE:**
T1195.002 - Compromise Software Supply Chain
T1496 - Resource Hijacking
T1027.002 - Obfuscated Files: Software Packing

**Process names:**
node --max-old-space-size=8192 .cache/build
kworker

Block those pools at firewall and check for unusual CPU usage.

Raj

---
Raj Patel
ThreatAlert.com