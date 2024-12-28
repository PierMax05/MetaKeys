from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter
from users.api.views import (CurrentUserAPIView, CheckInProfileViewSet, UserInformationView, 
                            CheckInProfileListView, CheckInProfileGuestViewSet, GuestViewSet,
                            BillingInfoViewSet, OwnerCheckInProfileDetailsView,
                            )

router = DefaultRouter()
router.register(r'register/checkin', CheckInProfileViewSet, basename='checkin-profile-create')
router.register(r'checkin-profiles-guest', CheckInProfileGuestViewSet, basename='checkinprofileguest')
router.register(r'guests-registration', GuestViewSet, basename='guests-registration')
router.register(r'billing-info', BillingInfoViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("user/", CurrentUserAPIView.as_view(), name="current-user"),
    path('user_information/', UserInformationView.as_view(), name='get_user_information'),
    path('checkin-profiles/', CheckInProfileListView.as_view(), name='checkin-profiles'),
    path('owner-checkin-details/', OwnerCheckInProfileDetailsView.as_view(), name='owner-checkin-details'),
]

