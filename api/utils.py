import logging

from django.http import JsonResponse
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.views import exception_handler

from api.serializers import ErrorSerializer

logger = logging.getLogger(__name__)


def process_packs_data(pack1_data, pack2_data, customer_id):
    # For processing of data received from endpoints
    pack1 = None
    pack2 = None

    for customer_data in pack1_data:
        if customer_data['customer_id'] == customer_id:
            pack1 = format_pack_data(customer_data['pack_data'])
            break

    for customer_data in pack2_data:
        if customer_data['customer_id'] == customer_id:
            pack2 = format_pack_data(customer_data['pack_data'])
            break

    return [pack1, pack2]


def format_pack_data(pack_data):
    # to parse and format packs data
    info = []
    for data in pack_data:
        info.append(f'{data["ingredient"]} {data["quantity"]}{data["unit"]}')
    return info


def format_serializer_validation_errors_as_json_response(
        serializer_errors: dict[str, list[ErrorDetail]]) -> JsonResponse:
    errors = []
    for k, v in serializer_errors.items():
        errors.append(str(v[0]))
    errors_str = ''.join(errors)

    logger.error(errors_str)

    return JsonResponse(ErrorSerializer(data={
        'message': errors_str
    }), status=status.HTTP_400_BAD_REQUEST)


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        response.data['status_code'] = response.status_code

    return response
