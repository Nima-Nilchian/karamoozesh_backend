from rest_framework import generics, status, views, permissions
from rest_framework.decorators import api_view
from .serializers import RegisterSerializer, EmailSerializer, ResetPasswordSerializer
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from user.models import User
from .utils import Util
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse

# Create your views here.

@api_view(['POST', ])
def registration_views(request):
    if request.method == 'POST':
        serializer = RegisterSerializer(data=request.data)
        dataa = {}

        if serializer.is_valid():
            user = serializer.save()
            current_site = get_current_site(request).domain

            data = Util.email_verification_body(user, current_site)
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




class PasswordReset(generics.GenericAPIView):
    # Request for Password Reset Link.
    serializer_class = EmailSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        user = User.objects.filter(email=email).first()
        if user:
            encoded_pk = urlsafe_base64_encode(force_bytes(user.pk))
            token = PasswordResetTokenGenerator().make_token(user)

            reset_url = reverse("reset-password", kwargs={"encoded_pk": encoded_pk, "token": token})
            current_site = get_current_site(request=request).domain
            reset_link = 'http://' + current_site + reset_url

            email_body = 'Hello, \n Use link below to reset your password  \n' + reset_link
            data = {'email_body': email_body, 'to_email': user.email, 'email_subject': 'Reset your passsword'}

            Util.send_email(data)

            return Response("reset email sent successfully", status=status.HTTP_200_OK)
        else:
            return Response({"message": "User doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordAPI(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer

    def patch(self, request, *args, **kwargs):
        # Verify token & encoded_pk , and then reset the password.

        serializer = self.serializer_class(data=request.data, context={"kwargs": kwargs})
        serializer.is_valid(raise_exception=True)

        return Response({"message": "Password reset complete"}, status=status.HTTP_200_OK)