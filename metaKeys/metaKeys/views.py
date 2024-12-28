# views.py
from django.http import HttpResponse
from django.conf import settings
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from users.models import CheckInProfile
import os

def trigger_error(request):
    division_by_zero = 1 / 0
    return HttpResponse("This will never be reached")

@login_required
def protected_media(request, path):
    print("Funzione protected_media chiamata")
    print(f"Richiesta per il file: {path} da parte dell'utente: {request.user}")

    # Estrai l'ID del CheckInProfile dal percorso del file
    parts = path.split('/')
    if len(parts) < 2:
        print("Percorso del file non valido")
        raise Http404

    checkin_profile_id = parts[6]
    print(f"ID del CheckInProfile estratto: {checkin_profile_id}")

    try:
        checkin_profile = CheckInProfile.objects.get(id=checkin_profile_id)
        print(f"CheckInProfile trovato: {checkin_profile}")
    except CheckInProfile.DoesNotExist:
        print(f"CheckInProfile con ID {checkin_profile_id} non trovato")
        raise Http404

    # Verifica se l'utente autenticato è l'owner del CheckInProfile
    if request.user.id != checkin_profile.owner.id:
        print(f"L'utente {request.user} non ha il permesso di accedere a questo file")
        return HttpResponse("You do not have permission to access this file.", status=403)

    media_path = os.path.join(settings.MEDIA_ROOT, path)
    print(f"Percorso del file multimediale: {media_path}")
    if os.path.exists(media_path):
        with open(media_path, 'rb') as f:
            print(f"File trovato: {media_path}")
            return HttpResponse(f.read(), content_type="image/jpeg")
    else:
        print(f"File non trovato: {media_path}")
        raise Http404