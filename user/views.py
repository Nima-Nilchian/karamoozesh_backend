from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import RegisterSerializer, ChangePasswordSerializer, LoginSerializer, ProfileSettingSerializer, ProfileActivitySerializer
from rest_framework import generics
from rest_framework import status
from .models import User, Profile
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

# Create your views here.

@api_view(['POST', ])
def registration_views(request):
    if request.method == 'POST':
        serializer = RegisterSerializer(data=request.data)
        data = {}

        if serializer.is_valid():
            account = serializer.save()
            data['response'] = 'Registration Successfully'
            data['username'] = account.username
            data['email'] = account.email

        else:
            data = serializer.errors

        return Response(data)

@api_view(['POST', ])
def login_view(request):
    if request.method == 'POST':
        data = {}

        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        data['response'] = 'Login Successfully'
        data['username'] = serializer.validated_data['user'].username
        data['token'] = token.key

        return Response(data)



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
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileSettingRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSettingSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'patch']

    def get_object(self):
        return Profile.objects.get(user_id=self.request.user)


class ProfileActivityRetrieveView(generics.RetrieveAPIView):
    serializer_class = ProfileActivitySerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

