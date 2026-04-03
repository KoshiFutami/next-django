"""API パスでは HTML エラーページを JSON に揃える。

DEBUG=True のときは未処理例外を JSON で返し、メッセージとトレースバックを含める
（Postman 等で原因調査できるようにする）。DEBUG=False では汎用メッセージのみ。
"""

import logging
import traceback
from http import HTTPStatus

from django.conf import settings

from showcase.interface.responses import json_response

logger = logging.getLogger(__name__)

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

    def process_exception(self, request, exception):
        """ビューで捕捉されなかった例外を JSON にする（DEBUG 時は詳細付き）。"""
        if not request.path.startswith(_API_PREFIX):
            return None
        logger.exception("Unhandled exception on %s", request.path)
        if settings.DEBUG:
            return json_response(
                {
                    "code": "internal_server_error",
                    "message": str(exception),
                    "exception": exception.__class__.__name__,
                    "traceback": traceback.format_exc(),
                },
                status=HTTPStatus.INTERNAL_SERVER_ERROR,
            )
        return json_response(
            {"code": "internal_server_error", "message": "Internal server error"},
            status=HTTPStatus.INTERNAL_SERVER_ERROR,
        )

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
