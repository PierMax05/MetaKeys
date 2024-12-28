import logging
from django.db import models

logger = logging.getLogger(__name__)

class Apartment(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        "users.Profile", on_delete=models.CASCADE, related_name="apartment"
    )
    server_uri = models.URLField(max_length=200, blank=True, null=True)
    auth_key = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        logger.debug(f"Saving Apartment: {self.name}")
        super(Apartment, self).save(*args, **kwargs)

class Room(models.Model):
    apartment = models.ForeignKey(Apartment, related_name='rooms', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    doors = models.ManyToManyField("Door", related_name="rooms", blank=True)
    user = models.ForeignKey(
        "users.Profile", on_delete=models.CASCADE, related_name="rooms"
    )

    def __str__(self):
        return f"{self.name} in {self.apartment.name}"

    def save(self, *args, **kwargs):
        logger.debug(f"Saving Room: {self.name} in {self.apartment.name}")
        super(Room, self).save(*args, **kwargs)

class Door(models.Model):
    ACCESS_TYPE_CHOICES = [
        ('shelly', 'Shelly'),
        ('codice', 'Codice'),
        ('solo istruzioni', 'Solo Istruzioni'),
    ]

    apartment = models.ForeignKey(
        "Apartment", related_name="doors",
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        "users.Profile", on_delete=models.CASCADE, related_name="doors"
    )
    name = models.CharField(max_length=40)
    priority = models.IntegerField(default=1)
    id_device = models.CharField(max_length=255, null=True, blank=True)
    check_position_code = models.CharField(max_length=10, null=True, blank=True)
    access_code = models.CharField(max_length=20, null=True, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    instructions = models.TextField(max_length=5000, null=True, blank=True)
    access_type = models.CharField(max_length=20, choices=ACCESS_TYPE_CHOICES, default='solo istruzioni')
    channel_device = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        logger.debug(f"Saving Door: {self.name}")
        super(Door, self).save(*args, **kwargs)

class ApartmentInfo(models.Model):
    INFO_TYPE_CHOICES = [
        ('general', 'General'),
        ('parking_info', 'Parking Information'),
        ('restaurants', 'Restaurants'),
        ('nearby', 'Nearby'),
        ('places_to_visit', 'Places to Visit'),
        ('apartment_info', 'Apartment Information'),
        ('room_info', 'Room Information'),
    ]
    user = models.ForeignKey(
        "users.Profile", on_delete=models.CASCADE, related_name="apartment_info"
    )
    title = models.CharField(max_length=255)
    apartment = models.ForeignKey(Apartment, related_name="apartment_info", on_delete=models.CASCADE, null=True, blank=True)
    room = models.ForeignKey(Room, related_name="apartment_info", on_delete=models.CASCADE, null=True, blank=True)
    google_link = models.URLField(max_length=200, null=True, blank=True)
    info = models.TextField(max_length=5000, null=True, blank=True)
    type = models.CharField(max_length=20, choices=INFO_TYPE_CHOICES, default='general')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        logger.debug(f"Saving ApartmentInfo: {self.title}")
        super(ApartmentInfo, self).save(*args, **kwargs)


