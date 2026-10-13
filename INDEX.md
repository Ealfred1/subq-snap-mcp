# Codebase Semantic Index: `subq-snap-mcp`

> Indexed via **SubQ Snap** (`subq-snap-preview`) using local disk offloading.

---

## 🗺️ Architectural Map

```
subq/
├── GEMINI.md                          # Mandatory agent guardrails for SubQ context offloading
├── .agents/
│   └── rules/
│       └── subq.md                    # Project-level credit-saving rules
├── README.md                          # Global repository guide and multi-PC setup instructions
├── .gitignore                         # Protects .venv, .env, and sensitive credentials
└── subq-mcp-server/                   # MCP Server Core Package
    ├── server.py                      # FastMCP server exposing evaluate_files, evaluate_command, evaluate_decision
    ├── requirements.txt               # Pinned dependencies (mcp<2, httpx, python-dotenv)
    ├── setup.sh                       # One-command automated installer for Unix/macOS
    ├── .env.example                   # Environment variable template
    ├── .env                           # Local machine secrets (ignored by git)
    └── README.md                      # Detailed server documentation
```

---

## ⚡ Tool Capabilities Index (Verified by SubQ)

### 1. `evaluate_files`
- **Location**: [`subq-mcp-server/server.py`](file:///Users/eric/subq/subq-mcp-server/server.py#L93)
- **SubQ Classification**: **Primary File Offloader (98.13% confidence)**
- **Role**: Reads disk paths and glob patterns (`src/**/*.py`, `logs/*.log`) directly inside the local MCP process.
- **Credit Benefit**: Passes up to 384k tokens directly to SubQ Snap. Gemini uses **~15 tokens**.

### 2. `evaluate_command`
- **Location**: [`subq-mcp-server/server.py`](file:///Users/eric/subq/subq-mcp-server/server.py#L147)
- **SubQ Classification**: **Primary Command Offloader (97.45% confidence)**
- **Role**: Executes shell commands (`npm test`, `pytest`, `git diff`) and pipes stdout/stderr directly into SubQ.
- **Credit Benefit**: Assistant never ingests terminal logs into chat context.

### 3. `evaluate_decision`
- **Location**: [`subq-mcp-server/server.py`](file:///Users/eric/subq/subq-mcp-server/server.py#L80)
- **Role**: Direct in-memory text evaluation when context is already loaded.

---

## 🛡️ Autonomous Rule Enforcement

- **Location**: [`GEMINI.md`](file:///Users/eric/subq/GEMINI.md) & [`~/.gemini/rules/subq.md`](file:///Users/eric/.gemini/rules/subq.md)
- **SubQ Classification**: **Autonomous Token Guardrail (97.39% confidence)**
- **Enforcement**:
  1. Any file triage or inspect > 100 lines MUST route through `evaluate_files`.
  2. Any command output triage MUST route through `evaluate_command`.
  3. `view_file` is strictly reserved for small target line ranges after the culprit is identified.
