
from rest_framework import serializers


class DataLuceneSerializer(serializers.Serializer):

    SORT_CHOICES = (
        ("asc", "ascending"),
        ("desc", "descending"),
    )
    indices = serializers.ListField(default=[], child=serializers.CharField())
    query = serializers.CharField(default="*", label="查询lucene", help_text="lucene格式的搜索语句")
    sort = serializers.DictField(child=serializers.ChoiceField(choices=SORT_CHOICES), default={"_score": "desc"})
    page = serializers.IntegerField(default=1, min_value=1, label="页码")
    page_size = serializers.IntegerField(default=10, min_value=1)


# class DeletedDataLuceneSerializer(DataLuceneSerializer):
#
#     def validate_indices(self, indices):
#         return list(map(lambda i: i+"..", indices))

class DataDSLSerializer(DataLuceneSerializer):
    query = None
    body = serializers.DictField(label="DSL查询内容")