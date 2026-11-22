# Offboarding and Exit Procedures

**Procedure code:** NGT-HR-009  
**Owners:** People & HR and Internal IT  
**Security owner:** Omar Farouk, Information Security Officer  
**Effective date:** 1 January 2026  
**Version:** 2.1  
**Classification:** Internal - Restricted for individual cases

---

## 1. Purpose

This procedure coordinates employment separation, knowledge transfer, access removal, asset return, final payroll, and continuing confidentiality obligations. It applies to resignations, end of fixed-term employment, retirement, redundancy, and company-initiated termination.

## 2. Notice Periods

The applicable employment agreement and law control where they provide a different period. NewGen Tech's standard notice periods are:

| Career level | Standard notice period |
|---|---:|
| L1-L2 | 30 calendar days |
| L3-L4 | 60 calendar days |
| L5-L6 | 90 calendar days |
| Intern or fixed-term employee | As stated in the agreement |

A shorter or longer working period may be agreed in writing by the employee, manager, and People & HR. NewGen Tech may place an employee on paid notice without active duties where lawful and appropriate.

## 3. Resignation Submission

An employee resigns by sending a dated written notice to the manager and People & HR. The notice should state the intended final employment date.

People & HR will acknowledge receipt within two business days and confirm:

- Contractual notice period.
- Provisional final employment date.
- Remaining annual-leave balance.
- Exit coordinator.
- Handover and asset-return requirements.
- Any restrictions applying during notice.

A Slack message or verbal discussion does not replace written notice.

## 4. Offboarding Case Classification

People & HR assigns one of the following handling paths:

- **Standard:** voluntary departure with normal notice.
- **Accelerated:** shortened working notice or immediate access changes.
- **End of term:** expiry of an internship or fixed-term agreement.
- **Involuntary:** company-initiated separation.
- **Sensitive:** separation involving security, legal, employee-relations, or safety risk.

Only people with an operational need may access the case record.

## 5. Roles and Responsibilities

### People & HR

- Confirms dates, documentation, leave, benefits, and final-payroll instructions.
- Coordinates the exit interview.
- Maintains the official case record.
- Notifies Legal when required.

### Manager

- Defines the transition plan.
- Reassigns work and customer responsibilities.
- Reviews documentation and confirms completion.
- Communicates the departure appropriately.

### Internal IT

- Removes or transfers access.
- Collects and verifies assets.
- Preserves business data where authorized.
- Updates the asset register.

### Information Security

- Determines risk-based access timing.
- Preserves logs or evidence for sensitive cases.
- Reviews privileged, production, and customer access.

### Finance and Payroll

- Calculates final salary, approved expenses, leave treatment, deductions, and other amounts.
- Cancels cards and financial approval rights.

### Departing Employee

- Completes an accurate handover.
- Returns company property.
- Submits expenses promptly.
- Protects confidential information before and after departure.

## 6. Offboarding Timeline

| Timing | Required action |
|---|---|
| Notice received | HR opens case; manager confirms transition needs |
| Within 2 business days | Dates, notice, access risk, and asset inventory confirmed |
| During notice | Knowledge transfer, ownership reassignment, expense submission |
| 5 business days before final day | IT validates access-removal plan and return appointment |
| Final working day | Assets returned; access removed at approved time; final checklist signed |
| Within 5 business days after departure | Shared ownership, forwarding, and system records verified |
| Final payroll cycle | Final amounts processed under payroll schedule and law |

For accelerated or sensitive cases, access may be removed before a discussion or immediately after notification.

## 7. Knowledge Transfer Protocol

The manager creates a transition plan in the approved restricted workspace. It must cover, as applicable:

1. Active projects, status, deadlines, and risks.
2. Jira epics, tickets, and decision records.
3. Product or architecture documentation.
4. Customer accounts, commitments, and escalation history.
5. Operational runbooks and PagerDuty responsibilities.
6. Vendor relationships and renewal dates.
7. Recurring reports, meetings, and approvals.
8. Named successor or temporary owner for every critical responsibility.

Credentials, private keys, tokens, and passwords must never be placed in handover documents. They must be rotated or transferred through the approved secrets-management process.

### 7.1 Product and Engineering Handover

Engineering departures must also address:

- Repository and code-owner assignments.
- Open pull requests and release branches.
- Production access and break-glass roles.
- Service dashboards, alerts, and runbooks.
- Architecture decisions not yet recorded.
- Dependencies across NovaCloud, PulseAI, or ShieldGate.

### 7.2 Customer-Facing Handover

Customer-facing departures must identify:

- Account owner and backup.
- Contractual or SLA commitments.
- Open support escalation.
- Renewal or implementation milestones.
- Customer communication owner.

The departing employee must not announce the departure to a customer before the manager approves the communication plan.

## 8. Access Removal

Internal IT uses the HR-confirmed final date and risk classification as the source of truth.

Access to be reviewed includes:

- Microsoft 365 or company email.
- Slack, Jira, Confluence, GitHub, and source repositories.
- AWS, GCP, Kubernetes, databases, and observability platforms.
- NovaCloud, PulseAI, and ShieldGate internal environments.
- Customer tenants and support tools.
- VPN, SSO, privileged access, and password management.
- Banking, payroll, expense, procurement, and signing authority.
- Office, coworking, badge, and physical key access.

