# apartments/api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apartments.api.views import ApartmentViewSet, DoorViewSet, RoomViewSet, GuestRoomListView, CheckCPCView, ApartmentInfoViewSet, CheckDoorsStatusView

router = DefaultRouter()
router.register(r"apartments", ApartmentViewSet, basename="apartment")
router.register(r"doors", DoorViewSet, basename="door")
router.register(r"rooms", RoomViewSet, basename="room")
router.register(r"apartment-info", ApartmentInfoViewSet, basename="apartment-info")

urlpatterns = [
    path("", include(router.urls)),
    path("guest-room/", GuestRoomListView.as_view(), name="guest-room"),
    path("check-cpc/", CheckCPCView.as_view(), name="check-cpc"),
    path("check-doors-status/", CheckDoorsStatusView.as_view(), name="check-doors-status"),
]
