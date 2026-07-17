from rest_framework import permissions
from config.permissions import IsAdminOrReadOnly

class AdminOrReadOnlyPermissionMixin:
    permission_classes = [IsAdminOrReadOnly]


class AuthenticatedOrReadOnlyPermissionMixin:
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class StaffOnlyPermissionMixin:
    permission_classes = [permissions.IsAdminUser]
    
# class DetailListingPermission:
#     permission_classes = [permissions.IsAuthenticated]
    
    
class AuthenticatedPermissionMixin:
    permission_classes = [permissions.IsAuthenticated]