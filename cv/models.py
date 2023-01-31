from django.db import models
from django.conf import settings
from custom_lib.models import BaseModel


class CV(BaseModel):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    DUTY_SYSTEM_CHOICES = (
        ('1', 'معافیت تحصیلی'),
        ('2', 'معافیت'),
        ('3', 'مشمول'),
        ('4', 'پایان خدمت'),
    )
    MARTIAL_STATUS_CHOICES = (
        ('1', 'متاهل'),
        ('2', 'مجرد'),
        ('3', 'تمایل به اعلام ندارم'),
    )
    CHARACTER_CHOICES = (
        ('1', 'منزوی'),
        ('2', 'دارای روحیه تیمی'),
        ('3', 'متمایل به ارتباط'),
        ('4', 'نداشتن تمایل به ارتباط')
    )
    firstname = models.CharField(max_length=250)
    lastname = models.CharField(max_length=250)
    avatar = models.ImageField(upload_to='image/cv/avatar', blank=True, null=True)
    about_me = models.TextField(blank=True, null=True)
    phone_number = models.BigIntegerField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    character = models.CharField(max_length=100, choices=CHARACTER_CHOICES, blank=True, null=True)
    user_id = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cv')
    duty_system = models.CharField(max_length=1, choices=DUTY_SYSTEM_CHOICES)
    martial_status = models.CharField(max_length=1, choices=MARTIAL_STATUS_CHOICES)
    data_of_birth = models.DateField()
    city = models.CharField(max_length=250)
    address = models.TextField(blank=True, null=True)
    suggested_salary = models.BigIntegerField(blank=True, null=True)
    file = models.FileField(upload_to='files/cv/%Y/%m/%d/', blank=True, null=True)
    is_active = models.BooleanField(default=False)


class Language(BaseModel):
    LEVEL_CHOICES = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    )
    title = models.CharField(max_length=250)
    level = models.CharField(max_length=1, choices=LEVEL_CHOICES)
    cv_id = models.ForeignKey(CV, related_name='languages', blank=True, on_delete=models.CASCADE)


class Work(BaseModel):
    title = models.CharField(max_length=250)
    company = models.CharField(max_length=250)
    industry = models.CharField(max_length=250, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    until_now = models.BooleanField(default=False)
    description = models.TextField(blank=True, null=True)
    cv_id = models.ForeignKey(CV, related_name='works', blank=True, null=True, on_delete=models.CASCADE)


class Education(BaseModel):
    grade = models.CharField(max_length=250)
    field_of_study = models.CharField(max_length=250)
    university = models.CharField(max_length=250)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    until_now = models.BooleanField(default=False)
    gpa = models.FloatField(blank=True, null=True)
    cv_id = models.ForeignKey(CV, related_name='educations', blank=True, null=True, on_delete=models.CASCADE)


class Skill(BaseModel):
    LEVEL_CHOICES = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    )
    skill = models.CharField(max_length=250)
    level = models.CharField(max_length=1, blank=True, null=True, choices=LEVEL_CHOICES)
    cv_id = models.ForeignKey(CV, related_name='skills', blank=True, null=True, on_delete=models.CASCADE)


class Certificate(BaseModel):
    title = models.CharField(max_length=250)
    institute = models.CharField(max_length=250)
    file = models.FileField(blank=True, upload_to='files/certificate/%Y/%d/%m/', null=True)
    issue_date = models.DateField()
    expiration_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    cv_id = models.ForeignKey(CV, related_name='certificates', blank=True, null=True, on_delete=models.CASCADE)


class Project(BaseModel):
    title = models.CharField(max_length=250)
    link = models.URLField()
    description = models.TextField(blank=True, null=True)
    cv_id = models.ForeignKey(CV, related_name='projects', blank=True, null=True, on_delete=models.CASCADE)


class Link(BaseModel):
    title = models.CharField(max_length=250)
    link = models.URLField()
    cv_id = models.ForeignKey(CV, related_name='links', blank=True, null=True, on_delete=models.CASCADE)
