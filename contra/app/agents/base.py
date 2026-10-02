"""Base Agent class for Contra."""

import logging
from typing import Dict, Any, Optional
from contra.app.core.llm import llm_client

logger = logging.getLogger("contra.agents")


class BaseAgent:
    def __init__(self, name: str, role_description: str):
        self.name = name
        self.role_description = role_description
        self.llm = llm_client

    async def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError
