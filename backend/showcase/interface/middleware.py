"""API パスでは DEBUG=True でも HTML エラーページを JSON に揃える。"""

from http import HTTPStatus

from showcase.interface.responses import json_response

_API_PREFIX = "/api/"

# Django の handler404 は DEBUG 時は使われないため、HTML になったステータスを JSON に寄せる。
_STATUS_TO_CODE: dict[HTTPStatus, tuple[str, str]] = {
    HTTPStatus.BAD_REQUEST: ("bad_request", "Bad request"),
    HTTPStatus.FORBIDDEN: ("forbidden", "Forbidden"),
    HTTPStatus.NOT_FOUND: ("not_found", "Not found"),
    HTTPStatus.METHOD_NOT_ALLOWED: ("method_not_allowed", "Method not allowed"),
    HTTPStatus.INTERNAL_SERVER_ERROR: (
        "internal_server_error",
        "Internal server error",
    ),
}


def _is_json_response(response) -> bool:
    content_type = response.get("Content-Type", "").split(";")[0].strip().lower()
    return content_type == "application/json"


class ApiJsonErrorMiddleware:
    """`/api/` 配下で、HTML のエラーレスポンスを共通 JSON 形式に置き換える。"""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if not request.path.startswith(_API_PREFIX):
            return response
        try:
            status = HTTPStatus(response.status_code)
        except ValueError:
            return response
        if status not in _STATUS_TO_CODE:
            return response
        if _is_json_response(response):
            return response
        code, message = _STATUS_TO_CODE[status]
        return json_response({"code": code, "message": message}, status=status)
