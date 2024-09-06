from rest_framework import generics, status, permissions
from rest_framework.response import Response
from .models import Tenant, Domain
from .serializers import TenantSerializer, DomainSerializer
from accounts.permissions import IsSuperAdmin  # Use existing permission classes


class TenantListCreateView(generics.ListCreateAPIView):
    """
    Allows super admin to list and create tenants.
    """
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer
    permission_classes = [permissions.IsAuthenticated, IsSuperAdmin]


class TenantDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Allows super admin to view, update, and delete tenants.
    """
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer
    permission_classes = [permissions.IsAuthenticated, IsSuperAdmin]


class TenantActivateDeactivateView(generics.UpdateAPIView):
    """
    Allows super admin to activate or deactivate tenants.
    """
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer
    permission_classes = [permissions.IsAuthenticated, IsSuperAdmin]

    def patch(self, request, *args, **kwargs):
        tenant = self.get_object()
        is_active = request.data.get('is_active')

        if is_active is None:
            return Response({"error": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST)

        tenant.is_active = is_active
        tenant.save()
        status_message = "activated" if is_active else "deactivated"
        return Response({"message": f"Tenant {tenant.name} has been {status_message}."}, status=status.HTTP_200_OK)
