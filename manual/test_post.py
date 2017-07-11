from django.core.urlresolvers import resolve
from .base import TestMixin
import ujson


class PostTest(TestMixin):
    path = "/image_search/get_posts/"

    def test_request(self):
        view, _args, _kwargs = resolve(self.request.path)
        response = view(self.request, *_args, **_kwargs)
        json_response = ujson.loads(response.content)
        self.check_old_status(json_response)
