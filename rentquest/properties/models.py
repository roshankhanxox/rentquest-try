from django.db import models
from api.models import User
from cloudinary.models import CloudinaryField
from geopy.geocoders import GoogleV3
from django.conf import settings

# Create your models here.


class Property(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    size = models.IntegerField()  # size to be entered in square feet
    landlord = models.ForeignKey(User, on_delete=models.CASCADE)
    images = models.ImageField(upload_to="properties/")
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True
    )
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.latitude or not self.longitude:
            self.latitude, self.longitude = self.get_lat_lng(self.location)
        super(Property, self).save(*args, **kwargs)

    def get_lat_lng(self, address):
        geolocator = GoogleV3(api_key=settings.GOOGLE_MAPS_API_KEY)
        location = geolocator.geocode(address)
        if location:
            return location.latitude, location.longitude
        return None, None

    def __str__(self):
        return self.name


class PropertyImage(models.Model):
    property = models.ForeignKey(
        Property, related_name="property_images", on_delete=models.CASCADE
    )
    image = CloudinaryField("image")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.property.name}"
