# 210 minutes: schedule and learning goals

[Home](../README.md) · [Facilitator runbook](INSTRUCTOR.md)

**Audience:** intermediate; basic Azure, Python/JSON, terminal and RBAC concepts.
No machine-learning training required. Work in teams of two or three with
separate customer identities. Prepare approved customer resources/quota before
the event where possible. Facilitators help configure own-subscription access
on the day; customer admins retain privileged operations. Readiness is a
15-minute checkpoint, not enough for full bootstrap, subscription approval,
network changes or quota increases. A separate clinic may take 60–90 minutes
or more plus organizational lead time.

| Time from start | Minutes | Format / outcome |
|---|---:|---|
| 00:00–00:30 | 30 | Facilitator demo: evidence → inventory → recommendation → denied/approved local draft |
| 00:30–00:45 | 15 | [00 Readiness](labs/00-readiness.md): supported customer-access checkpoint, Python, roles, endpoint, model, identity |
| 00:45–01:10 | 25 | [01 Portal](labs/01-portal.md): prompt agent in new Foundry, limitations without knowledge |
| 01:10–01:40 | 30 | [02 Grounding](labs/02-grounding.md): File Search, index status, version, sources |
| 01:40–01:50 | 10 | **Break**; stop polling/chat processes |
| 01:50–02:25 | 35 | [03 Code & Tools](labs/03-tools.md): Python in VS Code, tool loop, human gate |
| 02:25–02:45 | 20 | [04 Evaluation](labs/04-evaluation.md): counterexamples, evidence, diagnostics, rubric |
| 02:45–03:20 | 35 | [05 Hackathon](labs/05-hackathon.md): measurable improvement and attack test |
| 03:20–03:30 | 10 | [06 Pitch & Cleanup](labs/06-cleanup.md): short proof and scoped cleanup |
| **Total** | **210** | **3.5 hours including the break** |

## By the end you can …

1. Distinguish a **server-registered, versioned prompt agent** from its local
   executing Python process.
2. Verify real File Search citation annotations rather than trust a source claim.
3. Validate tool parameters in code and technically separate writes from the model.
4. Explain the limits of offline tests, structural checks and semantic evaluation.
5. Explain the additional value of Foundry IQ, Fabric IQ and Work IQ without
   requiring extra licenses for the core.

## Core definition of done

- Your own starter function is read-only and its learning checks pass.
- At least one real response under your own customer identity has a verifiable
  current-policy citation and a separate inventory source. Missing access stays
  `BLOCKED`; another person's/admin's pass is not your individual proof.
- Denied approval creates no DB/write; exact human approval creates at most one
  row per proposal; inventory stays unchanged.
- Three counterexamples and a manual score, not just response length.
- Only owned resources removed, or a named customer cleanup owner/action recorded.

**Cloud unavailable:** [honest offline learning](INSTRUCTOR.md) teaches tools,
validation and approval, but does **not** satisfy cloud-agent/citation acceptance.
Approved observation of a customer teammate is not an individual cloud pass.
There is no instructor-hosted fallback.
