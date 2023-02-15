from rest_framework import serializers
from .models import TalentSurvey


class TalentSurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = TalentSurvey
        fields = "__all__"
