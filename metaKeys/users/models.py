from django.contrib.auth.models import User
from django.db import models
from apartments.models import Apartment, Room
from .utils import PathAndRename
import os
from django.db.models.signals import post_delete, pre_delete
from django.dispatch import receiver
from django.core.validators import FileExtensionValidator
import logging

logger = logging.getLogger(__name__)

class Profile(models.Model):
    id = models.BigAutoField(primary_key=True)
    profile_type = models.CharField(max_length=50, default="owner")
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        logger.debug(f"Saving Profile: {self.user.username}")
        super(Profile, self).save(*args, **kwargs)

class CheckInProfile(models.Model):
    id = models.BigAutoField(primary_key=True)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="guests")
    user = models.OneToOneField(User, on_delete=models.SET_NULL, related_name="guest_profile", null=True, blank=True)
    username = models.CharField(max_length=100, blank=True, null=True)
    psw = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    surname = models.CharField(max_length=100, blank=True, null=True)
    source = models.CharField(max_length=100, blank=True, null=True)
    guest_number = models.IntegerField()
    profile_type = models.CharField(max_length=50, default="guest")
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    check_in_time = models.TimeField()
    check_out_time = models.TimeField()
    active = models.BooleanField(default=True)
    doors_is_active = models.BooleanField(default=False)
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, related_name="guests")
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="guests")
    require_document_photo = models.BooleanField(default=True)
    require_registration_form = models.BooleanField(default=True)
    require_billing_info = models.BooleanField(default=True)
    got_document_photo = models.BooleanField(default=False)
    got_billing_info = models.BooleanField(default=False)
    got_registration_form = models.BooleanField(default=False)
    sent_to_alloggiati_web = models.BooleanField(default=False)  
    sent_to_regional_tourism = models.BooleanField(default=False) 
    invoiced = models.BooleanField(default=False)  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    room_name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.name}-{self.surname}/{self.apartment.name}"

    def is_valid_stay(self):
        return self.check_in_date <= self.check_out_date

    def save(self, *args, **kwargs):
        logger.debug(f"Saving CheckInProfile: {self.name} {self.surname}")
        # Imposta il nome della stanza automaticamente
        if self.room:
            self.room_name = self.room.name
        super(CheckInProfile, self).save(*args, **kwargs)

class Guest(models.Model):
    checkin_profile = models.ForeignKey(CheckInProfile, on_delete=models.CASCADE, related_name="guest_details")
    citizenship = models.CharField(max_length=100, blank=True, null=True)
    place_of_birth = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100,blank=True, null=True)
    first_name = models.CharField(max_length=100,blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=[('F', 'Female'), ('M', 'Male')], blank=True, null=True)
    place_of_issue = models.CharField(max_length=100, blank=True, null=True)
    document_type = models.CharField(max_length=20, choices=[('passport', 'Passport'), ("identity card", "Identity Card")], blank=True, null=True)    
    document_number = models.CharField(max_length=50, blank=True, null=True)
    document_photo = models.ImageField(
        upload_to=PathAndRename("document_photos/"),
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'bmp', 'gif', 'pdf'])],
        blank=True,
        null=True
    )
    document_photo_back = models.ImageField(
        upload_to=PathAndRename("document_photos/"),
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'bmp', 'gif', 'pdf'])],
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def save(self, *args, **kwargs):
        try:
            # Get the old document photo file path
            this = Guest.objects.get(id=self.id)
            # Check if the document photo file has changed
            if this.document_photo != self.document_photo:
                # Delete the old document photo file from the filesystem
                delete_file_and_empty_dirs(this.document_photo.path)
                logger.debug(f"Deleted old document photo for Guest: {self.first_name} {self.last_name}")
            # Check if the document photo back file has changed
            if this.document_photo_back != self.document_photo_back:
                # Delete the old document photo back file from the filesystem
                delete_file_and_empty_dirs(this.document_photo_back.path)
                logger.debug(f"Deleted old document photo back for Guest: {self.first_name} {self.last_name}")
        # If the instance is new and not updated yet
        except Guest.DoesNotExist:
            # Do nothing
            pass
        logger.debug(f"Saving Guest: {self.first_name} {self.last_name}")
        # Save the instance
        super(Guest, self).save(*args, **kwargs)

@receiver(post_delete, sender=Guest)
def delete_document_photo(sender, instance, **kwargs):
    # Delete the document photo file from the filesystem
    if instance.document_photo:
        delete_file_and_empty_dirs(instance.document_photo.path)
        logger.debug(f"Deleted document photo for Guest: {instance.first_name} {instance.last_name}")
    # Delete the document photo back file from the filesystem
    if instance.document_photo_back:
        delete_file_and_empty_dirs(instance.document_photo_back.path)
        logger.debug(f"Deleted document photo back for Guest: {instance.first_name} {instance.last_name}")

@receiver(pre_delete, sender=Guest)
def delete_document_photo_pre_delete(sender, instance, **kwargs):
    # Delete the document photo file from the filesystem
    if instance.document_photo:
        delete_file_and_empty_dirs(instance.document_photo.path)
        logger.debug(f"Deleted document photo for Guest: {instance.first_name} {instance.last_name}")
    # Delete the document photo back file from the filesystem
    if instance.document_photo_back:
        delete_file_and_empty_dirs(instance.document_photo_back.path)
        logger.debug(f"Deleted document photo back for Guest: {instance.first_name} {instance.last_name}")

# Function to delete the file and empty directories
def delete_file_and_empty_dirs(file_path):
    # Delete the file
    if os.path.isfile(file_path):
        # Delete the file
        os.remove(file_path)
        # Remove empty directories
        directory = os.path.dirname(file_path)
        # Get the media root directory
        media_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'media', 'document_photos'))
        # Remove empty directories until the media root directory
        while directory != media_root and directory != '':
            try:
                # Remove the directory
                os.rmdir(directory)
            except OSError:
                # Stop if the directory is not empty
                break
            # Move to the parent directory
            directory = os.path.dirname(directory)

class BillingInfo(models.Model):
    PERSON_TYPE_CHOICES = [
        ('individual', 'Persona Fisica'),
        ('company', 'Azienda'),
    ]

    checkin_profile = models.ForeignKey(CheckInProfile, on_delete=models.CASCADE, related_name="billing_info")
    person_type = models.CharField(max_length=20, choices=PERSON_TYPE_CHOICES)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    vat_number = models.CharField(max_length=50, blank=True, null=True)
    tax_code = models.CharField(max_length=50, blank=True, null=True)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return f"Billing Info for {self.checkin_profile}"