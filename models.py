from __future__ import unicode_literals

from django.db import models
import time


class Request(models.Model):
    id = models.AutoField(primary_key=True)
    path = models.CharField(max_length=512, db_index=True)
    method = models.CharField(max_length=16)
    request = models.BinaryField(default=b'')
    request_md5 = models.CharField(max_length=64, default='', db_index=True)
    response = models.BinaryField(default=b'')
    db_updated = models.BooleanField(default=False)
    create_at = models.IntegerField(default=time.time)

    class Meta:
        abstract = True


class RequestCache(Request):

    class Meta:
        app_label = 'test_db'


class AvailableRequest(Request):
    request_md5 = models.CharField(max_length=64, default='', db_index=True, unique=True)

    class Meta:
        app_label = 'test_db'

