from django.db import models
from custom_lib.models import BaseModel


class TalentSurvey(BaseModel):
    name = models.CharField(max_length=250)
    result = models.URLField()

    def __str__(self):
        return self.name
