import json
from http import HTTPStatus
from uuid import UUID

from django.db import DatabaseError, connection
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from showcase.application.create_my_dog import CreateMyDogUseCase
from showcase.application.delete_my_dog import DeleteMyDogUseCase
from showcase.application.get_dog import GetDogUseCase
from showcase.application.get_my_profile import GetMyProfileUseCase
from showcase.application.list_all_dogs import ListAllDogsUseCase
from showcase.application.list_breeds import ListBreedsUseCase
from showcase.application.login_owner import LoginFailedError, LoginOwnerUseCase
from showcase.application.refresh_access_token import (
    RefreshAccessTokenUseCase,
    RefreshTokenInvalidError,
)
from showcase.application.register_owner import RegisterOwnerUseCase
from showcase.application.update_my_dog import UpdateMyDogUseCase
from showcase.application.update_my_profile import UpdateMyProfileUseCase
from showcase.domain.exceptions import (
    DomainValidationError,
    EmailAlreadyRegisteredError,
)
from showcase.infrastructure import DjangoBreedRepository, DjangoOwnerRepository
from showcase.infrastructure.django_repositories import DjangoDogRepository
from showcase.interface.auth import OwnerAuthError, get_current_owner_id
from showcase.interface.responses import json_response
from showcase.interface.serializers import (
    breed_to_json,
    dog_to_json,
    login_result_to_json,
    owner_to_json,
    refresh_access_to_json,
)


