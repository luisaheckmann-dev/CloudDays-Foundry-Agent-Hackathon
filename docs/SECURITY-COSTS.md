# Security, privacy, permissions and costs

[Home](../README.md) · [Architecture](ARCHITECTURE.md) · [Cleanup](labs/06-cleanup.md)

## Customer authority and least privilege

All hands-on resources, billing and identities belong to the customer.
Facilitators guide participants in their own browser/terminal; they do not
provide accounts, resource access, keys or roles, and need no customer tenant
invitation. Never collect passwords, MFA codes, tokens or credential exports.
An authorized customer admin approves privileged operations, IAM, consent,
network changes and spending. Guidance is not permission to bypass policy.

Use the official [Foundry RBAC reference](https://learn.microsoft.com/en-us/azure/foundry/concepts/rbac-foundry)
and [environment setup](https://learn.microsoft.com/en-us/azure/foundry/agents/environment-setup).
Roles may still display their former "Azure AI …" names; verify the definition
and scope, not a similarly named legacy hub/ML role.

| Identity / operation | Approved authority and narrow scope |
|---|---|
| Customer subscription/security/budget owner | Approves active subscription, cost ceiling/process, region, data, network and retention |
| Customer bootstrap operator: new RG / required provider registration | Relevant subscription actions; a project role or RG-only role cannot register subscription providers |
| Customer resource/model operator: Foundry resource, project, deployment | Foundry Account Owner or other approved management role at the needed dedicated RG/subscription scope; management alone does not grant project data actions |
| Customer access administrator | `Microsoft.Authorization/roleAssignments/write` at each target, e.g. approved RBAC Administrator/User Access Administrator/Owner; Foundry roles' conditional assignment powers are limited |
| Human participant: create/edit/test agents and vector stores | **Foundry User on the intended project**; **Reader on the parent resource** only if navigation needs it |
| Project runtime | **Project managed identity**, with verified model/resource access; documented baseline: Foundry User on the actual parent Foundry resource for that identity |
| Human upload path, if required by actual setup | **Storage Blob Data Contributor** only on the actual upload storage scope; not speculative access to unrelated storage |
| Standard backing resources | Customer admin applies the current Storage/Search/Cosmos roles and connections to the correct managed identities, separately from human roles |
| Designated quota operator | **Cognitive Services Usages Reader at subscription scope** if quota/eligibility visibility requires it; not routine for all learners |
| Approved monitoring reader | Narrow monitoring/workspace access, e.g. Log Analytics Reader; protected tables may need additional approval |
| Optional IQ KB/index management and ingestion | **Search Service Contributor** for KB/index; **Search Index Data Contributor** for synthetic indexing, on the one approved Search service |
| Optional IQ runtime | **Search Index Data Reader** for the actual project/agent runtime identity on the approved Search service |
| Optional IQ: Search calls its model | Search managed identity with **Cognitive Services User** on that model resource as required by the Search integration, not a replacement for Foundry project roles |
| Optional IQ: project RemoteTool connection | Customer-approved connection-management permission, e.g. Foundry Project Manager at the appropriate documented scope; verify the denied operation before any grant |

**Foundry User cannot create resources/projects, deploy models or assign roles.**
Azure Owner/Contributor alone does not grant Foundry data actions; Contributor
also cannot assign roles. Foundry Owner combines privileged management/data
capabilities and is not the default attendee role. Do not distribute blanket
subscription Owner, Contributor, Global Administrator or resource-wide Foundry
User as a workshop repair.

## Scoped role assignment procedure

1. The authorized **customer admin** signs in to the Azure portal with their
   own identity, verifies directory/subscription and activates approved privileged
   authority if required. The participant never uses the admin's session.
2. Open the **specific target** → **Access control (IAM)** → **Check access**.
   Review direct/inherited roles and the denied operation.
3. If approved, use **Add → Add role assignment**, choose the exact role and
   inspect permissions/scope. For humans choose **User, group, or service principal**
   and the verified customer-internal principal/group, not a guessed identity.
4. For project-scoped Foundry User, use **Manage → Project details → Users →
   Add user** when exposed and correctly project-scoped, or the project IAM
   route. Verify the final scope. If unavailable, the customer access admin
   uses an approved administration route or records `BLOCKED`; do not silently
   widen human access to all projects. Add parent Reader only when needed.
5. On the Foundry resource's IAM page choose **Managed identity** for runtime
   access and select the **project's** identity, not merely the parent resource
   or the human. Verify its Foundry User/model access. A role-capable creator
   may cause automatic assignments at project creation; **check both human
   and project identity**, including broad inherited creator rights.
6. For Standard setup verify the exact Storage/Search/Cosmos dependencies and
   resource-specific runtime roles using the official setup contract. Human
   upload access and service runtime access are different. Do not substitute keys.
7. Review assignments, allow propagation, refresh/re-authenticate as needed.
   Have each participant verify with **their own sign-in**: portal, CLI,
   model preflight, upload/indexing and Lab 02 smoke. Admin success is not
   participant proof.

Prefer one person per project. A team may intentionally share a **customer-owned**
project/model only with explicit customer approval of the common data boundary
and budget. Agents in one project are not a confidentiality boundary for files,
conversations, vectors or indexes. Check membership and inherited grants without
opening another person's data; unexpected access goes to the customer security
owner. Never test against instructor infrastructure.

## Data and identities

- Upload only the synthetic policy/inventory material. No real orders, PII,
  email, chats, customer documents or business secrets.
- `.env.example` contains placeholders only; `.env`, `.local` and `.venv` are
  Git-ignored. No keys or access tokens belong in environment files.
- `AzureCliCredential` deliberately uses explicit `az login`, not a silent
  managed-identity/VS Code/default-credential fallback. Optional **one** selector,
  `AZURE_TENANT_ID` **or** `AZURE_SUBSCRIPTION_ID`, selects an already signed-in
  context per call; Azure CLI permits only one token selector. The application
  does not change the global CLI default. A matching tenant alone does not
  prove entitlement to the correct subscription; verify the actual project scope.
- Shell variables take precedence over `.env`; privately inspect names/values
  only as necessary to resolve unexpected configuration. Never export credentials.
- Diagnostics store IDs, tool names, status, token counts and timing, not full
  prompts/responses. Private evaluation results do contain model text in `.local`.
- **Git ignore is not OneDrive protection.** Work in a customer-approved local
  nonsynchronized folder where required. Keep private artifacts out of synced
  locations and public screenshots. This workshop uses only synthetic data.
- Cloud responses/files may be retained by the service; the manifest tracks
  created IDs for scoped cleanup. Customer retention/audit policy still applies;
  deletion does not promise immediate removal from every compliance copy/backup.
- No external MCP servers or internet tools in the core. Test injection as
  synthetic data, never by real secret access or exfiltration.

## Local approval: exact guarantees

`propose_order` validates and stages only an **in-memory** proposal. It is not
a write tool. The opt-in `--enable-local-drafts` **and** exact human terminal
`APPROVE <displayed-id>` are required for the sole write: a local SQLite
simulation record. Chat "yes", model output and piped approval do not qualify.
SKU, quantity, policy ID and current policy-file SHA-256 bind the proposal.
Before saving, the code revalidates the proposal and stock/blocked status.
Parameterized SQL and a primary key deduplicate; inventory remains read-only.
Policy translation changes hashes/IDs; do not reuse old IDs or migrate old drafts.

Not guaranteed: ERP reservation, real orders, distributed approval, M365 identity
approval, immutable audit or actual delivery. A local file owner can edit the
program. Production requires server-side authorization, transactions, role/
dual-control design and immutable audit. Azure customer access and this local
prototype approval gate are different security boundaries.

## Budget limits and cost traps

- Every cloud command requires `--allow-cloud`. Offline is never an automatic
  replacement that masquerades as cloud success.
- Per request: max **4 Responses**, **6 local function calls**, **3 service-side
  tool calls per Response**, **1200 requested output tokens**. Input max 8000
  characters; chat max 10 independent requests.
- Cloud preflight performs a real model probe with up to 512 output tokens.
- Evaluation defaults to 3 cases, explicitly max 10, with no automatic LLM judge.
  Ten cases could use up to 40 Responses and 48,000 requested output tokens;
  input/retrieval/reasoning tokens and actual billing are additional. This is
  **not a fixed currency price**.
- SDK retries are disabled. Visible failures and manual reruns may still cost.
  Upload polling is bounded; existing stores block accidental duplicate upload.
- File Search may charge for storage/tools as well as model use. Store expiry
  after one day of inactivity does not clean up uploaded files.
- Standard backing Search/Storage/Cosmos, optional Search KBs, hosted compute,
  container registries and monitoring have separate costs.
- Fabric and M365 Work IQ are not core requirements; optional integrations may
  require additional capacity, usage billing and licenses.

The **customer budget/resource owner** approves budget alerts, allowed deployment,
team call limits and a stop-spending contact. Facilitators help estimate and
coordinate requests; they neither pay nor control customer billing. Azure
budget alerts are **notifications, not a hard cap**. Check current prices,
region and deployment type; never promise universal free usage.

Size customer quota before the event: concurrent teams × measured input/output
tokens per minute. Do not first test registration/evaluation and ten parallel
teams on a small deployment on the day. A starting coordination plan is at most
two teams per request wave; the designated customer operator verifies actual
quota and handles 429, without automatic retries or instructor fallback.

## Resource-scoped cleanup

1. Inspect the SDK manifest, then `cleanup` only its versions, Responses, stores
   and files. Retain the manifest on partial failure.
2. Manually remove only the separately created personal portal agent.
3. Optional KB, source, index, connection, toolbox or hosted compute requires
   a separate customer ownership list and approval.
4. Never broadly delete shared model/Foundry/Search/Storage/resource groups.
5. Customer owners approve removal of dedicated remaining infrastructure and
   check billing/retention. Track any blocker with a customer owner and action.
