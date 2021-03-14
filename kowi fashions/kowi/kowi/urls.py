"""kowi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from kowiapp.views import *
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.conf.urls import url
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index,name="index"),
    path('login/',login,name="login"),
    path('logout/',logoutuser,name="logout"),
    path('elogin/',elogin,name="elogin"),
    path('register/',signup,name="signup"),
    path('eupdate/',eupdate,name="eupdate"),
    path('update/',update,name="update"),
    path('dashboard/',dashboard,name="dashboard"),
    path('edashboard/',edashboard,name="edashboard"),
    path('resetpassword/',auth_views.PasswordResetView.as_view(),name="reset_password"),
    path('resetpasswordsent/',auth_views.PasswordResetDoneView.as_view(),name="password_reset_done"),
    path('reset/<uidb64/<token>/',auth_views.PasswordResetConfirmView.as_view(),name="password_reset_confirm"),
    path('resetpasswordcomplete/',auth_views.PasswordResetCompleteView.as_view(),name="password_reset_complete"),

    url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
]

urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


admin.site.site_header = "KOWI Fashions"
admin.site.site_title = "Admin Area | KOWI Fashions"
admin.site.index_title = "Admin Control | KOWI Fashions"



#1.submit email form
#2.Email sent success message
#3.Link to password reset form in email
#4.Password successfully changed message