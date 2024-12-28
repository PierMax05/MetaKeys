# apartments/api/serializers.py
from rest_framework import serializers
from apartments.models import Apartment, Door, Room, ApartmentInfo


class ApartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Apartment
        exclude = ["user"]

class DoorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Door
        exclude = ["user"]

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        exclude = ["user"]

class GuestDoorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Door
        fields = ["id", "name", "instructions", "priority",
                  "access_type", "access_code"]

class GuestRoomSerializer(serializers.ModelSerializer):
    doors = GuestDoorSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = ["id", "name", "doors"]

class ApartmentInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApartmentInfo
        exclude = ["user"]