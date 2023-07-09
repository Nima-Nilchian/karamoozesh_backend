from django.db import models
from custom_lib.models import BaseModel
from consultation.models import Skill, Consultant
from django.contrib.auth import get_user_model

from user.models import User


class Ticket(BaseModel):
    LEVEL_CHOICES = (
        ('1', 'آشنا نیستم'),
        ('2', 'تا حدودی آشنایی دارم'),
        ('3', 'کاملا آشنا هستم')
    )
    STATUS_CHOICES = (
        ('1', 'درحال بررسی'),
        ('2', 'پاسخ داده شده'),
        ('3', 'اتمام مکالمه')
    )
    CONTACTWAY_CHOICES = (
        ('1', 'مشاوره تلفنی'),
        ('2', 'پیامک'),
        ('3', 'ایمیل')
    )
    title = models.CharField(max_length=200, null=False, blank=False)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='1')
    meeting_date = models.DateField(null=True, blank=True)
    skill_level = models.CharField(max_length=1, choices=LEVEL_CHOICES, null=True, blank=True)
    contact_way = models.CharField(max_length=1, choices=CONTACTWAY_CHOICES, null=True, blank=True)


class Question(BaseModel):
    ticket_id = models.ForeignKey(
        Ticket, on_delete=models.CASCADE, related_name='question'
    )
    user_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='question', null=True, blank=True
    )
    question = models.TextField()


class Answer(BaseModel):
    ticket_id = models.ForeignKey(
        Ticket, on_delete=models.CASCADE, related_name='answer'
    )
    consultant_id = models.ForeignKey(
        Consultant, on_delete=models.CASCADE, related_name='answer'
    )
    answer = models.TextField()


class Tag(BaseModel):
    TAG_CHOICES = (
        ('html', 'اچ تی ام ال'),
        ('css', 'سی اس اس'),
        ('javascript', 'جاوا اسکریپت'),
        ('typescript', 'تایپ اسکریپت'),
        ('frontend', 'فرانت اند'),
        ('python', 'پایتون'),
        ('backend', 'بک اند'),
        ('ai', 'هوش مصنوعی'),
        ('nlp', 'ان ال پی')
    )
    ticket_id = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='ticket_tags')
    name = models.CharField(max_length=50, choices=TAG_CHOICES)
