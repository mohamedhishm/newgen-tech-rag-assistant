# NovaCloud Architecture Overview

**Document ID:** NGT-PROD-NC-010  
**Owner:** NovaCloud Engineering  
**Executive sponsor:** Tarek Mansour, CTO  
**Product sponsor:** Nadia Kamal, Head of Product  
**Effective date:** 15 October 2026  
**Version:** 3.2  
**Classification:** Internal - Confidential  
**Audience:** Engineering, Product, Security, Solutions Engineering, and Support

---

## 1. Product Purpose

NovaCloud is NewGen Tech's cloud infrastructure management platform. It gives enterprise teams a governed view of cloud inventory, policy posture, cost signals, capacity, and operational health across supported AWS and Google Cloud environments.

NovaCloud is a control and visibility plane. It does not require customers to route normal application traffic through NewGen Tech infrastructure.

## 2. Architectural Principles

1. **Tenant isolation first:** Every request, event, and stored record carries an immutable tenant context.
2. **Least privilege:** Customer integrations use scoped roles and read-only access by default.
3. **Regional containment:** Tenant data remains in the contracted processing region except for explicitly approved global metadata.
4. **Asynchronous collection:** Cloud inventory and policy evaluation are decoupled from the user interface.
5. **Auditable change:** Administrative actions and policy changes generate protected audit events.
6. **Graceful degradation:** A delayed cloud provider API or analytics job must not make the tenant console unavailable.
7. **Observable services:** Each production service publishes health, latency, error, saturation, and dependency metrics.

## 3. Supported Production Regions

| NovaCloud region | Primary location | Paired recovery location | Supported cloud accounts |
|---|---|---|---|
| `eu-central` | Frankfurt, Germany | Dublin, Ireland | AWS and GCP |
| `me-central` | UAE | Frankfurt, Germany | AWS and GCP |

New customer tenants are assigned a home region during provisioning. Tenant content, inventory, policy results, and audit records remain in that home region. Cross-region transfer is limited to encrypted backup metadata, service-health telemetry without customer payloads, and approved disaster-recovery replication.

Region changes require a migration plan, customer approval, Product Operations coordination, and Information Security review.

## 4. High-Level Component Model

| Component | Responsibility |
|---|---|
| Web Console | Tenant administration, inventory search, policy findings, cost views, and operational dashboards |
| API Gateway | Request authentication, routing, quotas, schema validation, and request correlation |
| Identity Broker | Enterprise SSO integration, OIDC/SAML federation, role mapping, and session controls |
| Tenant Context Service | Resolves tenant, region, entitlements, and authorization context |
| Connector Manager | Manages AWS roles and GCP service-account integrations |
| Collection Workers | Poll provider APIs and process cloud events |
| Resource Inventory | Stores normalized cloud resource state and relationships |
| Policy Engine | Evaluates resources against built-in and customer-defined controls |
| Cost Analytics | Ingests billing exports and calculates allocation, trend, and optimization signals |
| Workflow Service | Assigns findings, records exceptions, and integrates with Jira or webhooks |
| Notification Service | Sends approved email, Slack, and webhook notifications |
| Audit Ledger | Stores append-only security and administrative events |
| Observability Stack | Metrics, logs, traces, dashboards, and service-level alerts |

## 5. Request Flow

A normal interactive request follows this sequence:

1. The user authenticates through the configured enterprise identity provider.
2. The Identity Broker validates the assertion and maps the user to NovaCloud roles.
3. The API Gateway validates the session, request schema, rate limit, and correlation ID.
4. The Tenant Context Service resolves the tenant home region and authorization scope.
5. The target service executes a tenant-scoped query or command.
6. Administrative or security-relevant activity is written to the Audit Ledger.
7. The response includes a correlation ID used by Support and Engineering for investigation.

No service may infer tenant identity from an email domain, URL text, or client-supplied database key.

## 6. Cloud Account Integration

### 6.1 AWS

NovaCloud uses a customer-created IAM role with an external ID unique to the tenant and integration. The default integration is read-only and permits inventory, configuration, CloudWatch metadata, and approved cost-data access.

