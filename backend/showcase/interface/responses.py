from http import HTTPStatus

from django.http import JsonResponse


def json_response(payload: dict, status: HTTPStatus = HTTPStatus.OK) -> JsonResponse:
    """UTF-8 の JSON レスポンスを返す共通ヘルパー。"""
    return JsonResponse(
        data=payload, status=status.value, json_dumps_params={"ensure_ascii": False}
    )
