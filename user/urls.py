from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.registration_views, name='register'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change-password'),
]
