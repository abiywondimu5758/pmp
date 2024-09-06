from django.urls import path
from .views import TenantListCreateView, TenantDetailView, TenantActivateDeactivateView

urlpatterns = [
    path('', TenantListCreateView.as_view(), name='tenant_list_create'),
    path('<int:pk>/', TenantDetailView.as_view(), name='tenant_detail'),
    path('activate-deactivate/<int:pk>/',
         TenantActivateDeactivateView.as_view(), name='tenant_activate_deactivate'),
]
