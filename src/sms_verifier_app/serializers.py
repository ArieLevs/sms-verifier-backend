# REST API
from rest_framework import serializers


class ApproveGuestSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(required=True)
    attending = serializers.BooleanField(required=True)
    num_of_guests = serializers.IntegerField(required=True)
