from http import HTTPStatus
import json

from django.db import DatabaseError, connection
from django.views.decorators.csrf import csrf_exempt
from showcase.application.list_breeds import ListBreedsUseCase
from showcase.infrastructure import DjangoBreedRepository
from showcase.interface.responses import json_response
from showcase.application.list_my_dogs import ListMyDogsUseCase
from showcase.infrastructure.django_repositories import DjangoDogRepository
from showcase.interface.auth import get_current_owner_id
from showcase.application.create_dog import CreateDogUseCase
from showcase.interface.serializers import breed_to_json, dog_to_json


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

# Health Check
def health(_request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
    except DatabaseError:
        return json_response(
            {"code": "service_unavailable", "message": "Database unavailable"},
            status=HTTPStatus.SERVICE_UNAVAILABLE,
        )
    return json_response({"status": "ok"})

# Dogs
def dogs_list(request):
    if request.method != "GET":
        return json_response(
            {"code": "method_not_allowed", "message": "Method not allowed"},
            status=HTTPStatus.METHOD_NOT_ALLOWED,
        )
    owner_id = get_current_owner_id(request)
    use_case = ListMyDogsUseCase(DjangoDogRepository())
    dogs = use_case.execute(owner_id)
    return json_response({"items": [dog_to_json(d) for d in dogs]})

def dogs_create(request):
    try:
        owner_id = get_current_owner_id(request)
        use_case = CreateDogUseCase(DjangoDogRepository())
        payload = parse_request_payload(request)
        dog = use_case.execute(owner_id, payload)
        return json_response(
            payload=dog_to_json(dog),
            status=HTTPStatus.CREATED
        )
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
    if request.method == "GET":
        return dogs_list(request)
    if request.method != "POST":
        return json_response(
            {"code": "method_not_allowed", "message": "Method not allowed"},
            status=HTTPStatus.METHOD_NOT_ALLOWED,
        )
    return dogs_create(request)

# Breeds
def breeds_list(request):
    if request.method != "GET":
        return json_response(
            {"code": "method_not_allowed", "message": "Method not allowed"},
            status=HTTPStatus.METHOD_NOT_ALLOWED,
        )
    use_case = ListBreedsUseCase(DjangoBreedRepository())
    breeds = use_case.execute()
    return json_response({"items": [breed_to_json(b) for b in breeds]})

