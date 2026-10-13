# SubQ Snap MCP Server

Fast Model Context Protocol (MCP) server exposing **SubQ Snap** (`subq-snap-preview`) directly to AI coding assistants (**Antigravity**, **Claude Code**, **Claude Desktop**, **Cursor**) for sub-second, ultra-fast triage and discrete decision-making over large context (up to 384k tokens).

---

## 💡 How It Saves Your AI Assistant Credits (Context Offloading)

Standard coding assistants charge you per input token. If your assistant reads a 100,000-token log file or 15 codebase files into its context, you waste significant LLM tokens and hit context limits.

This MCP server solves that by **reading disk and commands locally inside the MCP process**, bypassing your primary model's context window completely:

```
❌ Traditional LLM Flow (Burns Context Credits):
[100k Token Log File] ──> Read by Assistant ($$$) ──> Sent to Tool

✅ SubQ Context-Offloaded Flow (Saves 99.9% Credits):
Assistant sends: { file_paths: ["/var/log/app.log"] }  (~15 tokens)
MCP reads file locally on disk ──> Streams 384k tokens directly to SubQ Snap ($0.005)
Assistant receives: "payment_service.py"  (~5 tokens)
```

---

## 🛠️ Available MCP Tools

| Tool | Credit-Saving Benefit | Description |
|---|---|---|
| `evaluate_files` | **Saves 99%+ Tokens** | Reads file paths or glob patterns directly from disk without passing file content through the assistant. |
| `evaluate_command` | **Saves 99%+ Tokens** | Runs a local shell command (e.g. `npm test`, `pytest`, `git diff`, `docker logs`) and pipes stdout/stderr straight into SubQ Snap. |
| `evaluate_decision` | Direct evaluation | Accepts raw in-memory context string, query, and candidates. |

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

Instead of asking your agent to read files or run tests in chat:

- **Pinpoint test failures without reading giant logs**:
  > *"Run `evaluate_command` with `npm test` to tell me which test suite failed among `[auth, billing, checkout]`."*

- **Scan multiple files without loading them into context**:
  > *"Use `evaluate_files` on `['src/**/*.py']` to find which file defines the JWT expiration logic."*
