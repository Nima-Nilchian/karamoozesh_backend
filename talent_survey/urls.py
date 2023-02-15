from django.urls import path
from . import views


urlpatterns = [
    path('', views.TalentSurveyList.as_view(), name='talent-survey-list'),
]
