from http import HTTPStatus

from aws_lambda_powertools.event_handler import Response, content_types


def success_response(message="ok", status_code=HTTPStatus.OK.value):
    return Response(
        status_code=status_code,
        content_type=content_types.APPLICATION_JSON,
        body={"message": message},
    )
