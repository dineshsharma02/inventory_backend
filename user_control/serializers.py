from rest_framework import serializers 
from .models import CustomUser, Roles

class CreateUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    role = serializers.ChoiceField(Roles)


class LoginUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password =serializers.CharField()
    is_new_user = serializers.BooleanField(required=False,default=False)

