# SubQ Snap MCP Server

Fast Model Context Protocol (MCP) server exposing **SubQ Snap** (`subq-snap-preview`) directly to AI coding assistants (**Antigravity**, **Claude Code**, **Claude Desktop**, **Cursor**) for sub-second, ultra-fast triage and discrete decision-making over massive contexts (up to 384k tokens).

---

## 💡 How It Saves Your AI Assistant Credits (Context Offloading)

Standard coding assistants (Gemini, Claude, GPT) charge per input token. If your assistant reads a 100,000-token log file or dozens of codebase files into its chat context, you quickly exhaust token budgets and hit context limits.

This MCP server solves that by **reading disk and commands locally inside the MCP process**, bypassing your primary model's context window completely:

```
❌ Traditional LLM Flow (Burns Context Credits):
[100k Token Log File] ──> Read by Assistant ($$$) ──> Sent to Tool

✅ SubQ Context-Offloaded Flow (Saves 99.9% Credits):
Assistant sends: { file_paths: ["src/**/*.ts"] }  (~15 tokens)
MCP reads files locally on disk ──> Streams 384k tokens directly to SubQ Snap ($0.005)
Assistant receives: "auth_service.ts"  (~5 tokens)
```

---

## 🛠️ Available MCP Tools

| Tool | Credit-Saving Benefit | Description |
|---|---|---|
| `evaluate_files` | **Saves 99%+ Tokens** | Reads file paths or glob patterns directly from disk without passing file content through the assistant. |
| `evaluate_command` | **Saves 99%+ Tokens** | Runs a local shell command (e.g. `npm test`, `pytest`, `git diff`, `docker logs`) and pipes stdout/stderr straight into SubQ Snap. |
| `evaluate_decision` | Direct evaluation | Accepts raw in-memory context string, query, and candidates. |

---

## ⚠️ Critical Rule: SubQ is an MCP Tool, NOT a CLI Binary!

If you ask an assistant like Claude or Gemini to "use SubQ", assistants sometimes try to run `which subq` in the terminal looking for a CLI binary, or they start reading files manually with `view_file`.

To prevent this:
1. Always tell the assistant to use the MCP tool name: `evaluate_files` or `evaluate_command`.
2. Add the [Rule file](GEMINI.md) (`GEMINI.md` or `.agents/rules/subq.md`) to your projects so assistants know SubQ is an MCP server.

---

## 🚀 Quick Setup (New Machine / Another PC)

### Prerequisites
- **Python 3.10+**
- Git

### 1. Clone the Repository
```bash
git clone https://github.com/Ealfred1/subq-snap-mcp.git subq
cd subq/subq-mcp-server
```

### 2. Run the Automated Installer
On macOS / Linux:
```bash
chmod +x setup.sh
./setup.sh
```

Or manually:
```bash
python3 -m venv .venv
source .venv/bin/activate       # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

### 3. Add Your SubQ API Key
Edit `.env` in `subq-mcp-server/`:
```bash
SUBQ_API_KEY=your_subq_api_key_here
SUBQ_API_URL=https://api.subq.ai/v1/systemone
SUBQ_MODEL=subq-snap-preview
```

---

## 🔌 Registering with AI Coding Assistants

Find the absolute path to your environment on your machine:
- **macOS / Linux**:
  - Python: `/path/to/subq/subq-mcp-server/.venv/bin/python`
  - Script: `/path/to/subq/subq-mcp-server/server.py`
- **Windows**:
  - Python: `C:\path\to\subq\subq-mcp-server\.venv\Scripts\python.exe`
  - Script: `C:\path\to\subq\subq-mcp-server\server.py`

---

### Option 1: Antigravity

Add to your global MCP config (`~/.gemini/config/mcp_config.json`):

```json
{
  "mcpServers": {
    "subq-snap": {
      "command": "/path/to/subq/subq-mcp-server/.venv/bin/python",
      "args": ["/path/to/subq/subq-mcp-server/server.py"],
      "env": {
        "SUBQ_API_KEY": "your_subq_api_key_here"
      }
    }
  }
}
```

> **Antigravity Tip**: To ensure Antigravity exposes all 3 tools eagerly, ensure tool schema files are present in `~/.gemini/antigravity/mcp/subq-snap/` (`evaluate_files.json`, `evaluate_command.json`, `evaluate_decision.json`).

---

### Option 2: Claude Desktop / Claude Code

Add to your `claude_desktop_config.json`:
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "subq-snap": {
      "command": "/path/to/subq/subq-mcp-server/.venv/bin/python",
      "args": ["/path/to/subq/subq-mcp-server/server.py"],
      "env": {
        "SUBQ_API_KEY": "your_subq_api_key_here"
      }
    }
  }
}
```

---

### Option 3: Cursor

1. Open Cursor Settings (`Cmd + ,` or `Ctrl + ,`).
2. Go to **Features** ➔ **MCP**.
3. Click **Add New MCP Server**:
   - **Name**: `subq-snap`
   - **Type**: `command`
   - **Command**: `/path/to/subq/subq-mcp-server/.venv/bin/python /path/to/subq/subq-mcp-server/server.py`
4. Under environment variables, add:
   - `SUBQ_API_KEY` = `your_subq_api_key_here`
5. Save & test connection (green checkmark will appear).

---

## 💬 Prompts to Save Credits

Use these exact phrasing styles to trigger the MCP tools directly:

- **Auditing a codebase without reading raw files**:
  > *"Use `evaluate_files` on `['src/**/*.ts']` to determine the primary architecture and function of this codebase."*

- **Pinpointing test failures without reading giant logs**:
  > *"Run `evaluate_command` with `npm test` to tell me which test suite failed among `[auth, billing, checkout]`."*

- **Finding which file causes a bug**:
  > *"Use `evaluate_files` on `['src/**/*.py']` to find which file defines the JWT expiration logic among candidate files."*

---

## 🤖 Global Agent Rule (`GEMINI.md` / `AGENTS.md`)

Place this in `~/.gemini/rules/subq.md` or your project's root `GEMINI.md`:

```markdown
# SubQ Snap Context Offloading & Credit-Saving Rule

## Critical Instruction: SubQ is an MCP Tool, NOT a CLI binary
subq is registered as an MCP server named subq-snap.
- NEVER run terminal commands like which subq, subq, or search disk for a subq binary.
- NEVER read large codebase files (>100 lines) with view_file to understand or audit.
- ALWAYS call the MCP tool directly using call_mcp_tool(ServerName="subq-snap", ToolName="evaluate_files", ...).

## Follow-up Action
Only after SubQ identifies the exact culprit file should the assistant selectively view the specific relevant lines (using small line ranges) to write the fix.
```
