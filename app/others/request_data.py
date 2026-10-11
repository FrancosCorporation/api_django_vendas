import json

from django.http import QueryDict


def request_data(request):
    """Return structured request-body data; credentials must not come from query strings."""
    content_type = request.content_type or ""
    if content_type == "application/json":
        try:
            value = json.loads(request.body or b"{}")
        except (UnicodeDecodeError, json.JSONDecodeError):
            return {}
        return value if isinstance(value, dict) else {}

    if request.method == "POST":
        return request.POST.dict()

    try:
        return QueryDict(request.body.decode("utf-8")).dict()
    except (UnicodeDecodeError, ValueError):
        return {}


def bearer_token(request):
    """Read a bearer token without accepting credentials from a URL or body."""
    authorization = request.headers.get("Authorization", "")
    scheme, separator, token = authorization.partition(" ")
    if not separator or scheme.lower() != "bearer" or not token or " " in token:
        return None
    return token
