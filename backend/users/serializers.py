from rest_framework import serializers
from django.contrib.auth import get_user_model


User = get_user_model()

class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    role=serializers.CharField(read_only=True)



class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'