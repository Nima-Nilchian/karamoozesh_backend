from rest_framework.decorators import api_view
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from ticket.models import Ticket
from .serializers import ProfileSettingSerializer, ProfileActivitySerializer, ProfileImageSerializer
from ticket.serializers import *
from rest_framework import generics
from rest_framework import status
from .models import Profile, UserSurvey
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework import generics
from rest_framework.response import Response
from talent_survey.serializers import TalentSurveySerializer
from talent_survey.models import TalentSurvey


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


class ProfileUserCreatedTicketsView(generics.ListAPIView):
    serializer_class = TicketListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Ticket.objects.filter(question__user_id=self.request.user).distinct().order_by('created_time')

      
class UserTalentSurveysView(generics.ListAPIView):
    serializer_class = TalentSurveySerializer

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        user_surveys = UserSurvey.objects.filter(user_id=user_id)
        survey_ids = [survey.survey_id_id for survey in user_surveys]
        return TalentSurvey.objects.filter(id__in=survey_ids)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

class ProfileImageView(generics.UpdateAPIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileImageSerializer

    def get_object(self):
        token = self.request.META.get('HTTP_AUTHORIZATION', None)
        token = token.split(' ')[1]
        if token is not None:
            user = Token.objects.get(key=token).user
            prof = Profile.objects.get(user_id=user.id)
            return prof
