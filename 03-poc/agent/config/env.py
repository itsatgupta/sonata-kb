"""Load the POC .env file into the process environment.

All POC modules read credentials/base URLs from os.environ. This module resolves the
.env path relative to this file (03-poc/agent/.env) so it works no matter what the
working directory is, and exposes load_env() which tools/__init__, ingestion, and
orchestrator call BEFORE reading their variables. Without this, a fresh shell running
`python -c "from tools.jira_tool import ..."` sees every var as empty.
"""
import os
from pathlib import Path

from dotenv import load_dotenv

_ENV_FILE = Path(__file__).resolve().parents[1] / ".env"


def load_env() -> Path:
    """Load .env into os.environ. Safe to call repeatedly (no override)."""
    load_dotenv(_ENV_FILE, override=False)
    # Claude Code spawns child processes with ANTHROPIC_BASE_URL set to its own local
    # session proxy (http://localhost:<port>/v1). The POC orchestrator must call the
    # real Anthropic API with the .env key, so drop any inherited localhost proxy.
    # A non-localhost base URL (e.g. a corporate gateway set in .env or the shell)
    # is preserved.
    base = os.environ.get("ANTHROPIC_BASE_URL", "")
    if base.startswith("http://localhost:") or base.startswith("http://127.0.0.1:"):
        os.environ.pop("ANTHROPIC_BASE_URL", None)
    return _ENV_FILE
