"""
A file contains functions for curator and tokens
"""
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import BasePermission

def get_tokens(user):
    """
    A method used to get the user tokens
    """
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class IsCurator(BasePermission):
    """
    A class used to represent curator
    """
    def has_permission(self, request, view):
        """
        A method used to check whether or not a user is a staff
        """
        return request.user.is_staff
