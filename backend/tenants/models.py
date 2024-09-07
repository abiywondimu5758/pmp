from django_tenants.models import TenantMixin, DomainMixin
from django.db import models


class Tenant(TenantMixin):
    """
    Model representing a tenant (company). Each tenant will have its own schema.
    """
    name = models.CharField(max_length=100)
    paid_until = models.DateField(null=True, blank=True)
    on_trial = models.BooleanField(default=True)
    created_on = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    auto_create_schema = True  # Automatically create schema when the tenant is saved

    def __str__(self):
        return self.name


class Domain(DomainMixin):
    """
    Model representing the domain associated with a tenant.
    """
    domain = models.CharField(max_length=255, unique=True)
    tenant = models.ForeignKey(
        Tenant, related_name='domains', on_delete=models.CASCADE)
    is_primary = models.BooleanField(default=True)

    def __str__(self):
        return self.domain
