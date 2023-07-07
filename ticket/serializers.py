from rest_framework import serializers, status
from .models import *
from consultation.serializers import ConsultantSerializers, SkillSerializers
from consultation.models import Consultant, Skill
from user.serializers import UserSerializer
from rest_framework.response import Response


class TicketCreateSerializer(serializers.ModelSerializer):
    question = serializers.CharField()
    tags = serializers.ListField(child=serializers.CharField())

    class Meta:
        model = Ticket
        fields = ['title', 'question', 'tags', 'skill_level', 'phone_number', 'meeting_date']

    def save(self, **kwargs):
        ticket = Ticket.objects.create(title=self.validated_data['title'],
                                       skill_level=self.validated_data.get('skill_level', None),
                                       phone_number=self.validated_data.get('phone_number', None),
                                       meeting_date=self.validated_data.get('meeting_date', None))
        Question.objects.create(user_id=self.context['request'].user,
                                question=self.validated_data['question'],
                                ticket_id=ticket)
        for tag_name in self.validated_data.get('tags', None):
            Tag.objects.create(name=tag_name)
        return Response({'message': 'ticket has successfully created!', 'ticket_id': ticket.id}, status.HTTP_201_CREATED)
