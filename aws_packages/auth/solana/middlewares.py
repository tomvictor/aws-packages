"""Auth middleware."""

from aws_lambda_powertools.event_handler import APIGatewayRestResolver, Response
from aws_lambda_powertools.event_handler.exceptions import UnauthorizedError
from aws_lambda_powertools.event_handler.middlewares import NextMiddleware

from aws_packages.auth.models import AuthorizationRequest

from .auth_backend import solana_auth_backend


def solana_login_required(
    app: APIGatewayRestResolver, next_middleware: NextMiddleware
) -> Response:
    """Login required middleware

    :param app: application instance
    :param next_middleware: next middleware
    :return: Response object after the middleware has been applied
    """

    request = AuthorizationRequest(**app.current_event.headers)
    try:
        access_token_obj = solana_auth_backend.authenticate_with_token(request.token)
    except Exception as exc:
        raise UnauthorizedError(f"Unauthorized: {exc}")

    token_payload = access_token_obj.get_payload()
    print(f"Token payload: {token_payload}")

    user_id = token_payload.get("user_id", None)
    if user_id is None:
        raise UnauthorizedError(f"Unauthorized: no user present")
    setattr(app.current_event, "user_id", user_id)
    return next_middleware(app)
