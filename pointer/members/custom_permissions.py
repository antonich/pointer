from rest_framework import permissions

from point.models import Pointer

class PointerAuthorPermission(permissions.BasePermission):
    """
    Global permission check if request user is author of pointer.
    """

    def has_permission(self, request, view):
        pass
        # return True if request.user ==
