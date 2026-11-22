# Incident Response and On-Call Runbook

**Document ID:** NGT-OPS-016 | **Owner:** Site Reliability Engineering | **Security owner:** Omar Farouk

## 1. Severity
| Severity | Definition | Acknowledge | Update |
|---|---|---:|---:|
| SEV-1 | Broad outage, confirmed cross-tenant exposure, active critical compromise, or unrecoverable data-loss threat | 5 min | 30 min |
| SEV-2 | Major degradation or multiple customers blocked without workaround | 15 min | 2 hours |
| SEV-3 | Limited impact or workaround available | 4 business hours | Daily as needed |
| SEV-4 | Minor defect or request | 1 business day | Case plan |

## 2. PagerDuty Rotation
Each production service maintains primary and secondary weekly rotations. Handover occurs Sunday at 10:00 AM EET. The outgoing engineer reviews open incidents, muted alerts, risky changes, capacity concerns, expiring certificates, and maintenance. Annual leave requires prior rotation reassignment.

## 3. First 15 Minutes
1. Acknowledge PagerDuty and open the incident channel.
2. Confirm symptoms using dashboards and customer reports.
3. Assign Incident Commander, Technical Lead, Communications Lead, and Scribe.
4. Set severity and start an incident timeline.
5. Stop risky deployments and preserve evidence.
6. Apply the safest available mitigation.

## 4. Roles
- **Incident Commander:** owns coordination, severity, decisions, and closure.
- **Technical Lead:** directs diagnosis and mitigation.
- **Communications Lead:** prepares internal, status-page, and customer updates.
- **Scribe:** timestamps events, decisions, hypotheses, and actions.
- **Security Lead:** required for suspected compromise, PII, credentials, or cross-tenant risk.

## 5. Escalation
SEV-1 pages the service owner, SRE manager, Support Duty Manager, and executive duty contact. Security events page Omar Farouk. Material product decisions involve Nadia Kamal; systemic platform risk involves Tarek Mansour.

## 6. Communication Template
**Status:** Investigating / Identified / Monitoring / Resolved  
**Affected product/region:**  
**Customer impact:**  
**Started:**  
**Current action:**  
**Next update:**  
Do not speculate about cause, blame, or data exposure before confirmation.

## 7. Recovery and Closure
Confirm metrics remain stable for the agreed observation period, backlog is processing, failed jobs are safely retried, customer impact has ended, temporary access is removed, and monitoring is restored. The Incident Commander declares resolution.

## 8. Post-Mortem
SEV-1 and SEV-2 incidents require a blameless post-mortem within five business days.

### Template
- Incident ID, severity, product, region, and owners
- Executive summary and customer impact
- Timeline in EET/EEST and UTC
- Detection method and gaps
- Technical root cause and contributing factors
- What worked and what did not
- Corrective actions with owner, priority, and due date
- Security, privacy, contractual, and support follow-up
- Evidence and dashboard links

## 9. Action Tracking
Actions are Jira items, not only prose. SEV-1 corrective actions are reviewed weekly until closure. Overdue risk requires an owner, revised date, and documented acceptance.

## 10. Related
`12_ShieldGate_Security_Compliance_Specs.pdf`, `14_Customer_SLA_and_Support_Tiers.txt`, `17_Information_Security_and_Data_Privacy.pdf`.
