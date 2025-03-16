from rest_framework import permissions
from rest_framework_simplejwt.tokens import AccessToken
from django.core.exceptions import ObjectDoesNotExist
from users.models import User 

class BasePermissionWithToken(permissions.BasePermission):
    
    def get_access_token(self, request):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return None  
        return auth_header.split(" ")[1] 

    def get_user_from_token(self, token):
        try:
            access = AccessToken(token) 
            return User.objects.get(id=access["user_id"]) 
        except Exception as e:
            return None  

    def is_authenticated_with_role(self, request, roles):
        token = self.get_access_token(request)

        if token is None:
            return None  

        user = self.get_user_from_token(token)
        if user is None:
            return None

        return user.role in roles


class IsAdmin(BasePermissionWithToken):
    def has_permission(self, request, view):
        return self.is_authenticated_with_role(request, ['admin'])


class IsReviewer(BasePermissionWithToken):
    def has_permission(self, request, view):
        return self.is_authenticated_with_role(request, ['reviewer'])


class IsContributor(BasePermissionWithToken):
    def has_permission(self, request, view):
        return self.is_authenticated_with_role(request, ['contributor'])


class IsAdminOrReviewer(BasePermissionWithToken):
    def has_permission(self, request, view):
        return self.is_authenticated_with_role(request, ['admin', 'reviewer'])
    
class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user == view.get_object().auteur or request.method in permissions.SAFE_METHODS

class IsAdminOrContributor(BasePermissionWithToken):
    def has_permission(self, request, view):
        return self.is_authenticated_with_role(request, ['admin', 'contributor'])


class IsReviewerOrContributor(BasePermissionWithToken):
    def has_permission(self, request, view):
        return self.is_authenticated_with_role(request, ['reviewer', 'contributor'])


class IsAuthenticated(BasePermissionWithToken):
    def has_permission(self, request, view):
        return self.is_authenticated_with_role(request, ['reviewer', 'contributor', 'admin'])


class IsAny(BasePermissionWithToken):
    def has_permission(self, request, view):
        return True
