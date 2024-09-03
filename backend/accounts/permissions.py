from rest_framework import permissions


class IsSuperAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.role == 'super_admin'


class IsCompanyAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.role in ['super_admin', 'company_admin']

    def has_object_permission(self, request, view, obj):
        # Company admins can only manage users within their own company
        return obj.company == request.user.company


class IsCompanyAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        # Allow GET, HEAD or OPTIONS requests for any authenticated user
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        # Allow only company admins to perform write operations
        return request.user and request.user.role == 'company_admin'

    def has_object_permission(self, request, view, obj):
        # Company admins can only manage users within their own company
        return obj.company == request.user.company


class IsProjectManagerOrHigher(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.role in ['super_admin', 'company_admin', 'project_manager']


class IsTeamMemberOrHigher(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.role in ['super_admin', 'company_admin', 'project_manager', 'team_member']


class IsClientOrHigher(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.role in ['super_admin', 'company_admin', 'project_manager', 'team_member', 'client']
