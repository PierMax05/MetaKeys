# views.py
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import viewsets, status
from rest_framework.response import Response
from users.api.serializers import ProfileSerializer, CheckInProfileSerializer, CheckInProfileGuestSerializer, GuestSerializer, BillingInfoSerializer, CheckInProfileDetailSerializer
from users.models import CheckInProfile, Guest, BillingInfo
from users.api.permissions import IsOwner
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.db.models import Q

import logging

logger = logging.getLogger(__name__)

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = "page_size"
    max_page_size = 1000


class CurrentUserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = ProfileSerializer(request.user.profile)
        return Response(serializer.data)

class CheckInProfileViewSet(viewsets.ModelViewSet):
    queryset = CheckInProfile.objects.all()
    serializer_class = CheckInProfileSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        # Filtra i CheckInProfile in base all'owner (utente autenticato)
        return CheckInProfile.objects.filter(owner=self.request.user.profile)

    def perform_create(self, serializer):
        # Imposta l'utente autenticato come owner del CheckInProfile
        serializer.save(owner=self.request.user.profile)

    def perform_destroy(self, instance):
        user = instance.user
        profile = user.profile
        instance.delete()
        profile.delete()
        user.delete()


class UserInformationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        profile_type = request.user.profile.profile_type
        
        return Response({
            'username': user.username,
            'profile_type': profile_type,
            'is_authenticated': user.is_authenticated,
        })


class CheckInProfileListView(generics.ListAPIView):
    serializer_class = CheckInProfileSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        """
        Restituisce il queryset dei CheckInProfile filtrati in base ai parametri di ricerca.
        Se non ci sono parametri di ricerca, restituisce tutti i CheckInProfile dell'owner loggato.
        """
        owner = self.request.user.profile  # Ottiene il profilo dell'utente loggato
        queryset = CheckInProfile.objects.filter(owner=owner)  # Filtra i CheckInProfile per owner

        # Ottiene i parametri di ricerca dalla richiesta
        first_name = self.request.query_params.get('name', None)
        last_name = self.request.query_params.get('surname', None)
        check_in_date = self.request.query_params.get('check_in_date', None)

        # Costruisce la query utilizzando l'operatore Q per combinare i filtri
        query = Q()
        if first_name:
            query &= Q(name__icontains=first_name)
        if last_name:
            query &= Q(surname__icontains=last_name)
        if check_in_date:
            query &= Q(check_in_date=check_in_date)

        # Applica i filtri al queryset
        if query:
            queryset = queryset.filter(query)

        return queryset

    def list(self, request, *args, **kwargs):
        """
        Sovrascrive il metodo list per restituire i risultati della ricerca o i profili correnti.
        """
        queryset = self.get_queryset() # Ottiene il queryset filtrato
        first_name = request.query_params.get('name', None)
        last_name = request.query_params.get('surname', None)
        check_in_date = request.query_params.get('check_in_date', None)

        # Se ci sono parametri di ricerca, restituisce i risultati della ricerca
        if first_name or last_name or check_in_date:
            serializer = self.get_serializer(queryset, many=True)
            return Response({'search_results': serializer.data})

        # Se non ci sono parametri di ricerca, restituisce i profili correnti, precedenti e prossimi
        current_date = timezone.now().date() # Ottiene la data corrente
         # Filtra il profilo di check-in corrente
        current_checkin = queryset.filter(check_in_date=current_date)

        # Serializza i profili corrente
        current_serializer = self.get_serializer(current_checkin, many=True)

        return Response({
            'currents': current_serializer.data,
        })
    

class CheckInProfileGuestViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CheckInProfile.objects.all()
    serializer_class = CheckInProfileGuestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filtra i profili di check-in in base all'utente autenticato
        return CheckInProfile.objects.filter(user=self.request.user)
    

