# Lab 00 — Configure and verify your customer access

**15 minutes · 00:30–00:45 · Outcome:** local tools ready; own-customer cloud
access verified or a specific `BLOCKED` item with customer owner/action.
[Agenda](../AGENDA.md) · [Next](01-portal.md)

Facilitators actively guide account/directory/subscription choice, new customer
resource/project/model setup where needed, scoped access and error diagnosis
in **your own browser and terminal**. Customer admins perform approved privileged
creation, IAM, consent and billing; guidance gives no extra authority and needs
no facilitator tenant invite. Never share passwords, MFA codes, tokens, exports
or instructor accounts/resources. An approved private one-to-one view of your
own screen is optional; do not expose credentials to a group.

Complete bootstrap as prework where possible. Bring your own customer Entra
sign-in/MFA, an **approved active own Azure subscription**, budget owner and a
reachable authorized customer admin. Corporate email/M365 access alone is not
an Azure entitlement. Full bootstrap may take **60–90 minutes or more plus
organizational lead time**; the day-of checkpoint cannot guarantee resolution
of first-time approval, permission, quota or network issues. Arrange a separate
clinic/follow-up if needed. No purchase, terms acceptance, directory migration
or security-policy bypass is part of this guide.

## Customer bootstrap before the workshop

These are instructions for your **authorized customer operator**, not actions
automatically performed by this repository. An authorized solo learner may
also be the operator. Existing approved customer resources may be reused only
after the owner verifies compatibility, access, capacity, data boundary, costs
and cleanup dependencies. Otherwise follow this from-zero route.

### A. Approve scope and environment

1. Customer owners approve subscription/billing, Foundry Agent Service and a
   model supporting **Responses + function calling + File Search** in the actual
   region/version/deployment type, with sufficient quota. No model is universally
   available; `gpt-5.4-mini` is a public sample example, not a guarantee.
2. Approve model processing geography (regional/data-zone/global), resource/
   backing-data locations, data/trace retention and synthetic-only uploads.
   A global deployment need not process within the resource's region.
3. Approve model/File Search/storage/tool/monitoring costs and a named person
   who can stop spending. Set budget alerts; **alerts are not a hard spending cap**.
   The customer alone decides purchasing, marketplace offers, terms and consent.
4. Check Azure Policy, allowed offers, quota and approved networking. IT must
   permit GitHub, PyPI/package delivery, Entra, Azure/Foundry and customer data
   endpoints through approved DNS/proxy/private-network routes. Do not disable
   TLS, public-network restrictions, Conditional Access or organizational policy.
