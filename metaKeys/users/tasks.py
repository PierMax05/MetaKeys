from celery import shared_task
from django.utils import timezone
from datetime import datetime
from .models import CheckInProfile, Guest
from django.contrib.auth.models import User
import os

@shared_task
def delete_expired_checkin_data():
    now = timezone.now().date()
    checkin_profiles = CheckInProfile.objects.filter(check_out_date__lt=now)
    for profile in checkin_profiles:
        # Cancella i campi username, psw e l'utente associato
        profile.username = None
        profile.psw = None
        if profile.user:
            profile.user.delete()
            profile.user = None
        profile.save()

        # Cancella i campi document_number e document_photo dai modelli Guest associati
        guests = Guest.objects.filter(checkin_profile=profile)
        for guest in guests:
            guest.document_number = None
            if guest.document_photo:
                delete_file_and_empty_dirs(guest.document_photo.path)
                guest.document_photo = None
            guest.save()

def delete_file_and_empty_dirs(file_path):
    if os.path.isfile(file_path):
        os.remove(file_path)
        print(f"Deleted file: {file_path}")
        # Remove empty directories
        directory = os.path.dirname(file_path)
        media_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'media', 'document_photos'))
        while directory != media_root and directory != '':
            try:
                os.rmdir(directory)
                print(f"Deleted directory {directory}")
            except OSError:
                print(f"Break directory: {directory}")
                break
            directory = os.path.dirname(directory)