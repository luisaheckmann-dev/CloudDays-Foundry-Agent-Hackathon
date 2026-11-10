# Azure: Building & Deploying AI Agents with Microsoft Foundry

**Cloud Days · 210 minutes · English · Intermediate · Updated 2026-11-10**

## Contoso OrderOps: from evidence to controlled action

Build a **versioned Foundry prompt agent**: retrieve policy evidence, check synthetic
stock using local Python, explain a recommendation and save a **local simulated
draft only after explicit human CLI approval**. No real orders.
Foundry is the agent platform; VS Code is the local tool runtime.

**Required:** your own customer Microsoft Entra sign-in/MFA, an approved active
**customer-owned Azure subscription**, a budget owner and a reachable authorized
customer administrator; Python 3.11+, VS Code and Azure CLI. Foundry (new), a
compatible model deployment and scoped access must be ready before cloud labs.
**Not required:** Fabric capacity or an M365 Copilot license. File Search here
is **not Foundry IQ**; real IQ integrations are separate, optional extensions.

Facilitators actively help you configure Foundry access **in your own subscription,
with your own identity**, as far as customer permissions and prerequisites allow.
They guide account/directory/subscription selection, approved creation and access
diagnosis; customer admins perform privileged creation, IAM, consent and billing.
No instructor account, tenant invite, project, model, key or other infrastructure
is provided or required. Facilitators need no role in your tenant and never
collect passwords, MFA codes or credential exports.

Complete [from-zero customer setup](docs/labs/00-readiness.md#customer-bootstrap-before-the-workshop)
as prework where possible. Allow **60–90 minutes or more plus approval lead time**.
Lab 00 is a supported **15-minute checkpoint**, not a guarantee to resolve
first-time subscription, quota, network or permission issues. Unresolved access
is `BLOCKED` with a customer owner/action and a setup clinic or follow-up.

## Get started

Open the repository folder in VS Code; run all commands in the integrated
**PowerShell** terminal:

```powershell
.\scripts\bootstrap.ps1
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m orderops offline
```

These commands do **not** access Azure. Bootstrap installs the pinned packages
from PyPI. If script execution is blocked, [Readiness](docs/labs/00-readiness.md)
provides individual commands without changing execution policy.

| Your next step | Guide |
|---|---|
| Schedule and learning goals | [210-minute agenda](docs/AGENDA.md) |
| Customer setup, permissions and cloud preflight | [00 Readiness](docs/labs/00-readiness.md) |
| Understand an agent in the new portal | [01 Portal](docs/labs/01-portal.md) |
| File upload, indexing, citations and SDK version | [02 Grounding](docs/labs/02-grounding.md) |
| Debug your Python function and approval gate | [03 Code & Tools](docs/labs/03-tools.md) |
| Measure rather than guess | [04 Evaluation & Diagnostics](docs/labs/04-evaluation.md) |
| Team challenge | [05 Hackathon](docs/labs/05-hackathon.md) |
| Pitch and scoped cleanup | [06 Finish](docs/labs/06-cleanup.md) |

**Starter:** [starter](starter/inventory.py) contains real TODOs; its separate
learning checks are initially red by design. **Reference:** [solution](solution/inventory.py).
Never silently switch tracks; use `--track starter` or `--track solution`.
The opt-in local SQLite draft simulation remains a Pro-Code exercise, not an
enterprise identity-authorization system or a real ERP transaction.

## For facilitators

- [Demo and facilitator runbook](docs/INSTRUCTOR.md), [Architecture](docs/ARCHITECTURE.md)
- [Real Foundry IQ / Fabric IQ / Work IQ, optional](docs/optional/IQ.md)
- [Costs, privacy and least privilege](docs/SECURITY-COSTS.md)
- [Troubleshooting](docs/TROUBLESHOOTING.md), [Sources](SOURCES.md), [MIT license](LICENSE)

**Evidence boundary:** pinned SDKs and local offline checks have been validated.
Historical model and separate IQ probes are not acceptance evidence for a
participant's customer environment. **Customer identity, permissions, model,
File Search and end-to-end cloud acceptance remain `NOT_RUN` until executed
with that participant's own identity.** Run the explicit cloud smoke after Lab 02:
`.\.venv\Scripts\python.exe -m orderops smoke --allow-cloud --track solution`.
A green offline test is not a passed Foundry, IQ or model-quality test.
