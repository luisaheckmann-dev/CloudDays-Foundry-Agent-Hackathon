# Lab 06 — Pitch, scoped cleanup and final check

**10 minutes · 03:20–03:30 · Outcome:** short proof and no forgotten owned
workshop artifacts. [Back](05-hackathon.md) · [Home](../../README.md)

## 1. Pitch — 4 minutes

1. The facilitator selects 2–3 teams for 60 seconds each.
2. Show a real source and denied approval or a negative test.
3. Name the executed path: cloud prompt agent **or** local simulation.
4. Explicitly state whether real IQ KB/MCP evidence exists. Normal File Search
   must not be described as IQ. Own-customer acceptance not executed is `NOT_RUN`;
   known missing prerequisites stay `BLOCKED` with customer owner/action.

## 2. Remove only manifested SDK artifacts — 3 minutes

1. Stop chats/debuggers; no concurrent upload/register/cleanup processes.
2. Privately inspect:

   ```powershell
   Get-Content .local\cloud-state.json
   ```

3. Check own customer project endpoint, agent name and listed versions, files,
   vector stores and Responses. Cleanup deletes **only those IDs**; confirm
   their ownership and customer approval first.
4. Use the exact agent name from your own `.env`:

   ```powershell
   .\.venv\Scripts\python.exe -m orderops cleanup --allow-cloud --confirm "YOUR-EXACT-AGENT-NAME"
   ```

5. Expected: only manifested versions, Responses, stores and files removed.
   Already absent objects (404) count as removed.
6. On partial failure retain the manifest, diagnose and repeat the same scoped
   command. **Do not delete the manifest first.**

**Not deleted:** Foundry project/resource, model, Search, Storage, roles, RG,
other agents, portal agent or local drafts. One-day store expiry does not
replace cleanup; uploaded files are separately removed by this command.

**Recovery:** no manifest → perhaps only portal/offline used; do not guess IDs.
Wrong project → restore original own configuration and clean that approved scope.
403 → authorized customer admin handles the exact recorded IDs, not the shared
RG. Facilitators guide; they do not need customer roles.

## 3. Deliberately clean portal agent and local data — 3 minutes

1. Open **Build → Agents** in your customer project.
2. Find **exactly your own `…-portal` agent** from Lab 01.
3. Verify name/project, then **… → Delete** or the available version-specific
   delete action. Confirm only that owned artifact.
4. Verify manifested SDK versions are gone; unrelated versions stay.
5. Only after completed cloud cleanup, optionally remove your own local
   synthetic outputs under customer retention policy:

   ```powershell
   # Only your own local workshop artifacts, not Azure resources:
   if (Test-Path .local\drafts.sqlite3) { Remove-Item .local\drafts.sqlite3 }
   if (Test-Path .local\evaluation-results.jsonl) { Remove-Item .local\evaluation-results.jsonl }
   if (Test-Path .local\diagnostics.jsonl) { Remove-Item .local\diagnostics.jsonl }
   ```

6. On a shared machine remove your private `.env` deliberately and sign out
   using `az logout` if customer policy requires it. On your own machine follow
   your policy. Git ignore does not prevent OneDrive sync.

**Customer-owner follow-up:** inspect remaining dedicated deployments, Search
KB/indexes, Storage, Cosmos, optional hosted compute and monitoring, billing and
retention. Remove only explicitly approved dedicated assets after dependency
checks; shared resources need owner agreement. Track outstanding costs/access
with a customer owner/action. There is deliberately **no broad RG delete command**.
Deletion does not promise immediate erasure of compliance/backup copies.

**Final checkpoint:** what is the agent definition, where does Python run,
which source is real, who could write, and which cost resources remain?
