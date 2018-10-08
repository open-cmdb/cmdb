"""cmdb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from rest_framework.documentation import include_docs_urls
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    url(r'^api/v1/search/', include("search.urls")),
    url(r'^api/v1/data/', include("data.urls")),
    url(r'^api/v1/record-data/', include("record_data.urls")),
    url(r'^api/v1/deleted-data/', include("deleted_data.urls")),
    url(r'^api/v1/token', obtain_jwt_token),
    url(r'^api/v1/mgmt/', include("mgmt.urls")),
    url(r'^api-docs', include_docs_urls(title="cmdb接口文档", permission_classes=())),
    url(r'^admin/', admin.site.urls),
    url(r'^c-test/', include("c_test.urls")),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

handler404 = "utils.exceptions.interface_not_defined"
