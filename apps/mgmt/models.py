import time
from functools import lru_cache

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

from rest_framework import serializers

from utils import fields as c_fields


class Permission(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="权限名")
    alias = models.CharField(max_length=100, verbose_name="权限别名")

    def __str__(self):
        return self.alias

    class Meta:
        verbose_name = "权限"
        verbose_name_plural = "权限"


class Department(models.Model):
    name = models.CharField(max_length=20, verbose_name="部门名")
    level = models.SmallIntegerField(verbose_name="级别")
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, verbose_name="上级部门")
    permissions = models.ManyToManyField(Permission, blank=True, related_name="departments", verbose_name="所有权限")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "部门"
        verbose_name_plural = verbose_name
        unique_together = ("name", "parent")


class User(AbstractUser):

    name = models.CharField(max_length=10, verbose_name="姓名")
    position = models.CharField(blank=True, max_length=20, verbose_name="职位")
    departments = models.ManyToManyField(Department, related_name="users", blank=True, verbose_name="部门集")
    permissions = models.ManyToManyField(Permission, related_name="users", blank=True, verbose_name="权限集")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    def get_all_permissions_no_cache(self):
        perms = [p.name for p in self.permissions.all()]
        perms = set(perms)
        for d in self.departments.all():
            for p in d.permissions.all():
                perms.add(p.name)
        return list(perms)

    @lru_cache(maxsize=64)
    def _get_all_permissions_by_cache(self, refresh_mark_number):
        print(f"{self.name} get_all_permissions_by_cache")
        return self.get_all_permissions_no_cache()

    # def get_all_permissions(self):
    #     if settings.PERMISSION_CACHE_TIME == 0:
    #         return self.get_all_permissions_no_cache()
    #     return self._get_all_permissions_by_cache(time.time()//settings.PERMISSION_CACHE_TIME)

    def get_all_permission_names(self):
        if settings.PERMISSION_CACHE_TIME == 0:
            return self.get_all_permissions_no_cache()
        return self._get_all_permissions_by_cache(time.time()//settings.PERMISSION_CACHE_TIME)


class Table(models.Model):
    """
    cmdb表
    """
    name = models.CharField(primary_key=True, max_length=20, verbose_name="表名")
    alias = models.CharField(max_length=20, unique=True, null=True, verbose_name="别名")
    readme = models.TextField(blank=True, default="", verbose_name="自述")
    creator = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="创建者")
    creation_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "表"
        verbose_name_plural = verbose_name


class Field(models.Model):
    """
    cmdb字段
    """
    FIELD_TYPE_CHOICES = ((0, "string"),
                          (1, "integer"),
                          (2, "floating"),
                          (3, "datetime"),
                          (4, "date"),
                          (5, "boolean"),
                          (6, "Ip"))
    FIELD_TYPE_MAP = {
        0: serializers.CharField,
        1: serializers.IntegerField,
        2: serializers.FloatField,
        3: serializers.DateTimeField,
        4: serializers.DateField,
        5: c_fields.BooleanField,
        6: serializers.IPAddressField,
    }

    table = models.ForeignKey(Table, related_name="fields", verbose_name="字段", on_delete=models.CASCADE)

    name = models.CharField(max_length=20, verbose_name="字段名")
    alias = models.CharField(default="", max_length=20, null=True, blank=True, verbose_name="别名")
    readme = models.TextField(null=True, blank=True, default="", verbose_name="自述")
    type = models.SmallIntegerField(choices=FIELD_TYPE_CHOICES, verbose_name="字段类型")
    is_multi = models.BooleanField(default=False, verbose_name="是否为多值字段")
    required = models.BooleanField(default=False, verbose_name="是否必填")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "字段"
        verbose_name_plural = verbose_name


class RestPWVerifyCode(models.Model):
    user = models.OneToOneField(User, unique=True)
    code = models.CharField(max_length=10)
    add_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = "验证码"
        verbose_name_plural = verbose_name
