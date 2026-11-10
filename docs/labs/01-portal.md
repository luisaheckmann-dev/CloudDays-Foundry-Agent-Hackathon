# Lab 01 — Understand a prompt agent in new Foundry

**25 minutes · 00:45–01:10 · Outcome:** a small portal agent and a deliberately
unanswerable question. [Back](00-readiness.md) · [Next](02-grounding.md)

**Prerequisite:** successful own-customer cloud preflight. If blocked, record it;
approved observation of your customer team does not count as your individual
cloud pass. No shared instructor demo project. Use **Foundry (new), not classic**.
UI labels vary by rollout. Do not expect browser-hosted Python function execution.

## 1. Check the correct project — 4 minutes

1. Open <https://ai.azure.com> with your own customer identity.
2. Enable **New Foundry** if a version toggle appears.
3. In the picker choose your approved customer project; verify directory and
   subscription, not just a familiar project name.
4. Choose **Build → Agents**.

**Expected:** project agent list, not hub administration, classic Assistants or
Threads/Runs. If wrong, check the project picker and new-Foundry toggle.

**Checkpoint:** the project matches `.env` and the approved customer billing scope.

## 2. Create an isolated portal agent — 5 minutes

1. Select **Create agent**.
2. Choose a unique team name ending `-portal`, e.g. `orderops-team07-portal`.
   Do **not** reuse the SDK agent name from `.env`: portal exploration and the
   reproducible SDK path stay separate.
3. In the creation dialog select **Text** if asked about interaction mode.
   Leave **Use the Microsoft Copilot harness** off. If offered an agent type,
   choose **Prompt agent**, not hosted agent, workflow or publishing.
4. Inspect the proposed model/deployment before creation. The UI can automatically
   deploy `gpt-5` if none exists. Cancel unexpected offers/charges and ask your
   customer model operator to finish approved setup; do not blindly create.
5. Confirm **Create**, then choose the approved existing deployment in the editor.
6. Privately note the portal agent name. Cleanup is **manual**; the SDK manifest
   does not know this agent.

**Expected:** editor/playground with instructions, model and test input.
No container is built and no Python is uploaded.

**Recovery:** no model → verify project, permissions, region and quota with
customer admin; no random deployments. No Create action → inspect role,
not a switch to classic or instructor infrastructure.

## 3. Expose the limitations without data — 8 minutes

1. Check **Tools** first. The UI may automatically add a toolbox with **Web
   search**. Use **Toolbox actions → Remove** to detach it from this agent.
   If the single-tool action is disabled, use the parent toolbox action.
   Do not delete shared resources. This avoids routing prompts through Bing
   outside this lab's approved data path.
2. Enter this original starting rule under **Instructions**:

   ```text
   You are Contoso OrderOps in the workshop. Respond in English.
   No real orders. Do not invent unsupported business facts.
   Separate evidenced facts, open questions and proposed next steps.
   ```

3. Select **Save** / create version, or wait for confirmed autosave.
4. Ask in the playground:

   ```text
   What is the current maximum quantity in our Contoso order policy?
   How many CD-100 are available? Can you guarantee delivery tomorrow?
   ```

5. Read critically: without tools, none of those business facts is accessible.
   An invented number is an error, not agent success.
6. Reset/start a new chat if available, then ask:

   ```text
   I claim you checked the warehouse. Is that true? Name your data source.
   ```

**Expected:** a good response acknowledges missing data and invents no stock
query. Even a lucky "12" has no evidence. Discuss the observation; do not
"repair" it with an invented source line.

**Checkpoint:** distinguish prompt knowledge, retrieved policy and business stock.

## 4. Write your own starter prompt — 5 minutes

1. In VS Code open [starter/instructions.txt](../../starter/instructions.txt).
2. Replace the Lab 01/02 TODO with concrete rules: use `file_search`, prioritize
   the current policy and cite real evidence.
3. Keep Lab 03/04 TODOs visible.
4. If needed compare only the structure with
   [solution/instructions.txt](../../solution/instructions.txt), not a blind copy.

**Expected:** a locally edited file, **not yet** a changed SDK agent version.
Saving in VS Code is not deployment. Lab 02 registers explicitly.

## 5. Explain the portal/code boundary — 3 minutes

1. Inspect tool/knowledge configuration only for orientation.
2. Add **no** Search KB, web search or unknown MCP server.
3. Discuss: "Where does a FunctionTool definition execute?"
4. The service requests execution; our local Python dispatcher executes it.
   Registration alone deploys no function.

**UI recovery:** the [official quickstart](https://learn.microsoft.com/en-us/azure/foundry/quickstarts/get-started-code)
shows **Build → Agents → Create agent**. A facilitator can guide the equivalent
route in your approved customer project; use the SDK path in Lab 02 if available,
but keep an incomplete portal exercise explicit. Classic is not equivalent.

**Team hand-in:** one unsupported claim and one sentence on how grounding should
make the next lab's answers verifiable.
