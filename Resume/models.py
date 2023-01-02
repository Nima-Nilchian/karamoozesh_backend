from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Language(models.Model):
    LEVEL_CHOICES = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    )
    title = models.CharField(max_length=250)
    level = models.CharField(max_length=1, choices=LEVEL_CHOICES)


class Work(models.Model):
    title = models.CharField(max_length=250)
    company = models.CharField(max_length=250)
    industry = models.CharField(max_length=250)
    start_date = models.DateField(blank=True)
    end_date = models.DateField(blank=True,null=True)
    until_now = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)


class Education(models.Model):
    grade = models.CharField(max_length=250)
    field_of_study = models.CharField(max_length=250)
    university = models.CharField(max_length=250)
    start_date = models.DateField()
    end_date = models.DateField(blank=True,null=True)
    until_now = models.BooleanField(default=False)
    created_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)


class Skill(models.Model):
    LEVEL_CHOICES = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    )
    skill = models.CharField(max_length=250)
    level = models.CharField(max_length=1,choices=LEVEL_CHOICES)

class Certificate(models.Model):
    title = models.CharField(max_length=250)
    institute = models.CharField(max_length=250)
    file = models.FileField(blank=True,upload_to='files/certificate/%Y/%d/%m/',null=True)
    issue_date = models.DateField()
    expiration_date = models.DateField(blank=True)
    description = models.TextField(blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)



class Project(models.Model):
    title = models.CharField(max_length=250)
    link = models.URLField()
    description = models.TextField(blank=True)

class Link(models.Model):
    title = models.CharField(max_length=250)
    link = models.URLField()

class Resume(models.Model):

    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    DUTY_SYSTEM_CHOICES = (
        ('1','معافیت تحصیلی'),
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
        ('1','منزوی'),
        ('2','دارای روحیه تیمی '),
        ('3','متمایل به ارتباط'),
        ('4','نداشتن تمایل به ارتباط')
    )
    firstname = models.CharField(max_length=250)
    lastname = models.CharField(max_length=250)
    avatar = models.ImageField(upload_to='image/resume/avatar',blank=True)
    about_me = models.TextField()
    phone_number = models.BigIntegerField()
    gender = models.CharField(max_length=1,choices=GENDER_CHOICES)
    character = models.CharField(max_length=100,choices=CHARACTER_CHOICES,blank=True)
    user_id = models.OneToOneField(User,on_delete=models.CASCADE,related_name='resume')
    duty_system = models.CharField(max_length=1,choices=DUTY_SYSTEM_CHOICES)
    martial_status = models.CharField(max_length=1,choices=MARTIAL_STATUS_CHOICES)
    data_of_birth = models.DateField()
    city = models.CharField(max_length=250)
    address = models.TextField(blank=True)
    suggested_salary = models.BigIntegerField(blank=True)
    work_experience = models.ManyToManyField(Work,related_name='resume',blank=True,)
    education = models.ManyToManyField(Education,related_name='resume',blank=True)
    skill = models.ManyToManyField(Skill,related_name='resume')
    certificate = models.ManyToManyField(Certificate,related_name='resume',blank=True)
    link = models.ManyToManyField(Link,related_name='resume',blank=True)
    project = models.ManyToManyField(Project,related_name='resume',blank=True)
    language = models.ManyToManyField(Language,related_name='resume',blank=True)
    # talent_survey = models.ManyToManyField(Talent_survey,related_name='resume',blank=True),
    file = models.FileField(upload_to='files/resume/%Y/%m/%d/',blank=True,null=True)
    is_active = models.BooleanField(default=False)
    created_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)


