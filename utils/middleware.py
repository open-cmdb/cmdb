import json
import logging
import traceback

from django.http.response import HttpResponse

logger = logging.getLogger("default")


class ExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        data = {
            "detail": str(exception)
        }
        logger.error(traceback.format_exc())
        return HttpResponse(json.dumps(data), status=500)
