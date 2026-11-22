# Product Release Lifecycle and Versioning

**Document ID:** NGT-PROD-013 | **Owner:** Product Operations and Engineering | **Version:** 2.2

## 1. Versioning
NewGen Tech uses semantic versioning `MAJOR.MINOR.PATCH` for public APIs and deployable customer-facing components.
- **MAJOR:** intentional incompatible change with migration guidance.
- **MINOR:** backward-compatible feature.
- **PATCH:** backward-compatible fix or security update.
Prerelease labels include `-alpha`, `-beta`, and `-rc.N`. Build metadata is internal and must not be used for precedence.

## 2. Lifecycle Stages
Discovery, design, implementation, internal validation, staging, release candidate, production, adoption monitoring, and retirement. Each stage has a named Product and Engineering owner.

## 3. Quality Gates
Required gates are automated tests, peer review, dependency and secret scanning, observability, runbook impact, migration and rollback plan, Product acceptance, and security review for material risk.

## 4. Environments
| Environment | Purpose | Data rule |
|---|---|---|
| Development | Local or ephemeral engineering work | Synthetic data only |
| Integration | Service-to-service validation | Synthetic or approved test fixtures |
| Staging | Production-like acceptance and performance tests | Masked or synthetic data |
| Production | Contracted customer workloads | Authorized customer data only |

## 5. Production Windows
- Standard production deployment: Sunday-Wednesday, 10:00 AM-2:00 PM EET.
- Low-risk configuration: Sunday-Thursday, 10:00 AM-4:00 PM EET.
- Thursday production changes require Engineering Manager approval.
- Friday, Saturday, and published company holidays are change freezes unless an approved hotfix or customer-specific window applies.

## 6. Release Approval
Low-risk changes require service owner approval. Medium-risk changes require Engineering Manager and Product owner approval. High-risk changes require Architecture or Security review, change record, tested rollback, and designated incident coverage.

## 7. Hotfix SLA
| Priority | Target |
|---|---|
| Active critical security exploit or SEV-1 defect | Mitigation within 4 hours; corrected release target within 24 hours |
| SEV-2 production defect | Mitigation within 8 hours; corrected release target within 2 business days |
| High but non-incident defect | Patch target within 5 business days |

Targets are operational objectives, not separate customer-service credits.

## 8. Rollback
Rollback triggers include material error increase, authorization failure, cross-tenant risk, corruption, latency breach, or customer workflow failure. The incident commander may halt or reverse a deployment without waiting for normal approval.

## 9. API Compatibility
Deprecated API versions remain supported for at least 12 months after published notice unless security, law, or third-party dependency makes continued operation unsafe. Notices identify replacement, migration steps, test environment, and removal date.

## 10. Release Notes
Customer-visible notes state product, version, release date, features, fixes, known limitations, migration action, and documentation links. Internal notes also identify change record, owners, dashboards, flags, and rollback reference.

## 11. Related
`11_PulseAI_API_Integration_Guide.html`, `12_ShieldGate_Security_Compliance_Specs.pdf`, `16_Incident_Response_and_OnCall_Runbook.md`.