def parse_request_payload(request) -> dict:
    content_type = (request.content_type or "").split(";")[0].strip().lower()
    if content_type == "application/json":
        if not request.body:
            return {}
        try:
            payload = json.loads(request.body.decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            raise ValueError("Invalid JSON body") from exc
        if not isinstance(payload, dict):
            raise ValueError("JSON body must be an object")
        return payload
    return request.POST.dict()


def _unauthorized_json(message: str):
    return json_response(
        {"code": "unauthorized", "message": message},
        status=HTTPStatus.UNAUTHORIZED,
    )


# Health Check
def health(_request):
    """ヘルスチェックを返す。"""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
    except DatabaseError:
        return json_response(
            {"code": "service_unavailable", "message": "Database unavailable"},
            status=HTTPStatus.SERVICE_UNAVAILABLE,
        )
    return json_response({"status": "ok"})


# Auth / Owner profile（Bearer 時は JWT、無ければスタブ Owner ID）
def get_auth_me(request):
    try:
        owner_id = get_current_owner_id(request)
    except OwnerAuthError as exc:
        return _unauthorized_json(str(exc))
    use_case = GetMyProfileUseCase(DjangoOwnerRepository())
    owner = use_case.execute(owner_id)
    if owner is None:
        return json_response(
            {"code": "not_found", "message": "Owner not found"},
            status=HTTPStatus.NOT_FOUND,
        )
    return json_response(owner_to_json(owner))


def patch_auth_me(request):
    try:
        owner_id = get_current_owner_id(request)
        payload = parse_request_payload(request)
        use_case = UpdateMyProfileUseCase(DjangoOwnerRepository())
        owner = use_case.execute(owner_id, payload)
        if owner is None:
            return json_response(
                {"code": "not_found", "message": "Owner not found"},
                status=HTTPStatus.NOT_FOUND,
            )
        return json_response(owner_to_json(owner))
    except ValueError as exc:
        return json_response(
            {"code": "bad_request", "message": str(exc)},
            status=HTTPStatus.BAD_REQUEST,
        )
    except DomainValidationError as exc:
        return json_response(
            {"code": "bad_request", "message": str(exc)},
            status=HTTPStatus.BAD_REQUEST,
        )
    except OwnerAuthError as exc:
        return _unauthorized_json(str(exc))


@csrf_exempt  # NOTE: 開発中の Postman 動作確認用。認証実装時に外す。
def auth_me(request):
    """`/api/auth/me/` の GET / PATCH。現在のオーナープロフィール。"""
    match request.method:
        case "GET":
            return get_auth_me(request)
        case "PATCH":
            return patch_auth_me(request)
        case _:
            return json_response(
                {"code": "method_not_allowed", "message": "Method not allowed"},
                status=HTTPStatus.METHOD_NOT_ALLOWED,
            )


def post_auth_register(request):
    """`/api/auth/register/` の POST。メール・パスワード・ニックネームで Owner を新規作成。"""
    try:
        payload = parse_request_payload(request)
        use_case = RegisterOwnerUseCase(DjangoOwnerRepository())
        owner = use_case.execute(payload)
        return json_response(owner_to_json(owner), status=HTTPStatus.CREATED)
    except ValueError as exc:
        return json_response(
            {"code": "bad_request", "message": str(exc)},
            status=HTTPStatus.BAD_REQUEST,
        )
    except DomainValidationError as exc:
        return json_response(
            {"code": "bad_request", "message": str(exc)},
            status=HTTPStatus.BAD_REQUEST,
        )
    except EmailAlreadyRegisteredError:
        return json_response(
            {
                "code": "email_already_registered",
                "message": "このメールアドレスは既に登録されています",
            },
            status=HTTPStatus.CONFLICT,
        )


@csrf_exempt  # NOTE: 開発中の Postman 動作確認用。認証実装時に外す。
def auth_register(request):
    """`/api/auth/register/` の POST のみ。"""
    if request.method != "POST":
        return json_response(
            {"code": "method_not_allowed", "message": "Method not allowed"},
            status=HTTPStatus.METHOD_NOT_ALLOWED,
        )
    return post_auth_register(request)


def post_auth_login(request):
    """`/api/auth/login/` の POST。メール・パスワードで JWT を発行する。"""
    try:
        payload = parse_request_payload(request)
        use_case = LoginOwnerUseCase(DjangoOwnerRepository())
        result = use_case.execute(payload)
        return json_response(
            login_result_to_json(
                access=result.access,
                refresh=result.refresh,
                owner=result.owner,
            )
        )
    except ValueError as exc:
        return json_response(
            {"code": "bad_request", "message": str(exc)},
            status=HTTPStatus.BAD_REQUEST,
        )
    except DomainValidationError as exc:
        return json_response(
            {"code": "bad_request", "message": str(exc)},
            status=HTTPStatus.BAD_REQUEST,
        )
    except LoginFailedError:
        return json_response(
            {
                "code": "invalid_credentials",
                "message": "メールアドレスまたはパスワードが正しくありません",
            },
            status=HTTPStatus.UNAUTHORIZED,
        )


@csrf_exempt  # NOTE: 開発中の Postman 動作確認用。認証実装時に外す。
def auth_login(request):
    """`/api/auth/login/` の POST のみ。"""
    if request.method != "POST":
        return json_response(
            {"code": "method_not_allowed", "message": "Method not allowed"},
            status=HTTPStatus.METHOD_NOT_ALLOWED,
        )
    return post_auth_login(request)


def post_auth_refresh(request):
    """`/api/auth/refresh/` の POST。リフレッシュトークンから access を再発行する。"""
    try:
        payload = parse_request_payload(request)
        use_case = RefreshAccessTokenUseCase()
        access = use_case.execute(payload)
        return json_response(refresh_access_to_json(access=access))
    except ValueError as exc:
        return json_response(
            {"code": "bad_request", "message": str(exc)},
            status=HTTPStatus.BAD_REQUEST,
        )
    except RefreshTokenInvalidError:
        return json_response(
            {
                "code": "invalid_refresh_token",
                "message": "リフレッシュトークンが無効または期限切れです",
            },
            status=HTTPStatus.UNAUTHORIZED,
        )


@csrf_exempt  # NOTE: 開発中の Postman 動作確認用。認証実装時に外す。
def auth_refresh(request):
    """`/api/auth/refresh/` の POST のみ。"""
    if request.method != "POST":
        return json_response(
            {"code": "method_not_allowed", "message": "Method not allowed"},
            status=HTTPStatus.METHOD_NOT_ALLOWED,
        )
    return post_auth_refresh(request)


# Dogs
def dogs_list(request):
    """`/api/dogs/` の GET。認証不要（全件閲覧用）。"""
    if request.method != "GET":
        return json_response(
            {"code": "method_not_allowed", "message": "Method not allowed"},
            status=HTTPStatus.METHOD_NOT_ALLOWED,
        )
    use_case = ListAllDogsUseCase(DjangoDogRepository())
    dogs = use_case.execute()
    return json_response({"items": [dog_to_json(d) for d in dogs]})


def create_my_dog(request):
    """`/api/dogs/` の POST。現在のオーナーに犬を登録する。"""
    try:
        owner_id = get_current_owner_id(request)
        use_case = CreateMyDogUseCase(DjangoDogRepository())
        payload = parse_request_payload(request)
        dog = use_case.execute(owner_id, payload)
        return json_response(payload=dog_to_json(dog), status=HTTPStatus.CREATED)
    except OwnerAuthError as exc:
        return _unauthorized_json(str(exc))
    except ValueError as exc:
        return json_response(
            {"code": "bad_request", "message": str(exc)},
            status=HTTPStatus.BAD_REQUEST,
        )
    except Exception as exc:
        return json_response(
            {"code": "internal_server_error", "message": str(exc)},
            status=HTTPStatus.INTERNAL_SERVER_ERROR,
        )


@csrf_exempt  # NOTE: 開発中の Postman 動作確認用。認証実装時に外す。
def dogs(request):
    """`/api/dogs/` の GET/POST をディスパッチする。"""
    if request.method == "GET":
        return dogs_list(request)
    if request.method != "POST":
        return json_response(
            {"code": "method_not_allowed", "message": "Method not allowed"},
            status=HTTPStatus.METHOD_NOT_ALLOWED,
        )
    return create_my_dog(request)


def patch_my_dog_detail(request, dog_id: UUID):
    """`/api/dogs/<dog_id>/` の PATCH。本人の犬のみ部分更新。"""
    try:
        owner_id = get_current_owner_id(request)
        payload = parse_request_payload(request)
        use_case = UpdateMyDogUseCase(DjangoDogRepository())
        dog = use_case.execute(owner_id, dog_id, payload)
        if dog is None:
            return json_response(
                {"code": "not_found", "message": "Dog not found"},
                status=HTTPStatus.NOT_FOUND,
            )
        return json_response(dog_to_json(dog))
    except OwnerAuthError as exc:
        return _unauthorized_json(str(exc))
    except ValueError as exc:
        return json_response(
            {"code": "bad_request", "message": str(exc)},
            status=HTTPStatus.BAD_REQUEST,
        )
    except DomainValidationError as exc:
        return json_response(
            {"code": "bad_request", "message": str(exc)},
            status=HTTPStatus.BAD_REQUEST,
        )


def delete_my_dog_detail(request, dog_id: UUID):
    """`/api/dogs/<dog_id>/` の DELETE。本人の犬のみ。"""
    try:
        owner_id = get_current_owner_id(request)
    except OwnerAuthError as exc:
        return _unauthorized_json(str(exc))
    use_case = DeleteMyDogUseCase(DjangoDogRepository())
    if use_case.execute(owner_id, dog_id) == 0:
        return json_response(
            {"code": "not_found", "message": "Dog not found"},
            status=HTTPStatus.NOT_FOUND,
        )
    return HttpResponse(status=HTTPStatus.NO_CONTENT)


@csrf_exempt  # NOTE: 開発中の Postman 動作確認用。認証実装時に外す。
def dog_detail(request, dog_id: UUID):
    """`/api/dogs/<dog_id>/` の GET（認証不要）/ PATCH・DELETE（オーナー要・スタブ）。"""
    match request.method:
        case "GET":
            use_case = GetDogUseCase(DjangoDogRepository())
            dog = use_case.execute(dog_id)
            if dog is None:
                return json_response(
                    {"code": "not_found", "message": "Dog not found"},
                    status=HTTPStatus.NOT_FOUND,
                )
            return json_response(dog_to_json(dog))
        case "PATCH":
            return patch_my_dog_detail(request, dog_id)
        case "DELETE":
            return delete_my_dog_detail(request, dog_id)
        case _:
            return json_response(
                {"code": "method_not_allowed", "message": "Method not allowed"},
                status=HTTPStatus.METHOD_NOT_ALLOWED,
            )


# Breeds
def breeds_list(request):
    """犬種一覧を返す。"""
    if request.method != "GET":
        return json_response(
            {"code": "method_not_allowed", "message": "Method not allowed"},
            status=HTTPStatus.METHOD_NOT_ALLOWED,
        )
    use_case = ListBreedsUseCase(DjangoBreedRepository())
    breeds = use_case.execute()
    return json_response({"items": [breed_to_json(b) for b in breeds]})
