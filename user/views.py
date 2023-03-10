from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import ProfileSettingSerializer, ProfileActivitySerializer
from rest_framework import generics
from rest_framework import status
from .models import User, Profile
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token


@api_view(['GET', ])
def user_id_getter(request):
    if request.method == 'GET':
        token = request.META.get('HTTP_AUTHORIZATION')
        user_id = Token.objects.filter(key=token)
        if user_id:
            user_id = user_id.first().user_id
            return Response({"user_id": user_id}, status=status.HTTP_200_OK)

        return Response({"message": "User Not Found"}, status=status.HTTP_400_BAD_REQUEST)

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