Privileged and production access should normally be removed at the start of the final working day unless a documented operational need supports later removal. All remaining access is disabled no later than the approved separation time.

Shared credentials are prohibited. If exposure is suspected, Information Security initiates credential rotation and incident handling under `16_Incident_Response_and_OnCall_Runbook.md`.

## 9. Data Preservation and Mailbox Handling

Business records must remain in approved company systems. The departing employee must not copy company data to personal storage or delete records outside normal retention processes.

The manager may request:

- Transfer of OneDrive or repository ownership.
- Preservation of relevant mailbox or chat records.
- A time-limited email auto-reply.
- Reassignment of shared mailboxes, calendars, reports, and workflows.

Automatic forwarding to another person's mailbox is not enabled by default. People & HR, Legal, and Information Security must approve any exception.

## 10. Equipment Return Checklist

The employee must return all assigned property, including:

- Laptop and charger.
- External monitor owned by NewGen Tech.
- Docking station, headset, webcam, or security key.
- Mobile device or SIM, where issued.
- Access badge, office key, and visitor card.
- Test devices, hardware prototypes, and removable media.
- Purchasing card or other financial instrument.
- Paper records containing company or customer information.

IT compares returned items with the asset register and records condition. Normal wear is acceptable. Loss, damage, or delayed return is reviewed individually and is not deducted from pay unless lawful and documented.

Remote employees receive return instructions and an approved courier arrangement. Assets should normally be handed to the courier no later than three business days after the final working day.

## 11. Home-Office Equipment

Items fully or substantially reimbursed under `08_Expense_Reimbursement_Guidelines.txt` may be company assets. IT and Finance determine whether an item must be returned, transferred at residual value, or written off. The employee must not assume that reimbursement created personal ownership.

## 12. Annual Leave, Expenses, and Final Pay

People & HR and Payroll reconcile:

- Salary through the final employment date.
- Approved unpaid salary elements.
- Accrued but unused annual leave.
- Leave taken beyond accrual, where lawful.
- Approved expenses submitted before the deadline.
- Variable compensation under the relevant plan.
- Lawful asset or advance recovery.

Expense claims should be submitted at least five business days before the final working day. Late claims must follow `08_Expense_Reimbursement_Guidelines.txt`.

Final payment timing follows the normal payroll cycle unless law or the separation agreement requires earlier payment.

## 13. Benefits and Insurance

People & HR provides a written summary of:

- Medical-insurance end date.
- Dependent coverage end date.
- Any continuation option.
- Final learning or wellbeing benefit eligibility.
- Required employee contribution or refund.

Benefits must not be promised outside the applicable plan documents.

## 14. Exit Interview

People & HR offers a confidential exit interview for voluntary departures. Topics may include:

- Role and workload.
- Manager support.
- Career growth.
- Compensation and benefits.
- Hybrid work.
- Product or operational concerns.
- Reasons for leaving.

Participation is voluntary. People & HR may share aggregated themes with leadership but does not attribute comments unless needed to address misconduct, safety, legal, or security concerns.

## 15. Communications

The manager and People & HR agree on internal and external messaging. Communications should state only what is appropriate and confirmed.

- Team notification should identify the final date and transition owner.
- Customer notification requires account-owner approval.
- Sensitive case facts must not be discussed with employees who do not need them.
- References and employment verification are handled only by People & HR.

## 16. Continuing Obligations

After departure, the former employee remains bound by applicable obligations concerning:

- Confidentiality.
- Intellectual property.
- Customer and employee data.
- Return or deletion of company information.
- Non-solicitation or other lawful contractual restrictions.
- Cooperation with authorized legal or compliance requests.

Former employees must report accidental continued access to People & HR or Information Security and must not use it.

## 17. Rehire Eligibility

People & HR records rehire eligibility based on documented facts, including performance, conduct, notice compliance, and role availability. Rehire eligibility is an internal assessment and is not a guarantee of future employment.

## 18. Final Checklist

- [ ] Final employment and working dates confirmed.
- [ ] Leave and payroll balances reviewed.
- [ ] Knowledge-transfer owner confirms completion.
- [ ] Customer and vendor ownership reassigned.
- [ ] On-call and approval duties removed.
- [ ] All system and physical access disabled.
- [ ] Assets returned and condition recorded.
- [ ] Expenses submitted and cards cancelled.
- [ ] Business records and ownership preserved.
- [ ] Benefits notice issued.
- [ ] Exit interview offered.
- [ ] Final communication completed.

## 19. Related Documents

- `03_Code_of_Conduct_and_Ethics.txt`
- `05_Annual_and_Sick_Leave_Policy.pdf`
- `07_Compensation_Benefits_and_Health_Insurance.pdf`
- `08_Expense_Reimbursement_Guidelines.txt`
- `16_Incident_Response_and_OnCall_Runbook.md`
- `17_Information_Security_and_Data_Privacy.pdf`

**End of document**
