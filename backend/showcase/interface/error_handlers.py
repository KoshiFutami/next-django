from http import HTTPStatus

from showcase.interface.responses import json_response


def bad_request(_request, exception):
    """400 Bad Request を JSON で返す。"""
    return json_response(
        {"code": "bad_request", "message": str(exception) or "Bad request"},
        status=HTTPStatus.BAD_REQUEST,
    )


def permission_denied(_request, exception):
    """403 Forbidden を JSON で返す。"""
    return json_response(
        {"code": "forbidden", "message": str(exception) or "Permission denied"},
        status=HTTPStatus.FORBIDDEN,
    )


def page_not_found(_request, exception):
    """404 Not Found を JSON で返す。"""
    return json_response(
        {"code": "not_found", "message": str(exception) or "Not found"},
        status=HTTPStatus.NOT_FOUND,
    )


def server_error(_request):
    """500 Internal Server Error を JSON で返す。"""
    return json_response(
        {"code": "internal_server_error", "message": "Internal server error"},
        status=HTTPStatus.INTERNAL_SERVER_ERROR,
    )


def csrf_failure(_request, reason=""):
    """CSRF 検証失敗時の 403 レスポンスを返す。"""
    return json_response(
        {"code": "csrf_failed", "message": reason or "CSRF validation failed"},
        status=HTTPStatus.FORBIDDEN,
    )
