from rest_framework import serializers

class S(serializers.Serializer):
    name = serializers.CharField()


s = S()