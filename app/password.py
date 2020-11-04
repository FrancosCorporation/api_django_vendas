from django.contrib.auth.hashers import make_password, check_password


def encrpty_password(password):
    return make_password(password)


def decripyt_password(password,password_encrypt):
    return check_password(password,password_encrypt)