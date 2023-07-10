from django.urls import path
from . import views

urlpatterns = [
    path('profile/setting/', views.ProfileSettingRetrieveUpdateView.as_view(), name='profile-setting'),
    path('profile/activity/', views.ProfileActivityRetrieveView.as_view(), name='profile-activity'),
    path('get_user-id', views.user_id_getter, name='get_user-id'),
    path('profile/ticket/', views.ProfileUserCreatedTicketsView.as_view(), name='profile-tickets')
]
