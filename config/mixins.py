from rest_framework import permissions

# we customize those later, for now we will use the default permissions

class VehicleDataPermission:
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ListingPermission:
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
class DetailListingPermission:
    permission_classes = [permissions.IsAuthenticated]
    
    
class UserPermission:
    permission_classes = [permissions.IsAuthenticated]