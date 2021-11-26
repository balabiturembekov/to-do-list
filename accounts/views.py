import uuid
import sys

from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login, logout as auth_logout

from accounts.models import Token


def send_login_email(request):
    ''' Выслать ссылку на логин по почте '''
    email = request.POST['email']
    uid = str(uuid.uuid4())
    Token.objects.create(email=email,uid=uid)
    print('Saving uid', uid, 'for email', email, file=sys.stderr)
    url = request.build_absolute_uri(f'/accounts/login?uid={uid}')
    send_mail(
            'Your login link for superlists',
            f'use this link to log in:\n\n{url}',
            'noreplay@superlists',
            [email],
        )
    return render(request, 'login_email_send.html')


def login(request):
    ''' Регистрация пользователя в системе '''
    print('Login View', file=sys.stderr)
    uid = request.GET.get('uid')
    user = authenticate(uid=uid)
    if user is not None:
        auth_login(request, user)

    return redirect('/')


def logout(request):
    ''' Выход из системы '''
    auth_logout(request)
    return redirect('/')
