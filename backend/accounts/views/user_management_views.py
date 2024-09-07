from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from ..models import User, ROLE_CHOICES
from ..serializers import UserSerializer
from ..permissions import IsSuperAdmin, IsCompanyAdmin, IsCompanyAdminOrReadOnly
from tenants.models import Tenant


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


class TenantUserListView(generics.ListCreateAPIView):
    """
    Allows tenant admins to list and create users within their own tenant.
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsCompanyAdminOrReadOnly]

    def get_queryset(self):
        # Restrict the queryset to users within the tenant admin's tenant
        return User.objects.filter(tenant=self.request.user.tenant)

    def perform_create(self, serializer):
        # Automatically associate the created user with the tenant admin's tenant
        serializer.save(tenant=self.request.user.tenant)


class TenantUserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Allows tenant admins to view, update, and delete users within their own tenant.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsCompanyAdmin]

    def get_queryset(self):
        # Restrict the queryset to users within the tenant admin's tenant
        return User.objects.filter(tenant=self.request.user.tenant)


class AssignTenantRoleView(generics.UpdateAPIView):
    """
    Allows tenant admins to assign roles to users within their tenant.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsCompanyAdmin]

    def patch(self, request, *args, **kwargs):
        user = self.get_object()
        role = request.data.get('role')

        if role not in dict(ROLE_CHOICES).keys() or role == 'super_admin':
            return Response({"error": "Invalid or unauthorized role"}, status=status.HTTP_400_BAD_REQUEST)

        if user.tenant != request.user.tenant:
            return Response({"error": "Cannot assign roles to users outside your tenant"}, status=status.HTTP_403_FORBIDDEN)

        user.role = role
        user.save()
        return Response({"message": f"Role '{role}' has been assigned to {user.email}"}, status=status.HTTP_200_OK)


class ActivateDeactivateUserView(generics.UpdateAPIView):
    """
    Allows tenant admins to activate or deactivate users within their tenant.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsCompanyAdmin]

    def patch(self, request, *args, **kwargs):
        user = self.get_object()
        if user.tenant != request.user.tenant:
            return Response({"error": "Cannot modify users outside your tenant"}, status=status.HTTP_403_FORBIDDEN)

        is_active = request.data.get('is_active')
        user.is_active = is_active
        user.save()
        status_message = "activated" if is_active else "deactivated"
        return Response({"message": f"User {user.email} has been {status_message}."}, status=status.HTTP_200_OK)
