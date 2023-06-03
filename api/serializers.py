import json

from rest_framework import serializers

from api.models import CustomerRequest


class CustomerRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerRequest
        fields = '__all__'
        extra_kwargs = {'customer_id': {
            'error_messages': {'invalid': 'Customer ID is invalid'}
        }}

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        pack1 = representation['pack1']
        pack2 = representation['pack2']
        representation['pack1'] = json.loads(pack1) if pack1 else None
        representation['pack2'] = json.loads(pack2) if pack2 else None
        return representation


class InputSerializer(serializers.Serializer):
    customer_id = serializers.IntegerField(error_messages={'required': 'Customer ID is required'})


class ErrorSerializer(serializers.Serializer):
    message = serializers.CharField()