class GuestViewSet(viewsets.ModelViewSet):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        checkin_profile_id = request.data.get('checkin_profile')
        if not checkin_profile_id:
            return Response({"detail": "checkin_profile is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            checkin_profile = CheckInProfile.objects.get(id=checkin_profile_id)
        except CheckInProfile.DoesNotExist:
            return Response({"detail": "CheckInProfile not found."}, status=status.HTTP_404_NOT_FOUND)
        if checkin_profile.user == "null":
            return Response({"detail": "CheckInProfile is not assigned to a user."}, status=status.HTTP_400_BAD_REQUEST)
        # Verifica se l'utente autenticato è uguale a user o owner del checkin profile
        if request.user != checkin_profile.user and request.user.profile != checkin_profile.owner:
            return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)

        response = super().create(request, *args, **kwargs)

        # Imposta got_registration_form a True
        checkin_profile.got_registration_form = True

        # Controlla se è stata ricevuta la foto del documento
        if 'document_photo' in request.data and request.data['document_photo']:
            checkin_profile.got_document_photo = True

        checkin_profile.save()

        return response

    def get_queryset(self):
        return super().get_queryset().filter(checkin_profile__owner=self.request.user.profile)
    
    def get_object(self):
        obj = super().get_object()
        # Verifica se l'utente autenticato è l'owner del checkin profile
        if obj.checkin_profile.owner != self.request.user.profile:
            self.permission_denied(
                self.request, message="You do not have permission to perform this action."
            )
        return obj
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # Handle document_photo field
        if 'document_photo' in request.data:
            if request.data['document_photo'] == '':
                instance.document_photo.delete(save=False)
            else:
                # Imposta got_document_photo a True se è stata caricata una nuova foto del documento
                instance.checkin_profile.got_document_photo = True
                instance.checkin_profile.save()

        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        self.get_object()  # Verifica i permessi
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        self.get_object()  # Verifica i permessi
        return super().destroy(request, *args, **kwargs)
    
class BillingInfoViewSet(viewsets.ModelViewSet):
    queryset = BillingInfo.objects.all()
    serializer_class = BillingInfoSerializer
    permission_classes = [IsAuthenticated]


    def create(self, request, *args, **kwargs):
        checkin_profile_id = request.data.get('checkin_profile')
        if not checkin_profile_id:
            return Response({"detail": "checkin_profile is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            checkin_profile = CheckInProfile.objects.get(id=checkin_profile_id)
        except CheckInProfile.DoesNotExist:
            return Response({"detail": "CheckInProfile not found."}, status=status.HTTP_404_NOT_FOUND)
        if checkin_profile.user=="null":
            return Response({"detail": "CheckInProfile is not assigned to a user."}, status=status.HTTP_400_BAD_REQUEST)
        # Verifica se l'utente autenticato è uguale a user o owner del checkin profile
        if request.user != checkin_profile.user and request.user.profile != checkin_profile.owner:
            return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)

        response = super().create(request, *args, **kwargs)
    
        # Imposta got_billing_info a True
        checkin_profile.got_billing_info = True
        checkin_profile.save()

        return response

    
    def get_queryset(self):
        return super().get_queryset().filter(checkin_profile__owner=self.request.user.profile)
    
    def get_object(self):
        obj = super().get_object()
        # Verifica se l'utente autenticato è l'owner del checkin profile
        if obj.checkin_profile.owner != self.request.user.profile:
            self.permission_denied(
                self.request, message="You do not have permission to perform this action."
            )
        return obj
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        self.get_object()  # Verifica i permessi
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        self.get_object()  # Verifica i permessi
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        self.get_object()  # Verifica i permessi
        return super().destroy(request, *args, **kwargs)

class OwnerCheckInProfileDetailsView(APIView):
    permission_classes = [IsAuthenticated, IsOwner]

    def get(self, request):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        if not start_date or not end_date:
            return Response({"detail": "Both start_date and end_date are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            start_date = timezone.datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = timezone.datetime.strptime(end_date, '%Y-%m-%d').date()
        except ValueError:
            return Response({"detail": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

        checkin_profiles = CheckInProfile.objects.filter(
            owner=request.user.profile,
            check_in_date__range=(start_date, end_date)
        )

        serializer = CheckInProfileDetailSerializer(checkin_profiles, many=True)
        return Response(serializer.data)

