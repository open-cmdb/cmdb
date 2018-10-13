
import json
import logging
import datetime

from django.conf import settings

from elasticsearch.exceptions import NotFoundError

from django.contrib.auth import get_user_model
from django.conf import settings

from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import permissions
from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import detail_route, list_route
from rest_framework import filters


from utils.es import indices_client
from utils.verify_code import EmailVerifyCode
from utils.c_permissions import IsAdminCreate, IsAdminOrSelfChange, IsAdminOrReadOnly
from utils.c_pagination import CPageNumberPagination
from utils import c_permissions

from . import app_serializers
from . import models
from utils.es import es
from . import initialize

User = get_user_model()
email_verify_code = EmailVerifyCode()
logger = logging.getLogger("default")

#验证码过期时间（秒）
MAX_AGE = settings.MAX_AGE


# Create your views here.
class TableViewset(mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.UpdateModelMixin,
                   viewsets.GenericViewSet,):
    serializer_class = app_serializers.TableSerializer
    queryset = models.Table.objects.all()
    permission_classes = (IsAdminOrReadOnly, )
    pagination_class = CPageNumberPagination

    def has_data_raise(self, table_name):
        res = es.search(index=[table_name, table_name+".", table_name+".."], doc_type="data")
        if res["hits"]["total"]:
            raise exceptions.ParseError("Table has started to use, if need to modify, please delete and re-create")

    def list(self, request, *args, **kwargs):
        has_read_perm = request.query_params.get("has_read_perm")
        if not has_read_perm:
            return super().list(request, *args, **kwargs)
        queryset = self.filter_queryset(self.get_queryset())
        has_perm_tables = []
        perms = self.request.user.get_all_permission_names()
        for item in queryset:
            if item.name + ".read" in perms:
                has_perm_tables.append(item)
        data = {
            "count": len(has_perm_tables),
            "results": self.get_serializer(has_perm_tables, many=True).data
        }
        return Response(data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        table = serializer.save()
        initialize.add_table(table, create_index=True)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        self.has_data_raise(instance.name)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        initialize.delete_table(instance)
        table = serializer.save()
        initialize.add_table(table, create_index=True)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        confirm = request.query_params.get("confirm")
        if not confirm:
            raise exceptions.ParseError("删除表为高危操作 请输入您的用户名确认")
        if confirm != request.user.username:
            return Response({"confirm": "用户名错误"}, status=status.HTTP_400_BAD_REQUEST)
        instance = self.get_object()
        table_name = instance.name
        initialize.delete_table(instance)
        self.perform_destroy(instance)
        logger.debug(f"{request.user.username}删除表{table_name}")
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserViewset(viewsets.ModelViewSet):
    serializer_class = app_serializers.UserSerializer
    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsAdminCreate, IsAdminOrSelfChange)
    pagination_class = CPageNumberPagination
    filter_backends = (filters.SearchFilter, )
    search_fields = ("username", "email")

    def get_serializer_class(self):
        # if(settings.AUTH_LDAP_SERVER_URI and self.action!="get_my_info"):
        #     raise exceptions.ParseError("Please operate on LDAP server")
        if self.action == "change_password":
            return app_serializers.ChangePWSerializer
        elif self.action == "reset_password_admin":
            return app_serializers.RestPWAdminSerializer
        elif self.action == "reset_password_email":
            return app_serializers.RestPWEmailSerializer
        elif self.action == "send_verify_code":
            return app_serializers.SendVerifyCodeSerializer
        elif self.action == "get_my_info":
            return super().get_serializer_class()
        return super().get_serializer_class()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.is_superuser:
            raise exceptions.ParseError("Super user can not delete")
        if instance.table_set.exists():
            raise exceptions.ParseError("该用户创建过表 无法删除 请将其设置为禁用")
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @list_route(methods=['post'], permission_classes=[permissions.IsAuthenticated], url_path='change-password')
    def change_password(self, request, pk=None):
        serializer = self.get_serializer(data=request.data, context={"request", request})
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data["new_password"])
        request.user.save()
        return Response({"detail": "Successfully modified!"})

    @list_route(methods=['post'], permission_classes=[permissions.IsAdminUser], url_path='reset-password-admin')
    def reset_password_admin(self, request, pk=None):
        serializer = self.get_serializer(data=request.data, context={"request", request})
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data["new_password"])
        request.user.save()
        return Response({"detail": "Reset successfully"})

    @list_route(methods=['post'], permission_classes=[], url_path="send-verify-code")
    def send_verify_code(self, request, pk=None):
        serializer = self.get_serializer(data=request.data, context={"request", request})
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data["username"]
        try:
            verify_code_inst = models.RestPWVerifyCode.objects.get(user__username=username)
        except models.RestPWVerifyCode.DoesNotExist:
            pass
        else:
            if datetime.datetime.now() - verify_code_inst.add_time < datetime.timedelta(seconds=60):
                raise exceptions.ParseError("Less than 60 seconds from last sent")
            verify_code_inst.delete()
        user = User.objects.get(username=username)
        if not user.email:
            raise exceptions.ParseError(f"{username} user does not have a email, please contact the administrator to"
                                        f" reset password")
        try:
            code = email_verify_code.send_verifycode(user.email)
        except Exception as exc:
            raise exceptions.ParseError("send failed, please try again later！")
        reset_pw_verify_code = models.RestPWVerifyCode(user=user, code=code)
        reset_pw_verify_code.save()
        return Response({"detail": "send successfully", "email": user.email})

    @list_route(methods=['post'], permission_classes=[], url_path="reset-password-email")
    def reset_password_email(self, request, pk=None):
        serializer = self.get_serializer(data=request.data, context={"request", request})
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data["username"]
        user = User.objects.get(username=username)
        user.set_password(serializer.validated_data["new_password"])
        user.save()
        return Response({"detail": "Reset successfully"})

    @list_route(methods=['get'], permission_classes=[permissions.IsAuthenticated], url_path="get-my-info")
    def get_my_info(self, request, pk=None):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @detail_route(methods=['post'], permission_classes=[permissions.IsAdminUser], url_path='reset-password-by-admin')
    def reset_password_by_admin(self, request, pk=None):
        instance = self.get_object()
        new_password = request.data.get("password")
        if not new_password:
            raise exceptions.ParseError("新密码不能为空")
        instance.set_password(new_password)
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @list_route(methods=['post'], permission_classes=[permissions.IsAdminUser], url_path='update-password')
    def update_password(self, request, pk=None):
        instance = request.user
        new_password = request.data.get("password")
        if not new_password:
            raise exceptions.ParseError("新密码不能为空")
        instance.set_password(new_password)
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @list_route(methods=["get"], permission_classes=[permissions.IsAuthenticated], url_path="my-permission-names")
    def my_permission_names(self, request):
        perms = self.request.user.get_all_permission_names()
        data = {
            "count": len(perms),
            "results": perms
        }
        return Response(data)


class LdapUserViewset(viewsets.GenericViewSet):
    serializer_class = app_serializers.UserSerializer
    queryset = User.objects.all()

    @list_route(methods=['get'], permission_classes=[permissions.IsAuthenticated], url_path="get-my-info")
    def get_my_info(self, request, pk=None):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class DepartmentViewSet(viewsets.GenericViewSet):
    serializer_class = app_serializers.DepartmentSerializer
    queryset = models.Department.objects.all()
    permission_classes = (c_permissions.IsAdminOrReadOnly, )
