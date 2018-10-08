import re
import logging
import datetime

from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import authenticate

from rest_framework import serializers
from rest_framework import exceptions

from . import models

User = get_user_model()

MAX_AGE = settings.MAX_AGE

logger = logging.getLogger(__name__)


class FieldSerializer(serializers.ModelSerializer):
    def validate_name(self, value):
        if not re.match('[a-z][a-z-0-9]*$', value):
            raise serializers.ValidationError("Name must be lowercase letters, numbers, hyphens the composition, And can only begin with a letter")
        return value

    class Meta:
        model = models.Field
        exclude = ("table", )
        # read_only_fields = ("table", "name", "type", "is_multi")


class TableSerializer(serializers.ModelSerializer):
    creator = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    creator_username = serializers.CharField(read_only=True, source="creator.username")

    fields = FieldSerializer(required=True, many=True)

    def validate_name(self, value):
        if not re.match('[a-z][a-z-0-9]*$', value):
            raise serializers.ValidationError("Name must be lowercase letters, numbers, hyphens the composition, And can only begin with a latter")
        return value

    def validate_fields(self, value):
        if not value:
            raise exceptions.ValidationError("表字段至少一个")
        return value

    class Meta:
        model = models.Table
        fields = "__all__"
        # read_only_fields = ("name", "creator", "creation_time")

    def create(self, validated_data):
        fields_data = validated_data.pop("fields")
        table = models.Table.objects.create(**validated_data)
        for field_data in fields_data:
            models.Field.objects.create(table=table, **field_data)
        return table

    def update(self, instance, validated_data):
        fields_data = validated_data.pop("fields")
        models.Field.objects.filter(table=instance).delete()
        super().update(instance, validated_data)
        for field_data in fields_data:
            models.Field.objects.create(table=instance, **field_data)
        return instance


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(label="邮箱")
    # password = serializers.CharField(required=False, min_length=6, max_length=20, label="密码", write_only=True)
    is_staff = serializers.BooleanField(default=False, label="管理员")

    def create(self, validated_data):
        password = get_random_string(10)
        user = User.objects.create_user(**validated_data)
        # user = super().create(**validated_data)
        user.set_password(password)
        user.save()
        username = validated_data["username"]
        permissions = "管理员" if validated_data["is_staff"] else "普通用户"
        try:
            send_mail("CMDB 用户创建成功",
                      "Hi, {}, 您的CMDB用户已成功创建：\n\t用户名:{}\n\t权限:{}\n\t初始密码:{}\n\t网站地址:{}".format(
                          username, username, permissions, password, settings.SITE_URL),
                      settings.SEND_EMAIL,
                      [validated_data["email"]],
                      fail_silently=False)
        except Exception as exc:
            logger.error(f"用户创建成功 邮件发送失败 {exc}")
            raise exceptions.ParseError("用户创建成功 邮件发送失败")
        return user

    # def update(self, instance, validated_data):
    #     super().update(instance, validated_data)
    #     if "password" in validated_data:
    #         instance.set_password(validated_data)
    #     return instance

    class Meta:
        model = User
        # fields = "__all__"
        exclude = ("password", )


class ChangePWSerializer(serializers.Serializer):
    current_password = serializers.CharField(min_length=6, max_length=20, label="当前密码")
    new_password = serializers.CharField(min_length=6, max_length=20, label="新密码")

    def validate_current_password(self, value):
        username = self.context["request"].user.username
        user = authenticate(username=username, password = value)
        if user is None:
            raise exceptions.ValidationError("The current password incorrect")
        return value


class RestPWVerifyCodeSerializer(serializers.Serializer):
    username = serializers.CharField()

    def validate_username(self, value):
        try:
            User.objects.get(username=value)
        except User.DoesNotExist as exc:
            raise exceptions.ValidationError("{} does not exist!".format(value))
        return value


class RestPWAdminSerializer(serializers.Serializer):
    new_password = serializers.CharField(min_length=6, max_length=20, label="新密码")


class RestPWEmailSerializer(serializers.Serializer):
    username = serializers.CharField(label="用户名")
    new_password = serializers.CharField(min_length=6, max_length=20, label="新密码")
    verify_code = serializers.CharField(min_length=6, max_length=6, label="验证码")

    def validate(self, attrs):
        valid_datetime = datetime.datetime.now() - datetime.timedelta(seconds=MAX_AGE)
        try:
            reset_model = models.RestPWVerifyCode.objects.get(user__username=attrs["username"])
        except models.RestPWVerifyCode.DoesNotExist as exc:
            raise exceptions.ValidationError("The verification code is incorrect!")
        if reset_model.code != attrs["verify_code"]:
            raise exceptions.ValidationError("The verifaction code is incorrect!")
        if datetime.datetime.now() - reset_model.add_time > datetime.timedelta(seconds=MAX_AGE):
            raise exceptions.ValidationError("The verifaction code has expired!")
        return attrs


class SendVerifyCodeSerializer(serializers.Serializer):
    username = serializers.CharField()

    def validate_username(self, value):
        try:
            user = User.objects.get(username = value)
        except User.DoesNotExist as exc:
            raise exceptions.ValidationError("user {} does not exist".format(value))
        return value


class DepartmentSerializer(serializers.ModelSerializer):
    parent__name = serializers.CharField(read_only=True, source="parent.name")

    class Meta:
        model = models.Department
        fields = "__all__"
