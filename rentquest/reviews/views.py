from rest_framework import viewsets, permissions
from .models import Review
from .serializers import ReviewSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]  # Anyone can view, but only authenticated users can post

    def get_queryset(self):
        property_id = self.request.query_params.get("property_id", None)
        if property_id:
            return Review.objects.filter(property_id=property_id)
        return super().get_queryset()

    def perform_create(self, serializer):
        serializer.save()
