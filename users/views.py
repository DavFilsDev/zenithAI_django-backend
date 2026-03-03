from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, RegisterSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['user_id'] = self.user.id
        data['email'] = self.user.email
        data['username'] = self.user.username
        data['credits'] = self.user.credits
        data['is_premium'] = self.user.is_premium
        return data

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    
    @extend_schema(
        summary="Login - Get JWT Tokens",
        description="Authenticate with email/password to receive access and refresh tokens",
        tags=['Authentication']
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class RegisterView(generics.CreateAPIView):
    """
    Register a new user account.
    
    Creates a new user with default credits (10) and non-premium status.
    Returns the created user data upon success.
    """
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer
    
    @extend_schema(
        summary="Register new user",
        description="Create a new user account with email and password",
        request=RegisterSerializer,
        responses={
            201: UserSerializer,
            400: OpenApiExample(
                'Validation Error',
                value={
                    "email": ["user with this email already exists."],
                    "password": ["Password fields didn't match."]
                }
            ),
        },
        examples=[
            OpenApiExample(
                'Valid Registration',
                value={
                    "email": "user@example.com",
                    "username": "newuser",
                    "password": "SecurePass123!",
                    "password2": "SecurePass123!"
                },
                request_only=True,
            ),
        ],
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    def get_object(self):
        return self.request.user