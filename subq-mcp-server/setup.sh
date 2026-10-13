#!/usr/bin/env bash
set -e

# Determine script directory
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

echo "=== Setting up SubQ Snap MCP Server ==="

# Check Python 3
if ! command -v python3 &> /dev/null; then
    echo "Error: python3 is not installed. Please install Python 3.10+."
    exit 1
fi

# Create virtual environment if not present
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment at $DIR/.venv..."
    python3 -m venv .venv
fi

# Install dependencies
echo "Installing dependencies..."
./.venv/bin/pip install --upgrade pip
./.venv/bin/pip install -r requirements.txt

# Create .env from template if missing
if [ ! -f ".env" ]; then
    echo "Creating .env from .env.example..."
    cp .env.example .env
    echo "NOTE: Please edit $DIR/.env and set your SUBQ_API_KEY."
fi

# Smoke test MCP server
echo "Verifying server startup..."
echo '{"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "test", "version": "1.0"}}}' | ./.venv/bin/python3 server.py > /dev/null 2>&1

echo "Setup completed successfully!"
echo "Server path: $DIR/server.py"
echo "Python binary: $DIR/.venv/bin/python"
