
from django.shortcuts import render
from rest_framework import generics, status, views, permissions
from rest_framework.decorators import api_view

from .serializers import EmailVerificationSerializer, RegisterSerializer
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
            account = serializer.save()
            user_data = serializer.data
            user = User.objects.get(email=user_data['email'])
            token, created = Token.objects.get_or_create(user=user)
            current_site = get_current_site(request).domain
            relativeLink = reverse('email-verify')
            absurl = 'http://' + current_site + relativeLink + "?token=" + str(token.key)
            email_body = 'Hi ' + user.username + \
                         ' Use the link below to verify your email \n' + absurl
            data = {'email_body': email_body, 'to_email': user.email,
                    'email_subject': 'Verify your email'}

            Util.send_email(data)
            dataa['response'] = 'Registration Successfully'
            dataa['username'] = account.username
            dataa['email'] = account.email

        else:
            dataa = serializer.errors

        return Response(dataa, status=status.HTTP_201_CREATED)

class VerifyEmail(views.APIView):
    serializer_class = EmailVerificationSerializer
