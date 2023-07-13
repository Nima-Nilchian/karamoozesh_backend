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


class TicketSendMessageSerializer(serializers.Serializer):
    ticket_id = serializers.IntegerField()
    message = serializers.CharField()

    def save(self, **kwargs):
        user = self.context['request'].user
        ticket = Ticket.objects.get(id=self.validated_data['ticket_id'])
        if user.is_consultant:
            Answer.objects.create(consultant_id=user.consultant,
                                  answer=self.validated_data['message'],
                                  ticket_id=ticket)
            ticket.status = '2'
            ticket.save()
        else:
            Question.objects.create(user_id=user,
                                    question=self.validated_data['message'],
                                    ticket_id=ticket)
            ticket.status = '1'
            ticket.save()


class TicketEndSerializer(serializers.Serializer):
    ticket_id = serializers.IntegerField(write_only=True)
    status = serializers.CharField(read_only=True)

    def save(self, **kwargs):
        ticket = Ticket.objects.get(id=self.validated_data['ticket_id'])
        ticket.status = '3'
        ticket.save()


class ConsultantAllRelatedTicketSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    tags = TagSerializer(many=True, source='ticket_tags')
    questions = QuestionSerializer(many=True, source='question')
    phone_number = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()

    class Meta:
        model = Ticket
        fields = ['name', 'tags', 'questions', 'meeting_date', 'skill_level', 'contact_way', 'phone_number', 'email']

    def get_name(self, instance):
        return instance.question.first().user_id.get_full_name()

    def get_phone_number(self, instance):
        return instance.question.first().user_id.profile.phone_number

    def get_email(self, instance):
        return instance.question.first().user_id.email


class TicketCreateSerializer(serializers.ModelSerializer):
    question = serializers.CharField()
    tags = serializers.ListSerializer(child=serializers.CharField())

    class Meta:
        model = Ticket
        fields = ['title', 'skill_level', 'meeting_date', 'contact_way', 'question', 'tags']

    def save(self, **kwargs):
        user = self.context['request'].user
        ticket = Ticket.objects.create(title=self.validated_data.get('title'),
                                       skill_level=self.validated_data.get('skill_level', None),
                                       meeting_date=self.validated_data.get('meeting_date', None),
                                       contact_way=self.validated_data.get('contact_way', None))
        Question.objects.create(user_id=user,
                                question=self.validated_data['question'],
                                ticket_id=ticket)
        for tag_name in self.validated_data.get('tags', None):
            Tag.objects.create(name=tag_name, ticket_id=ticket)
        return ticket

