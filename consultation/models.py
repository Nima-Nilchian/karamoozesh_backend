from django.core.validators import RegexValidator
from django.db import models
from custom_lib.models import BaseModel
from user.models import User


class Consultant(BaseModel):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE, related_name='consultant')
    phone_number = models.CharField(max_length=20, null=True, blank=True, validators=[
        RegexValidator(regex=r"^(09|\+989)\d{9}$", message='the phone number is wrong!')])

    def __str__(self):
        return f'{self.user_id}: {self.user_id.first_name} {self.user_id.last_name}'


class Skill(BaseModel):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class ConsultantSkills(BaseModel):
    LEVEL_CHOICES = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    )
    consultant_id = models.ForeignKey(Consultant, on_delete=models.CASCADE, related_name='consultant_skills')
    skill_id = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='consultant_skills')
    skill_level = models.CharField(max_length=1, choices=LEVEL_CHOICES)
