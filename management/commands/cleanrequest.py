from django.core.management.base import BaseCommand, CommandError
from acipenser.models import RequestCache, AvailableRequest
import pickle
import time


class Command(BaseCommand):

    def update_safe_request(self, force=False):
        last_available = AvailableRequest.objects.last()
        if not last_available:
            self.last_available_id = 0
        else:
            self.last_available_id = last_available.id
        request_ids = RequestCache.objects.filter(id__gt=self.last_available_id).values('id')

        request_fields = list(map(lambda x:x.name, RequestCache._meta.local_fields))

        for request_id in request_ids:
            requestcache = RequestCache.objects.get(id=request_id['id'])
            new_request = AvailableRequest()
            for field in request_fields:
                setattr(new_request, field, getattr(requestcache, field))
            try:
                new_request.save()
            except Exception as e:
                print("skip request :%s" % requestcache.path)

    def update_unsafe_request(self):
        RequestCache

    def handle(self, *args, **options):
        self.update_safe_request(force=True)
