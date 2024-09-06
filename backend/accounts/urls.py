from django.urls import path
from .views import (
    CustomTokenObtainPairView, LogoutView, RegisterView,
    UserListView, AssignRoleView, TenantUserListView,
    TenantUserDetailView, AssignTenantRoleView, ActivateDeactivateUserView
)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    # Authentication endpoints
    path('register/', RegisterView.as_view(), name='register'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # User management endpoints
    # Super admin access only
    path('users/', UserListView.as_view(), name='user_list'),
    path('assign-role/<int:pk>/', AssignRoleView.as_view(),
         name='assign_role'),  # Super admin access only

    # Tenant user management endpoints
    path('tenant/users/', TenantUserListView.as_view(), name='tenant_user_list'),
    path('tenant/users/<int:pk>/', TenantUserDetailView.as_view(),
         name='tenant_user_detail'),
    path('tenant/assign-role/<int:pk>/',
         AssignTenantRoleView.as_view(), name='assign_tenant_role'),
    path('tenant/activate-deactivate/<int:pk>/',
         ActivateDeactivateUserView.as_view(), name='activate_deactivate_user'),
]
