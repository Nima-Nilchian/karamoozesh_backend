
from django.shortcuts import render
from django.template.loader import get_template
from rest_framework import generics, status, views, permissions
from rest_framework.decorators import api_view

from .serializers import RegisterSerializer, ResetPasswordEmailRequestSerializer
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from user.models import User
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.shortcuts import redirect
from django.http import HttpResponsePermanentRedirect
import os
# Create your views here.

@api_view(['POST', ])
def registration_views(request):
    if request.method == 'POST':
        serializer = RegisterSerializer(data=request.data)
        dataa = {}

        if serializer.is_valid():
            user = serializer.save()
            current_site = get_current_site(request).domain

            data = Util.email_body(user, current_site)
            Util.send_email(data)

            dataa['response'] = 'Registration Successfully'
            dataa['username'] = user.username
            dataa['email'] = user.email

        else:
            dataa = serializer.errors

        return Response(dataa, status=status.HTTP_201_CREATED)



@api_view(['get'])
def verify_email_view(request):
    if request.method == 'GET':
        token = request.GET.get('token')
        user = Token.objects.filter(key=token)
        if user:
            user = user.first()
            if not user.is_verified:
                user.is_verified = True
                user.save()

            return Response({"email": "Successfully Activated"}, status=status.HTTP_200_OK)

        return Response({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)


