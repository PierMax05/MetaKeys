from rest_framework import permissions
from ..models import CheckInProfile

class IsOwnProfileOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user == request.user

class IsOwner(permissions.BasePermission):
    """
    Permesso personalizzato per consentire solo all'owner di accedere e modificare il CheckInProfile.
    """


    def has_permission(self, request, view):
        # Verifica se l'utente è autenticato e ha un profilo di tipo 'owner'
        return request.user.is_authenticated and request.user.profile.profile_type == 'owner'

    def has_object_permission(self, request, view, obj):
        # Verifica se l'utente è l'owner dell'oggetto
        return obj.owner == request.user.profile

