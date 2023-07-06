from rest_framework import serializers
from .models import Ticket, TicketTag, QA
from consultation.serializers import ConsultantSerializers
from user.serializers import UserSerializer


class QASerializers(serializers.ModelSerializer):
    consultant = ConsultantSerializers(source='user_id', read_only=True)
    user = UserSerializer(source='user_id', read_only=True)

    class Meta:
        model = QA
        fields = [
            'id',
            'ticket_id',
            'consultant_id',
            'consultant',
            'question',
            'user_id',
            'user',
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
            'ticket',
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
            'created_time',
            'updated_time',
            'last_time_question',
            'last_time_answer',
            'qa',
            'tag',
        ]



