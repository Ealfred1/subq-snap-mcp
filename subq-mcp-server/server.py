import os
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


@mcp.tool()
async def evaluate_decision(context: str, query: str, candidates: list[str]) -> str:
    """Evaluate massive text/code context (up to 384k tokens) and return the single best discrete decision or choice from a list of candidates in under a second.

    Args:
        context: The raw code, logs, diffs, or documents to analyze.
        query: The specific question or criteria to evaluate (e.g., 'Which file causes this error?').
        candidates: The list of possible options/choices to select from.
    """
    api_key = os.getenv("SUBQ_API_KEY") or SUBQ_API_KEY
    api_url = os.getenv("SUBQ_API_URL") or SUBQ_API_URL

    if not api_key:
        return "Error: SUBQ_API_KEY environment variable is not configured."

    # Build criteria mapping candidate keys to descriptions
    # Handles list of strings by creating distinct identifiers
    criteria = {}
    key_to_candidate = {}
    for idx, c in enumerate(candidates):
        # Create a valid identifier key for SubQ
        safe_key = f"opt_{idx}_{c[:30].strip()}".replace(" ", "_").replace("-", "_").replace(".", "_")
        safe_key = "".join(ch for ch in safe_key if ch.isalnum() or ch == "_").lower()
        criteria[safe_key] = c
        key_to_candidate[safe_key] = c

    payload = {
        "model": SUBQ_MODEL,
        "state": context,
        "questions": {
            "decision": {
                "type": "choice",
                "instructions": query,
                "criteria": criteria
            }
        }
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(api_url, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
            
            # Extract chosen candidate from SubQ answers
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


if __name__ == "__main__":
    mcp.run()
