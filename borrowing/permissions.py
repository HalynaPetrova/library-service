from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrIsOwner(BasePermission):
    edit_methods = (
        "PUT",
        "DELETE",
    )

    def has_permission(self, request, view):
        return bool(
            (
                request.method in SAFE_METHODS
                or request.method not in self.edit_methods
                and request.user
                and request.user.is_authenticated
            )
            or (request.user and request.user.is_staff)
        )
