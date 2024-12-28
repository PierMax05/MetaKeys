"""
URL configuration for metaKeys project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include, re_path

from django_registration.backends.one_step.views import RegistrationView
from users.forms import UserForm
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from .views import protected_media

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include("users.api.urls")),
    path("api/", include("apartments.api.urls")),
    path('api/auth/', include('dj_rest_auth.urls')),
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),
    path('api/auth/login/', include('dj_rest_auth.urls')),
    path('api/auth/logout/', include('dj_rest_auth.urls')),
    re_path(r'^media/(?P<path>.*)$', protected_media, name='protected_media'),
    # Route fallback per Vue
    path('', TemplateView.as_view(template_name="index.html"), name='home'),
    # Fallback per tutte le altre route
    re_path(r'^.*$', TemplateView.as_view(template_name="index.html"), name='vue_app'),
] 

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)