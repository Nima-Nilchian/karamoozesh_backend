from rest_framework import serializers, status
from .models import Ticket, TicketTag, QA
from consultation.serializers import ConsultantSerializers
from consultation.models import Consultant, Skill
from user.serializers import UserSerializer
from rest_framework.response import Response


class QASerializers(serializers.ModelSerializer):
    consultant = ConsultantSerializers(source='consultant_id', read_only=True)
    user = UserSerializer(source='user_id', read_only=True)

    class Meta:
        model = QA
        fields = [
            'ticket_id',
            'user_id',
            'user',
            'question',
            'consultant_id',
            'consultant',
            'answer',
            'last_time_question',
            'last_time_answer',
            'created_time',
            'updated_time',
        ]


class TicketTagSerializers(serializers.ModelSerializer):
    class Meta:
        model = TicketTag
        fields = [
            'ticket_id',
            'tag',
            'created_time',
            'updated_time',
        ]


class TicketSerializers(serializers.ModelSerializer):
    qa = QASerializers(many=True, required=False)
    tag = TicketTagSerializers(many=True, required=False)

    class Meta:
        model = Ticket
        fields = [
            'id',
            'title',
            'status',
            'meeting_date',
            'skill_level',
            'qa',
            'tag',
            'created_time',
            'updated_time',
        ]


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
        QA.objects.create(user_id=self.context['request'].user,
                          question=self.validated_data['question'],
                          ticket_id=ticket)
        for tag_name in self.validated_data.get('tags', None):
            tag = Skill.objects.get(name=tag_name)
            TicketTag.objects.create(ticket_id=ticket, tag=tag)
        return Response({'message': 'ticket has successfully created!'}, status.HTTP_201_CREATED)
