from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied

class IsAuthenticatedVerified(BasePermission):
    message_auth = "you are not authenticated"
    message_ver = " you have not verified your email"

    def has_permission(self, request, view):
        if not bool(request.user and request.user.is_authenticated and request.user.is_email_verified):
            if not bool(request.user and request.user.is_authenticated):
                raise PermissionDenied(self.message_auth)
            else:
                raise PermissionDenied(self.message_ver)
        return True


class IsVerified(BasePermission):
    message = 'you have not verified your email'

    def has_permission(self, request, view):
        if not bool(request.user and request.user.is_email_verified):
            raise PermissionDenied(self.message)

        return True