> Public sanitized edition: sensitive personal, target, path, IP, alias, advisory, and run-specific evidence fields are redacted. This repository does not authorize live testing.

# Cloud Security Reference

Read when AWS / Azure / GCP / Kubernetes / serverless / cloud-native security comes up — both offence and defence.

## Table of contents
1. Cloud security mental model
2. AWS — IAM, S3, EC2 metadata, common attack paths
3. Azure / Entra ID — Conditional Access, Managed Identities, common attacks
4. GCP — IAM, service accounts, common attacks
5. Kubernetes — RBAC, pod security, common attacks
6. Cross-cloud common misconfigurations
7. Audit / pentest tools
8. Defence — logging, alerting, hardening baselines
9. Cloud Incident Response specifics

---

## 1. Mental model

Cloud security is **mostly identity, then network, then storage**. The bug class differs from on-prem:

| On-prem-style bug | Cloud equivalent |
|---|---|
| Buffer overflow in service | Misconfigured IAM policy |
| Privilege escalation via SUID | `iam:PassRole` to a higher-privileged role |
| Credential reuse | Long-lived access keys committed to GitHub |
| Lateral movement via SMB | Lateral movement via instance role + STS |
| Kernel exploit | Container escape / privileged pod |

> "The shared responsibility model" = the customer is responsible for ~85% of breaches in cloud.

---

## 2. AWS

### Core services to know
- **IAM** — users, groups, roles, policies (Identity-based + Resource-based + Permissions Boundaries + SCPs).
- **STS** — short-lived credentials via `AssumeRole`.
- **S3** — public ACLs, bucket policies, presigned URLs.
- **EC2** — instance metadata service (IMDS).
- **CloudTrail** — control-plane audit.
- **VPC Flow Logs** — network-plane visibility.
- **GuardDuty** — managed threat detection.

### Common attack paths

#### Path A — Leaked access key on GitHub
1. Trufflehog / Gitleaks finds `AKIA...` in commit history.
2. `aws sts get-caller-identity` to identify role.
3. `aws iam list-attached-user-policies` to enumerate permissions.
4. Pivot via `iam:PassRole` to any role the user can pass.

