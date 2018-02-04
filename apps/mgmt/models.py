import re

from django.db import models
from django.contrib.auth import get_user_model

from rest_framework import exceptions
from rest_framework import serializers

User = get_user_model()

# Create your models here.

class Table(models.Model):
    """
    cmdb表
    """
    name = models.CharField(max_length=20, unique=True, verbose_name="表名")
    alias = models.CharField(max_length=20, unique=True, null=True, verbose_name="别名")
    creator = models.ForeignKey(User, verbose_name="创建者")
    creation_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

class Field(models.Model):
    """
    cmdb字段
    """
    FIELD_TYPE_CHOICES = ((0, "string"),
                          (1, "integer"),
                          (2, "floating"),
                          (3, "datetime"))
    FIELD_TYPE_MAP = {
        0: serializers.CharField,
        1: serializers.IntegerField,
        2: serializers.FloatField,
        3: serializers.DateTimeField,
    }

    table = models.ForeignKey(Table, related_name="fields", verbose_name="字段", on_delete=models.CASCADE)

    name = models.CharField(max_length=20, verbose_name="字段名")
    alias = models.CharField(max_length=20, unique=True, null=True, verbose_name="别名")
    readme = models.TextField(default="", verbose_name="自述")
    type = models.SmallIntegerField(choices=FIELD_TYPE_CHOICES, verbose_name="字段类型")
    is_multi = models.BooleanField(verbose_name="是否为多值字段")
    requried = models.BooleanField(verbose_name="是否必填")
