import json
import logging

import requests
from django.http import JsonResponse
from rest_framework import status
from rest_framework.viewsets import ModelViewSet

from api.models import CustomerRequest
from api.serializers import CustomerRequestSerializer
from api.utils import process_packs_data

logger = logging.getLogger(__name__)


# Create your views here.
class CustomerRequestModelViewSet(ModelViewSet):
    serializer_class = CustomerRequestSerializer
    queryset = CustomerRequest.objects.all()
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        if 'customer_id' not in request.data:
            logger.error('Missing customer id')
            return JsonResponse(data={
                'message': 'Customer id is required'
            }, status=status.HTTP_400_BAD_REQUEST)

        customer_id = request.data['customer_id']

        pack1_response = requests.get('https://6466e9a7ba7110b663ab51f2.mockapi.io/api/v1/pack1')
        pack1_data = pack1_response.json()
        pack2_response = requests.get('https://6466e9a7ba7110b663ab51f2.mockapi.io/api/v1/pack2')
        pack2_data = pack2_response.json()

        [pack1, pack2] = process_packs_data(pack1_data, pack2_data, customer_id)

        serializer = CustomerRequestSerializer(data={
            'customer_id': customer_id,
            'pack1': json.dumps(pack1) if pack1 else '',
            'pack2': json.dumps(pack2) if pack2 else '',
        })
        if serializer.is_valid():
            customer_request = serializer.save()
            return JsonResponse({
                'id': customer_request.id,
                'customer_id': customer_id,
                'pack1': pack1 if pack1 else '',
                'pack2': pack2 if pack2 else '',
            }, status=status.HTTP_200_OK)

        logger.error('Error occurred while serializing data')
        return JsonResponse(data={
            'message': 'An error occurred'
        }, status=status.HTTP_400_BAD_REQUEST)
