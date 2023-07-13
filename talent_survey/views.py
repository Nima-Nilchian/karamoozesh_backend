from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from custom_lib.permissions import IsStaffOrReadOnly
from .models import TalentSurvey
from .serializers import TalentSurveySerializer


class TalentSurveyList(generics.CreateAPIView):
    # queryset = TalentSurvey.objects.all()
    serializer_class = TalentSurveySerializer
    permission_classes = (IsAuthenticated,)
    # permission_classes = (IsStaffOrReadOnly,)
    # search_fields = ('name',)


