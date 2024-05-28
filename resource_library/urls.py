from django.urls import path

from resource_library import views

urlpatterns = [
    path('', views.resources, name='resources'),
    path('dictionary/', views.dictionary, name='dictionary'),
]
