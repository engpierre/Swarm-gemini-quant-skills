# Swarm Gemini Quant Skills

Autonomous multi-agent quant skills, reliability guardrails, and behavioral contracts powering the **Pierre Quant** and **OpenClaw Swarm** platforms.

---

## 🎯 Repository Purpose
This repository serves as the centralized, canonical upstream distribution point for all custom AI Agent Skills utilized across:
- **Pierre Quant Trading Swarm** (16-Agent Autonomous Execution Matrix)
- **Julie Core Spatial Cockpit** (Acoustic HUD & Real-Time Decision Support)
- **Anti-Gravity Multi-Agent Workspace** (Google DeepMind Antigravity Protocol)

Whenever new quant, macro, execution, or visualizer skills are developed, a mirror is committed here to maintain portability and modularity across all systems.

---

## 📦 Active Skills Catalog

| Skill Name | Domain / Subsystem | Primary Function & Directives |
| :--- | :--- | :--- |
| **`agent-gateway-security`** | **Security & Sandboxing** | Enforces strict blast-radius containment, immutable subsystem boundaries, and mandatory read-only SQLite URI modes (`?mode=ro`). Zero mutation of production databases without human air-gap approval. |
| **`gemini-api-cli`** | **CLI & Automation** | Governs programmatic execution of `gemini-api` from the shell. Strictly enforces prompt token minimization (< 25-line forecast blocks) and zero-noise stdin streaming. |
| **`gemini-api-dev`** | **Inference & Contracts** | Canonical SDK implementation standards for Gemini models in Python and TypeScript. Enforces strict typed JSON schema adherence (`AgentExecutionPayload`) and zero reliance on deprecated SDK methods. |
| **`gemini-live-api-dev`** | **Real-Time & Audio HUD** | Real-time bidirectional streaming contracts for the Gemini Live API. Coordinates Julie-Core 3-layer visualizer stages (Video loop + Canvas Oscilloscope + Aerospace Telemetry HUD). |
| **`well-architected-reliability`** | **SRE & High Availability** | Evaluates and hardens systems against the Google Cloud Well-Architected Framework. Implements 20% data-opacity discounts, multi-tier fallback chains, and sub-second failovers. |

---

## 🔄 Automated Synchronization
This repository includes a native synchronization tool (`sync_skills.py`) that mirrors any active skills added to the core platform:

```bash
python sync_skills.py
```

### Automation Workflow:
1. Scans `C:\Anti-Gravity-Core\skills\active` and `.agent\skills` for new `SKILL.md` definitions.
2. Clones new skills into `skills/<skill_name>/`.
3. Auto-indexes frontmatter and regenerates `manifest.json`.
4. Prepares commits with sanitization checks verified.

---

## 🛡️ Security Protocol
In adherence to **Project Anti-Gravity Git Security Protocols**:
- **Zero IP Disclosures:** All sample network bindings use standard RFC loopbacks (`127.0.0.1`) or documentation placeholders (`<HOST_IP>`, `192.0.2.x`).
- **Zero Credentials:** No API keys, tokens, or `.env` files are tracked.
- **Strict Read-Only Sandboxing:** All database ingestion operations default to SQLite read-only mode.
