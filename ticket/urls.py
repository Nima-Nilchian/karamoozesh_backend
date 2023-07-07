from django.urls import path
from . import views


urlpatterns = [
    # ticket
    path('ticket/', views.TicketList.as_view(), name='ticket-list'),
    path('ticket/<int:pk>/', views.TicketDetail.as_view(), name='ticket-detail'),

    # skill
    path('qa/', views.QAList.as_view(), name='qa-list'),
    path('qa/<int:pk>/', views.QADetail.as_view(), name='qa-detail'),

    # consultant skills
    path('ticket-tag/', views.TicketTagList.as_view(), name='ticket-tag-list'),
    path('ticket-tag/<int:pk>/', views.TicketTagDetail.as_view(), name='ticket-tag-detail'),
]