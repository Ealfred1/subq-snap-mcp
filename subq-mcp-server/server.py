import glob
import os
import subprocess
from typing import List, Optional
import httpx
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

# Load local .env if present
load_dotenv()

# Initialize FastMCP server
mcp = FastMCP("subq-snap")

SUBQ_API_KEY = os.getenv("SUBQ_API_KEY")
SUBQ_API_URL = os.getenv("SUBQ_API_URL", "https://api.subq.ai/v1/systemone")
SUBQ_MODEL = os.getenv("SUBQ_MODEL", "subq-snap-preview")

# Safe context truncation limit (chars ~ 350k tokens)
MAX_CONTEXT_CHARS = 1_200_000


async def call_subq_decision(context: str, query: str, candidates: List[str]) -> str:
    """Internal helper to dispatch decision query to SubQ Snap API."""
    api_key = os.getenv("SUBQ_API_KEY") or SUBQ_API_KEY
    api_url = os.getenv("SUBQ_API_URL") or SUBQ_API_URL

    if not api_key:
        return "Error: SUBQ_API_KEY environment variable is not configured."

    if not candidates:
        return "Error: At least one candidate must be provided."

    # Build criteria mapping candidate keys to descriptions
    criteria = {}
    key_to_candidate = {}
    for idx, c in enumerate(candidates):
        safe_key = f"opt_{idx}_{c[:30].strip()}".replace(" ", "_").replace("-", "_").replace(".", "_")
        safe_key = "".join(ch for ch in safe_key if ch.isalnum() or ch == "_").lower()
        if not safe_key:
            safe_key = f"opt_{idx}"
        criteria[safe_key] = c
        key_to_candidate[safe_key] = c

    # Guard against overflowing max context
    if len(context) > MAX_CONTEXT_CHARS:
        context = context[:MAX_CONTEXT_CHARS] + "\n\n... [Context truncated to 1.2M chars / ~350k tokens]"

    payload = {
        "model": SUBQ_MODEL,
        "state": context,
        "questions": {
            "decision": {
                "type": "choice",
                "instructions": query,
                "criteria": criteria,
            }
        },
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    try:
        async with httpx.AsyncClient(timeout=45.0) as client:
            response = await client.post(api_url, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()

            answers = data.get("answers", {})
            decision_answer = answers.get("decision", {})
            chosen_key = decision_answer.get("choice")

            if chosen_key and chosen_key in key_to_candidate:
                confidence = decision_answer.get("confidence")
                conf_str = f" (confidence: {confidence:.2%})" if confidence is not None else ""
                return f"{key_to_candidate[chosen_key]}{conf_str}"

            return str(data)
    except httpx.HTTPStatusError as e:
        return f"SubQ API Error ({e.response.status_code}): {e.response.text}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"


@mcp.tool()
async def evaluate_decision(context: str, query: str, candidates: list[str]) -> str:
    """Evaluate massive raw text/code context directly and return the best choice among candidates in under a second.

    Args:
        context: The raw text, logs, diffs, or code string to analyze.
        query: The specific question or criteria to evaluate (e.g. 'Which file causes this error?').
        candidates: The list of possible options/choices to select from.
    """
    return await call_subq_decision(context=context, query=query, candidates=candidates)


@mcp.tool()
async def evaluate_files(
    file_paths: list[str],
    query: str,
    candidates: list[str],
    max_file_size_kb: int = 2048,
) -> str:
    """TOKEN-SAVING TOOL: Reads files directly from disk on the local machine and feeds their full content to SubQ Snap without loading them into the AI assistant's context window.

    Supports exact paths or glob patterns (e.g., ['src/**/*.py', 'logs/*.log']).

    Args:
        file_paths: List of absolute or relative file paths or glob patterns to read.
        query: The evaluation question (e.g. 'Which file has the bug that crashes payment?').
        candidates: List of candidate options.
        max_file_size_kb: Max size per file in KB before truncation (default 2048 KB).
    """
    expanded_files = []
    for pattern in file_paths:
        expanded = glob.glob(os.path.expanduser(pattern), recursive=True)
        if expanded:
            expanded_files.extend(expanded)
        else:
            expanded_files.append(os.path.expanduser(pattern))

    # Remove duplicates while preserving order
    seen = set()
    unique_files = [f for f in expanded_files if not (f in seen or seen.add(f))]

    context_blocks = []
    loaded_count = 0
    max_bytes = max_file_size_kb * 1024

    for path in unique_files:
        if not os.path.exists(path) or os.path.isdir(path):
            continue
        try:
            with open(path, "r", encoding="utf-8", errors="replace") as f:
                content = f.read(max_bytes)
                context_blocks.append(f"=== FILE: {path} ===\n{content}\n")
                loaded_count += 1
        except Exception as e:
            context_blocks.append(f"=== FILE: {path} (Error reading: {e}) ===\n")

    if not context_blocks:
        return f"Error: No readable files found matching provided paths: {file_paths}"

    combined_context = (
        f"Analyzed {loaded_count} files locally on disk without inflating LLM context:\n\n"
        + "\n".join(context_blocks)
    )

    return await call_subq_decision(
        context=combined_context, query=query, candidates=candidates
    )


@mcp.tool()
async def evaluate_command(
    command: str,
    query: str,
    candidates: list[str],
    cwd: Optional[str] = None,
    timeout_seconds: int = 60,
) -> str:
    """TOKEN-SAVING TOOL: Executes a shell command locally (e.g. 'npm test', 'git diff', 'pytest', 'docker logs') and pipes its full stdout/stderr directly into SubQ Snap without consuming any AI assistant context tokens.

    Args:
        command: The shell command to run (e.g. 'pytest -v', 'git log -n 50 -p').
        query: The question to evaluate on the command output.
        candidates: Candidate options to select from.
        cwd: Directory in which to run the command (defaults to current working directory).
        timeout_seconds: Maximum command execution time in seconds (default 60s).
    """
    try:
        proc = subprocess.run(
            command,
            shell=True,
            cwd=cwd or os.getcwd(),
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
        )
        combined_output = f"Command: {command}\nExit Code: {proc.returncode}\n\nSTDOUT:\n{proc.stdout}\n\nSTDERR:\n{proc.stderr}"
    except subprocess.TimeoutExpired:
        return f"Error: Command '{command}' timed out after {timeout_seconds} seconds."
    except Exception as e:
        return f"Error executing command '{command}': {str(e)}"

    return await call_subq_decision(
        context=combined_output, query=query, candidates=candidates
    )


if __name__ == "__main__":
    mcp.run()
