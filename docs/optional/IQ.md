# Optional stretch — real Foundry IQ, Fabric IQ and Work IQ

[Home](../../README.md) · [Architecture](../ARCHITECTURE.md) · [Sources](../../SOURCES.md)

**Not a core prerequisite.** Use a separately approved customer-owned test setup
for an optional demonstration or after core completion, not an additional block
inside 210 minutes. The mandatory path works without these resources/licenses.
Local files are not Fabric IQ, Work IQ or Foundry IQ. No required instructor
endpoint, project, account, model, Search service or other infrastructure.
Customer admins approve privileged provisioning, IAM, consent and billing;
facilitators guide without customer tenant access.

The procedures below are instructions only, **not executed by this update**.
Actual customer IQ acceptance remains **NOT_RUN** until tested with the intended
authorized identities. Missing approvals/resources are `BLOCKED`, not a cue to
rename a fixture or to use instructor hosting.

## 1. What proves a real integration?

| Component | Minimum evidence | Explicitly insufficient |
|---|---|---|
| Foundry IQ | Actual Azure AI Search KB, knowledge source, real retrieval/MCP call and sources | Renaming FileSearchTool |
| Fabric IQ | Actual Fabric item/semantic context and authorized service query with traceable source/metric | Reading JSON from `data` |
| Work IQ | Authorized real Work IQ query against approved M365 context with sources | Invented email/Teams fixture |

GA/preview boundaries depend on the exact API/source. The referenced Search
documentation distinguishes **2026-04-01** for GA/minimal extractive retrieval
and **2026-08-01-preview** for relevant advanced/LLM-based features. Portal/sample
paths may use preview; no blanket GA or production-readiness guarantee.

## 2. Foundry IQ — separate prerequisite check

The **customer's authorized operator** prepares:

1. A dedicated or explicitly approved customer Azure AI Search service in an
   eligible region/tier supporting managed identity, with approved RBAC.
2. Synthetic index, knowledge source and KB. Files/vector stores are **not**
   a Search knowledge base.
3. Optional LLM planning/synthesis: compatible Azure OpenAI deployment; Search
   system-assigned managed identity with **Cognitive Services User** on that
   model resource. Verify version/region compatibility separately.
4. Provisioning principal: **Search Service Contributor** for KB/index,
   **Search Index Data Contributor** for ingestion on that Search service.
5. Read-only runtime identity: **Search Index Data Reader** on Search.
6. Foundry (new) project and approved RemoteTool connection-management access.
7. Customer-approved cost estimate, data/retention policy and separate cleanup
   ownership list. No new terms/consent are accepted on a customer's behalf.

For ACL-protected or remote SharePoint sources, a global service identity
does **not** prove end-to-end user authorization. Verify source permissions,
ACL metadata and user-context propagation using the
[official connection guide](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/foundry-iq-connect).
An open synthetic index does not prove user-specific security trimming.

## 3. Portal path with a prepared knowledge base

