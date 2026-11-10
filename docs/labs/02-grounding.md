# Lab 02 — File Search, index status, versions and real citations

**30 minutes · 01:10–01:40 · Outcome:** a versioned, file-grounded agent response.
Then **10-minute break**. [Back](01-portal.md) · [Next](03-tools.md)

**Prerequisite:** own-customer `.env`, identity/access and successful cloud
preflight. Commands run in the repo. This lab deploys **agent definition and
tool metadata**, not a hosted Python application. Customer pays cloud costs.

## 1. Inspect the synthetic evidence — 4 minutes

1. Open [current policy](../../data/policy/order-policy-2026-11.txt).
2. Identify policy ID, effective date, maximum **20**, stock limit and approval.
3. Open [archive](../../data/policy/archive-policy-2025.txt): maximum 100 is
   explicitly **withdrawn**.
4. Open [inventory](../../data/inventory.json): `CD-100` has **12**, `CD-200`
   has **3**, `CD-400` is blocked. No document supplies a delivery date.

The two policy files are indexed. The JSON snapshot stays local for Python.
The attack file in `data\adversarial` is deliberately **not uploaded**.

**Checkpoint:** you know the correct facts before asking the model.

## 2. Upload and wait for complete indexing — 8 minutes

1. In integrated PowerShell run explicitly:

   ```powershell
   .\.venv\Scripts\python.exe -m orderops upload --allow-cloud
   ```

2. Wait for **both** `[completed]` messages and `File Search ready`.
3. Privately inspect:

   ```powershell
   Get-Content .local\cloud-state.json
   ```

4. Verify two `file_ids` and a populated `active_vector_store`. Do not publish
   endpoint/IDs from this ignored customer manifest.

**Code behavior:** create a store expiring after one day of inactivity; upload
files with supported Files API `purpose="assistants"`, attach and poll status.
That purpose does **not** mean we use the classic Assistants/Threads/Runs API.
Polling max 180 seconds per file; network calls are separately bounded.

**Expected:** only completed indexing activates the store. Upload alone does
not make a file searchable.

**Recovery:**

- **403:** customer admin checks human project role and actual runtime/backing
  setup. Human Storage Blob Data Contributor only on real upload storage if needed.
- **failed/cancelled/timeout:** no pass. Retain error/manifest, diagnose, then
  [scoped cleanup](06-cleanup.md) before retry.
- **A store already exists:** reuse; deliberate rebuild requires scoped cleanup,
  not deleting ownership records and uploading duplicates.
- **Expired store:** cleanup tolerates missing objects; then upload/register again.

## 3. Register the first referenceable agent — 5 minutes

1. Deliberately use the reference for a reliable first grounding proof:

   ```powershell
   .\.venv\Scripts\python.exe -m orderops register --allow-cloud --track solution
   ```

2. Read printed name and **version**.
3. In **Build → Agents**, refresh and choose the `.env` agent, not `-portal`.
4. Select the registered version if offered; inspect model, instructions and tools.
5. If tool details are hidden, inspect [cloud.py](../../orderops/cloud.py):
   `PromptAgentDefinition` includes FileSearchTool and two FunctionTools.
6. Do not remove tools in the portal; reproducible versions come from code.

**Expected:** `Registered: … version … / solution`; manifest `active_agent`
matches. Each `register` creates a new version, not an in-place patch.

**Checkpoint:** "agent definition deployed" is correct; "Python deployed to
the portal" is not.

## 4. Verify a response with a technical citation — 8 minutes

1. Ask a policy-only question:

   ```powershell
   .\.venv\Scripts\python.exe -m orderops chat --allow-cloud --track solution --prompt "What is the current quantity limit? Find the policy and cite order-policy-2026-11.txt."
   ```

2. Read **FILE-SEARCH CITATIONS** beneath the response.
3. Check `filename`, `file_id` and matching manifest `file_ids`.
4. Open the source (the local current policy, plus the portal source view if
   exposed) and verify that it supports the claim: **20, OPS-2026-11**.
5. Compare a plain "Source: order-policy-2026-11.txt" with **no** annotation:
   that text alone proves no retrieval.
6. Check the integrated path:

   ```powershell
   .\.venv\Scripts\python.exe -m orderops smoke --allow-cloud --track solution
   ```

**Expected:** real response, known citation annotation and successful local
read-only inventory function under **your own customer identity**. Smoke asks
for no drafts and offers no write gate. Passing proves this integration
structure, **not** all semantic quality, every model case or real IQ.
Record actual own-identity evidence; until executed, acceptance is `NOT_RUN`.
If blocked, record action/customer owner; admin/teammate success is not your pass.

**Recovery:** empty citations → explicit File Search request, correct store,
version and ingestion status; never add a fake citation afterward.
`incomplete` → customer operator checks reasoning/output needs, budget and
compatible approved deployment; repeat preflight/register/smoke deliberately.

## 5. Prepare starter and version switching — 5 minutes

1. Add current/archive policy and missing-delivery rules to your
   [starter prompt](../../starter/instructions.txt).
2. Explain to your partner: solution smoke did **not** implement your starter TODO.
3. Leave solution active for now; Lab 03 explicitly registers `--track starter`.
4. Stop every chat before the break with `exit` or `Ctrl+C`.

**Final checkpoint:** real File Search evidence is **not** a Foundry IQ KB/MCP
integration. Failed cloud smoke stays unresolved even if offline tests pass.
