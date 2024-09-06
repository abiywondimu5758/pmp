from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from ..serializers import CustomTokenObtainPairSerializer, UserSerializer
from ..models import User


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom view to handle user login and token generation.
    """
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        print(f"Request data: {request.data}")
        response = super().post(request, *args, **kwargs)
        print(f"Response data: {response.data}")
        return response


class LogoutView(generics.GenericAPIView):
    """
    View to handle user logout without blacklisting the refresh token.
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        return Response({"message": "Successfully logged out."}, status=status.HTTP_205_RESET_CONTENT)


class RegisterView(generics.CreateAPIView):
    """
    View to handle user registration.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
