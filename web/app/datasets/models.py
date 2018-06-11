from django.db import models


class ExternalAPI(models.Model):
    name = models.CharField(max_length=255)


class Signal(models.Model):
    signal_id = models.IntegerField()
    datetime_retrieved = models.DateTimeField()
    datetime_sent = models.DateTimeField()
    external_api = models.ForeignKey(ExternalAPI, on_delete=models.CASCADE)
    status = models.CharField(max_length=255)
