"""Tool package. Importing it loads the POC .env so every tool module can read its
credentials from os.environ. The sanity-check and eval scripts import tools directly
(not just orchestrator.py), so this side-effect lives here in the package __init__.
"""
from config.env import load_env

load_env()
