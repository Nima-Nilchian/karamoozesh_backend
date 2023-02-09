from django.urls import path
from . import views


urlpatterns = [
    # subject
    path('subject/', views.SubjectList.as_view(), name='subject-list'),
    path('subject/<int:pk>/', views.SubjectDetail.as_view(), name='subject-detail'),

    # link
    path('link/', views.LinkList.as_view(), name='link-list'),
    path('link/<int:pk>/', views.LinkDetail.as_view(), name='link-detail'),
]
