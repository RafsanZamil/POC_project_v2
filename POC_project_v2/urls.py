"""
URL configuration for POC_project_v2 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path,include

from blogs.views import PostListAPIVIEW

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', PostListAPIVIEW.as_view(), name='index'),
    path('api/', include('auths.urls')),
    path('api/', include('blogs.urls')),
    path('api/', include('blog_comments.urls')),
    path('api/', include('feed.urls', )),
    path('api/', include('transactions.urls', )),



]
