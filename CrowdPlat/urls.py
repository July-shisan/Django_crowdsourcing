"""CrowdPlat URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from home import views
from django.views.generic.base import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', views.home),
    path('', views.homeView.as_view(), name='home'),
    path('alldeveloper/', views.alldeveloper),
    path('workbench/', RedirectView.as_view(url='http://www.baidu.com')),
    path('resource/', RedirectView.as_view(url='http://www.baidu.com')),
    # path('release/', views.release),
    path('release/', views.releaseView.as_view(), name='release'),
    path('details/', views.details, name='details'),
    path('register/', views.registerView.as_view(), name='register'),
    path('login/', views.loginView.as_view(), name='login'),
    path('logout/', views.logout, name='logout'),
    path('profile/<userId>', views.profile, name='profile'),
    # path('task/', views.task, name='task'),
    path('task/<taskId>', views.task, name='task'),
    path('developer/<deveId>', views.developer, name='deve'),
    path('search', include('haystack.urls')),
    # path('login/', views.login),
]