NovaCloud does not request customer root credentials, IAM user passwords, or long-lived access keys. Optional remediation actions use a separate role with explicitly approved permissions.

### 6.2 Google Cloud

NovaCloud uses workload identity federation or a dedicated service account with defined organization, folder, project, and billing permissions. Customer-managed service-account keys are discouraged and require an approved exception when federation is unavailable.

### 6.3 Connector Behavior

- Credentials and federation configuration are stored in the regional secrets service.
- Collection jobs are queued by account and resource family.
- Provider throttling uses exponential backoff with jitter.
- Last successful collection time is visible to authorized users.
- A connector failure does not delete the last known inventory state.
- Stale records are clearly marked and excluded from current-state assertions after the configured threshold.

## 7. Event and Collection Pipeline

NovaCloud combines periodic reconciliation with provider events.

1. Connector Manager schedules collection.
2. Collection Workers call provider APIs using tenant-scoped credentials.
3. Raw responses are validated and written to a short-retention regional landing store.
4. Normalization converts provider-specific objects into the NovaCloud resource model.
5. Resource Inventory performs idempotent upsert and relationship resolution.
6. Policy Engine evaluates new or changed resources.
7. Cost Analytics attaches billing and allocation data where available.
8. Workflow and Notification services process actionable changes.

Every event includes `tenant_id`, `region`, `source_account`, `resource_id`, `schema_version`, `observed_at`, and `correlation_id`.

## 8. Multi-Tenant Isolation Model

NovaCloud uses logical multi-tenancy with layered controls.

### 8.1 Identity and Authorization

- Tenant membership is established through the Identity Broker.
- Role-based access control is evaluated for every API request.
- Sensitive operations may require step-up authentication.
- Support impersonation is disabled. Approved support access uses time-limited, audited roles.

### 8.2 Data Layer

- Application queries require a server-resolved tenant identifier.
- Row-level security policies enforce tenant boundaries in shared relational stores.
- High-volume object and analytics data use tenant-prefixed namespaces and scoped service credentials.
- Cache keys include tenant and region identifiers.
- Search indexes are partitioned by tenant boundary or enforce tenant filters in the service layer and index policy.

### 8.3 Compute and Messaging

- Worker messages include signed tenant context.
- Consumers reject missing, malformed, or region-mismatched context.
- Dead-letter queues retain tenant metadata and follow regional access restrictions.
- High-risk batch jobs run with a single tenant scope per execution.

### 8.4 Verification

Isolation controls are tested through:

- Automated authorization tests in CI.
- Negative cross-tenant API tests.
- Row-level security tests.
- Quarterly privileged-access reviews.
- Annual penetration testing.
- Security review for material changes to tenancy, identity, caching, or indexing.

A suspected cross-tenant exposure is treated as SEV-1 under `16_Incident_Response_and_OnCall_Runbook.md`.

## 9. Data Stores

| Store | Content | Retention summary |
|---|---|---|
| Regional relational database | Tenant configuration, identities, policy definitions, workflows | Contract term plus controlled deletion period |
| Resource inventory store | Normalized cloud resources and relationships | Current state plus configured history |
| Regional object storage | Billing exports, reports, temporary collection artifacts | By data class and customer plan |
| Search index | Searchable inventory projection | Rebuilt from authoritative inventory |
| Audit ledger | Authentication, administration, access, and policy events | Minimum 12 months online; longer by contract |
| Metrics and logs | Service telemetry and diagnostic events | Operational retention; customer payloads excluded by default |

Deletion is orchestrated by tenant and region. Search, cache, analytics, backup, and audit obligations are handled as separate deletion targets.

## 10. Encryption and Secrets

- External traffic uses TLS 1.2 or later.
- Data at rest uses provider-managed encryption with customer-specific or service-specific key boundaries where supported.
- Secrets are stored only in the approved secrets manager.
- Production secrets are not stored in source code, Jira, Slack, or CI variables without approved secret backing.
- Key use and privileged secret access are logged.
- Backup encryption keys are separated from primary workload permissions.

