from django.core.management.base import BaseCommand, CommandError
from django.core.urlresolvers import resolve
from acipenser.models import AvailableRequest
from acipenser.settings import ACIPENSER_SETTINGS
from acipenser.loader import loader
import unittest
import pickle
import ujson
import time


class Command(BaseCommand):

    def add_arguments(self, parser):
        # Positional arguments

        # Named (optional) arguments
        parser.add_argument(
            '-s',
            '--safe',
            type=bool,
            default=False,
            # help='run test if request not update db',
        )

    def handle(self, *args, **options):
        is_safe = options.get('safe', True)
        runner = TestRunner(is_safe=is_safe)
        runner.run()


class TestRunner(object):
    test_limit = 100

    def __init__(self, is_safe=True):
        self.force_run = not is_safe

    @property
    def __need_test_request(self):
        if self.force_run:
            return AvailableRequest.objects.all()
        return AvailableRequest.objects.filter(db_updated=False)

    def test_request(self, request):
        if request.path in ACIPENSER_SETTINGS['CUSTOM_LIST']:
            test_cast = loader(request.path)(request=request, methodName='test_request')
        else:
            test_cast = TestFactory(request=request, methodName='test_request')
        self.suite.addTest(test_cast)

    def run(self):
        self.suite = unittest.TestSuite()
        list(map(self.test_request,
                 self.__need_test_request[:self.test_limit]))
        runner = unittest.TextTestRunner()
        runner.run(self.suite)


class TestFactory(unittest.TestCase):

    def __init__(self, request=None, **kargs):
        super(TestFactory, self).__init__(**kargs)
        self.cache_request = request
        self.response = pickle.loads(request.response)
        self.request = pickle.loads(request.request)
        print("running test: {request}".format(request=self.request))

    @property
    def errors(self):
        return "failed at: %s [%s]" % (self.request.path, self.cache_request.id)

    def format_respone(self, response):
        try:
            current_res = ujson.loads(response.content)
            cache_res = ujson.loads(self.response.content)
        except:
            current_res = response.content
            cache_res = self.response.content
        return current_res, cache_res

    def only_check_status(self, response):
        self.assertEqual(200, response.status_code)

    def test_request(self):
        view, _args, _kwargs = resolve(self.request.path)
        response = view(self.request, *_args, **_kwargs)

        current_res, cache_res = self.format_respone(response)

        if self.request.path in ACIPENSER_SETTINGS['HOG_LIST']:
            self.only_check_status(response)
            return

        if isinstance(current_res, dict):
            self.assertDictEqual(current_res, cache_res, self.errors)
        elif isinstance(current_res, list):
            self.assertListEqual(current_res, cache_res, self.errors)
        else:
            self.assertEqual(response.content, self.response.content, self.errors)
