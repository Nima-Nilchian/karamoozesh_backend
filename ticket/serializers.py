from rest_framework import serializers, status
from .models import *
from consultation.serializers import ConsultantSerializers, SkillSerializers
from consultation.models import Consultant, Skill
from user.serializers import UserSerializer
from rest_framework.response import Response


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name']


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['created_time', 'question', 'user_id']


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['created_time', 'answer', 'consultant_id']


class TicketListSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, source='ticket_tags')
    phone_number = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    last_date = serializers.SerializerMethodField()
    messages = serializers.SerializerMethodField()

    class Meta:
        model = Ticket
        fields = ['id', 'title', 'status', 'tags', 'meeting_date', 'skill_level', 'contact_way',
                  'email', 'phone_number', 'last_date', 'messages']

    def get_last_date(self, instance):
        return instance.answer.order_by('created_time').last().created_time

    def get_email(self, instance):
        return instance.question.first().user_id.email

    def get_phone_number(self, instance):
        return instance.question.first().user_id.profile.phone_number

    def get_messages(self, instance):
        questions = QuestionSerializer(many=True, instance=Question.objects.filter(ticket_id=instance)).data
        answers = AnswerSerializer(many=True, instance=Answer.objects.filter(ticket_id=instance)).data
        combined_list = answers + questions

        return sorted(combined_list, key=lambda k: k['created_time'])