1. In your approved **New Foundry** customer project open **Build → Knowledge**.
2. Connect the customer-approved Search service or select its prepared KB.
3. Only if authorized to create: **Create knowledge base**, add an existing
   knowledge source/prepared index, then inspect properties/validity using the
   [official KB guide](https://learn.microsoft.com/en-us/azure/search/agentic-retrieval-how-to-create-knowledge-base).
   Labels/source dialogs vary by rollout.
4. Test with a question only the synthetic index can answer. Inspect retrieval
   output and source references.
5. In **Build → Agents**, choose a **separate stretch agent**, not the core
   agent with its manifested File Search contract.
6. Connect the KB through the offered knowledge/tool configuration.
7. Ask a policy fact and verify the actual retrieval path and source.
   Add no write tools.

English equivalents of the portal flow originally inspected on **2026-11-04**:

1. **Build → Knowledge → Create new resource** may show capacity limits.
   Select an available **customer-approved** region before creation.
2. In Azure inspect Search pricing explicitly. **Basic, one replica and one
   partition** is a small managed-identity demo configuration if supported;
   never accidentally accept a Standard tier or extra search units. This
   **Search pricing tier** is not the Agent Service Basic/Standard setup mode.
3. Create the Foundry Search connection using **Project managed identity**.
   Search must allow the approved RBAC design: **Keys → API access control →
   Both** or **Role-based access control**, as approved by the customer.
   Do not weaken authentication to work around an error.
4. **Create knowledge base → Upload files** opens **Create knowledge source**
   after file selection. If embeddings require **Grant access**, the authorized
   customer admin verifies the **Search identity's** model access on the correct
   resource. Wait for processing; "active source, 0 files" is insufficient.
5. For actual LLM planning choose a supported chat deployment and **Retrieval
   reasoning effort: Low**. **Minimal** has no LLM query planning. **Extracted
   data** lets the agent reason from returned sources.
6. Save KB → **Use in an agent** → select the separate IQ agent. Verify the new
   saved agent version.
7. On **Search → Access control (IAM)** the customer admin assigns **Search
   Index Data Reader** to the **Foundry project identity** on that service.
   This is a different direction from Search → model access. Do not repair
   a 403 with generic Owner/Contributor.
8. After propagation ask in a new chat. Open **Agent → Traces → completed trace
   ID → execute_tool … knowledge_base_retrieve** and inspect input/output.

**Expected:** actual KB request and returned sources. Planning/synthesis depends
on mode; minimal extractive retrieval must not be called LLM search planning.

**Recovery:** 403 → actual runtime identity/scope; empty results → index,
source, scope and question. Missing Knowledge view → official current route,
not relabeled File Search. Customer admin success is not participant access proof.

## 4. SDK/MCP path: use the exact official contract

The [official connection guide](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/foundry-iq-connect)
describes the **prompt-agent** route:

1. Existing KB exposes an endpoint like
   `https://<search>.search.windows.net/knowledgebases/<kb>/mcp?api-version=2026-08-01-preview`.
2. A **RemoteTool project connection** authenticates to it; the documented
   example uses **ProjectManagedIdentity**.
3. The prompt agent gets an **MCPTool** using that project connection.
4. Expose only **knowledge_base_retrieve**, not every external MCP tool.
5. Verify answer sources and the identity/permission flow separately.

This repository does **not** register that connection automatically and has no
fake KB client reading local fixtures. For real setup follow the complete
official example; do not infer preview ARM connection contracts/project IDs
from the core manifest.

## 5. Optional executable Python as a hosted agent — different path

**Exact reference:** [Foundry sample / Responses / 17-foundry-iq-toolbox](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/python/hosted-agents/agent-framework/responses/17-foundry-iq-toolbox).
It includes `provision_kb.py`, `toolbox.yaml`, hooks, a manifest and a real
Responses host.

Source contract originally inspected on **2026-11-04**:

- `FoundryChatClient` comes from `agent_framework.foundry`.
- `FoundryToolbox` and `ResponsesHostServer` in its `main.py` come from
  **`agent_framework_foundry_hosting`**; do not blindly copy older imports.
- Sample Python requirement in `pyproject.toml`: **≥3.13**.
- Replace sample model `gpt-5.4-mini` deliberately with an actually available
  compatible customer deployment; no universal availability claim.

### Isolated customer-approved setup

These are **instructions**, not executed validation. Only an authorized
customer operator uses a separate ignored copy after approval. Keep it in an
approved nonsynchronized working folder; Git ignore alone does not stop OneDrive.

```powershell
# From the workshop repo; leave the core .venv unchanged.
New-Item -ItemType Directory -Path .local\iq-reference -Force | Out-Null
Set-Location .local\iq-reference
azd version
azd ext install microsoft.foundry
az login --tenant "YOUR-CUSTOMER-TENANT-ID"
azd ai agent init -m "https://github.com/microsoft-foundry/foundry-samples/blob/main/samples/python/hosted-agents/agent-framework/responses/17-foundry-iq-toolbox/azure.yaml"
```

1. In initialization choose your approved customer subscription/project and
   actual model. Verify CLI/directory context as in Lab 00. Do not accept an
   unknown subscription or unreviewed automatic infrastructure.
2. Read generated files/current sample README **before provisioning**. The
   top-level `postprovision` hook must be explicitly registered and point at
   actual `src\<agent-name>\hooks\postprovision.ps1`. Service-scoped hooks are
   not equivalent.
3. Configure the approved existing customer Search service:

   ```powershell
   azd env set AZURE_SEARCH_ENDPOINT "https://YOUR-SEARCH-SERVICE.search.windows.net"
   ```

4. Only after customer resource/cost/permission review, run `azd provision`
   according to the sample. Its hook creates index/KB, RemoteTool connection
   and toolbox; inspect exactly which resources/roles it proposes.
5. `TOOLBOX_ENDPOINT` then points to a Foundry toolbox MCP endpoint, which
   brokers to the actual Search KB.
6. Follow the sample's local hosting instructions and test in another terminal:

   ```powershell
   azd ai agent invoke --local "What can you tell me about the Earth at night?"
   ```

7. Only for explicitly approved cloud hosting follow the
   [hosted-agent deployment guide](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/deploy-hosted-agent).
   Verify Search Reader access for the **new agent identity after creation**.

**Difference:** hosted agents deploy executable Python as a service. Core
`register` deploys a prompt agent/tool metadata, not hosted Python.

**Cleanup:** sample resources are not in the core manifest. Track owned KB,
source, index, connection, toolbox, agent versions/compute and any created
infrastructure separately with the customer owner. No unreviewed `azd down`
on shared projects.

## 6. Fabric IQ — only with prepared business/semantic context

**Separate prerequisites:** customer-approved Fabric workspace and the capacity/
license for the actual feature, approved items, roles and tenant settings.
None is required for core. References: [Fabric IQ](https://learn.microsoft.com/en-us/fabric/iq/overview),
[Microsoft IQ Samples](https://github.com/microsoft/iq-samples).

Optional demonstration in an approved customer-owned test scope:

1. Prepare purely synthetic business data in a real Fabric item. Show the
   semantics of "available" versus "physical" and "reserved".
2. Select an actual semantic model/ontology/data-agent scenario with correct
   item/workspace authorization; disclose its preview status.
3. Execute an authorized service query and check response/query against source.
   A separate read-only adapter could later integrate this context into Foundry;
   it is **not included in core**.
4. Name identity, data freshness and metric definition.

**Expected:** evidenced Fabric business semantics. Exporting Fabric data and
reading it locally is only an export fixture, not current live Fabric IQ.

**Offline alternative:** `data\inventory.json` labeled "local synthetic snapshot".
Same business question, **no** Fabric IQ acceptance. Do not require an instructor
Fabric workspace/account.

## 7. Work IQ — only approved M365 work context

Reference: [Microsoft Work IQ CLI](https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/work-iq/cli).
The page originally inspected on 2026-11-04 lists Node.js, admin consent,
a Copilot Studio usage-billing plan and user assignment. Verify current
license/pay-as-you-go/tenant requirements **for the actual route**. Neither
"everyone needs M365 Copilot" nor "always free" is a safe blanket claim.

Optional demonstration only with approved customer identities/context:

1. The customer operator selects a supported Work IQ CLI build and prepares
   it in isolation per policy, not an unapproved global installation.
2. Customer authorized owners handle applicable terms, consent and billing
   outside the core exercise. This repo grants no consent and does not ask
   facilitators to accept terms on the customer's behalf.
3. Use an approved synthetic test source, e.g. a meeting about order priority.
4. Execute an actual authorized `workiq ask -q "..."` or approved MCP request;
   verify sources and the user's authorized context.
5. Call it a **separate Work IQ demonstration**. It is not automatically a
   core-agent tool without another supported connection.
6. Keep real emails/people/results out of the repo/public screenshots; do not
   enable unchecked Work IQ write tools.

**Offline alternative:** discuss "Which work context is missing?" Never present
invented email as real Work IQ output or require an instructor M365 account.

## 8. Final evidence question

"Which service was actually called, with which identity and source, and which
integration is only planned?" If unanswered, that IQ integration remains
**unverified / NOT_RUN**, regardless of offline test success.
