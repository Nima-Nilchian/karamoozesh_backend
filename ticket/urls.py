from django.urls import path
from . import views

urlpatterns = [
    # ticket
    path('', views.TicketCreateView.as_view(), name='create-ticket'),
]
