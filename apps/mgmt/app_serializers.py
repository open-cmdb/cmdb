import re

from rest_framework import serializers
from rest_framework import exceptions

from . import models


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

    fields = FieldSerializer(many=True)

    def validate_name(self, value):
        if not re.match('[a-z][a-z-0-9]*$', value):
            raise serializers.ValidationError("Name must be lowercase letters, numbers, hyphens the composition, And can only begin with a latter")
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