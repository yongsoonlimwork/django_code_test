import json

import requests
from django.http import JsonResponse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.viewsets import ModelViewSet

from api.models import CustomerRequest
from api.serializers import CustomerRequestSerializer, InputSerializer, ErrorSerializer
from api.utils import process_packs_data, format_serializer_validation_errors_as_json_response


# Create your views here.
class CustomerRequestModelViewSet(ModelViewSet):
    serializer_class = CustomerRequestSerializer
    queryset = CustomerRequest.objects.all()
    http_method_names = ['post']

    @swagger_auto_schema(
        operation_description='Get customer medication info',
        # request_body=openapi.Schema(
        #     type=openapi.TYPE_OBJECT,
        #     required=['customer_id'],
        #     properties={
        #         'customer_id': openapi.Schema(type=openapi.TYPE_NUMBER)
        #     }
        # ),
        request_body=InputSerializer,
        responses={
            # 200: openapi.Response('Success', openapi.Schema(
            #     type=openapi.TYPE_OBJECT,
            #     required=['id', 'customer_id'],
            #     properties={
            #         'id': openapi.Schema(type=openapi.TYPE_NUMBER),
            #         'customer_id': openapi.Schema(type=openapi.TYPE_NUMBER),
            #         'pack1': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING)),
            #         'pack2': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING)),
            #     }
            # )),
            '200': CustomerRequestSerializer,
            '400': ErrorSerializer
        }
    )
    def create(self, request, *args, **kwargs):
        input_serializer = InputSerializer(data=request.data)
        if not input_serializer.is_valid():
            return format_serializer_validation_errors_as_json_response(input_serializer.errors)

        customer_id = input_serializer.data['customer_id']

        pack1_response = requests.get('https://6466e9a7ba7110b663ab51f2.mockapi.io/api/v1/pack1')
        pack1_data = pack1_response.json()
        pack2_response = requests.get('https://6466e9a7ba7110b663ab51f2.mockapi.io/api/v1/pack2')
        pack2_data = pack2_response.json()

        [pack1, pack2] = process_packs_data(pack1_data, pack2_data, customer_id)

        form_serializer = CustomerRequestSerializer(data={
            'customer_id': customer_id,
            'pack1': json.dumps(pack1) if pack1 else '',
            'pack2': json.dumps(pack2) if pack2 else '',
        })
        if form_serializer.is_valid():
            form_serializer.save()
            return JsonResponse(form_serializer.data, status=status.HTTP_200_OK)
        else:
            return format_serializer_validation_errors_as_json_response(form_serializer.errors)
