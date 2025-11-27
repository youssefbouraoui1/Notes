from rest_framework import serializers
from .models import Users
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
import uuid



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
        

class ResetPasswordRequest(serializers.Serializer):
    user_id = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField()
    def validate(self, data):
        try:
            user_id = urlsafe_base64_decode(data["user_id"]).decode()
            user_uuid = uuid.UUID(user_id)
        except Exception:
            raise serializers.ValidationError("Invalid user ID format")
        
        try:
            user = Users.objects.get(id=user_uuid)
        except Users.DoesNotExist:
            raise serializers.ValidationError("User not found.")
        token = data.get("token")
        if not verify_reset_token(user, token):
            raise serializers.ValidationError("Invalid or expired token.")

        data["user"] = user
        return data
    
def verify_reset_token(user,token):
    return default_token_generator.check_token(user, token)