Detailed corporate requirements are defined in `17_Information_Security_and_Data_Privacy.pdf`.

## 11. Availability and Resilience

NovaCloud production services are deployed across multiple availability zones in each home region.

Key resilience patterns include:

- Stateless service replicas behind managed load balancing.
- Automatic health checking and replacement.
- Queue-based buffering for collection and policy evaluation.
- Database point-in-time recovery.
- Encrypted regional backups and tested restoration procedures.
- Circuit breakers for cloud provider and notification dependencies.
- Idempotency keys for retryable commands.

Target service objectives are maintained in the service catalog and aligned with the customer commitments in `14_Customer_SLA_and_Support_Tiers.txt`.

## 12. Disaster Recovery

Each critical service has a documented recovery tier, recovery-time objective, recovery-point objective, owner, and test schedule.

The regional recovery process prioritizes:

1. Identity and tenant routing.
2. API and Web Console read access.
3. Resource inventory.
4. Policy evaluation.
5. Collection backlog processing.
6. Cost analytics and non-urgent notifications.

Failover is authorized by the incident commander with the NovaCloud engineering owner and Information Security. Recovery tests are performed at least twice per year.

## 13. Observability

Mandatory telemetry includes:

- Request rate, errors, and latency by service and region.
- Queue depth and oldest message age.
- Collection success and staleness by provider.
- Database saturation, replication health, and slow queries.
- Policy-evaluation throughput and failure rate.
- Authentication failures and privileged actions.
- Tenant-impact indicators without exposing customer payloads.

Logs must use correlation IDs and structured fields. Sensitive tokens, credentials, personal data, and raw customer payloads must not be logged.

## 14. Deployment Model

Services are deployed through approved CI/CD pipelines using immutable artifacts and infrastructure as code.

- Pull requests require review and automated checks.
- Production artifacts are signed and promoted, not rebuilt.
- Database changes use backward-compatible migration patterns.
- Feature flags separate deployment from customer activation.
- Production windows and hotfix rules follow `13_Product_Release_Lifecycle_and_Versioning.md`.
- Emergency changes require incident or change references and retrospective review.

## 15. External Integrations

Supported integration categories include:

- AWS and Google Cloud APIs.
- Enterprise identity providers.
- Jira issue creation.
- Slack and email notifications.
- Customer webhooks.
- Approved billing exports.

Outbound webhooks are signed. Destinations are validated against tenant configuration, and repeated failures are disabled or quarantined to prevent uncontrolled retries.

## 16. Ownership Boundaries

| Area | Primary owner |
|---|---|
| Product requirements and customer use cases | NovaCloud Product Management |
| Service implementation and operations | NovaCloud Engineering |
| Shared runtime, Kubernetes, and CI/CD | Platform Engineering |
| Identity and access standards | ShieldGate and Information Security |
| Security review and incident oversight | Information Security |
| Customer configuration and adoption | Solutions Engineering and Customer Success |
| SLA communication | Customer Support and Commercial Operations |

## 17. Known Constraints

- Provider API limits can delay large-account reconciliation.
- Billing exports may arrive 24-48 hours after usage.
- NovaCloud cannot guarantee completeness when a customer removes required integration permissions.
- Resource relationships vary by provider and service maturity.
- Cross-region tenant migration is a planned operation, not an instant self-service action.
- Remediation is disabled unless the customer has configured the separate write-capable role.

These constraints must be represented accurately in customer discussions.

## 18. Related Documents

- `12_ShieldGate_Security_Compliance_Specs.pdf`
- `13_Product_Release_Lifecycle_and_Versioning.md`
- `14_Customer_SLA_and_Support_Tiers.txt`
- `16_Incident_Response_and_OnCall_Runbook.md`
- `17_Information_Security_and_Data_Privacy.pdf`
- `19_Q3_2026_Engineering_Performance_Report.pdf`
- `20_2026_Annual_Product_Roadmap_Summary.md`
- `22_Cloud_Infrastructure_Cost_Optimization_Audit.md`

**End of document**
