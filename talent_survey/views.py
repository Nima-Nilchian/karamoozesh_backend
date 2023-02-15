from rest_framework import generics
from custom_lib.permissions import IsStaffOrReadOnly
from .models import TalentSurvey
from .serializers import TalentSurveySerializer


class TalentSurveyList(generics.ListCreateAPIView):
    queryset = TalentSurvey.objects.all()
    serializer_class = TalentSurveySerializer
    permission_classes = (IsStaffOrReadOnly,)
    search_fields = ('name',)
