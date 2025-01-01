from rest_framework import serializers
from users.models import Profile, CheckInProfile, Guest, BillingInfo
from django.contrib.auth.models import User
from apartments.models import Apartment

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["id", "user"]

class GuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guest
        fields = '__all__'

class BillingInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillingInfo
        fields = '__all__'

class CheckInProfileSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CheckInProfile
        fields = ['name', 'surname', 'guest_number', 'source',
                  'check_in_date', 'check_out_date',
                  'check_in_time', 'check_out_time', 'apartment', 'password',
                  'username', 'psw', 'id','require_document_photo', 'require_registration_form', 
                  'require_billing_info', 'got_billing_info', 'got_registration_form', 'room', 'room_name']
        

    def create(self, validated_data):
        password = validated_data.pop('password')
        name = validated_data['name']
        surname = validated_data['surname']
        base_username = f"{name}.{surname}".lower()
        username = base_username

        # Check if the username already exists and append a number if it does
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1

        user = User.objects.create_user(username=username, password=password)

        # Check if a profile already exists for the user
        profile, created = Profile.objects.get_or_create(user=user, defaults={'profile_type': 'guest'})
        if not created:
            profile.profile_type = 'guest'
            profile.save()

        checkin_profile = CheckInProfile.objects.create(user=user, **validated_data)
        checkin_profile.username = username
        checkin_profile.psw = password
        checkin_profile.save()
        return checkin_profile
    
class CheckInProfileGuestSerializer(serializers.ModelSerializer):
    apartment_name = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()
    google_maps_link = serializers.SerializerMethodField()

    class Meta:
        model = CheckInProfile
        fields = ['name', 'surname', 'check_in_date',
                  'check_in_time', 'check_out_date',
                  'check_out_time', 'guest_number',
                  'apartment', 'apartment_name', 'address', 'google_maps_link', 'id', 
                  'require_document_photo', 'require_registration_form', 
                  'require_billing_info', 'got_billing_info', 'got_registration_form',
                  'room_name']
        
    def get_apartment_name(self, obj):
        # Ottieni il nome dell'appartamento tramite l'ID
        try:
            apartment = Apartment.objects.get(id=obj.apartment.id)
            return apartment.name
        except Apartment.DoesNotExist:
            return None

    def get_address(self, obj):
        # Ottieni l'indirizzo dell'appartamento tramite l'ID
        try:
            apartment = Apartment.objects.get(id=obj.apartment.id)
            return apartment.address
        except Apartment.DoesNotExist:
            return None

    def get_google_maps_link(self, obj):
        # Ottieni il link di Google Maps dell'appartamento tramite l'ID
        try:
            apartment = Apartment.objects.get(id=obj.apartment.id)
            return apartment.google_maps_link
        except Apartment.DoesNotExist:
            return None

class CheckInProfileDetailSerializer(serializers.ModelSerializer):
    guests = GuestSerializer(many=True, read_only=True, source='guest_details')
    billing_info = BillingInfoSerializer(many=True, read_only=True)
    apartment_name = serializers.SerializerMethodField()

    class Meta:
        model = CheckInProfile
        fields = ['id', 'name', 'surname', 'guest_number', 'source',
                  'check_in_date', 'check_out_date', 'check_in_time', 'check_out_time',
                  'apartment', 'apartment_name', 'got_billing_info', 'got_registration_form', 'guests', 'billing_info',
                  'got_document_photo']

    def get_apartment_name(self, obj):
        try:
            apartment = Apartment.objects.get(id=obj.apartment.id)
            return apartment.name
        except Apartment.DoesNotExist:
            return None