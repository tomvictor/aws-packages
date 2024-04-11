from http import HTTPStatus

from aws_lambda_powertools.event_handler import Response, content_types


def success_message(message="ok", status_code=HTTPStatus.OK.value):
    return Response(
        status_code=status_code,
        content_type=content_types.APPLICATION_JSON,
        body={"message": message},
    )


def success_response(data, status_code=HTTPStatus.OK.value):
    return Response(
        status_code=status_code,
        content_type=content_types.APPLICATION_JSON,
        body=data,
    )
