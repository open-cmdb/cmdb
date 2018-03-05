
from elasticsearch.exceptions import NotFoundError

from rest_framework.routers import SimpleRouter
from rest_framework import exceptions

from . import models
import data.initialize
import record_data.initialize
import deleted_data.initialize
from utils.es import indices_client

data_url_map = {}
record_data_url_map = {}
deleted_data_url_map = {}

def add_index(table_name):
    indices_client.create(index=table_name)

def delete_index(table_name):
    try:
        indices_client.delete(index=table_name)
    except NotFoundError:
        return

def add_table(table, create_index=False):
    if(create_index):
        add_index(table.name)
        add_index(table.name+".")
        add_index(table.name+"..")

    data.initialize.add_serializer(table)
    viewset = data.initialize.add_viewset(table)
    router = SimpleRouter(trailing_slash=False)
    router.register(table.name, viewset, base_name=table.name)
    urls = router.urls
    data.urls.urlpatterns.extend(urls)
    data_url_map[table.name] = urls

    viewset = record_data.initialize.add_viewset(table)
    router = SimpleRouter(trailing_slash=False)
    router.register(table.name, viewset, base_name=table.name)
    urls = router.urls
    record_data.urls.urlpatterns.extend(urls)
    record_data_url_map[table.name] = urls

    viewset = deleted_data.initialize.add_viewset(table)
    router = SimpleRouter(trailing_slash=False)
    router.register(table.name, viewset, base_name=table.name)
    urls = router.urls
    deleted_data.urls.urlpatterns.extend(urls)
    deleted_data_url_map[table.name] = urls


def delete_table(table):
    for url in data_url_map[table.name]:
        index = data.urls.urlpatterns.index(url)
        del data.urls.urlpatterns[index]

    for url in record_data_url_map[table.name]:
        index = record_data.urls.urlpatterns.index(url)
        del record_data.urls.urlpatterns[index]

    for url in deleted_data_url_map[table.name]:
        index = deleted_data.urls.urlpatterns.index(url)
        del deleted_data.urls.urlpatterns[index]

    delete_index(table.name)
    delete_index(table.name+".")
    delete_index(table.name+"..")

tables = models.Table.objects.all()
for table in tables:
    add_table(table)