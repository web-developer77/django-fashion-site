from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import auth,User
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required 
from .models import *
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

def index(request):
    trend = trends.objects.all()
    user = request.user
    if user.is_authenticated:
        if request.method == 'POST':
            feed = request.POST['feed']
            feedback(userid=user.id,feed=feed).save()
            messages.info(request,"Feedback Sent")
    return render(request, 'index.html', {'title':'index','trend':trend,})


def edashboard(request):
    title = "KOWI Fashions | Employee Dashboard"
    user = request.user
    if user.is_authenticated and user.is_staff == True:
        try:
            employee = EmployeeInfo.objects.get(id=user.id)
            flag = 0
        except ObjectDoesNotExist:
            flag = 1
        if flag == 0:
            return render(request,'edashboard.html',{'title':title,'employee':employee})
        elif flag == 1:
            messages.error(request,'Complete Profile First')
            return redirect(eupdate)
    else:
        messages.error(request,'Login First')
        return redirect('elogin')
    return render(request,'edashboard.html',{'title':title})

def eupdate(request):
    title = "KOWI Fashions | Employee Update"
    user = request.user
    if user.is_authenticated and user.is_staff == True:
        if request.method == 'POST':
            gender = request.POST['gender']
            mobno = request.POST['mobno']
            age = request.POST['age']
            EmployeeInfo(id=user.id,gender=gender,mobno=mobno,age=age).save()
            return redirect('edashboard')
    else:
        messages.error(request,'Login First')
        return redirect('elogin')
    return render(request,'eupdate.html',{'title':title})

def update(request):
    title = "KOWI Fashions | Profile Update"
    user = request.user
    if user.is_authenticated and user.is_staff == False:
        if request.method == 'POST':
            gender = request.POST['gender']
            height = request.POST['height']
            weight = request.POST['weight']
            skintone = request.POST['skintone']
            haircolors = request.POST['haircolors']
            mobno = request.POST['mobno']
            age = request.POST['age']
            CustInfo(id=user.id,gender=gender,skintone=skintone,height=height,weight=weight,haircolors=haircolors,mobno=mobno,age=age).save()
            return redirect('dashboard')
    else:
        messages.error(request,'Login First')
        return redirect('login')
    return render(request,'update.html',{'title':title})

def dashboard(request):
    title = "KOWI Fashions | User Dashboard"
    user = request.user
    if user.is_authenticated and user.is_staff == False:
        try:
            customer = CustInfo.objects.get(id=user.id)
            flag = 0
        except ObjectDoesNotExist:
            flag = 1
        if flag == 0:
            return render(request,'dashboard.html',{'title':title,'customer':customer})
        elif flag == 1:
            messages.error(request,'Complete Profile First!')
            return redirect(update)
    else:
        messages.error(request,'Login First')
        return redirect('login')
    return render(request,'dashboard.html',{'title':title}) 


def signup(request):
    title = "Register with KOWI Fashions"
    if request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']
        gender = request.POST['gender']
        height = request.POST['height']
        weight = request.POST['weight']
        skintone = request.POST['skintone']
        haircolors = request.POST['haircolors']
        mobno = request.POST['mobno']
        age = request.POST['age']
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,'Username Taken')
                return redirect('signup')
            elif User.objects.filter(email=email).exists():
                messages.info(request,'Email Taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username,password=password1,email=email).save()
                user = auth.authenticate(username=username,password=password1)
                auth.login(request,user)
                us = request.user
                customer = CustInfo.objects.create(id=us.id,gender=gender,skintone=skintone,height=height,weight=weight,haircolors=haircolors,mobno=mobno,age=age)
                us.is_active = False
                us.save()
                current_site = get_current_site(request)
                mail_subject = 'Activate your account.'
                message = render_to_string('registration/acc_active_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                })
                to_email = email
                email = EmailMessage(
                    mail_subject, message, to=[to_email]
                )
                email.send()
                messages.info(request,'Check email and Verify your account')
                return redirect(index)
        else:
            messages.info(request,'Password not matched')
            return redirect('signup')
    return render(request,'signup.html',{'title':title})

def login(request):
    title = "Login with KOWI Fashions"
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username,password=password)
        if user is not None and user.is_staff == False:
            auth.login(request,user)
            messages.info(request,'Logged In')
            return redirect('dashboard')
        else:
            messages.info(request,'Invalid Credentials')
            return redirect('login')

    else:
        return render(request,'login.html',{'title':title})

def elogin(request):
    title = "Employee Login with KOWI Fashions"
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username,password=password)
        if user is not None and user.is_staff == True:
            auth.login(request,user)
            messages.info(request,'Logged In')
            return redirect('edashboard')
        else:
            messages.info(request,'Invalid Credentials')
            return redirect('login')

    else:
        return render(request,'elogin.html',{'title':title})


def logoutuser(request):
    logout(request)
    return redirect('login')

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')