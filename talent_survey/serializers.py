from rest_framework import serializers
from .models import TalentSurvey


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = TalentSurvey
        fields = "__all__"


