from rest_framework import generics, status, permissions, serializers
from rest_framework.response import Response
from .models import Tenant, Domain
from .serializers import TenantSerializer, DomainSerializer
from accounts.permissions import IsSuperAdmin


class TenantListCreateView(generics.ListCreateAPIView):
    """
    Allows super admin to list and create tenants.
    """
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer
    permission_classes = [permissions.IsAuthenticated, IsSuperAdmin]

    # def create(self, request, *args, **kwargs):
    #     tenant_data = {
    #         "schema_name": request.data.get("schema_name"),
    #         "name": request.data.get("name"),
    #         "paid_until": request.data.get("paid_until"),
    #         "on_trial": request.data.get("on_trial", True),
    #         "is_active": request.data.get("is_active", True)
    #     }

    #     domain_data = {
    #         "domain": request.data.get("domain"),
    #         "is_primary": request.data.get("is_primary", True)
    #     }
    #     tenant_serializer = self.get_serializer(data=tenant_data)
    #     tenant_serializer.is_valid(raise_exception=True)
    #     tenant = tenant_serializer.save()

    #     domain_data['tenant'] = tenant.id
    #     domain_serializer = DomainSerializer(data=domain_data)
    #     domain_serializer.is_valid(raise_exception=True)
    #     domain_serializer.save(tenant=tenant)

    #     headers = self.get_success_headers(tenant_serializer.data)
    #     return Response(
    #         {"tenant": tenant_serializer.data, "domain": domain_serializer.data},
    #         status=status.HTTP_201_CREATED,
    #         headers=headers
    #     )


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


class DomainCreateView(generics.CreateAPIView):
    """
    Allows super admin to create a domain for a tenant.
    """
    queryset = Domain.objects.all()
    serializer_class = DomainSerializer
    permission_classes = [permissions.IsAuthenticated, IsSuperAdmin]

    def perform_create(self, serializer):
        # Custom logic to associate the domain with a tenant
        tenant_id = self.request.data.get('tenant')
        if not Tenant.objects.filter(id=tenant_id).exists():
            raise serializers.ValidationError({"tenant": "Invalid tenant ID."})
        tenant = Tenant.objects.get(id=tenant_id)
        serializer.save(tenant=tenant)

class DomainDetailView(generics.RetrieveUpdateDestroyAPIView):
    
    queryset = Domain.objects.all()
    serializer_class = DomainSerializer
    permission_classes = [permissions.IsAuthenticated, IsSuperAdmin]