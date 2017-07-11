from django.utils.deprecation import MiddlewareMixin
from django.db import connection
from django.test import RequestFactory
from acipenser.models import *
from functools import reduce
from django.contrib.auth.models import AnonymousUser
import pickle
import re
import hashlib


class AcipenserMiddleware(MiddlewareMixin):

    def __is_db_update(self, query):
        sql = query.get('sql', '')
        sql_action = sql.split(' ')[0]
        __update_keys = ["UPDATE", "INSERT"]
        if sql_action in __update_keys:
            return True
        return False

    def check_queries(self, result, query):
        return result | self.__is_db_update(query)

    def count_request_md5(self, request, response):
        method = request.method.upper()
        data = "%s;%s;%s" % (request.path, getattr(
            request, method), response.content)
        m = hashlib.md5()
        m.update(data.encode())
        return m.hexdigest()

    def process_response(self, request, response):
        db_queries = connection.queries
        db_updated = reduce(self.check_queries, db_queries, False)

        method = request.method.upper()
        request_data = getattr(request, method)
        fake_request = RequestFactory().generic(request.method, request.get_full_path(),
                                                data=request._stream, content_type=request.content_type)
        setattr(fake_request, method, request_data)

        fake_request.COOKIES = request.COOKIES

        if hasattr(request, 'user'):
            fake_request.user = request.user
        else:
            fake_request.user = AnonymousUser()


        fake_request_obj = pickle.dumps(fake_request)
        fake_respones_obj = pickle.dumps(fake_request)
        RequestCache.objects.create(path=request.path, method=request.method, request=fake_request_obj, response=pickle.dumps(
            response), db_updated=db_updated, request_md5=self.count_request_md5(request, response))
        return response
