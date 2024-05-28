from django.urls import path

from profile_page import views

urlpatterns = [
    path("<str:username>", views.profile_page, name="profile_page"),
    path('settings/', views.profile_settings, name="profile_settings"),
    path('logout/', views.logout_page, name="logout")
]
