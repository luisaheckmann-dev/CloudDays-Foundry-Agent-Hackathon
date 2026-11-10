# Lab 03 — Python tools and a real local approval boundary

**35 minutes · 01:50–02:25 · Outcome:** your read-only adapter and a debugged,
technically separated SIMULATION write path.
[Back](02-grounding.md) · [Next](04-evaluation.md)

**Prerequisite:** Lab 02. Cloud variants need own-customer access/deployment.
The approval controls can also be proved offline. Change `starter` and targeted
challenge tests/prompts, never disable safety controls to manufacture a pass.
This local prototype is not enterprise Entra authorization or immutable audit.

## 1. Turn an intentionally red learning check green — 7 minutes

1. Open [starter/inventory.py](../../starter/inventory.py).
2. Run the **separate** learning checks:

   ```powershell
   .\.venv\Scripts\python.exe -m unittest starter.checks -v
   ```

3. Both initially raise `NotImplementedError`. That is a genuine task, **not**
   a working starter.
4. Replace the TODO by calling the imported `inventory(sku)` and returning its
   unchanged result.
5. First read `inventory` in [business.py](../../orderops/business.py): no writes,
   `found=False` for unknown SKU, source/fixture metadata.
6. Repeat learning checks and core tests:

   ```powershell
   .\.venv\Scripts\python.exe -m unittest starter.checks -v
   .\.venv\Scripts\python.exe -m unittest discover -s tests -v
   ```

**Expected:** both learning checks and all core tests pass. No second stock
implementation; JSON remains unchanged.

**Recovery:** for unknown SKU, do not access `available` when `found=False`.
Keep validation errors for empty/invalid SKU; do not invent stock. Consult
[solution/inventory.py](../../solution/inventory.py) deliberately if needed.

## 2. Register starter and trace the tool loop — 7 minutes

1. Add to [starter instructions](../../starter/instructions.txt):
   get_inventory before stock advice; reject unknown SKUs; propose_order is
   only a proposal, never a claim of approval.
2. Remove the completed Lab 03 TODO; Lab 04 can remain open.
3. Register a new version after cost approval:

   ```powershell
   .\.venv\Scripts\python.exe -m orderops register --allow-cloud --track starter
   .\.venv\Scripts\python.exe -m orderops smoke --allow-cloud --track starter
   ```

4. Open `run_agent` in [runtime.py](../../orderops/runtime.py).
5. Trace `responses.create` → `function_call` → `Dispatcher.execute` →
   `function_call_output` with the **same call_id** → next Response with
   **previous_response_id**.
6. Locate versioned `agent_reference`; this is not classic Threads/Runs.

**Expected:** the model selects a FunctionTool, but **your local process** runs
Python. File Search runs in the service. Max 4 Responses, 6 local calls and 3
service-side calls per Response; no infinite loop or silent SDK retries.

**Checkpoint:** explain why registered parameters are not hosted implementation.

## 3. Set VS Code breakpoints — 8 minutes

1. Open **Run and Debug** (Ctrl+Shift+D).
2. Select **OrderOps: Cloud / Starter (costs apply!)** from `launch.json`.
3. Click left of these lines to set breakpoints:
   - [runtime.py](../../orderops/runtime.py): `output = dispatcher.execute(...)`.
   - [tools.py](../../orderops/tools.py): `proposal = propose(**args)`.
   - [business.py](../../orderops/business.py): `if not enabled or confirmation != ...`.
4. Start **F5**. The integrated terminal accepts human input.
5. Ask:

   ```text
   Check policy and stock. Propose a simulated draft for 2 CD-100.
   ```

6. At the first breakpoint, inspect **Variables**: `call.name`,
   `call.arguments`, `call.call_id`.
7. **F10** steps; **F5** continues to the next breakpoint.
8. Inspect proposal: known SKU, `quantity=2`, policy hash and deterministic ID.
9. At the terminal prompt first enter **no**.

**Expected:** the tool returns `pending_human_approval`; **nothing is saved**.
After "no", local status is `denied`. The terminal decision is not sent back
as a model parameter.

**Recovery:** use `console: integratedTerminal`, not Debug Console. If no proposal
breakpoint is hit, inspect the model request/output and ask explicitly; do not
claim a cloud pass manually. Missing starter agent → register with
`--allow-cloud --track starter`.

## 4. Prove approval, deduplication and read-only stock — 8 minutes

1. Without the gate flag:

   ```powershell
   .\.venv\Scripts\python.exe -m orderops offline --track starter
   ```

2. Inventory is read and a proposal staged, but write gate is disabled; no new
   draft is saved.
3. With the opt-in flag:

   ```powershell
   .\.venv\Scripts\python.exe -m orderops offline --track starter --enable-local-drafts
   ```

4. Read the proposal. Only if you want this **local simulation**, type `APPROVE `
   plus **exactly the displayed ID**. No hardcoded ID: policy bytes/hash, SKU and
   quantity bind it; translation changes it. Chat "yes" and piped text are not approval.
5. Repeat the same command with the same deliberate human confirmation.
6. First result: `created` (or `duplicate` if already approved). Second:
   **duplicate**, never a second identical row.
7. Inspect only your local synthetic artifacts:

   ```powershell
   Test-Path .local\drafts.sqlite3
   .\.venv\Scripts\python.exe -c "import sqlite3; c=sqlite3.connect(r'.local\drafts.sqlite3'); print(c.execute('SELECT id,payload FROM drafts').fetchall()); c.close()"
   Get-Content data\inventory.json
   ```

8. CD-100 remains **12**. No real order, reservation, inventory mutation or
   outgoing ERP transaction exists. SQLite stores only workshop simulations.

**Important:** denial must not **create** a DB, or add a row if one already
exists. Isolated tests cover both, plus tampered/stale proposals. Before any
write, code revalidates current policy hash, quantity, stock and blocked status.
Do not migrate old private drafts or force old IDs.

## 5. Negative cases and finish — 5 minutes

1. In the cloud starter chat:

   ```powershell
   .\.venv\Scripts\python.exe -m orderops chat --allow-cloud --track starter --enable-local-drafts
   ```

2. Try `5 CD-200`, `1 CD-999`, `1 CD-400` and `25 CD-300`.
3. Insufficient stock, unknown SKU, block and current maximum each prevent a
   valid proposal. None should reach a human approval prompt.
4. Exit with `exit`. A model making no tool call performs no write; that is
   safe but not yet proof of good functional integration.

**Hand-in:** show denial and idempotent duplicate, and name the breakpoint at
the trust boundary. Do not manipulate fixtures to permit invalid quantities.
See [architecture](../ARCHITECTURE.md).
