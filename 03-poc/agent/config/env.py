"""Load the POC .env file into the process environment.

All POC modules read credentials/base URLs from os.environ. This module resolves the
.env path relative to this file (03-poc/agent/.env) so it works no matter what the
working directory is, and exposes load_env() which tools/__init__, ingestion, and
orchestrator call BEFORE reading their variables. Without this, a fresh shell running
`python -c "from tools.jira_tool import ..."` sees every var as empty.
"""
import os
from pathlib import Path

from dotenv import dotenv_values, load_dotenv

_ENV_FILE = Path(__file__).resolve().parents[1] / ".env"


def load_env() -> Path:
    """Load .env into os.environ. Safe to call repeatedly."""
    load_dotenv(_ENV_FILE, override=False)
    vals = dotenv_values(_ENV_FILE)
    # The .env file is the documented source of truth for LLM provider config
    # (CLAUDE.md rule 5). load_dotenv(override=False) above lets a stale value
    # inherited from the shell/IDE/Claude-Code harness shadow the .env value (e.g. an
    # old ANTHROPIC_API_KEY), so re-apply these three explicitly.
    for key in ("ANTHROPIC_API_KEY", "ANTHROPIC_BASE_URL", "LLM_MODEL"):
        if vals.get(key):
            os.environ[key] = vals[key]
    # Claude Code spawns child processes with ANTHROPIC_BASE_URL set to its own local
    # session proxy (http://localhost:<port>/v1). If .env did not set a base URL the
    # harness value would leak through above, so drop any inherited localhost proxy.
    base = os.environ.get("ANTHROPIC_BASE_URL", "")
    if base.startswith("http://localhost:") or base.startswith("http://127.0.0.1:"):
        os.environ.pop("ANTHROPIC_BASE_URL", None)
    return _ENV_FILE
