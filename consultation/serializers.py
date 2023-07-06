from rest_framework import serializers
from .models import Consultant, Skill, ConsultantSkills
from user.serializers import UserSerializer


class ConsultantSerializers(serializers.ModelSerializer):
    user = UserSerializer(source='user_id', read_only=True)

    class Meta:
        model = Consultant
        fields = [
            'id',
            'user',
            'phone_number',
        ]


class SkillSerializers(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = [
            'id',
            'name',
        ]


class ConsultantSkillsSerializers(serializers.ModelSerializer):
    class Meta:
        model = ConsultantSkills
        fields = [
            'id',
            'consultant_id',
            'skill_id',
            'skill_level',
        ]
