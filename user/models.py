from django.contrib.auth.hashers import make_password
from django.db import models
from django.dispatch import receiver
from django.urls import reverse

from custom_lib.models import BaseModel
from talent_survey.models import TalentSurvey
from cv.models import CV
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator, EmailValidator
from django.utils.translation import ugettext_lazy as _
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email, and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(_('email address'), unique=True, validators=[EmailValidator])
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()


class Profile(BaseModel):
    user_id = models.OneToOneField('User', on_delete=models.CASCADE, related_name='profile')
    image = models.ImageField(null=True, blank=True)  # should add upload to
    phone_number = models.CharField(max_length=20, null=True, blank=True, validators=[
        RegexValidator(regex="/^(09|\\+989)\\d{9}$/", message='the phone number is wrong!')])


class FavoriteCVs(BaseModel):
    user_id = models.ForeignKey('User', related_name='favorite_cv', on_delete=models.CASCADE)
    cv_id = models.ForeignKey(CV, related_name='favorite_cv', on_delete=models.CASCADE)


class UserSurvey(BaseModel):
    user_id = models.ForeignKey('User', related_name='surveys', on_delete=models.CASCADE)
    survey_id = models.ForeignKey(TalentSurvey, related_name='users', on_delete=models.CASCADE)
    result = models.URLField()






from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)

    send_mail(
        # title:
        "Password Reset for {title}".format(title="Some website title"),
        # message:
        email_plaintext_message,
        # from:
        "amoozeshyar@local.ir",
        # to:
        [reset_password_token.user.email]
    )
