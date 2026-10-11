from .request_data import bearer_token, request_data


def _present(data, key):
    value = data.get(key)
    return isinstance(value, str) and bool(value.strip())


def verify_fields_none(request, method):
    data = request_data(request)
    if method == "create":
        return (
            all(_present(data, key) for key in ("email", "password", "username"))
            and len(data["password"]) <= 128
        )
    if method == "login":
        return (
            all(_present(data, key) for key in ("email", "password"))
            and len(data["password"]) <= 128
        )
    if method == "update":
        return _present(data, "current_password") and any(
            _present(data, key) for key in ("username", "new_password")
        )
    if method in ("logout", "delete"):
        return bearer_token(request) is not None
    if method == "active":
        return _present(request.GET, "token")
    return False
