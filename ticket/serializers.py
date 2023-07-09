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
        fields = ['question']


class TicketCreateSerializer(serializers.ModelSerializer):
    question = QuestionSerializer()
    tags = TagSerializer(many=True, source='ticket_tags')

    class Meta:
        model = Ticket
        fields = ['id', 'title', 'question', 'tags', 'skill_level', 'meeting_date', 'contact_way', 'status']
        write_only_fields = ['title', 'question', 'tags', 'skill_level', 'meeting_date', 'contact_way']

    # def save(self, **kwargs):
    #     ticket = Ticket.objects.create(title=self.validated_data['title'],
    #                                    skill_level=self.validated_data.get('skill_level', None),
    #                                    meeting_date=self.validated_data.get('meeting_date', None),
    #                                    contact_way=self.validated_data.get('contact_way', None))
    #     Question.objects.create(user_id=self.context['request'].user,
    #                             question=self.validated_data['question'],
    #                             ticket_id=ticket)
    #     for tag_name in self.validated_data.get('tags', None):
    #         Tag.objects.create(name=tag_name, ticket_id=ticket)

    # def create(self, validated_data):
    #     ticket = Ticket.objects.create(title=validated_data['title'],
    #                                    skill_level=validated_data.get('skill_level', None),
    #                                    meeting_date=validated_data.get('meeting_date', None),
    #                                    contact_way=validated_data.get('contact_way', None))
    #     Question.objects.create(user_id=self.context['request'].user,
    #                             question=validated_data['question'],
    #                             ticket_id=ticket)
    #     for tag_name in validated_data.get('tags', None):
    #         Tag.objects.create(name=tag_name, ticket_id=ticket)
    #     return ticket
