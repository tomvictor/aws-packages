import json
from http import HTTPStatus

from aws_lambda_powertools.event_handler import Response, content_types
from aws_lambda_powertools.event_handler.exceptions import BadRequestError
from pydantic_core import ValidationError

from aws_packages.auth.auth_backend_abc import AuthBackendBase
from aws_packages.auth.models import LoginResponse, User

from .auth_backend import solana_auth_backend
from .models import SolanaAuthenticationRequest


def _process_authenticate_request(request_body, auth_backend: AuthBackendBase):
    if request_body is None:
        raise BadRequestError("No request body provided")

    try:
        request_obj = SolanaAuthenticationRequest(**json.loads(request_body))
    except ValidationError as e:
        # TODO: user aws package error response
        raise BadRequestError(msg="request validation error")

    try:
        is_verified = auth_backend.authenticate(request_obj)
        if not is_verified:
            return Response(
                status_code=HTTPStatus.BAD_REQUEST.value,
                content_type=content_types.APPLICATION_JSON,
                body={"message": "Message verification failed"},
            )
    except Exception as e:
        # TODO: Raise error instead of response
        return Response(
            status_code=HTTPStatus.BAD_REQUEST.value,
            content_type=content_types.APPLICATION_JSON,
            body={"message": str(e)},
        )

    return Response(
        status_code=HTTPStatus.OK.value,
        content_type=content_types.APPLICATION_JSON,
        body=LoginResponse(
            # TODO: package needs to be updated?
            access_token=auth_backend.get_access_token(
                User(principal=request_obj.public_key)
            )
        ).as_dict(),
    )


def process_solana_authenticate_request(request_body):
    return _process_authenticate_request(request_body, solana_auth_backend)
