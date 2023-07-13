from rest_framework import serializers
from rest_framework.authtoken.models import Token
from user.models import UserSurvey

from .models import TalentSurvey


class TalentSurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = TalentSurvey
        fields = "__all__"

    def create(self, validated_data):
        request = self.context.get('request')
        auth_header = request.headers.get('Authorization', None)

        if auth_header:
            token = auth_header.split(' ')[1]
            user = Token.objects.get(key=token).user
            survey = TalentSurvey.objects.create(**validated_data)
            UserSurvey.objects.create(user_id=user, survey_id=survey)
            return survey
        else:
            return serializers.ValidationError('Token not found')
