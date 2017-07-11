from unittest import TestCase
import pickle

class TestMixin(TestCase):

    def __init__(self, request=None, **kargs):
        super(TestMixin, self).__init__(**kargs)
        self.cache_request = request
        self.response = pickle.loads(request.response)
        self.request = pickle.loads(request.request)

    def check_old_status(self, current_respone):
        self.assertEqual(0, current_respone[0]['status'])

    def check_status(self, current_respone):
        self.assertEqual(0, current_respone['meta']['status'])