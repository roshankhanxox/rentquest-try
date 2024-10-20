from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet,
    CustomTokenObtainPairView,
    CustomTokenRefreshView,
    LogoutView,
)

router = (
    DefaultRouter()
)  # router automaticall generates your basic urls so like /api/ or /api/users/
router.register(r"users", UserViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("login/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("properties/", include("properties.urls")),
    path("login/refresh/", CustomTokenRefreshView.as_view(), name="token_refresh"),
    path("logout/", LogoutView.as_view(), name="logout"),  # Add the logout URL
    path("reviews/", include("reviews.urls")),
]
