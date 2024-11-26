from rest_framework.permissions import BasePermission, SAFE_METHODS


class LibrarianOrReaderReadOnlyPermission(BasePermission):

    def has_permission(self, request, view):
        return (
            (
                request.user.is_librarian or
                request.user.is_admin
            ) or (
                request.user.is_reader and
                request.method in SAFE_METHODS
            )
        )
