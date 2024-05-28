"""
URL configuration for ALPP project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

import feedback.views
import registration_handle.views
from ALPP import settings
from ALPP.swagger import schema_view

urlpatterns = ([
    path('admin/', admin.site.urls),
    path('api/', include('modules.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('',  include('registration_handle.urls')),
    path("accounts/", include("allauth.urls")),
    path('profile/', include("profile_page.urls")),
    path('register/', registration_handle.views.register, name='register'),
    path('langs/', include("modules.urls")),
    path('about/', registration_handle.views.about, name='about'),
    path('forums/', include("discussion_forums.urls")),
    path('resources/', include("resource_library.urls")),
    path('feedback/', feedback.views.feedback, name='feedback'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
