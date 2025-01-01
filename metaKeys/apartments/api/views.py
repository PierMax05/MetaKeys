# apartments/api/views.py
from apartments.models import Apartment, Door, Room, ApartmentInfo
from apartments.api.serializers import ApartmentSerializer, DoorSerializer, RoomSerializer, GuestRoomSerializer, ApartmentInfoSerializer
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwner, IsOwnerOrReadOnly
from rest_framework import generics
from users.models import CheckInProfile
from django.utils import timezone
from rest_framework.response import Response
import pytz
from rest_framework.decorators import action
from rest_framework.views import APIView
import requests
import threading
from django.db import models
import time

def validate_google_link(google_link):
    if google_link and not google_link.startswith("https://maps.app.goo.gl/"):
        raise ValidationError("Il link deve essere un link di Google Maps.")

class ApartmentViewSet(viewsets.ModelViewSet):

    serializer_class = ApartmentSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        apartments = Apartment.objects.filter(user=self.request.user.id)
        return apartments

    def perform_create(self, serializer):
        # Verifica se l'utente autenticato ha un profilo di tipo "owner"
        if self.request.user.profile.profile_type != 'owner':
            raise PermissionDenied("Solo i proprietari possono creare appartamenti.")
        # Imposta l'utente autenticato come proprietario dell'appartamento
        validate_google_link(serializer.validated_data.get('google_maps_link'))
        serializer.save(user=self.request.user.profile)
    
    def perform_update(self, serializer):
        # Verifica se l'utente autenticato è il proprietario dell'appartamento
        if serializer.instance.user != self.request.user.profile:
            raise PermissionDenied("Non hai il permesso di modificare questo appartamento.")
        validate_google_link(serializer.validated_data.get('google_maps_link'))
        serializer.save()

    def perform_destroy(self, instance):
        # Verifica se l'utente autenticato è il proprietario dell'appartamento
        if instance.user != self.request.user.profile:
            raise PermissionDenied("Non hai il permesso di cancellare questo appartamento.")
        instance.delete()

class DoorViewSet(viewsets.ModelViewSet):

    serializer_class = DoorSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filtra le porte in base all'utente autenticato e all'appartamento specificato
        queryset = Door.objects.filter(user=self.request.user.id)
        apartment_id = self.request.query_params.get('apartment')
        if apartment_id:
            queryset = queryset.filter(apartment_id=apartment_id)
        return queryset
    
    def perform_create(self, serializer):
        # Verifica se l'utente autenticato ha un profilo di tipo "owner"
        if self.request.user.profile.profile_type != 'owner':
            raise PermissionDenied("Solo i proprietari possono creare le porte.")
        # Imposta l'utente autenticato come proprietario della porta
        serializer.save(user=self.request.user.profile)

    def perform_update(self, serializer):
        # Verifica se l'utente autenticato è il proprietario della porta
        if serializer.instance.user != self.request.user.profile:
            raise PermissionDenied("Non hai il permesso di modificare questa porta.")
        serializer.save()

    def perform_destroy(self, instance):
        # Verifica se l'utente autenticato è il proprietario della porta
        if instance.user != self.request.user.profile:
            raise PermissionDenied("Non hai il permesso di cancellare questa porta.")
        instance.delete()

class RoomViewSet(viewsets.ModelViewSet):

    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        # Filtra le stanze in base all'utente autenticato e all'appartamento specificato
        queryset = Room.objects.filter(user=self.request.user.id)
        apartment_id = self.request.query_params.get('apartment')
        if apartment_id:
            queryset = queryset.filter(apartment_id=apartment_id)
        return queryset

    def perform_create(self, serializer):
        # Verifica se l'utente autenticato ha un profilo di tipo "owner"
        if self.request.user.profile.profile_type != 'owner':
            raise PermissionDenied("Solo i proprietari possono creare stanze.")
        # Imposta l'utente autenticato come proprietario della stanza
        serializer.save(user=self.request.user.profile)

    def perform_update(self, serializer):
        # Verifica se l'utente autenticato è il proprietario della stanza
        if serializer.instance.user != self.request.user.profile:
            raise PermissionDenied("Non hai il permesso di modificare questa stanza.")
        serializer.save()

    def perform_destroy(self, instance):
        # Verifica se l'utente autenticato è il proprietario della stanza
        if instance.user != self.request.user.profile:
            raise PermissionDenied("Non hai il permesso di cancellare questa stanza.")
        instance.delete()

