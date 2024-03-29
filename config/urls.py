"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


# Customizing django admin
admin.site.site_header = 'KarAmoozesh Administration'  # default: "Django Administration"
admin.site.index_title = 'KarAmoozesh'  # default: "Site administration"
admin.site.site_title = 'KarAmoozesh admin'  # default: "Django site admin"

urlpatterns = [
    path('admin/', admin.site.urls),

    # rest-framework
    path('api-auth/', include('rest_framework.urls')),

    # drf-Spectacular - Swagger
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # user
    path('user/', include('user.urls')),
    path('api/user/', include('authentication.urls')),
    
    # cv
    path('api/cv/', include('cv.urls')),

    # skills
    path('api/skills/', include('skills.urls')),

    # talent survey
    path('api/talent-survey/', include('talent_survey.urls')),

    # consultation
    path('api/consultation/', include('consultation.urls')),

    # ticket
    path('api/ticket/', include('ticket.urls')),
]
