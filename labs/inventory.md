> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Lab Inventory

Use this file to track intentionally vulnerable or self-owned systems. Do not list third-party production systems here unless they are part of a written authorized engagement.

| Name | Type | Address | Credentials | Purpose | Reset Steps | Status |
| --- | --- | --- | --- | --- | --- | --- |
| Juice Shop local | Web lab | `http://127.0.0.1:3000` | Local lab account only | Web vulnerability practice | Restart container or app | Planned |
| DVWA local | Web lab | `http://127.0.0.1:8080` | Local lab account only | Web basics and manual verification | Reset database | Planned |

## Lab Rules

- Keep labs isolated from personal and production systems.
- Snapshot virtual machines before risky experiments.
- Store only disposable credentials.
- Record what was tested, what changed, and how to reset it.

