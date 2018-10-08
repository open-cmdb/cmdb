from importlib import import_module

from elasticsearch.exceptions import NotFoundError

from django.conf import settings
from django.urls.resolvers import get_resolver

from rest_framework.routers import SimpleRouter



import data.initialize
import record_data.initialize
import deleted_data.initialize
from utils.es import indices_client, Mapping
from . import models


data_url_map = {}
record_data_url_map = {}
deleted_data_url_map = {}


#添加es索引
def add_index(table_name, mapping):
    body = {
        "settings": {
            "index": {
                "number_of_shards": 3,
                "number_of_replicas": 1
            }
        },
        "mappings": {
            "data": {
                "properties": mapping
            }
        }

    }
    indices_client.create(index=table_name, body=body)


# 删除es索引
def delete_index(table_name):
    try:
        indices_client.delete(index=table_name)
    except NotFoundError:
        return


def add_table(table, create_index=False):
    if create_index:
        mapp = Mapping()
        data_mapping = mapp.generate_data_mapping(table)
        record_mapping = mapp.generate_record_data_mapping(table)
        delete_mapping = mapp.generate_deleted_data_mapping(table)
        add_index(table.name, data_mapping)
        add_index(table.name + ".", record_mapping)
        add_index(table.name + "..", delete_mapping)

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

    # 添加权限
    permission, is_new = models.Permission.objects.get_or_create(name=f"{table.name}.read")
    permission.alias = f"{table.name}读权限"
    permission.save()
    permission, is_new = models.Permission.objects.get_or_create(name=f"{table.name}.write")
    permission.alias = f"{table.name}写权限"
    permission.save()


# 删除表和api
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

    # 更新url
    # url_conf.url_conf_manager.update_urlpatterns(getattr(import_module(settings.ROOT_URLCONF), "urlpatterns"))
    get_resolver.cache_clear()

    # 删除ES index
    delete_index(table.name)
    delete_index(table.name + ".")
    delete_index(table.name + "..")

    # 删除permission
    permission = models.Permission.objects.get(name=f"{table.name}.read")
    permission.delete()
    permission = models.Permission.objects.get(name=f"{table.name}.write")
    permission.delete()



# 启动时添加read_all 和 write_all权限
permission, is_new = models.Permission.objects.get_or_create(name="read_all")
permission.alias = "所有可读"
permission.save()

permission, is_new = models.Permission.objects.get_or_create(name="write_all")
permission.alias = "所有可写"
permission.save()

# 启动时建立所有table api 和 对应的权限
tables = models.Table.objects.all()
for table in tables:
    add_table(table)
