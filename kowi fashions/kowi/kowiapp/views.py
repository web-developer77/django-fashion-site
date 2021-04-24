from django.shortcuts import render, redirect
from django.http import Http404
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
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.files.storage import FileSystemStorage
from django.core.exceptions import ObjectDoesNotExist
import datetime
import requests,json
from geopy.geocoders import Nominatim
from decimal import *

def index(request):
    trend = trends.objects.all()
    user = request.user
    TopAuthors =Author.objects.order_by('-rate')[:4]
    AuthorsPost = [Post.objects.filter(auther = author).first() for author in TopAuthors]
    all_post = Paginator(Post.objects.filter(publish = True),3)
    page = request.GET.get('page')
    lat=''
    lng=''
    flag=1
    nearby = []
    if request.method=='POST':
        address = request.POST['add']
        geolocator = Nominatim(user_agent="Kowi")
        location = geolocator.geocode(address)
        if location == None:
            flag=1
            messages.error(request,"Enter Correct Address")
        else:
            flag=0
            lat = location.latitude
            lng = location.longitude
            Decimal(lat)
            Decimal(lng)
            if user.is_authenticated and user.is_staff == False:
                try:
                    customer = CustInfo.objects.get(id=user.id)
                    CustInfo(id=user.id,gender=customer.gender,skintone=customer.skintone,height=customer.height,weight=customer.weight,haircolors=customer.haircolors,mobno=customer.mobno,age=customer.age,lat=lat,lng=lng).save()
                except ObjectDoesNotExist:
                    CustInfo(id=user.id,lat=lat,lng=lng).save()

                employees = EmployeeInfo.objects.all()
                cust = CustInfo.objects.get(id=user.id)
                for employee in employees:
                    latemp = employee.lat
                    lngemp = employee.lng
                    latc = cust.lat
                    lngc = cust.lng
                    distance = dist(latemp,lngemp,latc,lngc)
                    if distance <= 100:
                        nearby.append(employee)
                    
            elif user.is_authenticated and user.is_staff == True:
                try:
                    employee = EmployeeInfo.objects.get(id=user.id)
                    EmployeeInfo(id=user.id,gender=employee.gender,mobno=employee.mobno,age=employee.age,lat=lat,lng=lng).save()
                except ObjectDoesNotExist:
                    EmployeeInfo(id=user.id,lat=lat,lng=lng).save()
            else:
                messages.error(request,'Login First')

    try:
        posts = all_post.page(page)
    except PageNotAnInteger:
        posts = all_post.page(1)
    except EmptyPage:
        posts = all_post.page(all_post.num_pages)

    #if user.is_authenticated:
    #    if request.method == 'POST':
     #       feed = request.POST['feed']
      #      feedback(userid=user.id,feed=feed).save()
       #     messages.info(request,"Feedback Sent")
    
    parms = {
		'posts': posts,
        'author_post':AuthorsPost,
        'title':'index',
        'trend':trend,
        'lat':lat,
        'lng':lng,
        'flag':flag,
        'nearby':nearby,
	}
    return render(request, 'index.html', parms)


def edashboard(request):
    title = "KOWI Fashions | Employee Dashboard"
    user = request.user
    if user.is_authenticated and user.is_staff == True:
        try:
            employee = EmployeeInfo.objects.get(id=user.id)
            geolocator = Nominatim(user_agent="Kowi")
            indent = str(employee.lat)+","+str(employee.lng)
            location = geolocator.reverse(indent)
            return render(request,'edashboard.html',{'title':title,'employee':employee,'location':location})
        except ObjectDoesNotExist:
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
            geolocator = Nominatim(user_agent="Kowi")
            indent = str(customer.lat)+","+str(customer.lng)
            location = geolocator.reverse(indent)
            return render(request,'dashboard.html',{'title':title,'customer':customer,'location':location})
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

def post(request, id, slug):
	try:
		post = Post.objects.get(pk=id, slug=slug)
	except:
		raise Http404("Post Does Not Exist")	

	post.read+=1
	post.save()

	if request.method == 'POST':
		comm = request.POST.get('comm')
		comm_id = request.POST.get('comm_id') #None

		if comm_id:
			SubComment(post=post,
					user = request.user,
					comm = comm,
					comment = Comment.objects.get(id=int(comm_id))
				).save()
		else:
			Comment(post=post, user=request.user, comm=comm).save()


	comments = []
	for c in Comment.objects.filter(post=post):
		comments.append([c, SubComment.objects.filter(comment=c)])
	
	post_author = post.auther

	parms = {
		'comments':comments,
		'post_author':post_author,
		'post':post,
		'pop_post': Post.objects.order_by('-read')[:2],
		}
	return render(request, 'blog-single.html', parms)

