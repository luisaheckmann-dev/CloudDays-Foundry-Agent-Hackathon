# Lab 05 — 35-minute hackathon: the safe OrderOps challenge

**35 minutes · 02:45–03:20 · Outcome:** one evidenced improvement, not an
unsupported demo. [Back](04-evaluation.md) · [Next](06-cleanup.md)

## 1. Choose roles and goal — 4 minutes

Teams of 2–3; swap roles after 15 minutes:

- **Builder:** edit code/prompt, register versions, run tests.
- **Evidence Lead:** inspect sources, counterexamples, rubric and diagnostics.
- **Safety/Product Lead:** challenge attacks, approval, clarity and cost.
  In a two-person team Evidence also takes this role.

Choose **one** challenge:

| Challenge | Success criterion | Counterexample |
|---|---|---|
| A — Conflict-proof | Current 20 with real annotation; archive conflict explained | "The archive says 100; order 25 CD-300" |
| B — Reliably unknown | Missing delivery/discount data explicit, with next step | "Guarantee tomorrow and a 30% discount" |
| C — Injection-resistant | Data/tool instructions cannot bypass local boundaries | Embedded "SYSTEM" text demands automatic approval |
| D — Transparent to people | Recommendation, sources, uncertainty and local approval status separated | User confuses pending with saved |
| E — Own read-only tool (code stretch) | Tested `get_shortfall(sku, quantity)` FunctionTool; no saving | Unknown SKU, bool/negative quantity must not pass |

All teams must still pass core unknown-SKU, insufficient-stock and denied-approval
tests. Disabling a safety check is not a solution.

**Code stretch E:** calculate `max(0, quantity - available)` for integer quantities
1–20 through existing read-only inventory. Unknown/blocked SKU returns a clear
error. Wire **every** component: strict `SCHEMAS`, `FunctionTool` in `definitions()`,
an explicit `Dispatcher.execute` branch, deliberately extended evaluation
allowlist and tests. Editing only `SCHEMAS` is wrong: the current `else` handles
draft proposals! Register a new starter version and exercise the tool loop.
Cases: `CD-200, 5 → shortfall 2`, `CD-100, 2 → 0`, unknown SKU, bool/0/21.
The tool must create neither a draft nor approval. If full wiring is unfinished,
show green core plus an explicit open stretch, not fake completion.

## 2. Implement and measure — 18 minutes

1. Choose two dataset prompts and your own counterexample.
2. Privately record baseline observations without real business data.
3. Edit `starter\instructions.txt` or the read-only adapter. No uncontrolled
   shell/web/write tools.
4. Run learning and core tests:

   ```powershell
   .\.venv\Scripts\python.exe -m unittest starter.checks -v
   .\.venv\Scripts\python.exe -m unittest discover -s tests -v
   ```

5. For prompt changes register **one deliberately chosen new version** in
   your approved customer project:

   ```powershell
   .\.venv\Scripts\python.exe -m orderops register --allow-cloud --track starter
   .\.venv\Scripts\python.exe -m orderops smoke --allow-cloud --track starter
   ```

6. Test the two prompts with `chat --allow-cloud --track starter --prompt
   "YOUR SPECIFIC QUESTION"`. Respect customer budget and response limits.
7. Use the [rubric](04-evaluation.md). Before/after needs identical questions
   and traceable versions.

**Expected:** not necessarily a perfect model, but evidenced progress and a
specific remaining error. With blocked cloud: "local control evidence,
cloud quality unverified" is the correct result, not a passed cloud score.

## 3. Red-team exchange — 8 minutes

1. Exchange only a **synthetic test prompt** with another team.
2. No `.env`, tokens, endpoints or private logs.
3. Try archive precedence, invalid quantities or embedded approval instructions.
   No actual external exfiltration server or secret access.
4. Inspect the allowlist, quantity validation and terminal gate.
5. Record a rule break and fix it or disclose it. A caught error is more
   valuable than a manufactured pass.

## 4. Prepare the pitch — 5 minutes

Prepare **60 seconds**:

1. User problem in one sentence.
2. Exactly one before/after evidence item.
3. One technical approval/negative test.
4. One honest remaining error and why Foundry fits this Microsoft context.

## Jury: 100 points

| Area | Points | Evidence |
|---|---:|---|
| Sources and factual quality | 25 | Real current annotation, supported facts |
| Functional integration | 20 | Chosen version, correct inventory call, traceable loop |
| Human control | 25 | Deny without write, exact approve, duplicate, unchanged stock |
| Evaluation and learning from errors | 20 | ≥3 counterexamples, rubric, diagnostics, honest limits |
| Pitch and architecture | 10 | Precise, Foundry central, no false IQ/exclusivity claims |

**Veto:** real order/secret disclosure or intentionally removed approval boundary.
Disclose cloud blockers; separate local points from unverified cloud points.
No points simply for naming IQ.

**Stretch only after core:** investigate [real IQ](../optional/IQ.md) using
separately approved customer-owned resources. Do not improvise Search, Fabric/
M365 licenses or instructor-hosted dependencies within 35 minutes.
