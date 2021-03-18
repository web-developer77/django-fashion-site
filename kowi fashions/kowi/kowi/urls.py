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
    url('^', include('django.contrib.auth.urls')),
    path('activate/<uidb64>/<token>/',activate, name='activate'),
    path('post/<int:id>/<slug:slug>', post, name = 'post'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('createblog/',create_blog,name="create_blog"),
    path('manageblog/',manageblog,name="manageblog"),
    path('deleteblog/<int:id>/',deleteblog,name="deleteblog"),
    path('editblog/<int:id>/',editblog,name="editblog"),
    path('handlecomments/<int:id>/',handlecomments,name="handlecomments"),
    path('deletecomment/<int:id>/<cm>/',deletecomment,name="deletecomment"),
    path('deletesubcomment/<int:id>/<cm>/<subc>/',deletesubcomment,name="deletesubcomment"),
    path('chat/',chat_system,name="chat_system"),
    url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
]

urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


admin.site.site_header = "KOWI Fashions"
admin.site.site_title = "Admin Area | KOWI Fashions"
admin.site.index_title = "Admin Control | KOWI Fashions"


