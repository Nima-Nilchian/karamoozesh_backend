from django.urls import path
from . import views


urlpatterns = [
    # cv
    path('',views.CvList.as_view(), name='resume_list'),
    path('<int:pk>/',views.CvDetail.as_view(), name='resume_detail'),

    # link
    path('<int:cv_id>/link/',views.LinkListView.as_view() , name='link_list'),
    path('<int:cv_id>/link/<int:link_id>/',views.LinkDetailView.as_view() , name='link_detail'),

    # project
    path('<int:cv_id>/project/',views.ProjectListView.as_view() , name='project_list'),
    path('<int:cv_id>/project/<int:project_id>/',views.ProjectDetailView.as_view() , name='project_detail'),

    # certificate
    path('<int:cv_id>/certificate/',views.CertificateListView.as_view() , name='certificate_list'),
    path('<int:cv_id>/certificate/<int:certificate_id>/',views.CertificateDetailView.as_view() , name='certificate_detail'),

    # skill
    path('<int:cv_id>/skill/', views.SkillListView.as_view(), name='skill_list'),
    path('<int:cv_id>/skill/<int:skill_id>/', views.SkillDetailView.as_view(),name='skill_detail'),

    # education
    path('<int:cv_id>/education/', views.EducationListView.as_view(), name='education_list'),
    path('<int:cv_id>/education/<int:education_id>/', views.EducationDetailView.as_view(),name='education_detail'),

    # work
    path('<int:cv_id>/work/', views.WorkListView.as_view(), name='work_list'),
    path('<int:cv_id>/work/<int:work_id>/', views.WorkDetailView.as_view(),name='work_detail'),

    # language
    path('<int:cv_id>/language/', views.LanguageListView.as_view(), name='language_list'),
    path('<int:cv_id>/language/<int:language_id>/', views.LanguageDetailView.as_view(),name='language_detail'),


]