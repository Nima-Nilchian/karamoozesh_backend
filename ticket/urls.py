from django.urls import path
from . import views

urlpatterns = [
    # ticket
    # path('', views.TicketList.as_view(), name='ticket-list'),
    path('<int:pk>/', views.TicketDetail.as_view(), name='ticket-detail'),
    path('', views.TicketCreateView.as_view(), name='create-ticket'),

    # skill
    path('qa/', views.QAList.as_view(), name='qa-list'),
    path('qa/<int:pk>/', views.QADetail.as_view(), name='qa-detail'),

    # consultant skills
    path('ticket-tag/', views.TicketTagList.as_view(), name='ticket-tag-list'),
    path('ticket-tag/<int:pk>/', views.TicketTagDetail.as_view(), name='ticket-tag-detail'),
]
