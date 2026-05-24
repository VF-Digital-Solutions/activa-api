from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema

from apps.identity.serializers import (
    LoginSerializer,
    RegisterSerializer,
    UserSerializer,
)


@extend_schema(tags=["Authenticacion"])
class RegisterView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        summary="Register a new user",
        description="Creates a new user account and returns JWT tokens",
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "user": UserSerializer(user).data,
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            },
            status=status.HTTP_201_CREATED,
        )


@extend_schema(tags=["Authenticacion"])
class LoginView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        summary="Login",
        description="Authenticates auser and returns JWT tokens.",
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "user": UserSerializer(user).data,
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            }
        )


@extend_schema(tags=["Authenticacion"])
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(summary="Logout", description="Invalidates the refresh token")
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=["Authenticacion"])
class MeView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Get current user",
        description="Returns the authenticated user's profile.",
    )
    def get(self, request):
        return Response(UserSerializer(request.user).data)

    def patch(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
