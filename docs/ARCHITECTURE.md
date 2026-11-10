# Architecture: what actually runs where

[Home](../README.md) · [Security & Costs](SECURITY-COSTS.md)

```text
Human / VS Code / PowerShell
  │ explicit --allow-cloud + AzureCliCredential (own customer identity)
  ▼
AIProjectClient (azure-ai-projects 2.10.0, Projects API v1)
  ├─ agents.create_version(PromptAgentDefinition)
  │    ├─ Deployment (customer-chosen, no model fallback)
  │    ├─ FileSearchTool → vector store → 2 synthetic policy files
  │    └─ FunctionTool METADATA (no Python deployment)
  └─ get_openai_client() → Responses API
       ├─ agent_reference {name, version}; max. 4 Responses / request
       ├─ file_search: service-executed → file_citation
       └─ function_call → local allowlist dispatcher (max. 6 calls)
            ├─ get_inventory → read-only JSON snapshot
            └─ propose_order → validated proposal ONLY in memory
                 │ pending_human_approval ≠ saved
                 ▼
       LOCAL CLI GATE outside the model
       --enable-local-drafts AND exact APPROVE <id> in an interactive terminal
                 ▼
       .local/drafts.sqlite3 — SIMULATION, primary-key idempotent, not an order
```

## Trust boundaries

- **Model text is not an authorization decision.** The model cannot set the
  gate flag or terminal input. `save_approved` is not registered.
- The CLI denies noninteractive/piped approval; an `APPROVE` forwarded from
  model output is not human confirmation.
- `propose_order` and the write path revalidate a known SKU, integer quantity
  (not bool/float), 1–20, available stock and blocked status. The current policy
  is also enforced in domain code; production rules need central version management.
- Documents are evidence, not executable instructions. Prompt defenses do not
  prove complete injection resistance; the allowlist and code are the hard boundary.
- Inventory is a static synthetic snapshot. No ERP, reservation, subtraction or
  delivery promise exists.
- Idempotency ID hashes policy ID, **current policy file SHA-256**, SKU and quantity.
  Identical proposals under identical policy bytes produce the same row throughout
  the **local DB lifetime**. Revalidation rejects changed policy content before
  writing. Translation therefore changes IDs; always approve the displayed ID.
  Existing private drafts are not migrated. A real order API would need an
  authorized business/request ID and transaction logic.
- A local file owner can edit Python/SQLite. This gate prevents model-directed
  writes in the unchanged workshop program, not a malicious administrator.
  It is not enterprise Entra authorization, immutable audit or a multi-user backend.
- Human Azure project access, customer control-plane administration and project
  managed-identity runtime access are separate. All cloud resources belong to
  the customer; facilitator guidance grants no Azure access. See the
  [role procedure](SECURITY-COSTS.md#scoped-role-assignment-procedure).

## Executable components

| Path | Responsibility |
|---|---|
| [CLI](../orderops/__main__.py) | Explicit cloud consent, chat, smoke, separate local approval |
| [Cloud](../orderops/cloud.py) | Clients, upload/index polling, versioned registration, scoped cleanup |
| [Runtime](../orderops/runtime.py) | Responses loop with `previous_response_id` and `call_id` |
| [Domain](../orderops/business.py) | Read-only inventory, validated proposals, SQLite idempotency |
| [Dispatcher](../orderops/tools.py) | Tool allowlist, strict parameters, no dynamic execution |
| [Starter](../starter/inventory.py) / [Solution](../solution/inventory.py) | Replaceable inventory adapter; separate prompt per track |
| [Dataset](../data/evaluation.jsonl) | 10 synthetic normal/negative cases |

Each SDK agent request explicitly references a version. Registration changes
the active version in ignored `.local/cloud-state.json`. A prompt edit alone
does **not** update the service: run `register` again. Every CLI chat question
is independent; only tool continuations within that question are linked.
No unbounded conversation history accumulates.

## File Search and the three IQ terms

| Component | Actual meaning | In the core |
|---|---|---|
| File Search | Agent tool with files/vector store and citable retrieval | **Yes** |
| Foundry IQ | Azure AI Search knowledge base, agentic retrieval and knowledge sources, e.g. MCP | **No**; separate optional setup |
| Fabric IQ | Semantic business context, e.g. ontologies, semantic models, data agents | **No**; JSON is not Fabric IQ |
| Work IQ | M365 work context from collaboration, relationships and workflows | **No**; a prompt/fixture is not Work IQ |

## Why Microsoft can fit — without exclusivity claims

Foundry combines agent definitions, model deployment, tools and diagnostics.
Entra/RBAC, Azure AI Search and optional Fabric/M365 context can reduce integration
effort in existing Microsoft environments. The value is **appropriate identity,
data integration and operations**, not a claim that other platforms lack agents,
RAG, governance or human approval. AWS and Databricks also offer agent, retrieval
and evaluation components. Compare actual sources, permission propagation, region,
operating model, costs and team skills; this exercise is not a feature benchmark.

Hosted agents use a **different deployment model**: an executable service/container
with additional infrastructure. FunctionTool registration uploads no Python.
See [optional extensions](optional/IQ.md).
