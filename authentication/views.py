from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from .serializers import RegisterSerializer, EmailSerializer,\
    ResetPasswordSerializer, LoginSerializer, ChangePasswordSerializer
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from user.models import User, Profile
from .utils import Util
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse


@api_view(['POST', ])
def registration_views(request):
    if request.method == 'POST':
        serializer = RegisterSerializer(data=request.data)
        dataa = {}

        if serializer.is_valid(raise_exception=True):

            user = serializer.save()
            Profile.objects.create(user_id=user)
            current_site = get_current_site(request).domain

            data = Util.email_verification_body(user, current_site)
            Util.send_email(data)

            dataa['username'] = user.username
            dataa['email'] = user.email

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(dataa, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def verify_email_view(request):
    if request.method == 'GET':
        token = request.GET.get('token')
        user = Token.objects.filter(key=token)
        if user:
            user = user.first().user
            if not user.is_verified:
                user.is_verified = True
                user.save()

            return Response({"email": "Successfully Activated"}, status=status.HTTP_200_OK)

        return Response({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST', ])
def login_view(request):
    if request.method == 'POST':
        data = {}

        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        data['username'] = serializer.validated_data['user'].username
        data['token'] = token.key

        return Response(data, status=status.HTTP_200_OK)


class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)

            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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

            context_data = {'name': user.username, 'url': reset_link}
            data = Util.password_reset_body(context_data, user.email)

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
