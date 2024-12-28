from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    """
    Permesso personalizzato per consentire solo all'owner di accedere e modificare il CheckInProfile.
    """


    def has_permission(self, request, view):
        # Verifica se l'utente è autenticato e ha un profilo di tipo 'owner'
        return request.user.is_authenticated and request.user.profile.profile_type == 'owner'

    def has_object_permission(self, request, view, obj):
        # Verifica se l'utente è l'owner dell'oggetto
        return obj.user == request.user.profile

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Permesso personalizzato per consentire solo agli owner di modificare o cancellare le istanze.
    I guest possono solo leggere.
    """

    def has_permission(self, request, view):
        # I guest possono solo leggere
        if request.method in permissions.SAFE_METHODS:
            return True
        # Gli owner possono creare, modificare e cancellare
        return request.user.is_authenticated and request.user.profile.profile_type == 'owner'

    def has_object_permission(self, request, view, obj):
        # I guest possono solo leggere
        if request.method in permissions.SAFE_METHODS:
            return True
        # Solo chi ha creato l'istanza può modificarla o cancellarla
        return obj.user == request.user.profile