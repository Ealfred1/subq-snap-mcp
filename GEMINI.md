# SubQ Snap Context Offloading & Credit-Saving Rule

## Goal
Protect the assistant's context window and minimize token consumption by offloading large context evaluations directly to **SubQ Snap** via local MCP tools instead of loading raw text into context.

## Trigger Conditions
Whenever you need to:
1. **Triage test or build failures**: When tests fail, builds break, or terminal commands produce large outputs.
2. **Search or inspect large files (>100 lines)**: Including logs, configs, database dumps, diffs, or code files.
3. **Pinpoint bug root causes across multiple files**: To determine which file, module, or function is causing an issue.
4. **Choose between competing technical options**: Architecture candidates, routing decisions, or classifications.

## Mandatory Actions
- **NEVER** run `view_file` on large files (>100 lines) or dump massive terminal outputs directly into chat memory if the goal is triage, pinpointing, or classification.
- **ALWAYS** call the `subq-snap` MCP tools:
  - **`evaluate_files(file_paths, query, candidates)`**:
    - Pass paths or glob patterns (e.g. `['src/**/*.py']`, `['logs/*.log']`).
    - The MCP server reads disk locally and streams up to 384k tokens directly to SubQ Snap.
    - Context tokens spent by primary model: **~15 tokens instead of 100,000+**.
  - **`evaluate_command(command, query, candidates, cwd)`**:
    - Pass shell commands that produce large output (e.g., `npm test`, `pytest`, `git log -p`, `docker logs`).
    - The MCP server executes locally and pipes stdout/stderr straight to SubQ Snap.
    - Context tokens spent by primary model: **~15 tokens**.
  - **`evaluate_decision(context, query, candidates)`**:
    - Use for in-memory text when context is already loaded.

## Follow-up Action
Only after SubQ identifies the exact culprit file or root cause should the assistant selectively view the specific relevant lines (e.g., using precise line ranges) to write the fix.
