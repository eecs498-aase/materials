"""The one place this program talks to a model.

Standard library only: a POST to the Ollama endpoint named in OLLAMA_API_BASE.
Read-only reference material for the L03 demo -- worth having in the repo map
so you can see what "which files does the model need to read?" feels like
when the answer is "none of them."

Every failure path returns None. A transcript analysis that cannot reach a
model still has to print its word counts.
"""

import json
import os
import urllib.error
import urllib.request

DEFAULT_HOST = "http://127.0.0.1:11434"
DEFAULT_MODEL = "qwen3.5:4b"
REQUEST_TIMEOUT_SECONDS = 120

SUMMARY_PROMPT = (
    "Summarize this meeting transcript in one paragraph of at most four "
    "sentences. Name the decisions that were made and who owns the follow-up. "
    "Do not add anything the transcript does not say.\n\nTRANSCRIPT:\n{text}"
)


def _endpoint() -> str:
    """The Ollama generate endpoint, honoring OLLAMA_API_BASE."""
    base = os.environ.get("OLLAMA_API_BASE", DEFAULT_HOST).rstrip("/")
    return f"{base}/api/generate"


def _post(request: dict) -> dict | None:
    """POST `request` to Ollama and return the decoded body, or None.

    None covers all of: no server listening, model not pulled, field the
    server does not understand, request timed out, response was not JSON.
    """
    encoded = json.dumps(request).encode("utf-8")
    call = urllib.request.Request(
        _endpoint(),
        data=encoded,
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(call, timeout=REQUEST_TIMEOUT_SECONDS) as response:
            return json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, OSError):
        return None


def summarize(text: str, model: str | None = None) -> str | None:
    """Return a one-paragraph summary of `text`, or None if that fails.

    The caller decides what an absent summary means; here a model that cannot
    be reached is never an error worth crashing over.
    """
    request = {
        "model": model or os.environ.get("SUMMARY_MODEL", DEFAULT_MODEL),
        "prompt": SUMMARY_PROMPT.format(text=text),
        "stream": False,
        # qwen3.5 reasons before it answers unless you tell it not to, which
        # turns a two second summary into a two minute one. Older Ollama
        # builds reject the field, so `_post` retries without it.
        "think": False,
    }
    body = _post(request)
    if body is None and "think" in request:
        del request["think"]
        body = _post(request)
    if body is None:
        return None

    summary = body.get("response")
    if not isinstance(summary, str) or not summary.strip():
        return None
    return summary.strip()
