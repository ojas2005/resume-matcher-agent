"""Optional LLM client. Returns None when no model is configured, so the agent falls back to rules."""

import os

from app.config import get_settings
from app.logging_config import get_logger

log = get_logger(__name__)

_KEY_FOR_PROVIDER = {
    "openai": "OPENAI_API_KEY",
    "azure_openai": "AZURE_OPENAI_API_KEY",
    "anthropic": "ANTHROPIC_API_KEY",
    "ollama": None,
}


def get_llm():
    settings = get_settings()
    if not settings.use_llm:
        return None
    key_name = _KEY_FOR_PROVIDER.get(settings.llm_provider)
    if key_name and not os.getenv(key_name):
        log.info("No %s set, running in rule-based mode", key_name)
        return None
    try:
        from langchain.chat_models import init_chat_model

        return init_chat_model(
            settings.llm_model,
            model_provider=settings.llm_provider,
            temperature=settings.llm_temperature,
        )
    except Exception as exc:  # missing provider package, bad config, etc.
        log.warning("Could not initialise LLM (%s), using rule-based mode", exc)
        return None
