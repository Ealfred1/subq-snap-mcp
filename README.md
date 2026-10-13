# SubQ Snap MCP Server

Fast Model Context Protocol (MCP) server exposing **SubQ Snap** (`subq-snap-preview`) directly to AI coding assistants (**Antigravity**, **Claude Code**, **Claude Desktop**, **Cursor**) for sub-second, ultra-fast triage and discrete decision-making over large context (up to 384k tokens).

---

## 🚀 Quick Setup (New Machine / Another PC)

### Prerequisites
- **Python 3.10+**
- Git

### 1. Clone or Copy the Repository
```bash
git clone <your-repo-url> subq
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
Edit the `.env` file in `subq-mcp-server/`:
```bash
SUBQ_API_KEY=your_subq_api_key_here
SUBQ_API_URL=https://api.subq.ai/v1/systemone
SUBQ_MODEL=subq-snap-preview
```

---

## 🔌 Registering with AI Coding Assistants

Find the absolute path to your environment on your new PC:
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

## 🛠️ Testing the Server

You can run an end-to-end decision check directly from terminal:

```bash
./.venv/bin/python -c '
import asyncio
from server import evaluate_decision

async def test():
    res = await evaluate_decision(
        context="Error: connect ECONNREFUSED 127.0.0.1:5432 in db.js:42",
        query="Which service is failing to connect?",
        candidates=["PostgreSQL database", "Redis cache", "Auth server"]
    )
    print("Result:", res)

asyncio.run(test())
'
```

Output:
```
Result: PostgreSQL database (confidence: 98.24%)
```

---

## 💬 How Your Coding Assistant Uses It

Prompt your assistant naturally:
> *"Check the terminal output and use the evaluate_decision tool to pinpoint which test failed instead of reading the whole raw file."*

The model offloads context processing to SubQ Snap, saving context tokens and returning decisions in sub-second time.
