from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import auth,User
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required 
from .models import *
def index(request):
    return render(request, 'index.html', {'title':'index'})


#logout
#reset pass
#index - feedback
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
                messages.info(request,'Customer Created')
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