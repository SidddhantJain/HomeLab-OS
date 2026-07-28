1. Security Objective

HomeLab OS manages:

Personal data
Development projects
Credentials
Private documents
Server infrastructure

The primary security goals are:

Goal	Description
Confidentiality	Prevent unauthorized access
Integrity	Prevent data modification
Availability	Keep services running
Accountability	Track important actions
2. Threat Actors
T1: Physical Attacker

Scenario:

Laptop or external HDD stolen.

Threat:

Access personal files.
Access projects.
Extract credentials.

Protection:

✔ Full disk encryption (optional)
✔ Vault encryption
✔ Strong user password
✔ Auto-lock vault
✔ No stored plaintext credentials
T2: Local Network Attacker

Scenario:

Someone connects to your WiFi.

Threat:

Access open services.
Scan ports.
Attempt login.

Protection:

✔ Firewall
✔ Service authentication
✔ Network isolation
✔ No exposed services by default
✔ VPN for remote access
T3: Malicious Software

Scenario:

A compromised application/container.

Threat:

Access files.
Modify data.
Steal secrets.

Protection:

✔ Docker isolation
✔ Separate service users
✔ Read-only mounts where possible
✔ Permission control
✔ Container resource limits
T4: User Mistake

Scenario:

Accidental deletion.

Threat:

Project loss.
Configuration loss.

Protection:

✔ Git
✔ Snapshots
✔ File versioning
✔ Backups
✔ Recycle bin
T5: Hardware Failure

Scenario:

SSD/HDD failure.

Threat:

Data loss.

Protection:

✔ SMART monitoring
✔ Backup system
✔ Snapshot system
✔ Drive health alerts
T6: Remote Attack

Scenario:

Server exposed through internet.

Threat:

Brute force.
Exploitation.
Malware.

Protection:

Default:

Internet
   |
   X
(No direct access)

Remote access:

Internet

↓

VPN

↓

HomeLab OS

Technologies:

WireGuard
Tailscale (optional)
3. Security Architecture
                 User Device

                     |
                     |
                Authentication

                     |
                     |
              HomeLab OS API

                     |
        ┌────────────┼────────────┐
        |            |            |
    Storage       Docker       Vault
        |            |            |
    Permissions   Isolation   Encryption
4. Authentication Model
Password Requirements

Minimum:

12 characters
Mixed case
Numbers
Symbols
Future:

Multi-factor authentication:

Options:

TOTP authenticator
Hardware key
Mobile approval
5. Vault Security Design

The vault is the highest-security component.

Architecture:

Encrypted Container

        |
        |
 Password Key

        |
        |
 Mounted temporarily

        |
        |
 User Access

Rules:

Never automatically unlock.
Never expose through Samba while locked.
Log every unlock attempt.
Auto-lock option.
6. Secrets Management

No passwords inside:

docker-compose.yml

Instead:

secrets/

├── database_password
├── api_keys
└── tokens

Permissions:

chmod 600
7. Audit Logging

Track:

Login attempts

Vault unlock

Vault lock

User creation

Service start/stop

Backup actions

Configuration changes

Example:

2026-07-28 09:30

admin unlocked vault

Device:
Windows-Laptop

IP:
192.168.1.20
8. Backup Security

Backup rule:

Never keep:

Original
+
Backup

in same physical location

Future:

HomeLab HDD

        |

Second HDD

        |

Cloud/Offline backup
9. Security Levels

HomeLab OS will support profiles.

Level 1: Normal

For daily use.

Password
Firewall
Vault
Backups
Level 2: Secure
SSH Keys
2FA
VPN
Encrypted backups
Level 3: Maximum
Offline vault
Hardware key
Encrypted full disk
Audit monitoring
