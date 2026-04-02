from http import HTTPStatus

from showcase.interface.responses import json_response


def bad_request(_request, exception):
    return json_response(
        {"code": "bad_request", "message": str(exception) or "Bad request"},
        status=HTTPStatus.BAD_REQUEST,
    )


def permission_denied(_request, exception):
    return json_response(
        {"code": "forbidden", "message": str(exception) or "Permission denied"},
        status=HTTPStatus.FORBIDDEN,
    )


def page_not_found(_request, exception):
    return json_response(
        {"code": "not_found", "message": str(exception) or "Not found"},
        status=HTTPStatus.NOT_FOUND,
    )


def server_error(_request):
    return json_response(
        {"code": "internal_server_error", "message": "Internal server error"},
        status=HTTPStatus.INTERNAL_SERVER_ERROR,
    )


def csrf_failure(_request, reason=""):
    return json_response(
        {"code": "csrf_failed", "message": reason or "CSRF validation failed"},
        status=HTTPStatus.FORBIDDEN,
    )
