from rest_framework import permissions
from .models import Chat


class IsOwnerChat(permissions.BasePermission):
    message = {"errors": {"details": ["Available only for the owner"]}}

    def has_permission(self, request, view):
        """
        Check if the user has permission to access the view.

        For POST requests, the user must provide a 'user_id' field in the request data
        that matches their own user ID. For other methods, the user must be authenticated.

        Args:
            request (HttpRequest): The HTTP request object.
            view (View): The Django view being accessed.

        Returns:
            bool: True if the user has permission, False otherwise.
        """

        if request.method == 'POST':
            try:
                return request.user.id == request.data['owner_id']
            except Exception as e:
                return False
        if request.user.is_authenticated:
            return True

    def has_object_permission(self, request, view, obj):
        """
        Check if the user has permission to access the object.

        The user must be the owner of the object (obj) in order to have permission.

        Args:
            request (HttpRequest): The HTTP request object.
            view (View): The Django view being accessed.
            obj: The object being accessed.

        Returns:
            bool: True if the user has permission, False otherwise.
        """
        if obj.owner_id.id == request.user.id or obj.addressee_id.id == request.user.id:
            return True