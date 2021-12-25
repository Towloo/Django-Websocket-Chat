from django.core import exceptions
from rest_framework import serializers
from django.contrib.auth import authenticate

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if user and user.is_active:
                data["user"] = user
            else:
                raise exceptions.ValidationError("Invalid Credentials")
        else:
            raise exceptions.ValidationError
        
        return data