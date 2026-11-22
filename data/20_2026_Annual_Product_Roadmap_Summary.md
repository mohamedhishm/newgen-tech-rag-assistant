# 2026 Annual Product Roadmap Summary

**Document ID:** NGT-STRAT-020 | **Owner:** Product Operations | **Sponsor:** Nadia Kamal

> Roadmap items express current intent, not contractual commitments. Dates may change after discovery, security review, customer validation, or dependency changes.

## Q1: Foundation
| Product | Milestone |
|---|---|
| NovaCloud | GCP organization inventory, policy-pack v2, regional onboarding automation |
| PulseAI | Report-template studio beta, dataset quality profiler, job retry controls |
| ShieldGate | OIDC federation enhancements, administrative audit export, mTLS pilot |

## Q2: Scale and Adoption
| Product | Milestone |
|---|---|
| NovaCloud | Cost allocation tags, account-health dashboard, Jira workflow integration |
| PulseAI | Forecast model registry, scheduled report API, Arabic report localization beta |
| ShieldGate | Adaptive risk policies, client-credential rotation workflow, SCIM provisioning beta |

## Q3: Reliability and Enterprise Controls
| Product | Milestone |
|---|---|
| NovaCloud | me-central collection isolation, stale-data indicators, recovery rehearsal |
| PulseAI | p95 report latency program, model-monitoring dashboard, webhook signing |
| ShieldGate | regional session continuity, key lifecycle dashboard, audit retention controls |

## Q4: Portfolio Integration
| Product | Milestone |
|---|---|
| NovaCloud | ShieldGate-backed privileged actions, optimization recommendation controls |
| PulseAI | NovaCloud operations-data connector, explainability export, enterprise quota controls |
| ShieldGate | unified policy insights for NovaCloud and PulseAI APIs, customer-managed signing-key pilot |

## Shared Platform Commitments
- Signed production artifacts across all services.
- Unified tenant and entitlement service.
- Standard regional data-residency controls.
- Common audit-event schema and correlation IDs.
- Customer-facing status integration aligned with support tiers.

## Success Measures
NovaCloud: collection freshness, policy-action rate, cloud spend coverage. PulseAI: report latency, successful job rate, template adoption. ShieldGate: authorization latency, key-rotation adoption, policy-denial accuracy. Portfolio: 99.95%+ availability and reduced onboarding time.

## Governance
Monthly Product Council reviews scope, evidence, risk, staffing, and dependencies. High-risk identity, tenancy, privacy, or data-residency changes require Omar Farouk's security review. Material architecture investment is escalated to Tarek Mansour.

## Dependencies and Risks
Cloud-provider API changes, data residency, model validation, shared identity migration, hiring capacity, and customer migration readiness may change sequence. Product Operations maintains the authoritative detailed roadmap.
