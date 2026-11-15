# SubQ Snap Agent Workflow Examples

## Example 1: Codebase Audit & Triage

**User Request:**
> "I just cloned this codebase. Audit the architecture and tell me how authentication is structured."

**Traditional Flow (Burns 50,000+ tokens):**
- Agent lists all files.
- Agent calls `read_file` on 15 different files.
- Hundreds of lines fill the agent's context window.

**SubQ Snap Flow (Uses ~15 tokens):**
- Agent calls `evaluate_files`:
  ```json
  {
    "file_paths": ["src/**/*.ts", "package.json"],
    "query": "Which file handles user authentication and session management?",
    "candidates": [
      "src/auth/jwt.ts",
      "src/auth/session.ts",
      "src/routes/login.ts",
      "src/middleware/auth.ts"
    ]
  }
  ```
- SubQ returns: `src/auth/jwt.ts (confidence: 97.2%)`.
- Agent reads only `src/auth/jwt.ts` to answer the user's question concisely.

---

## Example 2: Massive Test Failure Triage

**User Request:**
> "Our E2E test suite failed with 4,000 lines of logs. What broke?"

**SubQ Snap Flow:**
- Agent calls `evaluate_command`:
  ```json
  {
    "command": "npm run test:e2e",
    "query": "What was the root cause of the test failure?",
    "candidates": [
      "Database connection timeout on port 5432",
      "Expired mock JWT token",
      "Missing Stripe webhook secret environment variable",
      "CORS policy rejection"
    ]
  }
  ```
- SubQ returns: `Missing Stripe webhook secret environment variable (confidence: 99.1%)`.
- Agent immediately tells the user the exact issue and offers to update `.env`.
