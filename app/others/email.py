from app.models import *
from django.core.mail import EmailMessage
from validate_email import validate_email
from django.contrib.sites.shortcuts import get_current_site


def validador_email_correct(request):
    if((request.GET.get('email').__contains__('.')) and (request.GET.get('email').__contains__('@')) and (validate_email(request.GET.get('email')))):
        list = ['com', 'org', 'br']
        email = request.GET.get('email')
        new_email = email.split('.')
        for x in list:
            if(new_email[1] == x):
                return True
    else:
        return False


def verificador_email_db(request):
    try:
        if(Users.objects.get(email=request.GET.get('email'))):
            return True
    except:
        return False


def send_email(request):

    domain = get_current_site(request).domain
    http=''
    if(str(domain).__contains__('19')):
         http = 'https://'
    else:
        http= 'https://'
    
    link = http+ domain+ '/account/activation?token=' + \
        Users.objects.get(email=request.GET.get('email')).token
    email_subject = 'Ativação de Conta !!'
    email_body = 'Hey ' + \
        request.GET.get(
            'username')+' , Não responda esse email, este é um link de validação automatica !!\n'+link
    email = EmailMessage(
        email_subject,
        email_body,
        to=[request.GET.get('email')],
        from_email=request.GET.get('email'),
        reply_to=['noreply@gmail.com'],
    )
    email.send(fail_silently=False)


def verify_email_existy(request):
    email = request.GET.get('email')
    # verificando se o email existe no banco
    try:
        # se o email existir ele retorna True
        if(Users.objects.get(email=email)):
            return True

    # se o email nao existir
    except:
        return False
