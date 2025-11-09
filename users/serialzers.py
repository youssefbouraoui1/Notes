from rest_framework import serializers
from .models import Users

class CreateUser(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ["username","email","password","first_name","last_name"]
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = Users(**validated_data)
        user.set_password(password)
        user.save()
        return user

class UserListSeriaizer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ["id","email", "first_name","last_name","username","role"]