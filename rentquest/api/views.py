from rest_framework import viewsets, permissions, status
from .models import User
from .serializers import UserSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.response import Response
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]  # Allow any user to register

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = (
                serializer.save()
            )  # This saves the user and returns the user instance

            # Generate verification token and link
            token = user.verification_token
            verification_link = request.build_absolute_uri(
                reverse("user-verify-email", args=[token])
            )

            # Sending verification email
            send_mail(
                "Verify Your Email",
                f"Click the link to verify your email: {verification_link}",
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )

            return Response(
                {
                    "success": True,
                    "message": "User created successfully! A verification email has been sent.",
                },
                status=status.HTTP_201_CREATED,
            )
        else:
            # Return error messages from the serializer
            return Response(
                {"success": False, "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(detail=False, methods=["get"], url_path="verify-email/(?P<token>[^/.]+)")
    def verify_email(self, request, token):
        try:
            user = User.objects.get(verification_token=token)
            user.is_verified = True
            user.save()
            return Response(
                {"message": "Email verified successfully!"}, status=status.HTTP_200_OK
            )
        except User.DoesNotExist:
            return Response(
                {"error": "Invalid token!"}, status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class CustomTokenObtainPairView(TokenObtainPairView):
    # You can override the serializer here if needed
    pass


class CustomTokenRefreshView(TokenRefreshView):
    pass


class LogoutView(APIView):
    permission_classes = [
        IsAuthenticated
    ]  # Ensure that only authenticated users can log out

    def post(self, request):
        # You can implement token blacklisting here if required
        return Response(
            {"message": "Successfully logged out."}, status=status.HTTP_200_OK
        )
