from django.urls import path
from . import views


urlpatterns = [
    # consultant
    path('consultant/', views.ConsultantList.as_view(), name='consultant-list'),
    path('consultant/<int:pk>/', views.ConsultantDetail.as_view(), name='consultant-detail'),

    # skill
    path('skill/', views.SkillList.as_view(), name='skill-list'),
    path('skill/<int:pk>/', views.SkillDetail.as_view(), name='skill-detail'),

    # consultant skills
    path('consultant-skills/', views.ConsultantSkillsList.as_view(), name='consultant-skills-list'),
    path('consultant-skills/<int:pk>/', views.ConsultantSkillsDetail.as_view(), name='consultant-skills-detail'),
]