def create_blog(request):
    headtitle = "KOWI Fashions | Create Blogs"
    user = request.user
    if user.is_authenticated and user.is_staff == True:
        try:
            employee = EmployeeInfo.objects.get(id=user.id)
            flag = 0
        except ObjectDoesNotExist:
            flag = 1
        if flag == 0:
            try:
                auther = Author.objects.get(user=user)
            except ObjectDoesNotExist:
                return HttpResponse('Ask the Admin to become a Author First!')
            if request.method == 'POST' and request.FILES['myfile']:
                myfile = request.FILES['myfile']
                fs = FileSystemStorage()
                thumbnail = fs.save(myfile.name, myfile)
                title = request.POST['title']
                overview = request.POST['overview']
                slug = request.POST['slug']
                body_text = request.POST['body_text']
                publish = request.POST['publish']
                Post.objects.create(title=title,overview=overview,slug=slug,body_text=body_text,auther=auther,thumbnail=thumbnail,publish=publish)
            parms = {
                'headtitle':headtitle,
                'employee':employee,
            }
            return render(request,'createblog.html',parms)
        elif flag == 1:
            messages.error(request,'Complete Profile First')
            return redirect(eupdate)
    else:
        messages.error(request,'Login First')
        return redirect('elogin')
    return render(request,'createblog.html',{'title':title})

def manageblog(request):
    title = "KOWI FASHIONS | MANAGE BLOGS"
    user = request.user
    if user.is_authenticated and user.is_staff == True:
        try:
            employee = EmployeeInfo.objects.get(id=user.id)
            flag = 0
        except ObjectDoesNotExist:
            flag = 1
        if flag == 0:
            try:
                author = Author.objects.get(user=user)
            except ObjectDoesNotExist:
                return HttpResponse('Ask the Admin to become a Author First!')
            posts = Post.objects.filter(auther=author)
            parms = {
                'title':title,
                'posts':posts,
            }
            return render(request,'manageblog.html',parms)
        elif flag == 1:
            messages.error(request,'Complete Profile First')
            return redirect(eupdate)
    else:
        messages.error(request,'Login First')
        return redirect('elogin')
    parms = {
        'title':title,
    }
    return render(request,'manageblog.html',parms)

def editblog(request,id):
    headtitle = "KOWI FASHIONS | EDIT BLOG"
    user = request.user
    if user.is_authenticated and user.is_staff == True:
        try:
            employee = EmployeeInfo.objects.get(id=user.id)
            flag = 0
        except ObjectDoesNotExist:
            flag = 1
        if flag == 0:
            try:
                author = Author.objects.get(user=user)
            except ObjectDoesNotExist:
                return HttpResponse('Ask the Admin to become a Author First!')
            try:
                old = Post.objects.get(id=id)
            except ObjectDoesNotExist:
                return HttpResponse('Blog Not Found')
            if request.method == 'POST' and request.FILES['myfile']:
                myfile = request.FILES['myfile']
                fs = FileSystemStorage()
                thumbnail = fs.save(myfile.name, myfile)
                title = request.POST['title']
                overview = request.POST['overview']
                slug = request.POST['slug']
                body_text = request.POST['body_text']
                publish = request.POST['publish']
                Post(id=old.id,title=title,overview=overview,slug=slug,body_text=body_text,auther=author,thumbnail=thumbnail,publish=publish,time_upload=datetime.datetime.now()).save()
                messages.success(request,"Blog Updated!")
            parms = {
                'headtitle':headtitle,
                'old':old,
                'employee':employee,
            }
            return render(request,'editblog.html',parms)
        elif flag == 1:
            messages.error(request,'Complete Profile First')
            return redirect(eupdate)
    else:
        messages.error(request,'Login First')
        return redirect('elogin')
    parms = {
        'headtitle':headtitle,
    }
    return render(request,'editblog.html',parms)

def deleteblog(request,id):
    title = "KOWI FASHIONS | DELETE BLOG"
    user = request.user
    if user.is_authenticated and user.is_staff == True:
        try:
            employee = EmployeeInfo.objects.get(id=user.id)
            flag = 0
        except ObjectDoesNotExist:
            flag = 1
        if flag == 0:
            try:
                author = Author.objects.get(user=user)
            except ObjectDoesNotExist:
                return HttpResponse('Ask the Admin to become a Author First!')
            post = Post.objects.filter(id=id).delete()
            return HttpResponse("Blog Deleted Successfully!")
        elif flag == 1:
            messages.error(request,'Complete Profile First')
            return redirect(eupdate)
    else:
        messages.error(request,'Login First')
        return redirect('elogin')
    parms = {
        'title':title,
    }
    return render(request,'deleteblog.html',parms)

