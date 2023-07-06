from rest_framework import serializers
from .models import Ticket, TicketTag, QA
from consultation.serializers import ConsultantSerializers
from consultation.models import Consultant
from user.serializers import UserSerializer


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
            'qa',
            'tag',
            'created_time',
            'updated_time',
        ]



