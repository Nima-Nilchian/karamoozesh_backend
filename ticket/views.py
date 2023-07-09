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

# class TicketList(generics.ListAPIView):
#     queryset = Ticket.objects.all()
#     serializer_class = TicketSerializers
#     filterset_fields = (
#         'status', 'skill_level'
#     )
#     search_fields = ('status', 'title')
#     ordering_fields = ["created_time", "updated_time", "meeting_date"]
#     ordering = ["-meeting_date"]
#     permission_classes = (IsAuthenticated, IsConsultant)
#
#
# class TicketDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Ticket.objects.all()
#     serializer_class = TicketSerializers
#     # permission_classes = (IsAdminUser,)
#     permission_classes = (IsAuthenticated,)
#
#
# class QAList(generics.ListCreateAPIView):
#     queryset = QA.objects.all()
#     serializer_class = QASerializers
#     filterset_fields = (
#         'consultant_id',
#     )
#     search_fields = ('question', 'answer')
#     ordering_fields = [
#         "created_time", "updated_time",
#         "last_time_question", "last_time_answer"
#     ]
#     ordering = ["-created_time"]
#     # permission_classes = (IsAdminUser,)
#     permission_classes = (IsAuthenticated,)
#
#
# class QADetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = QA.objects.all()
#     serializer_class = QASerializers
#     # permission_classes = (IsAdminUser,)
#     permission_classes = (IsAuthenticated,)
#
#
# class TicketTagList(generics.ListCreateAPIView):
#     queryset = TicketTag.objects.all()
#     serializer_class = TicketTagSerializers
#     filterset_fields = (
#         'tag',
#     )
#     search_fields = ('tag',)
#     ordering_fields = [
#         "created_time", "updated_time"
#     ]
#     ordering = ["-created_time"]
#     # permission_classes = (IsAdminUser,)
#     permission_classes = (IsAuthenticated,)
#
#
# class TicketTagDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = TicketTag.objects.all()
#     serializer_class = TicketTagSerializers
#     # permission_classes = (IsAdminUser,)
#     permission_classes = (IsAuthenticated,)


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




