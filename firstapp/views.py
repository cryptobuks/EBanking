from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.template.response import TemplateResponse


# Create your views here.

#from firstapp.forms import CreateAccountForm

from models import CreateAccount, Mail, VerCode, Redirects, Accounts
import models
#from firstapp.forms import NameForm
#from firstapp.models import Name

from random import randint
from django.core.mail import send_mail
import datetime, random, sha
from forms import CreateAccountForm

from django.views.generic.base import TemplateView


def sign_up(request):
    if request.method == 'POST' and request.POST.get('password') == request.POST.get('rePassword'):
        form = CreateAccountForm(request.POST)
        if form.is_valid():
            m = form.save()
            try:
                m.save()
            except:
                m = CreateAccount()
                return render(request, 'Sign_up.html', {'form': m})  # There will be a validation error on this page
            dateOpened = datetime.datetime.now()
            date = datetime.datetime.now() + datetime.timedelta(1)
            status = 'Activation Required'
            n =False
            while n == False:
                try:
                    accNum = randint(1000000000, 9999999999)
                    m.accNum = accNum
                    m.save()
                    n = True
                except:
                    pass
            m.accNick = str(accNum)
            m.dateOpened = dateOpened
            m.status = status
            m.date = date
            salt = sha.new(str(random.random())).hexdigest()[:5]
            activation_key = sha.new(salt + str(m.userName)).hexdigest()
            key_expires = date
            mailer = Mail.objects.create(user=m.userName,email=m.email,activation_key=activation_key,date=key_expires)
            mailer.save()
            models.mail_activation(m.userName, m.email, activation_key)
            m.save()
            return HttpResponseRedirect ('/Success1')
        else:
            m = CreateAccount()
            return render(request, 'Sign_up.html', {'form': m}) #There will be a validation error on this page
    else:
        m = CreateAccount()
        return render(request, 'Sign_up.html', {'form': m})

def activation(request, activation_key):
    if Mail.objects.get(activation_key=activation_key):
        q = Mail.objects.get(activation_key=activation_key)
        m = CreateAccount.objects.get(User_name=q.user)
        m.Status = 'Active'
        del m.date
        m.save()
        Mail.objects.filter(activation_key=activation_key).delete()
        return HttpResponseRedirect('/Success2')
    else:
        return HttpResponse('Sorry, your activation link has expired')


def login(request):
    request.session.clear()
    if request.method == 'POST':
        if request.POST.get('Login'):
            User_name = request.POST.get('User_name')
            Password = request.POST.get('Password')
            request.session['User_name'] = User_name
            request.session.set_expiry(600)
            m = CreateAccount.objects.get(User_name=User_name)
            if m.Verification == 'True' and m.Status == 'Active' and m.User_name == User_name and m.Password == Password:
                models.mail_verify(User_name)
                return HttpResponseRedirect ('/Verification')
            elif m.Satus == 'Active' and m.Username == User_name and m.Password == Password:
                return HttpResponseRedirect ('/Main')
        else:
            return HttpResponseRedirect('/Sign-up')
    else:
        return render(request, 'login.html',)

def verify(request):
    if request.method == 'POST':
        User_name = request.session['User_name']
        m = CreateAccount.objects.get(User_name=User_name)
        Password = request.POST.get('Password')
        ver = request.POST.get('Code')
        s = VerCode.objects.get(User_name=User_name)
        if int(ver) == s.Ver_code and m.Password == Password:
            s.delete()
            return HttpResponseRedirect ('/Main')
        else:
            return HttpResponse('Incorrect verification information')
    else:
        return render(request, 'Verification.html')

def redirects(request, key):
    if key == '3':
        q = Redirects.objects.all()
        q.delete()
        url = '/accountProfile'
        msg = 'Thank you, your profile has been updated. You are being redirected back the Account Profile page...'
        q = Redirects.objects.create(url=url, msg=msg)
    else:
        q = Redirects.objects.all()
        q.delete()
        url = '/'
        if key == '1':
            msg = 'Thank you for signing up, we have sent an activation link to your Email. You are being redirected back the login page...'
        elif key == '2':
            msg = 'Thank you for activating your PTCeBanking Account. You are being redirected back the login page...'
        q = Redirects.objects.create(url=url, msg=msg)
    return render(request, 'Redirects.html', {'q': q})

def main_page(request):
    User_name = request.session['User_name']
    if request.method == 'POST':
        if request.POST.get('logout'):
            return HttpResponseRedirect ('logout')
        else:
            pass
    else:
        return render(request, 'MainPage.html')