def handlecomments(request,id):
    title = "KOWI FASHIONS | HANDLE COMMENTS"
    user = request.user
    if user.is_authenticated and user.is_staff == True:
        try:
            employee = EmployeeInfo.objects.get(id=user.id)
            flag = 0
        except ObjectDoesNotExist:
            flag = 1
        if flag == 0:
            try:
                author = Author.objects.get(user=user)
            except ObjectDoesNotExist:
                return HttpResponse('Ask the Admin to become a Author First!')
            comments = []
            try:
                post = Post.objects.get(pk=id)
            except:
                raise Http404("Post Does Not Exist")
            for c in Comment.objects.filter(post=post):
                comments.append([c, SubComment.objects.filter(comment=c)])
            parms = {
                'title':title,
                'comments':comments,
                'id':id,
            }
            return render(request,'handlecomments.html',parms)
        elif flag == 1:
            messages.error(request,'Complete Profile First')
            return redirect(eupdate)
    else:
        messages.error(request,'Login First')
        return redirect('elogin')
    parms = {
        'title':title,
    }
    return render(request,'handlecomments.html',parms)

def deletecomment(request,id,cm):
    title = "KOWI FASHIONS | DELETE COMMENT"
    user = request.user
    if user.is_authenticated and user.is_staff == True:
        try:
            employee = EmployeeInfo.objects.get(id=user.id)
            flag = 0
        except ObjectDoesNotExist:
            flag = 1
        if flag == 0:
            try:
                author = Author.objects.get(user=user)
            except ObjectDoesNotExist:
                return HttpResponse('Ask the Admin to become a Author First!')
            comments = []
            try:
                post = Post.objects.get(pk=id)
            except:
                raise Http404("Post Does Not Exist")
            for c in Comment.objects.filter(post=post):
                comments.append([c, SubComment.objects.filter(comment=c)])
            cum = Comment.objects.filter(comm=cm).delete()
            return HttpResponse("Comment is Deleted!")
        elif flag == 1:
            messages.error(request,'Complete Profile First')
            return redirect(eupdate)
    else:
        messages.error(request,'Login First')
        return redirect('elogin')
    parms = {
        'title':title,
    }
    return render(request,'deletecomment.html',parms)

def deletesubcomment(request,id,cm,subc):
    title = "KOWI FASHIONS | DELETE SUB COMMENT"
    user = request.user
    if user.is_authenticated and user.is_staff == True:
        try:
            employee = EmployeeInfo.objects.get(id=user.id)
            flag = 0
        except ObjectDoesNotExist:
            flag = 1
        if flag == 0:
            try:
                author = Author.objects.get(user=user)
            except ObjectDoesNotExist:
                return HttpResponse('Ask the Admin to become a Author First!')
            comments = []
            try:
                post = Post.objects.get(pk=id)
            except:
                raise Http404("Post Does Not Exist")
            for c in Comment.objects.filter(post=post):
                comments.append([c, SubComment.objects.filter(comment=c)])
            cum = SubComment.objects.filter(comm=subc).delete()
            return HttpResponse("Sub Comment is Deleted!")
        elif flag == 1:
            messages.error(request,'Complete Profile First')
            return redirect(eupdate)
    else:
        messages.error(request,'Login First')
        return redirect('elogin')
    parms = {
        'title':title,
    }
    return render(request,'deletesubcomment.html',parms)


def chat_system(request):
    title = "KOWI Fashions | Employee Chat System"
    user = request.user
    if user.is_authenticated and user.is_staff == True:
        try:
            employee = EmployeeInfo.objects.get(id=user.id)
            return render(request,'chat.html',{'title':title,'employee':employee})
        except ObjectDoesNotExist:
            messages.error(request,'Complete Profile First')
            return redirect(eupdate)
    else:
        messages.error(request,'Login First')
        return redirect('elogin')
    return render(request,'chat.html',{'title':title})


from math import radians, cos, sin, asin, sqrt
def dist(lat1, long1, lat2, long2):
    """
Replicating the same formula as mentioned in Wiki
    """
    # convert decimal degrees to radians 
    lat1, long1, lat2, long2 = map(radians, [lat1, long1, lat2, long2])
    # haversine formula 
    dlon = long2 - long1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    # Radius of earth in kilometers is 6371
    km = 6371* c
    return km