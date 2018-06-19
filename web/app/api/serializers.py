from rest_framework import serializers

from datasets import models

from datapunt_api.rest import HALSerializer


class MessageLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MessageLog
        fields = '__all__'
