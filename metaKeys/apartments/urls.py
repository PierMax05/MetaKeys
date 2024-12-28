from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ApartmentInfoViewSet

router = DefaultRouter()
router.register(r'apartment-info', ApartmentInfoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
