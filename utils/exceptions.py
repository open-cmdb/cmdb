import json

from django.http.response import HttpResponseNotFound, HttpResponseServerError
from django.views.defaults import server_error
from rest_framework.views import exception_handler


def interface_not_defined(request, exception, template_name=None):
    return HttpResponseNotFound('{"detail": "The interface not defined!"}')
#
# def server_error(request, template_name=None):
#     # data = {
#     #     "detail": "Server error: {}".format(str(exception))
#     # }
#     data = {
#         "detail": "Server error:"
#     }
#     return HttpResponseServerError(content=json.dumps(data))