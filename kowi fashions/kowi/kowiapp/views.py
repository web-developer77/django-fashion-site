from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import auth,User
from .models import *
def index(request):
    return render(request, 'index.html', {'title':'index'})

#dashboardofuser
#dashboardofemployee
#admin redesign

#logout
#reset pass
#index - feedback

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
                customer = CustInfo.objects.create(user=user,gender=gender,skintone=skintone,height=height,weight=weight,haircolors=haircolors,mobno=mobno,age=age)
                messages.info(request,'User Created')
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
            return redirect('/')
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
            return redirect('/')
        else:
            messages.info(request,'Invalid Credentials')
            return redirect('login')

    else:
        return render(request,'elogin.html',{'title':title})