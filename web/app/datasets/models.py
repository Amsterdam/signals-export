from django.db import models


class MessageLog(models.Model):
    signal_id = models.CharField(max_length=255, unique=True)
    t_entered = models.DateTimeField()
    t_sent = models.DateTimeField(null=True)
    handler_name = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=255, blank=True)
    is_sent = models.BooleanField(default=False)
