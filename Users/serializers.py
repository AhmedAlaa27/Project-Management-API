from rest_framework import serializers
from django.contrib.auth import get_user_model


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ("username", "email", "password", "avatar")

    def create(self, validated_data):
        user = get_user_model().objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            avatar=validated_data.get("avatar"),
        )
        return user
