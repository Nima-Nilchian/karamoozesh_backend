from django.db import models


class BaseModel(models.Model):
    created_time = models.DateTimeField(verbose_name='created time', auto_now_add=True)
    updated_time = models.DateTimeField(verbose_name='updated time', auto_now=True)

    class Meta:
        abstract = True
