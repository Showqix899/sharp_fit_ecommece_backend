from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import AdminInvitation


User = get_user_model()

class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    role=serializers.CharField(read_only=True)
    default_deviece=serializers.CharField(read_only=True)



class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


class AdminInviteSerializer(serializers.Serializer):

    admin_email=serializers.EmailField()


    def validate(self, data):

        email=data['admin_email']
        if not email:
            raise serializers.ValidationError("email required")
        return super().validate(data)

