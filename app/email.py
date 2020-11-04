import requests
from .models import *
from decouple import config
from django.core.mail import EmailMessage
import requests
from datetime import datetime
from validate_email import validate_email


def validador_email_correct(request):
    if((request.GET.get('email').__contains__('.'))and(request.GET.get('email').__contains__('.'))):
        list = ['com','org','br']
        email = request.GET.get('email')
        new_email = email.split('.')
        for x in list:
            if(new_email[1] == x):
                return validate_email(email)
        
    else:
        return False
    
    
def verificador_email_db(email):
    if(Users.objects.filter(email=email)):
        return True
    else:
        return False


def send_email(request, email):
    email_subject = 'Ativação de Conta !!'
    email_body = 'Não responda esse email, esta é uma validação automatica !!'
    email = EmailMessage(
        email_subject,
        email_body,
        config('EMAIL_HOST_USER'),
        [email],
    )
    email.send(fail_silently=False)


def recaptcha(request):
    dt_object = datetime.fromtimestamp(1545730073)
    recaptcha_response = request.POST.get('g-recaptcha-response')
    data = {
        'success': 'true',
        'challenge_ts': dt_object,
        'hostname': recaptcha_response,
    }
    requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
    
