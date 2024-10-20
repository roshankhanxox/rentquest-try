from rest_framework import serializers
from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    # Exclude the user field when returning data, but include it for internal processing
    class Meta:
        model = Review
        fields = ["id", "property", "comment", "rating", "created_at"]
        read_only_fields = ["id", "created_at"]

    def create(self, validated_data):
        request = self.context["request"]
        validated_data["user"] = (
            request.user
        )  # Set the user to the one making the request
        return super().create(validated_data)
