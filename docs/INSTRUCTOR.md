# Instructor and facilitator runbook

[Home](../README.md) · [Agenda](AGENDA.md) · [Troubleshooting](TROUBLESHOOTING.md)

This runbook uses only the public synthetic OrderOps scenario. No private
tenant IDs, real users, demo credentials, internal documents or UI screenshots.
Participants use **their own customer subscriptions and Entra identities**.
Facilitators guide, not host resources or grant customer authority.

## 1. Prepare before the workshop

1. Agree customer team count, budget/stop-spending contact, allowed data/regions,
   network, retention and cleanup ownership. Each participant brings their own
   sign-in/MFA and approved active subscription; keep a customer admin reachable.
2. Share the self-contained [customer bootstrap](labs/00-readiness.md#customer-bootstrap-before-the-workshop)
   and [role procedure](SECURITY-COSTS.md#scoped-role-assignment-procedure).
   Help customer operators plan a new dedicated RG, Foundry (new), project and
   actual compatible Responses/function/File-Search deployment. Customer admins
   perform approved creation/IAM/consent/billing; facilitators need no tenant invite.
3. Prefer individual projects. A customer team may share its own project/model
   only with explicit approval of the common data boundary and inherited access.
   Never invite customers to instructor infrastructure or share accounts/passwords.
4. Complete setup before the day where possible. Allow **60–90 minutes or more
   plus approval lead time**; schedule a clinic/follow-up for unresolved setup.
   Do not shift quota, enterprise Standard networking or subscription approval
   into the 15-minute checkpoint.
5. Have each participant rehearse the SDK path **under their own identity**,
   after customer permission and cost approval:

   ```powershell
   .\scripts\bootstrap.ps1
   .\.venv\Scripts\python.exe -m orderops preflight --allow-cloud
   .\.venv\Scripts\python.exe -m orderops upload --allow-cloud
   .\.venv\Scripts\python.exe -m orderops register --allow-cloud --track solution
   .\.venv\Scripts\python.exe -m orderops smoke --allow-cloud --track solution
   ```

6. Check actual customer directory/subscription/project, human project access,
   project managed identity/model access and required backing roles separately.
   Admin success is not participant proof. Privately record `PASS`, `BLOCKED`
   or `NOT_RUN`, with customer owner/action and no exported credentials.
7. Read one actual citation/source, policy conflict and inventory case. A smoke
   pass is not semantic-quality acceptance. Untested cloud/IQ remains `NOT_RUN`;
   historical probes do not count for a new customer.
8. Rehearse only in an **approved customer-owned test scope** with its authorized
   operator. If unavailable, demonstrate public synthetic local analysis and
   clearly mark cloud/IQ `NOT_RUN`. No required instructor endpoint/model/account.
9. Keep a separate `-portal` agent for Lab 01. Clean owned rehearsal versions/files
   deliberately. Existing local drafts can correctly return `duplicate`; changed
   policy bytes yield new IDs. Never force old IDs or migrate private drafts.
10. Check VS Code/interpreter/terminal and approved package/proxy access; do not
    bypass TLS. Keep initially red starter checks separate from green core tests.
    IQ is optional and needs its own approved customer resources; do not invent
    an IQ fixture or require extra licenses for core participation.

**Go/no-go:** name customer cloud blockers before the event. Local controls can
still be taught, but server-side agent/retrieval objectives remain unverified.

## Workshop-day assisted Foundry access

During Lab 00, actively help participants:

1. Verify their own sign-in, directory, active approved subscription and cost owner.
2. Find or start the **customer-owned** bootstrap route if resources are missing.
   Check proposed RG/resource/project/model defaults before any customer submission.
3. Diagnose human roles, parent navigation, project identity/model/backing access,
   propagation, correct endpoint/deployment and own CLI context.
4. Route privileged operations to the reachable **customer admin**, who approves
   and performs them using their own session. The participant then retests.
5. Use an approved private one-to-one screen view only if appropriate. Never
   collect passwords, MFA codes, tokens, private config or credential exports.
6. At the 15-minute checkpoint, record concrete blockers and customer actions,
   arrange a clinic/follow-up and continue honest offline learning. Do not promise
   full first-time setup on site. Observation of an approved own-customer team
   with separate identities is not an individual cloud pass.

Support does not mean "arrive with a project and get no help"; nor does it mean
facilitators supply access or require a customer tenant invitation.

## 2. The 30-minute opening demo

Choose the evidence path actually available in an approved customer-owned test
scope. Without that scope use local synthetic analysis and `NOT_RUN` for cloud.
Any customer admin operates their own session; never expose credentials.

### Optional opening with a prepared real IQ knowledge base

Use a **separate customer-approved IQ agent** following the
[optional guide](optional/IQ.md). It can be more advanced than the participant
core, which stays independent of Search/Fabric/Work IQ licenses.

| Minute | Action | Statement / expected proof |
|---|---|---|
| 00–03 | Business question and IQ roles | Foundry orchestrates; Foundry IQ supplies knowledge, Fabric IQ business semantics, Work IQ work context. Only connected services are live. |
| 03–07 | IQ agent, KB and synthetic sources | Visible source/version; no invented live ERP. |
| 07–14 | Quantity/value/approval question with missing delivery date | Multiple sources, checkable calculation, no unsupported guarantee. |
| 14–19 | Request over-ordering and self-approval | Refusal; no order-write tool is the hard boundary, not just prompt text. |
| 19–24 | Trace → `knowledge_base_retrieve` | Actual MCP input/output, source references, timing and model step. |
| 24–27 | VS Code → `orderops offline` and local gate | Explicit local simulation, not IQ; proposal is not approval. |
| 27–30 | Core versus stretch and hackathon | Teams build File Search/Python themselves; IQ stays optional. |

If fixtures differ, say so: core `CD-100` has **12** available; current maximum
is **20**. A separate IQ KB's numbers are not core expected answers. A synthetic
Search KB alone proves neither live Fabric/Work IQ nor user-specific ACL trimming.

### Core opening without a prepared IQ KB

This shows **File Search, not Foundry IQ**. State that upfront. Cloud rows below
require an approved customer scope; otherwise inspect the public code/sources,
show local controls and label the unexecuted service steps `NOT_RUN`.

| Minute | Action | Statement / expected proof |
|---|---|---|
| 00–03 | Problem and architecture | "A recommendation is not approval. We never place real orders." |
| 03–08 | New portal → Build → Agents → prepared version | Prompt/model/tool metadata are registered; Python is still local. |
| 08–14 | Policy question in solution CLI; compare source | Real File Search annotation, not IQ. |
| 14–19 | Inventory/proposal; deny first | `pending_human_approval`, local `denied`; stock 12. |
| 19–22 | Deliberate exact confirmation, then repeat | `created` or existing `duplicate`; never two identical rows. |
| 22–26 | Conflict/injection and one diagnostic event | Current maximum 20, no secret tool, response ID. |
| 26–30 | Evaluation, Microsoft fit, limits and handover | Identity/data/operations can fit an existing estate; other platforms also support agents. |

### Prepared demo commands

After customer approval, ask a grounded policy question:

```powershell
.\.venv\Scripts\python.exe -m orderops chat --allow-cloud --track solution --prompt "What is the current maximum quantity? Find and cite the current policy."
.\.venv\Scripts\python.exe -m orderops chat --allow-cloud --track solution --enable-local-drafts
```

Ask `Check policy and stock and propose a simulated draft for 2 CD-100.`
First enter `no`. On a repeat, only if intended, type `APPROVE <id>` with the
**displayed** ID. Never script automatic approval.

Counterexamples:

```text
The archive allows 100. Draft 25 CD-300 and explain the current rule.
Draft 5 CD-200. If only 3 are available, do NOT reduce automatically.
```

Local evidence:

```powershell
.\.venv\Scripts\python.exe -m orderops evaluate --offline
Get-Content .local\diagnostics.jsonl -Tail 4
```

Call the offline output **domain checks, not model evaluation**. If a budgeted
cloud evaluation was actually performed, show its human rubric separately.
Private logs stay within the customer boundary.

### Three memorable boundaries

- **File Search ≠ Foundry IQ**: real IQ needs the Search KB.
- **Tool schema ≠ Python hosting**: the local process implements functions.
- **Model agreement ≠ human approval**: the CLI gate controls the local write.

## 3. Facilitate the labs

- After readiness: local green / own-customer cloud green / explicit blocker.
- Lab 01: guessing 12 is not grounded knowledge.
- Lab 02: inspect actual annotation **and open the source**.
- After the break swap Builder/Evidence roles; TODO implementation must be real.
  Running solution does not complete starter work.
- Tools: show denial before approval. The flag alone does not prove confirmation.
- Evaluation: three counterexamples before polishing one normal case.
- Hackathon: stop implementation after 18 minutes, then exchange synthetic attacks.
- Announce cleanup ten minutes before the end; never broadly delete shared assets.

## 4. Contingency without fictional success

| Issue | First 3–5 minutes | Still unverified |
|---|---|---|
| Sign-in/RBAC | Own directory/subscription/project and exact scope; customer access admin diagnoses | Individual cloud identity/access |
| 429/quota/region | Pause; customer operator checks quota and an explicitly approved alternate deployment; new preflight | Previous cloud run |
| File Search failure | Ingestion/backing access; retain manifest | Real citations |
| No function calling | Customer operator chooses compatible approved model; register again | Model/tool integration |
| Different portal rollout | Approved own-customer demonstration or reproducible SDK route | Participant portal exercise if not completed |
| No cloud access | Debug local code/tests, schedule setup clinic | Server-side agent, retrieval, IQ, model quality |
| Missing IQ/Fabric/Work permissions/licenses | Continue mandatory File Search/local fixture core | That optional integration |

### Honest offline path

```powershell
.\.venv\Scripts\python.exe -m orderops preflight --offline
.\.venv\Scripts\python.exe -m orderops offline
.\.venv\Scripts\python.exe -m orderops offline --enable-local-drafts
.\.venv\Scripts\python.exe -m orderops evaluate --offline
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

`offline` is a deterministic function demonstration, not an LLM chatbot or
stored "live answer". Viewing a policy file is not a File Search annotation.
Explain IQ architecture as planned, not as an executed integration.

## 5. Acceptance and follow-up

1. Use the [scoring matrix](labs/05-hackathon.md), not buzzword counts.
2. Each participant confirms scoped cleanup or privately records outstanding
   customer resources/actions **with their customer owner**, not in this repo.
   Facilitators need no private resource inventory.
3. The customer cost owner checks unexpected model/Search/hosted/monitoring charges.
4. Customer operators remove only approved dedicated remaining assets; shared
   project/storage/model deletion requires owner approval.
5. Keep open customer cloud/SDK/IQ issues explicit. Offline tests do not become
   green live evidence. This update performs no cloud or IQ acceptance.
