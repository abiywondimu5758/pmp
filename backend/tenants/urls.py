from django.urls import path
from .views import TenantListCreateView, TenantDetailView, TenantActivateDeactivateView, DomainCreateView, DomainDetailView

urlpatterns = [
    path('', TenantListCreateView.as_view(), name='tenant_list_create'),
    path('<int:pk>/', TenantDetailView.as_view(), name='tenant_detail'),
    path('activate-deactivate/<int:pk>/',
         TenantActivateDeactivateView.as_view(), name='tenant_activate_deactivate'),
    path('domains/', DomainCreateView.as_view(), name='domain_create'),
    # Handles retrieving, updating, and deleting a domain
    path('domains/<int:pk>/', DomainDetailView.as_view(), name='domain_detail'),
]