Defence: secrets-scanning in CI; AWS Access Analyzer; rotate immediately on exposure (it's already too late but patch the bleeding).

#### Path B — IMDSv1 SSRF
- Vulnerable web app SSRF → `curl http://169.254.169.254/latest/meta-data/iam/security-credentials/<role>`.
- Get temporary credentials of the EC2 instance role.
- Pivot to S3, Secrets Manager, etc.

Defence: **enforce IMDSv2** (token-based, defeats SSRF). On every EC2: `aws ec2 modify-instance-metadata-options --http-tokens required --http-endpoint enabled`.

#### Path C — S3 bucket misconfiguration
- Public-read ACL or bucket policy → unauthenticated GetObject.
- Public-write → defacement, malware hosting, log poisoning.
- ListBucket → enumerate everything.

Defence: S3 Block Public Access at account level; Bucket Policy denying `principal: "*"`; default encryption + KMS; access logs to a separate account.

#### Path D — `iam:PassRole` privilege escalation
- User has `iam:PassRole` + `lambda:CreateFunction` + `lambda:InvokeFunction`.
- Pass an admin role to a Lambda → invoke → run `iam:CreateAccessKey` for the root account.

Defence: Permissions Boundaries on every user/role; `iam:PassRole` scoped with `iam:PassedToService` condition; Access Analyzer findings on overly permissive trust policies.

#### Path E — Cross-account role assumption
- Trust policy allows `arn:aws:iam::*:root` (everyone) or external account without ExternalID.
- Attacker `AssumeRole` from their account → pivot in.

Defence: tighten trust policies; enforce `ExternalId` for third-party integrations; scan for `Effect: Allow Principal: "*"` in trust documents.

### Useful commands

```bash
# Enumerate via assumed role
aws sts get-caller-identity
aws iam list-attached-user-policies --user-name $USER
aws iam simulate-principal-policy --policy-source-arn $ARN --action-names "*"

# Walk every region (services are regional)
for r in $(aws ec2 describe-regions --query 'Regions[].RegionName' --output text); do
  aws ec2 describe-instances --region $r --query 'Reservations[].Instances[?State.Name==`running`].[InstanceId,InstanceType,PublicIpAddress]'
done

# S3 enum
aws s3api list-buckets
aws s3 ls s3://bucket-name --recursive --human-readable
```

### Audit tools
- **Prowler** — comprehensive AWS audit; CIS / SOC2 / GDPR profiles.
- **ScoutSuite** — multi-cloud, generates HTML report.
- **Pacu** — AWS exploitation framework (think Metasploit for AWS).
- **CloudSploit** / **Steampipe** — query cloud config like SQL.
- **Stratus Red Team** — adversary emulation.

---

## 3. Azure / Entra ID

### Core services
- **Microsoft Entra ID** (formerly Azure AD) — identity provider.
- **Conditional Access** — policies on who can sign in from where.
- **Managed Identities** — Azure-native short-lived tokens for compute.
- **Activity Log** — control-plane audit; Sign-in Logs separately.
- **Defender for Cloud** — recommendations + alerting.
- **Sentinel** — SIEM.

### Common attack paths

#### Path A — Token theft / device code phishing
- Phishing redirects user to legit Microsoft device-code flow.
- Attacker gets the access + refresh tokens.
- Refresh token → mailbox, SharePoint, OneDrive access.

Defence: Conditional Access blocking device-code from untrusted networks; phishing-resistant MFA (FIDO2 / Windows Hello); short-lived access token lifetimes.

#### Path B — Service Principal abuse
- App registration with `Application.ReadWrite.All` Graph permission.
- Attacker who controls it can grant itself any other permission via Graph.

Defence: review consented app permissions monthly; limit who can register apps; monitor `Application.ReadWrite.All`, `RoleManagement.ReadWrite.Directory`, `AppRoleAssignment.ReadWrite.All`.

#### Path C — Synced AD compromise → Cloud
- On-prem AD compromise + AD Connect → password hashes / tickets sync to cloud.
- DA on-prem usually = Global Admin equivalence in cloud.

Defence: cloud-only Global Admins (no on-prem sync); separate admin tier for cloud.

#### Path D — Hybrid Worker / Automation Account
- Compromised hybrid worker can access Azure resources via the automation account's identity.
- Often over-privileged.

Defence: scope automation account RBAC tightly; review runbooks for hardcoded creds.

### Useful commands

```bash
# AzureCLI
az login
az account list
az role assignment list --all
az ad sp list --filter "appOwnerOrganizationId eq '<tenant>'" --query "[].{displayName:displayName, appId:appId}"

# AzureAD module (PowerShell)
Connect-AzureAD
Get-AzureADUser -Top 50
Get-AzureADDirectoryRole | ForEach-Object { Get-AzureADDirectoryRoleMember -ObjectId $_.ObjectId }
```

### Audit / red-team tools
- **ROADtools** — comprehensive Entra ID enumeration + analysis (must-have).
- **AADInternals** — Azure AD red-team toolkit.
- **MicroBurst** — Azure misconfiguration finder.
- **Stormspotter** — graph view of Azure resources (Azure equiv of BloodHound).
- **Prowler** — supports Azure too now.

---

## 4. GCP

### Core services
- **IAM** — primitive (Owner/Editor/Viewer), predefined, custom roles.
- **Service Accounts** — non-human identities; can be impersonated by humans.
- **Workload Identity** — GKE pod → GCP service account binding.
- **Cloud Audit Logs** — Admin Activity (always on) + Data Access (off by default).
- **Security Command Center** — central security view.

### Common attack paths

#### Path A — Service account key leak
- JSON key committed to GitHub.
- Attacker uses `gcloud auth activate-service-account --key-file=key.json`.
- Pivot using whatever the SA can do.

Defence: don't create user-managed SA keys (use Workload Identity); if you must, rotate every 90 days; scan for `"type": "service_account"` patterns in repos.

#### Path B — `iam.serviceAccounts.actAs` privesc
- User has `actAs` on a high-privileged SA + `compute.instances.create`.
- Create a VM running as the SA → SSH in → use the SA's permissions.

Defence: tighten `actAs`; use Org Policy `iam.disableServiceAccountKeyCreation`.

#### Path C — Public Cloud Storage buckets
- Same class as S3. `gsutil ls -L gs://bucket`.

Defence: Uniform bucket-level access; Public Access Prevention enforced; Org policies preventing public buckets.

### Useful commands

```bash
gcloud auth list
gcloud projects list
gcloud projects get-iam-policy $PROJECT
gcloud iam service-accounts list --project=$PROJECT

# Recursive bucket listing
gsutil ls -r gs://bucket
```

### Audit tools
- **Prowler** — GCP support.
- **GCPBucketBrute** — find public / writable storage buckets.
- **Hayat** — GCP audit.
- **CloudFox** — multi-cloud post-exploitation enumeration.

---

## 5. Kubernetes

### Threat model
1. RBAC misuse → cluster admin escalation.
2. Container escape → host pwn.
3. Secrets exposed in env vars / mounted files.
4. Network policy gaps → pod-to-pod lateral movement.
5. Supply chain → malicious image.

### Common attacks

#### Pod escape via privileged: true
- Pod with `securityContext.privileged: true` can mount host filesystem → cluster admin.
- Pod with `hostPID: true` can `nsenter` into host processes.

Defence: PodSecurityStandards (Restricted profile); `runAsNonRoot: true`; admission controller (Kyverno / OPA Gatekeeper) blocking privileged pods.

#### RBAC privilege escalation
- ServiceAccount with `pods/exec` + access to a high-privileged pod (e.g. the API server).
- `kubectl exec -n kube-system <pod>` → admin context.

Defence: minimize ServiceAccount permissions; `automountServiceAccountToken: false` on pods that don't need API access.

#### Etcd plaintext secrets
- etcd by default stores secrets unencrypted.
- Anyone with etcd access reads everything.

Defence: enable encryption-at-rest with KMS; restrict etcd to control-plane network only.

### Audit tools
- **kube-bench** — CIS benchmark scanner.
- **kube-hunter** — penetration tester.
- **Trivy** — image + IaC scanner.
- **Falco** — runtime threat detection.
- **Peirates** — k8s exploitation.

---

## 6. Cross-cloud common misconfigurations

| Pattern | Found via |
|---------|-----------|
| Storage bucket publicly readable | scoutsuite, prowler |
| Long-lived access keys / SA keys | IAM credential reports |
| Overly permissive `*` in policies | iam_simulator, Access Analyzer |
| Logs disabled or short retention | per-service audit |
| MFA missing on root / Global Admins | IAM credential reports, Entra reports |
| Default VPC / network used in production | network audit |
| Snapshots / images publicly shared | per-service audit (`describe-images --executable-users all`) |
| Lambda / Function secrets in env vars (vs Secrets Manager) | code review, IaC scan |

---

## 7. Audit / pentest tools — quick selector

| Goal | Tool |
|------|------|
| Multi-cloud audit, HTML report | ScoutSuite |
| AWS deep audit + benchmarks | Prowler |
| Azure deep audit | Prowler / MicroBurst |
| GCP audit | Prowler / Hayat |
| AWS exploitation framework | Pacu |
| Azure exploitation | ROADtools + AADInternals |
| Cross-cloud post-ex enum | CloudFox |
| Adversary emulation | Stratus Red Team |
| Find public buckets | GCPBucketBrute, S3Scanner |
| K8s benchmark | kube-bench |
| K8s pentest | kube-hunter, Peirates |

---

## 8. Defence — minimum baseline by cloud

### AWS
- All accounts under an Organization with SCPs preventing root key creation, public S3, IMDSv1.
- CloudTrail enabled in all regions, logs to a dedicated logging account.
- GuardDuty enabled in all accounts + regions.
- Access Analyzer enabled.
- Block Public Access on S3 at org level.
- Permissions Boundaries on developer roles.
- Quarterly access review.

### Azure
- Conditional Access policies: block legacy auth, require MFA, geo-fence admin.
- Privileged Identity Management (PIM) — just-in-time admin elevation.
- Defender for Cloud Standard tier on all subs.
- Sentinel ingesting Sign-in Logs + Azure Activity + on-prem AD.
- App registrations restricted to specific users.
- No standing Global Admins for ops work.

### GCP
- Org Policy: disable SA key creation, restrict public IPs, force uniform bucket access.
- Cloud Audit Logs Data Access enabled on critical services.
- VPC Service Controls around sensitive data perimeters.
- Workload Identity for GKE (no node-level SA keys).
- Security Command Center Standard or Premium.

### Cross-cloud
- IaC scanning (Checkov / tfsec / Trivy) in CI before deploy.
- SBOM + image scanning in CI.
- Secrets in a vault (Secrets Manager / Key Vault / Secret Manager), never in env or code.
- Cost anomaly alerts (cheap pre-compromise indicator: crypto-mining spikes spend).

---

## 9. Cloud incident response specifics

When an incident is in cloud (vs on-prem):

1. **Don't just delete the compromised credential.** Disable, rotate, but preserve audit trail.
2. **Snapshot before remediation.** EBS snapshot / Azure disk snapshot / GCP snapshot of any compromised compute. You'll want forensic copies later.
3. **CloudTrail / Activity Log replay** — query for everything the credential did. CSV-export it; logs may roll over.
4. **Look for persistence specific to cloud**: new IAM users, new access keys on existing users, new SSH keys on EC2, new IAM roles trusted across accounts, new login profiles, console password resets, Lambda functions with admin roles.
5. **Cross-account audit** — attacker may have set up an AssumeRole trust into their account.
6. **Spend anomaly check** — cryptomining is the #1 monetization pattern after stolen creds.
7. **Notify the cloud provider** — AWS Trust & Safety, Azure incident response. They sometimes have additional telemetry.
