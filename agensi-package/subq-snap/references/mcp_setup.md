# MCP Server Setup Guide for All Agents

To use this skill, the **SubQ Snap MCP Server** must be registered in your AI agent.

Repository: `https://github.com/Ealfred1/subq-snap-mcp`

---

## 1. Local Server Installation

```bash
git clone https://github.com/Ealfred1/subq-snap-mcp.git
cd subq-snap-mcp/subq-mcp-server
chmod +x setup.sh && ./setup.sh
```

In `.env`, configure:
```env
SUBQ_API_KEY=your_subq_api_key_here
SUBQ_API_URL=https://api.subq.ai/v1/systemone
SUBQ_MODEL=subq-snap-preview
```

---

## 2. Agent Configuration

### Claude Code / Claude Desktop
Add to `claude_desktop_config.json`:
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "subq-snap": {
      "command": "/absolute/path/to/subq-mcp-server/.venv/bin/python",
      "args": ["/absolute/path/to/subq-mcp-server/server.py"],
      "env": {
        "SUBQ_API_KEY": "your_subq_api_key_here"
      }
    }
  }
}
```

### Cursor
1. Go to **Settings** ➔ **Features** ➔ **MCP**.
2. Click **Add New MCP Server**:
   - **Name**: `subq-snap`
   - **Type**: `command`
   - **Command**: `/path/to/subq-mcp-server/.venv/bin/python /path/to/subq-mcp-server/server.py`
   - **Environment Variable**: `SUBQ_API_KEY = your_key`

### Antigravity
Add to `~/.gemini/config/mcp_config.json`:
```json
{
  "mcpServers": {
    "subq-snap": {
      "command": "/path/to/subq-mcp-server/.venv/bin/python",
      "args": ["/path/to/subq-mcp-server/server.py"],
      "env": {
        "SUBQ_API_KEY": "your_subq_api_key_here"
      }
    }
  }
}
```
