import requests
from rest_framework import viewsets, permissions, status, generics
from django.db.models import Q, Avg
from django.conf import settings
from django.http import JsonResponse
from geopy.geocoders import GoogleV3
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView
from rest_framework.views import APIView
from .models import Property, PropertyImage
from .serializers import PropertySerializer, PropertyImageSerializer
from math import radians, sin, cos, sqrt, atan2
from reviews.models import Review
from reviews.serializers import ReviewSerializer


class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if self.request.user.role != "landlord":
            raise PermissionDenied("Only landlords can create property")
        property_instance = serializer.save(landlord=self.request.user)
        return Response(
            {"message": "Property created successfully", "id": property_instance.id},
            status=status.HTTP_201_CREATED,
        )

    def get_queryset(self):
        return Property.objects.filter(landlord=self.request.user)


class PropertyImageViewSet(viewsets.ModelViewSet):
    queryset = PropertyImage.objects.all()
    serializer_class = PropertyImageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        property_id = self.request.data.get("property_id")
        property_instance = Property.objects.get(id=property_id)
        if property_instance.landlord != self.request.user:
            raise PermissionDenied(
                "You can only upload images for your own properties."
            )
        serializer.save(property=property_instance)


class PropertyGeoSearchView(generics.ListAPIView):
    serializer_class = PropertySerializer

    def get_queryset(self):
        query = self.request.query_params.get("query", None)
        min_price = self.request.query_params.get("min_price", None)
        max_price = self.request.query_params.get("max_price", None)
        min_size = self.request.query_params.get("min_size", None)
        max_size = self.request.query_params.get("max_size", None)

        properties = Property.objects.all()

        if query:
            # Geocode the location to get latitude and longitude
            geolocator = GoogleV3(api_key=settings.GOOGLE_MAPS_API_KEY)
            location = geolocator.geocode(query)

            if location:
                lat = location.latitude
                lng = location.longitude

                # Filter properties based on the latitude and longitude
                properties = properties.filter(
                    Q(latitude__isnull=False, longitude__isnull=False)
                )

                # Apply distance filtering
                nearby_properties = []
                for property in properties:
                    distance = self.calculate_distance(
                        lat, lng, property.latitude, property.longitude
                    )
                    if distance <= 5:  # Assuming 5 km radius
                        nearby_properties.append(property)

                properties = nearby_properties

        # Apply additional filters if specified
        if min_price:
            properties = [prop for prop in properties if prop.price >= float(min_price)]
        if max_price:
            properties = [prop for prop in properties if prop.price <= float(max_price)]
        if min_size:
            properties = [prop for prop in properties if prop.size >= int(min_size)]
        if max_size:
            properties = [prop for prop in properties if prop.size <= int(max_size)]

        return properties

    def calculate_distance(self, lat1, lon1, lat2, lon2):
        # Convert Decimal to float
        lat1 = float(lat1)
        lon1 = float(lon1)
        lat2 = float(lat2)
        lon2 = float(lon2)

        # Haversine formula to calculate the distance
        dlat = radians(lat2 - lat1)
        dlon = radians(lon2 - lon1)
        a = (
            sin(dlat / 2) ** 2
            + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
        )
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distance = 6371 * c  # Radius of Earth in kilometers
        return distance


class PropertyDetailView(APIView):
    # permisssion_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            property_instance = Property.objects.get(id=pk)
        except Property.DoesNotExist:
            return Response(
                {"error": "Property not found"}, status=status.HTTP_404_NOT_FOUND
            )

        # serialize property details
        property_data = PropertySerializer(property_instance).data

        # fetcdhing the images from propertyimage model
        images = PropertyImage.objects.filter(property=property_instance)
        images_data = PropertyImageSerializer(images, many=True).data

        # fetching reviews and calculating average rating
        reviews = Review.objects.filter(property=property_instance)
        reviews_data = ReviewSerializer(reviews, many=True).data
        averge_rating = reviews.aggregate(Avg("rating"))["rating__avg"] or 0

        # combining the data to return
        response_data = {
            "property": property_data,
            "images": images_data,
            "reviews": reviews_data,
            "averge_rating": round(averge_rating, 1),
            "latitude": property_data["latitude"],  # Include latitude
            "longitude": property_data["longitude"],
        }

        return Response(response_data, status=status.HTTP_200_OK)


def nearby_places(request):
    lat = request.GET.get("lat")
    lng = request.GET.get("lng")
    radius = request.GET.get("radius", "400")  # Default radius (e.g., 400 meters)

    # Define place types to search for, excluding police for the radius restriction
    place_types = [
        "shopping_mall",
        "hospital",
        "pharmacy",
    ]  # Google API types
    restaurant_keyword = "restaurant"

    # Store results for all types
    all_results = []

    # Google Places API base URL
    google_api_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"

    # Search for the closest police station without radius restriction
    police_station_params = {
        "location": f"{lat},{lng}",
        "radius": "5000",  # Use a larger radius for police stations
        "type": "police",  # Place type filter for police stations
        "key": settings.GOOGLE_MAPS_API_KEY,
    }
    police_response = requests.get(google_api_url, params=police_station_params)
    police_data = police_response.json()

    # Collect the closest police station if available
    if "results" in police_data and police_data["results"]:
        all_results.append(police_data["results"][0])  # Add the closest police station

    # Search for other place types (limiting to 2 closest results)
    for place_type in place_types:
        params = {
            "location": f"{lat},{lng}",
            "radius": radius,
            "type": place_type,  # Place type filter
            "key": settings.GOOGLE_MAPS_API_KEY,
        }
        response = requests.get(google_api_url, params=params)
        data = response.json()

        # Collect the 2 closest results for this place type
        if "results" in data:
            all_results.extend(data["results"][:2])

    # Search for restaurants (limiting to 2 closest results)
    params = {
        "location": f"{lat},{lng}",
        "radius": radius,
        "keyword": restaurant_keyword,  # Keyword filter for restaurants
        "key": settings.GOOGLE_MAPS_API_KEY,
    }
    response = requests.get(google_api_url, params=params)
    data = response.json()

    # Collect the 2 closest restaurants
    if "results" in data:
        all_results.extend(data["results"][:2])

    # Return the combined results (including the closest police station)
    return JsonResponse({"results": all_results})
