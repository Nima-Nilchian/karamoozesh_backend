import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from .models import Ticket
from .serializers import *
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from consultation.permissions import IsConsultant
from django.views import View


@csrf_exempt
def TicketCreateView(request):
    data = json.loads(request.body)
    ticket = Ticket.objects.create(title=data.get('title'),
                                   skill_level=data.get('skill_level', None),
                                   meeting_date=data.get('meeting_date', None),
                                   contact_way=data.get('contact_way', None))
    Question.objects.create(user_id=request.user,
                            question=data['question'],
                            ticket_id=ticket)
    for tag_name in data.get('tags', None):
        Tag.objects.create(name=tag_name, ticket_id=ticket)
    return JsonResponse(data={'ticket_id': ticket.id})


class TicketSendMessageView(generics.CreateAPIView):
    serializer_class = TicketSendMessageSerializer
    permission_classes = [IsAuthenticated]


class TicketEndView(generics.CreateAPIView):
    serializer_class = TicketEndSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return Ticket.objects.get(id=self.request['ticket_id'])

    def check_permissions(self, request):
        if request.user.is_consultant:
            return False
        return True

