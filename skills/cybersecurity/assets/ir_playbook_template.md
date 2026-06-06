> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Incident Response Case File

Copy this template at incident T+0. Fill as you go. All timestamps in UTC.

---

## 1. Metadata

- **Case ID**:
- **Severity**: P1 (critical) / P2 (high) / P3 (medium) / P4 (low)
- **Status**: Active / Contained / Eradicated / Recovered / Closed
- **Detected at (UTC)**:
- **Reported by**:
- **IR Commander**:
- **Affected systems / accounts / data**:
- **Suspected initial access vector**:
- **Suspected MITRE ATT&CK techniques**:

## 2. Timeline (UTC)

| Time (UTC) | Actor | Action | Source |
|------------|-------|--------|--------|
| | | | |

> Add a row for every meaningful event: detection, decisions made, containment actions, evidence collection, communications. Don't fill in retroactively — log as you go.

## 3. Triage notes

### What we know
- 

### What we don't know yet
- 

### Working hypotheses (mark which is most likely)
1. 

### Excluded hypotheses (with reasoning)
- 

## 4. Containment actions taken

| Time (UTC) | Action | Authorized by | Result |
|------------|--------|---------------|--------|
| | | | |

## 5. Evidence collected

| ID | Description | Source host / system | Collected by | Time (UTC) | SHA256 | Storage location |
|----|-------------|----------------------|--------------|------------|--------|------------------|
| E-001 | | | | | | |

> Hash every artefact file at collection. Verify hash on every transfer. Keep originals read-only.

## 6. Indicators of Compromise (IOCs)

### File hashes (SHA256)
- 

### IPs (with role: C2, exfil, scanner, etc.)
- 

### Domains
- 

### Accounts / users
- 

### Persistence mechanisms found
- 

## 7. Affected data

- **Data type**: PII / PHI / PCI / IP / credentials / config / unknown
- **Volume estimate**:
- **Confirmed exfiltrated?** Yes / No / Unknown
- **Regulatory implications** (GDPR, HIPAA, PCI-DSS, SOC 2, local law):

## 8. Communications log

| Time (UTC) | Audience | Channel | Sender | Summary | Reviewed by |
|------------|----------|---------|--------|---------|-------------|
| | | | | | |

> Every external comms goes through legal first.

## 9. Eradication actions

- [ ] All malicious files removed (hash list verified)
- [ ] All persistence mechanisms removed
- [ ] All compromised credentials rotated
- [ ] Affected systems rebuilt from known-good state
- [ ] Patches applied for entry-vector vulnerability
- [ ] Detection rules added to prevent recurrence

## 10. Recovery checklist

- [ ] Production traffic restored
- [ ] Heightened monitoring enabled (≥ 30 days)
- [ ] Backup integrity verified
- [ ] Credentials rotated for any service that was on the affected segment
- [ ] Customer-facing comms sent (if applicable)
- [ ] Regulator notification filed (if applicable, within deadline)

## 11. Lessons learned (post-mortem)

> Schedule within 2 weeks of recovery. No blame. Focus: how do we make this NOT happen again, or detect it faster if it does?

### What happened
- 

### Why was it possible
- 

### Why didn't we catch it sooner
- 

### Action items (each with owner + deadline)

| # | Item | Owner | Deadline |
|---|------|-------|----------|
| 1 | | | |

### Process / tooling improvements to make
- 

### Training needs identified
- 

## 12. Closure

- **Closed at (UTC)**:
- **Total time to detect (T_d)**:
- **Total time to contain (T_c)**:
- **Total time to recover (T_r)**:
- **Final classification**:
- **External report filed**: Yes / No (where, when)
- **Insurance claim filed**: Yes / No
- **Sign-off**:
