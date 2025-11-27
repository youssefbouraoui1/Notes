from rest_framework import serializers
from .models import Users
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
import uuid
from uuid import UUID
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.settings import api_settings




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
        

class ResetPasswordConfirmationRequest(serializers.Serializer):
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
    
class ResetPasswordRequest(serializers.Serializer):
    user_id = serializers.CharField()
    def validate(self, data):
        try:
            user_id =data["user_id"]
        except Exception:
            raise serializers.ValidationError("User Id is missing")
        
        try:
            user = Users.objects.get(id=user_id)
        except Users.DoesNotExist:
            raise serializers.ValidationError("User not found.")

        data["user"] = user
        return data



User = get_user_model()

class UUIDTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        refresh_token = attrs.get("refresh")

        try:
            token = RefreshToken(refresh_token)
        except TokenError as e:
            raise InvalidToken({"detail": "Refresh token is invalid or expired."})

        user_id_claim = api_settings.USER_ID_CLAIM
        if user_id_claim in token.payload:
            raw_uid = token.payload[user_id_claim]
            try:
                token.payload[user_id_claim] = str(UUID(raw_uid))
            except Exception:
                pass

        access = token.access_token

        data = {"access": str(access)}

        if api_settings.ROTATE_REFRESH_TOKENS:
            if api_settings.BLACKLIST_AFTER_ROTATION:
                try:
                    token.blacklist()
                except Exception:
                    pass
            new_refresh = RefreshToken()
            for claim in token.payload:
                new_refresh.payload[claim] = token.payload[claim]
            data["refresh"] = str(new_refresh)

        return data
    
    
    
    
def verify_reset_token(user,token):
    return default_token_generator.check_token(user, token)
