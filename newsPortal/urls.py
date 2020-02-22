'''newsPortal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  re_path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  re_path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, re_path
    2. Add a URL to urlpatterns:  re_path('blog/', include('blog.urls'))
'''
from django.contrib import admin
from django.urls import re_path, include
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views
from django.conf.urls import url

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(
        r'^portal_login/',
        auth_views.LoginView.as_view(
            template_name='portalusers/login.html', redirect_authenticated_user=True
        ),
        name='portal-login',
    ),
    re_path(
        r'^portal_logout/',
        auth_views.LogoutView.as_view(template_name='portalusers/logout.html'),
        name='portal-logout',
    ),
    re_path(r'^newsextractor/', include('newsextractor.urls')),
    re_path(r'^$', RedirectView.as_view(url='newsextractor/', permanent=True)),
    url(r'^api-auth/', include('rest_framework.urls')),
    re_path(r'^newstraining/', include('newstraining.urls')),
]
