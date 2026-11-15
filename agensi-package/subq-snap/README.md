# SubQ Snap Agent Skill

> Ultra-fast, sub-second decision making, triage, and filtering over massive contexts (up to 384k tokens) using SubQ Snap.

This skill equips any AI coding agent (**Claude Code**, **Cursor**, **Copilot**, **Antigravity**, **Gemini CLI**, and 20+ other agents) with the knowledge of how and when to offload massive context evaluations to the **SubQ Snap MCP Server**.

---

## ⚡ The Problem: LLM Context Window Burn

When agents triage large test logs (100k+ tokens) or scan an entire codebase for bugs, they typically read all files into their primary context window:
- 💸 **Costly**: Burns hundreds of thousands of input tokens per triage turn.
- ⏳ **Slow**: Large context ingestion takes 10–30+ seconds.
- ⚠️ **Context Pollution**: Chat memory fills up rapidly, degrading reasoning performance.

---

## 🚀 The Solution: SubQ Snap Context Offloading

By connecting your agent to the **SubQ Snap MCP Server**, the agent delegates disk-reading and terminal log parsing directly to SubQ Snap:

1. **`evaluate_files`**: Agent passes glob patterns (e.g. `["src/**/*.ts"]`). The MCP server reads files locally on disk and streams up to 384k tokens straight to SubQ Snap. **The primary agent spends ~15 tokens instead of 100,000+!**
2. **`evaluate_command`**: Agent runs test suites (`npm test`, `pytest`) locally without dumping massive terminal output into the chat window. SubQ parses stdout/stderr and pinpoints the culprit in under a second.
3. **`evaluate_decision`**: Instant probabilistic choice and confidence scoring between candidate options.

---

## 📦 What's Included

- `SKILL.md`: Standard Agent Skills instruction file defining negative boundaries, tool schemas, and step-by-step procedures.
- `references/mcp_setup.md`: Complete setup and installation guide for Claude Code, Claude Desktop, Cursor, and Antigravity.
- `references/examples.md`: Practical workflows and prompt patterns.

---

## 🛠️ Quick MCP Server Setup

This skill pairs with the open-source **SubQ Snap MCP Server**:
Repository: [https://github.com/Ealfred1/subq-snap-mcp](https://github.com/Ealfred1/subq-snap-mcp)

1. Clone and install:
   ```bash
   git clone https://github.com/Ealfred1/subq-snap-mcp.git
   cd subq-snap-mcp/subq-mcp-server
   chmod +x setup.sh && ./setup.sh
   ```
2. Add your SubQ API Key (`https://subq.ai`) to `.env`:
   ```env
   SUBQ_API_KEY=your_key_here
   ```
3. Register the server in your agent's MCP configuration (see `references/mcp_setup.md`).
