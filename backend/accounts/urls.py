from django.urls import path
from .views import (
    RegisterView, UserListView, AssignRoleView, SomeAdminView,
    CompanyUserListView, CompanyUserDetailView, AssignCompanyRoleView, ActivateDeactivateUserView,
    CustomTokenObtainPairView, LogoutView
)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('token/', CustomTokenObtainPairView.as_view(),
         name='token_obtain_pair'),  # Custom login
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),  # Logout endpoint
    path('users/', UserListView.as_view(), name='user_list'),
    path('assign-role/<int:pk>/', AssignRoleView.as_view(), name='assign_role'),
    path('admin-view/', SomeAdminView.as_view(), name='admin_view'),

    # Company admin URLs
    path('company/users/', CompanyUserListView.as_view(), name='company_user_list'),
    path('company/users/<int:pk>/', CompanyUserDetailView.as_view(),
         name='company_user_detail'),
    path('company/assign-role/<int:pk>/',
         AssignCompanyRoleView.as_view(), name='assign_company_role'),
    path('company/activate-deactivate/<int:pk>/',
         ActivateDeactivateUserView.as_view(), name='activate_deactivate_user'),
]
