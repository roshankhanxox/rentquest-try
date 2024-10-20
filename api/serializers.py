from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True
    )  # Ensures the password is write-only

    class Meta:
        model = User
        fields = ["id", "username", "email", "role", "password"]

    def create(self, validated_data):
        # Remove role if you want to handle it separately or add additional logic
        role = validated_data.pop("role", None)

        user = User(**validated_data)  # Create a User instance without saving
        user.set_password(validated_data["password"])  # Hash the password
        user.role = role  # Set the role if applicable
        user.save()  # Save the user

        return user
