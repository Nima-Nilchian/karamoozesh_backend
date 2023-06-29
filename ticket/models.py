from django.db import models
from custom_lib.models import BaseModel
from consultation.models import Skill, Consultant
from django.contrib.auth import get_user_model


class Ticket(BaseModel):
    STATUS_CHOICES = (
        ('A', 'Active'),
        ('E', 'Ended')
    )
    title = models.CharField(max_length=200, null=False, blank=False)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='A')


class QA(BaseModel):
    user_id = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, related_name='QA')
    question = models.TextField()
    consultant_id = models.ForeignKey(Consultant, on_delete=models.SET_NULL, related_name='QA', null=True, blank=True)
    answer = models.TextField(null=True, blank=True)
    last_time_question = models.DateTimeField(auto_now_add=True)
    last_time_answer = models.DateTimeField(null=True, blank=True)


class TicketTag(BaseModel):
    ticket_id = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='ticket_tags')
    tag = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='ticket_tags')
