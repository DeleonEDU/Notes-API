from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Кастомний пермішин, потрібен буде, якщо
    треба глянути усі існуючі нотатки маючи
    права, тобто, якщо маєш права, можеш
    подивитись чужі нотатки 
    """
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user