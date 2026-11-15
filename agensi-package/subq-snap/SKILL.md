---
name: subq-snap
description: Ultra-fast sub-second decision making, triage, and filtering over massive contexts (up to 384k tokens) using SubQ Snap. Use when triaging test failures, diagnosing bugs across large files, or evaluating candidates without burning LLM context window tokens.
when_to_use: |
  - User asks to triage test logs, terminal errors, or build failures
  - User wants to pinpoint bug root causes across many codebase files
  - User wants to evaluate large files or logs (>100 lines) without inflating context
  - User asks to decide between architectural, routing, or classification options
  - Do NOT use for: generating free-form code or open-ended essays (SubQ Snap is a discrete decision engine)
argument-hint: Provide the query, candidate options, and target file paths or command.
allowed-tools:
  - evaluate_files
  - evaluate_command
  - evaluate_decision
---

# SubQ Snap Decision & Context-Offloading Skill

This skill teaches the AI assistant how to leverage the **SubQ Snap MCP Server** to evaluate massive context (up to 384k tokens) in under a second while saving 99%+ of LLM context tokens.

---

## Critical Rules & Negative Boundaries

1. **SubQ is an MCP Tool, NOT a CLI binary**:
   - NEVER run shell commands like `which subq`, `which subq-snap`, or search the filesystem for a `subq` binary.
   - ALWAYS invoke the registered MCP tools: `evaluate_files`, `evaluate_command`, or `evaluate_decision`.

2. **Context Offloading Priority**:
   - NEVER read entire large files (>100 lines), logs, or full codebase trees directly into context using file-reading tools when the goal is triage, pinpointing, or classification.
   - Offload the raw reading directly to the MCP server via `evaluate_files` or `evaluate_command`. The MCP server streams disk bytes straight to SubQ Snap's 384k token window, returning only the discrete answer to the assistant (~15 tokens total).

3. **Follow-Up Precision**:
   - After SubQ Snap identifies the exact culprit file or root cause, the assistant should selectively inspect only the specific lines or functions needed to implement the fix.

---

## Tool Usage Guide

### 1. `evaluate_files` (Disk Offloading)
Use when triaging codebase architecture, identifying buggy files, or finding specific implementations across files.

**Arguments:**
- `file_paths`: List of exact file paths or glob patterns (e.g. `["src/**/*.ts"]`, `["logs/*.log"]`).
- `query`: The specific criteria or question (e.g. *"Which file causes the authentication token expiration failure?"*).
- `candidates`: List of discrete choices/options to select from (e.g. `["src/auth.ts", "src/db.ts", "src/router.ts"]`).
- `max_file_size_kb`: (Optional) Max file size in KB per file (defaults to 2048).

**Workflow:**
1. Formulate 2 to 10 clear candidate options based on the user's inquiry.
2. Call `evaluate_files` with target file globs.
3. SubQ Snap reads disk locally, evaluates the candidates, and returns the winner with confidence.

### 2. `evaluate_command` (Terminal Output Offloading)
Use when test suites fail, builds break, or terminal commands produce massive logs.

**Arguments:**
- `command`: The shell command to run locally (e.g. `npm test`, `pytest -v`, `git log -n 50 -p`).
- `query`: The evaluation criteria (e.g. *"Which test suite failed and why?"*).
- `candidates`: List of possible failure causes or test suites.
- `cwd`: (Optional) Working directory.

**Workflow:**
1. Run `evaluate_command` instead of dumping terminal stdout into the chat context.
2. SubQ Snap receives stdout/stderr directly and returns the winning diagnosis.

### 3. `evaluate_decision` (In-Memory Evaluation)
Use when context is already short and in-memory, but a fast, probabilistic decision or ranking between candidates is needed.

**Arguments:**
- `context`: Raw string to analyze.
- `query`: Question or criteria.
- `candidates`: List of choices.

---

## Example Interaction

**User:**
> "Why is the test suite failing? Check the logs and fix it."

**Assistant Procedure:**
1. Call `evaluate_command`:
   ```json
   {
     "command": "npm test",
     "query": "Which test suite failed?",
     "candidates": ["auth.test.ts", "payment.test.ts", "user.test.ts"]
   }
   ```
2. SubQ returns: `payment.test.ts (confidence: 98.4%)`.
3. Assistant reads only `payment.test.ts` (spending minimal tokens) and crafts the exact bug fix.
