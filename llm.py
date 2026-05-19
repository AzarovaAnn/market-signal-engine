"""
Thin LLM wrapper using LiteLLM for provider-agnostic model calls.

Supports Anthropic, OpenAI, Google, Mistral, and any provider LiteLLM supports.
Configure via environment variables:
  - LLM_MODEL: model identifier (default: anthropic/claude-haiku-4-5-20251001)
  - LLM_CLASSIFY_MODEL: override model for classification (optional)
  - LLM_ACTIVATE_MODEL: override model for activation (optional)

Model format follows LiteLLM conventions:
  - Anthropic: anthropic/claude-haiku-4-5-20251001
  - OpenAI:    openai/gpt-4o-mini
  - Google:    gemini/gemini-2.0-flash
  - Mistral:   mistral/mistral-small-latest

Set the appropriate API key env var for your provider:
  - ANTHROPIC_API_KEY, OPENAI_API_KEY, GEMINI_API_KEY, MISTRAL_API_KEY, etc.
"""

import os

from litellm import completion


DEFAULT_MODEL = "anthropic/claude-haiku-4-5-20251001"


def get_model(task: str = "default") -> str:
    """Get the model to use for a given task.
    Checks task-specific override first, then falls back to LLM_MODEL, then default."""
    task_var = f"LLM_{task.upper()}_MODEL"
    return os.environ.get(task_var) or os.environ.get("LLM_MODEL") or DEFAULT_MODEL


def chat(
    system: str,
    user: str,
    task: str = "default",
    max_tokens: int = 1000,
) -> str:
    """Send a chat completion request and return the text response."""
    model = get_model(task)
    response = completion(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        max_tokens=max_tokens,
    )
    return response.choices[0].message.content
