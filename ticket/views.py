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


class TicketCreateView(generics.CreateAPIView):
    serializer_class = TicketCreateSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ticket = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        data = serializer.data
        data['ticket_id'] = ticket.id
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()


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

