import json
from django.http.response import HttpResponse
from django.http import Http404

class ExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        data = {
            "detail": "Server error: "+str(exception)
        }
        return HttpResponse(json.dumps(data), status=500)