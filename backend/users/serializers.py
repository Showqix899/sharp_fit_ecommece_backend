from rest_framework import serializers

class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    role=serializers.CharField(read_only=True)
