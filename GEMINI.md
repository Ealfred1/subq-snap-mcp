# SubQ Snap Context Offloading & Credit-Saving Rule

## Critical Instruction: SubQ is an MCP Tool, NOT a CLI binary
`subq` is registered as an MCP server named `subq-snap`.
- **NEVER run terminal commands like `which subq`, `subq`, or search disk for a `subq` binary.**
- **NEVER read large codebase files (>100 lines) or raw scripts with `view_file` to understand or audit.**
- **ALWAYS call the MCP tool directly using `call_mcp_tool`**:
  `call_mcp_tool(ServerName="subq-snap", ToolName="...", Arguments={...})`

## When to Call SubQ MCP Tools
1. **Auditing or understanding a codebase / workspace**:
   - Call `evaluate_files`:
     ```json
     {
       "file_paths": ["src/**/*.ts", "**/*.py"],
       "query": "What is the primary architecture and function of this codebase?",
       "candidates": [
         "Candidate architecture A",
         "Candidate architecture B",
         "Candidate architecture C"
       ]
     }
     ```
   - The MCP server reads the files locally from disk and feeds up to 384k tokens directly to SubQ Snap.
   - Context tokens spent by assistant: **~15 tokens instead of 100,000+**.

2. **Triaging test, build, or terminal failures**:
   - Call `evaluate_command`:
     ```json
     {
       "command": "npm test",
       "query": "Which test suite failed and why?",
       "candidates": ["Auth test", "Database connection", "Syntax error"]
     }
     ```

3. **Pinpointing bug root cause across files**:
   - Call `evaluate_files` with candidate file paths to locate the exact culprit before viewing lines.

## Follow-up Action
Only after SubQ identifies the exact culprit file or answers the query should the assistant selectively view the specific relevant lines (using small line ranges) to write the fix.
