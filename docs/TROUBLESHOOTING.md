# Recovery card: diagnose before reinstalling

[Home](../README.md) · [Readiness](labs/00-readiness.md)

**Rule:** a failure exit code is a failure, not an automatic offline pass.
Share only sanitized synthetic error details; never post `.env`, tokens or private
logs. Facilitators guide; customer admins perform approved privileged repairs.

| Symptom | Precise recovery |
|---|---|
| Wrong working folder / `No module named orderops` | Open the repo in VS Code; `Get-Location`; `.\.venv\Scripts\python.exe -m orderops --help`. Do not run from the parent folder. |
| Missing `python` / Store opens | `py -0p`; choose an installed 3.11+ version and create `.venv` with it. |
| PowerShell blocks `.ps1` | Use individual Lab 00 commands; no global execution-policy change. |
| `ModuleNotFoundError azure...` | Select `.venv`; `.\.venv\Scripts\python.exe -m pip install -r requirements.txt`, then `-m pip check`. |
| Mixed SDK 1.x/2.x / old OpenAI signatures | `-m pip show azure-ai-projects openai azure-identity`; install pinned requirements in the same `.venv`. |
| Corporate proxy / TLS | Customer IT supplies approved network/CA configuration; never disable certificate checks. |
| No active subscription, approval or admin | Record `BLOCKED` with customer owner/action; schedule clinic/follow-up. Corporate email is not Azure entitlement; no instructor fallback or new purchase in the lab. |
| Resource/provider creation denied | Customer bootstrap operator checks subscription actions, registration and policy; project Foundry User is not management authority. |
| Standard/private network required | Customer architecture/admin team provisions the approved backing resources, identities and routing. Basic/public access is not a policy workaround. |
| `.env` placeholder / rejected URL | Use own customer project `/api/projects/NAME`, actual deployment name, unused unique agent name. No keys. |
| Unexpected project despite `.env` | Privately inspect relevant `FOUNDRY*` shell variables; shell values override `.env`. Deliberately correct obsolete settings/open a new terminal; do not publish output. |
| CredentialUnavailable / 401 | Explicit own `az login --tenant "YOUR-CUSTOMER-TENANT-ID"`; compare intended subscription using `az account show --subscription "YOUR-CUSTOMER-SUBSCRIPTION-ID"`. Never use admin/instructor credentials. |
| CLI accepts only one selector | Set either `AZURE_TENANT_ID` or `AZURE_SUBSCRIPTION_ID`, not both. Exact subscription helps disambiguate signed-in accounts without application changes to the CLI default. Tenant match alone is insufficient. |
| 403 project/agent | Customer admin verifies human Foundry User on the project, parent Reader if needed, project runtime identity and exact denied action; allow propagation. No blanket Owner. |
| 403 upload | Check actual File Search setup/runtime backing access; human Storage Blob Data Contributor only if the real upload path requires it. |
| Deployment not found | Check own project and **deployment name**, not catalog model name; customer model operator verifies availability, then preflight. |
| 404 `agents` / API path | Use Foundry (new), not hub connection strings/classic; SDK 2.10.0 and project endpoint. |
| 400 tool/model support | Customer operator verifies Responses + function calling + File Search for actual version/region/deployment; choose approved compatible model, then preflight/register/smoke. |
| 429 / quota | Stop loops. Customer quota/budget operator checks Retry-After/capacity; manual retry later or deliberate approved deployment change. |
| Timeout/network | Customer IT checks endpoint/DNS/private route. No endless retry; inspect owned IDs for failed actions. |
| Ingestion not completed | Check status/storage/file; do not register. Retain manifest, scoped cleanup, retry only after repair. |
| `A store already exists` | Reuse it or scoped cleanup for deliberate rebuild; do not delete the manifest and forget cloud assets. |
| Store expired | One-day inactivity expiry; cleanup, upload again, register a new version. |
| Missing citation | Explicit policy/File Search question; correct store, ingestion and active version. Plain filename is no replacement. |
| `No active starter agent` | `register --allow-cloud --track starter`. Tracks never mix silently. |
| Prompt edited, behavior unchanged | Save **and** register a new version; check printed/manifest version. |
| Starter inventory rejected | Implement the TODO in `starter\inventory.py`; `python -m unittest starter.checks -v`. |
| Tool budget exhausted | Reduce needless calls/clarify prompt. No approval after error; do not blindly remove limits. |
| Response `incomplete` | Check output/reasoning needs and approved model choice. A runtime budget edit needs tests and a new cost estimate. |
| Approval denied | Both `--enable-local-drafts` **and** exact displayed `APPROVE <id>` required. Chat `yes`, model text and pipes are not human terminal approval. |
| Old proposal ID no longer matches | Policy content/hash is part of the ID. Translation changes it; inspect and approve only the newly displayed ID, never migrate private drafts to force a match. |
| First demo returns `duplicate` | Identical policy/SKU/quantity already saved in that DB; correct idempotency, not a real order. |
| SQLite locked | Close your DB viewers/debugger connections. Connections are explicitly closed; never stop unrelated system processes. |
| Windows/OneDrive locks `cloud-state.json` | Bounded retries handle transient locks; persistent errors remain visible. Preserve `cloud-state.new`/manifest, close own file/sync access and resume deliberately. Do not delete ownership evidence. Use an approved nonsynchronized folder for private data. |
| Debugger waits without input | Use integrated terminal, not Debug Console, for `input()`. |
| No portal traces | Monitoring target/view may be unavailable. Show local diagnostics/response IDs; this repo has no automatic OTel export. |
| Partial cleanup | Retain manifest, repair exact access/error with customer admin and repeat the same scoped command. |
| Manifest belongs to another project | Restore original configuration privately and clean only that approved scope. Never continue with foreign IDs. |

## Reproducible local health check

```powershell
$env:PYTHONUTF8 = "1"
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe -m orderops preflight --offline
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m orderops offline
.\.venv\Scripts\python.exe -m orderops evaluate --offline
.\.venv\Scripts\python.exe scripts\check_links.py
```

Only then, with actual customer access and cost approval, deliberately run a cloud
preflight/smoke. Unexecuted individual cloud acceptance stays `NOT_RUN`; a known
missing prerequisite is `BLOCKED` plus customer owner/action. Offline learning
or approved teammate observation is not an individual live verification.
