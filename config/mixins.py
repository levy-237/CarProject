from rest_framework import permissions


class VehicleDataPermission:
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
