from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import User, ROLE_CHOICES, Company
from .serializers import UserSerializer, CustomTokenObtainPairSerializer
from .permissions import IsSuperAdmin, IsCompanyAdmin, IsCompanyAdminOrReadOnly


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom view to handle user login and token generation.
    """
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        return response


class LogoutView(generics.GenericAPIView):
    """
    View to handle user logout by blacklisting the refresh token.
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"message": "Successfully logged out."}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserListView(generics.ListAPIView):
    """
    List all users; access restricted to super admins.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsSuperAdmin]


class AssignRoleView(generics.UpdateAPIView):
    """
    Allows super admins to assign roles to users.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsSuperAdmin]

    def patch(self, request, *args, **kwargs):
        user = self.get_object()
        role = request.data.get('role')

        if role not in dict(ROLE_CHOICES).keys():
            return Response({"error": "Invalid role"}, status=status.HTTP_400_BAD_REQUEST)

        user.role = role
        user.save()
        return Response({"message": f"Role '{role}' has been assigned to {user.email}"}, status=status.HTTP_200_OK)


class SomeAdminView(generics.ListCreateAPIView):
    """
    Allows only super admins and company admins to access.
    """
    queryset = User.objects.filter(
        role='team_member')  # Example usage; filter users based on some role
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsCompanyAdmin]


class CompanyUserListView(generics.ListCreateAPIView):
    """
    Allows company admins to list and create users within their own company.
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsCompanyAdminOrReadOnly]

    def get_queryset(self):
        # Restrict the queryset to users within the company admin's company
        return User.objects.filter(company=self.request.user.company)

    def perform_create(self, serializer):
        # Automatically associate the created user with the company admin's company
        serializer.save(company=self.request.user.company)


class CompanyUserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Allows company admins to view, update, and delete users within their own company.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsCompanyAdmin]

    def get_queryset(self):
        # Restrict the queryset to users within the company admin's company
        return User.objects.filter(company=self.request.user.company)


class AssignCompanyRoleView(generics.UpdateAPIView):
    """
    Allows company admins to assign roles to users within their company.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsCompanyAdmin]

    def patch(self, request, *args, **kwargs):
        user = self.get_object()
        role = request.data.get('role')

        if role not in dict(ROLE_CHOICES).keys() or role == 'super_admin':
            return Response({"error": "Invalid or unauthorized role"}, status=status.HTTP_400_BAD_REQUEST)

        if user.company != request.user.company:
            return Response({"error": "Cannot assign roles to users outside your company"}, status=status.HTTP_403_FORBIDDEN)

        user.role = role
        user.save()
        return Response({"message": f"Role '{role}' has been assigned to {user.email}"}, status=status.HTTP_200_OK)


class ActivateDeactivateUserView(generics.UpdateAPIView):
    """
    Allows company admins to activate or deactivate users within their company.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsCompanyAdmin]

    def patch(self, request, *args, **kwargs):
        user = self.get_object()
        if user.company != request.user.company:
            return Response({"error": "Cannot modify users outside your company"}, status=status.HTTP_403_FORBIDDEN)

        is_active = request.data.get('is_active')
        user.is_active = is_active
        user.save()
        status_message = "activated" if is_active else "deactivated"
        return Response({"message": f"User {user.email} has been {status_message}."}, status=status.HTTP_200_OK)