5. Choose the supported setup with the customer architecture/admin team:
   - **Basic/managed setup:** default learning route only if service-managed
     backing storage and its networking/retention are approved. You still own
     the Foundry resource/project/deployment; no instructor service is involved.
   - **Standard / BYO private network:** customer-provisioned Storage, Search,
     Cosmos, identities/connections/networking and separate costs may be needed.
     Follow the official [environment setup](https://learn.microsoft.com/en-us/azure/foundry/agents/environment-setup)
     and [BYO resource guide](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/use-your-own-resources)
     with customer-approved parameters/templates/tools. This Pro-Code workshop
     does not supply or execute enterprise infrastructure automation. If policy
     requires Standard, Basic is not an equivalent workaround; mark `BLOCKED`
     until the approved architecture is ready.

### B. Create a dedicated customer resource group

1. Sign in to <https://portal.azure.com> using your **own customer identity**,
   complete MFA and verify the customer directory in the account menu.
2. Open **Subscriptions** and the approved **active customer subscription**.
   Ask the customer admin to confirm private IDs if display names are ambiguous.
3. The customer operator verifies relevant creation/provider permissions;
   project Foundry User is insufficient. See [roles](../SECURITY-COSTS.md).
4. If required, the subscription admin opens **Subscriptions → your subscription
   → Resource providers** and registers only approved required providers:
   normally `Microsoft.CognitiveServices`; monitoring may need `Microsoft.Insights`
   and `Microsoft.OperationalInsights`; Standard may need `Microsoft.Storage`,
   `Microsoft.Search` and `Microsoft.DocumentDB`. Wait for **Registered**.
   This does not bypass policy/quota or grant data actions.
5. Open **Resource groups → Create**. Explicitly select the approved subscription
   and a **new unused dedicated name**, e.g. `rg-orderops-workshop` plus a
   customer-chosen suffix. Do not assume an existing name is safe to reuse.
6. Select the approved RG metadata region (not the model-processing region),
   add approved purpose/owner/expiry tags, then **Review + create**.
   Inspect subscription, name and location **before Create**.
7. Open the successful RG and privately record scope/ownership for cleanup.
   Denied creation goes to the customer admin, not blanket attendee Owner.

### C. Create Foundry (new), project and a compatible model

1. Open <https://ai.azure.com>, recheck your customer identity/directory and
   enable **New Foundry** if a toggle is present. Do not use classic/hub projects.
2. In the project picker choose **Create new project**. Enter a new project
   name, e.g. `orderops-workshop` with an unused customer-chosen suffix.
3. Open **Advanced options** and explicitly select the approved subscription,
   **new dedicated RG**, region and **new** parent Foundry resource with a new
   globally unique customer-chosen name. Inspect any automatically chosen
   resource, deployment/model offer, networking and charges before submission.
4. If the form creates a parent automatically, verify its proposed name/scope.
   If required choices cannot be reviewed, cancel and use the customer's
   approved Azure portal **Create a resource → Microsoft Foundry** form, then
   create the new project under it. If no correct route is available, `BLOCKED`;
   do not accept unknown defaults or switch to classic.
5. Keep approved Entra/managed identities and network design. After customer
   review choose **Create project** / final create. Wait for readiness and
   **Succeeded** in Azure RG **Deployments**; inspect partial failures with
   the customer admin before retrying instead of creating duplicates.
6. Verify parent, project, subscription and region in **Manage → Project
   details / Resource details** and Azure. Confirm the project's own managed
   identity. A project page is not proof of correct billing scope.
7. The customer admin follows the [scoped role procedure](../SECURITY-COSTS.md#scoped-role-assignment-procedure):
   participant **Foundry User on this project**, parent **Reader** if needed;
   verify **project managed identity** model/resource access separately.
   For Standard verify actual backing roles/connections; grant human storage
   access only if the real upload path needs it. Foundry User alone cannot
   create/manage deployments; Owner/Contributor alone lacks Foundry data actions.
8. The customer model operator opens **Models + endpoints** / the deployment
   view under **Build**, chooses **Deploy model / Deploy base model**, and
   selects an actually eligible Responses/function/File-Search-compatible
   model **and version**, approved geography/type and quota.
9. Give it a new deployment name. Review the price, capacity, filters and offer
   before **Deploy**; do not weaken safety settings or accept terms without
   customer approval. Wait for deployment success and record the **deployment
   name**, not just the catalog model name. If the project wizard already
   deployed a model, verify it before reuse rather than deploying twice.
10. With the participant's own sign-in open **Build → Agents**. Confirm scoped
    authoring access after propagation. An admin-only success is not proof.
    Prefer individual projects; intentional customer-team sharing requires
    explicit approval of the common data boundary and inherited access.

**Bootstrap checkpoint:** customer-approved scope, roles, project identity,
actual deployment/version/quota, budget/retention and cleanup owner recorded
privately in a customer-approved location. No instructor endpoints, IDs, key
or tenant access is needed. No claim is made that this update tested Azure.

## 1. Open the project and terminal — 3 minutes

1. Open VS Code → **File → Open Folder** → `CloudDays-Foundry-Agent-Hackathon`.
2. Select **Terminal → New Terminal** and the **PowerShell** profile.
3. All paths below are relative to the repository, not its parent. Check:

   ```powershell
   Get-Location
   python --version
   az version
   $env:PYTHONUTF8 = "1"
   ```

**Expected:** Python ≥3.11, Azure CLI available, correct working folder, no
credential output. Use `py -0p` to find an installed Python if `python` opens
the Store, e.g. `py -3.14 -m venv .venv`. Missing tools go to customer IT;
continue offline learning while access remains blocked.

## 2. Install locally and check — 7 minutes

1. Run:

   ```powershell
   .\scripts\bootstrap.ps1
   ```

2. If script execution is blocked, do not change organization-wide policy.
   Run individual commands (create `.venv` only if absent):

   ```powershell
   if (-not (Test-Path .venv)) { python -m venv .venv }
   .\.venv\Scripts\python.exe -m pip --disable-pip-version-check install -r requirements.txt
   .\.venv\Scripts\python.exe -m pip check
   .\.venv\Scripts\python.exe -m orderops preflight --offline
   ```

3. **Ctrl+Shift+P → Python: Select Interpreter → Enter interpreter path**:
   select `.venv\Scripts\python.exe`.
4. Run core tests:

   ```powershell
   .\.venv\Scripts\python.exe -m unittest discover -s tests -v
   ```

**Expected:** pinned `azure-ai-projects 2.10.0`, `azure-identity 1.27.0`,
`openai 3.42.1`; `No broken requirements found`; core tests green. The separate
starter checks remain intentionally red until Lab 03. Offline preflight reports
**Config/Credential/Project/Model: NOT_RUN**; packages/imports do not prove cloud
permissions or availability.

**Recovery:** approved proxy/CA route with IT, never disable TLS. Use a fresh
compatible `.venv` for Python/wheel conflicts; do not swap SDK pins silently.
Choose the correct interpreter for 1.x/2.x mix-ups.

## 3. Verify configuration, identity, project and model — 5 minutes

This checkpoint assumes bootstrap/local installation are ready. If they are
not, facilitators start diagnosis and record the customer-owned follow-up,
rather than promising all creation within five minutes.

1. In Foundry verify your own customer directory, subscription, project and
   deployment. Copy **Project endpoint** from the overview:
   `https://…services.ai.azure.com/api/projects/…` or documented `…ai.azure.com`
   variant, not a hub connection string or `openai.azure.com` resource endpoint.
2. Copy the actual **deployment name** from **Models + endpoints**.
3. Create `.env` only if absent, then edit locally:

   ```powershell
   if (-not (Test-Path .env)) { Copy-Item .env.example .env }
   code .env
   ```

4. Replace the three placeholders with **your own approved customer** project
   endpoint, deployment and unused team-unique agent name, e.g. `orderops-team07`.
   No keys. Optionally set **one** of `AZURE_TENANT_ID` or `AZURE_SUBSCRIPTION_ID`,
   not both (Azure CLI token-selector limit). An exact subscription selector
   disambiguates multiple signed-in accounts without changing the global default.
   A matching directory alone is not proof of subscription access.
5. Sign in explicitly using your own identity in the approved directory, then
   privately inspect the target account and compare it with the portal:

   ```powershell
   az login --tenant "YOUR-CUSTOMER-TENANT-ID"
   az account show --subscription "YOUR-CUSTOMER-SUBSCRIPTION-ID" --query "{subscription:name,id:id,tenant:tenantId,user:user.name}" -o table
   ```

   Replace placeholders privately. Do not print tokens or run `get-access-token`.
   If `.env` has no subscription selector, the default CLI account must already
   match the intended subscription; if necessary deliberately select your own
   approved target with `az account set --subscription "YOUR-CUSTOMER-SUBSCRIPTION-ID"`.
   This user command changes the CLI default; **the application never does**.
   Tenant-only selection cannot disambiguate subscriptions; verify both.
6. With customer cost approval run the explicit **real model probe**:

   ```powershell
   .\.venv\Scripts\python.exe -m orderops preflight --allow-cloud
   ```

**Expected:** explicit `AzureCliCredential` identity, reachable customer project,
matching deployment and completed small Responses probe (up to 512 output
tokens; real charges possible). No DefaultCredential fallback.
Function calling/File Search are only verified by Lab 02 upload/indexing/smoke:
both files **completed**, actual citation/source opened and checked.

**Checkpoint:** record your own evidence as `PASS`, `BLOCKED` or `NOT_RUN`,
with next action/customer owner; no public IDs/screenshots. Until you execute
it, customer end-to-end acceptance stays **NOT_RUN**.

- **401 / CredentialUnavailable:** correct own sign-in/directory; never use an
  instructor/admin login instead.
- **403:** customer admin inspects the exact denied action, human/project identity
  and scope, waits for propagation; no speculative Owner escalation.
- **Missing deployment / 400:** correct name/model compatibility with customer
  model operator, not automatic fallback.
- **429:** stop; designated customer quota/budget owner diagnoses capacity.
- **Unresolved after checkpoint:** record `BLOCKED` + action/customer owner,
  arrange setup clinic/follow-up, use [offline learning](../INSTRUCTOR.md).
  Approved observation of an own-customer teammate with separate accounts is
  possible, but does not pass individual cloud acceptance. No instructor fallback.

`.env` and `.local` are Git-ignored, **not automatically excluded from OneDrive**.
Use a customer-approved nonsynchronized working folder when required. Never
copy account details, endpoints, private logs or credentials into public files.