class GuestRoomListView(generics.ListAPIView):
    serializer_class = GuestRoomSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Ottieni il profilo di check-in dell'ospite
        checkin_profile = CheckInProfile.objects.get(user=self.request.user)
        # Ottieni la data e l'ora attuali
        now = timezone.now()
        # Verifica se la data e l'ora attuali sono comprese tra il check-in e il check-out
        if checkin_profile.check_in_date <= now.date() <= checkin_profile.check_out_date:
            if checkin_profile.check_in_date < now.date() or (checkin_profile.check_in_date == now.date() and checkin_profile.check_in_time <= now.time()):
                if checkin_profile.check_out_date > now.date() or (checkin_profile.check_out_date == now.date() and checkin_profile.check_out_time >= now.time()):
                    # Restituisci solo la stanza associata al profilo di check-in dell'ospite
                    return Room.objects.filter(id=checkin_profile.room.id)
        # Se non è durante il periodo di soggiorno, restituisci un queryset vuoto
        return Room.objects.none()

    def list(self, request, *args, **kwargs):
        try:
            # Ottieni il profilo di check-in dell'ospite
            checkin_profile = CheckInProfile.objects.get(user=self.request.user)
            now = timezone.now().astimezone(pytz.timezone('Europe/Rome'))
            check_in_date = checkin_profile.check_in_date.strftime("%d/%m/%Y")
            check_in_time = checkin_profile.check_in_time.strftime("%H:%M")
            
            # Controlla i requisiti mancanti
            missing_requirements = []
            if checkin_profile.require_document_photo and not checkin_profile.got_document_photo:
                missing_requirements.append("foto dei documenti")
            if checkin_profile.require_registration_form and not checkin_profile.got_registration_form:
                missing_requirements.append("form di registrazione")
            if checkin_profile.require_billing_info and not checkin_profile.got_billing_info:
                missing_requirements.append("informazioni di fatturazione")
            if missing_requirements:
                missing_requirements_list = ''.join([f"<li>{req}</li>" for req in missing_requirements])
                return Response({"detail": f"Potrai avere accesso alla stanza dopo aver fornito:<ul>{missing_requirements_list}</ul>"})
            
            # Ottieni il queryset della stanza
            queryset = self.get_queryset()
            if not queryset.exists():
                # Verifica se è troppo presto per accedere alla stanza
                if now.date() < checkin_profile.check_in_date or (now.date() == checkin_profile.check_in_date and now.time() < checkin_profile.check_in_time):
                    return Response({"detail": f"Troppo presto, torna alle {check_in_time} del {check_in_date}."})
                # Verifica se l'accesso alla stanza è scaduto
                elif now.date() > checkin_profile.check_out_date or (now.date() == checkin_profile.check_out_date and now.time() > checkin_profile.check_out_time):
                    return Response({"detail": "Non hai più accesso alla stanza."})
            # Serializza i dati della stanza
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        except Exception as e:
            # Gestisci eventuali errori durante il recupero dei dati della stanza
            return Response({"detail": f"Errore durante il recupero dei dati della stanza: {str(e)}"}, status=500)

