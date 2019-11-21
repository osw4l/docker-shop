from rest_framework.permissions import BasePermission


class IsTiendaUser(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'usuariotienda')


