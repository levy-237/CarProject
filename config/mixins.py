from rest_framework import permissions
from config.permissions import IsAdminOrReadOnly

class VehicleDataPermission:
    permission_classes = [IsAdminOrReadOnly]


class ListingPermission:
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class StaffPermission:
    permission_classes = [permissions.IsAdminUser]
    
# class DetailListingPermission:
#     permission_classes = [permissions.IsAuthenticated]
    
    
class UserPermission:
    permission_classes = [permissions.IsAuthenticated]