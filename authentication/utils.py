from django.core.mail import EmailMessage
import threading
from django.template.loader import get_template
from django.urls import reverse
from rest_framework.authtoken.models import Token


class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


class Util:
    @staticmethod
    def email_verification_body(user, current_site):
        token, created = Token.objects.get_or_create(user=user)

        relative_link = reverse('email-verify')
        url = 'http://' + current_site + relative_link + "?token=" + str(token.key)

        html_tpl_path = 'email_confirmation_template.html'
        context_data = {'name': user.username, 'url': url}
        email_html_template = get_template(html_tpl_path).render(context_data)

        data = {'email_body': email_html_template, 'to_email': user.email,
                'email_subject': 'تایید ایمیل'}
        return data

    @staticmethod
    def password_reset_body(context_data, email):
        html_tpl_path = 'index.html'
        email_html_template = get_template(html_tpl_path).render(context_data)

        data = {'email_body': email_html_template, 'to_email': email,
                'email_subject': 'ریست پسورد'}
        return data

    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['email_subject'], body=data['email_body'], to=[data['to_email']])
        email.content_subtype = 'html'
        EmailThread(email).start()
