from django.urls import path
from . import views

urlpatterns = [
    # ticket
    path('', views.TicketCreateView.as_view(), name='create-ticket'),
    path('send-message/', views.TicketSendMessageView.as_view(), name='send-message'),
    path('end/', views.TicketEndView.as_view(), name='end-ticket'),
]
