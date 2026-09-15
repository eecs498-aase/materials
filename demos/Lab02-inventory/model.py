"""A transport boundary, with no agent policy or tool dispatcher."""
import json
import os
import urllib.error
import urllib.request


def complete(messages: list[dict], **options) -> dict:
    """Return an assistant message from a configured Chat Completions endpoint."""
    base = os.environ.get('MODEL_BASE_URL', '').rstrip('/')
    model = os.environ.get('MODEL_NAME', '')
    if not base or not model:
        raise ValueError('set MODEL_BASE_URL (ending /v1) and MODEL_NAME')
    payload = {'model': model, 'messages': messages, 'stream': False, **options}
    headers = {'Content-Type': 'application/json'}
    if key := os.environ.get('MODEL_API_KEY'):
        headers['Authorization'] = f'Bearer {key}'
    request = urllib.request.Request(base + '/chat/completions',
                                     json.dumps(payload).encode(), headers)
    try:
        with urllib.request.urlopen(request, timeout=float(os.environ.get('MODEL_TIMEOUT', '90'))) as response:
            result = json.load(response)
        message = result['choices'][0]['message']
        if not isinstance(message, dict):
            raise ValueError('invalid assistant message')
        return message
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f'model HTTP error {exc.code}') from None
    except (urllib.error.URLError, TimeoutError):
        raise RuntimeError('model endpoint unavailable or timed out') from None
    except (KeyError, IndexError, json.JSONDecodeError):
        raise RuntimeError('invalid model response envelope') from None
