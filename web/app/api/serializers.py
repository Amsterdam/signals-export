from rest_framework import serializers

from datasets import models

from datapunt_api.rest import HALSerializer


class ExternalAPISerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ExternalAPI


class SignalSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Signal
