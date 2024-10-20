from rest_framework import serializers
from .models import Property, PropertyImage


class PropertyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = ["id", "image", "uploaded_at"]


class PropertySerializer(serializers.ModelSerializer):
    landlord = serializers.ReadOnlyField(
        source="landlord.username"
    )  # Read-only field for landlord
    property_images = PropertyImageSerializer(many=True, read_only=True)

    class Meta:
        model = Property
        fields = [
            "id",
            "name",
            "location",
            "price",
            "size",
            "landlord",
            "property_images",
            "created_at",
            "latitude",
            "longitude",
        ]
