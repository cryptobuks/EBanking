


from django.db import models
import datetime
from django.utils import timezone
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.shortcuts import render
from django.http import HttpResponse

# Create your models here.
from django.contrib.auth.models import User
from django.db import models

from mongoengine import *
from django.core.mail import send_mail

from django.conf import settings

connect('CreateAccount')



class CreateAccount(Document):
    firstName = StringField(max_length=50)
    lastName = StringField(max_length=50)
    phoneNum = IntField(max_length=10)
    ssn = IntField(max_length=9)
    address = StringField(max_length=4096)
    email = StringField(max_length=4096)
    userName = StringField(max_length=4096, unique=True)
    password = StringField(max_length=4096)
    verification = StringField(max_length=4096)
    accNum = IntField(max_length=10, unique=True)
    accNick = StringField(max_length=4096)
    billing = StringField(max_length=4096)
    authUser = SortedListField(StringField(), default = [])
    dateOpened = DateTimeField()
    status = StringField(max_length=4096)
    date = DateTimeField()

class Accounts(Document):
    First_name = StringField(max_length=50)
    Last_name = StringField(max_length=50)
    User_name = StringField(max_length=4096, unique=True)
    Account_use = StringField(max_length=50)
    Account_type = StringField(max_length=50)
    Acc_number = IntField(max_length=50)
    Rout_number = IntField(max_length=50)
    Acc_nickname = StringField(max_length=50)

class Mail(Document):
    user = StringField(max_length=50)
    email = StringField(max_length=4096)
    activation_key = StringField(maxlength=40)
    date = DateTimeField()

class VerCode (Document):
    User_name = StringField(max_length=4096, unique=True)
    Email = StringField(max_length=4096)
    Password = StringField(max_length=4096)
    Ver_code = IntField(max_length=4, unique=True)
    date = DateTimeField()

class Redirects(Document):
    url = StringField(max_length=4096)
    msg = StringField(max_length=4096)

def mail_activation(user, email, activation_key):
    email_body = "Hello %s,\n\n\
        and thanks for signing up for a PTCeBanking account!\n\n\
        To activate your account, click this link within 24 hours:\n\nhttp://localhost:8000/activate/%s" % (user, activation_key)
    send_mail('Activate PTCeBanking Account', email_body, settings.EMAIL_HOST_USER, [email])

def mail_verify(user, attribute=None):
    from random import randint
    m = CreateAccount.objects.get(userName = user)
    date = datetime.datetime.now() + datetime.timedelta(minutes=10)
    n = False
    while n == False:
        try:
            ver_code = randint(1000, 9999)
            n = VerCode(User_name=user, Email=m.Email,Password=m.Password,Ver_code=ver_code,date=date)
            n.save()
        except:
            VerCode.objects.filter(User_name=user).delete()
    if attribute == None:
        email_body = "Hello %s,\n\n\
        Please enter the following code in the verification page to confirm login: %d" % (user, ver_code)
        send_mail('Verify Login', email_body, settings.EMAIL_HOST_USER, [m.Email])
    else:
        email_body = "Hello %s,\n\n\
            Please enter the following code in the verification page to confirm %s change: %d" % (user, attribute, ver_code)
        send_mail('Verify Update', email_body, settings.EMAIL_HOST_USER, [m.Email])