def acc_pro(request):
    User_name = request.session['User_name']
    m = CreateAccount.objects.get(User_name = User_name)
    field = ['*'] * len(m.Password)
    m.password = ''.join(field)
    if m.Billing == "Paperless":
        m.billing = "Signed-up"
        m.billchange = "Cancel"
    else:
        m.billing = "Not signed-up"
        m.billchange = "Sign-Up"
    if request.POST.get('User_name'):
        return HttpResponseRedirect('/accountProfilechangeUsername')
    elif request.POST.get('Password'):
        return HttpResponseRedirect('/accountProfilechangePassword')
    elif request.POST.get('Add_user'):
        return HttpResponseRedirect('/accountProfileaddAuthUser')
    elif request.POST.get('Billing'):
        return HttpResponseRedirect('/accountProfilepaperlessEnrollment')
    elif request.POST.get('Contact'):
        return HttpResponseRedirect('/accountProfileupdateContactInfo')
    else:
        return render(request, 'TestProfile.html', {'m' : m})

def change(request, slink):
    User_name = request.session['User_name']
    m = CreateAccount.objects.get(User_name=User_name)
    if request.method == 'POST':
        if request.POST.get('newUsername'):
            models.mail_verify(User_name, 'Username')
            newUsername = request.POST.get("newUsername")
            request.session['newUsername'] = newUsername

        elif request.POST.get('newPassword'):
            models.mail_verify(User_name, 'Password')
            newPassword = request.POST.get('newPassword')
            request.session['newPassword'] = newPassword

        elif request.POST.get('newAuthUser'):
            models.mail_verify(User_name, 'Authorized Users')
            newAuthUser = request.POST.get('newAuthUser')
            request.session['newAuthUser'] = newAuthUser

        elif request.POST.get('newBilling'):
            models.mail_verify(User_name, 'Billing change')
            newBilling = request.POST.get('newBilling')
            request.session['newBilling'] = newBilling

        elif request.POST.get('newAddress') or request.POST.get('newPhone') or request.POST.get('newEmail'):
            models.mail_verify(User_name, 'Contact Information')
            newAddress = request.POST.get('newAddress')
            request.session['newAddress'] = newAddress
            newPhone = request.POST.get('newPhone')
            request.session['newPhone'] = newPhone
            newEmail = request.POST.get('newEmail')
            request.session['newEmail'] = newEmail

        return HttpResponseRedirect('/confirmUpdate')
    else:
        m.q = slink
        if m.Billing == 'Standard':
            m.billchange = "Go Paperless"
        elif m.Billing == 'Paperless':
            m.billchange = 'Cancel Service'
        return render(request, 'Change.html', {'m': m})

def confirm(request):
    if request.method == 'POST':
        Password = request.POST.get('Password')
        User_name = request.session['User_name']
        ver = request.POST.get('Code')
        s = VerCode.objects.get(User_name=User_name)
        m = CreateAccount.objects.get(User_name=User_name)
        if int(ver) == s.Ver_code and m.Password == Password:
            s.delete()
            try:
                try:
                    newUsername = request.session['newUsername']
                    User_name = newUsername
                    request.session['User_name'] = newUsername
                    m.User_name = User_name
                    m.save()
                except:
                    pass
                try:
                    newPassword = request.session['newPassword']
                    m.Password = newPassword
                    m.save()
                except:
                    pass
                try:
                    newAuthUser = request.session['newAuthUser']
                    m.Auth_users.append(newAuthUser)
                    m.save()
                except:
                    pass
                try:
                    if request.session['newBilling']:
                        if m.Billing == "Paperless":
                            m.Billing = 'Standard'
                        elif m.Billing == "Standard":
                            m.Billing = 'Paperless'
                        m.save()
                except:
                    pass
                try:
                    newAddress = request.session['newAddress']
                    if newAddress != '':
                        m.Address = newAddress
                        m.save()
                except:
                    pass
                try:
                    newPhone = request.session['newPhone']
                    if newPhone != '':
                        m.Phone = newPhone
                        m.save()
                except:
                    pass
                try:
                    newEmail = request.session['newEmail']
                    if newEmail != '':
                        m.Email = newEmail
                        m.save()
                except:
                    pass
            except:
                pass
            return HttpResponseRedirect('/Success3')
        else:
            return HttpResponse('Incorrect verification code')
    else:
        return render(request, 'Verification.html')

def add_account(request):
    if request.method == 'POST':
        accountUse = request.POST.get('accountUse')
        accountType = request.POST.get('accountType')
        accountNumber = request.POST.get('accountNumber')
        reAccountNumber = request.POST.get('reAccountNumber')
        rtn = request.POST.get('rtn')
        reRtn = request.POST.get('reRtn')
        nickname = request.POST.get('nickname')
        User_name = request.session['User_name']
        m = CreateAccount.objects.get(User_name=User_name)
        if accountNumber==reAccountNumber and rtn==reRtn:
            q = Accounts.objects.create(First_name=m.First_name,Last_name=m.Last_name,User_name=m.User_name,Account_use=accountUse,
                                        Account_type=accountType,Acc_number=accountNumber,Rout_number=rtn,Acc_nickname=nickname)
            q.save()
            return HttpResponseRedirect('/Main')
    else:
        return render(request, 'addAccount.html')


def logout(request):
    request.session.clear()
    return render(request, 'logout.html')

