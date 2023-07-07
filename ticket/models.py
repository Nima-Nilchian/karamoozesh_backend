from django.core.validators import RegexValidator
from django.db import models
from custom_lib.models import BaseModel
from consultation.models import Skill, Consultant
from django.contrib.auth import get_user_model


class Ticket(BaseModel):
    LEVEL_CHOICES = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    )
    STATUS_CHOICES = (
        ('A', 'Active'),
        ('E', 'Ended')
    )
    title = models.CharField(max_length=200, null=False, blank=False)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='A')
    phone_number = models.CharField(max_length=20, null=True, blank=True, validators=[
        RegexValidator(regex=r"^(09|\+989)\d{9}$", message='the phone number is wrong!')
    ])
    meeting_date = models.DateTimeField(null=True, blank=True)
    skill_level = models.CharField(max_length=1, choices=LEVEL_CHOICES, null=True, blank=True)


class QA(BaseModel):
    user_id = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name='QA', null=True, blank=True
    )
    question = models.TextField()
    consultant_id = models.ForeignKey(
        Consultant, on_delete=models.CASCADE, related_name='QA', null=True, blank=True
    )
    answer = models.TextField(null=True, blank=True)
    last_time_question = models.DateTimeField(auto_now_add=True)
    last_time_answer = models.DateTimeField(null=True, blank=True)
    ticket_id = models.ForeignKey(
        Ticket, on_delete=models.CASCADE, related_name='QA', null=True, blank=True
    )


class TicketTag(BaseModel):
    ticket_id = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='ticket_tags')
    tag = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='ticket_tags')
