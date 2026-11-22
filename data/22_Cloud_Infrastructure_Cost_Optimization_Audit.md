# Cloud Infrastructure Cost Optimization Audit

**Document ID:** NGT-AUD-022 | **Period:** January-September 2026 | **Owner:** FinOps and Platform Engineering

## 1. Executive Summary
Average monthly cloud spend in Q3 2026 was **USD 412,000**. AWS represented 72% and GCP 28%. The audit identified an annualized gross opportunity of USD 768,000, before growth and implementation cost. Q4's approved net savings target is **USD 145,000** against the existing forecast.

## 2. Spend Breakdown
| Platform / workload | Monthly average | Share |
|---|---:|---:|
| AWS compute and Kubernetes | $146,000 | 35.4% |
| AWS databases and cache | $78,000 | 18.9% |
| AWS storage, network, other | $73,000 | 17.7% |
| GCP PulseAI processing | $67,000 | 16.3% |
| GCP analytics and storage | $48,000 | 11.7% |
| **Total** | **$412,000** | **100%** |

## 3. Existing Commitment Savings
AWS Savings Plans and Reserved Instances cover 61% of stable compute and database usage and produced estimated Q3 savings of **USD 132,000** versus equivalent on-demand pricing. GCP committed-use discounts cover 43% of predictable model-serving capacity and saved approximately **USD 54,000** in Q3.

## 4. Findings
### Idle and Oversized Compute
Thirty-seven development instances had under 5% average CPU for 30 days. Eleven production node groups showed sustained memory headroom above 55%. Estimated annual opportunity: USD 214,000.

### Non-Production Scheduling
Development and integration clusters run continuously despite defined working windows. Weeknight and weekend scheduling can save an estimated USD 156,000 annually after excluding CI and on-call test capacity.

### Storage Lifecycle
NovaCloud raw collection objects and PulseAI intermediate artifacts exceed operational retention in several buckets. Lifecycle and compaction changes can save USD 91,000 annually without changing contractual retention.

### Data Transfer
Cross-region observability and duplicate model artifacts add approximately USD 18,000 monthly. Regional aggregation and artifact locality can reduce this by 35-45%.

### Commitments
An additional USD 27,000 monthly of stable database and model-serving baseline is suitable for one-year commitments. Three-year terms are not recommended while regional architecture is changing.

## 5. Approved Q4 Actions
| Action | Owner | Q4 target |
|---|---|---:|
| Schedule eligible non-production clusters | Platform Engineering | $42,000 |
| Right-size Kubernetes node groups | SRE | $31,000 |
| Add object lifecycle and compaction | NovaCloud / PulseAI | $24,000 |
| Purchase approved one-year commitments | FinOps | $33,000 |
| Reduce cross-region telemetry and artifacts | Observability / ML Platform | $15,000 |
| **Total** |  | **$145,000** |

## 6. Controls
Savings changes must preserve service objectives, recovery capacity, security logging, contracted retention, and incident response. Production downsizing requires a rollback plan and 14-day observation period. Commitments require Finance approval and documented break-even analysis.

## 7. Measurement
FinOps will compare normalized cost per active tenant, PulseAI job, NovaCloud account, and ShieldGate million requests. Reported savings exclude customer growth, credits, tax, and currency effects unless stated.

## 8. Risks
Over-commitment, reduced incident headroom, storage deletion errors, regional concentration, and hidden egress can eliminate savings. No action may bypass `13_Product_Release_Lifecycle_and_Versioning.md` or `17_Information_Security_and_Data_Privacy.pdf`.
