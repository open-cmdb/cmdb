from rest_framework import serializers
from rest_framework import schemas
from rest_framework import metadata


class S(serializers.Serializer):
    name = serializers.CharField()


s = S()