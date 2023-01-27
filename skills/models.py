from django.db import models
from custom_lib.models import BaseModel


class Subject(BaseModel):
    description = models.TextField(blank=True, null=True)
    statistics = models.TextField(blank=True, null=True)
    roadmap = models.ImageField(upload_to='image/skills/roadmaps', null=True, blank=True)


class Link(BaseModel):
    address = models.URLField(null=True, blank=True)
    subject_id = models.ForeignKey(Subject, related_name='links', on_delete=models.CASCADE)