class CheckCPCView(APIView):
    permission_classes = [IsAuthenticated]
    last_request_time = {}

    def post(self, request, *args, **kwargs):
        try:
            door_id = request.data.get('door_id')
            cpc = request.data.get('cpc')
            user_id = request.user.id

            # Controlla se l'utente ha fatto una richiesta di recente
            current_time = time.time()
            if user_id in self.last_request_time and current_time - self.last_request_time[user_id] < 10:
                return Response({"detail": "Richiesta troppo frequente. Attendere qualche secondo."}, status=429)

            # Aggiorna il tempo dell'ultima richiesta
            self.last_request_time[user_id] = current_time

            # Ottieni la porta specificata
            door = Door.objects.get(id=door_id)

            # Verifica se l'access type della porta è 'shelly'
            if door.access_type != 'shelly':
                raise PermissionDenied("Accesso non consentito per questo tipo di porta.")

            # Ottieni il profilo di check-in dell'utente loggato
            checkin_profile = CheckInProfile.objects.get(user=request.user)

            # Verifica se l'utente loggato corrisponde allo user del check-in profile
            if door.apartment.user != checkin_profile.owner:
                raise PermissionDenied("Non hai il permesso di accedere a questa porta.")

            # Verifica se il CPC inviato corrisponde a quello impostato sulla porta
            if door.check_position_code == cpc:
                # Ottieni i dettagli dell'appartamento associato
                apartment = checkin_profile.apartment
                server_uri = apartment.server_uri
                auth_key = apartment.auth_key
                device_id = door.id_device
                channel_device = door.channel_device

                # Invia la richiesta POST a Shelly
                response = requests.post(
                    f"{server_uri}/device/relay/control",
                    data={
                        "channel": channel_device,
                        "turn": "on",
                        "id": device_id,
                        "auth_key": auth_key
                    }
                )

                if response.status_code == 200:
                    # Invia la richiesta POST a Shelly per spegnere dopo 5 secondi
                    def send_off_request():
                        off_response = requests.post(
                            f"{server_uri}/device/relay/control",
                            data={
                                "channel": channel_device,
                                "turn": "off",
                                "id": device_id,
                                "auth_key": auth_key
                            }
                        )
                        print(off_response.text)  # Stampa la risposta di Shelly

                    threading.Timer(3.0, send_off_request).start()

                    return Response({"detail": "CPC corretto e richiesta inviata a Shelly."})
                else:
                    return Response({"detail": "CPC corretto, ma errore nella richiesta a Shelly."}, status=response.status_code)
            else:
                return Response({"detail": "CPC errato."}, status=400)

        except Door.DoesNotExist:
            return Response({"detail": "Porta non trovata. Contatta l'Host"}, status=404)
        except CheckInProfile.DoesNotExist:
            return Response({"detail": "Profilo di check-in non trovato. Contatta l'Host"}, status=404)
        except Exception as e:
            return Response({"detail": f"Errore durante il controllo del CPC: {str(e)}, contatta L'Host"}, status=500)

class ApartmentInfoViewSet(viewsets.ModelViewSet):
    serializer_class = ApartmentInfoSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        if self.request.user.profile.profile_type == 'guest':
            checkin_profile = CheckInProfile.objects.get(user=self.request.user)
            return ApartmentInfo.objects.filter(
                models.Q(apartment__guests__user=self.request.user) & ~models.Q(type='room_info') |
                models.Q(room=checkin_profile.room, type='room_info')
            )
        return ApartmentInfo.objects.filter(user=self.request.user.profile)

    def perform_create(self, serializer):
        # Solo gli owner possono creare informazioni sugli appartamenti
        if self.request.user.profile.profile_type != 'owner':
            raise PermissionDenied("Solo i proprietari possono creare informazioni sugli appartamenti.")
        validate_google_link(serializer.validated_data.get('google_link'))
        serializer.save(user=self.request.user.profile)

    def perform_update(self, serializer):
        # Solo chi ha creato l'istanza può modificarla
        if serializer.instance.user != self.request.user.profile:
            raise PermissionDenied("Non hai il permesso di modificare queste informazioni.")
        validate_google_link(serializer.validated_data.get('google_link'))
        serializer.save()

    def perform_destroy(self, instance):
        # Solo chi ha creato l'istanza può cancellarla
        if instance.user != self.request.user.profile:
            raise PermissionDenied("Non hai il permesso di cancellare queste informazioni.")
        instance.delete()

class CheckDoorsStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        result = []
        apartments = Apartment.objects.filter(server_uri__isnull=False).exclude(server_uri__exact='')
        for apartment in apartments:
            doors = Door.objects.filter(apartment=apartment, access_type='shelly')
            for door in doors:
                try:
                    response = requests.post(
                        f"{apartment.server_uri}/device/status",
                        data={
                            "id": door.id_device,
                            "auth_key": apartment.auth_key
                        }
                    )
                    if response.status_code == 200:
                        data = response.json()
                        status = {
                            "isok": data.get("isok", False),
                            "connected": data.get("data", {}).get("device_status", {}).get("cloud", {}).get("connected", False),
                        }
                    else:
                        status = {
                            "isok": False,
                            "connected": False,
                            "response": "server non raggiungibile"
                        }
                except requests.exceptions.RequestException:
                    status = {
                        "isok": False,
                        "connected": False,
                        "response": "server non raggiungibile"
                    }
                
                result.append({
                    "apartment_name": apartment.name,
                    "door_name": door.name,
                    "door_id": door.id,
                    "status": status
                })
        return Response(result)