# Öffentliche Quellen und Prüfstand

Abruf und lokale SDK-Prüfung: **2026-11-04**. Code, Geschäftsdaten und deutsche
Labtexte dieses Repositories sind eigenständig verfasst. Verlinkte Beispiele sind
Referenzen, nicht als vollständiger Quelltext übernommen. Produktverfügbarkeit,
Portalbeschriftungen und Preview-Verträge können sich verändern.

## Verbindlicher Core-Vertrag

| Quelle | Wofür verwendet |
|---|---|
| [Foundry SDK Quickstart (new)](https://learn.microsoft.com/en-us/azure/foundry/quickstarts/get-started-code) | `AIProjectClient`, `PromptAgentDefinition`, `agents.create_version`, Portal Build → Agents |
| [Function calling](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/tools/function-calling) | Lokale Ausführung, FunctionTool, function_call_output |
| [File Search](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/tools/file-search) | Files, Vector Stores, Ingestion, Tool, zusätzliche Kosten |
| [SDK Function-Beispiel](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/agents/tools/sample_agent_function_tool.py) | Responses-Fortsetzung über previous_response_id |
| [SDK File-Search-Beispiel](https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/ai/azure-ai-projects/samples/agents/tools/sample_agent_file_search.py) | Projekt-OpenAI-Client, FileSearchTool, agent_reference |
| [azure-ai-projects Releases](https://pypi.org/project/azure-ai-projects/2.10.0/) | Installiertes Paket 2.10.0 |
| [azure-identity Release](https://pypi.org/project/azure-identity/1.27.0/) | Installiertes Paket 1.27.0 |
| [openai Release](https://pypi.org/project/openai/3.42.1/) | Installiertes Paket 3.42.1 |

Die drei Paketversionen wurden über den Paketindex ermittelt und in `.venv`
installiert. Auch transitive Abhängigkeiten sind in [requirements.txt](requirements.txt)
festgehalten. Testsystem: Windows, CPython **3.14.2**. Python 3.11+ ist der Zielbereich;
andere Python-/OS-Kombinationen wurden hier nicht ausgeführt.

Die **installierten** Signaturen wurden mit `inspect.signature` und Modell-Docstrings geprüft:

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

API-Version des Projects-Clients: **v1**. Dieses Repository verwendet den
Projekt-OpenAI-Client und `extra_body.agent_reference` **mit Version**. Es benötigt
keinen agentgebundenen Preview-Endpoint. In 2.10.0 verlangt
`get_openai_client(agent_name=...)` ausdrücklich `allow_preview=True`; manche
öffentlichen Quickstart-Snippets zeigen das noch nicht. Wir übernehmen dieses
Snippet deshalb nicht unverändert. Modell-Preflight und eine lesende
Agent-Reference-/Responses-/MCP-Abfrage gegen einen separat vorbereiteten
IQ-Agenten wurden live ausgeführt. Der vollständige File-Search-/Function-Pfad
bleibt separat durch den tenantabhängigen Core-Smoke nachzuweisen.

## IQ, Architektur und didaktische Inspiration

- [Was ist Foundry IQ?](https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/what-is-foundry-iq)
- [Knowledge Base erstellen](https://learn.microsoft.com/en-us/azure/search/agentic-retrieval-how-to-create-knowledge-base)
- [Foundry-Agent mit KB verbinden](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/foundry-iq-connect)
- [Offizieller IQ-Toolbox-Sample 17](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/python/hosted-agents/agent-framework/responses/17-foundry-iq-toolbox)
  — `FoundryChatClient`, `FoundryToolbox`, echte Search-KB/MCP, Modellbeispiel
  `gpt-5.4-mini`; kein Beleg für dessen Verfügbarkeit in jedem Tenant.
- [Enterprise Knowledge Agent](https://github.com/microsoft/Foundry-Agent-Solution-Templates/tree/main/enterprise-knowledge-agent)
  — weiterführende Enterprise-Architektur, nicht die Pflichtinstallation.
- [Microsoft IQ Samples](https://github.com/microsoft/iq-samples)
  — optionale produktübergreifende Integrationen; keine Lizenzzusage.
- [Azure-centric LangChain Referenz](https://github.com/fustok/langchain-azure-centric)
  — Community-Referenz, **keine** Laufzeitabhängigkeit oder offizielle Produktgarantie.
- [Ausführlicher Fabric-Labstil](https://github.com/customer-success-microsoft/WSPlus-Fabric-Introduction/blob/main/LabGuide_Instructor/LabGuide/Lab05_FabricDB_DS_RTI.md)
  — Orientierung für nummerierte UI-Schritte, Checkpoints und Recovery, kein kopierter Labtext.
- [Fabric IQ](https://learn.microsoft.com/en-us/fabric/iq/overview)
- [Work IQ CLI](https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/work-iq/cli)
- [Foundry-Ressourcen vorbereiten](https://learn.microsoft.com/en-us/azure/foundry/tutorials/quickstart-create-foundry-resources)
- [Hosted Agent bereitstellen](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/deploy-hosted-agent)

Keine internen Unterlagen, privaten Tenantdaten, Nutzeridentitäten oder
UI-Screenshots wurden in das Teilnehmerrepository aufgenommen.
