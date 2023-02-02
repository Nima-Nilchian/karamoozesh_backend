from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.registration_views, name='register'),
    path('login/', views.login_view, name='login'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change-password'),
    path('profile/setting/', views.ProfileSettingRetrieveUpdateView.as_view(), name='profile'),
]
