# Public sources and validation scope

Original source/SDK inspection: **2026-11-04**. English/customer-access update:
**2026-11-10**, locally validated without Azure operations. Code, business data
and lab text are original workshop material. Linked samples are references,
not copied source distributions. Availability, portal labels and preview
contracts can change; verify them for the actual customer environment.

## Core contract

| Source | Used for |
|---|---|
| [Foundry SDK Quickstart (new)](https://learn.microsoft.com/en-us/azure/foundry/quickstarts/get-started-code) | `AIProjectClient`, `PromptAgentDefinition`, `agents.create_version`, Portal Build → Agents |
| [Function calling](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/tools/function-calling) | Local execution, FunctionTool, function_call_output |
| [File Search](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/tools/file-search) | Files, vector stores, ingestion, tool and additional costs |
| [SDK function sample](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/agents/tools/sample_agent_function_tool.py) | Responses continuation through previous_response_id |
| [SDK File Search sample](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/agents/tools/sample_agent_file_search.py) | Project OpenAI client, FileSearchTool, agent_reference |
| [azure-ai-projects release](https://pypi.org/project/azure-ai-projects/2.10.0/) | Installed package 2.10.0 |
| [azure-identity release](https://pypi.org/project/azure-identity/1.27.0/) | Installed package 1.27.0 |
| [openai release](https://pypi.org/project/openai/3.42.1/) | Installed package 3.42.1 |

The three SDKs and transitive dependencies are pinned in
[requirements.txt](requirements.txt). Original test system: Windows, CPython
**3.14.2**. Python 3.11+ is the target; other Python/OS combinations were not run.
Installed signatures were inspected with `inspect.signature` and model docstrings:

```text
AIProjectClient(endpoint, credential, *, allow_preview=False, **kwargs)
AIProjectClient.get_openai_client(*, agent_name=None, **kwargs)
AgentsOperations.create_version(agent_name, *, definition, metadata=None, description=None, ...)
AgentsOperations.get_version(agent_name, agent_version, ...)
AgentsOperations.delete_version(agent_name, agent_version, ...)
DeploymentsOperations.list(*, model_publisher=None, model_name=None, ...)
AgentReference: type='agent_reference', name, version
FunctionTool: name, parameters, strict, description
FileSearchTool: vector_store_ids, max_num_results
Responses.create: input, previous_response_id, max_output_tokens, max_tool_calls,
                  parallel_tool_calls, extra_body, ...
```

Projects client API version: **v1**. This repository uses the project OpenAI
client and **versioned** `extra_body.agent_reference`, not an agent-bound
preview endpoint. In 2.10.0, `get_openai_client(agent_name=...)` explicitly
requires `allow_preview=True`; some public quickstarts may differ. Do not copy
that snippet unchanged. Historical model and read-only Responses/MCP probes
against a separate IQ agent do not validate the customer-owned core path.
Customer cloud access, File Search/functions and IQ remain **NOT_RUN** until
tested in the intended environment with the actual participant identity.

## Customer setup and authorization

- [Create Foundry resources](https://learn.microsoft.com/en-us/azure/foundry/tutorials/quickstart-create-foundry-resources)
- [Foundry role-based access control](https://learn.microsoft.com/en-us/azure/foundry/concepts/rbac-foundry)
- [Agent Service environment setup](https://learn.microsoft.com/en-us/azure/foundry/agents/environment-setup)
- [Standard setup with customer resources](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/use-your-own-resources)
- [Azure role assignment procedure](https://learn.microsoft.com/en-us/azure/role-based-access-control/role-assignments-portal)
- [Azure CLI sign-in](https://learn.microsoft.com/en-us/cli/azure/authenticate-azure-cli-interactively)
- [AzureCliCredential](https://learn.microsoft.com/en-us/python/api/azure-identity/azure.identity.azureclicredential)
- [Azure budgets](https://learn.microsoft.com/en-us/azure/cost-management-billing/costs/tutorial-acm-create-budgets)

The self-contained [readiness guide](docs/labs/00-readiness.md) and
[security procedure](docs/SECURITY-COSTS.md) describe approved customer bootstrap,
separate human/runtime identities and scoped access. Official role definitions
and the customer's policies govern actual authority.

## IQ, architecture and teaching references

- [What is Foundry IQ?](https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/what-is-foundry-iq)
- [Create a knowledge base](https://learn.microsoft.com/en-us/azure/search/agentic-retrieval-how-to-create-knowledge-base)
- [Connect a Foundry agent to a KB](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/foundry-iq-connect)
- [Official IQ toolbox sample 17](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/python/hosted-agents/agent-framework/responses/17-foundry-iq-toolbox)
  — `FoundryChatClient`, `FoundryToolbox`, real Search KB/MCP and model example
  `gpt-5.4-mini`; not proof of availability in every tenant.
- [Enterprise Knowledge Agent](https://github.com/microsoft/Foundry-Agent-Solution-Templates/tree/main/enterprise-knowledge-agent)
  — advanced enterprise architecture, not the required installation.
- [Microsoft IQ Samples](https://github.com/microsoft/iq-samples)
  — optional cross-product integrations; no license entitlement promised.
- [Azure-centric LangChain reference](https://github.com/fustok/langchain-azure-centric)
  — community reference, **not** a runtime dependency or official product guarantee.
- [Detailed Fabric lab style](https://github.com/customer-success-microsoft/WSPlus-Fabric-Introduction/blob/main/LabGuide_Instructor/LabGuide/Lab05_FabricDB_DS_RTI.md)
  — inspiration for numbered UI steps, checkpoints and recovery; no copied lab text.
- [Fabric IQ](https://learn.microsoft.com/en-us/fabric/iq/overview)
- [Work IQ CLI](https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/work-iq/cli)
- [Deploy a hosted agent](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/deploy-hosted-agent)

No internal documents, private tenant data, user identities or UI screenshots
are included in the participant repository. The MIT copyright notice is unchanged.
